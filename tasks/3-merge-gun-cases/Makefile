GENERATED_FILES: output/gun_cases.csv

include ../../Makefile

output/gun_cases.csv: \
		src/extract_text.py \
		$(wildcard input/*)
	@$(PYTHON) $^ > $@

cleanup:
	rm -f output/*