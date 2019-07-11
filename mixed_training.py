import glob
from joblib import dump,load
# from keras.optimizers import Adam
from lib import datasets, models
import numpy as np
import os
# from sklearn.model_selection import train_test_split

df = load("./lib/df.joblib")

images = datasets.import_images("data", ["*.jpg", "*.jpeg"])
# Need to perform normalisation on numeric features

print(images)
