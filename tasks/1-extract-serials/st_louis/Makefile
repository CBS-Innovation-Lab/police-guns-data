GENERATED_FILES: output/st_louis.csv

include ../../../Makefile

output/st_louis.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/Report_from_Lab.xlsx
	python $^ Sheet1 "Evidence Description" \
		--date_col KeyIn_Dt \
		--agency_name "st louis police department" \
	> $@

cleanup:
	rm -f output/*