#!/bin/bash


echo "Installing OpenJDK 11 JDK and JRE..."
sudo apt install openjdk-11-jdk openjdk-11-jre -y

echo "Setting up Node.js..."
curl -fsSL https://deb.nodesource.com/setup_X | sudo -E bash -
sudo apt install -y nodejs npm

echo "Updating package lists..."
sudo apt-get update -y

echo "Installing Ruby and RubyGems..."
sudo apt-get install ruby-full rubygems -y

echo "Setup completed successfully."
