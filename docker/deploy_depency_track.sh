#!/bin/bash

echo "Deploying Dependency Track"
docker-compose -f ./docker/docker-compose-depency-track.yml up -d
echo "Dependency Track deployed"

