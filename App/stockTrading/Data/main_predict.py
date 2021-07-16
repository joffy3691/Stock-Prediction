import datetime as dt
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from .utils import fit_days_data
from nsepy import get_history as gh
import datetime as dt
import tensorflow as tf
import pickle

def predict_data(symbol, is_agent = False):
    df_list=[]

    if(symbol is not None):

        df = gh(symbol, start = dt.date(2018, 9, 10), end = dt.date.today())

        df_list.append(df[-300:])

        df_list.append(svr_model(df, symbol, is_agent))

        df_list.append(lstm_model(df, symbol, is_agent))

    return df_list

def svr_model(df, symbol, is_agent):
    print("Started SVR")
    input_days = 18

    symbol = symbol

    df = fit_days_data(df, input_days = input_days)

    sc = StandardScaler()
    if(is_agent):
        filename = 'stockTrading/Data/SVR_Pickled/finalized_model_' + symbol + '.sav'
    else:
        filename = 'App/stockTrading/Data/SVR_Pickled/finalized_model_' + symbol + '.sav'
    regressor = pickle.load(open(filename, 'rb'))

    #Fetching the test data and preprocessing
    testdataframe = df[1]
    testdataframe['Date'] = testdataframe.index
    testdataframe['delta'] = ''

    for i in range(len(testdataframe)):
        if(i>0):
            testdataframe['delta'][i] = (testdataframe['Close'][i] - testdataframe['Close'][i-1])/testdataframe['Close'][i-1]
        else:
            testdataframe['delta'][i] = 0

    testdata = pd.DataFrame(columns = ['Date', 'Close'])
    testdata['Date'] = testdataframe['Date']
    testdata['Close'] = testdataframe['delta']

    inputs = testdata['Close'].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.fit_transform(inputs)
    X_test = []

    l=len(inputs)

    for i in range(input_days, l):
        X_test = (inputs[i - input_days:i])
        X_test = np.array(X_test)
        X_test = X_test.reshape(1,-1)
        abc = regressor.predict(X_test)
        b = abc.flatten()
        inputs = np.append(inputs, b)

    le=len(inputs)

    for i in range(le, le+30):
        X_test = (inputs[i - input_days:i])
        X_test = np.array(X_test)
        X_test = X_test.reshape(1,-1)
        abc = regressor.predict(X_test)
        b = abc.flatten()
        inputs = np.append(inputs, b)

    predicted_stock_price=inputs[l:len(inputs)]
    predicted_stock_price=predicted_stock_price.reshape(-1,1)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    #Visualizing the prediction
    testdataframe1 = df[2]
    testdataframe1['Date'] = testdataframe1.index
    testdata1 = pd.DataFrame(columns = ['Date', 'Close'])
    testdata1['Date'] = testdataframe1['Date']
    testdata1['Close'] = testdataframe1['Close']
    real_stock_price = testdata1.iloc[:, 1:2].values

    for i in range(len(testdata1)):
        if(i>0):
            predicted_stock_price[i] = testdata1['Close'][i-1]*(1 + predicted_stock_price[i])
        else:
            predicted_stock_price[i] = testdata1['Close'][i]

    for i in range(len(testdata1), len(testdata1) + 30):
        predicted_stock_price[i] = predicted_stock_price[i-1]*(1+predicted_stock_price[i])
    print("Completed SVR")
    return(predicted_stock_price)

def lstm_model(df, symbol, is_agent):
    print("Started LSTM")
    symbol = symbol
    input_days = 24

    df = fit_days_data(df, input_days = input_days)

    sc = StandardScaler()
    tf.keras.backend.clear_session()
    if(is_agent):
        regressor = tf.keras.models.load_model("stockTrading/Data/LSTM_Pickled/" + symbol +"_lstm", compile = False)
    else:
        regressor = tf.keras.models.load_model("App/stockTrading/Data/LSTM_Pickled/" + symbol +"_lstm", compile = False)

    #Fetching the test data and preprocessing
    testdataframe = df[1]
    testdataframe['Date'] = testdataframe.index
    testdataframe['delta'] = ''

    for i in range(len(testdataframe)):
        if(i>0):
            testdataframe['delta'][i] = (testdataframe['Close'][i] - testdataframe['Close'][i-1])/testdataframe['Close'][i-1]
        else:
            testdataframe['delta'][i] = 0
            
    testdata = pd.DataFrame(columns = ['Date', 'Close'])
    testdata['Date'] = testdataframe['Date']
    testdata['Close'] = testdataframe['delta']

    inputs = testdata['Close'].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.fit_transform(inputs)
    X_test = []

    l=len(inputs)
    for i in range(input_days, l):
        X_test = (inputs[i - input_days:i, 0])
        X_test = np.array(X_test)
        X_test = X_test.reshape(1, input_days, 1)

        abc = regressor.predict(X_test)
        b = abc.flatten()

        inputs = np.append(inputs, b)
        inputs = inputs.reshape(-1, 1)
    le=len(inputs)

    for i in range(le, le+30):
        X_test = (inputs[i - input_days:i, 0])
        X_test = np.array(X_test)
        X_test = X_test.reshape(1, input_days, 1)

        abc = regressor.predict(X_test)
        b = abc.flatten()

        inputs = np.append(inputs, b)
        inputs = inputs.reshape(-1, 1)

    predicted_stock_price=inputs[l:len(inputs)]



    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    #Visualizing the prediction
    testdataframe1 = df[2]
    testdataframe1['Date'] = testdataframe1.index
    testdata1 = pd.DataFrame(columns = ['Date', 'Close'])
    testdata1['Date'] = testdataframe1['Date']
    testdata1['Close'] = testdataframe1['Close']
    real_stock_price = testdata1.iloc[:, 1:2].values

    for i in range(len(testdata1)):
        if(i>0):
            predicted_stock_price[i] = testdata1['Close'][i-1]*(1 + predicted_stock_price[i])
        else:
            predicted_stock_price[i] = testdata1['Close'][i]

    for i in range(len(testdata1), len(testdata1) + 30):
        predicted_stock_price[i] = predicted_stock_price[i-1]*(1+predicted_stock_price[i])
    print("Completed LSTM")
    return(predicted_stock_price)