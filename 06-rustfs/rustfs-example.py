#!/usr/bin/env python3
"""Periodically demonstrate basic S3 operations against a RustFS endpoint."""
import os
import sys
import time
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

endpoint = os.getenv("RUSTFS_ENDPOINT", "http://localhost:9000")
access_key = os.getenv("AWS_ACCESS_KEY_ID", "rustfs-lab-user")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "replace-this-demo-secret")
bucket_name = os.getenv("RUSTFS_BUCKET", "rustfs-demo-bucket")

client = boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)

# These files are copied into the example image by the Dockerfile.
files_to_upload = [Path("./rustfs-example.py"), Path("./README.md")]

while True:
    try:
        existing = {item["Name"] for item in client.list_buckets().get("Buckets", [])}
        if bucket_name not in existing:
            print(f"Creating bucket: {bucket_name}")
            client.create_bucket(Bucket=bucket_name)

        print("Buckets:")
        for item in client.list_buckets().get("Buckets", []):
            print(f"  {item['Name']} (created {item.get('CreationDate')})")

        print(f"Objects in {bucket_name} before upload:")
        response = client.list_objects_v2(Bucket=bucket_name)
        for item in response.get("Contents", []):
            print(f"  {item['Key']} ({item['Size']} bytes)")

        for path in files_to_upload:
            if path.is_file():
                print(f"Uploading {path.name}")
                client.upload_file(str(path), bucket_name, path.name)

        print(f"Objects in {bucket_name} after upload:")
        response = client.list_objects_v2(Bucket=bucket_name)
        for item in response.get("Contents", []):
            print(f"  {item['Key']} ({item['Size']} bytes)")

    except (BotoCoreError, ClientError) as exc:
        print(f"RustFS/S3 request failed: {exc}", file=sys.stderr)

    sys.stdout.flush()
    time.sleep(30)
