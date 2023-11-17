.DEFAULT_GOAL:=help


# This for future release of Compose that will use Docker Buildkit, which is much efficient.
COMPOSE_PREFIX_CMD := COMPOSE_DOCKER_CLI_BUILD=1

COMPOSE_ALL_FILES := -f docker-compose.yml
SERVICES          := #db web proxy redis celery celery-beat
PYTHON=python
PIP=pip3
# --------------------------

.PHONY: up build username pull down stop restart rm logs test clean lab cleanlab cleanoutput


setup:
	sudo apt-get install build-essential -y
	$(PIP) install -r requirements.txt
	sudo apt update -y
	# Add Docker's official GPG key:
	sudo apt-get update
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
	export PATH := /usr/local/go/bin:$(HOME)/bin:$(HOME)/go/bin:$(PATH)
	sudo apt update -y
	wget https://go.dev/dl/go1.21.4.linux-amd64.tar.gz
	sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.4.linux-amd64.tar.gz
	sudo apt update -y
	sudo apt install openjdk-11-jdk openjdk-11-jre
	curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
	sudo apt install -y nodejs
	sudo apt-get install -y nodejs
	sudo apt-get update -y
	sudo apt-get install ruby-full rubygems -y



up:				## Build and start all services.
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} up -d --build ${SERVICES}

build:			## Build all services.
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} build ${SERVICES}

pull:			## Pull Docker images.
	docker login
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} pull

down:			## Down all services.
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} down

stop:			## Stop all services.
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} stop ${SERVICES}

restart:		## Restart all services.
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} restart ${SERVICES}

rm:				## Remove all services containers.
	${COMPOSE_PREFIX_CMD} docker-compose $(COMPOSE_ALL_FILES) rm -f ${SERVICES}

test:
	$(PYTHON) -m unittest discover -s test/

logs:			## Tail all logs with -n 1000.
	${COMPOSE_PREFIX_CMD} docker-compose $(COMPOSE_ALL_FILES) logs --follow --tail=1000 ${SERVICES}

images:			## Show all Docker images.
	${COMPOSE_PREFIX_CMD} docker-compose $(COMPOSE_ALL_FILES) images ${SERVICES}

prune:			## Remove containers and delete volume data.
	@make stop && make rm && docker volume prune -f

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

lab:
	echo "Cloning Test Secret Scanner repo"
	mkdir -p  lab && cd lab && git clone https://github.com/BonJarber/SecretsTest.git
	echo "Cloning Test DVWA repo"
	git clone https://github.com/digininja/DVWA.git
	echo "Cloning Test lambhack repo"
	git clone https://github.com/wickett/lambhack.git
	echo "Cloning Test NodeGoat repo"
	git clone https://github.com/OWASP/NodeGoat.git
	echo "Cloning Test DVSA repo"
	git clone https://github.com/OWASP/DVSA.git
	echo "Cloning Test railsgoat repo"
	git clone https://github.com/OWASP/railsgoat
	echo "Cloning Test WebGoat repo"
	git clone https://github.com/WebGoat/WebGoat
	echo "Cloning Test WebGoat.NET repo"
	git clone https://github.com/OWASP/WebGoat.NET.git
	echo "Cloning Test WebGoat.PHP repo"
	git clone https://github.com/OWASP/OWASPWebGoatPHP.git
	echo "Cloning Test  JAVA vulnado repo"
	git clone https://github.com/ScaleSec/vulnado.git


cleanlab:
	echo "Cleaning Test Secret Scanner repo"
	cd lab && rm -rf *
cleanoutput:
	echo "Cleaning Test Secret Scanner repo"
	cd command_outputs && rm -rf *.txt

help:			## Show this help.
	@echo "Make application docker images and manage containers using docker-compose files."
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)