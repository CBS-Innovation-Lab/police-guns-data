SHELL := /bin/bash

GENERATED_FILES: output/recovered_serials.csv

output/recovered_serials.csv: $(wildcard input/*)
	echo "source_file,serial" > $@
	for csv_file in $^ ; do \
		csvstack -H -g $(basename $$(basename $$csv_file)) $$csv_file | \
		awk "NR > 1" >> $@ ; \
	done

cleanup:
	rm -f output/*