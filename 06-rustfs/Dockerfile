FROM python:3.12-slim

RUN pip install --no-cache-dir boto3
COPY ./rustfs-example.py /rustfs-example.py
COPY ./README.md /README.md
WORKDIR /
CMD ["python", "/rustfs-example.py"]
