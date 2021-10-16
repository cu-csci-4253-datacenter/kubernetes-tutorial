# Example: Guestbook application on Kubernetes

This directory contains the source code and Kubernetes manifests for a Python
Guestbook application following the similar tutorial in [the Kubernetes distribution](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/). The differences in this version is that the `php-redis` application has been replaced with the `python-redis` application and that application implements a Flask web service.

This example solves some of the issues in the previous steps of our Kubernetes tutorial -- rather than use an application with a local database, the application is using a network database based on [Redis](https://redis.com/). In order to support load balancing you could set the Redis server to be a primary/secondary setup (that's what the Kubernetes tutorial does) but we just use a single Redis server.

The Kubernetes structures are:
* A deployment for the frontend Python application
* A service for the frontend Python application
* An ingress for the frontend Python application
* Deployments for both the redis master and replica pods
* Services for both the redis master and replica pods

Services are used throughout so that simple DNS hostnames can be used to locate the appropriate pods (either the frontend or Redis).

The Python application is built using [the Dockerfile in the `python-redis` directory](python-redis/Dockerfile). The application is slightly more complicated than the blog application from the Flask tutorial. It combines ["static pages"](python-redis/app/static) where Flask acts as a regular web server with ["templates"](python-redis/app/static) that are dynamically updated by the Flask program.

The [routes in the Flask program](python-redis/app/routes.py) include one route for `/` to load the [one static web page](python-redis/app/static/index.html) that also [loads javascript code](python-redis/app/static/controllers.js). That javascript uses asynchronous javascript HTTP requests ("AJAX") to retrieve the actual blog data using the `/message/all`, `/message/set` and `/message/erase` routes. The code associated with those routes simply retrieves data or updates the Redis database.

In order to use the Ingress, you need to install an ingress controller as [we did before](../02-blog/README.md) and then deploy [the ingress for the guestbook](ingres-nginx.yaml). Before you do that, you should make certain that any prior ingress has been removed since both of them will be targeting the `/` route:
```
> kubectl delete ingress minimal-ingress
ingress.networking.k8s.io "minimal-ingress" deleted
> kubectl apply -f frontend-deployment.yaml
deployment.apps/frontend created
> kubectl apply -f frontend-service.yaml
service/frontend created
> kubectl apply -f redis-deployment.yaml
deployment.apps/redis-master created
> kubectl apply -f redis-service.yaml
service/redis-master created
service/redis-slave created
> kubectl apply -f ingress-nginx.yaml
ingress.networking.k8s.io/guestbook-ingress configured
```

This should deploy multiple web "frontends" and a single Redis database as below:
```
> kubectl get all
NAME                                READY   STATUS    RESTARTS   AGE
pod/frontend-7b5d84cdf9-bckbb       1/1     Running   0          3m30s
pod/frontend-7b5d84cdf9-px7kz       1/1     Running   0          3m30s
pod/frontend-7b5d84cdf9-tjsdn       1/1     Running   0          3m30s
pod/redis-master-869bcc55f5-825rj   1/1     Running   0          3m19s

NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/blog-svc       ClusterIP   10.105.46.241   <none>        9999/TCP   168m
service/frontend       ClusterIP   10.97.216.171   <none>        80/TCP     3m24s
service/kubernetes     ClusterIP   10.96.0.1       <none>        443/TCP    22d
service/redis-master   ClusterIP   10.101.67.253   <none>        6379/TCP   3m15s
service/redis-slave    ClusterIP   10.98.122.100   <none>        6379/TCP   3m15s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/frontend       3/3     3            3           3m31s
deployment.apps/redis-master   1/1     1            1           3m20s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/frontend-7b5d84cdf9       3         3         3       3m31s
replicaset.apps/redis-master-869bcc55f5   1         1         1       3m20s
```
The web frontends locate the Redis instance using the `redis-master` service. The ingress locates the web frontends using the `service/frontend` service. That service knows about each web frontend as you can verify through:
```
> kubectl describe svc/frontend
Name:              frontend
Namespace:         default
Labels:            app=guestbook
                   tier=frontend
Annotations:       <none>
Selector:          app=guestbook,tier=frontend
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.97.216.171
IPs:               10.97.216.171
Port:              <unset>  80/TCP
TargetPort:        5000/TCP
Endpoints:         10.1.0.56:5000,10.1.0.57:5000,10.1.0.58:5000
Session Affinity:  None
Events:            <none>
```
and examining the `Endpoints` the service has identified.

Once the ingress has been installed, you should be able to visit the sample application by going to [http://localhost](http://localhost) -- you'll be using one of multiple web front-ends to edit the blog.

From here, you should try modifying [the frontend deployment](frontend-deployment.yaml) to increase or decrease the number of front-end web servers. You can also try deleting pods in the frontend-deployment and you'll find that the deployment will then create new pods to maintain the specified number of replicas.