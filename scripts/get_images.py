import os
import requests
import pandas as pd

data = pd.read_csv("./data/csv/browse_api_product_info.csv")

for idx, row in data.iterrows():
    imageUrl = row["imageUrl"].split("?")[0]
    imageFile = imageUrl.split("https://stockx.imgix.net/")[-1]
    imageFile = str(idx) + os.path.splitext(imageFile)[-1]
    imageFilepath = os.path.join(os.getcwd(), "data", "images", imageFile)

    print(f"Getting image for {imageFile}")

    f = open(imageFilepath,'wb')
    f.write(requests.get(imageUrl).content)
    f.close()

print("Done!")