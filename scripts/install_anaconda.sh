#!/bin/bash

# This script installs Anaconda, a popular Python distribution, on a Linux system.
# It downloads the Anaconda installer from the specified URL, runs the installer in silent mode,
# adds Anaconda to the system's PATH, initializes Anaconda for the current session,
# creates a Conda environment named 'redscan' with Python version 3.11 (if it doesn't already exist),
# and sets 'redscan' as the default Conda environment.
# The script also includes functions to check if Conda is installed and to create the Conda environment.

# Anaconda installer download link
ANACONDA_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"

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

# Function to check if Conda is installed
function check_conda_installed {
    if ! command -v conda &> /dev/null
    then
        echo "Conda could not be found, please install it first."
        exit 1
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
        # No need to exit here, we can proceed to make it the default environment
    else
        # Create new environment
        echo "Creating Conda environment '${env_name}' with Python ${python_version}"
        conda create -n "${env_name}" python="${python_version}" -y
    fi

    # Make 'redscan' the default Conda environment
    echo "conda activate ${env_name}" >> ~/.bashrc
}

# Check if Conda is installed
check_conda_installed

# Create the Conda environment
create_conda_env
