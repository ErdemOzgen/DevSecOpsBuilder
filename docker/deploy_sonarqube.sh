#!/bin/bash
echo "Deploying SonarQube"
echo "Creating directories in $(pwd)"
mkdir -p ./docker/sonarqube_conf
mkdir -p ./docker/sonarqube_data
mkdir -p ./docker/sonarqube_extensions
mkdir -p ./docker/sonarqube_logs
#docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
docker-compose -f ./docker/docker-compose-sonarqube.yaml up -d
echo "SonarQube deployed"