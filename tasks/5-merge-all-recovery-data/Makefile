GENERATED_FILES: output/recovery_data.csv

include ../../Makefile

output/recovery_data.csv: \
		src/concat_files.py \
		input/recovered_serials.csv \
		input/gun_cases.csv \
		input/recap_docs.csv
	$(PYTHON) $^ > $@

cleanup:
	rm -f output/*