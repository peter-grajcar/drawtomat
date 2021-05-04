FROM python:3.8.9-slim AS build

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y build-essential curl wget
RUN python3 -m venv ./venv
RUN venv/bin/pip3 install -r requirements.txt
RUN make udpipe
RUN make sklearn
RUN make fasttext


FROM python:3.8.9-slim

WORKDIR /app
COPY --from=build /app /app

ENV PYTHONPATH=/app/src
EXPOSE 5000
CMD venv/bin/gunicorn -b :5000 drawtomat.api:app
