import os
import requests
import pandas as pd

data = pd.read_csv("./data/combined_browse_info.csv")

for idx, row in data.iterrows():
    imageUrl = row["imageUrl"].split("?")[0]
    imageFile = imageUrl.split("https://stockx.imgix.net/")[-1]
    imageFilepath = os.path.join(os.getcwd(), "data", imageFile)

    print(f"Getting image for {imageFile}")

    f = open(imageFilepath,'wb')
    f.write(requests.get(imageUrl).content)
    f.close()

print("Done!")