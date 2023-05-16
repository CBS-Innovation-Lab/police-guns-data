GENERATED_FILES: output/indianapolis.csv

include ../../../Makefile

output/indianapolis.csv: \
		$(SRC_DIR)/extract_serials.py \
		input/DP_Case_Numbers_2012-2019.xlsx \
		input/IP_Case_Numbers_2017-2022.xlsx
	$(PYTHON) $< input/DP_Case_Numbers_2012-2019.xlsx \
		Sheet1 \
		Ser \
		CaseNo,Make,Model,Cal,TYPE \
		--agency_name "indianapolis metropolitan police department" \
	> $@

	$(PYTHON) $< input/IP_Case_Numbers_2017-2022.xlsx \
		Sheet1\
		Ser \
		CaseNo,Make,Model,Cal,TYPE \
		--agency_name "indianapolis metropolitan police department" \
	>> $@

cleanup:
	rm -f output/*