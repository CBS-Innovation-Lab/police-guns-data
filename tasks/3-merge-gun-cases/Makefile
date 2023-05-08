GENERATED_FILES: output/gun_cases.csv

output/gun_cases.csv: \
		src/extract_text.py \
		$(wildcard input/*)
	@python $^ > $@

cleanup:
	rm -f output/*