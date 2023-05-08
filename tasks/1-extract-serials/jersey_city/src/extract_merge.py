"""extracts data from jersey city data"""

import sys
import pandas as pd


def find_serial_col(colnames):
    """finds serial number column"""
    for colname in colnames:
        if "serial" in colname.lower():
            return colname
    return None


def find_date_col(colnames):
    """finds date column"""
    for colname in colnames:
        if "date" in colname.lower():
            return colname
    return None


for filename in sys.argv[1:]:
    sheet_names = pd.ExcelFile(filename).sheet_names
    for sheet_name in sheet_names:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if len(df) == 0:
            continue

        serial_col = find_serial_col(df.columns)
        date_col = find_date_col(df.columns)
        if serial_col and date_col:
            df = df.assign(agency="el paso police department")
            print(
                df[[serial_col, date_col, "agency"]].to_csv(index=False, header=False)
            )
