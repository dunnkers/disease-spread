# 2020_group_01_s4192044_s2546736_s2995697

## General architecture

GCP: Google Cloud Platform.

1. We use **Helm** to obtain 'charts' (packages) for Kubernetes:
https://medium.com/google-cloud/helm-on-gke-cluster-quick-hands-on-guide-ecffad94b0
2. Install spark chart:

`helm install --name superspark  stable/spark`