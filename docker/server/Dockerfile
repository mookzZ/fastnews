FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/reqiurements.txt

RUN pip install --no-cache-dir --upgrade -r /app/reqiurements.txt

COPY . /app

RUN chmod +x /app/docker/server/server-entrypoint.sh