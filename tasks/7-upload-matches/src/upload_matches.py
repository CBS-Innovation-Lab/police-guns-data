"""uploads matches from previous tasks to airtable for inspection"""

import sys
import logging
import airtable
import pandas as pd
from tqdm import tqdm
from src.utils import get_airtable_client

TABLE_NAME = "Serial matches"


def create_unique_ids(df, *colnames):
    """creates a unique id column for each row in dataframe"""
    if len(colnames) == 0:
        raise ValueError("Must provide at least one column name")

    df["unique_id"] = df[list(colnames)].apply("-".join, axis=1)
    # make unique id column the first column
    df = df[["unique_id"] + [col for col in df.columns if col != "unique_id"]]
    return df


def main():
    """main functon"""
    logging.basicConfig(level=logging.INFO, filename="upload_matches.log", filemode="w")
    logger = logging.getLogger(__name__)
    client = get_airtable_client()

    # read in data
    logger.info("Reading in data")
    df = pd.read_csv(sys.argv[1], dtype=str).fillna(0)
    logger.info("Data read in")

    # create unique ids
    logger.info("Creating unique ids")
    df = create_unique_ids(df, *sys.argv[2:])
    logger.info("Unique ids created\n%s", df.head())

    for _, row in tqdm(df.iterrows(), total=len(df)):
        # get any records with that unique id
        filter_by_formula = f"unique_id = \"{row['unique_id']}\""
        try:
            existing_records = client.get(
                TABLE_NAME, filter_by_formula=filter_by_formula
            )
        except airtable.airtable.AirtableError as exc:
            raise ValueError(
                f"Error getting records for {row['unique_id']} "
                f"using formula {filter_by_formula}"
            ) from exc

        n_results = len(existing_records["records"])
        if n_results == 0:
            row_data = row.to_dict()
            # remove any keys with empty values
            row_data = {k: v for k, v in row_data.items() if v != 0}
            try:
                client.create(TABLE_NAME, data=row_data)
            except airtable.airtable.AirtableError as exc:
                raise ValueError(f"Error creating record for {row_data}") from exc
            logger.info("Created record for: \n%s", row["unique_id"])
        elif n_results == 1:
            logger.info("Record already exists for: \n%s", row["unique_id"])
        else:
            raise ValueError(
                f"More than one record exists for {row['unique_id']}. "
                "This should not happen."
            )


if __name__ == "__main__":
    main()
