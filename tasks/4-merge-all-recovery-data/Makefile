GENERATED_FILES: output/recovery_data.csv

output/recovery_data.csv: \
		input/recovered_serials.csv \
		input/gun_cases.csv
	csvstack $^ > $@

cleanup:
	rm -f output/*