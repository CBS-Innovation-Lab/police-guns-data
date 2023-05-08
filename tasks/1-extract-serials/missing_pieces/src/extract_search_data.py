"""assigns a description column"""

import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
df = df.assign(
    description=lambda df: df[["MAKE", "MODEL", "PROPERTY_DESCRIPTION"]].apply(
        lambda row: " ".join([str(x) for x in row]), axis=1
    ),
)
df[["SERIAL NUMBER", "DATE", "AGENCY", "description"]].to_csv(
    sys.argv[2], index=False, header=False
)
