#!/bin/bash

# Check for solc
if ! command -v solc &> /dev/null; then
    echo "solc not found, installing..."
    sudo add-apt-repository ppa:ethereum/ethereum -y
    sudo apt-get update -y
    sudo apt-get install solc -y
else
    echo "solc is already installed."
fi

# Check for solc-select
if ! pip list | grep solc-select &> /dev/null; then
    echo "solc-select not found, installing..."
    pip install solc-select
    solc-select install latest
    solc-select use 0.8.23
else
    echo "solc-select is already installed."
fi

echo "Installation and setup complete."
