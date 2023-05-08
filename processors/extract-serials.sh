#!/bin/bash

# This script accepts a file name and a sheet name as arguments
# and performs the following actions:
# - Converts the sheet to CSV format using in2csv
# - Selects the MAKE column using csvcut
# - Skips the header row using awk
# - Writes the output to a new file

# Check that the correct number of arguments have been provided
if [ $# -ne 3 ]; then
    echo "Usage: $0 <filename> <sheetname> <colname>"
    exit 1
fi

# Assign the arguments to variables
filename="$1"
sheetname="$2"
colname="$3"

# Convert the sheet to CSV format using in2csv
in2csv --sheet "$sheetname" "$filename" |
    # Select the column using csvcut
    csvcut -c "$colname" |
    # Skip the header row using awk
    awk 'NR > 1'
