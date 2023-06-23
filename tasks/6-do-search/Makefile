GENERATED_FILES: output/matches.csv

include ../../Makefile

output/matches.csv: \
		src/do_search.py \
		input/recovery_data.csv
	$(PYTHON) $^ > $@

cleanup:
	rm -f output/*