import argparse
import ast
from glob import glob
import json
import pandas as pd
from pandas.io.json import json_normalize

# JSON downloaded 11.07.19

if __name__ == "__main__":

    json_files = []
    for json_file in glob("./data/*.json"):

        with open(json_file) as f:
            data = json.load(f)
            json_files.extend(data["Products"])

    df = pd.DataFrame.from_dict(json_files, orient="columns")
    df["imageUrl"] = df["media"].apply(lambda media: media["imageUrl"])
    df["pricePremium"] = df["market"].apply(lambda market: market["pricePremium"])
    df["deadstockSold"] = df["market"].apply(lambda market: market["deadstockSold"])
    df["averageDeadstockPrice"] = df["market"].apply(lambda market: market["averageDeadstockPrice"])

    cols_to_drop = [
        "_tags",
        "belowRetail",
        "breadcrumbs",
        "buying_countries",
        "charityCondition",
        "condition",
        "childId",
        "countryOfManufacture",
        "dataType",
        "description",
        "doppelgangers",
        "hidden",
        "ipoDate",
        "lock_selling",
        "market",
        "media",
        "minimumBid",
        "objectID",
        "releaseDate",
        "releaseTime",
        "productCategory",
        "selling_countries",
        "shoe",
        "shoeSize",
        "shortDescription",
        "styleId",
        "tickerSymbol",
        "traits",
        "type"
    ]
    df.drop(cols_to_drop, inplace=True, axis=1)
    df.to_csv("./data/browse_api_product_info.csv", index=False)
