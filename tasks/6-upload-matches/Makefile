.PHONY: all upload

all: upload

include ../../Makefile

upload: \
		src/upload_matches.py \
		input/matches.csv
	$(PYTHON) $^ sale_serial sale_agency match_agency

cleanup:
	rm -f $(GENERATED_FILES)