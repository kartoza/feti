#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/django-base
MAINTAINER Tim Sutton<tim@kartoza.com>

#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get update -y; apt-get -y --force-yes install yui-compressor

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

# Problems with current version on pip
RUN pip install git+https://github.com/django-haystack/django-haystack

# Add patch for raven per issue:
# https://github.com/getsentry/raven-python/pull/595
WORKDIR /home
RUN wget -c "https://raw.githubusercontent.com/getsentry/raven-python/04085c781621b47cfd47632531341fa7b2e9a956/raven/contrib/django/apps.py"
RUN mv apps.py /usr/local/lib/python2.7/site-packages/raven/contrib/django/apps.py
# Add latest haystack. uncomment this if we have v 2.4.0
#RUN wget -c "https://github.com/django-haystack/django-haystack/archive/v2.4.0.zip"
#RUN apt-get install unzip
#RUN unzip v2.4.0.zip
#RUN cp -R django-haystack-2.4.0/haystack /usr/local/lib/python2.7/site-packages/
#RUN rm -rf django-haystack-2.4.0 v2.4.0.zip

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
