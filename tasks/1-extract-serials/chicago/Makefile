GENERATED_FILES: output/chicago.csv

include ../../../Makefile

output/chicago.csv: \
		$(PROCESSOR_DIR)/extract-serials.sh \
		input/18994-P766502-FirearmRecoveries-Victims-2000-Present.xlsx
	$^ "FIREARMS 2000-15JUL22" MAKE > $@

cleanup:
	rm -f output/*