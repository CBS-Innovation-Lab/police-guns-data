"""contains shared utilities used by multiple tasks"""

import os
from airtable import Airtable
from dotenv import load_dotenv

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
