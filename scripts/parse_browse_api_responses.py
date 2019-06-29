import argparse
from glob import glob
import json
import pandas as pd

if __name__ == "__main__":

    json_files = []
    for json_file in glob("./data/*.json"):

        with open(json_file) as f:
            data = json.load(f)
            json_files.extend(data["Products"])

    df = pd.DataFrame.from_dict(json_files, orient='columns')
    df.to_csv("./data/browse_api_product_info.csv", index=False)
