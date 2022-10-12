#!/bin/sh

helm3 repo add bitnami https://charts.bitnami.com/bitnami
helm3 install -f ./minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio
sleep 10
kubectl port-forward --namespace minio-ns svc/minio-proj 9000:9000 &
kubectl port-forward --namespace minio-ns svc/minio-proj 9001:9001 &
