#!/bin/bash
set -e
python3 ./statisticService/consumer.py
echo $ENDPOINT_URL
exec "$@"