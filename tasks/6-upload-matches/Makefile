GENERATED_FILES: upload_matches.log

upload_matches.log: \
		src/upload_matches.py \
		input/matches.csv
	python $^ sale_serial sale_agency match_agency

cleanup:
	rm -f $(GENERATED_FILES)