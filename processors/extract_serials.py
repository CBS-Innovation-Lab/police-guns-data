"""extracts serial number data from one of the raw files"""

import argparse
import pandas as pd


def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file")
    parser.add_argument("sheet_name", help="name of the sheet to read")
    parser.add_argument(
        "serial_col", help="the name of the column containing serial numbers"
    )
    args = parser.parse_args()

    df = pd.read_excel(args.input_file, sheet_name=args.sheet_name)
    df = df[[args.serial_col]]
    print(df.to_csv(index=False, header=False))


if __name__ == "__main__":
    main()
