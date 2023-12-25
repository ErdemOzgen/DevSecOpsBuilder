#!/bin/bash

# Name of the conda environment
env_name="solidity_env"

# Check if the conda environment already exists
if conda info --envs | grep $env_name; then
    echo "Conda environment '$env_name' already exists. Activating it."
    conda activate $env_name
else
    # Create a new conda environment
    conda create -n $env_name python=3.8 -y
    echo "Created new conda environment: $env_name"
    conda activate $env_name
    echo "Activated conda environment: $env_name"
fi

# Install pip in the conda environment if not already installed
if ! command -v pip &> /dev/null; then
    conda install pip -y
    echo "Pip installed in the conda environment."
fi

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
