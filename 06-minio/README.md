# Installing Minio Object Store Using Helm

Kubernetes simplifies deploying complex applications through a *package manager*. One of the most common package manages is Helm, which we will demonstrate by deploying a complex application, [an open-source "object store" called Minio that is similar to S3](https://min.io/).

## What is Helm?

[Helm](https://helm.sh/) is a "package manager" for Kubernetes that simplifies the task of
deploying applications or entire systems by using template YAML files
for the Kubernetes components, providing default configuration
parameters for those templates and also providing a mechanism to
override the default values.

The collection of template files is called a "Chart" and there are
several repositories of Helm charts for the current release of Helm, version 3.
This includes:

* The open-source [Artifact project](https://artifacthub.io/)
* [Charts provided by Bitnami](https://bitnami.com/stacks/helm)

Helm provides mechanisms to install and upgrade applications; most of
the difficult work is actually done by Kubernetes which updates the current
configuration to match the specified upgrade.

## Using The Bitnami Helm

Helm lets you use different repositories of charts; to use the Bitnami
charts, you need to first add the Bitnami repository.
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

When you deploy a Helm chart, you can override the [provided
values](https://github.com/bitnami/charts/tree/master/bitnami/minio)
using your own configuration. I've provided a
[config file](./minio-config.yaml) that decreases the size of the persistent disk and
provides the user "rootuser" and password "rootpasswd123".

```
helm install -f ./minio-config.yaml myminio bitnami/minio
```

Once this is run, you should see something like this:
```
$ helm install -f ./minio-config.yaml myminio bitnami/minio
NAME: myminio
LAST DEPLOYED: Mon Oct 10 12:41:25 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: minio
CHART VERSION: 11.10.7
APP VERSION: 2022.10.8

** Please be patient while the chart is being deployed **

MinIO&reg; can be accessed via port  on the following DNS name from within your cluster:

   myminio.default.svc.cluster.local

To get your credentials run:

   export ROOT_USER=$(kubectl get secret --namespace default myminio -o jsonpath="{.data.root-user}" | base64 -d)
   export ROOT_PASSWORD=$(kubectl get secret --namespace default myminio -o jsonpath="{.data.root-password}" | base64 -d)

To connect to your MinIO&reg; server using a client:

- Run a MinIO&reg; Client pod and append the desired command (e.g. 'admin info'):

   kubectl run --namespace default myminio-client \
     --rm --tty -i --restart='Never' \
     --env MINIO_SERVER_ROOT_USER=$ROOT_USER \
     --env MINIO_SERVER_ROOT_PASSWORD=$ROOT_PASSWORD \
     --env MINIO_SERVER_HOST=myminio \
     --image docker.io/bitnami/minio-client:2022.10.6-debian-11-r1 -- admin info minio

To access the MinIO&reg; web UI:

- Get the MinIO&reg; URL:

   echo "MinIO&reg; web URL: http://127.0.0.1:9001/minio"
   kubectl port-forward --namespace default svc/myminio 9001:9001
```

## Using your Minio Object Store

[Minio provides a Python library](https://min.io/docs/minio/linux/developers/python/minio-py.html) and provides [examples using that library](https://github.com/minio/minio-py/tree/release/examples).

In order to access Minio outside the Kubernetes cluster, you'll need to "port-forward" the connection:

```
kubectl port-forward --namespace default svc/myminio 9000:9000
```

This connect `localhost:9000` to the Minio service in the Kubernetes cluster. You would need to do this before using [the sample Minio python program provided](./minio-example.py) or the [Minio command-line client](https://min.io/docs/minio/linux/reference/minio-mc.html).

## Reconfiguring

You can upgrade your Helm application to a new chart release or with new values from your configuration
file using

```
helm upgrade myminio -f ./minio-config.yaml bitnami/minio
```

## Cleaning up

When you're done, you can delete all the resources associated with a chart using
```
helm delete myminio
```

This will remove everything except any PVC and PV volumes used to hold
the data. Note that you can explicitly provide a template for the
volume names if you plan on reusing your data while experimenting with
Minio.