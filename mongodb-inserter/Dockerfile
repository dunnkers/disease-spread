# FROM python:3.5-alpine3.11
FROM jupyter/scipy-notebook:latest

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN rm requirements.txt

RUN mkdir /home/jovyan/app

WORKDIR /home/jovyan/app

ADD . .

# ENTRYPOINT python3 main.py