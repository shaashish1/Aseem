#DISCLAIMER:
#1) This sample code is for learning purposes only.
#2) Always be very careful when dealing with codes in which you can place orders in your account.
#3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
#4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
#5) Aseem Singhal do not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
#6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
#7) This is NOT a tip providing service/code.
#8) This is NOT a software. Its a tool that works as per the inputs given by you.
#9) Slippage is dependent on market conditions.
#10) Option trading and automatic API trading are subject to market risks

import time
import math
from datetime import datetime,timedelta
from pytz import timezone
import ta    # Python TA Lib
import pandas as pd
import pandas_ta as pta    # Pandas TA Libv
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def importLibrary():
    global shoonya_broker
    global nuvama_broker
    global icici_broker
    global angel_broker
    global alice_broker
    global fyers_broker
    global zerodha_broker
    global upstox_broker
    global helper
    global api_connect
    global breeze
    global alice
    global fyers
    global kc
    global api
    global xt
    global xt1

    if nuvama_broker == 1:
        import nuvama_login
        import helper_nuvama as helper
        api_connect = nuvama_login.api_connect

    if icici_broker == 1:
        import icici_login
        import helper_icici as helper
        breeze = icici_login.breeze

    if angel_broker == 1:
        import helper_angel as helper
        helper.login_trading()
        time.sleep(15)
        helper.login_historical()

    if alice_broker == 1:
        import alice_login
        import helper_alice as helper
        alice = alice_login.alice

    if fyers_broker == 1:
        from fyers_apiv3 import fyersModel
        import helper_fyers as helper
        app_id = open("fyers_client_id.txt",'r').read()
        access_token = open("fyers_access_token.txt",'r').read()
        fyers = fyersModel.FyersModel(token=access_token,is_async=False,client_id=app_id)

    if shoonya_broker == 1:
        from NorenApi import NorenApi
        import helper_shoonya as helper
        api = NorenApi()
        api.token_setter()

    if zerodha_broker == 1:
        from kiteconnect import KiteTicker
        from kiteconnect import KiteConnect
        import helper_zerodha as helper
        apiKey = open("zerodha_api_key.txt",'r').read()
        accessToken = open("zerodha_access_token.txt",'r').read()
        kc = KiteConnect(api_key=apiKey)
        kc.set_access_token(accessToken)

    if upstox_broker == 1:
        import helper_upstox as helper

    if iifl_broker == 1:
        from Connect import XTSConnect
        import helper_iifl as helper
        """Dealer credentials"""
        with open('iifl_api_key.txt','r') as f:
            API_KEY = f.read()
        with open('iifl_secret_key.txt','r') as f:
            API_SECRET = f.read()
        with open('user_id.txt','r') as f:
            userID = f.read()
        XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
        source = "WEBAPI"

        """Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
        xt = XTSConnect(API_KEY, API_SECRET, source)

        """Using the xt object we created call the interactive login Request"""
        response = xt.interactive_login()
        print("Login: ", response)

        with open('iifl_market_api_key.txt','r') as f:
            API_KEY_M = f.read()
        with open('iifl_market_secret_key.txt','r') as f:
            API_SECRET_M = f.read()
        # Initialise
        xt1 = XTSConnect(API_KEY_M, API_SECRET_M, source)
        # Login for authorization token
        response = xt1.marketdata_login()
        print("Market Data: ", response)


#If you have any below brokers, then make it 1
shoonya_broker = 0
nuvama_broker = 0
icici_broker = 0
angel_broker = 0
alice_broker = 0
fyers_broker = 1
zerodha_broker = 0
upstox_broker = 0
iifl_broker = 0

importLibrary()

def placeOrder1(inst ,t_type,qty,order_type,price,variety, papertrading=0):
    global api_connect
    global breeze
    global fyers
    global api
    global kc
    if papertrading == 0:
        return 0
    elif (nuvama_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, api_connect,papertrading)
    elif (icici_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, breeze,papertrading)
    elif (alice_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, alice,papertrading)
    elif (fyers_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,fyers, papertrading)
    elif (shoonya_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,api, papertrading)
    elif (zerodha_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,kc, papertrading)
    elif (iifl_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,xt, papertrading)
    else:
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, papertrading)

def getHistorical1(ticker,interval,duration):
    global api_connect
    global breeze
    global fyers
    global kc
    global alice
    global api
    if (nuvama_broker == 1):
        #THIS NEEDS TO BE UPDATED FOR STOCK/ETC
        #For index == INDEX, stock == EQUITY, future == FUTUREINDEX, option == OPTIONINDEX
        #optional_param1 = "INDEX", optional_param2 = api_connect
        return helper.getHistorical(ticker,interval,duration,"INDEX",api_connect)
    elif (icici_broker == 1):
        #optional_param1 = breeze
        return helper.getHistorical(ticker,interval,duration,breeze)
    elif (alice_broker == 1):
        #For index == INDEX, otherise == "NO"
        #optional_param1 = alice, optional_param2 = "INDEX"
        return helper.getHistorical(ticker,interval,duration,alice,"INDEX")
    elif (fyers_broker == 1):
        return helper.getHistorical(ticker,interval,duration,fyers)
    elif (shoonya_broker == 1):
        return helper.getHistorical(ticker,interval,duration,api)
    elif (zerodha_broker == 1):
        return helper.getHistorical(ticker,interval,duration,kc)
    elif (iifl_broker == 1):
        return helper.getHistorical(ticker,interval,duration,xt1)
    else:
        return helper.getHistorical(ticker,interval,duration)

#############################################################################################################
tickers = ["NSE:ABFRL-EQ",
           "NSE:ADANIENT-EQ",
           "NSE:INFY-EQ"]

capital = 5000 #position size
indicator_dir = {} #directory to store super trend status for each ticker
timeFrame = 1
papertrading = 0 #If paper trading is 0, then paper trading will be done. If paper trading is 1, then live trade
candle_formed = 0

entryHour   = 9
entryMinute = 19
entrySecond = 0
startTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, entryHour, entryMinute, entrySecond)
startTime = startTime.time()
print(startTime)


for ticker in tickers:
    indicator_dir[ticker] = [0,0,0,0,0,0,0,0]
    #0 high
    #1 low
    #(2 current trade) 0/BUY/SELL
    #(3 entry price)
    # (4 sl price) 0.5% of entry price,
    # #5 target 1%
    # #6 Exit Price,
    # 7 Quantity

x = 1
while x == 1:
    dt1 = datetime.now()

    #keep checking if entry time is reached
    if (dt1.time() >= startTime):
        print("time reached")
        x = 2
    else:
        time.sleep(1)
        print(dt1 , " Waiting for Time to check new ATM ")


while x == 2:
    dt1 = datetime.now()

    if dt1.second < 3 and dt1.minute % timeFrame == 0:

        if candle_formed == 0:
            for ticker in tickers:
                print("Checking for: ",ticker)
                try:
                    data = getHistorical1(ticker,timeFrame,5)
                    print(data)
                    print(data[['close']].to_string(index=True))
                    high = data['high'].to_numpy()
                    low = data['low'].to_numpy()

                    if shoonya_broker == 1 or icici_broker == 1:
                        high = [float(x) for x in high]
                        low = [float(x) for x in low]

                    indicator_dir[ticker][0] = high[-1]
                    indicator_dir[ticker][1] = low[-1]
                except:
                    print("API error for ticker :",ticker)

        #checking for entry at close of candle
        else:
            for ticker in tickers:
                print("Checking for: ",ticker)
                try:
                    data = getHistorical1(ticker,timeFrame,5)
                    print(data)
                    print(data[['close']].to_string(index=True))
                    opens = data['open'].to_numpy()
                    high = data['high'].to_numpy()
                    low = data['low'].to_numpy()
                    close = data['close'].to_numpy()
                    volume = data['volume'].to_numpy()
                    #ttime = data['date']

                    if shoonya_broker == 1 or icici_broker == 1:
                        opens = [float(x) for x in opens]
                        high = [float(x) for x in high]
                        low = [float(x) for x in low]
                        close = [float(x) for x in close]
                        if (volume[-1] != ''):
                            volume = [float(x) for x in volume]

                    #rsi = ta.momentum.RSIIndicator(pd.Series(close),14,False).rsi().iloc[-1]
                    quantity = int(capital/close[-1])
                    quantity = round(quantity,0)

                    #check for BUY ENTRY
                    if (indicator_dir[ticker][2] == 0) and (close[-1]>indicator_dir[ticker][0]):
                        print(ticker, " Take BUY trade")
                        oid = placeOrder1(ticker, "BUY", quantity, "MARKET", 0, "regular",papertrading)
                        indicator_dir[ticker][2] = "BUY"
                        indicator_dir[ticker][3] = close[-1]
                        stoploss = close[-1] * (1-0.005)
                        target = close[-1] * (1+0.01)
                        indicator_dir[ticker][4] = stoploss
                        indicator_dir[ticker][5] = target
                        indicator_dir[ticker][7] = quantity

                    #check for SELL ENTRY
                    elif (indicator_dir[ticker][2] == 0) and (close[-1]<indicator_dir[ticker][1]):
                        print(ticker, " Take SELL trade")
                        oid = placeOrder1(ticker, "SELL", quantity, "MARKET", 0, "regular",papertrading)
                        indicator_dir[ticker][2] = "SELL"
                        indicator_dir[ticker][3] = close[-1]
                        stoploss = close[-1] * (1+0.005)
                        target = close[-1] * (1-0.01)
                        indicator_dir[ticker][4] = stoploss
                        indicator_dir[ticker][5] = target
                        indicator_dir[ticker][7] = quantity

                    print(ticker, indicator_dir[ticker])

                except:
                    print("API error for ticker :",ticker)

        candle_formed = 1
        time.sleep(3)

    elif candle_formed == 1:
        for ticker in tickers:
            ltp = helper.getLTP(ticker)

            #BUY EXIT
            if (indicator_dir[ticker][2] == "BUY") and ((ltp < indicator_dir[ticker][4]) or (ltp > indicator_dir[ticker][5])):
                print(ticker, " BUY EXIT")
                oid = placeOrder1(ticker, "SELL", indicator_dir[ticker][7], "MARKET", 0, "regular",papertrading)
                indicator_dir[ticker][2] = -1
                indicator_dir[ticker][6] = ltp

            #SELL EXIT
            elif (indicator_dir[ticker][2] == "SELL") and ((ltp > indicator_dir[ticker][4]) or (ltp < indicator_dir[ticker][5])):
                print(ticker, " SELL EXIT")
                oid = placeOrder1(ticker, "BUY", indicator_dir[ticker][7], "MARKET", 0, "regular",papertrading)
                indicator_dir[ticker][2] = -1
                indicator_dir[ticker][6] = ltp

            print(indicator_dir[ticker])

    #TIME EXIT
    if candle_formed == 1 and (dt1.hour >= 14 and dt1.minute >= 15):
        for ticker in tickers:
            ltp = helper.getLTP(ticker)

            #BUY EXIT
            if (indicator_dir[ticker][2] == "BUY"):
                print(ticker, " BUY TIME EXIT")
                oid = placeOrder1(ticker, "SELL", indicator_dir[ticker][7], "MARKET", 0, "regular",papertrading)
                indicator_dir[ticker][2] = -1
                indicator_dir[ticker][6] = ltp

            #SELL EXIT
            elif (indicator_dir[ticker][2] == "SELL"):
                print(ticker, " SELL TIME EXIT")
                oid = placeOrder1(ticker, "BUY", indicator_dir[ticker][7], "MARKET", 0, "regular",papertrading)
                indicator_dir[ticker][2] = -1
                indicator_dir[ticker][6] = ltp

            print(indicator_dir[ticker])
        x = 3
        print("CODE COMPLETED")
        break

