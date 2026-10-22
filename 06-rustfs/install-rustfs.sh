#!/bin/sh
set -eu

# Install or update RustFS using the official RustFS Helm chart repository.
helm repo add rustfs https://www.charts.rustfs.com
helm repo update
helm upgrade --install rustfs rustfs/rustfs \
  --namespace rustfs-ns \
  --create-namespace \
  --values ./rustfs-config.yaml



echo
echo "RustFS has been submitted to Kubernetes. Check readiness with:"
echo "  kubectl get pods,svc,pvc -n rustfs-ns"
echo "Open the RustFS console at http://localhost:9001"
echo "S3 API available at http://localhost:9000"
echo "Run the following command in a separate terminal:"
echo "kubectl port-forward -n rustfs-ns svc/rustfs-svc 9000:9000 9001:9001"

