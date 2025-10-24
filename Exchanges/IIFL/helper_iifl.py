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

# from NorenApi import NorenApi
import datetime
import time
import requests
from datetime import timedelta
# from pytz import timezone
import pandas as pd
import ast
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
with open('symbol_mapping.txt', 'r') as f:
    symbol_to_id = ast.literal_eval(f.read())[0]

with open('user_id.txt','r') as f:
    user_id = f.read()
######PIVOT POINTS##########################
####################__INPUT__#####################

exchange1 = "NSE"

def getNiftyExpiryDate():
    nifty_expiry = {
        datetime.datetime(2025, 1, 2).date(): '25102',
        datetime.datetime(2025, 1, 9).date(): '25109',
        datetime.datetime(2025, 1, 16).date(): '25116',
        datetime.datetime(2025, 1, 23).date(): '25123',
        datetime.datetime(2025, 1, 30).date(): '25130',
        datetime.datetime(2025, 2, 6).date(): '25206',
        datetime.datetime(2025, 2, 13).date(): '25213',
        datetime.datetime(2025, 2, 20).date(): '25220',
        datetime.datetime(2025, 2, 27).date(): '25227',
        datetime.datetime(2025, 3, 6).date(): '25306',
        datetime.datetime(2025, 3, 13).date(): '25313',
        datetime.datetime(2025, 3, 20).date(): '25320',
        datetime.datetime(2025, 3, 27).date(): '25327',
        datetime.datetime(2025, 4, 3).date(): '25403',
        datetime.datetime(2025, 4, 10).date(): '25410',
        datetime.datetime(2025, 4, 17).date(): '25417',
        datetime.datetime(2025, 4, 24).date(): '25424',
        datetime.datetime(2025, 5, 1).date(): '25501',
        datetime.datetime(2025, 5, 8).date(): '25508',
        datetime.datetime(2025, 5, 15).date(): '25515',
        datetime.datetime(2025, 5, 22).date(): '25522',
        datetime.datetime(2025, 5, 29).date(): '25529',
        datetime.datetime(2025, 6, 5).date(): '25605',
        datetime.datetime(2025, 6, 12).date(): '25612',
        datetime.datetime(2025, 6, 19).date(): '25619',
        datetime.datetime(2025, 6, 26).date(): '25626',
        datetime.datetime(2025, 7, 3).date(): '25703',
        datetime.datetime(2025, 7, 10).date(): '25710',
        datetime.datetime(2025, 7, 17).date(): '25717',
        datetime.datetime(2025, 7, 24).date(): '25724',
        datetime.datetime(2025, 7, 31).date(): '25731',
        datetime.datetime(2025, 8, 7).date(): '25807',
        datetime.datetime(2025, 8, 14).date(): '25814',
        datetime.datetime(2025, 8, 21).date(): '25821',
        datetime.datetime(2025, 8, 28).date(): '25828',
        datetime.datetime(2025, 9, 4).date(): '25904',
        datetime.datetime(2025, 9, 11).date(): '25911',
        datetime.datetime(2025, 9, 18).date(): '25918',
        datetime.datetime(2025, 9, 25).date(): '25925',
        datetime.datetime(2025, 10, 2).date(): '25O02',
        datetime.datetime(2025, 10, 9).date(): '25O09',
        datetime.datetime(2025, 10, 16).date(): '25O16',
        datetime.datetime(2025, 10, 23).date(): '25O23',
        datetime.datetime(2025, 10, 30).date(): '25O30',
        datetime.datetime(2025, 11, 6).date(): '25N06',
        datetime.datetime(2025, 11, 13).date(): '25N13',
        datetime.datetime(2025, 11, 20).date(): '25N20',
        datetime.datetime(2025, 11, 27).date(): '25N27',
        datetime.datetime(2025, 12, 4).date(): '25D04',
        datetime.datetime(2025, 12, 11).date(): '25D11',
        datetime.datetime(2025, 12, 18).date(): '25D18',
        datetime.datetime(2025, 12, 25).date(): '25D25',
    }


    today = datetime.datetime.now().date()

    for date_key, value in nifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getBankNiftyExpiryDate():
    banknifty_expiry = {
        datetime.datetime(2025, 1, 30).date(): "25130",
        datetime.datetime(2025, 2, 27).date(): "25227",
        datetime.datetime(2025, 3, 27).date(): "25327",
        datetime.datetime(2025, 4, 24).date(): "25424",
        datetime.datetime(2025, 5, 29).date(): "25529",
        datetime.datetime(2025, 6, 26).date(): "25626",
        datetime.datetime(2025, 7, 31).date(): "25731",
        datetime.datetime(2025, 8, 28).date(): "25828",
        datetime.datetime(2025, 9, 25).date(): "25925",
        datetime.datetime(2025, 10, 30).date(): "25O30",
        datetime.datetime(2025, 11, 27).date(): "25N27",
        datetime.datetime(2025, 12, 25).date(): "25D25",
    
    }

    today = datetime.datetime.now().date()

    for date_key, value in banknifty_expiry.items():
        if today <= date_key:
            print(value)
            return value


def getFinNiftyExpiryDate():
    finnifty_expiry = {
        datetime.datetime(2025, 1, 30).date(): "25130",
        datetime.datetime(2025, 2, 27).date(): "25227",
        datetime.datetime(2025, 3, 27).date(): "25327",
        datetime.datetime(2025, 4, 24).date(): "25424",
        datetime.datetime(2025, 5, 29).date(): "25529",
        datetime.datetime(2025, 6, 26).date(): "25626",
        datetime.datetime(2025, 7, 31).date(): "25731",
        datetime.datetime(2025, 8, 28).date(): "25828",
        datetime.datetime(2025, 9, 25).date(): "25925",
        datetime.datetime(2025, 10, 30).date(): "25O30",
        datetime.datetime(2025, 11, 27).date(): "25N27",
        datetime.datetime(2025, 12, 25).date(): "25D25",
    }

    today = datetime.datetime.now().date()

    for date_key, value in finnifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getIndexSpot(stock):
    if stock == "BANKNIFTY":
        name = "Nifty Bank"
    elif stock == "NIFTY":
        name = "Nifty 50"
    elif stock == "FINNIFTY":
        name = "Nifty Fin Service"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return str(stock) + str(intExpiry)+str(strike)+str(ce_pe)

def getLTP(instrument):
    url = "http://localhost:4000/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data

def manualLTP(symbol,api):
    # exch = symbol[:3]
    # stockname = symbol[4:]
    symbol_array=[]
    print(symbol_to_id[symbol])
    try:
        sid = symbol_to_id[symbol].split('|')
        symbol_array.append({'exchangeSegment':sid[0],'exchangeInstrumentID':sid[1]})
    except:
        print("Symbol Not found. (Manual LTP)",symbol)
    # print(symbol_array)
    temp = api.get_quote(symbol_array,1512,'JSON')
    if temp['type']!='success':
        print("Manual LTP Error")
    # print(temp['result']['listQuotes'])
    ltp = ast.literal_eval(temp['result']['listQuotes'][0])['LastTradedPrice']
    print(ltp)
    return ltp

def placeOrder(inst ,t_type,qty,order_type,price,variety, api,papertrading=0,trigger_price=0):
    # exch = inst[:3]
    # symb = inst[4:]
    try:
        sid = symbol_to_id[inst].split('|')
    except:
        print("Order not placed. Instrument not found")
        return 0
    segments_dict = {'1':"NSECM",'2' :"NSEFO", '3':"NSECD", '11':"BSECM", '12':"BSEFO", '51':"MCXFO"}
    #paperTrading = 0 #if this is 1, then real trades will be placed
    if( t_type=="BUY"):
        t_type=api.TRANSACTION_TYPE_BUY
    else:
        t_type=api.TRANSACTION_TYPE_SELL

    if(order_type=="MARKET"):
        order_type=api.ORDER_TYPE_MARKET
        price = 0
    elif(order_type=="LIMIT"):
        order_type=api.ORDER_TYPE_LIMIT
    elif(order_type=='SL'):
        order_type=api.ORDER_TYPE_STOPMARKET

    try:
        if(papertrading == 1):
            print(t_type)
            print(inst)
            # print(symb)
            print(qty)
            print(order_type)
            print(price)

            order_id = api.place_order(
                exchangeSegment=segments_dict[sid[0]],
                exchangeInstrumentID=int(sid[1]),
                productType=api.PRODUCT_MIS,
                orderType=order_type,
                orderSide=t_type,
                timeInForce=api.VALIDITY_DAY,
                disclosedQuantity=0,
                orderQuantity=qty,
                limitPrice=price,
                stopPrice=trigger_price,
                orderUniqueIdentifier="454845",
                clientID=user_id)
            if order_id['type'] != 'error':
                order_id = order_id['result']['AppOrderID']
            print(" => ", inst , order_id )
            return order_id

        else:
            order_id=0
            return order_id

    except Exception as e:
        print(" => ", inst , "Failed : {} ".format(e))

def getHistorical(ticker,interval,duration,api):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    #token = pd.read_csv(f'https://api.shoonya.com/{exchange1}_symbols.txt.zip')
    segments_dict = {'1':"NSECM",'2' :"NSEFO", '3':"NSECD", '11':"BSECM", '12':"BSEFO", '51':"MCXFO"}
    try:
        sid = symbol_to_id[ticker].split('|')
    except:
        print("Historical data not found. Instrument not found")
        return 0
    # exch = ticker[:3]
    # token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')
    stockname = ticker
    # dt = datetime.datetime.now()
    # endTime = months[dt.month-1] + " " + str(dt.day) + " " + str(dt.year) + str(dt.hour)

    endtime = time.strftime("%b %d %Y %H%M%S",time.localtime())
    # startTime =
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    no_of_days_before = duration
    starting_date = today-timedelta(days=no_of_days_before)
    starting_date = datetime.datetime.strftime(starting_date,"%b %d %Y %H%M%S")
    print(endtime)
    print(starting_date)
    # Compression value
    # "In1Second:1"
    # "In1Minute: 60"
    # "In2Minute : 120"
    # "In3Minute : 180"
    # "In5Minute : 300"
    # "In10Minute : 600"
    # "In15Minute : 900"
    # "In30Minute : 1800"
    # "In60Minute : 3600"
    hist_data = api.get_ohlc(
        exchangeSegment=segments_dict[sid[0]],
        exchangeInstrumentID=int(sid[1]),
        startTime=starting_date,
        endTime=endtime,
        compressionValue=60)
    # print(starting_date)
    print(interval)

    # hist_data = api.get_time_price_series(exchange=exch, token=inst, starttime=starting_date, interval=1)
    # hist_data = pd.DataFrame(hist_data)
    print(hist_data)
    if hist_data['type'] != 'success':
        print("Error Getting historical data.")
        return 0
    hist_data = hist_data['result']['dataReponse'].split(',')
    hist_list = []
    for i in range(len(hist_data)):
        single_row = hist_data[i].split('|')
        hist_list.append(single_row)
    hist_data = pd.DataFrame(hist_list,columns=['timeframe','open','high','low','close','volume','oi','blank'])
    hist_data.drop(['blank'],axis=1)
    hist_data['timeframe'] = [datetime.datetime.utcfromtimestamp(int(x)) for x in hist_data['timeframe']]
    hist_data['timeframe'] = pd.to_datetime(hist_data['timeframe'])
    # hist_data =
    print(hist_data)

    #hist_data = hist_data.sort_values(by='time', ascending=True)
    hist_data = hist_data.reset_index(drop=True)

    # hist_data.columns = ['status','Date','Interval open','Interval high','Interval low','Interval close','Interval vwap','Interval volume','volume','Interval io change','oi']
    # for i in range(0,hist_data['Current epoch time'].size):
    #   hist_data['Current epoch time'][i] = datetime.fromtimestamp(int(hist_data['Current epoch time'][i]))
    reversed_df = hist_data
    # reversed_df = hist_data.iloc[::-1]

    reversed_df = reversed_df.reset_index(drop=True)
    # new_column_names = {'into': 'open', 'inth': 'high', 'intl': 'low', 'intc': 'close', 'intv': 'volume', 'intoi': 'openinterest'}
    # reversed_df.rename(columns=new_column_names, inplace=True)

    reversed_df['open'] = pd.to_numeric(reversed_df['open'])
    reversed_df['high'] = pd.to_numeric(reversed_df['high'])
    reversed_df['low'] = pd.to_numeric(reversed_df['low'])
    reversed_df['close'] = pd.to_numeric(reversed_df['close'])
    reversed_df['volume'] = pd.to_numeric(reversed_df['volume'])
    reversed_df['openinterest'] = pd.to_numeric(reversed_df['oi'])
    reversed_df['datetime2'] = reversed_df['timeframe'].copy()
    reversed_df['time'] = pd.to_datetime(reversed_df['timeframe'])
    reversed_df = reversed_df[reversed_df['time'].dt.time >= pd.to_datetime("09:15:00").time()]
    reversed_df = reversed_df.reset_index(drop=True)

    # Set 'datetime' as the index
    reversed_df.set_index('time', inplace=True)
    # Update the format of the datetime index and add 5 hours and 30 minutes for IST
    #reversed_df.index = reversed_df.index.floor('min')  # Floor to minutes
    #print(hist_data)

    finaltimeframe = str(interval)  + "min"

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
