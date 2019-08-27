FROM python:3.7.4-alpine3.10

RUN set -ex && \
    mkdir /var/opt/app && \
    apk add --no-cache \
    build-base \
    wget \
    git

WORKDIR /var/opt/app

ADD . /var/opt/app

RUN set -ex && \
    pip install -r requirements.txt

CMD ["python", "./run.py"]
