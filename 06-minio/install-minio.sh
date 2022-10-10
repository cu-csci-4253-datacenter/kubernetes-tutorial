#!/bin/sh

helm repo add bitnami https://charts.bitnami.com/bitnami
helm install -f ./minio-config.yaml myminio bitnami/minio