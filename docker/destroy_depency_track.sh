#!/bin/bash

echo "Deploying Dependency Track"
docker-compose -f ./docker/docker-compose-depency-track.yml down
echo "Dependency Track deployed"

