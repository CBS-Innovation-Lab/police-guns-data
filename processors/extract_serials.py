"""extracts serial number data from one of the raw files"""

import argparse
import numpy as np
import pandas as pd


def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file")
    parser.add_argument("sheet_name", help="name of the sheet to read")
    parser.add_argument(
        "serial_col", help="the name of the column containing serial numbers"
    )
    parser.add_argument(
        "desc_cols",
        help="a comma-separated list of columns containing firearm descriptions, "
        "to be concatenated",
    )
    parser.add_argument(
        "--date_col",
        help="the name of the column containing the date of the recovery",
        default=None,
    )
    parser.add_argument(
        "--agency_col",
        help="the name of the column containing the agency name",
        default=None,
    )
    parser.add_argument("--agency_name", help="the name of the agency", default=None)
    args = parser.parse_args()

    assert (
        args.agency_col is not None or args.agency_name is not None
    ), "either agency_col or agency_name must be specified"
    assert not all(
        [args.agency_col is not None, args.agency_name is not None],
    ), "only one of agency_col or agency_name can be specified"

    df = pd.read_excel(args.input_file, sheet_name=args.sheet_name)

    if args.agency_col is None:
        df["agency"] = args.agency_name
    else:
        df["agency"] = df[args.agency_col]

    if args.date_col is None:
        df["date"] = np.nan
        args.date_col = "date"

    if "," in args.desc_cols:
        args.desc_cols = args.desc_cols.split(",")
    else:
        args.desc_cols = [args.desc_cols]

    df["description"] = df[args.desc_cols].apply(
        lambda row: " ".join([str(x) for x in row]), axis=1
    )

    df = df[[args.serial_col, args.date_col, "agency", "description"]].rename(
        columns={args.date_col: "date", args.serial_col: "serial"}
    )

    print(df.to_csv(index=False, header=False))


if __name__ == "__main__":
    main()
