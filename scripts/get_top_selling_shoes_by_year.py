import argparse
from bs4 import BeautifulSoup
import json
import pandas as pd
import requests

base_url = "https://stockx.com/sneakers/top-selling?years="

def flatten(items):

    flattened_items = []
    for item in items:

        flattened = {}
        for key, value in item.items():
            
            if isinstance(value, dict):
                key_to_delete = key
                for nested_key, nested_value in value.items():
                    nested_key = "offers_" + nested_key
                    flattened[nested_key] = nested_value
            else:
                flattened[key] = value

        flattened_items.append(flattened)

    return flattened_items

def get_shoes(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # TODO: Add results from HTML
        # html = BeautifulSoup(response.text, "html5lib")
        # browse_grid = html.find("div", class_="browse-grid")
        # script = html.find("script", class_="browse-grid")

        lxml = BeautifulSoup(response.text, "lxml")
        scripts = lxml.find_all('script')

        data = scripts[13].string
        stock = json.loads(data)
        itemList = stock["itemListElement"]

        items = [item["item"] for item in itemList]
        
        flattened_items = flatten(items)
        items_df = pd.DataFrame(flattened_items)
        print(items_df.head())

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('--year')

    args = parser.parse_args()
    year = args.year
    search_url = base_url + year

    get_shoes(search_url)