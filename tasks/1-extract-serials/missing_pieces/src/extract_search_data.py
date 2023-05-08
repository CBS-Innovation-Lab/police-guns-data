"""assigns a description column"""

import logging
import sys
import pandas as pd
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO, filename="output/extract_search_data.log", filemode="w"
)


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


chunks = pd.read_csv(sys.argv[1], dtype=str, chunksize=10_000)
for chunk in tqdm(chunks):
    chunk["DATE"] = pd.to_datetime(chunk["DATE"])
    logging.info("Loaded %d rows from %s", len(chunk), sys.argv[1])
    logging.info("\n%s", chunk.dtypes)
    chunk["description"] = chunk.apply(get_description, axis=1)
    chunk[["SERIAL NUMBER", "DATE", "AGENCY", "description"]].to_csv(
        sys.argv[2], index=False, header=False, mode="a"
    )
