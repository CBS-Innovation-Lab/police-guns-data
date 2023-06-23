"""runs pd.concat on all files in the directory and saves the result as a csv file

This script is needed because some of the files are longer than csvkit's field size limit
"""

import sys
import pandas as pd


infiles = sys.argv[1:]

print(
    pd.concat([pd.read_csv(infile, dtype=str) for infile in infiles]).to_csv(
        index=False
    )
)
