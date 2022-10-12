FROM python:3.10-slim

RUN pip3 install minio

COPY ./minio-example.py /
COPY ./minio-config.yaml /
WORKDIR /
CMD  python3 /minio-example.py