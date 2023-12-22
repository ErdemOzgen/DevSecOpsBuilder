#!/bin/bash
echo "Destroying SonarQube"
docker-compose -f ./docker/docker-compose-sonarqube.yaml down
echo "SonarQube destroyed"