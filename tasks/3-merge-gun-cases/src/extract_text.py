"""extracts message text from json files and saves it to a csv file"""

import os
import sys
import pandas as pd
from tqdm import tqdm

infiles = sys.argv[1:]

for file_index, json_filename in tqdm(enumerate(infiles)):
    df = pd.read_json(json_filename)
    df = df.assign(  # pylint: disable=no-member
        source_file=os.path.basename(json_filename)
    )[["source_file", "text"]].rename(columns={"text": "serial"})
    print(df.to_csv(index=False, header=file_index == 0))
