GENERATED_FILES: output/el_paso.csv

include ../../../Makefile

output/el_paso.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/ORR_W113392-911ANALYST30.xlsx
	python $^ Firearms DESCRIPTION > $@

cleanup:
	rm -f output/*