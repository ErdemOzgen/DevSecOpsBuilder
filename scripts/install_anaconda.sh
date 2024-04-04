#!/bin/bash

# Anaconda installer download link
ANACONDA_URL="https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh"

# Function to check if Conda is installed
function is_conda_installed {
    if command -v conda &> /dev/null
    then
        echo "Conda is already installed."
        return 0
    else
        return 1
    fi
}

# Function to create Conda environment
function create_conda_env {
    env_name="redscan"
    python_version="3.11"

    # Check if the environment already exists
    if conda info --envs | grep -q "${env_name}"
    then
        echo "Conda environment '${env_name}' already exists. Using the same conda env."
    else
        # Create new environment
        echo "Creating Conda environment '${env_name}' with Python ${python_version}"
        conda create -n "${env_name}" python="${python_version}" -y
    fi

    # Make 'redscan' the default Conda environment
    echo "conda activate ${env_name}" >> ~/.bashrc
}

# Check if Conda is installed
if ! is_conda_installed
then
    # Download the installer
    wget $ANACONDA_URL -O anaconda.sh

    # Run the installer in silent mode
    bash anaconda.sh -b

    # Add Anaconda to PATH in .bashrc for future sessions
    echo 'export PATH=~/anaconda3/bin:$PATH' >> ~/.bashrc

    # Initialize Anaconda for current session
    export PATH=~/anaconda3/bin:$PATH
    ~/anaconda3/bin/conda init

    # Clean up
    rm anaconda.sh
fi

# Activate changes in .bashrc
source ~/.bashrc
# Create the Conda environment
create_conda_env
# Activate the environment
source ~/.bashrc
pip install -r requirements.txt