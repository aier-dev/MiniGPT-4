FROM ubuntu

# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

RUN apt-get update && apt-get install -y gcc g++ bash curl git make build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev ffmpeg libsm6 libxext6

RUN curl https://rtx.pub/install.sh | sh

RUN mkdir -p /app
WORKDIR /app

COPY .tool-versions .

ENV PATH /root/.local/share/rtx/bin:$PATH

RUN rtx install

COPY requirements.txt .
RUN eval $(rtx env) && pip install -r requirements.txt && pip install decord

COPY cli.py .
COPY config.py .
COPY env.py .
COPY minigpt4 minigpt4
COPY eval_configs eval_configs

# COPY sh .
# RUN ./sh/sharp.sh
