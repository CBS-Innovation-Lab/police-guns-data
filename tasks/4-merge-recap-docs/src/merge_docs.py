"""reads each file and creates a csv file with the full text of each document"""

import sys
import pandas as pd
from tqdm import tqdm

infiles = sys.argv[1:]

data = {
    "source_file": [],
    "serial": [],
}
for file_index, text_filename in tqdm(enumerate(infiles)):
    with open(text_filename, "r", encoding="utf-8") as f:
        text = f.read()
    data["source_file"].append(text_filename)
    data["serial"].append(text)

df = pd.DataFrame(data)
print(df.to_csv(index=False))
