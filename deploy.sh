#!/bin/bash

echo "Uploading code..."
rsync -avz --exclude-from .gitignore  . root@ruxlab.ru:/www/alexa-bus-stop.rux.vc/app

echo "Fixing rights.."
ssh root@ruxlab.ru "chown www-data:www-data -R /www/alexa-bus-stop.rux.vc/app"

echo "Restarting service.."
ssh root@ruxlab.ru "service uwsgi restart"