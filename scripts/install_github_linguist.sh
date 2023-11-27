#!/bin/bash
source ~/.bashrc
# Check if Ruby is installed
if ! command -v ruby &> /dev/null
then
    echo "Ruby not found, installing..."
    sudo apt-get install ruby-full -y
else
    echo "Ruby is already installed."
fi

# Check if RubyGems is installed
if ! command -v gem &> /dev/null
then
    echo "RubyGems not found, installing..."
    sudo apt-get install rubygems -y
else
    echo "RubyGems is already installed."
fi

# Install necessary build tools
echo "Installing build tools..."
sudo apt-get install build-essential cmake pkg-config libicu-dev zlib1g-dev libcurl4-openssl-dev libssl-dev ruby-dev -y

# Check if github-linguist is installed
if ! gem list -i github-linguist &> /dev/null
then
    echo "Installing github-linguist..."
    sudo gem install github-linguist
else
    echo "github-linguist is already installed."
fi
source ~/.bashrc