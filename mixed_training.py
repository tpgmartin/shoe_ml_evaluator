import cv2
from keras.layers.core import Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import concatenate
from lib import datasets, models
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer
import webcolors

df = pd.read_csv(os.path.join(os.getcwd(), "data/csv/browse_api_product_info.csv"))

df = df[["brand", "category", "colorway", "gender", "title", "averageDeadstockPrice", "deadstockSold", "imageUrl", "annualHigh", "lastSale", "pricePremium"]]

# Find colours in colorway, add as individual feature coloumns
df["uniqueColours"] = df["colorway"].apply(datasets.find_colours)
mlb = MultiLabelBinarizer()
unique_colour_labels = mlb.fit_transform(df['uniqueColours'])
df = df.join(pd.DataFrame(unique_colour_labels, columns=mlb.classes_))
df.drop(["uniqueColours"], axis=1, inplace=True)

cols_to_rename = {col: f"colour_{col}" for col in df.columns[11:]}
df.rename(index=str, columns=cols_to_rename, inplace=True)

for category in ["brand", "category", "gender"]:
    df = datasets.encode_categorical_features(df, category)

df.drop(["colorway", "title", "imageUrl"], axis=1, inplace=True)

outliers = datasets.find_outliers(df,"pricePremium")

df.drop(outliers, inplace=True)
images = datasets.import_images("data/images", ["*.jpg", "*.jpeg"], outliers)

df_train, df_test, images_train, images_test = train_test_split(df, images, test_size=0.3, random_state=42)

# Normalise numerical values
scaler = MinMaxScaler()
# annualHigh
df_train["annualHigh"] = scaler.fit_transform(df_train[["annualHigh"]])
df_test["annualHigh"] = scaler.fit_transform(df_test[["annualHigh"]])

# averageDeadstockPrice
df_train["averageDeadstockPrice"] = scaler.fit_transform(df_train[["averageDeadstockPrice"]])
df_test["averageDeadstockPrice"] = scaler.fit_transform(df_test[["averageDeadstockPrice"]])

# deadstockSold
df_train["deadstockSold"] = scaler.fit_transform(df_train[["deadstockSold"]])
df_test["deadstockSold"] = scaler.fit_transform(df_test[["deadstockSold"]])

# lastSale
df_train["lastSale"] = scaler.fit_transform(df_train[["lastSale"]])
df_test["lastSale"] = scaler.fit_transform(df_test[["lastSale"]])

y_train = df_train["pricePremium"]
y_test = df_test["pricePremium"]

df_train.drop(["pricePremium"], axis=1, inplace=True)
df_test.drop(["pricePremium"], axis=1, inplace=True)

# Create model
mlp = models.create_mlp(df_train.shape[1], regress=False)
cnn = models.create_cnn(64, 64, 3, regress=False)
 
combinedInput = concatenate([mlp.output, cnn.output])
 
# Final layers
x = Dense(4, activation="relu")(combinedInput)
x = Dense(1, activation="linear")(x)
 
model = Model(inputs=[mlp.input, cnn.input], outputs=x)

opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)
 
# train the model
print("Training model...")
model.fit([df_train, images_train], y_train, validation_data=([df_test, images_test], y_test), epochs=200, batch_size=8)

# make predictions on the testing data
print("Making predictions")
preds = model.predict([df_test, images_test])

percentDiff = ((preds.flatten() - y_test) / y_test) * 100
absPercentDiff = np.abs(percentDiff)

# compute the MAPE
# * averageDeadstockPrice
# * deadstockSold: loss: 31.7651 - val_loss: 51.3511, mean: 51.35%, std: 31.64%
# * pricePremium
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
print("mean: {:.2f}%, std: {:.2f}%".format(mean, std))