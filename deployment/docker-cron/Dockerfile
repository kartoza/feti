#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on fedora
FROM kartoza/qgis-desktop:2.8.0
MAINTAINER Tim Sutton<tim@kartoza.com>

RUN yum install -y cronie-anacron.x86_64 postgis.x86_64
RUN yum install -y xorg-x11-server-Xvfb.x86_64

ENV PYTHONPATH=$PYTHONPATH:/usr/share/qgis/python/
ADD crontab /var/spool/cron/root

# Change the timezone, to the timezone
RUN cp /usr/share/zoneinfo/Asia/Jakarta  /etc/localtime

CMD crond -p -s && Xvfb :99 -ac -screen 0 1280x1024x24
