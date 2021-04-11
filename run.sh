#!/bin/bash

docker run \
    -e OMNI_DATA_RATE_SECONDS=1 \
    -e OMNI_HOST_NAME=test \
    -e OMNI_HOST_IP=0.0.0.0 \
    --rm \
    -it \
    -v "/:/rootfs:ro" \
    omni:latest
