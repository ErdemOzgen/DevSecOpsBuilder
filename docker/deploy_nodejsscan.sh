#!/bin/bash

echo "Deploying NodeJsScan"
docker pull opensecurity/nodejsscan:latest && docker run -it -p 9090:9090 opensecurity/nodejsscan:latest -n nodejsscan
echo "NodeJsScan deployed"



