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

from __future__ import print_function
import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
import gzip
from io import BytesIO
import upstox_client
from upstox_client.rest import ApiException
import ast

######PIVOT POINTS##########################
####################__INPUT__#####################
access_token = open("upstox_access_token.txt", 'r').read()
gzipped_file_url  = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
# Download the gzipped file from the URL
response = requests.get(gzipped_file_url)
gzipped_content = BytesIO(response.content)

with gzip.open(gzipped_content, 'rb') as f:
    df2 = pd.read_csv(f)
    df2.to_csv('111.csv')

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
        name = "Nifty Bank"
    elif stock == "NIFTY":
        name = "Nifty 50"
    elif stock == "FINNIFTY":
        name = "Nifty Fin Service"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return str(stock) + str(intExpiry)+str(strike)+str(ce_pe)

def getLTP(instrument):
    print(instrument)
    token = df2[df2['tradingsymbol'] == instrument]['instrument_key']
    token2 = df2[df2['name'] == instrument]['instrument_key']

    if not token.empty:
        instrument_key = token.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]

    url = "http://localhost:4000/ltp?instrument=" + instrument_key

    try:
        resp = requests.get(url)
        resp2 = (resp.json())
        resp3 = resp2['ltp']
    except Exception as e:
        print(e)
    data = resp3
    return data

def manualLTP(symbol):
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token
    # create an instance of the API class
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

    token = df2[df2['tradingsymbol'] == symbol]['instrument_key']
    token2 = df2[df2['name'] == symbol]['instrument_key']
    ex = df2[df2['tradingsymbol'] == symbol]['exchange']
    ex2 = df2[df2['name'] == symbol]['exchange']

    if not token.empty:
        instrument_key = token.values[0]
        ex = ex.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]
        ex = ex2.values[0]

    try:
        # Market quotes and instruments - LTP quotes.
        api_response = api_instance.ltp(instrument_key, api_version)
        #print(api_response)
        api_response_str = str(api_response)
        #print(api_response_str)
        my_dict = ast.literal_eval(api_response_str)
        print(my_dict)
        symb = ex + ":" + symbol
        last_price = my_dict['data'][symb]['last_price']
        return(float(last_price))
    except ApiException as e:
        print("Exception when calling MarketQuoteApi->ltp: %s\n" % e)

def placeOrder(inst ,t_type,qty,order_type,price,variety, papertrading=0):
    # Configure OAuth2 access token for authorization: OAUTH2
    #https://upstox.com/developer/api-documentation/#tag/Order/operation/placeOrder
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token

    print(df2)

    if not df2[df2['tradingsymbol'] == inst].empty:
        instrument_key = df2[df2['tradingsymbol'] == inst]['instrument_key'].values[0]
    # If no data for 'tradingsymbol', check for 'name'
    else:
        print(inst)
        instrument_key = df2[df2['name'] == inst]['instrument_key'].values[0]
    #instrument_key = df2[df2['tradingsymbol'] == inst]['instrument_key'].values[0]

    #papertrading = 1 #if this is 1, then real trades will be placed
    dt = datetime.datetime.now()

    if order_type == "MARKET":
        price = 0

    try:
        if (papertrading == 1):
            order_details = {
                "quantity": qty,
                "product": "I",
                "validity": "DAY",
                "price": price,
                "tag": "string",
                "instrument_token": instrument_key,
                "order_type": order_type,
                "transaction_type": t_type,
                "disclosed_quantity": 0,
                "trigger_price": price,
                "is_amo": False
            }

            api_instance = upstox_client.OrderApi(
                upstox_client.ApiClient(configuration))
            api_response = api_instance.place_order(order_details, api_version)
            print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , api_response.data.order_id)
            return api_response.data.order_id
        else:
            return 0

    except Exception as e:
        print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , "Failed : {} ".format(e))

def getHistorical(ticker,interval,duration):
    # Configure OAuth2 access token for authorization: OAUTH2
    #https://upstox.com/developer/api-documentation/#tag/Order/operation/placeOrder
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token

    token = df2[df2['tradingsymbol'] == ticker]['instrument_key']
    token2 = df2[df2['name'] == ticker]['instrument_key']

    if not token.empty:
        instrument_key = token.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]

    if interval == 1:
        interval_str = "1minute"
    elif interval == 30:
        interval_str = "30minute"

    interval_str = "1minute"
    to_date = datetime.datetime.now().strftime("%Y-%m-%d")
    duration1 = timedelta(days=int(duration))
    from_date = datetime.datetime.now() - duration1
    from_date_str = from_date.strftime("%Y-%m-%d")
    print(from_date_str)

    #getting historical data
    try:
        # Historical candle data
        api_instance = upstox_client.HistoryApi()
        api_response = api_instance.get_historical_candle_data1(instrument_key, interval_str, to_date, from_date_str, api_version)
        #print(api_response)
        candles_data = api_response.data.candles

        # Define column names
        column_names = ["date", "open", "high", "low", "close", "volume", "openinterest"]

        # Create a DataFrame with the specified column names
        df = pd.DataFrame(candles_data, columns=column_names)
        df['datetime2'] = df['date'].copy()
        df.set_index("date",inplace=True)
        #print(df)

    except ApiException as e:
        print("Exception when calling HistoryApi->get_historical_candle_data1: %s\n" % e)

    #getting intraday data
    try:
        # Intra day candle data
        api_response = api_instance.get_intra_day_candle_data(instrument_key, interval_str, api_version)
        #pprint(api_response)
        candles_data = api_response.data.candles

        # Create a DataFrame with the specified column names
        df3 = pd.DataFrame(candles_data, columns=column_names)
        df3['datetime2'] = df3['date'].copy()
        df3.set_index("date",inplace=True)
        #print(df3)
    except ApiException as e:
        print("Exception when calling HistoryApi->get_intra_day_candle_data: %s\n" % e)

    merged_df = pd.concat([df3, df], ignore_index=False)
    # Convert the index to datetime explicitly
    merged_df.index = pd.to_datetime(merged_df.index)
    sorted_df = merged_df.sort_index(ascending=True)
    #finaltimeframe = str(interval)  + "min"
    if interval < 375:
        finaltimeframe = str(interval)  + "min"
    elif interval == 375:
        finaltimeframe = "D"

    # Resample to a specific time frame, for example, 30 minutes
    resampled_df = sorted_df.resample(finaltimeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'datetime2': 'first'
    })

    # If you want to fill any missing values with a specific method, you can use fillna
    #resampled_df = resampled_df.fillna(method='ffill')  # Forward fill

    #print(resampled_df)
    resampled_df = resampled_df.dropna(subset=['open'])

    return(resampled_df)

def getHistorical_old(ticker,interval,duration):
    # Configure OAuth2 access token for authorization: OAUTH2
    #https://upstox.com/developer/api-documentation/#tag/Order/operation/placeOrder
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token

    token = df2[df2['tradingsymbol'] == ticker]['instrument_key']
    token2 = df2[df2['name'] == ticker]['instrument_key']

    if not token.empty:
        instrument_key = token.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]

    if interval == 1:
        interval_str = "1minute"
    elif interval == 30:
        interval_str = "30minute"

    to_date = datetime.datetime.now().strftime("%Y-%m-%d")
    duration1 = timedelta(days=int(duration))
    from_date = datetime.datetime.now() - duration1
    from_date_str = from_date.strftime("%Y-%m-%d")
    print(from_date_str)

    #getting historical data
    try:
        # Historical candle data
        api_instance = upstox_client.HistoryApi()
        api_response = api_instance.get_historical_candle_data1(instrument_key, interval_str, to_date, from_date_str, api_version)
        #print(api_response)
        candles_data = api_response.data.candles

        # Define column names
        column_names = ["date", "open", "high", "low", "close", "volume", "oi"]

        # Create a DataFrame with the specified column names
        df = pd.DataFrame(candles_data, columns=column_names)
        df.set_index("date",inplace=True)
        #print(df)

    except ApiException as e:
        print("Exception when calling HistoryApi->get_historical_candle_data1: %s\n" % e)

    #getting intraday data
    try:
        # Intra day candle data
        api_response = api_instance.get_intra_day_candle_data(instrument_key, interval_str, api_version)
        #pprint(api_response)
        candles_data = api_response.data.candles

        # Create a DataFrame with the specified column names
        df3 = pd.DataFrame(candles_data, columns=column_names)
        df3.set_index("date",inplace=True)
        #print(df3)
    except ApiException as e:
        print("Exception when calling HistoryApi->get_intra_day_candle_data: %s\n" % e)

    merged_df = pd.concat([df3, df], ignore_index=False)
    sorted_df = merged_df.sort_index(ascending=True)
    #print(merged_df)
    return(sorted_df)