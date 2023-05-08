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


def find_make_model_caliber_columns(colnames):
    """finds make, model, caliber columns in colnames"""
    make = None
    model = None
    caliber = None
    for colname in colnames:
        if "make" in colname.lower():
            make = colname
        if "model" in colname.lower():
            model = colname
        if "caliber" in colname.lower():
            caliber = colname
    return make, model, caliber


for filename in sys.argv[1:]:
    sheet_names = pd.ExcelFile(filename).sheet_names
    for sheet_name in sheet_names:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if len(df) == 0:
            continue

        serial_col = find_serial_col(df.columns)
        date_col = find_date_col(df.columns)
        make_col, model_col, caliber_col = find_make_model_caliber_columns(df.columns)
        if serial_col and date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df = df.assign(
                agency="el paso police department",
                description=lambda df: df.apply(
                    lambda row: " ".join([str(x) for x in row]), axis=1
                ),
            )
            print(
                df[[serial_col, date_col, "agency", "description"]].to_csv(
                    index=False, header=False
                )
            )
