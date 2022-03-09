#FROM images.alm.site.sa/library/python:3.7-alpine
FROM kpavlovsky/python3.7
RUN pip install --upgrade pip virtualenv

# Add dependencies for packages lxml, Pillow and matplotlib
#RUN apk add --update --no-cache g++ gcc libxslt-dev freetype-dev libpng-dev postgresql-libs musl-dev postgresql-dev jpeg-dev zlib-dev
#RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc && pip3 install --upgrade pip
# RUN apt-get --update --no-cache g++ gcc libxslt-dev freetype-dev libpng-dev postgresql-libs musl-dev postgresql-dev jpeg-dev zlib-dev

# RUN apt-get python3-dev openssl-dev libffi-dev gcc && pip3 install --upgrade pip
# RUN apk --no-cache add lapack libstdc++ && apk --no-cache add --virtual .builddeps g++ gcc gfortran musl-dev lapack-dev py3-scipy make perlap
# RUN echo "http://mirror.leaseweb.com/alpine/edge/community" >> /etc/apk/repositories
# RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
# RUN apt-get --virtual .build-deps \
#     --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
#     --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
#     gcc libc-dev geos-dev geos && \
#     runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
#     | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#     | xargs -r apk info --installed \
#     | sort -u)" && \
#     apk add --virtual .rundeps $runDeps
# install openblas

RUN mkdir /code
WORKDIR /code

RUN virtualenv -p python3.7 env
ENV VIRTUAL_ENV env

ADD requirements.txt /code/

ADD . /code/

RUN mkdir -p /code/static
# RUN source env/bin/activate
# RUN pip install sciPy
RUN pip install -r requirements.txt
RUN pip install django-redis
#c
#COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]
