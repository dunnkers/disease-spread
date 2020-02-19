# 2020_group_01_s4192044_s2546736_s2995697

## General architecture

GCP: Google Cloud Platform.

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
    ```