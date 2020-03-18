# 2020_group_01_s4192044_s2546736_s2995697

## General architecture - configuring GCP

GCP: Google Cloud Platform.

1. Create a GKE cluster
2. Connect to the *specific* cluster (don't just use the general Cloud console)
-> via UI or:
`gcloud container clusters get-credentials cluster-1 --zone europe-north1-a --project sixth-utility-268609`

3. Add Helm service account
https://medium.com/google-cloud/helm-on-gke-cluster-quick-hands-on-guide-ecffad94b0
-> using some `.yaml` config file.
4. Init helm
`helm init`

5. Verify there is a tiller pod
`kubectl get deploy,svc tiller-deploy -n kube-system`

(if, for some reason, you are getting the 'could not find tiller' error: https://github.com/helm/helm/issues/4685#issuecomment-433209134)

(if, you are getting a 'namespace default forbidden' error: https://github.com/fnproject/fn-helm/issues/21#issue-312627792)

... wait a bit untill tiller pods are ready.

## Installing a Kafka cluster
6. Install Kafka using a chart
https://github.com/helm/charts/tree/master/incubator/kafka

e.g.:
```shell
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --name my-kafka incubator/kafka
```

## Installing Kafdrop
7. Installing Kafdrop

e.g. using default settings:
```shell
git clone https://github.com/obsidiandynamics/kafdrop && cd kafdrop
helm upgrade -i kafdrop chart
```

Then, configure the broker address as `my-kafka:9092`:

```yaml
apiVersion: apps/v1
# [...]
spec:
  template:
    spec:
      containers:
      - env:
        - name: KAFKA_BROKERCONNECT
          value: my-kafka:9092
```

(can easily be done in the GCP UI)
![Screenshot from 2020-03-03 10-39-58](https://user-images.githubusercontent.com/744430/75763328-601aa000-5d3c-11ea-9e1a-4b0d8a696eb0.png)

Finally, optionally expose Kafdrop externally using a `LoadBalancer`:

```shell
kubectl expose deployment kafdrop --type=LoadBalancer --name=kafdrop-external-service
```

This will create an external IP address such that you can access Kafdrop from your browser. ✌🏼 (in production though, you will probably not want to do this.)
<!-- 
1. We use **Helm** to obtain 'charts' (packages) for Kubernetes:
https://docs.bitnami.com/google/get-started-gke/#step-4-install-and-configure-helm
    Login to Cloud Shell and run:
    ```shell
    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get-helm-3 > get_helm.sh
    chmod 700 get_helm.sh
    ./get_helm.sh
    ```
2. Install spark chart:
    ```shell
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm install my-release bitnami/spark
    ``` -->

## Install spark

1. Installing a Spark cluster
https://hub.helm.sh/charts/microsoft/spark

```shell
helm repo add microsoft https://microsoft.github.io/charts/repo
helm install microsoft/spark --version 1.0.0
```
## Installing mongodb

To  install the mongodb helm chart with a repo stable that looks at https://kubernetes-charts.storage.googleapis.com/: 
```shell
helm install my-mongodb stable/mongodb-7.8.7
```

This will create a mongodb node witha an associated service ánd generates a secret called `mongodb-root-password` for authentication. To use it in a container that is supposed to connect to mongodb add the following to the container environment variables section in the deployment yaml:
```yaml
...
env:
  - name: MONGODB_ROOT_PASSWORD
    valueFrom:
      secretKeyRef:
        key: mongodb-root-password
        name: my-mongodb
...
```

Then the password can be used like in the following python snippet:
```python
password = os.getenv('MONGODB_ROOT_PASSWORD')
client = pymongo.MongoClient('mongodb://root:{}@my-mongodb:27017'.format(password))
```

## Upgrading Kubernetes cluster machine types

(from: https://cloud.google.com/kubernetes-engine/docs/tutorials/migrating-node-pool)

First, obtain the name of the node pool you want to upgrade:
```shell
gcloud container node-pools list
```

Then, upgrade the machine types:
```shell
gcloud container node-pools create larger-pool --cluster=cluster-1 --machine-type=n1-standard-1 --num-nodes=3
```

Now, make the previous pool nodes "unschedulable". Retrieve pool node names:

```shell
kubectl get nodes -l cloud.google.com/gke-nodepool=default-pool
```

Then for every node:

```shell
kubectl cordon <NODE>
```

After all nodes have been 'cordoned', 'drain' every node:

```shell
kubectl drain --force --ignore-daemonsets --delete-local-data --grace-period=10 <NODE>
```

Finally, we delete the old node pool:

```shell
gcloud container node-pools delete default-pool --cluster cluster-1
```

We can verify there exist only one node pool now using:

```shell
gcloud container node-pools list --cluster cluster-1
```

## Installing mongo-express

https://hub.helm.sh/charts/cowboysysop/mongo-express

1. `helm repo add cowboysysop https://cowboysysop.github.io/charts/`

2. `helm install cowboysysop/mongo-express --version 1.0.1 --set mongodbServer=my-mongodb,mongodbEnableAdmin=true,mongodbAdminPassword=jLWIWnJKe7`

3. Expose external IP:

```yaml
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/name: mongo-express
  name: mongo-express-service
spec:
  ports:
  - port: 8081
    protocol: TCP
    targetPort: 8081
  selector:
    app.kubernetes.io/name: mongo-express
  sessionAffinity: None
  type: LoadBalancer
```

-> also available in `mongo-express-config` folder