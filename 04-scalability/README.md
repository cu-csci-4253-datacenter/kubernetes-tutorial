# Deployments for Scalability and Reliability

So far, we've deployed a blog using a single Pod, but our solution is fragile:
* We can't reconfigure anything in our Pod other than by killing it and restarting it
* If our pod dies or exits for some reason, it's not automatically restarted
* If we have a flood of users, our single Pod may be overwhelmed

We can [solve both problems using Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), a type of "workload" that manages pods. In practice, you never deploy a "naked pod" -- you almost always use a Deployment to manage the pod lifecycle.

## Deployments

A deployment manages a set of pods specified by matching labels:
```
  selector:
    matchLabels:
      app: blog
```
The deployment can search for and receive information about changes to pods that match this label.

The [deployment specification](01-blog-deployment.yaml) can also specify the number of `replicas` of the pod that should be active:
```
spec:
  replicas: 3
```
If there are too many replicas running, surplus replicas are killed. If there are not enough replicas running, the deployment uses the `template` to create more:
```
  template:
    metadata:
      labels:
        app: blog
    spec:
      containers:
      - name: blog
        image: dirkcgrunwald/blog
        ports:
        - containerPort: 8888
        env:
          - name: FLASK_PORT
            value: "8888"
```
This template is just the pod specification we saw before.

The Deployment manages the lifecycle of the pods. When you create a Deployment, it will create needed pods. When you delete the Deployment, it will delete the pods it created.

The pods created by a deployment have unique identifiers added to prevent name conflicts:
```
> kubectl apply -f 01-blog-deployment.yaml
deployment.apps/blog-deployment created
> kubectl get pod
NAME                               READY   STATUS              RESTARTS   AGE
blog-deployment-7dd467b478-b9zwq   0/1     ContainerCreating   0          6s
blog-deployment-7dd467b478-cxdb9   0/1     ContainerCreating   0          7s
blog-deployment-7dd467b478-jdvbt   0/1     ContainerCreating   0          6s
```
If you [visit your blog through the existing ingress](http://localhost), you will be directed to one or the other deployment. Because the individual pods each have their own local data, when you register an account and then refresh the display, you may be directed to another blog instance that doesn't have that account created. This isn't an issue with the deployment, it's because our blog isn't very robust.

Although you can't change a Pod configuration, you can change a Deployment. For example, if you modify the number of `replicas` to be 1 rather than 3 and then re-apply the deployment YAML file, you'll see that two of the replicas will terminate:
```
> kubectl apply -f 01-blog-deployment.yaml
deployment.apps/blog-deployment configured
> kubectl get pod
NAME                               READY   STATUS        RESTARTS   AGE
blog-deployment-7dd467b478-b9zwq   1/1     Running       0          5m10s
blog-deployment-7dd467b478-cxdb9   1/1     Terminating   0          5m11s
blog-deployment-7dd467b478-jdvbt   1/1     Terminating   0          5m10s
```
Likewise, if you then increase the replica count to 8 and reapply, you'll see additional replicas created:
```
> kubectl apply -f 01-blog-deployment.yaml
deployment.apps/blog-deployment configured
> kubectl get pod
NAME                               READY   STATUS              RESTARTS   AGE
blog-deployment-7dd467b478-86k6d   0/1     Pending             0          1s
blog-deployment-7dd467b478-92g4m   0/1     Pending             0          1s
blog-deployment-7dd467b478-b9zwq   1/1     Running             0          6m7s
blog-deployment-7dd467b478-g9kx2   0/1     ContainerCreating   0          1s
blog-deployment-7dd467b478-nndd2   0/1     ContainerCreating   0          1s
blog-deployment-7dd467b478-qgbrj   0/1     ContainerCreating   0          1s
blog-deployment-7dd467b478-sg5dt   0/1     ContainerCreating   0          1s
blog-deployment-7dd467b478-xp4r5   0/1     Pending             0          1s
```
The deployment always attempts to match your intended state -- if you said 8 replicas, it will try to maintain 8 replicas. You can use a [horizontal pod autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) to automatically increase or decrease the number of replicas based on metrics (*e.g.* CPU utilization or number of requests). You can also use deployments to [perform "rolling updates"](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/) of your pods when you e.g update a container. The deployment will delete the old containers & deploy the new ones.

When you delete a deployment, all the pods created by that deployment will be deleted:
```
> kubectl delete deploy/blog-deployment
deployment.apps "blog-deployment" deleted
> kubectl get pod
NAME                               READY   STATUS        RESTARTS   AGE
blog-deployment-7dd467b478-86k6d   1/1     Terminating   0          4m37s
blog-deployment-7dd467b478-92g4m   1/1     Terminating   0          4m37s
blog-deployment-7dd467b478-b9zwq   1/1     Terminating   0          10m
blog-deployment-7dd467b478-g9kx2   1/1     Terminating   0          4m37s
blog-deployment-7dd467b478-nndd2   1/1     Terminating   0          4m37s
blog-deployment-7dd467b478-qgbrj   1/1     Terminating   0          4m37s
blog-deployment-7dd467b478-sg5dt   1/1     Terminating   0          4m37s
blog-deployment-7dd467b478-xp4r5   1/1     Terminating   0          4m37s
```