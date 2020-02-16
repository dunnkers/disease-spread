## Install

1. Run Zookeeper and Kafka Broker.

(Ubuntu/Linux instructions)
https://techexpert.tips/apache-kafka/apache-kafka-installation-ubuntu-linux/

2. Prepare virtual environment

    ```shell
    python3 -m venv /venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    ```

## Usage

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

## Adding a package 

```shell
pip3 install <package>
pip3 freeze > requirements.txt
```