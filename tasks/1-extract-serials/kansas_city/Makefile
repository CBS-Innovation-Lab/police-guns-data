SHELL := /bin/bash

GENERATED_FILES: output/kansas_city.csv

include ../../../Makefile

output/kansas_city.csv: \
		$(PROCESSOR_DIR)/extract_serials.py \
		input/CFR157_Recovered_Guns_Tiburon.xlsx \
		input/NPR018_Recovered_Firearms_Niche.xlsx
	python $(PROCESSOR_DIR)/extract_serials.py input/CFR157_Recovered_Guns_Tiburon.xlsx Sheet1 Description \
		--date_col "Reported Date" \
		--agency_name "kansas city police department" \
	> $@
	
	python $(PROCESSOR_DIR)/extract_serials.py input/NPR018_Recovered_Firearms_Niche.xlsx Sheet1 Description \
		--date_col "Reported Date/Time" \
		--agency_name "kansas city police department" \
	>> $@

cleanup:
	rm -f output/*