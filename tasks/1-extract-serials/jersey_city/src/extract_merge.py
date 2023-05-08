"""extracts data from jersey city data"""

import sys
import pandas as pd


def find_serial_number(colnames):
    """finds serial number column"""
    for colname in colnames:
        if "serial" in colname.lower():
            return colname
    return None


for filename in sys.argv[1:]:
    sheet_names = pd.ExcelFile(filename).sheet_names
    for sheet_name in sheet_names:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if len(df) == 0:
            continue
        
        serial_number = find_serial_number(df.columns)
        if serial_number:
            print(df[[serial_number]].to_csv(index=False, header=False))
