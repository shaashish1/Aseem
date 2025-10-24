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

from NorenApi import NorenApi
import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

######PIVOT POINTS##########################
####################__INPUT__#####################

exchange1 = "NSE"

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
        name = "NSE:Nifty Bank"
    elif stock == "NIFTY":
        name = "NSE:Nifty 50"
    elif stock == "FINNIFTY":
        name = "NSE:Nifty Fin Service"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return "NFO:" + str(stock) + str(intExpiry)+str(ce_pe[0])+str(strike)

def getLTP(instrument):
    url = "http://localhost:4002/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data

def manualLTP(symbol,api):
    exch = symbol[:3]
    stockname = symbol[4:]
    temp = api.get_quotes(exchange=exch, token=stockname)
    return float(temp['lp'])

def placeOrder(inst ,t_type,qty,order_type,price,variety, api,papertrading=0):
    exch = inst[:3]
    symb = inst[4:]
    #paperTrading = 0 #if this is 1, then real trades will be placed
    if( t_type=="BUY"):
        t_type="B"
    else:
        t_type="S"

    if(order_type=="MARKET"):
        order_type="MKT"
        price = 0
    elif(order_type=="LIMIT"):
        order_type="LMT"

    try:
        if(papertrading == 1):
            print(t_type)
            print(exch)
            print(symb)
            print(qty)
            print(order_type)
            print(price)
            order_id = api.place_order(buy_or_sell=t_type,  #B, S
                                       product_type="I", #C CNC, M NRML, I MIS
                                       exchange=exch,
                                       tradingsymbol=symb,
                                       quantity = qty,
                                       discloseqty=qty,
                                       price_type= order_type, #LMT, MKT, SL-LMT, SL-MKT
                                       price = price,
                                       trigger_price=price,
                                       amo="NO",#YES, NO
                                       retention="DAY"
                                       )
            print(" => ", symb , order_id['norenordno'] )
            return order_id['norenordno']

        else:
            order_id=0
            return order_id

    except Exception as e:
        print(" => ", symb , "Failed : {} ".format(e))

def getHistorical(ticker,interval,duration,api):
    #token = pd.read_csv(f'https://api.shoonya.com/{exchange1}_symbols.txt.zip')
    exch = ticker[:3]
    token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')
    stockname = ticker[4:]
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    no_of_days_before = duration
    starting_date = today-timedelta(days=no_of_days_before)
    starting_date = starting_date.timestamp()

    if stockname == "Nifty 50":
        inst = "26000"
    elif stockname == "Nifty Bank":
        inst = "26009"
    elif stockname == "Nifty Fin Service":
        inst = "26037"
    elif stockname == "NIFTY MID SELECT":
        inst = "26074"
    else:
        inst = str(token[token['TradingSymbol'] == stockname]['Token'].values[0])
        print(inst)
       # inst = token[token.TradingSymbol==stockname].Token.values[0]
       # print(inst)
       # inst = str(inst)
        #for j in range(0,len(token)):
        #    if(token['TradingSymbol'][j] == stockname):
        #        inst = str(token['Token'][j])
        #        time.sleep(1)
        #        break
    #print(inst)

    print(starting_date)
    print(interval)
    hist_data = api.get_time_price_series(exchange=exch, token=inst, starttime=starting_date, interval=1)
    hist_data = pd.DataFrame(hist_data)
    print(hist_data)

    #hist_data = hist_data.sort_values(by='time', ascending=True)
    hist_data = hist_data.reset_index(drop=True)

    # hist_data.columns = ['status','Date','Interval open','Interval high','Interval low','Interval close','Interval vwap','Interval volume','volume','Interval io change','oi']
    # for i in range(0,hist_data['Current epoch time'].size):
    #   hist_data['Current epoch time'][i] = datetime.fromtimestamp(int(hist_data['Current epoch time'][i]))

    reversed_df = hist_data.iloc[::-1]
    reversed_df = reversed_df.reset_index(drop=True)
    new_column_names = {'into': 'open', 'inth': 'high', 'intl': 'low', 'intc': 'close', 'intv': 'volume', 'intoi': 'openinterest'}
    reversed_df.rename(columns=new_column_names, inplace=True)

    reversed_df['open'] = pd.to_numeric(reversed_df['open'])
    reversed_df['high'] = pd.to_numeric(reversed_df['high'])
    reversed_df['low'] = pd.to_numeric(reversed_df['low'])
    reversed_df['close'] = pd.to_numeric(reversed_df['close'])
    reversed_df['volume'] = pd.to_numeric(reversed_df['volume'])
    reversed_df['openinterest'] = pd.to_numeric(reversed_df['openinterest'])
    reversed_df['datetime2'] = reversed_df['time'].copy()
    reversed_df['time'] = pd.to_datetime(reversed_df['time'],format="%d-%m-%Y %H:%M:%S")
    reversed_df = reversed_df[reversed_df['time'].dt.time >= pd.to_datetime("09:15:00").time()]
    reversed_df = reversed_df.reset_index(drop=True)

    # Set 'datetime' as the index
    reversed_df.set_index('time', inplace=True)
    # Update the format of the datetime index and add 5 hours and 30 minutes for IST
    #reversed_df.index = reversed_df.index.floor('min')  # Floor to minutes
    #print(hist_data)

    #finaltimeframe = str(interval)  + "min"
    if interval < 375:
        finaltimeframe = str(interval)  + "min"
    elif interval == 375:
        finaltimeframe = "D"

    # Resample to a specific time frame, for example, 30 minutes
    resampled_df = reversed_df.resample(finaltimeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'datetime2': 'first',
        'openinterest': 'last'
    })

    # If you want to fill any missing values with a specific method, you can use fillna
    #resampled_df = resampled_df.fillna(method='ffill')  # Forward fill

    #print(resampled_df)
    resampled_df = resampled_df.dropna(subset=['open'])
    return resampled_df

def getHistorical_old(ticker,interval,duration,api):
    token = pd.read_csv(f'https://api.shoonya.com/{exchange1}_symbols.txt.zip')
    exch = ticker[:3]
    stockname = ticker[4:]
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    no_of_days_before = duration
    starting_date = today-timedelta(days=no_of_days_before)
    starting_date = starting_date.timestamp()

    if stockname == "Nifty 50":
        inst = "26000"
    elif stockname == "Nifty Bank":
        inst = "26009"
    else:
        inst = token[token.TradingSymbol==stockname].Token.values[0]
        inst = str(inst)
        #for j in range(0,len(token)):
        #    if(token['TradingSymbol'][j] == stockname):
        #        inst = str(token['Token'][j])
        #        time.sleep(1)
        #        break
    #print(inst)

    print(starting_date)
    print(interval)
    hist_data = api.get_time_price_series(exchange=exch, token=inst, starttime=starting_date, interval=interval)
    hist_data = pd.DataFrame(hist_data)
    print(hist_data)

    #hist_data = hist_data.sort_values(by='time', ascending=True)
    hist_data = hist_data.reset_index(drop=True)

    # hist_data.columns = ['status','Date','Interval open','Interval high','Interval low','Interval close','Interval vwap','Interval volume','volume','Interval io change','oi']
    # for i in range(0,hist_data['Current epoch time'].size):
    #   hist_data['Current epoch time'][i] = datetime.fromtimestamp(int(hist_data['Current epoch time'][i]))

    reversed_df = hist_data.iloc[::-1]
    reversed_df = reversed_df.reset_index(drop=True)
    new_column_names = {'into': 'open', 'inth': 'high', 'intl': 'low', 'intc': 'close', 'intv': 'volume', 'intoi': 'oi'}
    reversed_df.rename(columns=new_column_names, inplace=True)
    print(reversed_df)
    return reversed_df