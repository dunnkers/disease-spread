## Install

1. Run Spark.

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

## Adding a package 

```shell
pip3 install <package>
pip3 freeze > requirements.txt
```