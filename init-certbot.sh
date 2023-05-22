#!/bin/bash
#  THIS script downloads certificates for you production instance
#  MAKE sure to add you domain name(s) to the variable in line 10
#     domains should list your dns registered name first, others after, (ex www.primaryDomainName)
#  IF USING CLOUDFLARE make sure Full (strict) is enabled under SSL

################################################################################
# PUT YOUR DOMAIN NAMES IN #####################################################
################################################################################
domains=(multimodalinsights.com www.multimodalinsights.com) # <- HERE          #
################################################################################
data_path="./data/certbot"

if [ -d "$data_path" ]; then
  read -p "Existing data found for $domains. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi
echo "### Creating certificate for $domains ..."

# open ports
sudo fuser -k 443/tcp
sudo fuser -k 80/tcp

# install 
apt-get update
sudo apt-get install certbot
apt-get install python3-certbot-nginx

# nginx load
nginx -t && nginx -s reload

# Prepare the certbot command with -d arguments
certbot_command="sudo certbot --nginx"

# Iterate over the domain names and add them as -d arguments
for domain in "${domains[@]}"; do
  certbot_command+=" -d $domain"
done

# Execute the certbot command
eval "$certbot_command"

# copy certs into application directory
cp -Lr /etc/letsencrypt/live $data_path/conf

# open ports
sudo fuser -k 443/tcp
sudo fuser -k 80/tcp