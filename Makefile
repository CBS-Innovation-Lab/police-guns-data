SHELL := /bin/bash

DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
export PYTHON := $(DIR)/.venv/bin/python
export SRC_DIR := $(DIR)/src

TASKS := $(sort $(wildcard tasks/*))

.PHONY: \
	all \
	$(TASKS) \
	init \
	cleanup-all

all: $(TASKS) $(NOTEBOOKS)

$(TASKS):
	$(MAKE) -C $@

setup: \
	.venv/bin/python \
	os-dependencies.log \
	git-lfs

git-lfs:
	git lfs install
	git lfs pull

<<<<<<< HEAD
os-dependencies.log: apt.txt
	sudo apt-get install -y $$(cat $<) > $@

.venv/bin/python: pyproject.toml poetry.toml
	poetry install

cleanup-all:
	find tasks -type f -path "*\output/*" -delete
=======
# os-dependencies.log is a file that contains the output of
# installing a list of packages that I commonly use and want to
# always be installed on my vm
os-dependencies.log: apt.txt
	sudo apt-get install -y $$(cat $<) > $@

# creates a virtual environment
.venv/bin/python: pyproject.toml poetry.toml
	poetry install
>>>>>>> template/main
