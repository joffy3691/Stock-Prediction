from datetime import date, datetime
import schedule
import sys
import os
import django
from django.conf import settings
from tensorflow.python.framework.op_def_registry import sync
from Data import main_predict
from stockTrading.settings import DATABASES, INSTALLED_APPS
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "stockTrading.settings"
)
django.setup()

from accounts.models import Wallet, Deposit, Trade, Stock
from django.contrib.auth.models import User
import time

import nsepy
import pandas as pd
import yfinance as yf

symbol_list = pd.read_csv("stockTrading/Data/ind_nifty50list.csv")
symbol_list = symbol_list["Symbol"].tolist()

  
# Functions setup
def get_ltp(symbol):
    ticker = yf.Ticker(symbol + ".NS")
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]
        
def execute_trade(user, stock, amount, quantity, type, is_open, open_price, target, trailing_sl):
    trade = Trade(user = user, stock = stock, amount = amount, quantity = quantity, type = type, is_open = is_open, open_price = open_price, target = target, trailing_sl = trailing_sl, date = datetime.now())
    trade.save()
    return True

def create_trade_for_users(symbol, type, cmp, target, trailing_sl):
    user_ids = User.objects.values_list('id', flat=True)
    for user in user_ids:
        user_instance = User.objects.filter(id=user).first() 
        open_trade= Trade.objects.filter(user=user_instance).filter(stock=symbol).filter(is_open=True).count()
        wallet = Wallet.objects.filter(user=user).first()
        if wallet is not None and wallet.balance >= 100 and not open_trade:
            execute_trade(user_instance, symbol, 100, 100/cmp, type, True, cmp, target, trailing_sl)
            wallet.balance = wallet.balance - 100
            wallet.save()

def buy_or_sell(cmp, max1, max2, min1, min2, symbol):
    max_of_both = max(max1, max2)
    min_of_both = min(min1, min2)
    max_percentage = (max_of_both - cmp)/cmp
    max_percentage *= 100
    min_percentage = (cmp - min_of_both)/cmp
    min_percentage *= 100
    if(max_percentage >= 8 and min(max1, max2) >= 1.02*cmp): #Worthy of buy
        create_trade_for_users(symbol, "buy", cmp, (max1 + max2)/2, 0.98*cmp)
    elif(min_percentage >= 8 and max(min1, min2) <= 0.98*cmp): #Worthy of sell
        create_trade_for_users(symbol, "sell", cmp, (min1 + min2)/2, 1.02*cmp)

def perform_predictions():
    for symbol in symbol_list:
        print(symbol)
        cmp = get_ltp(symbol)
        vals = main_predict.predict_data(symbol, is_agent=True)
        svr_pred = vals[1][-30:]
        lstm_pred = vals[2][-30:]
        svr_max = max(svr_pred)
        svr_min = min(svr_pred)
        lstm_max = max(lstm_pred)
        lstm_min = min(lstm_pred)
        buy_or_sell(cmp, svr_max[0], lstm_max[0], svr_min[0], lstm_min[0], symbol)

def update_trades():
    for symbol in symbol_list:
        print("Updating " + symbol + " - all trades")
        trades = Trade.objects.filter(stock = symbol).filter(is_open = True)
        cmp = get_ltp(symbol)
        stock = Stock.objects.filter(stock = symbol)
        if stock.first() is not None:
            stock = stock.first()
            old_ltp = stock.ltp
            stock.ltp = cmp
            stock.last_updated = datetime.now()
        stock.save()
        if trades.first() is not None:
            for trade in trades:
                if trade.type == "buy":
                    if cmp >= trade.target or cmp <= trade.trailing_sl:
                        trade.close_price = cmp
                        trade.is_open = False
                    elif cmp >= old_ltp:
                        trade.trailing_sl += cmp - trade.open_price
                else:
                    if cmp <= trade.target or cmp >= trade.trailing_sl:
                        trade.close_price = cmp
                        trade.is_open = False
                    elif cmp <= old_ltp:
                        trade.trailing_sl -= trade.open_price - cmp
                trade.last_updated = datetime.now()
                trade.save()

#schedule.every(15).minutes.do(update_trades)
#schedule.every().day.at("00:00").do(perform_predictions)

perform_predictions()
update_trades()

# Loop so that the scheduling task
# keeps on running all time.
# while True:
  
#     # Checks whether a scheduled task 
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)