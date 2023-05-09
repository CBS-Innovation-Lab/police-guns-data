GENERATED_FILES: output/el_paso.csv

include ../../../Makefile

output/el_paso.csv: \
		$(SRC_DIR)/extract_serials.py \
		input/ORR_W113392-911ANALYST30.xlsx
	$(PYTHON) $^ Firearms DESCRIPTION \
		DESCRIPTION \
		--date_col "CREATED_ON" \
		--agency_name "el paso police department" \
		> $@

cleanup:
	rm -f output/*