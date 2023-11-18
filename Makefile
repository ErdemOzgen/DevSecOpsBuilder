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
	# Set PATH for the duration of this recipe
	export PATH="/usr/local/go/bin:/home/erdem/bin:/home/erdem/go/bin:$$PATH"; \
	curl -L https://go.dev/dl/go1.21.4.linux-amd64.tar.gz -o go1.21.4.linux-amd64.tar.gz; \
	sudo rm -rf /usr/local/go; \
	sudo tar -C /usr/local -xzf go1.21.4.linux-amd64.tar.gz; \
	sudo apt update -y; \
	sudo apt install openjdk-11-jdk openjdk-11-jre; \
	curl -fsSL https://deb.nodesource.com/setup_X | sudo -E bash -; \
	sudo apt install -y nodejs; \
	sudo apt-get install -y nodejs; \
	sudo apt-get update -y; \
	sudo apt-get install ruby-full rubygems -y
	docker pull erdemozgen/blackcart:latest




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
	mkdir -p lab
	cd lab && { \
		echo "Cloning repositories..."; \
		test -d SecretsTest || git clone https://github.com/BonJarber/SecretsTest.git; \
		test -d DVWA || git clone https://github.com/digininja/DVWA.git; \
		test -d lambhack || git clone https://github.com/wickett/lambhack.git; \
		test -d NodeGoat || git clone https://github.com/OWASP/NodeGoat.git; \
		test -d DVSA || git clone https://github.com/OWASP/DVSA.git; \
		test -d railsgoat || git clone https://github.com/OWASP/railsgoat; \
		test -d WebGoat || git clone https://github.com/WebGoat/WebGoat; \
		test -d WebGoat.NET || git clone https://github.com/OWASP/WebGoat.NET.git; \
		test -d OWASPWebGoatPHP || git clone https://github.com/OWASP/OWASPWebGoatPHP.git; \
		test -d vulnado || git clone https://github.com/ScaleSec/vulnado.git; \
	}



cleanlab:
	echo "Cleaning Test Secret Scanner repo"
	cd lab && rm -rf *
cleanoutput:
	echo "Cleaning Test Secret Scanner repo"
	cd command_outputs && rm -rf *.txt

help:			## Show this help.
	@echo "Make application docker images and manage containers using docker-compose files."
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)