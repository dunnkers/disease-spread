FROM python:3.5-alpine3.11

RUN pip3 install -r requirements.txt

RUN mkdir /app

WORKDIR /app

ADD . .

ENTRYPOINT python3 main.py
