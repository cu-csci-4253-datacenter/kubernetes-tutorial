# Adding Persistent Data

The data in our existing blog is ephemeral, meaning it goes away when the pod holding the blog exits.

To see this, [visit your blog page](http://localhost), create an account and post blog page. Kill the blog pod and restart it and then visit your blog again. 
```
> kubectl delete pod blog-env
pod "blog-env" deleted             
> kubectl apply -f 02-blog-env.yaml
pod/blog-env created
```
You'll see the post is gone if you [visit your blog again](http:localhost). We will re-deploy the blog using persistent volumes to retain the data across restarts.

## Persistent Volumes & Claims
In order to retain the blog contents, we need to add [*persistent volumes*](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) which are file systems or directories that can be mounted within your application container.

There are [many types of persistent volumes depending on your cloud provider (files local to your cluster, AWS files, *etc*) and these different kinds are specified by a Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/).

In order to separate the details of how a volume is created from how the volume is used, Kubernetes introduces a `PersistentVolume` and `PersistentVolumeClaim`. A claim identifies a particular volume to be used by a pod; the volume definition specified the `StorageClass` and other implementation-specific details for the volume.

We have [combined both the PersistentVolume (PV) and PersistentVolumeClaim (PVC) in a single YAML file](01-pv.yaml) following the steps in the [Kubernetes storage tutorial](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/). This uses the `manual` storage class to create a volume at the `/mnt/data` directory in the virtual machine running the Kubernetes cluster. There are other options such as specifying an `emptyDir` without specifying the specific path. The PVC then binds to that volume.
```
> kubectl apply -f 01-pv.yaml
persistentvolume/blog-pv-volume unchanged
persistentvolumeclaim/blog-pv-claim created
> kubectl get pv
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                   STORAGECLASS   REASON   AGE
blog-pv-volume   10Gi       RWO            Retain           Bound    default/blog-pv-claim   manual                  4m22s
> kubectl get pvc
NAME            STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
blog-pv-claim   Bound    blog-pv-volume   10Gi       RWO            manual         14s
```

This storage set up is not very robust, because the data is only available on the node running the Kubernetes cluster. In production, you would use other, more robust storage. In addition, these volumes can't be shared across multiple blog instances -- to do that, we would need to use a StorageClass that provides shared data (such as NFS).

## Using the PVC in the blog

We can now [specify that the blog should use the PV through by specifying the PVC](02-blog-pv). This is done in two parts. First, we define a `volume` as part of the Pod. A pod can have multiple volumes, and each of them will be given a unique name.

Volumes can be shared between the different containers in a pod, so each container that wants to use a volume needs to specify the `volume` using a `volumeMounts` specification.

Once you've created the PV/PVC pair, you can kill your old blog pods and launch a new pod using the PVC.
```
> kubectl delete pod blog-env
pod "blog-env" deleted
> kubectl apply -f 02-blog-pv.yaml
pod/flask created
```
Note that this pod is named "flask" rather than "blog". However, if you [visit your blog through the existing ingress](http://localhost), you'll see that the service is able to "find" the blog because it has the `app:blog` label -- this just emphasizes that the *name* of the pod isn't important, it's the *label* that defines the service mapping.

You can now delete & restart the flask pod:
```
> kubectl delete pod/flask
pod "flask" deleted
> kubectl apply -f 02-blog-pv.yaml
pod/flask created
```
and when you [visit your blog through the existing ingress](http://localhost), you will see that the data persisted over the restart.

## Next Steps: Scalability

In the [next step of our tutorial](../04-scalability/README.md) we'll see how to make our blog be "scalable" and reliable by using a `Deployment` of 3 blog servers. However, because we are using a `StorageClass` that only allows a single Pod to access our PV in read-write mode, the blog servers will be independent of each other and have different content.

Then, in [step 5 of the tutorial](../05-guestbook/README.md) we'll show how to use a common database to share content across multiple applications.

For now, delete the blog pod, the PV and PVC:
```
> kubectl delete pod/flask pv/blog-pv-volume pvc/blog-pv-claim
pod "flask" deleted
persistentvolume "blog-pv-volume" deleted
persistentvolumeclaim "blog-pv-claim" deleted
```