# This Makefile is used to build and manage containers using docker-compose files.
# It provides various targets for different operations such as building services, starting services, pulling Docker images, stopping services, etc.
#     ____            _____           ____             ____        _ __    __         
#    / __ \___ _   __/ ___/___  _____/ __ \____  _____/ __ )__  __(_) /___/ /__  _____
#   / / / / _ \ | / /\__ \/ _ \/ ___/ / / / __ \/ ___/ __  / / / / / / __  / _ \/ ___/
#  / /_/ /  __/ |/ /___/ /  __/ /__/ /_/ / /_/ (__  ) /_/ / /_/ / / / /_/ /  __/ /    
# /_____/\___/|___//____/\___/\___/\____/ .___/____/_____/\__,_/_/_/\__,_/\___/_/     
#                                      /_/                                           

.DEFAULT_GOAL:=help
.PHONY: up build username pull down stop restart rm logs test clean lab cleanlab cleanoutput outputs pip
# This for future release of Compose that will use Docker Buildkit, which is much efficient.
COMPOSE_PREFIX_CMD := COMPOSE_DOCKER_CLI_BUILD=1

COMPOSE_ALL_FILES := -f docker-compose.yml
SERVICES          := #db web proxy redis celery celery-beat
PYTHON=python #Uses python3 using anaconda therefore default python is python3
PIP=pip3
# --------------------------

# Installs the necessary dependencies and tools.
setup: ## Installs the necessary dependencies and tools run as sudo.
	sudo apt-get install build-essential -y
	sudo apt update -y
	chmod +x ./scripts/*.sh
	@./scripts/install_docker_go.sh
	@./scripts/install_anaconda.sh
	@./scripts/install_java_ruby_nodejs.sh
	@make outputs
	$(PIP) install -r requirements.txt
	mkdir -p ~/bin
	cp -r ./docker/* ~/bin/
	chmod +x ~/bin/cleardocker*
	chmod +x ~/bin/*.sh
	echo 'export PATH="$${HOME}/bin:$$PATH"' >> ~/.bashrc

aftersetup: ## Installs do not run as sudo.
	@make outputs
	$(PIP) install -r requirements.txt
	mkdir -p ~/bin
	cp -r ./docker/* ~/bin/
	chmod +x ~/bin/cleardocker*
	chmod +x ~/bin/*.sh
	echo 'export PATH="$${HOME}/bin:$$PATH"' >> ~/.bashrc



# Builds and starts all services.
up:				## Build and start all services.
	bash ./docker/deploy_*.sh
#${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} up -d --build ${SERVICES}

# Builds all services.
build:			## Build all services.
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} build ${SERVICES}

# Pulls Docker images.
pull:			## Pull Docker images.
	docker login
	${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} pull

# Stops all services.
down:			## Down all services.
	bash ./docker/destroy_*.sh
#${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} down

# Stops all services.
stop:			## Stop all services.
	docker stop $(docker ps -q)
	
#${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} stop ${SERVICES}

# Restarts all services.
restart:		## Restart all services.
	docker restart $(docker ps -q)

#${COMPOSE_PREFIX_CMD} docker-compose ${COMPOSE_ALL_FILES} restart ${SERVICES}

# Removes all services containers.
rm:				## Remove all services containers.
	docker rm -f $$(docker ps -a -q)
#${COMPOSE_PREFIX_CMD} docker-compose $(COMPOSE_ALL_FILES) rm -f ${SERVICES}

# Runs unit tests.
test: ## Runs unit tests.
	$(PYTHON) -m unittest discover -s test/

# Tails all logs with -n 1000.
logs:			## Opens lazydocker for logs.
	lazydocker
#${COMPOSE_PREFIX_CMD} docker-compose $(COMPOSE_ALL_FILES) logs --follow --tail=1000 ${SERVICES}

# Shows all Docker images.
images:			## Show all Docker images.
	${COMPOSE_PREFIX_CMD} docker-compose $(COMPOSE_ALL_FILES) images ${SERVICES}

# Removes containers and deletes volume data.
prune:			## Remove containers and delete volume data.
	@make stop && make rm && docker volume prune -f

# Cleans up unnecessary files.
clean: ## Cleans up unnecessary files.
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# Clones repositories for lab purposes.
lab: ## Clones repositories for lab purposes.
	@echo "Cloning repositories..."
	@mkdir -p lab
	@test -d lab/SecretsTest || git clone https://github.com/BonJarber/SecretsTest.git lab/SecretsTest
	@test -d lab/DVWA || git clone https://github.com/digininja/DVWA.git lab/DVWA
	@test -d lab/lambhack || git clone https://github.com/wickett/lambhack.git lab/lambhack
	@test -d lab/NodeGoat || git clone https://github.com/OWASP/NodeGoat.git lab/NodeGoat
	@test -d lab/DVSA || git clone https://github.com/OWASP/DVSA.git lab/DVSA
	@test -d lab/railsgoat || git clone https://github.com/OWASP/railsgoat.git lab/railsgoat
	@test -d lab/WebGoat || git clone https://github.com/WebGoat/WebGoat.git lab/WebGoat
	@test -d lab/WebGoat.NET || git clone https://github.com/OWASP/WebGoat.NET.git lab/WebGoat.NET
	@test -d lab/OWASPWebGoatPHP || git clone https://github.com/OWASP/OWASPWebGoatPHP.git lab/OWASPWebGoatPHP
	@test -d lab/vulnado || git clone https://github.com/ScaleSec/vulnado.git lab/vulnado

# Cleans up lab repositories.
cleanlab:
	echo "Cleaning Test Secret Scanner repo"
	cd lab && rm -rf *

# Creates necessary directories for command outputs.
outputs: ## Creates necessary directories for command outputs.
	mkdir -p command_outputs
	mkdir -p command_outputs/git-secrets
	mkdir -p command_outputs/SBOM
	mkdir -p command_outputs/outputs
	mkdir -p command_outputs/jenkinsFiles/
	mkdir -p command_outputs/graphs/
	mkdir -p command_outputs/scanner/
	mkdir -p command_outputs/SAST/

# Cleans up command outputs.
cleanoutput: ## Cleans up command outputs.
	echo "Cleaning Outputs"
	cd command_outputs && rm -rf */


	

# Shows the help message.
help:			## Show this help.
	@echo "----------------------"
	@echo "▐▓█▀▀▀▀▀▀▀▀▀█▓▌░▄▄▄▄▄░"
	@echo "▐▓█░░▀░░▀▄░░█▓▌░█▄▄▄█░"
	@echo "▐▓█░░▄░░▄▀░░█▓▌░█▄▄▄█░"
	@echo "▐▓█▄▄▄▄▄▄▄▄▄█▓▌░█████░"
	@echo "░░░░▄▄███▄▄░░░░░█████░"
	@echo "----------------------"
	@echo "DevSecOps Builder"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)