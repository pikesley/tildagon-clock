APP = $(shell basename $$(pwd))

all: format test clean

push: convert-conf
	python -m mpremote cp -r * :/apps/${APP}/

mkdir:
	python -m mpremote mkdir apps/${APP}

connect:
	python -m mpremote

deploy: push connect

convert-conf:
	@python scripts/conf_yaml_to_json.py

format:
	ruff format
	ruff check --fix

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .ruff_cache -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;

test:
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

install: guard-LIBRARY
	mkdir -p pikesley
	rsync --archive --verbose --exclude tests ../pikesley/${LIBRARY} pikesley/

build:
	docker build \
		--build-arg APP=${APP} \
		--tag ${APP} .

run:
	docker run \
		--name ${APP} \
		--hostname ${APP} \
		--volume $(shell pwd):/opt/${APP} \
		--interactive \
		--tty \
		--rm \
		${APP} \
		bash

guard-%:
	@if [ -z "${${*}}" ] ; \
    then \
        echo "You must provide the ${*} variable" ; \
        exit 1 ; \
    fi

-include Makefile.local
