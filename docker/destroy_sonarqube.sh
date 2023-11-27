#!/bin/bash
echo "Destorying SonarQube"
docker-compose -f ./docker/docker-compose-sonarqube.yaml down
echo "SonarQube destroyed"