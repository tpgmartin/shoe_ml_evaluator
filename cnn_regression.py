import glob
# from keras.optimizers import Adam
# from lib import models
# import numpy as np
import os
# from sklearn.model_selection import train_test_split

# Get image files
image_files = []
image_files.extend(glob.glob(os.path.join(os.getcwd(), "data", "*.jpg")))
image_files.extend(glob.glob(os.path.join(os.getcwd(), "data", "*.jpeg")))
image_files.extend(glob.glob(os.path.join(os.getcwd(), "data", "*.png")))

image_files_dict = {}
for f in image_files:
    f_num = "".join(f.split("/")[-1]).split(".")[0]
    image_files_dict[int(f_num)] = f

sorted_files = []
for key, value in sorted(image_files_dict.items()):
    sorted_files.append(value)
