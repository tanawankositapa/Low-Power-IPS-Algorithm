import pandas as pd
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

# load data จาก csv
df = pd.read_csv('somedataset.csv')

# กำหนด coloumn เป็น input(x) output(y)
X = df[['BLE1', 'BLE2', 'BLE3', 'BLE4']]
y = df[['PosX', 'PosY']]

# ประกาศใช้โมเดลจาก Keras
model = Sequential()
# add layer ให้โมเดล
# input dimension = 4 เพราะมี 4 feature (BLE1-4)
model.add(Dense(12, input_dim=4, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(2, activation='relu'))

# compile the keras model
model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])
# train โมเดล
model.fit(X, y, epochs=150, batch_size=10)

# วัดผล
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

#
# fit the keras model on the df
# model.fit(X, y, epochs=150, batch_size=10, verbose=0)
# # make class predictions with the model
# predictions = model.predict_classes(X)
# # summarize the first 5 cases
# for i in range(5):
# 	print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
