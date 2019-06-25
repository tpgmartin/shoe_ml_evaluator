# Make request against product pages such as 
# https://stockx.com/adidas-yeezy-boost-350-v2-cream-white

import argparse
from bs4 import BeautifulSoup
import json
import pandas as pd
import requests

def get_product_page_info(url):

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        html = BeautifulSoup(response.text, "html5lib")
        product_page_data = {}

        # Information to get
        # * Last sale
        # * Lowest ask
        # * Highest bid
        # * Name
        # * Last sale

        product_details = html.find("div", class_="product-details")
        for div in product_details.find_all("div", class_="detail"):
            span_elements = div.find_all("span")
            title = span_elements[1].text
            value = span_elements[2].text.strip()
            product_page_data[title] = value
        
        product_description = html.find("div", class_="product-description").text
        product_page_data["product_description"] = product_description

        print(product_page_data)
        # * 52 week high
        # * Trade range
        # * Volatility
        # * Number of sales
        # * Price premium
        # * Average sale price

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument("--year")

    args = parser.parse_args()
    year = args.year

    filepath = "./data/top_selling_shoes_{}.csv".format(year)
    shoes = pd.read_csv(filepath)

    # all_product_page_data = []
    # for shoe in shoes:
        # get_product_page_info(shoe.link)
    get_product_page_info("https://stockx.com/adidas-yeezy-boost-350-v2-cream-white")
