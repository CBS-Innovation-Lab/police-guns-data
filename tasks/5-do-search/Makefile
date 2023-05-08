GENERATED_FILES: output/matches.csv

output/matches.csv: \
		src/do_search.py \
		input/recovery_data.csv
	python $^ > $@

cleanup:
	rm -f output/*