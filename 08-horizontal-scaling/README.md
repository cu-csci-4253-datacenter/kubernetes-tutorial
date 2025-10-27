From kubernetes walkthrough: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/

Requires 2 node or more kubernetes cluster.

Requires metric server. Follow install instructions from here:  
https://github.com/kubernetes-sigs/metrics-server#deployment.
To get it to work for my setup, I had to run 
_kubectl -n kube-system edit deployment/metrics-server_ 
and then edit the file to add _- --kubelet-insecure-tls_.
e.g.

```
    spec:
      template:
        spec:
          containers:
          - args:
            - --cert-dir=/tmp
            - --secure-port=4443
            - --kubelet-insecure-tls  # Add this line
            - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
            - --kubelet-use-node-status-port
            - --metric-resolution=15s
            image: registry.k8s.io/metrics-server/metrics-server:v0.6.4 # (version may vary)
            imagePullPolicy: IfNotPresent
            name: metrics-server
```

Steps:
* _kubectl apply -f application/php-apache.yaml_
* _kubectl autoscale deployment php-apache --cpu=50% --min=1 --max=10_
 - Or _kubectl apply -f application/hpa.yaml_
* _kubectl get hpa_
* _kubectl get hpa php-apache --watch_
* _kubectl run -i --tty load-generator --rm --image=busybox:latest --restart=Never -- /bin/sh -c "while sleep 0.001; do wget -q -O- http://php-apache; done"_
