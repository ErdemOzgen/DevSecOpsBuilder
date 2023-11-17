# DevSecOpsBuilder
Automatic DevSecOps builder


# TODO

Add to end of project all systems has anaconda
```bash
    cd /tmp
	curl -O https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
	bash Anaconda3-2022.05-Linux-x86_64.sh
	sudo apt-get install ca-certificates curl gnupg
	sudo install -m 0755 -d /etc/apt/keyrings
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
	sudo chmod a+r /etc/apt/keyrings/docker.gpg
	# Add the repository to Apt sources:
	echo \
	  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
	  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
	  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update
	sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
	sudo systemctl start docker
	sudo systemctl enable docker
	sudo groupadd docker
	sudo usermod -aG docker $USER

```	

# Requirements

* Docker
* python = anaconda
* golang
* java 11 sudo apt install default-jre ==> apt install openjdk-17-jdk openjdk-17-jre
* pipx ggshield
* nodejs https://nodejs.org/en/download/package-manager
* sudo apt install make -y
* sudo apt-get install ruby-full rubygems


## Tools

1. git-leaks
2. git-hound
3. truffleHog
4. detect-secrets
5. ggshield
6. syft
7. dependency