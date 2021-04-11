#!/bin/bash

# x86
docker build -t omni:latest .
docker tag omni:latest mattogodoy/omni:latest
docker push mattogodoy/omni:latest

# ARM
docker build -f DockerfileARM -t omni:arm .
docker tag omni:arm mattogodoy/omni:arm
docker push mattogodoy/omni:arm
