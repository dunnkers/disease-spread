# 2020_group_01_s4192044_s2546736_s2995697

## General architecture

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
6. Install Kafka using a chart
https://github.com/helm/charts/tree/master/incubator/kafka



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