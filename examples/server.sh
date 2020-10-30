#!/bin/sh

# wait for the kafka-broker docker to be running
while ! nc kafka-broker 9092; do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 1
done

>&2 echo "Kafka port is open - will start server soon"

sleep 20

gunicorn -b "0.0.0.0:8082" -w 1 examples.server:app --worker-class aiohttp.GunicornWebWorker
