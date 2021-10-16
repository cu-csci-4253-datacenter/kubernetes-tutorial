# Installing Cassandra Using Helm

Kubernetes simplifies deploying complex applications through a *package manager*. One of the most common package manages is Helm, which will demonstrate by deploying a complex application, [a multi-replica NoSQL database that is widely used](https://cassandra.apache.org/_/index.html).

## What is Helm?

[Helm](https://helm.sh/) is a "package manager" for Kubernetes that simplifies the task of
deploying applications or entire systems by using template YAML files
for the Kubernetes components, providing default configuration
paramaters for those tepmlates and also providing a mechanism to
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
values](https://github.com/bitnami/charts/blob/master/bitnami/cassandra/values.yaml)
using your own [config file](./cass-config.yaml). I've provided a
configuration that decreases the size of the presistent disk and
provides the password "changeme". You can also modify the
`replicatCount` and run an upgrade to see how Helm handles upgrades

```
helm install -f ./cass-config.yaml my-cas bitnami/cassandra
```

Once this is run, you should see something like this:
```
$ helm install -f ./cass-config.yaml my-cas bitnami/cassandra
NAME: my-cas
LAST DEPLOYED: Mon Oct 19 11:10:18 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
** Please be patient while the chart is being deployed **

Cassandra can be accessed through the following URLs from within the cluster:

  - CQL: my-cas-cassandra.default.svc.cluster.local:9042
  - Thrift: my-cas-cassandra.default.svc.cluster.local:9160

To get your password run:

   export CASSANDRA_PASSWORD=$(kubectl get secret --namespace default my-cas-cassandra -o jsonpath="{.data.cassandra-password}" | base64 --decode)

Check the cluster status by running:

   kubectl exec -it --namespace default $(kubectl get pods --namespace default -l app=cassandra,release=my-cas -o jsonpath='{.items[0].metadata.name}') nodetool status

To connect to your Cassandra cluster using CQL:

1. Run a Cassandra pod that you can use as a client:

   kubectl run --namespace default my-cas-cassandra-client --rm --tty -i --restart='Never' \
   --env CASSANDRA_PASSWORD=$CASSANDRA_PASSWORD \
    \
   --image docker.io/bitnami/cassandra:3.11.8-debian-10-r20 -- bash

2. Connect using the cqlsh client:

   cqlsh -u cassandra -p $CASSANDRA_PASSWORD my-cas-cassandra

To connect to your database from outside the cluster execute the following commands:

   kubectl port-forward --namespace default svc/my-cas-cassandra 9042:9042 &
   cqlsh -u cassandra -p $CASSANDRA_PASSWORD 127.0.0.1 9042
```

## Reconfiguring

You can upgrade your Helm application to a new chart release or with new values from your configuration
file using

```
helm upgrade my-cas -f ./cass-config.yaml bitnami/cassandra
```

## Cleaning up

When you're done, you can delete all the resources associated with a chart using
```
helm delete my-release
```

This will remove everything except the PVC and PV volumes used to hold
the data. Note that you can explicitly provide a template for the
volume names if you plan on reusing your data while experimenting with
Cassandra.