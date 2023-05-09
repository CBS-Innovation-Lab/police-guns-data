GENERATED_FILES: output/cincinnati.csv

include ../../../Makefile

output/cincinnati.csv: \
		$(SRC_DIR)/extract_serials.py \
		input/Firearm_Records.xlsx
	$(PYTHON) $^ Sheet1 "SERIAL NO" \
		"MAKE/MODEL/CALIBER/BARREL LENGTH" \
		--agency_name "cincinnati police department" \
		> $@

cleanup:
	rm -f output/*