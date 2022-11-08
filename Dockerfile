# pull official base image
FROM python:3.10.8-alpine

# set work directory
WORKDIR /usr/src/app
RUN mkdir -p /home/app


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles && mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]