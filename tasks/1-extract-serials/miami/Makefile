GENERATED_FILES: output/miami.csv

include ../../../Makefile

output/miami.csv: \
		$(PROCESSOR_DIR)/extract-serials.sh \
		input/W032780_fiream_public_record_request_redacted.xlsx
	$^ "FileOnQ Export" AdditionalDescription > $@

cleanup:
	rm -f output/*