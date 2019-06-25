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
            tile["image"] = div.find("img")["src"].split("?")[0]
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
    items_df["image"] = items_df["image"].apply(lambda image: image.split("?")[0])

    return items_df

def get_data(url, year):

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        html_data = get_html_data(response)
        script_data = get_script_data(response)
        top_selling_shoes = html_data.merge(script_data, on="image")

        # Rename columns
        top_selling_shoes.rename(columns={"itemCondition": "item_condition", "name_y": "name", "offers_priceCurrency": "offers_price_currency", "releaseDate": "release_date"}, inplace=True)
        # Cleanup df
        top_selling_shoes["total_sold"] = top_selling_shoes["total_sold"].apply(lambda s: int(s.split(" ")[-1]))
        top_selling_shoes["link"] = top_selling_shoes["link"].apply(lambda s: "https://stockx.com" + s)
        top_selling_shoes["lowest_ask"] = top_selling_shoes["lowest_ask"].apply(lambda s: int(s[1:].replace(",", "")))
        top_selling_shoes["offers_price_currency"] = "GBP"
        top_selling_shoes.drop(columns=["name_x", "@type", "url", "offers_highPrice", "offers_lowPrice", "offers_@type", "description"], inplace=True)
        # Change column order
        top_selling_shoes = top_selling_shoes[["name", "model", "brand", "color", "item_condition", "sku", "image", "link", "offers_url", "release_date", "lowest_ask", "offers_price_currency", "total_sold"]]

        filename = "{}_{}.csv".format("top_selling_shoes", year)
        top_selling_shoes.to_csv("./data/{}".format(filename), index=False)
    
    else:
        return

    return top_selling_shoes

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument("--year")

    args = parser.parse_args()
    year = args.year
    search_url = base_url + year

    # TODO: Want to get more shoes for given year
    # How to run JS on page?
    top_selling_shoes = get_data(search_url, year)
    print(top_selling_shoes.head())
