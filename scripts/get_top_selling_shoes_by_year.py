import argparse
from bs4 import BeautifulSoup
import pandas as pd
import requests

base_url = "https://stockx.com/sneakers/top-selling?years="

def get_shoes(url):

    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    print(response)

    if response.status_code == 200:
        html = BeautifulSoup(response.text, "html5lib")

        print(html)

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('--year')

    args = parser.parse_args()
    year = args.year
    search_url = base_url + year

    get_shoes(search_url)