# Kubernetes Object Storage Lab (MinIO SDK + RustFS)

This lab originally installed MinIO using the Bitnami Helm chart. That approach is no longer a reliable starting point: the old Bitnami chart/image references are stale, and the upstream MinIO container image repository is archived. The lab now uses [RustFS](https://github.com/rustfs/rustfs), an S3-compatible object store with a published container image, while retaining the MinIO Python SDK so students can learn the S3 API and object-storage programming model.

RustFS is **not MinIO**. It is an alternative implementation of the S3-compatible API, and compatibility is not guaranteed for every MinIO-specific feature. This lab uses only basic bucket and object operations.

## Learning goals

- Deploy a stateful application in Kubernetes.
- Expose an S3 API and web console using a Kubernetes Service.
- Store data in a PersistentVolumeClaim.
- Access the service from outside the cluster using `kubectl port-forward`.
- Use the MinIO Python SDK to create buckets, list objects, and upload files to an S3-compatible service.
- Use Kubernetes DNS to access a service from a pod in another namespace.

## Prerequisites

- A working Kubernetes cluster and `kubectl` configured for it.
- Permission to create a namespace, Secret, StatefulSet, Service, and PersistentVolumeClaim.
- A default StorageClass, unless you edit `rustfs.yaml` to specify a suitable StorageClass.
- Docker, only if you want to build and publish the optional Python example container.

## Deploy the object store

From this directory, run:

```sh
kubectl apply -f rustfs.yaml
kubectl rollout status statefulset/minio-proj -n minio-ns --timeout=180s
kubectl get pods,pvc,svc -n minio-ns
```

Or run `./install-minio.sh`, which applies the manifest and waits for the StatefulSet rollout.

The manifest creates a `minio-ns` namespace, a Kubernetes Secret for credentials, a Service, and a one-replica StatefulSet. A 1 GiB PVC stores data under `/data`; deleting or recreating the pod should not delete objects stored on that volume. The PVC is intentionally small for a teaching cluster.

The manifest uses the `rustfs/rustfs:latest` image published by the project. For a reproducible class deployment, consider pinning an explicit version or image digest after testing it in your cluster. This single-node configuration is for teaching and development, not a highly available or production storage system.

### Credentials

The manifest uses these **lab-only** credentials:

- Access key: `rootuser`
- Secret key: `change-this-demo-password`

They are stored in a Kubernetes Secret to avoid putting credentials directly in the pod specification. The example values are not suitable for a shared or public cluster. Change `stringData` in `rustfs.yaml` before deployment if needed. If you change them, use the same values when running the Python example.

## Access the console and S3 API

In a separate terminal, run:

```sh
kubectl port-forward -n minio-ns svc/minio-proj 9000:9000 9001:9001
```

Keep that command running while you use the service.

- S3 API endpoint: `http://localhost:9000`
- Web console: `http://localhost:9001`

Sign in to the console using the credentials above. The port-forward binds to localhost by default, so it does not expose the service to the entire network.

Check readiness from another terminal:

```sh
curl --fail http://localhost:9000/health
```

## Run the Python example locally

Install the SDK in your active Python environment:

```sh
python3 -m pip install minio
```

With the port-forward still running, execute:

```sh
python3 minio-example.py
```

The program creates `my-bucketname` if needed, lists buckets and objects, uploads the example source files when they are present, and repeats every 10 seconds. Stop it with `Ctrl-C`.

Environment variables can override the connection settings:

```sh
MINIO_HOST=localhost:9000 \
MINIO_USER=rootuser \
MINIO_PASSWD=change-this-demo-password \
python3 minio-example.py
```

The Python SDK package is still named `minio`; it can communicate with S3-compatible services using their S3 endpoint and credentials. The example is deliberately limited to common S3 operations.

## Run the example inside Kubernetes (optional)

The file `minio-example-dep.yaml` shows how an application pod can reach the object store by Kubernetes DNS. Build and push the image with your own registry account if needed:

```sh
make build
make push DOCKERUSER=YOUR_DOCKERHUB_USERNAME
```

Edit the image in `minio-example-dep.yaml` to match the image you pushed, then deploy the object store and example:

```sh
kubectl apply -f rustfs.yaml
kubectl apply -f minio-example-dep.yaml
kubectl logs -f deployment/minio-example-deployment
```

The example pod uses `minio-proj.minio-ns.svc.cluster.local:9000`, and reads its credentials from the Secret in `minio-ns`. Both the Secret and the example deployment are in the same namespace because Kubernetes Secrets are namespace-scoped.

## Troubleshooting

```sh
kubectl get pods,pvc,svc -n minio-ns
kubectl describe pod -n minio-ns -l app=minio-proj
kubectl logs -n minio-ns statefulset/minio-proj
kubectl get events -n minio-ns --sort-by=.lastTimestamp
```

- **PVC stays Pending:** your cluster may not have a default StorageClass. Check `kubectl get storageclass` and set `storageClassName` in `rustfs.yaml` to a class available in your cluster.
- **Pod cannot write to `/data`:** the manifest sets `fsGroup: 10001`, matching the non-root UID/GID documented by the RustFS image. Storage drivers differ; inspect pod events if permissions still fail.
- **Image pull failure:** verify that your cluster can pull `rustfs/rustfs:latest` from Docker Hub and that the image supports your node architecture.
- **SDK connection errors:** ensure the port-forward is running and that `MINIO_HOST` includes the port (`localhost:9000`). Verify that the credentials match the Secret.

## Access from another namespace

Kubernetes service DNS follows the pattern `service.namespace.svc.cluster.local`. The object-store endpoint is:

```text
minio-proj.minio-ns.svc.cluster.local:9000
```

A pod in another namespace can use that DNS name directly. The original `ExternalName` alias is unnecessary for this basic lab, so the example uses the full service DNS name instead.

## Clean up

Delete the application resources:

```sh
kubectl delete -f minio-example-dep.yaml --ignore-not-found=true
kubectl delete -f rustfs.yaml
```

The StatefulSet's PVC is created from a `volumeClaimTemplate`, and deleting the StatefulSet does not normally delete that PVC automatically. Check before deleting persistent data:

```sh
kubectl get pvc -n minio-ns
kubectl delete pvc data-minio-proj-0 -n minio-ns  # destructive: deletes the stored lab data
```

Kubernetes storage reclaim behavior depends on the StorageClass and underlying provisioner. Remove the PVC only when you are certain the data is no longer needed.

## References

- [RustFS container installation](https://docs.rustfs.com/en/installation/container)
- [RustFS source repository](https://github.com/rustfs/rustfs)
- [MinIO Python SDK](https://github.com/minio/minio-py)
- [Kubernetes StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Kubernetes port forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
