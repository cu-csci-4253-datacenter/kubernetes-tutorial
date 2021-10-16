FROM python:3.8

RUN  	cd /tmp && \
	git clone https://github.com/pallets/flask && \
	mv flask/examples/tutorial /app && \
	rm -rf /tmp/flask && \
	cd /app && \
	python3 setup.py install && \
	pip3 install -e .

COPY	app.sh /app

ENV	FLASK_PORT 5000

CMD	[ "/bin/sh", "-x", "/app/app.sh" ]
