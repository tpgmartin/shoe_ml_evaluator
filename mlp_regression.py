from joblib import dump,load
from keras.optimizers import Adam
from lib import models
import numpy as np
from sklearn.model_selection import train_test_split

X_train = load("./lib/X_train.joblib")
y_train = load("./lib/y_train.joblib")
X_test = load("./lib/X_test.joblib")
y_test = load("./lib/y_test.joblib")

# Not sure about scaling target variable?

model = models.create_mlp(X_train.shape[1], regress=True)
opt = Adam(lr=1e-3, decay=1e-3/200)
# Compile using MAPE
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

# Train model
print("Training model")
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, batch_size=8)

print("Generate predictions")
predictions = model.predict(X_test)

# Find percentage difference between actual and predicted sales
percentDiff = (predictions.flatten() - y_test / y_test) * 100
absPercentDiff = np.abs(percentDiff)

# MAPE ~ 20000% !?
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
print("mean: {:.2f}%, std: {:.2f}%".format(mean, std))