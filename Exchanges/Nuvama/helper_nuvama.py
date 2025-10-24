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

from APIConnect.APIConnect import APIConnect
from constants.exchange import ExchangeEnum
from constants.order_type import OrderTypeEnum
from constants.product_code import ProductCodeENum
from constants.duration import DurationEnum
from constants.action import ActionEnum
from constants.asset_type import AssetTypeEnum
from constants.chart_exchange import ChartExchangeEnum
from constants.intraday_interval import IntradayIntervalEnum
#import nuvama_login
import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
import json

######PIVOT POINTS##########################
####################__INPUT__#####################

#api_connect = nuvama_login.api_connect

def getNiftyExpiryDate():
    nifty_expiry = {
        datetime.datetime(2025, 1, 2).date(): '25102',
        datetime.datetime(2025, 1, 9).date(): '25109',
        datetime.datetime(2025, 1, 16).date(): '25116',
        datetime.datetime(2025, 1, 23).date(): '25123',
        datetime.datetime(2025, 1, 30).date(): '25JAN',
        datetime.datetime(2025, 2, 6).date(): '25206',
        datetime.datetime(2025, 2, 13).date(): '25213',
        datetime.datetime(2025, 2, 20).date(): '25220',
        datetime.datetime(2025, 2, 27).date(): '25FEB',
        datetime.datetime(2025, 3, 6).date(): '25306',
        datetime.datetime(2025, 3, 13).date(): '25313',
        datetime.datetime(2025, 3, 20).date(): '25320',
        datetime.datetime(2025, 3, 27).date(): '25MAR',
        datetime.datetime(2025, 4, 3).date(): '25403',
        datetime.datetime(2025, 4, 10).date(): '25410',
        datetime.datetime(2025, 4, 17).date(): '25417',
        datetime.datetime(2025, 4, 24).date(): '25APR',
        datetime.datetime(2025, 5, 1).date(): '25501',
        datetime.datetime(2025, 5, 8).date(): '25508',
        datetime.datetime(2025, 5, 15).date(): '25515',
        datetime.datetime(2025, 5, 22).date(): '25522',
        datetime.datetime(2025, 5, 29).date(): '25MAY',
        datetime.datetime(2025, 6, 5).date(): '25605',
        datetime.datetime(2025, 6, 12).date(): '25612',
        datetime.datetime(2025, 6, 19).date(): '25619',
        datetime.datetime(2025, 6, 26).date(): '25JUN',
        datetime.datetime(2025, 7, 3).date(): '25703',
        datetime.datetime(2025, 7, 10).date(): '25710',
        datetime.datetime(2025, 7, 17).date(): '25717',
        datetime.datetime(2025, 7, 24).date(): '25724',
        datetime.datetime(2025, 7, 31).date(): '25JUL',
        datetime.datetime(2025, 8, 7).date(): '25807',
        datetime.datetime(2025, 8, 14).date(): '25814',
        datetime.datetime(2025, 8, 21).date(): '25821',
        datetime.datetime(2025, 8, 28).date(): '25AUG',
        datetime.datetime(2025, 9, 4).date(): '25904',
        datetime.datetime(2025, 9, 11).date(): '25911',
        datetime.datetime(2025, 9, 18).date(): '25918',
        datetime.datetime(2025, 9, 25).date(): '25SEP',
        datetime.datetime(2025, 10, 2).date(): '25O02',
        datetime.datetime(2025, 10, 9).date(): '25O09',
        datetime.datetime(2025, 10, 16).date(): '25O16',
        datetime.datetime(2025, 10, 23).date(): '25O23',
        datetime.datetime(2025, 10, 30).date(): '25OCT',
        datetime.datetime(2025, 11, 6).date(): '25N06',
        datetime.datetime(2025, 11, 13).date(): '25N13',
        datetime.datetime(2025, 11, 20).date(): '25N20',
        datetime.datetime(2025, 11, 27).date(): '25NOV',
        datetime.datetime(2025, 12, 4).date(): '25D04',
        datetime.datetime(2025, 12, 11).date(): '25D11',
        datetime.datetime(2025, 12, 18).date(): '25D18',
        datetime.datetime(2025, 12, 25).date(): '25DEC',
    }


    today = datetime.datetime.now().date()

    for date_key, value in nifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getBankNiftyExpiryDate():
    banknifty_expiry = {
        datetime.datetime(2025, 1, 30).date(): "25JAN",
        datetime.datetime(2025, 2, 27).date(): "25FEB",
        datetime.datetime(2025, 3, 27).date(): "25MAR",
        datetime.datetime(2025, 4, 24).date(): "25APR",
        datetime.datetime(2025, 5, 29).date(): "25MAY",
        datetime.datetime(2025, 6, 26).date(): "25JUN",
        datetime.datetime(2025, 7, 31).date(): "25JUL",
        datetime.datetime(2025, 8, 28).date(): "25AUG",
        datetime.datetime(2025, 9, 25).date(): "25SEP",
        datetime.datetime(2025, 10, 30).date(): "25OCT",
        datetime.datetime(2025, 11, 27).date(): "25NOV",
        datetime.datetime(2025, 12, 25).date(): "25DEC",
    }

    today = datetime.datetime.now().date()

    for date_key, value in banknifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getFinNiftyExpiryDate():
    finnifty_expiry = {
        datetime.datetime(2025, 1, 30).date(): "25JAN",
        datetime.datetime(2025, 2, 27).date(): "25FEB",
        datetime.datetime(2025, 3, 27).date(): "25MAR",
        datetime.datetime(2025, 4, 24).date(): "25APR",
        datetime.datetime(2025, 5, 29).date(): "25MAY",
        datetime.datetime(2025, 6, 26).date(): "25JUN",
        datetime.datetime(2025, 7, 31).date(): "25JUL",
        datetime.datetime(2025, 8, 28).date(): "25AUG",
        datetime.datetime(2025, 9, 25).date(): "25SEP",
        datetime.datetime(2025, 10, 30).date(): "25OCT",
        datetime.datetime(2025, 11, 27).date(): "25NOV",
        datetime.datetime(2025, 12, 25).date(): "25DEC",
    }

    today = datetime.datetime.now().date()

    for date_key, value in finnifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getExpiryFormat(year, month, day, monthly):
    if monthly == 0:
        day1 = day
        if month == "JAN":
            month1 = 1
        elif month == "FEB":
            month1 = 2
        elif month == "MAR":
            month1 = 3
        elif month == "APR":
            month1 = 4
        elif month == "MAY":
            month1 = 5
        elif month == "JUN":
            month1 = 6
        elif month == "JUL":
            month1 = 7
        elif month == "AUG":
            month1 = 8
        elif month == "SEP":
            month1 = 9
        elif month == "OCT":
            month1 = "O"
        elif month == "NOV":
            month1 = "N"
        elif month == "DEC":
            month1 = "D"
    elif monthly == 1:
        day1 = ""
        month1 = month

    return str(year)+str(month1)+str(day1)

def getIndexSpot(stock):
    if stock == "BANKNIFTY":
        name = "NSE:Nifty Bank"
    elif stock == "NIFTY":
        name = "NSE:Nifty 50"
    elif stock == "FINNIFTY":
        name = "NSE:Nifty Fin Service"

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
    getLTP(symbol)

columns_to_select = ['exchangetoken', 'tradingsymbol', 'symbolname', 'description','assettype','exchange']
token = pd.read_csv('instruments\instruments.csv',usecols=columns_to_select, index_col=False)
print(token)

def get_tradingSymbol_exchangeToken(symbolname):
    exch = symbolname[:3]
    name = symbolname[4:]

    #print(token)

    if name == "Nifty 50":
        tradingsymbol = "Nifty 50"
        exchangetoken = "-29"
    elif name == "Nifty Bank":
        tradingsymbol = "Nifty Bank"
        exchangetoken = "-21"
    elif name == "Nifty Fin Service":
        tradingsymbol = "Nifty Fin Service"
        exchangetoken = "-40"
    elif name == "NSE Midcap 100":
        tradingsymbol = "NSE Midcap 100"
        exchangetoken = "-22"
    elif exch == "NSE":
        for j in range(0,len(token)):
            if(token['symbolname'][j] == name) and (token['exchange'][j] == exch):
                tradingsymbol = str(token['tradingsymbol'][j])
                exchangetoken = str(token['exchangetoken'][j])
                break
    elif exch == "NFO" or exch == "MCX":
        for j in range(0,len(token)):
            if(token['tradingsymbol'][j] == name) and (token['exchange'][j] == exch):
                tradingsymbol = str(token['tradingsymbol'][j])
                exchangetoken = str(token['exchangetoken'][j])
                break

    return (tradingsymbol, exchangetoken)

def placeOrder(inst ,t_type,qty,order_type,price,variety, api_connect, papertrading=0):
    exch = inst[:3]
    symb = inst[4:]
    tradingsymbol, exchangetoken = get_tradingSymbol_exchangeToken(inst)
    print(tradingsymbol)
    print(exchangetoken)
    dt = datetime.datetime.now()
    #papertrading = 0 #if this is 1, then actual trades will get placed
    print(dt.hour,":",dt.minute,":",dt.second ," => ",t_type," ",symb," ",qty," ",order_type)

    if(order_type=="MARKET"):
        order_type = OrderTypeEnum.MARKET
    elif(order_type=="LIMIT"):
        order_type = OrderTypeEnum.LIMIT

    if(t_type=="BUY"):
        action = ActionEnum.BUY
    elif(t_type=="SELL"):
        action = ActionEnum.SELL

    if(exch=="NSE"):
        exchange = ExchangeEnum.NSE
    elif(exch=="NFO"):
        exchange = ExchangeEnum.NFO

    try:
        if (papertrading == 1):
            #return tradingsymbol, exchange,action,DurationEnum.DAY,  order_type, qty, exchangetoken, price, "0", "0", ProductCodeENum.MIS

            orderid = api_connect.PlaceTrade(Trading_Symbol = tradingsymbol,
                                             Exchange = exchange,
                                             Action = action,
                                             Duration = DurationEnum.DAY,
                                             Order_Type = order_type,
                                             Quantity = qty,
                                             Streaming_Symbol = exchangetoken,
                                             Limit_Price = price,
                                             Disclosed_Quantity="0",
                                             TriggerPrice="0",
                                             ProductCode = ProductCodeENum.MIS)

            print(dt.hour,":",dt.minute,":",dt.second ," => ", symb , orderid)
            return orderid
        else:
            return 0

    except Exception as e:
        print(dt.hour,":",dt.minute,":",dt.second ," => ", symb , "Failed : {} ".format(e))

def getHistorical(ticker,interval,duration,assetType, api_connect):
    exch = ticker[:3]
    sym = ticker[4:]

    if exch == "NSE":
        chart_exch = ChartExchangeEnum.NSE
    elif exch == "NFO":
        chart_exch = ChartExchangeEnum.NFO

    if assetType == "INDEX":
        asset_type = AssetTypeEnum.INDEX
    elif assetType == "EQUITY":
        asset_type = AssetTypeEnum.EQUITY
    elif assetType == "FUTUREINDEX":
        asset_type = AssetTypeEnum.FUTIDX
    elif assetType == "FUTURESTOCK":
        asset_type = AssetTypeEnum.FUTSTK
    elif assetType == "OPTIONINDEX":
        asset_type = AssetTypeEnum.OPTIDX
    elif assetType == "OPTIONSTOCK":
        asset_type = AssetTypeEnum.OPTSTK

    if interval == 1:
        internal_nuvama = IntradayIntervalEnum.M1
    elif interval == 3:
        internal_nuvama = IntradayIntervalEnum.M3
    elif interval == 5:
        internal_nuvama = IntradayIntervalEnum.M5
    elif interval == 15:
        internal_nuvama = IntradayIntervalEnum.M15
    elif interval == 30:
        internal_nuvama = IntradayIntervalEnum.M30
    elif interval == 60:
        internal_nuvama = IntradayIntervalEnum.H1
    internal_nuvama = IntradayIntervalEnum.M1

    symm, symbolToken = get_tradingSymbol_exchangeToken(ticker)

    #return chart_exch, asset_type, symbolToken, internal_nuvama

    response = api_connect.getIntradayChart(chart_exch,
                                            asset_type,
                                            symbolToken,
                                            internal_nuvama,
                                            TillDate = None)
    #print(response)
    data_dict = json.loads(response)
    #print(data_dict['data'])
    df = pd.DataFrame(data_dict['data'], columns=["Timestamp", "open", "high", "low", "close", "volume"])
    print(df)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Timestamp'] = df['Timestamp'] - pd.Timedelta(minutes=1)
    filtered_df = df[(df['Timestamp'].dt.time >= pd.to_datetime("09:15:00").time()) & (df['Timestamp'].dt.time <= pd.to_datetime("15:29:00").time())]
    filtered_df = filtered_df.reset_index(drop=True)

    filtered_df['datetime2'] = filtered_df['Timestamp'].copy()
    # Set 'datetime' as the index
    filtered_df.set_index('Timestamp', inplace=True)
    # Update the format of the datetime index and add 5 hours and 30 minutes for IST
    #df.index = df.index.floor('min')  # Floor to minutes
    #print(hist_data)
    #finaltimeframe = str(interval)  + "min"
    if interval < 375:
        finaltimeframe = str(interval)  + "min"
    elif interval == 375:
        finaltimeframe = "D"

    # Resample to a specific time frame, for example, 30 minutes
    resampled_df = filtered_df.resample(finaltimeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'datetime2': 'first'
    })
    resampled_df = resampled_df.dropna(subset=['open'])

    # If you want to fill any missing values with a specific method, you can use fillna
    #resampled_df = resampled_df.fillna(method='ffill')  # Forward fill

    #print(resampled_df)

    return resampled_df

def getHistorical_old(ticker,interval,duration,assetType, api_connect):
    exch = ticker[:3]
    sym = ticker[4:]

    if exch == "NSE":
        chart_exch = ChartExchangeEnum.NSE
    elif exch == "NFO":
        chart_exch = ChartExchangeEnum.NFO

    if assetType == "INDEX":
        asset_type = AssetTypeEnum.INDEX
    elif assetType == "EQUITY":
        asset_type = AssetTypeEnum.EQUITY
    elif assetType == "FUTUREINDEX":
        asset_type = AssetTypeEnum.FUTIDX
    elif assetType == "FUTURESTOCK":
        asset_type = AssetTypeEnum.FUTSTK
    elif assetType == "OPTIONINDEX":
        asset_type = AssetTypeEnum.OPTIDX
    elif assetType == "OPTIONSTOCK":
        asset_type = AssetTypeEnum.OPTSTK

    if interval == 1:
        internal_nuvama = IntradayIntervalEnum.M1
    elif interval == 3:
        internal_nuvama = IntradayIntervalEnum.M3
    elif interval == 5:
        internal_nuvama = IntradayIntervalEnum.M5
    elif interval == 15:
        internal_nuvama = IntradayIntervalEnum.M15
    elif interval == 30:
        internal_nuvama = IntradayIntervalEnum.M30
    elif interval == 60:
        internal_nuvama = IntradayIntervalEnum.H1

    symm, symbolToken = get_tradingSymbol_exchangeToken(ticker)

    #return chart_exch, asset_type, symbolToken, internal_nuvama

    response = api_connect.getIntradayChart(chart_exch,
                                            asset_type,
                                            symbolToken,
                                            internal_nuvama,
                                            TillDate = None)
    #print(response)
    data_dict = json.loads(response)
    #print(data_dict['data'])
    df = pd.DataFrame(data_dict['data'], columns=["Timestamp", "open", "high", "low", "close", "volume"])
    #print(df)
    return df