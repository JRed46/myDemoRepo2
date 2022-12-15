# Audio Server Docker
This repository is version 3 of the mental wellness server application. Its primary objective is to serve relaxing audio files that help improve mental states. This is a custom wsgi Django application that is dockerized and deployed in production with nginx, gunicorn, and postgres. There are also intructions to run Django's development server for front end work.

## Table of Contents
1. [Repo Overview](#overview)
    1. [audio_server](#audio_server)
    2. [nginx](#nginx)
    3. [audio_app](#audio_app)
    4. [other](#other)
2. [Getting Started](#getting_started)
    1. [Local Front End Development](#front_end)
    2. [Docker Dev Build](#docker_dev)
    2. [Docker Prod Build](#docker_prod)
3. [Server Infrastructure Overview](#infrastructure)
    1. [Docker Production Server](#docker_prod)
    2. [Reference Virtual Machine Deployment](#reference_vm)
    3. [Development Server](#dev_server)
4. [Contribution Guidlines](#guidelines)
5. [Contributors](#contributors)



## Repo Overview <a name="overview"></a>
### audio_server <a name="audio_server"></a>
This is the standard django configuration folder for the project. It contains various settings, static files, and urls. The static subfolder contains a css, js, and img folder. To add a script to the project, create `{yourscript}.js` and add it to the js subfolder. This file can be added to a template with `src="{% static 'js/{yourscript}.js' %}"`. CSS and images can be added similarly. There is no need to specify a new url for a new static file. The templates subfolder contains html templates for the project. Currently, this folder contains only `base.html`. When making a new page for the project, it should extend from this template, to keep things like the topnav consistent across pages. `urls.py` specifies the url routing for each of the view functions in the project. Unlike new static files, make sure to update this file when creating new views.

### nginx <a name="nginx"></a>
This contains the configuration settings for the production nginx build. The `nginx.conf` file specifies how nginx should handle requests. Most requests are passed along to the django wsgi server (listening on port 8000, specified in `docker-compose.yml`), which will then map the url of the request to a view function based on our `urls.py` file. The special cases are requests made to the /static/ and /media/ urls, which are served directly by nginx to reduce load on the django wsgi server. The Dockerfile in this repo simply specifies to use our custom conf file. 

### audio_app <a name="audio_app"></a>
This is a custom django app with the views, models, and templates for the front end of the web application. Note if this project structure were to be reused for another project, we could replace this app with the project specific app(s) of the other project. The contigency is that the application is only using a wsgi server- additional work would be needed to configure an asgi server if, for example, the other project uses django channels; either way this repo would still be a good starting point. 

### Other <a name="other"></a>
- `.env.dev`: specifies environment variables for the development docker build
- `.gitignore`: standard gitignore file for django projects
- `docker-compose.yml`: intructions for the host machine to use to create the relevent docker containers for the project
- `Dockerfile`: set of instructions to initialize the django wsgi server, used by the "web" container in `docker-compose.yml`
- `entrypoint.sh`: script with a couple commands that is run after the containers have started
- `manage.py`: standard executable django file enabling project management commands.
- `README.md`: project description
- `requirements.txt`: project dependecies attained from using pip freeze. Used by docker or by the local development server for front end development. 



## Getting Started <a name="getting_started"></a>
This application can run in 3 modes: (1) local front end devlopment (2) dev docker (3) prod docker. (1) runs a lightweight development server which is a django built-in. It creates a sqlite datatbase and serves static/media files all on port 8000. It's useful for developing views and styling where you are constantly changing files and want to view the change in your browser since it initializes quickly. It runs very differently than the production server, so it should only be used for front end development usage. Consider this mode's functionality similar to just opening raw html files in your browser, where the local server will pull in static files and allow you to render templates with a dummy database. (2) runs a full production grade dockerized build of the project with a reverse proxy and postgres database over http that can run locally. (3) Runs the build on https, generating and automatically renewing certificates

### (1) Local Front End Development <a name="front_end"></a>

#### Step 1, Clone Repo, Prepare To Setup
- Check you have [python](https://www.python.org/downloads/) and [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) installed on your system. Using VSCode is recommended. 
```console
git clone https://bitbucket.org/fletcher2014/wellness_server_v3/src/master/
```

#### Step 2, Create and activate virtual environment 
- Navigate to the folder you just cloned
- Create the Virtual Environment (only do once)
    - Windows: *note: depending on your setup you may need to replace "python" with "py"* 
        ```console
        pip install virtualenv
        ```
        ```console
        python -m venv wellness_venv
        ```
    - Mac:
        ```console
        pip3 install virtualenv
        ```
        ```console
        python3 -m venv wellness_venv
        ```
- Activate the Virtual Environment
    - Windows:
        ```console
        wellness_venv\scripts\activate
        ```
    - Mac:
        ```console
        source wellness_venv/bin/activate
        ```
        

#### Step 3, Install Python dependencies 
- Windows:
    ```console
    pip install -r requirements.txt
    ```
- Mac:
    ```console
    pip3 install -r requirements.txt
    ``` 

#### Step 4, Create local development SQLite database, run migrations
- Windows:
    ```console
    python manage.py migrate
    ```
- Mac:
    ```console
    python3 manage.py migrate
    ```

#### Step 5, Run Django dev server
- Windows: 
    ```console
    python manage.py runserver
    ```
- Mac: 
    ```console
    python3 manage.py runserver
    ```
- The wellness server should be running locally at http://127.0.0.1:8000
- Note that the server automatically restarts when you change files, this does not happen with the docker build.
Also note that your browser may cache static files, and you will need to either disable this or clear your browser
cache when changing static files.
- A new folder called mediafiles will automatically be created in this mode in addition to the sqlite database. It will be ignored by git.

### (2) Dev Docker <a name="docker_dev"></a>
Clone the repo and navigate inside of it. Run the docker daemon. This is done most easily by downloading docker desktop and opening the application https://www.docker.com/products/docker-desktop/. For alternatives, see https://docs.docker.com/get-docker/
Before you run `docker-compose`, you may need to change the permissions of `entrypoint.sh`. **make sure you rebuild the docker file with `docker compose build` after you run `chmod`**
#### MacOS and Linux (Unix)
For both MacOS and Linux, run `chmod +x entrypoint.sh`
### Windows
If using Windows Subsystem for Linux (WSL), run the same command as the Linux section. Otherwise, run command line as administrator and execute `icacls entrypoint.sh /reset`, which resets the file permissions. (CURRENTLY UN-TESTED)

#### Running Docker
```console
docker-compose -f docker-compose.dev build
```
```console
docker-compose -f docker-compose.dev up
```

The server is now running at http://127.0.0.1. Note server logs are being printed which is useful for debugging. Print statements from the view functions are printed here in addition to the request logs. Also note the server is running on http://127.0.0.1 and not http://127.0.0.1:8000 like the front end development server. While the wsgi server is running on port 8000, it is not exposed to the web, rather only internally to other docker services. Now, nginx is listending on port 80, the default http port, which is the new gateway to the application.

To execute manual server commands, we need to run the application without printing server logs. Do this with
```console
docker-compose -f docker-compose.dev up -d --build
```
The build will not automatically run database migrations. Do this with:
```console
docker-compose -f docker-compose.dev exec web python manage.py migrate --noinput
```
In general, we can user "docker-compose -f docker-compose.dev exec web python manage.py {command}" to run commands in the containers, where "web" is the name of the wsgi server we specified in docker-compose.yml

### Troubleshooting Guide
When setting up the docker server for the first time, there are some common issues that can happen; this readme will be updated with solutions to these problems as we encounter them

1. The python executable (`docker-compose`) is technically deprecated, but it works for the purposes of this server. If it is out of date, you can update it easily using `pip`. For better alternatives, see point 2
2. The newer method of using `compose` is through docker itself, but this requires the installation of a new plugin (**unless you have Docker Desktop, which is supposed to ship with the `docker compose` command ready to go**). Instead of using `pip`, this plug-in adds `docker compose` as a valid command. To install it, use `sudo apt-get- install docker-compose-plugin` on Ubuntu, and the equivalent command on other Linux distros. For MacOS, this plug-in can be installed with [homebrew](https://brew.sh/), with the command `brew install docker-compose`. Note that there might be another step required for MacOS, as detailed [here](https://github.com/docker/compose/issues/8630#issuecomment-1169537632) There is no `docker-compose-plugin` on Windows.See [here](https://github.com/docker/compose/issues/8630#issuecomment-1141930536) for the github issue relating to this.
3. Another issue that is easy to run into is nginx (or possibly another component) saying the port is blocked. While you can run `docker-compose up -p PORT_NUMBER` to run on a different port, it is advisable to figure out what is blocking the original port, since that may cause problems in the future. If you are running Ubuntu, the most [common](https://stackoverflow.com/questions/14972792/nginx-nginx-emerg-bind-to-80-failed-98-address-already-in-use) problem is Apache listening on that port by default. If you are not using or don't need apache to be running on that port, you can kill the process with `sudo /etc/init.d/apache2 stop` on Ubuntu and `sudo apachectl stop` on other Linux Distros. Please be careful with sudo commands, and always run them at your own peril (the command itself is innocuous, but it is always important to keep that advice in mind). If that does not work, you may need to look up "how to see what is binding port 80 on Windows/Mac/Linux", find the process, and kill it (if it is not important). Sadly, the number of methods to this are too many to enumerate, but it should be a straightforward process.

### (3) Prod Docker <a name="docker_prod"></a>
For a new server, install docker on a linux machine by following the instructions at https://docs.docker.com/engine/install/ubuntu/. To clone the git repo, you can generate an ssh key and configure it in your bitbucket account following these instructions: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/BitBucket-SSH-Key-Example. There is an additional step to generate the first ssl certificates, which can be done by running  ./init-letsencrypt.sh. This script is from https://github.com/wmnnd/nginx-certbot and has been configured for our domain. After running these steps, you can build the code and certificates will be automatically renewed every 12 hours by the Certbot container.

On the configured server, note the production docker-compose file is just docker-compose.yml, not docker-compose.dev.yml. This version will not build on your local machine due to the ssl certificate script. Nonetheless, commands are the same for this version as the dev version, simply removing the "-f docker-compose.prod.yml" substring from the commands. 

Build and spin up in silent mode
```console
docker-compose up -d --build
```
The build will not automatically run database migrations. Do this with:
```console
docker-compose exec web python manage.py migrate --noinput
```


## Server Infrastructure Overview <a name="infrastructure"></a>
### Dockerized Production Server <a name="docker_prod"></a>
The production server consists of an Nginx reverse proxy, and Gunicorn WSGI server, and a Postgre SQL database. These components run as docker containers and connect to eachother via internal networking. Port 80/443 is exposed externally for http/https requests where nginx is listening. Static and media requests are served directly, and other requests are passed to the guinicorn wsgi server listening on port 8000. The database is available to all services on port 5432.

<img src="audio_server/static/img/dockerServerDiagram.png" alt="devServerDiagram" width="600"/>

### Reference VM Server <a name="reference_vm"></a>
For reference, below is a comparable deployment structure in a more traditional virtual machine deployment. 
<img src="audio_server/static/img/vmServerDiagram.png" alt="devServerDiagram" width="600"/>


### Development Server <a name="dev_Server"></a>
The development server only runs a lightweight wsgi server. This runs our view functions in a virtual environment in addition to serving static and media and connecting to a sqlite database. 

<img src="audio_server/static/img/devServerDiagram.png" alt="devServerDiagram" width="600"/>

## Contribution Guidelines <a name="guidelines"></a>
### Branches
- Please work on a branch and get pull requests reviewed by a peer before merging
### Test Cases
- Run unit tests in the Development Server virtual environment. 
    - Windows:
        ```console
        wellness_venv\scripts\activate
        ```
        ```console
        python manage.py test
        ```
    - Mac:
        ```console
        source wellness_venv/bin/activate
        ```
        ```console
        python3 manage.py test
        ```
- TODO: organize tests
- For now just make these pass when you change the code base and write new ones for new functionalities
        

## Contributors <a name="contributors"></a>
Fall 2022

- Richard Fletcher, Advisor
- Michael Cantow, MEng
- Sami Amer, UROP
- Sonia Uwase, UROP