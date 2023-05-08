GENERATED_FILES: output/missing_pieces.csv

output/missing_pieces.csv: input/missing_pieces_data_11-20-2017.csv
	cat $< | csvcut -c "SERIAL NUMBER,DATE,AGENCY" | awk "NR > 1" > $@

cleanup:
	rm -f output/*