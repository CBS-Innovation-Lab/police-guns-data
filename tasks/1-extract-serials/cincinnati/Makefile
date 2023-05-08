GENERATED_FILES: output/cincinnati.csv

include ../../../Makefile

output/cincinnati.csv: \
		$(PROCESSOR_DIR)/extract-serials.sh \
		input/Firearm_Records.xlsx
	$^ Sheet1 "SERIAL NO" > $@

cleanup:
	rm -f output/*