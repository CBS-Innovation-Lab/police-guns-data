GENERATED_FILES: output/miami.csv

include ../../../Makefile

output/miami.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/W032780_fiream_public_record_request_redacted.xlsx
	python $^ "FileOnQ Export" AdditionalDescription \
		--date_col "OffenseDate" \
		--agency_name "miami police department" \
	> $@

cleanup:
	rm -f output/*