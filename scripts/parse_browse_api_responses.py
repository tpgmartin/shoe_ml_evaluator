import argparse
import ast
from glob import glob
import json
import pandas as pd
from pandas.io.json import json_normalize

# JSON downloaded 28.06.19

if __name__ == "__main__":

    json_files = []
    for json_file in glob("./data/*.json"):

        with open(json_file) as f:
            data = json.load(f)
            json_files.extend(data["Products"])

    df = pd.DataFrame.from_dict(json_files, orient="columns")
    df["imageUrl"] = df["media"].apply(lambda media: media["imageUrl"])

    cols_to_drop = [
        "_tags",
        "breadcrumbs",
        "buying_countries",
        "charityCondition",
        "childId",
        "countryOfManufacture",
        "dataType",
        "description",
        "doppelgangers",
        "hidden",
        "ipoDate",
        "lock_selling",
        "media",
        "minimumBid",
        "productCategory",
        "selling_countries",
        "shoeSize",
        "traits",
        "type"
    ]
    df.drop(cols_to_drop, inplace=True, axis=1)
    df.to_csv("./data/browse_api_product_info.csv", index=False)
