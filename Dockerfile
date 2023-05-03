FROM python:3.10-alpine as build

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --no-cache python3 python3-dev gcc g++ curl bash

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY sh .

COPY cli.py .
COPY config.py .
COPY minigpt4 .
COPY eval_configs .
