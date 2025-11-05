#!/bin/bash
set -a
source .env
set +a

docker run -d \
  --name web-app \
  --restart unless-stopped \
  --network host \
  -e INFLUX_URL \
  -e INFLUX_TOKEN \
  -e INFLUX_ORG \
  smart_kip_web_app