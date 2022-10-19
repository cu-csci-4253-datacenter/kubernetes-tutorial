### Setting up Kubernetes
You will need to create a Kubernetes cluster to run your code. You can either use a local install of Docker and Kubernetes or use Google Cloud's service, GKE.

You will need to [install the Google gcloud command line SDK](https://cloud.google.com/sdk/docs/install).

Creating a cluster using GKE can be done by issuing the following `gcloud` commands:
```
gcloud config set compute/zone us-central1-b
gcloud container clusters create mykube --preemptible --release-channel None --zone us-central1-b
```
By default, this will create a 3-node cluster of `e2-medium` nodes. The `--premptible` flag drops the price (from \$0.05 per hour to \$0.01 per hour), but the nodes in your cluster will be deleted and restarted within 24 hours and may be deleted at any moment. Generally, this isn't a problem, but you can omit it if you're worried. It takes 3-4 minutes to create a cluster. 

Another option is to use an [automatically managed cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview). In this model, you do not manage the nodes in your cluster and you pay for the individual pods you deploy (plus some management cost). There are some [constraints](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview#limits) that arise from using shared infrastructure but in most cases, these won't be an issue. You also need to set resource limits on your pods so the system knows how much CPU and RAM you'll be using. The pricing is set based on the vCPU's that you're using - the regular price is \$0.0445 per hour and if you use e.g. 0.1vCPU for a pod, that would be \$0.00445 per hour; however, your pod would never get more than 0.1vCPU of performance.

You create such a cluster using e.g.:
```
gcloud container clusters create-auto mykube2 --region us-west3
```

You can delete your cluster using 
```
gcloud container clusters delete mykube
```
You can use `kubectl config current-context` to see what cluster configuration you're using (e.g. local or GKE).

Other than that, the process is exactly the same as in [running the standard guestbook application](../05-guestbook) except that [you need to install a slightly different ingress](https://kubernetes.github.io/ingress-nginx/deploy/#gce-gke). 

#### Using older gcloud packages:
You need to initialize your user as a cluster-admin with the following command:
```
gcloud components install gke-gcloud-auth-plugin
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole cluster-admin \
  --user $(gcloud config get-value account)
```

#### Using newer gcloud authentication API
You need to install 
```
sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
```
and then do:
```
gcloud container clusters get-credentials mykube --region us-central1-b
```

and then deploy the ingress:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
```

**Remember to delete your cluster when you're not using it.**
