"""contains shared utilities used by multiple tasks"""

import os
from airtable import Airtable

BASE_ID = "appo35FnVrocw6SO5"


def get_airtable_client():
    """gets an airtable client"""
    return Airtable(BASE_ID, os.getenv("AIRTABLE_API_KEY"))
