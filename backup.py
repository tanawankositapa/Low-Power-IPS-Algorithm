# from sklearn.model_selection import GridSearchCV
from numpy.lib.type_check import real
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from matplotlib import pyplot
from tensorflow.python.keras import activations
import csv
# import trilateration
from sklearn import preprocessing
import tensorflowjs as tfjs
# from helper import plot_model, predict_classes, visualize_errors
from plot_model import plot_model
import time
# สร้าง dataframe
raw_df = pd.DataFrame()
mac_list = []
rssi_list = []
posxx_list = []
posyy_list = []
# แบ่งข้อมูลออกเป็น block เพราะต้องการจะตรวขสอบว่าข้อมูลแต่ละชุดที่ได้มามี beacon ตัวไหนที่หายไป
# with open('Dataset/dataset-fingerprint.csv', 'r') as csvfile:
with open('Dataset/dataset-fingerprint2.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row == []:
            # print(row)
            mac_list.append("")
            rssi_list.append("")
            posxx_list.append("")
            posyy_list.append("")
            # mac = row.split(",")
            # print(row)
            # break
        else:
            mac_list.append(row[0])
            rssi_list.append(row[1])
            posxx_list.append(row[2])
            posyy_list.append(row[3])
        # row = [''.join(row)]
            # raw_df = raw_df.append(row)
            # print(mac)
# raw_df_tran = raw_df.transpose()
# print(len(mac_list));
# print(len(rssi_list));
# print(len(posx_list));
# print(len(posy_list));
# extract mac และ rssi ออกมาจาก csv
# ตั้งชื่อให้ column 0
# raw_df.columns = ['Raw']
raw_df.insert(loc=0, column='Beacon', value=mac_list)
raw_df.insert(loc=1, column='RSSI', value=rssi_list)
raw_df.insert(loc=2, column='PosX', value=posxx_list)
raw_df.insert(loc=3, column='PosY', value=posyy_list)
# checklist = []
# checklist2 = []
# posx_list = []
# posy_list = []
# print(raw_df.head(-1))

# for row in raw_df.itertuples():
# mac = row.Raw.split(" ")
# print(mac[11])
# print(mac[0]) #mac
# print(mac)
# print(len(mac))
# if len(mac) == 1:
#     print(mac[0])
#     checklist.append(mac[0])
#     checklist2.append(mac[0])
#     posx_list.append(mac[0])
#     posy_list.append(mac[0])

# if len(mac) > 1:
#     print(mac[1])
#     # note: mac[1] = mac address
#     # note: mac[4] = RSSI
#     # note: mac[10] = PosX
#     # note: mac[11] = PosY
#     checklist.append(mac[1])
#     checklist2.append(mac[4])
#     # print(mac[11])
#     posx_list.append(mac[10])
#     posy_list.append(mac[11])
#     # print(checklist4)


# # print(checklist)
# raw_df.insert(loc=0, column='Beacon', value=checklist)
# raw_df.insert(loc=1, column='RSSI', value=checklist2)
# raw_df.insert(loc=2, column='PosX', value=posx_list)
# raw_df.insert(loc=3, column='PosY', value=posy_list)
# raw_df.drop(columns='Raw', inplace=True)
# # print(raw_df.head(20))


# กรอง mac address ของ beacon อื่นออก และตรวจสอบว่าในการรับข้อมูลมาแต่ละครั้ง มี beacon ตัวไหนหายไป
list_B1, list_B2, list_B3, list_B4, list_B5, list_B6 = [], [], [], [], [], []
indicator_list = [0, 0, 0, 0, 0, 0]
len_counting = 0
len_rawdf = len(raw_df)
posx_list = []
posy_list = []
insert_counting = 0
nan_counting = 0
while len_counting < len_rawdf:

    for row in raw_df.iloc[len_counting:len_rawdf].itertuples():
        len_counting += 1
        if insert_counting != 1:
            insert_counting += 1
        # print(row.RSSI)
        mac = row.Beacon
        rssi = row.RSSI
        PosX = row.PosX
        PosY = row.PosY
        # print(PosX)
        # print(mac)
        # print(rssi)
        # print(row)
        # print(len(row))

        if mac == "e8:ba:41:56:8d:9e":
            list_B1.append(rssi)
            indicator_list[0] = 1

        elif mac == "f3:45:89:ef:19:1e":
            list_B2.append(rssi)
            indicator_list[1] = 1

        elif mac == "c3:d7:59:ef:38:2e":
            list_B3.append(rssi)
            indicator_list[2] = 1

        elif mac == "fd:cc:03:3b:fb:50":
            list_B4.append(rssi)
            indicator_list[3] = 1

        # elif mac == "F6:A0:DA:F5:E3:F3":
        #     list_B5.append(rssi)
        #     indicator_list[4] = 1

        # elif mac == "E9:F7:FE:7E:D0:48":
        #     list_B6.append(rssi)
        #     indicator_list[5] = 1

        if insert_counting == 1:
            posx_list.append(PosX)
            posy_list.append(PosY)
            insert_counting += 1
        # # ตรวจสอบว่า row ไหนที่เป็นช่องว่าง (หมดชุดข้อมูลที่ได้มา)
        # print()
        if mac == "" or len_counting == len_rawdf:  # หมดข้อมูล 1 ชุด ที่ส่งมา หรือ หมดทั้ง dataset
            # print('omega')
            nan_counting += 1
            if indicator_list[0] == 0:
                # print('b1 nan')
                list_B1.append(np.NaN)

            if indicator_list[1] == 0:
                # print('b2 nan')
                list_B2.append(np.NaN)

            if indicator_list[2] == 0:
                # print('b3 nan')
                list_B3.append(np.NaN)

            if indicator_list[3] == 0:
                # print('b4 nan')
                list_B4.append(np.NaN)
            # else:
                # print(indicator_list)
                # print('Hello')
            # if indicator_list[4] == 0:
            #     list_B5.append(np.NaN)

            # if indicator_list[5] == 0:
            #     list_B6.append(np.NaN)

            break
    insert_counting = 0
    indicator_list = [0, 0, 0, 0, 0, 0]

# print("Nan: ", nan_counting)
# print(list_B3)
# array_has_nan = pd.isna(list_B4)
# for i in array_has_nan:
#     if i == True:
#         print('Yeh')
# print(array_has_nan)
# print("b1 len ",len(list_B1))
# print("b2 len ",len(list_B2))
# print("b3 len ",len(list_B3))
# print("b4 len ",len(list_B4))
# print("posx len ",len(posx_list))
# print("posy len ",len(posy_list))
real_df = pd.DataFrame(list_B1, columns=['B1'])
# real_df = pd.DataFrame(list_B3, columns=['B1'])
# real_df.index = pd.RangeIndex(len(real_df.index))
real_df['B2'] = list_B2
# real_df = real_df.dropna()
real_df['B3'] = list_B3
real_df['B4'] = list_B4
# real_df['B5'] = list_B5
# real_df['B6'] = list_B6
real_df['PosX'] = posx_list
real_df['PosY'] = posy_list
# # real_df = real_df.dropna()
# print(real_df.head(2000))
# # nan_df = real_df[real_df["B1"].isnull()]
# # # nan_df.insert(loc=0, column="B1", value=real_df[real_df["B1"].isnull()])
# # nan_df = pd.concat(
# #     [real_df[real_df["B2"].isnull()], real_df[real_df["B3"].isnull()], real_df[real_df["B4"].isnull()]], axis=1)
# # print(nan_df.head(10))
# # fill missing value with last valid value
# real_df = real_df.fillna(method="ffill")
# real_df[real_df['PosX'] == ""] = np.NaN
# real_df[real_df['PosY'] == ""] = np.NaN
# real_df = real_df.fillna(method="ffill")
# # print(real_df.isna().sum())
# # print(real_df.head(200))
# real_df.index = pd.RangeIndex(len(real_df.index))

# # เลือก rssi 3 ค่าที่เข้มที่สุด นำไปใช้ใน trilateration และ เอาตำแหน่งที่ได้ ไปใส่ใน real_df
# temp_list = []
# pair = {}
# tri_posx_list = []
# tri_posy_list = []
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

#     print(pair)
#     # print(type(pair))
#     sorted_pair = sorted(pair.items(), key=lambda kv: kv[1])

#     # New
#     rssi1 = int(sorted_pair[0][1])  # -55
#     rssi2 = int(sorted_pair[1][1])  # -55
#     rssi3 = int(sorted_pair[2][1])  # -60
#     # print(rssi1)
#     # print(type(rssi1))
#     # a = pair[]
#     b_first = sorted_pair[0][0]
#     b_second = sorted_pair[1][0]
#     b_third = sorted_pair[2][0]
#     # print(b_first)
#     # print(b_second)
#     # print(b_third)
#     result = trilateration.calculate(
#         rssi1, rssi2, rssi3, b_first, b_second, b_third)
#     x, y = result
#     # print(x)
#     # print(y)
#     tri_posx_list.append(x)
#     tri_posy_list.append(y)
#     temp_list = []
#     # pair = {}
#     # print(b_first)
#     # print(b_second)
#     # print(b_third)
# tri_df = pd.DataFrame()
# tri_df['PosX'] = tri_posx_list
# tri_df['PosY'] = tri_posy_list
# tri_df = tri_df.replace([np.inf, -np.inf], np.nan)
# tri_df = tri_df.dropna()
# # print(tri_df.head(10))

# แปลง string เป็น float
# print(real_df.head())
# dataTypeSeries = real_df.dtypes
# print(dataTypeSeries)
real_df['B1'] = real_df.B1.astype(float)
real_df['B2'] = real_df.B2.astype(float)
real_df['B3'] = real_df.B3.astype(float)
real_df['B4'] = real_df.B4.astype(float)
real_df['PosX'] = real_df.PosX.astype(float)
real_df['PosY'] = real_df.PosY.astype(float)
# dataTypeSeries = real_df.dtypes
# print(dataTypeSeries)
# real_df['B1'] = pd.to_numeric(real_df['B1'])
# real_df['B2'] = pd.to_numeric(real_df['B2'])
# real_df['B3'] = pd.to_numeric(real_df['B3'])
# real_df['B4'] = pd.to_numeric(real_df['B4'])
# real_df['B5'] = pd.to_numeric(real_df['B5'])
# real_df['B6'] = pd.to_numeric(real_df['B6'])
# real_df['PosX'] = pd.to_numeric(real_df['PosX'])
# real_df['PosY'] = pd.to_numeric(real_df['PosY'])
# print(real_df.head())
# print("Correlation: ")
# print(real_df.corr())
# print(len(real_df))
# print(real_df.head(20))

# normalize data (unuse now)
# min_max_scaler = preprocessing.MinMaxScaler()
# real_df_scaled = min_max_scaler.fit_transform(real_df)
# df_normalized = pd.DataFrame(real_df_scaled)
# print(df_normalized.head(10))

# print(real_df.head(20))
# นำข้อมูล dataset ที่เตรียมไว้แล้ว ไปใช้ในการ train model
X = real_df[['B1', 'B2', 'B3', 'B4']]
# dataTypeSeries = X.dtypes
# print('Type of X')
# print(dataTypeSeries)
# X = real_df[['B1', 'B2', 'B3', 'B4', 'B5']]
# X = real_df[['B1', 'B2', 'B4', 'B5']]
# X = real_df[['B1', 'B5', 'B6']]
# X = real_df[['B5', 'B6']]
# X = real_df[['B6']]
y = real_df[['PosX', 'PosY']]
# dataTypeSeries = y.dtypes
# print('Type of Y')
# print(dataTypeSeries)
# print(X.head(10))
# print(y.head(10))
# X = df_normalized[[0, 1, 2, 3, 4, 5]]
# y = df_normalized[[6, 7]]
# print(y['PosX'])
# print(X['B6'])


X_train, X_test, Y_train, Y_test = train_test_split(
    X, y, test_size=0.2, random_state=101)

model = Sequential()
# add layer ให้โมเดล
# input dimension = 6 เพราะมี 6 feature (B1-6)
model.add(Dense(300, input_dim=4, kernel_initializer='normal', activation='elu'))
model.add(Dense(300, kernel_initializer='normal', activation='elu'))
model.add(Dense(300, kernel_initializer='normal', activation='elu'))
model.add(Dense(300, kernel_initializer='normal', activation='elu'))
# model.add(Dense(12, activation='relu'))
# model.add(Dense(24, activation='relu'))
model.add(Dense(2, kernel_initializer='normal', activation='linear'))
# model.add(Dense(2))
model.summary()
model.compile(loss='mse',
              optimizer='adam', metrics=['mse', 'mae'])

history = model.fit(X_train, Y_train, validation_data=(
    X_test, Y_test), epochs=2000, batch_size=32, verbose=1)


# # plt.plot(history.history['mean_absolute_percentage_error'])
# # ply.plot(history.history['cosine_proximity'])
# # plt.plot(history.history['mae'])
# # plt.plot(history.history['val_mae'])
plt.plot(history.history['mae'])
plt.plot(history.history['val_mae'])
plt.title('Model MAE')
plt.ylabel('MAE')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['mse'])
plt.plot(history.history['val_mse'])
plt.title('Model MSE')
plt.ylabel('MSE')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
# ลองกับ Test Set
_, mse, mae = model.evaluate(X_test, Y_test)
print('Mse: ', mse)
print('Mae: ', mae)

# _, accuracy = model.evaluate(X_test, Y_test)
# print('Accuracy: %.2f' % (accuracy*100))

# ประเมิลผล model ด้วยวิธีต่าง ๆ

# print(plot_model(model))
# print(model.evaluate(X_test, Y_test))
# print(model.evaluate(X_train, Y_train))
test_predictions = model.predict(X_test)
# from sklearn import metrics
# print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, test_predictions))
# print('Mean Squared Error:', metrics.mean_squared_error(Y_test, test_predictions))
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, test_predictions)))
test_predictions = pd.Series(list(test_predictions))
predictions_value_df = pd.DataFrame(Y_test)
predictions_value_df.reset_index(drop=True, inplace=True)
test_predictions.reset_index(drop=True, inplace=True)


# predictions_value_df = pd.concat(
#     [predictions_value_df, test_predictions, tri_df], axis=1)
# predictions_value_df.columns = ['TestTruePosX',
#                                 'TestTruePosY', 'Predict', 'TriPosX', 'TriPosY']
# # # งงว่าทำไมมันมี NaN ใน TriPos ได้ไง
# predictions_value_df = predictions_value_df.dropna()

predictions_value_df = pd.concat(
    [predictions_value_df, test_predictions], axis=1)
predictions_value_df.columns = ['TestTruePosX',
                                'TestTruePosY', 'Predict']
# # งงว่าทำไมมันมี NaN ใน TriPos ได้ไง
# predictions_value_df = predictions_value_df.dropna()

# predictions_value_df = pd.concat(
#     [predictions_value_df, test_predictions], axis=1)
# predictions_value_df.columns = ['TestTruePosX',
#                                 'TestTruePosY', 'Predict']


#####
# print(predictions_value_df.head(20))
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
predictions_value_df['TestPredPosX'] = pd.to_numeric(
    predictions_value_df['TestPredPosX'])
predictions_value_df['TestPredPosY'] = pd.to_numeric(
    predictions_value_df['TestPredPosY'])
predictions_value_df['TestPredPosX'] = predictions_value_df['TestPredPosX'].astype(
    float)
predictions_value_df['TestPredPosY'] = predictions_value_df['TestPredPosY'].astype(
    float)
predictions_value_df = predictions_value_df.drop(['Predict'], axis=1)

subtractionResultsX = (
    predictions_value_df['TestTruePosX'] - predictions_value_df['TestPredPosX'])**2
subtractionResultsY = (
    predictions_value_df['TestTruePosY'] - predictions_value_df['TestPredPosY'])**2

addResult = np.sqrt(subtractionResultsX+subtractionResultsY)

# triSubtractionResultsX = (
#     predictions_value_df['TestTruePosX'] - predictions_value_df['TriPosX'])**2
# triSubtractionResultsY = (
#     predictions_value_df['TestTruePosY'] - predictions_value_df['TriPosY'])**2

# triAddResult = np.sqrt(triSubtractionResultsX+triSubtractionResultsY)

# errorResult = math.sqrt((predictions_value_df['TestTruePosX']-predictions_value_df['TestPredPosX'])**2 + (predictions_value_df['TestTruePosY'] - predictions_value_df['TestPredPosY'])**2)
# print(subtractionResultsX.head())
predictions_value_df.insert(loc=4, column='ErrorX', value=subtractionResultsX)
predictions_value_df.insert(loc=5, column='ErrorY', value=subtractionResultsY)
# predictions_value_df.insert(loc=6, column='Error', value=errorResult)
predictions_value_df.insert(loc=6, column='Euclidian', value=addResult)

# predictions_value_df.insert(loc=7, column='TriEuclidian', value=triAddResult)
pd.set_option("display.max_rows", None)
print("Number of predicted data: ", len(predictions_value_df))
# print(predictions_value_df['TestTruePosX'].dtypes)
# print(predictions_value_df['TestTruePosY'].dtypes)
print(predictions_value_df.head(1000))

print(mean_squared_error(
    predictions_value_df['TestTruePosX'], predictions_value_df['TestPredPosX']))

print(mean_squared_error(
    predictions_value_df['TestTruePosY'], predictions_value_df['TestPredPosY']))

print("MAE-PosX-Model: %f" % (mean_absolute_error(
    predictions_value_df['TestTruePosX'], predictions_value_df['TestPredPosX'])))

print("MAE-PosY-Model %f" % (mean_absolute_error(
    predictions_value_df['TestTruePosY'], predictions_value_df['TestPredPosY'])))

# print("MAE-PosX-Trilateration: %f" % (mean_absolute_error(
#     predictions_value_df['TestTruePosX'], predictions_value_df['TriPosX'])))

# print("MAE-PosY-Trilateration: %f" % (mean_absolute_error(
#     predictions_value_df['TestTruePosY'], predictions_value_df['TriPosY'])))
print("S.D. of error:")
print(predictions_value_df[['ErrorX', 'ErrorY']].std(axis=0))
print("Max Euclidian: ", predictions_value_df['Euclidian'].max(axis=0))
print("Min Euclidian: ", predictions_value_df['Euclidian'].min(axis=0))
print("Mean of Euclidian: ", predictions_value_df['Euclidian'].mean(axis=0))
# print("Mean of TriEuclidian: ",
#       predictions_value_df['TriEuclidian'].mean(axis=0))

# Count Value
c0 = 0
c1, c2, c3, c4, c5, c6, c7, c8, c9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
for row in predictions_value_df['Euclidian']:
    if row >= 0.0 and row <= 0.5:
        c0 += 1
    if row > 0.5 and row <= 1.0:
        c1 += 1
    if row > 1.0 and row <= 1.5:
        c2 += 1
    if row > 1.5 and row <= 2.0:
        c3 += 1
    if row > 2.0 and row <= 2.5:
        c4 += 1
    if row > 2.5 and row <= 3.0:
        c5 += 1
    if row > 3.0 and row <= 3.5:
        c6 += 1
    if row > 3.5 and row <= 4.0:
        c7 += 1
    if row > 4.0 and row <= 4.5:
        c8 += 1
    if row > 4.5 and row <= 5.0:
        c9 += 1
print("C0: ", c0)
print("C1: ", c1)
print("C2: ", c2)
print("C3: ", c3)
print("C4: ", c4)
print("C5: ", c5)
print("C6: ", c6)
print("C7: ", c7)
print("C8: ", c8)
print("C9: ", c9)


# Create a sample dataframe with an text index
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
range = ['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-2.5',
         '2.5-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5']
count = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]

plt.bar(range, count, color='maroon',
        width=0.3)
plt.title('Quantized Euclidian')
plt.xlabel('Range')
plt.ylabel('Count')
plt.legend(['Range', 'Count'], loc='upper left')
plt.show()

time_before = time.perf_counter()

# model.save('D:/Work/Project/Github/Low-Power-IPS-Algorithm/model')
# # tfjs.converters.save_keras_model(
# #     model, "D:\Work\Project\Github\Low-Power-IPS-Web-App\model")

# items = [
#         [-48, -61, -65, -67, -68, -82],
#         [-48, -67, -53, -63, -72, -71],
#         [-51, -70, -65, -83, -69, -89]
# ]
# model_load = keras.models.load_model(
#     'D:/Work/Project/Github/Low-Power-IPS-Algorithm/model')
# test_predictions_new = model_load.predict(items)
# print(test_predictions_new)

# time_after = time.perf_counter()
# time_elapsed = time_after-time_before
# print("Time used for prediction is: ", time_elapsed)
# # layers = [[24, 24], [12, 12, 12]]
# # activations = ['relu', 'linear']
# # param_grid = dict(layers=layers, activation=activations,
# #                   batch_size=[16, 32], epochs=[350])
# # grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy')
# # grid_search = grid.fit(X_train, Y_train)
# # print("Best score: %0.3f" % grid_search.best_score_)
# # print(grid_search.best_estimator_)
# # print('best prarams:', grid.best_params_)
# # print(tri_df.head(200))
