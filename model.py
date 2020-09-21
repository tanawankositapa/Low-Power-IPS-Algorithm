# -*- coding: utf-8 -*-
"""Neural Network IPS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bSViM-AwiIDn9Tw0akSVj3Ue0tMUeiPT
"""

import pandas as pd
# import seaborn as sns
# import numpy as np

# from numpy import loadtxt
# from keras.models import Sequential
# from keras.layers import Dense
# from sklearn.model_selection import train_test_split
# from matplotlib import pyplot
import csv

# raw_df = pd.read_csv('P1.csv')
# raw_df = pd.DataFrame(columns=['Beacon', 'RSSI', 'Major', 'Minor'])
raw_df = pd.DataFrame()

# ต้อง append column

# แบ่งข้อมูลออกเป็น block เพราะต้องการจะตรวขสอบว่าข้อมูลแต่ละชุดที่ได้มามี beacon ตัวไหนที่หายไป
with open('P1.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:

        row = [''.join(row)]
        raw_df = raw_df.append(row)


# ตั้งชื่อให้ column 0
# raw_df.columns = ['Raw', 'Beacon', 'RSSI', 'Major', 'Minor']
raw_df.columns = ['Raw']
# raw_df = raw_df.transpose()
# print(raw_df.head(10))
# print(raw_df.head())
# print(len(raw_df.columns))
checklist = []
checklist2 = []
for row in raw_df.itertuples():
    mac = row.Raw.split(" ")

    # print(len(mac))
    if len(mac) == 1:
        checklist.append(mac[0])
        checklist2.append(mac[0])
        # print('hell')
    if len(mac) > 1:
        # note: mac[1] = mac address
        # note: mac[4] = RSSI
        # print(mac[1])
        # raw_df = raw_df['Beacon'].append(mac[1])
        # print(raw_df.head())
        checklist.append(mac[1])
        checklist2.append(mac[4])
        # raw_df.insert(loc=0, column='Beacon', value=mac[1])
    # print(type(row))
    # print(row)
# print(checklist)
raw_df.insert(loc=0, column='Beacon', value=checklist)
raw_df.insert(loc=1, column='RSSI', value=checklist2)
raw_df.drop(columns='Raw', inplace=True)
print(raw_df.head(15))


# list_B1, list_B2, list_B3, list_B4, list_B5, list_B6 = [], [], [], [], [], []
# indicator1, indicator2, indicator3, indicator4, indicator5, indicator6 = 0, 0, 0, 0, 0, 0
# indicator_list = []
# for row in raw_df.itertuples():
#     mac = row.Beacon.split(" ")
#     rssi = row.RSSI.split(" ")
#     # print(mac[1])
#     if mac[1] == "E0:D9:DA:22:34:1B":
#         list_B1.append(rssi[2])
#         indicator1 += 1
#         indicator_list.append(indicator1)
#     if mac[1] == "FA:0C:C8:48:E6:6A":
#         list_B2.append(rssi[2])
#         indicator2 += 1
#         indicator_list.append(indicator2)
#     if mac[1] == "EE:11:28:0E:61:39":
#         list_B3.append(rssi[2])
#         indicator3 += 1
#         indicator_list.append(indicator3)
#     if mac[1] == "CE:0E:9E:D9:8F:3B":
#         list_B4.append(rssi[2])
#         indicator4 += 1
#         indicator_list.append(indicator4)
#     if mac[1] == "F6:A0:DA:F5:E3:F3":
#         list_B5.append(rssi[2])
#         indicator5 += 1
#         indicator_list.append(indicator5)
#     if mac[1] == "E9:F7:FE:7E:D0:48":
#         list_B6.append(rssi[2])
#         indicator6 += 1
#         indicator_list.append(indicator6)
#     else:
#         # list_B1.append(0)
#         indicator_list.append(0)

# # if 0 in indicator_list:

# # print(list_B1)
# # df['B1'] = list_B1
# # print(df.head())
# print(list_B3)
# real_df = pd.DataFrame(list_B1, columns=['B1'])
# real_df['B2'] = list_B2
# # real_df['B3'] = list_B3
# real_df['B4'] = list_B4
# real_df['B5'] = list_B5
# real_df['B6'] = list_B6
# print(real_df.head())

###########################################################################################################

# df = pd.read_csv('somedataset.csv')

# X = df[['BLE1', 'BLE2', 'BLE3', 'BLE4', 'BLE5', 'BLE6']]
# y = df[['PosX', 'PosY']]


# X_train, X_test, Y_train, Y_test = train_test_split(
#     X, y, test_size=0.3, random_state=101)

# model = Sequential()
# # add layer ให้โมเดล
# # input dimension = 4 เพราะมี 4 feature (BLE1-4)
# model.add(Dense(4, input_dim=4, activation='relu'))
# model.add(Dense(4, activation='relu'))
# model.add(Dense(4, activation='relu'))

# model.add(Dense(2, activation='linear'))
# # model.add(Dense(2))

# model.compile(loss='mse',
#               optimizer='rmsprop', metrics=['accuracy'])

# model.fit(X_train, Y_train, epochs=50, batch_size=10)

# _, accuracy = model.evaluate(X_test, Y_test)
# print('Accuracy: %.2f' % (accuracy*100))
