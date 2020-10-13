import pandas as pd
import seaborn as sns
import numpy as np

from numpy import loadtxt

from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
# from sklearn.metrics import mean_absolute_percentage_error
from matplotlib import pyplot

import csv
raw_df = pd.DataFrame()

# แบ่งข้อมูลออกเป็น block เพราะต้องการจะตรวขสอบว่าข้อมูลแต่ละชุดที่ได้มามี beacon ตัวไหนที่หายไป
with open('Dataset/dataset-fingerprint.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:

        row = [''.join(row)]
        raw_df = raw_df.append(row)


# ตั้งชื่อให้ column 0
raw_df.columns = ['Raw']
checklist = []
checklist2 = []
posx_list = []
posy_list = []
for row in raw_df.itertuples():
    mac = row.Raw.split(" ")
    # print(mac[11])
    # print(len(mac))
    if len(mac) == 1:
        checklist.append(mac[0])
        checklist2.append(mac[0])
        posx_list.append(mac[0])
        posy_list.append(mac[0])

    if len(mac) > 1:
        # note: mac[1] = mac address
        # note: mac[4] = RSSI
        # note: mac[10] = PosX
        # note: mac[11] = PosY
        checklist.append(mac[1])
        checklist2.append(mac[4])
        # print(mac[11])
        posx_list.append(mac[10])
        posy_list.append(mac[11])
        # print(checklist4)


# print(checklist)
raw_df.insert(loc=0, column='Beacon', value=checklist)
raw_df.insert(loc=1, column='RSSI', value=checklist2)
raw_df.insert(loc=2, column='PosX', value=posx_list)
raw_df.insert(loc=3, column='PosY', value=posy_list)
raw_df.drop(columns='Raw', inplace=True)
# print(raw_df.head(20))


# กรอง mac address ของ beacon อื่นออก และตรวจสอบว่าในการรับข้อมูลมาแต่ละครั้ง มี beacon ตัวไหนหายไป
list_B1, list_B2, list_B3, list_B4, list_B5, list_B6 = [], [], [], [], [], []
indicator_list = [0, 0, 0, 0, 0, 0]
len_counting = 0
len_rawdf = len(raw_df)
posx_list = []
posy_list = []
assert_counting = 0
while len_counting < len_rawdf:

    for row in raw_df.iloc[len_counting:len_rawdf].itertuples():
        len_counting += 1
        if assert_counting != 1:
            assert_counting += 1
        mac = row.Beacon
        rssi = row.RSSI
        PosX = row.PosX
        PosY = row.PosY
        # print(PosX)
        # print(mac)
        # print(rssi)
        # print(row)
        # print(len(row))

        if mac == "E0:D9:DA:22:34:1B":
            list_B1.append(rssi)
            indicator_list[0] = 1

        elif mac == "FA:0C:C8:48:E6:6A":
            list_B2.append(rssi)
            indicator_list[1] = 1

        elif mac == "EE:11:28:0E:61:39":
            list_B3.append(rssi)
            indicator_list[2] = 1

        elif mac == "CE:0E:9E:D9:8F:3B":
            list_B4.append(rssi)
            indicator_list[3] = 1

        elif mac == "F6:A0:DA:F5:E3:F3":
            list_B5.append(rssi)
            indicator_list[4] = 1

        elif mac == "E9:F7:FE:7E:D0:48":
            list_B6.append(rssi)
            indicator_list[5] = 1

        if assert_counting == 1:
            posx_list.append(PosX)
            posy_list.append(PosY)
            assert_counting += 1
        # ตรวจสอบว่า row ไหนที่เป็นช่องว่าง (หมดชุดข้อมูลที่ได้มา)
        if mac == "" or len_counting == len_rawdf:

            if indicator_list[0] == 0:
                list_B1.append(np.NaN)

            if indicator_list[1] == 0:
                list_B2.append(np.NaN)

            if indicator_list[2] == 0:
                list_B3.append(np.NaN)

            if indicator_list[3] == 0:
                list_B4.append(np.NaN)

            if indicator_list[4] == 0:
                list_B5.append(np.NaN)

            if indicator_list[5] == 0:
                list_B6.append(np.NaN)

            break
    assert_counting = 0
    indicator_list = [0, 0, 0, 0, 0, 0]


real_df = pd.DataFrame(list_B1, columns=['B1'])
real_df['B2'] = list_B2
real_df['B3'] = list_B3
real_df['B4'] = list_B4
real_df['B5'] = list_B5
real_df['B6'] = list_B6
real_df['PosX'] = posx_list
real_df['PosY'] = posy_list
real_df = real_df.dropna()
real_df.index = pd.RangeIndex(len(real_df.index))

real_df['B1'] = pd.to_numeric(real_df['B1'])
real_df['B2'] = pd.to_numeric(real_df['B2'])
real_df['B3'] = pd.to_numeric(real_df['B3'])
real_df['B4'] = pd.to_numeric(real_df['B4'])
real_df['B5'] = pd.to_numeric(real_df['B5'])
real_df['B6'] = pd.to_numeric(real_df['B6'])
real_df['PosX'] = pd.to_numeric(real_df['PosX'])
real_df['PosY'] = pd.to_numeric(real_df['PosY'])
# print(real_df.head(50))


##############################
# นำข้อมูล dataset ที่เตรียมไว้แล้ว ไปใช้ในการ train model
# real_df = pd.read_csv('Dataset/testX12.csv')
# X = real_df[['BLE1', 'BLE2', 'BLE3', 'BLE4']]
X = real_df[['B1', 'B2', 'B3', 'B4', 'B5', 'B6']]
y = real_df[['PosX', 'PosY']]
# print(y['PosX'])
# print(X['B6'])


X_train, X_test, Y_train, Y_test = train_test_split(
    X, y, test_size=0.3, random_state=101)

model = Sequential()
# add layer ให้โมเดล
# input dimension = 6 เพราะมี 6 feature (B1-6)
model.add(Dense(4, input_dim=6, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))

model.add(Dense(2, activation='linear'))
# model.add(Dense(2))

model.compile(loss='mse',
              optimizer='rmsprop', metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=350, batch_size=10, verbose=0)

_, accuracy = model.evaluate(X_test, Y_test)
print('Accuracy: %.2f' % (accuracy*100))

# print(model.evaluate(X_test, Y_test))
# print(model.evaluate(X_train, Y_train))
test_predictions = model.predict(X_test)
test_predictions = pd.Series(list(test_predictions))
predictions_value_df = pd.DataFrame(Y_test)
predictions_value_df.reset_index(drop=True, inplace=True)
test_predictions.reset_index(drop=True, inplace=True)

predictions_value_df = pd.concat(
    [predictions_value_df, test_predictions], axis=1)
predictions_value_df.columns = ['TestTruePosX', 'TestTruePosY', 'Predict']

predictions_value_df['Predict'] = predictions_value_df['Predict'].astype(str)

predictions_value_df['Predict'] = predictions_value_df['Predict'].str.strip(
    '[]')

predictions_value_df['Predict'] = predictions_value_df['Predict'].str.strip(
    ' ')


predictions_value_df.reset_index(drop=True, inplace=True)
# print(predictions_value_df.head(10))
new = predictions_value_df.Predict.str.split(" ", n=1, expand=True)
# print(new)
predictions_value_df['TestPredPosX'] = new[0]

predictions_value_df['TestPredPosY'] = new[1]

# print(new[0])
# print(new[1])
# print(predictions_value_df.head(40))

predictions_value_df['TestPredPosX'] = pd.to_numeric(
    predictions_value_df['TestPredPosX'])
predictions_value_df['TestPredPosY'] = pd.to_numeric(
    predictions_value_df['TestPredPosY'])

predictions_value_df['TestPredPosX'] = predictions_value_df['TestPredPosX'].astype(
    float)

predictions_value_df['TestPredPosY'] = predictions_value_df['TestPredPosY'].astype(
    float)

# sns.regplot(x='Test True PosX', y='Test Pred PosX', data=predictions_value_df)

# sns.regplot(x='Test True PosY', y='Test Pred PosY',
#             data=predictions_value_df, color="g")

print(predictions_value_df.head(30))

print(mean_squared_error(
    predictions_value_df['TestTruePosX'], predictions_value_df['TestPredPosX']))

print(mean_squared_error(
    predictions_value_df['TestTruePosY'], predictions_value_df['TestPredPosY']))

print(mean_absolute_error(
    predictions_value_df['TestTruePosX'], predictions_value_df['TestPredPosX']))

print(mean_absolute_error(
    predictions_value_df['TestTruePosY'], predictions_value_df['TestPredPosY']))
