#!/bin/bash

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
