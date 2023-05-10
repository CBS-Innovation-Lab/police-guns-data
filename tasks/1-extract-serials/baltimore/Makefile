GENERATED_FILES: output/baltimore.csv

.PHONY: all cleanup

all: $(GENERATED_FILES)

include ../../../Makefile

output/baltimore.csv: \
		$(SRC_DIR)/extract_serials.py \
		input/BaltimoreRecoveredGuns.xlsx
	$(PYTHON) $^ Sheet1 SERIAL_NO MAKE,MODEL \
		--date_col DATE_IN \
		--agency_name "baltimore police department" \
	> $@

cleanup:
	rm -f output/*