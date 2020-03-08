## Install

Build Docker image & upload to Docker Hub.

### Docker image

1. Make sure you are `cd`'ed into this directory (`spark-playground`).
2. `docker build -t dunnkers/disease-spread:spark .`
3. `docker push dunnkers/disease-spread:spark`
4. Image uploaded to DockerHub 🙌🏼

### Deploying on GKE

1. Launch Cloud Console
2. Upload file > `deploy-to-gke.yaml`
3. In console, type:
```shell
kubectl apply -f deploy-to-gke.yaml
```
4. Should launch a pod 🚀
<!-- 1. Run Spark.

2. Prepare virtual environment

    ```shell
    python3 -m venv ./venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    ```

## Usage

Make sure to have entered the virtual environment:
```shell
source ./venv/bin/activate
```

## Adding a package 

```shell
pip3 install <package>
pip3 freeze > requirements.txt
``` -->