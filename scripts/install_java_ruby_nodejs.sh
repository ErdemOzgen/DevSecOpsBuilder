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
if ! command -v node &> /dev/null
then
    echo "Setting up Node.js..."
    # Replace 'X' with the version number you wish to install, e.g., '14' for Node.js 14
    curl -fsSL https://deb.nodesource.com/setup_X | sudo -E bash -
    sudo apt install -y nodejs npm
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