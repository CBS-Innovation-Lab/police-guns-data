GENERATED_FILES: output/cincinnati.csv

include ../../../Makefile

output/cincinnati.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/Firearm_Records.xlsx
	python $^ Sheet1 "SERIAL NO" > $@

cleanup:
	rm -f output/*