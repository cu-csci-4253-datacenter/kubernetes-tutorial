#!/bin/sh

cd /app

export FLASK_APP=flaskr

echo "Existing directory at " $(pwd)

if [ -f instance/flaskr.sqlite ]
then
    echo "Use existing database"
else
    flask init-db
fi

nohup flask run -h 0.0.0.0 -p $FLASK_PORT
