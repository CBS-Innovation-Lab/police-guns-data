GENERATED_FILES: output/recovery_data.csv

output/recovery_data.csv: $(wildcard input/*)
	csvstack $^ > $@

cleanup:
	rm -f output/*