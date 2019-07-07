import glob
from joblib import dump,load
from keras.optimizers import Adam
from lib import models
import numpy as np
import os
from sklearn.model_selection import train_test_split

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

df = load("./lib/df.joblib")
df_train, df_test, images_train, images_test = train_test_split(df, sorted_files, test_size=0.3, random_state=42)

# Won't normalise target variable
# Target variable is "deadstockSold"
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
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))