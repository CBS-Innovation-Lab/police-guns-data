"""contains shared utilities used by multiple tasks"""

import os
from airtable import Airtable
from dotenv import load_dotenv
import pandas as pd

DOTENV = load_dotenv(dotenv_path=".env")

BASE_ID = "appo35FnVrocw6SO5"


def get_airtable_client():
    """gets an airtable client"""
    api_key = os.environ.get("AIRTABLE_API_KEY")
    if not api_key:
        msg = "AIRTABLE_API_KEY environment variable not set"
        if not DOTENV:
            msg += ". Did you forget to put a .env file in your task?"
        raise ValueError(msg)

    return Airtable(BASE_ID, api_key)


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
