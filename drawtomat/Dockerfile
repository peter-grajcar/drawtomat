FROM python:3.8.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential curl wget
RUN make udpipe
RUN make sklearn
RUN make fasttext
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH=/app/src

CMD gunicorn -b :5000 drawtomat.api:app
