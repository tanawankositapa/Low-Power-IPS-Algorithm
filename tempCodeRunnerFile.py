
# # extract ค่า mac address และ rssi ออกมาจาก raw dataset
# checklist = []
# checklist2 = []
# for row in raw_df.itertuples():
#     mac = row.Raw.split(" ")

#     # print(len(mac))
#     if len(mac) == 1:
#         checklist.append(mac[0])
#         checklist2.append(mac[0])

#     if len(mac) > 1:
#         # note: mac[1] = mac address
#         # note: mac[4] = RSSI
#         checklist.append(mac[1])
#         checklist2.append(mac[4])


# # print(checklist)
# raw_df.insert(loc=0, column='Beacon', value=checklist)
# raw_df.insert(loc=1, column='RSSI', value=checklist2)
# raw_df.drop(columns='Raw', inplace=True)
# # print(raw_df.head(15))

# # กรอง mac address ของ beacon อื่นออก และตรวจสอบว่าในการรับข้อมูลมาแต่ละครั้ง มี beacon ตัวไหนหายไป
# list_B1, list_B2, list_B3, list_B4, list_B5, list_B6 = [], [], [], [], [], []
# indicator_list = [0, 0, 0, 0, 0, 0]
# len_counting = 0
# len_rawdf = len(raw_df)

# while len_counting < len_rawdf:

#     for row in raw_df.iloc[len_counting:len_rawdf].itertuples():
#         len_counting += 1
#         mac = row.Beacon
#         rssi = row.RSSI
#         # print(mac)
#         # print(rssi)
#         # print(row)
#         # print(len(row))

#         if mac == "E0:D9:DA:22:34:1B":
#             list_B1.append(rssi)
#             indicator_list[0] = 1

#         elif mac == "FA:0C:C8:48:E6:6A":
#             list_B2.append(rssi)
#             indicator_list[1] = 1

#         elif mac == "EE:11:28:0E:61:39":
#             list_B3.append(rssi)
#             indicator_list[2] = 1

#         elif mac == "CE:0E:9E:D9:8F:3B":
#             list_B4.append(rssi)
#             indicator_list[3] = 1

#         elif mac == "F6:A0:DA:F5:E3:F3":
#             list_B5.append(rssi)
#             indicator_list[4] = 1

#         elif mac == "E9:F7:FE:7E:D0:48":
#             list_B6.append(rssi)
#             indicator_list[5] = 1

#         # ตรวจสอบว่า row ไหนที่เป็นช่องว่าง (หมดชุดข้อมูลที่ได้มา)
#         if mac == "" or len_counting == len_rawdf:

#             if indicator_list[0] == 0:
#                 list_B1.append(np.NaN)

#             if indicator_list[1] == 0:
#                 list_B2.append(np.NaN)

#             if indicator_list[2] == 0:
#                 list_B3.append(np.NaN)

#             if indicator_list[3] == 0:
#                 list_B4.append(np.NaN)

#             if indicator_list[4] == 0:
#                 list_B5.append(np.NaN)

#             if indicator_list[5] == 0:
#                 list_B6.append(np.NaN)

#             break

#     indicator_list = [0, 0, 0, 0, 0, 0]

# # print(indicator_list)

# real_df = pd.DataFrame(list_B1, columns=['B1'])
# real_df['B2'] = list_B2
# real_df['B3'] = list_B3
# real_df['B4'] = list_B4
# real_df['B5'] = list_B5
# real_df['B6'] = list_B6
# real_df = real_df.dropna()
# real_df.index = pd.RangeIndex(len(real_df.index))

# # เลือก rssi 3 ค่าที่เข้มที่สุด นำไปใช้ใน trilateration และ เอาตำแหน่งที่ได้ ไปใส่ใน real_df
# temp_list = []
# pair = {}
# posx_list = []
# posy_list = []
# # for row in real_df.itertuples():
# for row in real_df.iterrows():

#     # print(int(row[1][5]))
#     # print(row[1].index[0])
#     pair = {
#         row[1].index[0]: row[1][0],
#         row[1].index[1]: row[1][1],
#         row[1].index[2]: row[1][2],
#         row[1].index[3]: row[1][3],
#         row[1].index[4]: row[1][4],
#         row[1].index[5]: row[1][5],
#     }
#     # print(pair)
#     key_list = list(pair.keys())
#     val_list = list(pair.values())
#     # print(val_list)
#     # temp_list.extend((int(row.B1),int(row.B2),int(row.B3),int(row.B4),int(row.B5),int(row.B6)))
#     temp_list.extend((int(row[1][0]), int(row[1][1]), int(
#         row[1][2]), int(row[1][3]), int(row[1][4]), int(row[1][5]),))

#     temp_list.sort()
#     temp_list.reverse()
#     # print(temp_list)
#     rssi1 = temp_list[0]
#     rssi2 = temp_list[1]
#     rssi3 = temp_list[2]
#     # a = pair[]
#     b_first = key_list[val_list.index(str(rssi1))]
#     b_second = key_list[val_list.index(str(rssi2))]
#     b_third = key_list[val_list.index(str(rssi3))]

#     result = trilateration.calculate(
#         rssi1, rssi2, rssi3, b_first, b_second, b_third)
#     x, y = result
#     # print(x)
#     # print(y)
#     posx_list.append(x)
#     posy_list.append(y)
#     temp_list = []
#     # pair = {}
#     # print(b_first)
#     # print(b_second)
#     # print(b_third)

# real_df['PosX'] = posx_list
# real_df['PosY'] = posy_list
# real_df = real_df.replace([np.inf, -np.inf], np.nan)
# real_df = real_df.dropna()
# real_df['B1'] = pd.to_numeric(real_df['B1'])
# real_df['B2'] = pd.to_numeric(real_df['B2'])
# real_df['B3'] = pd.to_numeric(real_df['B3'])
# real_df['B4'] = pd.to_numeric(real_df['B4'])
# real_df['B5'] = pd.to_numeric(real_df['B5'])
# real_df['B6'] = pd.to_numeric(real_df['B6'])
# # print(real_df.head(10))
# # print(len(real_df))
# # print(posx_list)
# # print(real_df['PosY'])
# ###########################################################################################################

# # นำข้อมูล dataset ที่เตรียมไว้แล้ว ไปใช้ในการ train model
# # real_df = pd.read_csv('Dataset/testX12.csv')
# # X = real_df[['BLE1', 'BLE2', 'BLE3', 'BLE4']]
# X = real_df[['B1', 'B2', 'B3', 'B4', 'B5', 'B6']]
# y = real_df[['PosX', 'PosY']]
# # print(y['PosX'])
# # print(X['B6'])


# X_train, X_test, Y_train, Y_test = train_test_split(
#     X, y, test_size=0.3, random_state=101)

# model = Sequential()
# # add layer ให้โมเดล
# # input dimension = 4 เพราะมี 4 feature (BLE1-4)
# model.add(Dense(4, input_dim=6, activation='relu'))
# model.add(Dense(12, activation='relu'))
# model.add(Dense(12, activation='relu'))

# model.add(Dense(2, activation='linear'))
# # model.add(Dense(2))

# model.compile(loss='mse',
#               optimizer='rmsprop', metrics=['accuracy'])

# model.fit(X_train, Y_train, epochs=250, batch_size=10)

# _, accuracy = model.evaluate(X_test, Y_test)
# print('Accuracy: %.2f' % (accuracy*100))

# # print(model.evaluate(X_test, Y_test))
# # print(model.evaluate(X_train, Y_train))
# test_predictions = model.predict(X_test)
# test_predictions = pd.Series(list(test_predictions))
# predictions_value_df = pd.DataFrame(Y_test)
# predictions_value_df.reset_index(drop=True, inplace=True)
# test_predictions.reset_index(drop=True, inplace=True)

# predictions_value_df = pd.concat(
#     [predictions_value_df, test_predictions], axis=1)
# predictions_value_df.columns = ['Test True PosX', 'Test True PosY', 'Predict']

# predictions_value_df['Predict'] = predictions_value_df['Predict'].astype(str)

# predictions_value_df['Predict'] = predictions_value_df['Predict'].str.strip(
#     '[]')

# new = predictions_value_df.Predict.str.split(" ", n=1, expand=True)

# predictions_value_df['Test Pred PosX'] = new[0]

# predictions_value_df['Test Pred PosY'] = new[1]

# predictions_value_df['Test Pred PosX'] = predictions_value_df['Test Pred PosX'].astype(
#     float)

# predictions_value_df['Test Pred PosY'] = predictions_value_df['Test Pred PosY'].astype(
#     float)

# sns.regplot(x='Test True PosX', y='Test Pred PosX', data=predictions_value_df)

# sns.regplot(x='Test True PosY', y='Test Pred PosY',
#             data=predictions_value_df, color="g")

# print(predictions_value_df.head(10))

# print(mean_squared_error(
#     predictions_value_df['Test True PosX'], predictions_value_df['Test Pred PosX']))

# print(mean_squared_error(
#     predictions_value_df['Test True PosY'], predictions_value_df['Test Pred PosY']))

# print(mean_absolute_error(
#     predictions_value_df['Test True PosX'], predictions_value_df['Test Pred PosX']))

# print(mean_absolute_error(
#     predictions_value_df['Test True PosY'], predictions_value_df['Test Pred PosY']))
