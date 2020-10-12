# Pushing an image to Docker Register / Hub

First, you need to create a log at `hub.docker.com`. Record your credentials (username and password).

On the command line, execute
```
docker login
```
It will ask for your credentials; provide them. It should indicate successful login.

## Pushing an image

You need to tag your image with you Docker hub username and a version and then push it to the hub.
For example, given:
```
docker images | grep -i blog
blog                                  latest                                           1aaf9a329fa0        8 minutes ago       228MB
```
we would tag this image using
```
docker tag 1aaf9a329fa0 dirkcgrunwald/blog:v1
```
and then push it to Docker Hub using
```
docker push dirkcgrunwald/blog:v1
```

## Using the image
You'll need to modify the YAML files to specify the proper image
