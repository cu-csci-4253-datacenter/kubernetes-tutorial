FROM ubuntu:20.04

RUN	DEBIAN_FRONTEND=noninteractive apt-get update -y && \
	apt-get install -yq --no-install-recommends \
	   git python3 python3-pip curl

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
