#!/bin/bash
source ~/.bashrc
# Check if OpenJDK 11 JDK and JRE are installed
if ! java -version 2>&1 | grep -q "openjdk 11"
then
    echo "Installing OpenJDK 11 JDK and JRE..."
    sudo apt install openjdk-11-jdk openjdk-11-jre -y
else
    echo "OpenJDK 11 JDK and JRE are already installed."
fi

# Check if Node.js is installed
if ! command -v node > /dev/null 2>&1
then
    echo "Setting up Node.js..."
    ## Replace '20' with the version number you wish to install, e.g., '14' for Node.js 14
    ##curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
    NODE_MAJOR=20
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
    sudo apt-get update
    source ~/.bashrc
    sudo apt install -y nodejs
else
    echo "Node.js is already installed."
fi

echo "Updating package lists..."
sudo apt-get update -y

# Check if Ruby is installed
if ! command -v ruby &> /dev/null
then
    echo "Installing Ruby and RubyGems..."
    sudo apt-get install ruby-full rubygems -y
else
    echo "Ruby and RubyGems are already installed."
fi

echo "Setup completed successfully."
source ~/.bashrc