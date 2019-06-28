import argparse
import json
import pandas as pd
import requests

if __name__ == "__main__":

    url = "https://stockx.com/api/browse"

    querystring = {"currency":"GBP","order":"DESC","productCategory":"sneakers","sort":"deadstock_sold","year":"2017","page":"1"}

    headers = {
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "3ce26b5c-7022-4610-85e8-6ca0dc26c046,0de7ab4d-e368-407d-81e8-5f74621ce57a",
        'Host': "stockx.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    for page in range(1,26):

        querystring["page"] = page

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.json)
