#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:3.4
MAINTAINER Dimas Ciputra<dimas@kartoza.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get update -y; apt-get -y --force-yes install yui-compressor

# python 3.4 has already installed by os
RUN apt-get install -y python3-pip
RUN apt-get install -y python-gdal
RUN apt-get install -y python-geoip
RUN apt-get install -y npm
RUN apt-get install -y nodejs
RUN apt-get install -y rpl
RUN apt-get -y  --force-yes install yui-compressor
RUN apt-get install -y python3-setuptools

RUN npm -g install yuglify

# Debian is messed up and aliases node as nodejs
# So when yuglify is installed it references the wrong node binary...
# lets fix that here...

RUN rpl "env node" "env nodejs" /usr/local/lib/node_modules/yuglify/bin/yuglify

# Install django requirements
ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

# Download cerbort
RUN wget https://dl.eff.org/certbot-auto
RUN chmod a+x certbot-auto

# Add latest haystack. uncomment this if we have v 2.4.0
#RUN wget -c "https://github.com/django-haystack/django-haystack/archive/v2.4.0.zip"
#RUN apt-get install unzip
#RUN unzip v2.4.0.zip
#RUN cp -R django-haystack-2.4.0/haystack /usr/local/lib/python2.7/site-packages/
#RUN rm -rf django-haystack-2.4.0 v2.4.0.zip


# Install Node js
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get -y --force-yes install nodejs

WORKDIR /home/web/django_project

# Install grunt
RUN npm install -g grunt-cli
COPY deployment/docker/package.json /home/web/django_project/package.json
RUN cd /home/web/django_project && npm install --save-dev grunt grunt-contrib-concat grunt-contrib-uglify
RUN cd /home/web/django_project && npm install --save-dev grunt-contrib-requirejs

COPY django_project /home/web/
ADD uwsgi.conf /uwsgi.conf

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

CMD ["uwsgi", "--ini", "/uwsgi.conf"]
