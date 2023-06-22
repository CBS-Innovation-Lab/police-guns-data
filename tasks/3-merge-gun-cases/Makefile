GENERATED_FILES: output/gun_cases.csv

include ../../Makefile

output/gun_cases.csv: \
		src/extract_text.py \
		$(wildcard input/gun_cases/*)
	@$(PYTHON) $^ > $@

cleanup:
	rm -f output/*