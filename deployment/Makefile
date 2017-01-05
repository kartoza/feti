SHELL := /bin/bash
PROJECT_ID := feti
DOMAIN := staging.feti.kartoza.com

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------

default: web

run: build permissions web migrate collectstatic

deploy: run
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bringing up fresh instance "
	@echo "You can access it on http://localhost:63100"
	@echo "------------------------------------------------------------------"

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build uwsgi

web:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d web
	@# Dont confuse this with the dbbackup make command below
	@# This one runs the postgis-backup cron container
	@# We add --no-recreate so that it does not destroy & recreate the db container
	@docker-compose -p $(PROJECT_ID) up --no-recreate --no-deps -d dbbackups

permissions:
	# Probably we want something more granular here....
	# Your sudo password will be needed to set the file permissions
	# on logs, media, static and pg dirs
	@if [ ! -d "logs" ]; then mkdir logs; fi
	@if [ ! -d "media" ]; then mkdir media; fi
	@if [ ! -d "static" ]; then mkdir static; fi
	@if [ ! -d "backups" ]; then mkdir backups; fi
	@if [ -d "logs" ]; then sudo chmod -R a+rwx logs; fi
	@if [ -d "media" ]; then sudo chmod -R a+rwx media; fi
	@if [ -d "static" ]; then sudo chmod -R a+rwx static; fi
	@if [ -d "pg" ]; then sudo chmod -R a+rwx pg; fi
	@if [ -d "backups" ]; then sudo chmod -R a+rwx backups; fi

db:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running db in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d db

nginx:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running nginx in production mode"
	@echo "Normally you should use this only for testing"
	@echo "In a production environment you will typically use nginx running"
	@echo "on the host rather if you have a multi-site host."
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d nginx
	@echo "Site should now be available at http://localhost"

migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in production mode"
	@echo "------------------------------------------------------------------"
	@#http://stackoverflow.com/questions/29689365/auth-user-error-with-django-1-8-and-syncdb-migrate
	@#and
	@#http://stackoverflow.com/questions/3143635/how-to-ignore-mv-error
	@# We add the '-' prefix to the next line as the migration may fail
	@# but we want to continue anyway.
	@#We need to migrate accounts first as it has a reference to user model
	-@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py migrate auth
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py migrate

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in production mode"
	@echo "------------------------------------------------------------------"
	#@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# uwsgi container it seems so I use docker exec here
	@docker exec -t -i $(PROJECT_ID)-uwsgi python manage.py collectstatic --noinput

makemigrations:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running makemigrations in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py makemigrations

updatelongdescription:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running updatelongdescription in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py updatelongdescription

updatecampuscourseentries:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running updatecampuscourseentries in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py updatecampuscourseentries

rebuildindex:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running rebuild_index in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py rebuild_index

updateindex:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running update_index in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py update_index

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in production mode"
	@echo "------------------------------------------------------------------"

	@docker-compose -p $(PROJECT_ID) kill

rm: dbbackup rm-only

rm-only: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing production instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) rm

logs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing uwsgi logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs uwsgi

nginxlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing nginx logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs web

shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run --rm uwsgi /bin/bash

dbshell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in production database"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-db psql -U docker -h localhost gis

sentry:
	@echo
	@echo "--------------------------"
	@echo "Running sentry production mode"
	@echo "--------------------------"
	@docker-compose  -p $(PROJECT_ID) up -d sentry
	# @dipall

maillogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing smtp logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)_smtp_1 tail -f /var/log/mail.log

mailerrorlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing smtp error logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)_smtp_1 tail -f /var/log/mail.err

mapproxylogs:
	@echo
	@echo "--------------------------"
	@echo "Showing mapproxy logs in production mode"
	@echo "--------------------------"
	@docker-compose -p $(PROJECT_ID) logs mapproxy

seed:
	@echo
	@echo "--------------------------"
	@echo "Seeding mapproxy in production mode"
	@echo "--------------------------"
	@docker-compose -p $(PROJECT_ID) run mapproxy /usr/local/bin/mapproxy-seed -f /mapproxy/mapproxy.yaml /mapproxy/seed.yaml

map:
	@echo
	@echo "--------------------------"
	@echo "Getting current 6 hour slot as pdf map"
	@echo "Make sure you have started the services with make run first"
	@echo "--------------------------"
	# Experimental way we had of getting it using QGIS Server
	#wget -O map.pdf "http://172.17.0.6/cgi-bin/qgis_mapserv.fcgi?map=/web/jk-floods.qgs&SERVICE=wms&LAYERS=Rw&REQUEST=GetPrint&TEMPLATE=6Hour&map0:EXTENT=11862318.594,-714081.378,11922154.957,-675870.096&map0:ROTATION=0&FORMAT=pdf&DPI=300"
	docker exec -t -i $(PROJECT_ID)_cron xvfb-run python /home/web/cron-scripts/pdf_report_generator.py
	@echo "--------------------------"
	@echo "PDF Generated - written to reports"
	@echo "--------------------------"
	evince reports/jk-floods-latest.pdf

qgis:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running QGIS desktop in production mode"
	@echo "Make sure you have started the services with make run first"
	@echo "------------------------------------------------------------------"
	@xhost +; docker run --rm --name="qgis-desktop-2-8" \
	-i -t \
	--link $(PROJECT_ID)_db:db \
	--link $(PROJECT_ID)_qgisserver:qgisserver \
	--link $(PROJECT_ID)_mapproxy:mapproxy \
	--volumes-from $(PROJECT_ID)_qgisserver \
	-v ${HOME}:/home/$(USER) \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY=unix$(DISPLAY) \
	kartoza/qgis-desktop:2.8.0; xhost -

reload:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Reload django project in production mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-uwsgi uwsgi --reload  /tmp/django.pid

runcertbot:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Run certbot to get certificate"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-uwsgi /certbot-auto --non-interactive --agree-tos certonly --webroot --email dimas@kartoza.com -w /var/www/webroot -d $(DOMAIN)

superuser:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Creating a superuser in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py createsuperuser

dbrestore:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Restore dump from backups/latest.dmp in production mode"
	@echo "------------------------------------------------------------------"
	@# - prefix causes command to continue even if it fails
	-@docker exec -t -i $(PROJECT_ID)-db su - postgres -c "dropdb gis"
	@docker exec -t -i $(PROJECT_ID)-db su - postgres -c "createdb -O docker -T template_postgis gis"
	@docker exec -t -i $(PROJECT_ID)-db pg_restore /backups/latest.dmp | docker exec -i $(PROJECT_ID)-db su - postgres -c "psql gis"

dbbackup:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Create `date +%d-%B-%Y`.dmp in production mode"
	@echo "Warning: backups/latest.dmp will be replaced with a symlink to "
	@echo "the new backup."
	@echo "------------------------------------------------------------------"
	@# - prefix causes command to continue even if it fails
	@# Explicitly don't use -it so we can call this make target over a remote ssh session
	@docker exec $(PROJECT_ID)-dbbackups /backups.sh
	@docker exec $(PROJECT_ID)-dbbackups cat /var/log/cron.log | tail -2 | head -1 | awk '{print $4}'
	-@if [ -f "backups/latest.dmp" ]; then rm backups/latest.dmp; fi
	# backups is intentionally missing from front of first clause below otherwise symlink comes
	# out with wrong path...
	@ln -s `date +%Y`/`date +%B`/PG_$(PROJECT_ID)_gis.`date +%d-%B-%Y`.dmp backups/latest.dmp
	@echo "Backup should be at: backups/`date +%Y`/`date +%B`/PG_$(PROJECT_ID)_gis.`date +%d-%B-%Y`.dmp"\

update-cache:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running command to make cache in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py generate_campus_index
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py generate_course_index
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py generate_occupation_index

scraping:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running command to make cache in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_campus
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_course
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_occupation

scrape-occupation:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running command to scrap occupation data from internet"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_occupation > occupation_scrape.log

clean-scraping:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running command to make cache in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_campus True
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_course True
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py scraping_occupation True

workerlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing celery worker logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs worker

worker:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running worker production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d worker

# ----------------------------------------------------------------------------
#    DEVELOPMENT C O M M A N D S
# --no-deps will attach to prod deps if running
# after running you will have ssh and web ports open (see dockerfile for no's)
# and you can set your pycharm to use the python in the container
# Note that pycharm will copy in resources to the /root/ user folder
# for pydevd etc. If they dont get copied, restart pycharm...
# ----------------------------------------------------------------------------

devweb: db
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in DEVELOPMENT mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up --no-deps -d devweb

build-devweb: db
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building devweb"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build devweb

rebuildindex-devweb:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running rebuild_index in DEVELOPMENT mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run devweb python manage.py rebuild_index

updateindex-devweb:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running update_index in DEVELOPMENT mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run devweb python manage.py update_index

import-map-administrative:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Import map administrative"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py import_countries
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py import_district
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py import_municipalities

# --------------- help --------------------------------

help:
	@echo "* **build** - builds all required containers."
	@echo "* **build-devweb** - build the development container. See [development notes](README-dev.md)."
	@echo "* **collectstatic** - run the django collectstatic command."
	@echo "* **create-machine** ."
	@echo "* **db** - build and run the db container."
	@echo "* **dbbackup** - make a snapshot of the database, saving it to deployments/backups/YYYY/MM/project-DDMMYYYY.dmp. It also creates a symlink to backups/latest.dmp for the latest backup."
	@echo "* **dbbash** - open a bash shell inside the database container."
	@echo "* **dblogs** - view the database logs."
	@echo "* **dbrestore** - restore deployment/backups/latest.dmp over the active database. Will delete any existing data in your database and replace with the restore, so **use with caution**."
	@echo "* **dbschema** - dump the current db schema (without data) to stdio. Useful if you want to compare changes between instances."
	@echo "* **dbshell** - get a psql prompt into the db container. "
	@echo "* **dbsnapshot** - as above but makes the backup as deployment/snapshot.smp - replacing any pre-existing snapshot."
	@echo "* **dbsync** - use this from a development or offsite machine. It will rsync all database backups from deployment/backups to your offsite machine."
	@echo "* **default** ."
	@echo "* **deploy** ."
	@echo "* **devweb** - create an ssh container derived from uwsgi that can be used as a remote interpreter for PyCharm. See [development notes](README-dev.md)."
	@echo "* **enable-machine** - "
	@echo "* **kill** - kills all running containers. Does not remove them."
	@echo "* **logs** - view the logs of all running containers. Note that you can also view individual logs in the deployment/logs directory."
	@echo "* **mailerrorlogs** - View the error logs from the mail server."
	@echo "* **maillogs** - view the transaction logs from the mail server."
	@echo "* **mediasync** - use this from a development or offsite machine. It will rsync all media backups from deployment/media to your offsite machine."
	@echo "* **migrate** - run any pending migrations. "
	@echo "* **nginx** - builds and runs the nginx container."
	@echo "* **nginxlogs** - view just the nginx activity logs."
	@echo "* **permissions** - Update the permissions of shared volumes. Note this will destroy any existing permissions you have in place."
	@echo "* **reload** - reload the uwsgi process. Useful when you need django to pick up any changes you may have deployed."
	@echo "* **rm** - remove all containers."
	@echo "* **rm-only** - remove any containers without trying to kill them first. "
	@echo "* **run** - builds and runs the complete orchestrated set of containers."
	@echo "* **sentry** - **currently not working I think.** The idea is to spin up a sentry instance together with your app for fault reporting."
	@echo "* **shell** - open a bash shell in the uwsgi (where django runs) container."
	@echo "* **superuser** - create a django superuser account."
	@echo "* **update-migrations** - freshen all migration definitions to match the current code base."
	@echo "* **web** - same as **run** - runs the production site."
