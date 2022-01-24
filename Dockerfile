#FROM images.alm.site.sa/library/python:3.7-alpine
FROM python:3.7-alpine

RUN pip install --upgrade pip virtualenv

# Add dependencies for packages lxml, Pillow and matplotlib
#RUN apk add --update --no-cache g++ gcc libxslt-dev freetype-dev libpng-dev postgresql-libs musl-dev postgresql-dev jpeg-dev zlib-dev
#RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc && pip3 install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev freetype-dev libpng-dev postgresql-libs musl-dev postgresql-dev jpeg-dev zlib-dev

RUN apk add python3-dev openssl-dev libffi-dev gcc && pip3 install --upgrade pip

RUN mkdir /code
WORKDIR /code

RUN virtualenv -p python3.7 env
ENV VIRTUAL_ENV env

ADD requirements.txt /code/

ADD . /code/

RUN mkdir -p /code/static
RUN source env/bin/activate
RUN pip install -r requirements.txt
RUN pip install django-redis
#c
#COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]
