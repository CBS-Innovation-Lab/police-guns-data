GENERATED_FILES: output/chicago.csv

include ../../../Makefile

output/chicago.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/18994-P766502-FirearmRecoveries-Victims-2000-Present.xlsx
	python $^ "FIREARMS 2000-15JUL22" MAKE --agency_name "chicago police department" > $@

cleanup:
	rm -f output/*