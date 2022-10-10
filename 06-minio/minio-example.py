#!/usr/bin/env python3

from minio import Minio

client = Minio('localhost:9000',
               secure=False,
               access_key='rootuser',
               secret_key='rootpass123')

bucketname='my-bucketname'
files_to_add=[ "minio-example.py", "minio-config.yaml"]

if not client.bucket_exists(bucketname):
    print(f"Create bucket {bucketname}")
    client.make_bucket(bucketname)

buckets = client.list_buckets()

for bucket in buckets:
    print(f"Bucket {bucket.name}, created {bucket.creation_date}")
    
print(f"Objects in {bucketname} are originally:")
for thing in client.list_objects(bucketname, recursive=True):
    print(thing.object_name)
    
try:
    for filename in files_to_add:
        print(f"Add file {filename} as object {filename}")
        client.fput_object(bucketname, filename, f"./{filename}")
except ResponseError as err:
    print("Error when adding files the first time")
    print(err)

print(f"Objects in {bucketname} are now:")
for thing in client.list_objects(bucketname, recursive=True):
    print(thing.object_name)