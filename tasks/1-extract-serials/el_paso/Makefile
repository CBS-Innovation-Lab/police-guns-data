GENERATED_FILES: output/el_paso.csv

include ../../../Makefile

output/el_paso.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/ORR_W113392-911ANALYST30.xlsx
	python $^ Firearms DESCRIPTION \
		--date_col "CREATED_ON" \
		--agency_name "el paso police department" \
		> $@

cleanup:
	rm -f output/*