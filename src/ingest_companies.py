import pandas as pd

INPUT = "data/raw/companies.csv"
OUTPUT = "data/processed/us_companies.csv"

columns = [
    "name",
    "website",
    "country_code",
    "state",
    "city",
    "industry",
    "type",
    "size",
]

first_chunk = True

for c in pd.read_csv(
    INPUT,
    usecols=columns,
    chunksize=100000
):
    filtered_c = c[
        (c["country_code"] == "US")
        & c["website"].notna()
        & c["industry"].notna()
        & c["name"].notna()
    ]

    filtered_c.to_csv(
        OUTPUT,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False