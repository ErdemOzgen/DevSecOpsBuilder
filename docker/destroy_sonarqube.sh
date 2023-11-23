#!/bin/bash
echo "Destorying SonarQube"
docker-compose -f ./docker/docker-sonarqube.yml down
echo "SonarQube destroyed"