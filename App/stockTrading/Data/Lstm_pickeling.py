import datetime as dt
from sklearn import model_selection
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing, svm
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import pickle
from nsepy import get_history as gh
import datetime as dt
import tensorflow as tf
from tensorflow import keras
symbol_list = pd.read_csv("C:/Users/vishn/PycharmProjects/stock/stock-trading/App/stockTrading/Data/ind_nifty50list.csv")
symbol_list = symbol_list["Symbol"].tolist()
for symbol in symbol_list:

    input_days = 18

    df = gh(symbol, start = dt.date(2018, 9, 10), end = dt.date.today())

    stk_data = df

    stk_data['Date'] = stk_data.index
    stk_data['delta'] = ''

    for i in range(len(stk_data)):
        if(i>0):
            stk_data['delta'][i] = (stk_data['VWAP'][i] - stk_data['VWAP'][i-1])/stk_data['VWAP'][i-1]
        else:
            stk_data['delta'][i] = 0

    data2 = pd.DataFrame(columns = ['Date', 'VWAP', 'High', 'Low', 'Close'])
    data2['Date'] = stk_data['Date']
    data2['VWAP'] = stk_data['delta']
    data2['High'] = stk_data['High']
    data2['Low'] = stk_data['Low']
    data2['Close'] = stk_data['Close']

    train_set = data2.iloc[:, 1:2].values

    sc = StandardScaler()
    training_set_scaled = sc.fit_transform(train_set)
    X_train = []
    y_train = []
    for i in range(input_days, len(training_set_scaled)):
        X_train.append(training_set_scaled[i-input_days:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

        #Defining the LSTM Recurrent Model
    regressor = Sequential()
    regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 50))
    regressor.add(Dropout(0.2))
    regressor.add(Dense(units = 1))

    checkpoint_filepath = 'LSTM_Pickled/checkpoint/'+symbol + '/'+symbol +'_lstm'
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['mse'])
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='loss',
        mode='min',
        save_best_only=True)

    regressor.fit(X_train, y_train, epochs = 200,callbacks=[model_checkpoint_callback])
    print("Modelf it")
    regressor.load_weights(checkpoint_filepath)
    print("Model save")
    regressor.save('LSTM_Pickled/'+symbol + '_lstm')
