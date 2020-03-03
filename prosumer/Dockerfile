FROM python:3.5-alpine3.11

RUN mkdir /app

WORKDIR /app

ADD . .

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 main.py