SHELL := /bin/bash

GENERATED_FILES: output/jersey_city.csv

include ../../../Makefile

output/jersey_city.csv: \
		src/extract_merge.py \
		$(wildcard input/*)
	$(PYTHON) $^ > $@

cleanup:
	rm -f output/*