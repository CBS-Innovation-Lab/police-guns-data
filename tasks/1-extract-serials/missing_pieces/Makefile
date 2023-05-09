GENERATED_FILES: output/missing_pieces.csv

include ../../../Makefile

output/missing_pieces.csv: \
		src/extract_search_data.py \
		input/missing_pieces_data_11-20-2017.csv
	$(PYTHON) $^ $@ > $@

cleanup:
	rm -f output/*