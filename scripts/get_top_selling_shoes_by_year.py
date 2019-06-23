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

def get_html_data(response):

    html = BeautifulSoup(response.text, "html5lib")
    browse_grid = html.find("div", class_="browse-grid")

    html_data = []
    try:
        for div in browse_grid.find_all("div", class_="browse-tile"):
            tile = {}
            tile["link"] = div.find("a", href=True)["href"]
            tile["image"] = div.find("img")["src"]
            tile["name"] = div.find("div", attrs={"class": "PrimaryText-sc-12c6bzb-0"}).text
            tile["lowest_ask"] = div.find_all("div", attrs={"class": "jwzdVc"})[0].text
            tile["total_sold"] = div.find_all("div", attrs={"class": "SecondaryText-sc-1mx0yoa-0"})[-1].text
            html_data.append(tile)
    except:
        pass
    
    html_df = pd.DataFrame(html_data)

    return html_df

def get_script_data(response):

    lxml = BeautifulSoup(response.text, "lxml")
    scripts = lxml.find_all("script")

    data = scripts[13].string
    stock = json.loads(data)
    itemList = stock["itemListElement"]

    items = [item["item"] for item in itemList]
    
    flattened_items = flatten(items)
    items_df = pd.DataFrame(flattened_items)

    return items_df

def get_data(url):

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        html_data = get_html_data(response)
        script_data = get_script_data(response)

    # TODO: handle errors
    data_df = html_data.merge(script_data, on="name")
    data_df.to_csv("data_df.csv", index=False)

    return data_df

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument("--year")

    args = parser.parse_args()
    year = args.year
    search_url = base_url + year

    get_data(search_url)