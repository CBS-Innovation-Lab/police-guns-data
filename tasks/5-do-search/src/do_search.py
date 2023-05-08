"""searches all serial numbers in our sale dataset in the recovery data"""

import logging
import os
import re
import sqlite3
import sys
import airtable
from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, filename="output/do_search.log", filemode="w")
assert load_dotenv(), ".env file not found"

# load the sale data from airtable
BASE_ID = "appo35FnVrocw6SO5"
client = airtable.Airtable(BASE_ID, os.getenv("AIRTABLE_API_KEY"))


def load_sale_data():
    """loads the sale data from airtable"""
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
    df = (
        pd.DataFrame(rows)
        .assign(
            serial=lambda df: df.fields.apply(lambda x: x["Serial number"]),
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
    for sale_serial in tqdm(sale_df["serial"], desc="Processing serials"):
        match_df = string_match(sale_serial, conn)
        if len(match_df) > 0:
            match_df = refine_matches(
                match_df.assign(sale_serial=sale_serial).rename(
                    columns={"serial": "match_serial"}
                )[["sale_serial", "match_serial", "source_file"]]
            )
            if len(match_df) > 0:
                match_dfs.append(match_df)
                logging.info(
                    "\n---\nFound %d matches for serial %s: \n%s\n---\n",
                    len(match_df),
                    sale_serial,
                    match_df.to_markdown(),
                )

    merged_df = pd.concat(match_dfs)
    return merged_df


def main():
    """main function"""
    try:
        sale = preprocess_serials(load_sale_data())
        recovery = preprocess_serials(pd.read_csv(sys.argv[1]))
        # Create database and load data
        conn = create_database()
        load_data_to_database(sale, recovery, conn)
        # Perform search
        match_df = do_search(conn)
        final_df = match_df.drop_duplicates(subset=["source_file", "sale_serial"])
        final_df = refine_matches(final_df)
        print(final_df.to_csv(index=False))
    except Exception as exc:
        logging.exception(exc)
        raise exc


if __name__ == "__main__":
    main()
