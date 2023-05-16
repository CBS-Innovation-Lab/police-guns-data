"""removes all matches from the matches table that are no longer in the serials table"""

import logging
import airtable
from dotenv import load_dotenv
from src.utils import get_airtable_client

load_dotenv()

logging.basicConfig(
    level=logging.INFO, filename="cleanup_airtable_matches.log", filemode="w"
)


def get_sale_serial(client, sale_serial, sale_agency):
    """searches for a sale serial in the serials table"""
    filter_by_formula = (
        f'AND({{Serial number}} = "{sale_serial}", {{Agency}} = "{sale_agency}")'
    )
    try:
        records = client.get("Serials", filter_by_formula=filter_by_formula)
    except airtable.airtable.AirtableError as exc:
        raise ValueError(
            f"Error getting records for {sale_serial} "
            f"using formula {filter_by_formula}"
        ) from exc

    n_results = len(records["records"])
    if n_results == 0:
        return None
    elif n_results == 1:
        return records["records"][0]
    else:
        raise ValueError(
            f"Found {n_results} results for {sale_serial} "
            f"using formula {filter_by_formula}"
        )


def main():
    """main function"""

    logging.info("Getting airtable client")
    client = get_airtable_client()

    logging.info("Getting matches")
    matches = client.get("Serial matches")

    while True:
        for record in matches["records"]:
            # search for that sale_serial in the serials table
            sale_records = get_sale_serial(
                client, record["fields"]["sale_serial"], record["fields"]["sale_agency"]
            )
            if sale_records is None:
                # delete the match record
                logging.info(
                    "No sale serial found for %s from %s. Deleting match record.",
                    record["fields"]["sale_serial"],
                    record["fields"]["sale_agency"],
                )
                client.delete("Serial matches", record["id"])
            else:
                logging.info(
                    "Found sale record for %s. Keeping match record.",
                    record["fields"]["sale_serial"],
                )
        else:
            if "offset" in matches:
                matches = client.get("Serial matches", offset=matches["offset"])
            else:
                break


if __name__ == "__main__":
    main()
