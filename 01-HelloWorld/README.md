# Basic Pod examples

To utilize a configuration file within kubernetes:

```
kubectl apply -f <yaml>
```

The config files all utilize the busybox container, which is an
extremely lightweight linux image.
* busybox1.yaml - Creates a busybox container to print "hi" and exits.
* busybox2-cmd.yaml - Prints the time in an infinite loop.	
* busybox3-cmd-and-arg.yaml - Same as busybox2, but specifies the arguments separate from the command.
* busybox4-multiline.yaml - Same thing again but with multiline yaml syntax.
* busybox5-sidecar-broken.yaml - Creates a pod with two containers that incorrectly tries to share the same filesystem.
* busybox6-sidecar-mount.yaml - Corrects the problem of the previous example by utilizing a shared volume. The volume utilizes an emptyDir, which is a temporary storage mechanism that can be shared between containers in the same pod. The volume is lost upon pod deletion.
