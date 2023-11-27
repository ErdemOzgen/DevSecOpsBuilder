#!/bin/bash
source ~/.bashrc
# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker not found, installing..."

    # Add Docker's official GPG key and repository
    sudo apt-get update -y
    sudo apt-get install ca-certificates curl gnupg -y
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    # Add the repository to Apt sources
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
    sudo groupadd docker
    sudo usermod -aG docker $USER
    sudo apt install gcc -y && sudo apt install build-essential -y
    sudo apt install docker-compose -y

    echo "Docker installation complete."
else
    echo "Docker is already installed."
fi

# Check if Go is installed
if ! command -v go &> /dev/null
then
    echo "Go not found, installing..."
    
    # URL of the Go binary
    GO_BINARY_URL="https://go.dev/dl/go1.21.4.linux-amd64.tar.gz"

    # Download the Go binary
    wget $GO_BINARY_URL -O go.tar.gz

    # Remove any existing Go installation
    sudo rm -rf /usr/local/go

    # Extract the downloaded Go binary to /usr/local
    sudo tar -C /usr/local -xzf go.tar.gz

    # Clean up the downloaded file
    rm go.tar.gz

    # Add Go binary paths to PATH
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    echo 'export PATH=$PATH:/home/$USER/go/bin' >> ~/.bashrc

    # Apply changes to current session
    source ~/.bashrc

    echo "Go installation and PATH update complete."
else
    echo "Go is already installed."
fi

# Check if LAZYDOCKER is installed
if ! command -v lazydocker &> /dev/null
then
    echo "LAZYDOCKER not found, installing..."

    # Install LAZYDOCKER
    LAZYDOCKER_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazydocker/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+')
    curl -Lo lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/latest/download/lazydocker_${LAZYDOCKER_VERSION}_Linux_x86_64.tar.gz"
    mkdir lazydocker-temp
    tar xf lazydocker.tar.gz -C lazydocker-temp
    sudo mv lazydocker-temp/lazydocker /usr/local/bin
    rm -rf lazydocker.tar.gz lazydocker-temp

    echo "LAZYDOCKER Installed"
else
    echo "LAZYDOCKER is already installed."
fi
source ~/.bashrc