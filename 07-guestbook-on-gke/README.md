### Setting up Kubernetes
You will need to create a Kubernetes cluster to run your code. You can either use a local install of Docker and Kubernetes or use Google Cloud's service, GKE.

Creating a cluster using GKE can be done by issuing the following `gcloud` commands:
```
gcloud config set compute/zone us-central1-b
gcloud container clusters create --preemptible mykube
```
By default, this will create a 3-node cluster of `e2-medium` nodes. The `--premptible` flag drops the price (from \$0.05 per hour to \$0.01 per hour), but the nodes in your cluster will be deleted and restarted within 24 hours and may be deleted at any moment. Generally, this isn't a problem, but you can omit it if you're worried. It takes 3-4 minutes to create a cluster. You can delete your cluster using  `gcloud container clusters delete mykube`.  You can use `kubectl config current-context` to see what cluster configuration you're using (e.g. local or GKE).

Other than that, the process is exactly the same as in [running the standard guestbook application](../05-guestbook) except that [you need to install a slightly different ingress](https://kubernetes.github.io/ingress-nginx/deploy/#gce-gke). You need to initialize your user as a cluster-admin with the following command:
```
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole cluster-admin \
  --user $(gcloud config get-value account)
```
and then deploy the ingress:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
```

**Remember to delete your cluster when you're not using it.**
