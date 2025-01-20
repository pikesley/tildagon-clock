APP = $(shell basename $$(pwd))

all: format test clean

push:
	python -m mpremote cp -r * :/apps/${APP}/

mkdir:
	python -m mpremote mkdir apps/${APP}

connect:
	python -m mpremote

format:
	ruff format
	ruff check --fix

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .ruff_cache -exec rm -fr {} \;

test:
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

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
