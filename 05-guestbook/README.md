# Example: Guestbook application on Kubernetes

This directory contains the source code and Kubernetes manifests for Python
Guestbook application from the Kubernetes distribution.

Follow the tutorial at https://kubernetes.io/docs/tutorials/stateless-application/guestbook/.

This example solves some of the issus in our Kubernetes tutorial --
rather than use an application with a local database, the application
is using a network database based on Redis. In order to support load balancing
the Redis is in a "primary/secondary".

The Kubernetes structures are:
* A deployment for the frontend Python application
* A service for the frontend Python application
* An ingress for the frontend Python application
* Deployments for both the redis master and replica pods
* Services for both the redis master and replica pods

The redis servers are configured to find each other using DNS.

The Python application is built using the Dockerfile in the `python-redis` directory.

