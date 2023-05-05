SHELL := /bin/bash

# DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
# export PROCESSOR_DIR := $(DIR)/processors

# TASKS := $(sort $(wildcard tasks/*))
# all: $(TASKS)

# $(TASKS):
#	$(MAKE) -C $@

setup: \
	.venv/bin/python \
	os-dependencies.log \
	git-lfs

git-lfs:
	git lfs install
	git lfs pull

os-dependencies.log: apt.txt
	sudo apt-get install -y $$(cat $<) > $@

.venv/bin/python: pyproject.toml poetry.toml
	poetry install

cleanup-all:
	find tasks -type f -path "*\output/*" -delete
