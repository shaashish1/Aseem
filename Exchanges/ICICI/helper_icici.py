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
#https://github.com/Idirect-Tech/Breeze-Python-SDK

from breeze_connect import BreezeConnect
import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
import urllib
import re
import calendar


######PIVOT POINTS##########################
####################__INPUT__#####################
#api_key = "T64987#r17926343Q420~96^77V12T3n"
#secret_key = "62579224n30z7s*926g2h37y1948o1d3"
#session_key = "31798535"

###NO NEED TO ENTER ANYTHING HERE
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#breeze = BreezeConnect(api_key=api_key)
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(api_key))

#breeze.generate_session(api_secret=secret_key, session_token=session_key)

todays_date = datetime.datetime.today().strftime('%d/%m/%Y')
iso_date_string = datetime.datetime.strptime(todays_date, "%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
validity_date_string = datetime.datetime.strptime(f"{todays_date} 06:00:00","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'

def extract_code_strike_expiry(stock : str):
    exchange_code = stock.split(":")[0]
    stock_name = stock.split(":")[1]
    expiry = ""
    right = ""
    strike = ""

    opt_search = re.search(r"(\d{2}\w{3})(\d+|\d+\.\d+)(CE|PE)", stock_name)
    fut_search = re.search(r"(\d{2}\w{3})(FUT)", stock_name)

    if opt_search:
        stock_name = stock_name.replace(opt_search[0], "")
        expiry = opt_search[1]
        strike = opt_search[2]
        right = opt_search[3]

    elif fut_search:
        stock_name = stock_name.replace(fut_search[0], "")
        expiry = fut_search[1]

    return [
        exchange_code,
        stock_name,
        expiry,
        strike,
        right
    ]

def expiry_to_date(expiry1, stock):
    full_date = ""

    monthdate = str(expiry1)[-3:]

    if stock == "NIFTY":
        if monthdate == "JAN":
            date = 25
            month = "Jan"
        elif monthdate == "FEB":
            date = 29
            month = "Feb"
        elif monthdate == "MAR":
            date = 28
            month = "Mar"
        elif monthdate == "APR":
            date = 25
            month = "Apr"
        elif monthdate == "MAY":
            date = 30
            month = "May"
        elif monthdate == "JUN":
            date = 27
            month = "Jun"
        elif monthdate == "JUL":
            date = 25
            month = "Jul"
        elif monthdate == "AUG":
            date = 29
            month = "Aug"
        elif monthdate == "SEP":
            date = 26
            month = "Sep"
        elif monthdate == "OCT":
            date = 31
            month = "Oct"
        elif monthdate == "NOV":
            date = 28
            month = "Nov"
        elif monthdate == "DEC":
            date = 26
            month = "Dec"
    elif stock == "CNXBAN":
        if monthdate == "JAN":
            date = 25
            month = "Jan"
        elif monthdate == "FEB":
            date = 29
            month = "Feb"
        elif monthdate == "MAR":
            date = 27
            month = "Mar"
        elif monthdate == "APR":
            date = 24
            month = "Apr"
        elif monthdate == "MAY":
            date = 29
            month = "May"
        elif monthdate == "JUN":
            date = 26
            month = "Jun"
        elif monthdate == "JUL":
            date = 31
            month = "Jul"
        elif monthdate == "AUG":
            date = 28
            month = "Aug"
        elif monthdate == "SEP":
            date = 25
            month = "Sep"
        elif monthdate == "OCT":
            date = 30
            month = "Oct"
        elif monthdate == "NOV":
            date = 27
            month = "Nov"
        elif monthdate == "DEC":
            date = 25
            month = "Dec"

    if expiry1[-1].isdigit():
        if expiry1[2] == "1":
            month = "Jan"
        elif expiry1[2] == "2":
            month = "Feb"
        elif expiry1[2] == "3":
            month = "Mar"
        elif expiry1[2] == "4":
            month = "Apr"
        elif expiry1[2] == "5":
            month = "May"
        elif expiry1[2] == "6":
            month = "Jun"
        elif expiry1[2] == "7":
            month = "Jul"
        elif expiry1[2] == "8":
            month = "Aug"
        elif expiry1[2] == "9":
            month = "Sep"
        elif expiry1[2] == "O":
            month = "Oct"
        elif expiry1[2] == "N":
            month = "Nov"
        elif expiry1[2] == "D":
            month = "Dec"

        date = str(expiry1)[-2:]

    year = "20" + str(expiry1)[:2]

    full_date = str(date)+"-"+str(month)+"-"+str(year)

    return full_date

def expiry_to_date_old(expiry1):
    full_date = ""

    search = re.search(r"(\d{2})(\w{3})", expiry1)
    month = search[2]
    date = month[1]+month[2]

    month = month[0] + month[1:].lower()

    month = months[int(month[0])-1] if month[0].isnumeric() else month

    if month[0] == "O":
        month = "Oct"
    elif month[0] == "N":
        month = "Nov"
    elif month[0] == "D":
        month = "Dec"

    if date.isnumeric():
        full_date = date+"-"+month+"-20"+search[1]
    else:
        lastdate = calendar.monthrange(int("20"+search[1]), months.index(month)+1)
        lastdate = lastdate[1]
        if month == "Nov":
            full_date = "30-"+month+"-20"+search[1]
        else:
            full_date = "31-"+month+"-20"+search[1]

    return full_date

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
        name = "NSE:CNXBAN"
    elif stock == "NIFTY":
        name = "NSE:NIFTY"
    elif stock == "FINNIFTY":
        name = "NSE:NIFFIN"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    if stock == "NIFTY":
        stock = "NIFTY"
    elif stock == "BANKNIFTY":
        stock = "CNXBAN"
    return "NFO:" + str(stock) + str(intExpiry)+str(strike)+str(ce_pe)

def getLTP(instrument):
    url = "http://localhost:4000/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data['data']

def manualLTP(symbol, breeze, symbolType="option"):
    if symbolType == "option":
        [exchange_code,stock_name,expiry,strike,right] = extract_code_strike_expiry(symbol)
        product_type = "options"
        if right == "CE":
            right = "call"
        else:
            right = "put"
        b = breeze.get_names(exchange_code = "NSE",stock_code = stock_name)
        expiry_date = expiry_to_date(expiry,stock_name)
        expiry_date_string = datetime.datetime.strptime(f"{expiry_date} 06:00:00","%d-%b-%Y %H:%M:%S").isoformat()[:19] + '.000Z'

        a = breeze.get_quotes(stock_code=b['isec_stock_code'],
                              exchange_code=exchange_code,
                              expiry_date=expiry_date_string,
                              product_type="options",
                              right=right,
                              strike_price=strike)

    elif symbolType == "equity": #this will also work for index
        exchange_code = symbol[:3]
        stock_name = symbol[4:]
        product_type = "cash"
        b = breeze.get_names(exchange_code = exchange_code,stock_code = stock_name)
        a = breeze.get_quotes(stock_code=b['isec_stock_code'],
                              exchange_code=exchange_code,
                              expiry_date="2022-08-25T06:00:00.000Z",
                              product_type=product_type,
                              right="others",
                              strike_price="0")
        print(a)

    elif symbolType == "future":
        exchange_code = symbol[:3]
        stock_name = symbol[4:-8]
        product_type = "futures"
        b = breeze.get_names(exchange_code = "NSE",stock_code = stock_name)

        index_24 = symbol.find("24")
        expiry = symbol[index_24:index_24 + 5]
        expiry_date = expiry_to_date(expiry,"NIFTY")
        expiry_date_string = datetime.datetime.strptime(f"{expiry_date} 06:00:00","%d-%b-%Y %H:%M:%S").isoformat()[:19] + '.000Z'

        a = breeze.get_quotes(stock_code=b['isec_stock_code'],
                              exchange_code=exchange_code,
                              expiry_date=expiry_date_string,
                              product_type=product_type,
                              right="others",
                              strike_price="0")
        print(a)

    ltp = a['Success'][0]['ltp']
    open = a['Success'][0]['open']
    high = a['Success'][0]['high']
    low = a['Success'][0]['low']
    return ltp

def placeOrder(inst ,t_type,qty,order_type,price,variety, breeze, papertrading=0):
    exchange_code = ""
    stock_name = ""
    expiry1 = ""
    strike = ""
    right = ""
    expiry_date_string = ""

    if (t_type == "BUY"):
        action = "buy"
    else:
        action = "sell"

    if order_type == "MARKET":
        order_type1 = "market"
        price = 0
    elif order_type == "LIMIT":
        order_type1 = "limit"

    #find first 3 letters of inst
    symbolType = inst[:3]

    if symbolType == "NSE":
        dt = datetime.datetime.now()
        print(dt.hour,":",dt.minute,":",dt.second ," => ",t_type," ",inst," ",qty," ",order_type)

        if (papertrading == 1):
            #return stock_name, exchange_code, action, order_type1, qty, price, expiry_date_string, right, strike
            order_id = breeze.place_order(
                stock_code=inst.split(":")[1], #
                exchange_code=symbolType, #
                product="cash", #
                action=action,
                order_type=order_type1,
                stoploss="",
                quantity=str(qty),
                price=str(price),
                validity="day",
            )

            print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , order_id )
            return order_id
        else:
            return 0


    else:
        try:
            [exchange_code, stock_name, expiry1, strike, right] = extract_code_strike_expiry(inst)
            if right == "CE":
                right = "call"
            else:
                right = "put"
        except Exception as e:
            print(e)

        if expiry1:
            expiry_date_string = datetime.datetime.strptime(f"{expiry_to_date(expiry1,stock_name)} 06:00:00","%d-%b-%Y %H:%M:%S").isoformat()[:19] + '.000Z'

        #papertrading = 0 #if this is 1, then real trades will be placed

        dt = datetime.datetime.now()
        print(dt.hour,":",dt.minute,":",dt.second ," => ",t_type," ",inst," ",qty," ",order_type)
        try:
            if (papertrading == 1):
                #return stock_name, exchange_code, action, order_type1, qty, price, expiry_date_string, right, strike
                order_id = breeze.place_order(
                    stock_code=stock_name, #
                    exchange_code=exchange_code, #
                    product="options", #
                    action=action,
                    order_type=order_type1,
                    stoploss=0,
                    quantity=str(qty),
                    price=str(price),
                    validity="day",
                    validity_date="",
                    disclosed_quantity="0",
                    expiry_date=expiry_date_string, #
                    right=right, #
                    strike_price=strike, #
                    user_remark="")

                print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , order_id )
                return order_id
            else:
                return 0

        except Exception as e:
            print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , "Failed : {} ".format(e))



def getHistorical(ticker,interval,duration, breeze):
    #https://pypi.org/project/breeze-connect/#historical_data1
    #https://www.icicidirect.com/futures-and-options/articles/how-to-download-historical-data-using-breeze-api-python-sdk
    exch = ticker[:3]
    sym = ticker[4:]

    time_intervals = {
        1: "1minute",
        5: "5minute",
        30: "30minute",
    }
    interval_str = time_intervals.get(interval, "Key not found")

    #find todate
    current_time = datetime.datetime.now()
    previous_minute_time = current_time - timedelta(minutes=1)
    start_date = previous_minute_time - timedelta(days=duration)
    to_date_string = previous_minute_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    start_date_string = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # downloading historical data for put option contract
    #data1 = breeze.get_historical_data(interval = time_interval,from_date = start_date,to_date = end_date,
    #                                 stock_code = "NIFTY",exchange_code = "NFO",product_type = "options",
    #                                 expiry_date = "2022-04-19T18:00:00.000Z",right = "put",strike_price = 19000)
    #put_data = pd.DataFrame(data1["Success"])


    #return interval_str, start_date_string, to_date_string, str(sym), str(exch)
    # downloading historical data for Nifty
    data2 = breeze.get_historical_data(interval = interval_str,
                                       from_date = start_date_string,
                                       to_date = to_date_string,
                                       stock_code = str(sym),
                                       exchange_code = str(exch),
                                       product_type = "cash")   #futures

    stock_data = pd.DataFrame(data2["Success"])
    stock_data['datetime'] = pd.to_datetime(stock_data['datetime'])
    # Filtering rows between 9:15 and 15:30
    start_time = pd.to_datetime('09:15:00').time()
    end_time = pd.to_datetime('15:29:00').time()
    filtered_df = stock_data[(stock_data['datetime'].dt.time >= start_time) & (stock_data['datetime'].dt.time <= end_time)]
    filtered_df.rename(columns={'open_interest': 'oi'}, inplace=True)

    return (filtered_df)



