SAM 			= sam
AWS				= aws
EVAL			= eval
UVICORN			= uvicorn
POETRY			= poetry
.PHONY			: install

.DEFAULT_GOAL	= help

# Colors stdout message
NO_COLOR		= \033[0m
ACTION			= \033[32;01m
RED          	:= $(shell tput -Txterm setaf 1)
MAGENTA        	:= $(shell tput -Txterm setaf 5)
BLUE        	:= $(shell tput -Txterm setaf 6)
RESET 			:= $(shell tput -Txterm sgr0)

help:
	@awk 'BEGIN {FS = ":.*##"; } /^[\.a-zA-Z0-9_-]+:.*?##/ { printf "$(ACTION)%-30s$(NO_COLOR) %s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort



install:
	$(info [*] Installing dev dependencies)
	python3 -m pip install --upgrade pip
	pip3 install -r requirements.txt

# Todo App
todo.install:
	$(info [*] Install todo package)
	cd todo-app && $(POETRY) install --without dev,test

todo.install-test-dependencies:
	$(info [*] Install test dependencies)
	cd todo-app && $(POETRY) install --with test,dev

todo.test:
	$(info [*] Build todo app tag docker container)
	cd todo-app && $(POETRY) run pytest

todo.build:
	$(info [*] Build todo app tag docker container)
	cd todo-app \
		&& docker build -t faboulaye/todo-api:latest .

todo.run:
	$(info [*] Start todo app server)
	cd todo-app && $(POETRY) run $(UVICORN) src.app:api --host 0.0.0.0 --port 8080 --reload

# CI/CD
ci.deploy: ## Deploy continuous integration pipeline
	$(info ${BLUE}[*] Deploy Continuous Integration pipeline ...${RESET})
	$(SAM) package --config-env ci
	$(SAM) deploy --config-env ci --no-fail-on-empty-changeset