import cv2
import glob
from joblib import dump, load
from keras.optimizers import Adam
from lib import datasets, models
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer
import webcolors

# Get text data
df = pd.read_csv(os.path.join(os.getcwd(), "data/csv/browse_api_product_info.csv"))

# Select features
df = df[["brand", "category", "colorway", "gender", "title", "averageDeadstockPrice", "deadstockSold", "imageUrl", "pricePremium"]]

# Find colours in colorway, add as individual feature coloumns
df["uniqueColours"] = df["colorway"].apply(datasets.find_colours)
mlb = MultiLabelBinarizer()
unique_colour_labels = mlb.fit_transform(df['uniqueColours'])
df = df.join(pd.DataFrame(unique_colour_labels, columns=mlb.classes_))
df.drop(["uniqueColours"], axis=1, inplace=True)

cols_to_rename = {col: f"colour_{col}" for col in df.columns[9:]}
df.rename(index=str, columns=cols_to_rename, inplace=True)

for category in ["brand", "category", "gender"]:
    df = datasets.encode_categorical_features(df, category)

df.drop(["colorway", "title", "imageUrl"], axis=1, inplace=True)

# Get image files
images = datasets.import_images("data/images", ["*.jpg", "*.jpeg"])

# need to think about imbalances in datasets e.g. brand
df_train, df_test, images_train, images_test = train_test_split(df, images, test_size=0.3, random_state=42)

# What to predict?
# * averageDeadstockPrice
# * deadstockSold: loss: 36.5430 - val_loss: 56.2292
# * pricePremium
y_train = df_train["deadstockSold"]
y_test = df_test["deadstockSold"]

model = models.create_cnn(64, 64, 3, regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

print("Train model")
model.fit(images_train, y_train, validation_data=(images_test, y_test), epochs=200, batch_size=8)

# make predictions on the testing data
print("Making predictions")
preds = model.predict(images_test)

percentDiff = ((preds.flatten() - y_test) / y_test) * 100
absPercentDiff = np.abs(percentDiff)

# compute the MAPE
# mean: 46.24%, std: 30.16%
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
print("mean: {:.2f}%, std: {:.2f}%".format(mean, std))