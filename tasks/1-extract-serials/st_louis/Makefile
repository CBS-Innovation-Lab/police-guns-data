GENERATED_FILES: output/st_louis.csv

include ../../../Makefile

output/st_louis.csv: \
		$(PROCESSOR_DIR)/extract-serials.sh \
		input/Report_from_Lab.xlsx
	$^ Sheet1 "Evidence Description" > $@

cleanup:
	rm -f output/*