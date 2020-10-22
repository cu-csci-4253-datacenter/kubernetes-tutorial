FROM python:3.9-alpine

RUN  pip3 install flask flask-wtf redis Flask-Debug

RUN  mkdir /app
COPY	app /app

EXPOSE	5000
WORKDIR /
CMD	FLASK_APP=app flask run -h 0.0.0.0
