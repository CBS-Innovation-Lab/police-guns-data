"""assigns a description column"""

import sys
import pandas as pd


def get_description(row):
    """generates a description based on row data"""
    desc = ""
    if pd.notna(row["STATUS"]):
        desc += f'[{row["STATUS"]}]'
    if pd.notna(row["OFFENSE"]):
        desc += f' [{row["OFFENSE"]}]'
    if pd.notna(row["MAKE"]):
        desc += f" {row['MAKE']}"
    if pd.notna(row["MODEL"]):
        desc += f" {row['MODEL']}"
    if pd.notna(row["PROPERTY_DESCRIPTION"]):
        desc += f" {row['PROPERTY_DESCRIPTION']}"
    return desc


df = pd.read_csv(sys.argv[1])
df["description"] = df.apply(get_description, axis=1)
df[["SERIAL NUMBER", "DATE", "AGENCY", "description"]].to_csv(
    sys.argv[2], index=False, header=False
)
