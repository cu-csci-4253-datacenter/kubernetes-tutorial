# Example: Guestbook application on Kubernetes

This directory contains the source code and Kubernetes manifests for Python
Guestbook application from the Kubernetes distribution. Follow the tutorial at https://kubernetes.io/docs/tutorials/stateless-application/guestbook/.

The differences in this version is that the `php-redis` application has been replaced with the `python-redis` application and that application implements a Flask web service.

This example solves some of the issues in our Kubernetes tutorial -- rather than use an application with a local database, the application is using a network database based on Redis. In order to support load balancing you could set the Redis server to be a primary/secondary setup (that's what the Kubernetes tutorial does) but we just use a single Redis server.

The Kubernetes structures are:
* A deployment for the frontend Python application
* A service for the frontend Python application
* An ingress for the frontend Python application
* Deployments for both the redis master and replica pods
* Services for both the redis master and replica pods

The redis servers are configured to find each other using DNS.

The Python application is built using the Dockerfile in the `python-redis` directory.

In order to use the Ingress, you need to install an ingress [using the directions at this site](https://kubernetes.github.io/ingress-nginx/deploy/#docker-for-mac). The same directions hold for "docker on mac" if you are using Docker on Windows/WSL2.

