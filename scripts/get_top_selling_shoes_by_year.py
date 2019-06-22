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
    # TODO: Add results from HTML
    html = BeautifulSoup(response.text, "html5lib")
    browse_grid = html.find("div", class_="browse-grid")

# <div class="tile browse-tile">
#     <div class="tile Tile-sc-18f3mrw-0 iCgYKH">
#         <a href="/adidas-yeezy-boost-350-v2-cream-white" style="color:black">
#             <div class="TileImage-wau2e8-0 cqDtuD" style="position:relative;padding-top:58%">
#                 <noscript>
#                     <img alt="adidas Yeezy Boost 350 V2 Cream/Triple White" class="LazyImage__StyledImage-sc-153p075-0 MEhRc" src="https://stockx.imgix.net/Adidas-Yeezy-Boost-350-V2-Cream-White-1-1.jpg?fit=fill&amp;bg=FFFFFF&amp;w=300&amp;h=214&amp;auto=format,compress&amp;trim=color&amp;q=90&amp;dpr=2&amp;updated_at=1539789713"/>
#                 </noscript>
#             </div>
#             <div class="TileBody-sc-1rlrno1-0 fjqeUQ">
#                 <div class="PrimaryText-sc-12c6bzb-0 gMymmc" size="16" style="height:38px;overflow:hidden;margin-bottom:6px">
#                     adidas Yeezy Boost 350 V2 Cream/Triple White
#                 </div>
#                 <div>
#                     <div class="price-line-div">
#                         <div class="SecondaryText-sc-1mx0yoa-0 fygSsx">lowest ask</div>
#                         <div class="PrimaryText-sc-12c6bzb-0 jwzdVc" size="22">£210</div>
#                     </div>
#                 </div>
#                 <div class="change SecondaryText-sc-1mx0yoa-0 fygSsx">
#                     # Sold: 43878
#                 </div>
#             </div>
#         </a>
#     </div>
# </div>

    try:
        for div in browse_grid.find_all("div", class_="browse-tile"):
            # TODO:
            # For each tile find,
            # * href
            # * name
            # * lowest ask price
            # * total sold
            print(div)
            print("----------")
    except:
        pass

def get_script_data(response):

    lxml = BeautifulSoup(response.text, "lxml")
    scripts = lxml.find_all('script')

    data = scripts[13].string
    stock = json.loads(data)
    itemList = stock["itemListElement"]

    items = [item["item"] for item in itemList]
    
    flattened_items = flatten(items)
    items_df = pd.DataFrame(flattened_items)
    print(items_df.head())
    return items_df

def get_data(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        html_data = get_html_data(response)
        
        # script_data = get_script_data(response)
    
    # TODO: return merged data frames
    # return ...

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('--year')

    args = parser.parse_args()
    year = args.year
    search_url = base_url + year

    get_data(search_url)