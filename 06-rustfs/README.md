# Exploring RustFS Object Storage on Kubernetes

This exercise explores **RustFS**, an S3-compatible object-storage service, and how it can be deployed and accessed from Kubernetes. The lab uses Helm to install RustFS, a namespace to group its resources, persistent volumes to retain objects, port forwarding to reach its interfaces, and a Python S3 client to create buckets and upload objects.

RustFS exposes two useful endpoints:

- **S3 API:** port `9000`, used by applications and S3-compatible clients.
- **Web console:** port `9001`, used to inspect and manage objects in a browser.

See the [RustFS project](https://github.com/rustfs/rustfs), [RustFS documentation](https://docs.rustfs.com/), and [official Helm chart documentation](https://docs.rustfs.com/en/installation/cloud-native).

## 1. Helm and Kubernetes

[Helm](https://helm.sh/) is a package manager for Kubernetes. A Helm chart templates Kubernetes resources and exposes configuration values so an application can be installed and configured with a small set of commands. Kubernetes then reconciles the requested state with the running cluster.

This lab uses the official RustFS chart repository. You need a running Kubernetes cluster, `kubectl`, Helm 3, and a default StorageClass (or a suitable StorageClass configured in `rustfs-config.yaml`).

## 2. Install RustFS

Review `rustfs-config.yaml` before installing. It selects a single-pod standalone deployment for a lightweight classroom demonstration, disables ingress, requests persistent storage, and sets demo credentials. This is not a production/high-availability configuration.

Run:

```sh
./install-rustfs.sh
```

The script adds the official chart repository and uses `helm upgrade --install` so it can be rerun to apply the same release configuration.

Check the resources:

```sh
kubectl get pods,services,pvc -n rustfs-ns
kubectl get events -n rustfs-ns --sort-by=.lastTimestamp
```

Wait until the RustFS pod is `Running` and `Ready`. If the pod is pending, check whether your cluster has a default StorageClass and whether the PersistentVolumeClaim was bound:

```sh
kubectl get storageclass
kubectl describe pvc -n rustfs-ns
kubectl describe pod -n rustfs-ns
```

## 3. Access the console and S3 API

Use port forwarding rather than exposing the demo service publicly. Run the command in a separate terminal and leave it running:

```sh
kubectl port-forward -n rustfs-ns svc/rustfs-svc 9000:9000 9001:9001
```

Then open `http://localhost:9001` in a browser. Sign in with the access key and secret configured in `rustfs-config.yaml`:

- Access key: `rustfs-lab-user`
- Secret key: `replace-this-demo-secret`

The S3-compatible API is available at `http://localhost:9000`. Verify that the service responds:

```sh
curl --fail http://localhost:9000/health
```

These credentials are intentionally simple lab values. Change them before using the deployment in a shared environment, and do not expose the service to an untrusted network with demo credentials.

## 4. Use RustFS from Python

The included `rustfs-example.py` uses the AWS SDK for Python (`boto3`) to demonstrate common S3 operations: listing buckets, creating a bucket, listing objects, and uploading files. These are common object-storage concepts and are useful even when the server is not AWS S3.

With the port-forward for port 9000 running, install dependencies and run the sample locally:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install boto3
python rustfs-example.py
```

The sample defaults to the local port-forward endpoint and the credentials in the configuration. It repeats the operations every 30 seconds so you can observe object listings after uploads. Press `Ctrl-C` to stop it.

You can override the endpoint and credentials using environment variables:

```sh
export RUSTFS_ENDPOINT=http://localhost:9000
export AWS_ACCESS_KEY_ID=rustfs-lab-user
export AWS_SECRET_ACCESS_KEY=replace-this-demo-secret
python rustfs-example.py
```

For this teaching example, the client uploads its own script and this README, which demonstrate object uploads without copying the credentials file into the bucket.

## 5. Run the Python client inside Kubernetes

`rustfs-example-dep.yaml` demonstrates a client running in the `default` namespace and accessing RustFS through Kubernetes DNS. Services can be addressed as `service.namespace.svc.cluster.local`; this example uses:

`rustfs.rustfs-ns.svc.cluster.local`

First build and publish the client image to a registry accessible by your cluster. For example, edit the image name in `rustfs-example-dep.yaml` to match your registry, then run:

```sh
make build IMAGE=your-dockerhub-user/rustfs-example:latest
docker push your-dockerhub-user/rustfs-example:latest
kubectl apply -f rustfs-example-dep.yaml
kubectl logs -f deployment/rustfs-example
```

If you use a local Kubernetes environment, you may instead load the image into that cluster and keep the image reference consistent with the image you loaded. Replace the demo credentials in the manifest with values matching the Helm configuration.

For a more secure deployment, put credentials in a Kubernetes Secret rather than directly in a Deployment manifest. The inline values here are for illustrating environment variables in a classroom exercise only.

## 6. Kubernetes concepts to observe

- **Namespace:** `rustfs-ns` groups the RustFS resources.
- **Helm release:** `rustfs` records the chart installation and its values.
- **Service:** provides stable in-cluster access to the S3 API and console.
- **PersistentVolumeClaim:** requests storage so object data can outlive a pod replacement.
- **Port forwarding:** temporarily maps a local port to a Kubernetes Service.
- **Service DNS:** lets another pod reach RustFS without knowing its pod IP.
- **S3 API:** uses buckets to organize objects and object keys to identify stored data.

RustFS is S3-compatible, but compatibility is not identical to every AWS S3 feature. For advanced APIs, check the RustFS compatibility documentation and test the exact operations your application requires.

## 7. Update or remove the deployment

Apply configuration changes with Helm:

```sh
helm upgrade rustfs rustfs/rustfs \
  --namespace rustfs-ns \
  --values rustfs-config.yaml
```

Remove the Helm release:

```sh
helm uninstall rustfs -n rustfs-ns
```

Remove the namespace if you want to delete the remaining namespaced resources:

```sh
kubectl delete namespace rustfs-ns
```

**Warning:** persistent-volume data retention depends on the chart, StorageClass, and reclaim policy. Inspect PVCs and PVs before deleting anything if you need to keep stored objects. This lab's goal is experimentation, not backup or durable production storage.

## Troubleshooting

- **Pod remains `Pending`:** check PVC status, available cluster capacity, and the StorageClass.
- **`ImagePullBackOff`:** check the image pull events and registry access.
- **Console or API won't open:** confirm the port-forward is still running and that the Service exposes ports 9000 and 9001.
- **Access denied:** make sure the client's access key and secret match the RustFS release configuration.
- **Python cannot connect:** verify the endpoint. A local script normally uses `http://localhost:9000` with port forwarding; a pod uses the in-cluster service DNS name.
