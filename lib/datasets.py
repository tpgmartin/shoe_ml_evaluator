import cv2
import glob
from joblib import dump,load
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer
import webcolors

# df = pd.read_csv("../data/combined_browse_info.csv")

# def find_colours(colorway):
    
#     colours = " ".join(colorway.lower().split("/")).split(" ")
    
#     unique_colours = list(set([colour_str for colour_str in colours if colour_str in webcolors.CSS3_NAMES_TO_HEX]))
    
#     return sorted(unique_colours)

# df["uniqueColours"] = df["colorway"].apply(find_colours)

# Will also want to parameterise image size for `cvs2.resize`
def import_images(image_dir, file_extensions):

    image_files = []
    for ext in file_extensions:
        image_files.extend(glob.glob(os.path.join(os.getcwd(), image_dir, ext)))

    image_files_dict = {}
    for f in image_files:
        f_num = "".join(f.split("/")[-1]).split(".")[0]
        image_files_dict[int(f_num)] = f

    sorted_files = []
    for key, value in sorted(image_files_dict.items()):
        sorted_files.append(value)

    images = []
    for filepath in sorted_files:
        image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image, (64, 64))
        images.append(image)

    images = np.array(images)
    images = images / 255.0

    return images