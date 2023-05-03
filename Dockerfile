FROM python:3.10-alpine as build

# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

RUN apk add --no-cache python3 python3-dev gcc g++ curl bash

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN python -m venv .py && source ./.py/bin/activate && pip install -r requirements.txt

# COPY sh .
# RUN ./sh/sharp.sh

COPY cli.py .
COPY config.py .
COPY minigpt4 .
COPY eval_configs .
