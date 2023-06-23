GENERATED_FILES: output/recap_docs.csv

include ../../Makefile

output/recap_docs.csv: \
		src/merge_docs.py \
		$(wildcard input/recap_docs/*)
	@$(PYTHON) $^ > $@

cleanup:
	rm -f output/*