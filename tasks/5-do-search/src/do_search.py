"""searches all serial numbers in our sale dataset in the recovery data"""

import logging
import re
import sqlite3
import sys
import pandas as pd
from tqdm import tqdm
from src.utils import get_airtable_client

logging.basicConfig(level=logging.INFO, filename="output/do_search.log", filemode="w")


def load_sale_data():
    """loads the sale data from airtable"""
    client = get_airtable_client()
    response = client.get("Serials")
    if len(response["records"]) == 0:
        raise ValueError("No records found in airtable")

    rows = []
    offset = None
    while True:
        response = client.get("Serials", offset=offset)
        rows.extend(response["records"])
        if "offset" in response:
            offset = response["offset"]
        else:
            break

    get_key_if_exists = (
        lambda x, y: x[y]  # pylint: disable=unnecessary-lambda-assignment
        if y in x
        else None
    )
    df = (
        pd.DataFrame(rows)
        .assign(
            serial=lambda df: df.fields.apply(
                lambda x: get_key_if_exists(x, "Serial number")
            ),
            sale_date=lambda df: df.fields.apply(
                lambda x: pd.to_datetime(get_key_if_exists(x, "Sale date"))
            ),
            sale_description=lambda df: df.fields.apply(
                lambda x: get_key_if_exists(x, "Firearm description")
            ),
            sale_agency=lambda df: df.fields.apply(
                lambda x: get_key_if_exists(x, "agency_name")
            ),
        )
        .drop(
            [
                "createdTime",
                "fields",
            ],
            axis=1,
        )
    )
    return df


def preprocess_serials(df):
    """preprocesses serial numbers"""
    df["serial"] = df["serial"].str.upper()
    # drop any serials that are less than 5 characterse
    df = df.query("serial.notna() & serial.str.len() >= 5")
    return df


def remove_leading_serial_alpha(df, col):
    """removes leading alpha characters from serial numbers"""
    df[col] = df[col].str.replace(r"&[a-zA-Z]+", "")
    # drop any rows that now have less than 4 characters
    df = df[df[col].str.len() >= 4]
    return df


def create_database():
    """creates a database in memory"""
    conn = sqlite3.connect(":memory:")
    return conn


def load_data_to_database(sale_df, recovery_df, conn):
    """loads the sale and recovery data to the database"""
    sale_df.to_sql("sale", conn, if_exists="replace", index=False)
    recovery_df.to_sql("recovery", conn, if_exists="replace", index=False)


def refine_matches(match_df):
    """uses a regex to filter out false positives from the SQL queries"""

    return (
        match_df.assign(
            real_match=lambda df: df.apply(
                # allow non-word characters before and after the match
                # but remove any matches that have a word character before or after
                lambda row: re.search(
                    rf"(?<!\w){row.sale_serial}(?!\w)", row.match_serial
                )
                is not None,
                axis=1,
            )
        )
        .query("real_match")
        .drop("real_match", axis=1)
        # only allow records where the sale date is BEFORE the recovery date
        .query("sale_date < match_date | sale_date.isna() | match_date.isna()")
    )


def do_search(conn):
    """finds any rows in recovery_df whose serial contains a serial in sale_df"""

    def string_match(sale_serial, conn):
        query = f"""
        SELECT *
        FROM recovery
        WHERE serial LIKE '%{sale_serial}%'
        """
        return pd.read_sql_query(query, conn)

    sale_df = pd.read_sql("SELECT * FROM sale", conn)
    match_dfs = []
    for _, sale_row in tqdm(
        sale_df.iterrows(), desc="Processing serials", total=len(sale_df)
    ):
        match_df = string_match(sale_row.serial, conn)
        if len(match_df) > 0:
            match_df = refine_matches(
                match_df.assign(
                    sale_serial=sale_row.serial,
                    sale_date=sale_row.sale_date,
                    sale_description=sale_row.sale_description,
                    sale_agency=sale_row.sale_agency,
                    match_agency=lambda df: df.agency,
                    match_date=lambda df: df.date,
                ).rename(
                    columns={
                        "serial": "match_serial",
                        "description": "match_description",
                    }
                )[
                    [
                        "sale_serial",
                        "sale_agency",
                        "sale_date",
                        "sale_description",
                        "match_serial",
                        "source_file",
                        "match_agency",
                        "match_date",
                        "match_description",
                    ]
                ]
            )
            if len(match_df) > 0:
                match_dfs.append(match_df)
                logging.info(
                    "\n---\nFound %d matches for serial %s: \n%s\n---\n",
                    len(match_df),
                    sale_row.serial,
                    match_df.to_markdown(),
                )

    merged_df = pd.concat(match_dfs)
    return merged_df


def main():
    """main function"""
    try:
        sale = preprocess_serials(load_sale_data())
        logging.info("Loaded %d rows from airtable", len(sale))
        recovery = preprocess_serials(pd.read_csv(sys.argv[1], low_memory=False))
        recovery["date"] = pd.to_datetime(recovery["date"], format="mixed")
        logging.info("Loaded %d rows from recovery data", len(recovery))
        # Create database and load data
        conn = create_database()
        load_data_to_database(sale, recovery, conn)
        # Perform search
        match_df = do_search(conn)
        final_df = match_df.drop_duplicates(subset=["source_file", "sale_serial"]).pipe(
            refine_matches
        )
        print(final_df.to_csv(index=False))
    except Exception as exc:
        logging.exception(exc)
        raise exc


if __name__ == "__main__":
    main()
