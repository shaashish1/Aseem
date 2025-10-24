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


import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
from pya3 import *


######PIVOT POINTS##########################
####################__INPUT__#####################


def getNiftyExpiryDate():
    nifty_expiry = {
        datetime(2025, 1, 2).date(): "02JAN25",
        datetime(2025, 1, 9).date(): "09JAN25",
        datetime(2025, 1, 16).date(): "16JAN25",
        datetime(2025, 1, 23).date(): "23JAN25",
        datetime(2025, 1, 30).date(): "30JAN25",
        datetime(2025, 2, 6).date(): "06FEB25",
        datetime(2025, 2, 13).date(): "13FEB25",
        datetime(2025, 2, 20).date(): "20FEB25",
        datetime(2025, 2, 27).date(): "27FEB25",
        datetime(2025, 3, 6).date(): "06MAR25",
        datetime(2025, 3, 13).date(): "13MAR25",
        datetime(2025, 3, 20).date(): "20MAR25",
        datetime(2025, 3, 27).date(): "27MAR25",
        datetime(2025, 4, 3).date(): "03APR25",
        datetime(2025, 4, 10).date(): "10APR25",
        datetime(2025, 4, 17).date(): "17APR25",
        datetime(2025, 4, 24).date(): "24APR25",
        datetime(2025, 5, 1).date(): "01MAY25",
        datetime(2025, 5, 8).date(): "08MAY25",
        datetime(2025, 5, 15).date(): "15MAY25",
        datetime(2025, 5, 22).date(): "22MAY25",
        datetime(2025, 5, 29).date(): "29MAY25",
        datetime(2025, 6, 5).date(): "05JUN25",
        datetime(2025, 6, 12).date(): "12JUN25",
        datetime(2025, 6, 19).date(): "19JUN25",
        datetime(2025, 6, 26).date(): "26JUN25",
        datetime(2025, 7, 3).date(): "03JUL25",
        datetime(2025, 7, 10).date(): "10JUL25",
        datetime(2025, 7, 17).date(): "17JUL25",
        datetime(2025, 7, 24).date(): "24JUL25",
        datetime(2025, 7, 31).date(): "31JUL25",
        datetime(2025, 8, 7).date(): "07AUG25",
        datetime(2025, 8, 14).date(): "14AUG25",
        datetime(2025, 8, 21).date(): "21AUG25",
        datetime(2025, 8, 28).date(): "28AUG25",
        datetime(2025, 9, 4).date(): "04SEP25",
        datetime(2025, 9, 11).date(): "11SEP25",
        datetime(2025, 9, 18).date(): "18SEP25",
        datetime(2025, 9, 25).date(): "25SEP25",
        datetime(2025, 10, 2).date(): "02OCT25",
        datetime(2025, 10, 9).date(): "09OCT25",
        datetime(2025, 10, 16).date(): "16OCT25",
        datetime(2025, 10, 23).date(): "23OCT25",
        datetime(2025, 10, 30).date(): "30OCT25",
        datetime(2025, 11, 6).date(): "06NOV25",
        datetime(2025, 11, 13).date(): "13NOV25",
        datetime(2025, 11, 20).date(): "20NOV25",
        datetime(2025, 11, 27).date(): "27NOV25",
        datetime(2025, 12, 4).date(): "04DEC25",
        datetime(2025, 12, 11).date(): "11DEC25",
        datetime(2025, 12, 18).date(): "18DEC25",
        datetime(2025, 12, 25).date(): "25DEC25",
    }


    today = datetime.now().date()

    for date_key, value in nifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getBankNiftyExpiryDate():

    banknifty_expiry = {

        datetime(2025, 1, 30).date(): "30JAN25",
        datetime(2025, 2, 27).date(): "27FEB25",
        datetime(2025, 3, 27).date(): "27MAR25",
        datetime(2025, 4, 24).date(): "24APR25",
        datetime(2025, 5, 29).date(): "29MAY25",
        datetime(2025, 6, 26).date(): "26JUN25",
        datetime(2025, 7, 31).date(): "31JUL25",
        datetime(2025, 8, 28).date(): "28AUG25",
        datetime(2025, 9, 25).date(): "25SEP25",
        datetime(2025, 10, 30).date(): "30OCT25",
        datetime(2025, 11, 27).date(): "27NOV25",
        datetime(2025, 12, 25).date(): "25DEC25",
}

    today = datetime.now().date()

    for date_key, value in banknifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getFinNiftyExpiryDate():
    finnifty_expiry = {datetime(2025, 1, 30).date(): "30JAN25",
                       datetime(2025, 2, 27).date(): "27FEB25",
                       datetime(2025, 3, 27).date(): "27MAR25",
                       datetime(2025, 4, 24).date(): "24APR25",
                       datetime(2025, 5, 29).date(): "29MAY25",
                       datetime(2025, 6, 26).date(): "26JUN25",
                       datetime(2025, 7, 31).date(): "31JUL25",
                       datetime(2025, 8, 28).date(): "28AUG25",
                       datetime(2025, 9, 25).date(): "25SEP25",
                       datetime(2025, 10, 30).date(): "30OCT25",
                       datetime(2025, 11, 27).date(): "27NOV25",
                       datetime(2025, 12, 25).date(): "25DEC25",
    }

    today = datetime.now().date()

    for date_key, value in finnifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getIndexSpot(stock):
    if stock == "BANKNIFTY":
        name = "NSE:NIFTY BANK"
    elif stock == "NIFTY":
        name = "NSE:NIFTY 50"
    elif stock == "FINNIFTY":
        name = "NSE:NIFTY FIN SERVICE"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return "NFO:" + str(stock) + str(intExpiry)+str(ce_pe[0])+str(strike)

def getLTP(instrument):
    url = "http://localhost:4000/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data

def manualLTP(symbol,alice):
    exch = symbol[:3]
    symb = symbol[4:]
    nifty_ltp = alice.get_scrip_info(alice.get_instrument_by_symbol(exch, symb))
    a = float(nifty_ltp['LTP'])
    return a

def placeOrder(inst ,t_type,qty,order_type,price,variety, alice, papertrading=0):
    exch = inst[:3]
    symb = inst[4:]
    #paperTrading = 0 #if this is 1, then real trades will be placed
    if( t_type=="BUY"):
        t_type=TransactionType.Buy
    else:
        t_type=TransactionType.Sell

    #OrderType.Market, OrderType.Limit, OrderType.StopLossMarket, OrderType.StopLossLimit
    #ProductType.Delivery, ProductType.Intraday

    if(order_type=="MARKET"):
        order_type=OrderType.Market
        price = 0
    elif(order_type=="LIMIT"):
        order_type=OrderType.Limit

    if variety == "regular":
        is_amo = False
    else:
        is_amo = True

    try:
        if(papertrading == 1):
            order_id = alice.place_order(transaction_type = t_type,
                                         instrument = alice.get_instrument_by_symbol(exch, symb),
                                         quantity = qty,
                                         order_type = order_type,
                                         product_type = ProductType.Intraday,
                                         price = float(price),
                                         trigger_price = float(price),
                                         stop_loss = None,
                                         square_off = None,
                                         trailing_sl = None,
                                         is_amo = is_amo,
                                         order_tag='order1')
            print(order_id)
            return order_id

        else:
            order_id=0
            return order_id

    except Exception as e:
        print(" => ", symb , "Failed : {} ".format(e))

def getHistorical(ticker,interval,duration, alice, index):
    exch = ticker[:3]
    stockname = ticker[4:]
    instrument = alice.get_instrument_by_symbol(exch, stockname)

    to_datetime = datetime.now()
    from_datetime = datetime.now() - timedelta(days=duration)     # From last & days

    ## ["1", "D"]
    if index == "INDEX":
        indices = True
    else:
        indices = False

    hist_data = alice.get_historical(instrument, from_datetime, to_datetime, 1, indices)
    hist_data = pd.DataFrame(hist_data)
    print(hist_data)

    # Convert string columns to float
    hist_data['open'] = pd.to_numeric(hist_data['open'])
    hist_data['high'] = pd.to_numeric(hist_data['high'])
    hist_data['low'] = pd.to_numeric(hist_data['low'])
    hist_data['close'] = pd.to_numeric(hist_data['close'])
    hist_data['volume'] = pd.to_numeric(hist_data['volume'])
    hist_data['datetime2'] = hist_data['datetime'].copy()
    hist_data['datetime'] = pd.to_datetime(hist_data['datetime'])
    # Set 'datetime' as the index
    hist_data.set_index('datetime', inplace=True)
    # Update the format of the datetime index and add 5 hours and 30 minutes for IST
    hist_data.index = hist_data.index.floor('min')  # Floor to minutes
    #print(hist_data)

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

    #print(resampled_df)
    resampled_df = resampled_df.dropna(subset=['open'])
    return resampled_df


