GENERATED_FILES: output/chicago.csv

include ../../../Makefile

output/chicago.csv: \
		$(SRC_DIR)/extract_serials.py \
		input/18994-P766502-FirearmRecoveries-Victims-2000-Present.xlsx
	$(PYTHON) $^ "FIREARMS 2000-15JUL22" MAKE \
		MAKE \
		--agency_name "chicago police department" \
	> $@

cleanup:
	rm -f output/*