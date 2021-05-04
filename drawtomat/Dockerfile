FROM python:3.8.9-slim AS build
WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential curl wget && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN python3 -m venv venv
RUN make udpipe
RUN make sklearn
RUN make fasttext
RUN venv/bin/pip3 install -r requirements.txt


FROM debian:buster-slim
WORKDIR /app

COPY --from=build /app /app

ENV PYTHONPATH=/app/src
EXPOSE 5000
CMD venv/bin/gunicorn -b :5000 drawtomat.api:app
