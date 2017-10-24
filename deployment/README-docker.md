# Deploying with docker

**Note:** This documentation is intentionally generic so that it can
be copy-pasted between projects - do not put project specific details here.

This document explains how to do various sysadmin related tasks when your
site has been deployed under docker. These deployment modes are supported:

* **production**: no debug etc is enabled, has its own discrete database. Configure
  your production environment in core.settings.prod_docker - this
  DJANGO_SETTINGS_MODULE is used when running in production mode.
* **staging**: Configure your staging environment in core.settings.staging_docker -
  this DJANGO_SETTINGS_MODULE is used when running in production mode.

# Build your docker images and run them

## Production

You can simply run the provided script and it will build and deploy the docker
images for you in **production mode**.

```
cd deployment
# allow pg volume to be written to
sudo chmod -R a+rwX pg/postgres_data/
make deploy
sudo chmod -R a+rwX static
```

Now point your browser at the ip of the web container on port 8080 or to the
host port mapping as defined in the docker-compose.yml file.


To make a superuser account do:

```
make shell
python manage.py createsuperuser
exit
```

## Staging

The procedure is exactly the same as production, but you should preceed
each command with 'staging' e.g. ``make staging-deploy``.

**Note:** VERY IMPORTANT - for staging deployment you should use a **separate
git checkout**  from the production checkout as the code from the git checkout
is shared into the source tree.

## Using make

The following key make commands are provided for production:

* **build** - build production containers
* **run** - builds then runs db and uwsgi services
* **collectstatic** - collect static in production instance
* **migrate** - run django migrations in production instance

Additional make commands are provided in the Makefile - please see there
for details.

#### Arbitrary commands

Running arbitrary management commands is easy


## Setup nginx reverse proxy

You should create a new nginx virtual host - please see
``*-nginx.conf`` in the deployment directory for examples. There is
one provided for production and one for staging.

Simply add the example file (renaming them as needed) to your
``/etc/nginx/sites-enabled/`` directory and then modify the contents to
match your local filesystem paths. Then use

```
sudo nginx -t
```

To verify that your configuration is correct and then reload / restart nginx
e.g.

```
sudo /etc/init.d/nginx restart
```
### Run  project in development environment

Firstly you need to be in the project **deployment** directory.

```
cd /path/to/feti/deployment/
``` 

Then after you may need to start the containers independently with the commands below, if your docker setup requires sudo privileges do include it.

```
sudo docker start feti_rabbitmq_1
sudo docker start feti_worker_1
sudo docker start feti-dev-web
```
Then to start the docker development environment. 

```
make devweb
```
This should allow you to start the debug server within pycharm.
But **elasticsearch** engine need to be aware of the current data index to search from, with that in mind run the following commands if your data search is not working.

Assuming you have the **.dmp** database dump file, copy it under the following project directory

```
feti/deployment/backups/
```
Having done so, you need to populate your empty database with some sample data from the dump file, to do so run the following command from within the **deployment** directory

```
make dbrestore
```
Then after you can rebuild the elasticsearch data index to search from as below (from within the **deployment** directory)

```
make rebuildindex
make rebuildindex-devweb
```
After that rebuild the search from the project home page should now work just fine. Enjoy! 


### Managing containers

Please refer to the general [docker-compose documentation](http://docs.docker.com/compose/)
for further notes on how to manage the infrastructure using docker-compose.

# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing the ``docker-compose*.yml``
files.
