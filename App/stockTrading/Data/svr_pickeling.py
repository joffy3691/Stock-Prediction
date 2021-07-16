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

from nsepy import get_history as gh
import datetime as dt
import pickle

symbol_list = pd.read_csv("App/stockTrading/Data/ind_nifty50list.csv")
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

    data2 = pd.DataFrame(columns=['Date', 'VWAP'])
    data2['Date'] = stk_data['Date']
    data2['VWAP'] = stk_data['delta']

    train_set = data2.iloc[:, 1:2].values
    sc = StandardScaler()
    training_set_scaled = sc.fit_transform(train_set)
    X_train = []
    y_train = []

    for i in range(input_days, len(training_set_scaled)):
        X_train.append(training_set_scaled[i - input_days:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Defining the LSTM Recurrent Model
    regressor = svm.SVR(kernel='rbf', C=1000.0, gamma=0.1)  # svm.SVR()
    regressor.fit(X_train, y_train)
    filename = 'finalized_model_' + symbol + '.sav'
    pickle.dump(regressor, open(filename, 'wb'))