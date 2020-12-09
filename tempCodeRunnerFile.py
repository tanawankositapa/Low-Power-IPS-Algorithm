# ###################################################################
# # print(posx_list)
# # real_df['PosX'] = posx_list
# # real_df['PosY'] = posy_list
# # real_df = real_df.dropna()
# # real_df.index = pd.RangeIndex(len(real_df.index))

# real_df['B1'] = pd.to_numeric(real_df['B1'])
# real_df['B2'] = pd.to_numeric(real_df['B2'])
# real_df['B3'] = pd.to_numeric(real_df['B3'])
# real_df['B4'] = pd.to_numeric(real_df['B4'])
# real_df['B5'] = pd.to_numeric(real_df['B5'])
# real_df['B6'] = pd.to_numeric(real_df['B6'])
# real_df['PosX'] = pd.to_numeric(real_df['PosX'])
# real_df['PosY'] = pd.to_numeric(real_df['PosY'])
# # print(len(real_df))
# # print(real_df.head(20))
# ##############################
# # min_max_scaler = preprocessing.MinMaxScaler()
# # real_df_scaled = min_max_scaler.fit_transform(real_df)
# # df_normalized = pd.DataFrame(real_df_scaled)
# # print(df_normalized.head(10))

# #############################

# ##############################
# # นำข้อมูล dataset ที่เตรียมไว้แล้ว ไปใช้ในการ train model

# X = real_df[['B1', 'B2', 'B3', 'B4', 'B5', 'B6']]
# # X = real_df[['B1', 'B2', 'B3', 'B4', 'B5']]
# # X = real_df[['B1', 'B2', 'B4', 'B5']]
# # X = real_df[['B1', 'B5', 'B6']]
# # X = real_df[['B5', 'B6']]
# # X = real_df[['B6']]
# y = real_df[['PosX', 'PosY']]
# print(X.head(10))
# # X = df_normalized[[0, 1, 2, 3, 4, 5]]
# # y = df_normalized[[6, 7]]
# # print(y['PosX'])
# # print(X['B6'])


# X_train, X_test, Y_train, Y_test = train_test_split(
#     X, y, test_size=0.3, random_state=101)

# model = Sequential()
# # add layer ให้โมเดล
# # input dimension = 6 เพราะมี 6 feature (B1-6)
# model.add(Dense(12, input_dim=6, activation='relu'))
# model.add(Dense(12, activation='relu'))
# model.add(Dense(12, activation='relu'))
# # model.add(Dense(24, activation='relu'))
# model.add(Dense(2, activation='linear'))
# # model.add(Dense(2))

# model.compile(loss='mse',
#               optimizer='rmsprop', metrics=['accuracy'])

# model.fit(X_train, Y_train, validation_data=(
#     X_test, Y_test), epochs=5, batch_size=32, verbose=0)

# # ลองกับ Test Set
# _, accuracy = model.evaluate(X_test, Y_test)
# print('Accuracy: %.2f' % (accuracy*100))


# # print(model.evaluate(X_test, Y_test))
# # print(model.evaluate(X_train, Y_train))
# test_predictions = model.predict(X_test)
# # from sklearn import metrics
# # print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, test_predictions))
# # print('Mean Squared Error:', metrics.mean_squared_error(Y_test, test_predictions))
# # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, test_predictions)))
# test_predictions = pd.Series(list(test_predictions))
# predictions_value_df = pd.DataFrame(Y_test)
# predictions_value_df.reset_index(drop=True, inplace=True)
# test_predictions.reset_index(drop=True, inplace=True)


# predictions_value_df = pd.concat(
#     [predictions_value_df, test_predictions, tri_df], axis=1)
# predictions_value_df.columns = ['TestTruePosX',
#                                 'TestTruePosY', 'Predict', 'TriPosX', 'TriPosY']
# # # งงว่าทำไมมันมี NaN ใน TriPos ได้ไง
# predictions_value_df = predictions_value_df.dropna()


# # predictions_value_df = pd.concat(
# #     [predictions_value_df, test_predictions], axis=1)
# # predictions_value_df.columns = ['TestTruePosX',
# #                                 'TestTruePosY', 'Predict']


# #####
# # print(predictions_value_df.head(20))
# predictions_value_df['Predict'] = predictions_value_df['Predict'].astype(str)

# predictions_value_df['Predict'] = predictions_value_df['Predict'].str.strip(
#     '[]')

# predictions_value_df['Predict'] = predictions_value_df['Predict'].str.strip(
#     ' ')


# predictions_value_df.reset_index(drop=True, inplace=True)
# # print(predictions_value_df.head(10))
# new = predictions_value_df.Predict.str.split(" ", n=1, expand=True)
# # print(new)
# predictions_value_df['TestPredPosX'] = new[0]

# predictions_value_df['TestPredPosY'] = new[1]

# # print(new[0])
# # print(new[1])
# # print(predictions_value_df.head(40))

# predictions_value_df['TestPredPosX'] = pd.to_numeric(
#     predictions_value_df['TestPredPosX'])
# predictions_value_df['TestPredPosY'] = pd.to_numeric(
#     predictions_value_df['TestPredPosY'])

# predictions_value_df['TestPredPosX'] = predictions_value_df['TestPredPosX'].astype(
#     float)

# predictions_value_df['TestPredPosY'] = predictions_value_df['TestPredPosY'].astype(
#     float)

# # sns.regplot(x='Test True PosX', y='Test Pred PosX', data=predictions_value_df)

# # sns.regplot(x='Test True PosY', y='Test Pred PosY',
# #             data=predictions_value_df, color="g")
# predictions_value_df = predictions_value_df.drop(['Predict'], axis=1)


# subtractionResultsX = (
#     predictions_value_df['TestTruePosX'] - predictions_value_df['TestPredPosX'])**2
# subtractionResultsY = (
#     predictions_value_df['TestTruePosY'] - predictions_value_df['TestPredPosY'])**2

# addResult = np.sqrt(subtractionResultsX+subtractionResultsY)

# triSubtractionResultsX = (
#     predictions_value_df['TestTruePosX'] - predictions_value_df['TriPosX'])**2
# triSubtractionResultsY = (
#     predictions_value_df['TestTruePosY'] - predictions_value_df['TriPosY'])**2

# triAddResult = np.sqrt(triSubtractionResultsX+triSubtractionResultsY)

# # errorResult = math.sqrt((predictions_value_df['TestTruePosX']-predictions_value_df['TestPredPosX'])**2 + (predictions_value_df['TestTruePosY'] - predictions_value_df['TestPredPosY'])**2)
# # print(subtractionResultsX.head())
# predictions_value_df.insert(loc=4, column='ErrorX', value=subtractionResultsX)
# predictions_value_df.insert(loc=5, column='ErrorY', value=subtractionResultsY)
# # predictions_value_df.insert(loc=6, column='Error', value=errorResult)
# predictions_value_df.insert(loc=6, column='Euclidian', value=addResult)

# predictions_value_df.insert(loc=7, column='TriEuclidian', value=triAddResult)
# pd.set_option("display.max_rows", None)
# print(len(predictions_value_df))
# print(predictions_value_df.head(1000))

# # print(mean_squared_error(
# #     predictions_value_df['TestTruePosX'], predictions_value_df['TestPredPosX']))

# # print(mean_squared_error(
# #     predictions_value_df['TestTruePosY'], predictions_value_df['TestPredPosY']))

# print("MAE-PosX-Model: %f" % (mean_absolute_error(
#     predictions_value_df['TestTruePosX'], predictions_value_df['TestPredPosX'])))

# print("MAE-PosY-Model %f" % (mean_absolute_error(
#     predictions_value_df['TestTruePosY'], predictions_value_df['TestPredPosY'])))

# # print("MAE-PosX-Trilateration: %f" % (mean_absolute_error(
# #     predictions_value_df['TestTruePosX'], predictions_value_df['TriPosX'])))

# # print("MAE-PosY-Trilateration: %f" % (mean_absolute_error(
# #     predictions_value_df['TestTruePosY'], predictions_value_df['TriPosY'])))
# print("S.D. of error:")
# print(predictions_value_df[['ErrorX', 'ErrorY']].std(axis=0))
# print("Mean of Euclidian:")
# print(predictions_value_df['Euclidian'].mean(axis=0))
# print("Mean of TriEuclidian:")
# print(predictions_value_df['TriEuclidian'].mean(axis=0))

# model.save('D:/Work/Project/Github/Low-Power-IPS-Algorithm/model')
# tfjs.converters.save_keras_model(
#     model, "D:\Work\Project\Github\Low-Power-IPS-Web-App\model")

# # model_load = keras.models.load_model('D:/Work/Project/Github/Low-Power-IPS-Algorithm/model')
# # test_predictions_new = model_load.predict(X_test)
# # print(test_predictions_new)

# # layers = [[24, 24], [12, 12, 12]]
# # activations = ['relu', 'linear']
# # param_grid = dict(layers=layers, activation=activations,
# #                   batch_size=[16, 32], epochs=[350])
# # grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy')
# # grid_search = grid.fit(X_train, Y_train)
# # print("Best score: %0.3f" % grid_search.best_score_)
# # print(grid_search.best_estimator_)
# # print('best prarams:', grid.best_params_)
# print(tri_df.head(200))