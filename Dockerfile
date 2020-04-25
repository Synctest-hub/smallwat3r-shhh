FROM alpine:latest

# musl-dev gcc
RUN apk update && \
    apk add build-base python3 python3-dev libffi-dev libressl-dev postgresql-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 usr/bin/pip && \
    pip install --upgrade pip

RUN mkdir -p /var/log/celery/ /var/run/celery/ /var/log/shhh/
RUN addgroup app && \
    adduser --disabled-password --gecos "" --ingroup app app && \
    chown app:app /var/run/celery/ && \
    chown app:app /var/log/celery/ && \
    chown app:app /var/log/shhh/

USER app

ENV PATH="/home/app/.local/bin:${PATH}"
WORKDIR app/

COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY shhh shhh

ENV FLASK_APP=shhh
