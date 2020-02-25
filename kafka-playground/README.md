## GCP

1. Install Kafka via Cloud Marketplace

https://console.cloud.google.com/marketplace/details/click-to-deploy-images/kafka

<!-- 2. Install Kafdrop
```shell
helm upgrade -i kafdrop chart --set image.tag=3.23.0    --set kafka.brokerConnect=kafka-1-vm.europe-north1-a.c.sixth-utility-268609.internal:9092    --set server.servlet.contextPath="/"    --set cmdArgs="--message.format=AVRO --schemaregistry.connect=http://localhost:8080" --set jvm.opts="-Xms32M -Xmx64M"
``` -->

[WIP] Still to implement:
2. Run a pod on Kubernetes, 'produce' a message to Kafka. Check whether it's in.

## LOCAL
### Install

1. Run Zookeeper and Kafka Broker.

(Ubuntu/Linux instructions)
https://techexpert.tips/apache-kafka/apache-kafka-installation-ubuntu-linux/

2. Prepare virtual environment

    ```shell
    python3 -m venv ./venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    ```

### Usage

Make sure to have entered the virtual environment:
```shell
source ./venv/bin/activate
```

Now start the consumer:
```shell
python3 kafka-consumer.py
```

Finally, send some messages:
```shell
python3 kafka-producer.py
```

### Adding a package 

```shell
pip3 install <package>
pip3 freeze > requirements.txt
```