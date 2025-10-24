#DISCLAIMER:
#1) This sample code is for learning purposes only.
#2) Always be very careful when dealing with codes in which you can place orders in your account.
#3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
#4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
#5) TFU and Aseem Singhal do not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
#6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
#7) This is NOT a tip providing service/code.
#8) This is NOT a software. Its a tool that works as per the inputs given by you.
#9) Slippage is dependent on market conditions.
#10) Option trading and automatic API trading are subject to market risks

# from SmartWebsocketv2 import SmartWebSocketV2

from SmartApi import SmartConnect
import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
import pyotp
import traceback

######PIVOT POINTS##########################
####################__INPUT__#####################

trading_api_key= '6L9HcEAl'
hist_api_key = 'yrneyZ6r'
username = 'P792853'
password = '1317'   #This is 4 digit MPIN
otp_token = 'NJMJOV5A6NTO7HJ4DTN4UOFFOI'
allinst = pd.read_json('https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json')

def login_trading():
    global trading_obj
    totp=pyotp.TOTP(otp_token).now()

    trading_obj=SmartConnect(api_key=trading_api_key)
    trading_session=trading_obj.generateSession(username,password,totp)
    print(trading_session)

    if trading_session['message'] == 'SUCCESS':
        trading_refreshToken= trading_session['data']['refreshToken']  #till here
        #trading_authToken = trading_session['data']['jwtToken']
        #trading_feedToken=trading_obj.getfeedToken()
        #print(".........................................")
        #print(trading_feedToken)
        #print("Connection Successful")
    else:
        print(trading_session['message'])

    #SmartWebSocketV2OBJ = SmartWebSocketV2(trading_authToken, trading_api_key, username, trading_feedToken)

def login_historical():
    global hist_obj
    totp=pyotp.TOTP(otp_token).now()
    hist_obj=SmartConnect(api_key=hist_api_key)
    hist_session=hist_obj.generateSession(username,password,totp)
    print(hist_session)

    if hist_session['message'] == 'SUCCESS':
        hist_refreshToken= hist_session['data']['refreshToken']
        #hist_authToken = hist_session['data']['jwtToken']
        #hist_feedToken=hist_obj.getfeedToken()
        #print(".........................................")
        #print(hist_feedToken)
        #print("Connection Successful")
    else:
        print(hist_session['message'])



def get_tokens(symbols):
    for i in range(len(allinst)):
        if symbols[4:] == "NIFTY":
            return 99926000
        elif symbols[4:] == "BANKNIFTY":
            return 99926009
        elif symbols[4:] == "FINNIFTY":
            return 99926037
        elif allinst['symbol'][i] == symbols[4:] and allinst['exch_seg'][i] == symbols[:3]:
            if allinst['expiry'][i] == "":
                exch = get_exch_type(symbols, 'NO')
            else:
                exch = get_exch_type(symbols, 'YES')
            # print(exch)
            # symbol_token=allinst['token'][i]
            print(allinst['token'][i])
            return allinst['token'][i]


def get_exch_type(symbol, exp):
    if exp == 'NO':
        if symbol[:3] == 'NSE': return 1
        elif symbol[:3] == 'BSE': return 3
    if exp == 'YES':
        if symbol[:3] == 'NFO': return 2
        elif symbol[:3] == 'BSE': return 4
        elif symbol[:3] == 'MCX': return 5
        elif symbol[:3] == 'NCDEX': return 6
        elif symbol[:3] == 'CDS': return 7



def getNiftyExpiryDate():
    nifty_expiry = {
        datetime.datetime(2025, 1, 2).date(): "02JAN25",
        datetime.datetime(2025, 1, 9).date(): "09JAN25",
        datetime.datetime(2025, 1, 16).date(): "16JAN25",
        datetime.datetime(2025, 1, 23).date(): "23JAN25",
        datetime.datetime(2025, 1, 30).date(): "30JAN25",
        datetime.datetime(2025, 2, 6).date(): "06FEB25",
        datetime.datetime(2025, 2, 13).date(): "13FEB25",
        datetime.datetime(2025, 2, 20).date(): "20FEB25",
        datetime.datetime(2025, 2, 27).date(): "27FEB25",
        datetime.datetime(2025, 3, 6).date(): "06MAR25",
        datetime.datetime(2025, 3, 13).date(): "13MAR25",
        datetime.datetime(2025, 3, 20).date(): "20MAR25",
        datetime.datetime(2025, 3, 27).date(): "27MAR25",
        datetime.datetime(2025, 4, 3).date(): "03APR25",
        datetime.datetime(2025, 4, 10).date(): "10APR25",
        datetime.datetime(2025, 4, 17).date(): "17APR25",
        datetime.datetime(2025, 4, 24).date(): "24APR25",
        datetime.datetime(2025, 5, 1).date(): "01MAY25",
        datetime.datetime(2025, 5, 8).date(): "08MAY25",
        datetime.datetime(2025, 5, 15).date(): "15MAY25",
        datetime.datetime(2025, 5, 22).date(): "22MAY25",
        datetime.datetime(2025, 5, 29).date(): "29MAY25",
        datetime.datetime(2025, 6, 5).date(): "05JUN25",
        datetime.datetime(2025, 6, 12).date(): "12JUN25",
        datetime.datetime(2025, 6, 19).date(): "19JUN25",
        datetime.datetime(2025, 6, 26).date(): "26JUN25",
        datetime.datetime(2025, 7, 3).date(): "03JUL25",
        datetime.datetime(2025, 7, 10).date(): "10JUL25",
        datetime.datetime(2025, 7, 17).date(): "17JUL25",
        datetime.datetime(2025, 7, 24).date(): "24JUL25",
        datetime.datetime(2025, 7, 31).date(): "31JUL25",
        datetime.datetime(2025, 8, 7).date(): "07AUG25",
        datetime.datetime(2025, 8, 14).date(): "14AUG25",
        datetime.datetime(2025, 8, 21).date(): "21AUG25",
        datetime.datetime(2025, 8, 28).date(): "28AUG25",
        datetime.datetime(2025, 9, 4).date(): "04SEP25",
        datetime.datetime(2025, 9, 11).date(): "11SEP25",
        datetime.datetime(2025, 9, 18).date(): "18SEP25",
        datetime.datetime(2025, 9, 25).date(): "25SEP25",
        datetime.datetime(2025, 10, 2).date(): "02OCT25",
        datetime.datetime(2025, 10, 9).date(): "09OCT25",
        datetime.datetime(2025, 10, 16).date(): "16OCT25",
        datetime.datetime(2025, 10, 23).date(): "23OCT25",
        datetime.datetime(2025, 10, 30).date(): "30OCT25",
        datetime.datetime(2025, 11, 6).date(): "06NOV25",
        datetime.datetime(2025, 11, 13).date(): "13NOV25",
        datetime.datetime(2025, 11, 20).date(): "20NOV25",
        datetime.datetime(2025, 11, 27).date(): "27NOV25",
        datetime.datetime(2025, 12, 4).date(): "04DEC25",
        datetime.datetime(2025, 12, 11).date(): "11DEC25",
        datetime.datetime(2025, 12, 18).date(): "18DEC25",
        datetime.datetime(2025, 12, 25).date(): "25DEC25",
    }


    today = datetime.datetime.now().date()

    for date_key, value in nifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getBankNiftyExpiryDate():
    banknifty_expiry = {
        datetime.datetime(2025, 1, 30).date(): "30JAN25",
        datetime.datetime(2025, 2, 27).date(): "27FEB25",
        datetime.datetime(2025, 3, 27).date(): "27MAR25",
        datetime.datetime(2025, 4, 24).date(): "24APR25",
        datetime.datetime(2025, 5, 29).date(): "29MAY25",
        datetime.datetime(2025, 6, 26).date(): "26JUN25",
        datetime.datetime(2025, 7, 31).date(): "31JUL25",
        datetime.datetime(2025, 8, 28).date(): "28AUG25",
        datetime.datetime(2025, 9, 25).date(): "25SEP25",
        datetime.datetime(2025, 10, 30).date(): "30OCT25",
        datetime.datetime(2025, 11, 27).date(): "27NOV25",
        datetime.datetime(2025, 12, 25).date(): "25DEC25",
        
    }

    today = datetime.datetime.now().date()

    for date_key, value in banknifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getFinNiftyExpiryDate():
    finnifty_expiry = {

        datetime.datetime(2025, 1, 30).date(): "30JAN25",
        datetime.datetime(2025, 2, 27).date(): "27FEB25",
        datetime.datetime(2025, 3, 27).date(): "27MAR25",
        datetime.datetime(2025, 4, 24).date(): "24APR25",
        datetime.datetime(2025, 5, 29).date(): "29MAY25",
        datetime.datetime(2025, 6, 26).date(): "26JUN25",
        datetime.datetime(2025, 7, 31).date(): "31JUL25",
        datetime.datetime(2025, 8, 28).date(): "28AUG25",
        datetime.datetime(2025, 9, 25).date(): "25SEP25",
        datetime.datetime(2025, 10, 30).date(): "30OCT25",
        datetime.datetime(2025, 11, 27).date(): "27NOV25",
        datetime.datetime(2025, 12, 25).date(): "25DEC25",
    }

    today = datetime.datetime.now().date()

    for date_key, value in finnifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getIndexSpot(stock):
    if stock == "BANKNIFTY":
        name = "NSE:BANKNIFTY"
    elif stock == "NIFTY":
        name = "NSE:NIFTY"
    elif stock == "FINNIFTY":
        name = "NSE:FINNIFTY"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return "NFO:" + str(stock) + str(intExpiry)+str(strike)+str(ce_pe)

def getLTP(instrument):
    url = "http://localhost:4000/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data

def manualLTP(symbol):
    global hist_obj
    exch = symbol[:3]
    sym = symbol[4:]
    tok = get_tokens(symbol)
    ltp = hist_obj.ltpData(exch, symbol, tok)
    time.sleep(1)
    return (ltp['data']['ltp'])

def placeOrder(inst ,t_type,qty,order_type,price,variety, papertrading=0):
    global trading_obj
    variety = 'NORMAL'
    exch = inst[:3]
    symbol_name = inst[4:]
    if(order_type=="MARKET"):
        price = 0
    #papertrading = 0 #if this is 1, then real trades will be placed
    token = get_tokens(inst)

    try:
        if (papertrading == 1):
            Targetorderparams = {
                "variety": "NORMAL",
                "tradingsymbol": symbol_name,
                "symboltoken": token,
                "transactiontype": t_type,
                "exchange": exch,
                "ordertype": order_type,
                "producttype": "INTRADAY", #
                "duration": "DAY",
                "price": price,
                "squareoff": 0,
                "stoploss": 0,
                "triggerprice": 0,
                "trailingStopLoss": 0,
                "quantity": qty
            }

            print(Targetorderparams)
            orderId = trading_obj.placeOrder(Targetorderparams)
            print("The order id is: {}".format(orderId))
            return orderId
        else:
            return 0
    except Exception as e:
        traceback.print_exc()
        print("Order placement failed: {}".format(e.message))

def getHistorical(ticker,interval,duration):
    exch = ticker[:3]
    sym = ticker[4:]
    tok = get_tokens(ticker)

    time_intervals = {
        1: "ONE_MINUTE",
        3: "THREE_MINUTE",
        5: "FIVE_MINUTE",
        10: "TEN_MINUTE",
        15: "FIFTEEN_MINUTE",
        30: "THIRTY_MINUTE",
        60: "ONE_HOUR"
    }

    interval_str = time_intervals.get(interval, "Key not found")
    interval_str = "ONE_MINUTE"

    #find todate
    current_time = datetime.datetime.now()
    previous_minute_time = current_time - timedelta(minutes=1)
    start_date = previous_minute_time - timedelta(days=duration)
    to_date_string = previous_minute_time.strftime("%Y-%m-%d %H:%M")
    start_date_string = start_date.strftime("%Y-%m-%d %H:%M")

    historyparams = {
        "exchange": str(exch),
        #  "tradingsymbol":str(sym),
        "symboltoken": str(tok),
        "interval": interval_str,
        "fromdate": start_date_string,
        "todate": to_date_string
    }
    hist_data = hist_obj.getCandleData(historicDataParams= historyparams)
    hist_data = pd.DataFrame(hist_data['data'])
    hist_data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    hist_data['datetime2'] = hist_data['timestamp'].copy()
    hist_data['timestamp'] = pd.to_datetime(hist_data['timestamp'])
    hist_data.set_index('timestamp', inplace=True)
    #finaltimeframe = str(interval)  + "min"
    if interval < 375:
        finaltimeframe = str(interval)  + "min"
    elif interval == 375:
        finaltimeframe = "D"


    # Resample to a specific time frame, for example, 30 minutes
    resampled_df = hist_data.resample(finaltimeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'datetime2': 'first'
    })

    # If you want to fill any missing values with a specific method, you can use fillna
    #resampled_df = resampled_df.fillna(method='ffill')  # Forward fill

    resampled_df = resampled_df.dropna(subset=['open'])
    return (resampled_df)

def getHistorical_old(ticker,interval,duration):
    exch = ticker[:3]
    sym = ticker[4:]
    tok = get_tokens(ticker)

    time_intervals = {
        1: "ONE_MINUTE",
        3: "THREE_MINUTE",
        5: "FIVE_MINUTE",
        10: "TEN_MINUTE",
        15: "FIFTEEN_MINUTE",
        30: "THIRTY_MINUTE",
        60: "ONE_HOUR"
    }

    interval_str = time_intervals.get(interval, "Key not found")

    #find todate
    current_time = datetime.datetime.now()
    previous_minute_time = current_time - timedelta(minutes=1)
    start_date = previous_minute_time - timedelta(days=duration)
    to_date_string = previous_minute_time.strftime("%Y-%m-%d %H:%M")
    start_date_string = start_date.strftime("%Y-%m-%d %H:%M")

    historyparams = {
        "exchange": str(exch),
        #  "tradingsymbol":str(sym),
        "symboltoken": str(tok),
        "interval": interval_str,
        "fromdate": start_date_string,
        "todate": to_date_string
    }
    hist_data = hist_obj.getCandleData(historicDataParams= historyparams)
    hist_data = pd.DataFrame(hist_data['data'])
    hist_data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    return (hist_data)