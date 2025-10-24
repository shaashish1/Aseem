from breeze_connect import BreezeConnect
import urllib
from flask import Flask, request
import threading
import re
import calendar
import helper_icici as helper
import pandas as pd

api_key = open("icici_api_key.txt",'r').read()
secret_key = open("icici_secret_key.txt").read()
session_key = open("icici_session_key.txt").read()
#https://www.icicidirect.com/futures-and-options/api/breeze/article/what-is-a-session-key-and-how-to-generate-it-for-using-breezeapi

ltp_dict = {}
optInstrList = []
futInstrList = []
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

intExpiry=helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
strikeList=[]
instrumentList = []

breeze = BreezeConnect(api_key=api_key)
breeze.generate_session(api_secret=secret_key,
                        session_token=session_key)

#NIFTY
a = helper.getHistorical("NSE:NIFTY",1,1,breeze)
nifty_ltp = float(a['close'].iloc[-1])

for i in range(-5, 5):
    strike = (int(nifty_ltp / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:NIFTY" + str(intExpiry)+str(strike)+"CE"
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:NIFTY" + str(intExpiry)+str(strike)+"PE"
    instrumentList.append(ltp_option)

strikeList=[]
#BANKNIFTY
a = helper.getHistorical("NSE:CNXBAN",1,1,breeze)
bnnifty_ltp = float(a['close'].iloc[-1])
print(a)

for i in range(-5, 5):
    strike = (int(bnnifty_ltp / 100) + i) * 100
    strikeList.append(strike)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:CNXBAN" + str(intExpiry_BN)+str(strike)+"CE"
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:CNXBAN" + str(intExpiry_BN)+str(strike)+"PE"
    instrumentList.append(ltp_option)

instrumentList1 = [
    "NSE:SBIN",
    "NSE:NIFTY",
    "NSE:CNXBAN",
    "NSE:NIFFIN",
    "NSE:NIFSEL"
]

instrumentList = instrumentList + instrumentList1
print("BELOW IS THE COMPLETE INSTRUMENT LIST")
print(instrumentList)

# This is where you can get your session key
print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(api_key))

def on_ticks(ticks):
    #print("Ticks: {}".format(ticks))
    if ticks.get('symbol') != None:
        #USUAL
        #print(ticks)
        if 'last' in ticks:
            ltp_dict[ticks["symbol"]] = float(ticks["last"])

    elif ticks.get('symbol') == None and ticks.get('right_type') == None:
        #FUTURES
        expiry_split = ticks['expiry_date'].split("-")
        monthrange = calendar.monthrange(int(expiry_split[2]), months.index(expiry_split[1])+1)
        if expiry_split[0] != str(monthrange[1]):
            expiry = expiry_split[2][2:]+str(months.index(expiry_split[1])+1)+expiry_split[0]
        else:
            expiry = expiry_split[2][2:]+expiry_split[1].upper()
        
        stock_full = ticks["stock_code"]+expiry+"FUT"
        ltp_dict[stock_full] = float(ticks["close"])
        
    elif ticks.get('right_type') != None:
        #OPTIONS
        '''
        expiry_split = ticks['expiry_date'].split("-")
        print("expiry split",expiry_split)
    
        monthrange = calendar.monthrange(int(expiry_split[2]), months.index(expiry_split[1])+1)
        print("monthrange",monthrange)
        if expiry_split[0] != str(monthrange[1]):
            expiry = expiry_split[2][2:]+str(months.index(expiry_split[1])+1)+expiry_split[0]
        else:
            expiry = expiry_split[2][2:]+expiry_split[1].upper()
        '''
        if ticks['stock_code'] == "CNXBAN":
            expiry = intExpiry_BN
        else:
            expiry = intExpiry
        stock_full = ticks["stock_code"]+expiry+str(ticks['strike_price']).split('.')[0]+ticks["right_type"]
        ltp_dict[stock_full] = float(ticks["close"])

    print(ltp_dict)

def get_tokens(instr_list):
    tokens = []
    for instr in instr_list:
        try:
            instr_info = instr.split(":")
            stock_name = instr_info[1]
            opt_search = re.search(r"(\d{2})(\w{3})((\d+)|(\d+\.\d+))(CE|PE)", stock_name)
            fut_search = re.search(r"(\d{2}\w{3})(FUT)", stock_name)

            if opt_search:
                optInstrList.append(instr)
            elif fut_search:
                futInstrList.append(instr)
            else:
                name = breeze.get_names(instr_info[0], instr_info[1])
                tokens.append(name["isec_token_level1"])

        except Exception as e:
            print("Error getting stock token:", e)
    
    print("token list", tokens)
    return tokens

token_list = get_tokens(instrumentList)

app = Flask(__name__)

@app.route('/ltp')
def getLTP():
    try:
        instrument = request.args.get('instrument')
        instr_info = instrument.split(":")
        stock_name = instr_info[1]

        opt_search = re.search(r"(\d{2})(\w{3})((\d+)|(\d+\.\d+))(CE|PE)", stock_name)
        fut_search = re.search(r"(\d{2}\w{3})(FUT)", stock_name)

        if opt_search or fut_search:
            ltp = ltp_dict[stock_name]
        else:
            name = breeze.get_names(instr_info[0], stock_name)
            ltp = ltp_dict[name["isec_token_level1"]]

        return {
            "data": float(ltp)
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    
def expiry_to_date(expiry):
    full_date = ""

    search = re.search(r"(\d{2})(\w{3})", expiry)
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
        month_cal = calendar.monthcalendar(int("20"+search[1]), months.index(month)+1)
        thursday = max(month_cal[-1][calendar.THURSDAY], month_cal[-2][calendar.THURSDAY])

        full_date = str(thursday)+"-"+month+"-20"+search[1]

    return full_date

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4000)

def main():
    print("Inside main()")
    t1 = threading.Thread(target=startServer)
    t1.start()

    breeze.ws_connect()
    breeze.on_ticks = on_ticks

    for stock_token in token_list:
        msg = breeze.subscribe_feeds(stock_token=stock_token)
        print(msg)

    for future_stock in futInstrList:
        split = future_stock.split(":")
        exchange = split[0]
        stock_name = split[1]
        fut_search = re.search(r"(\d{2}\w{3})(FUT)", stock_name)

        if fut_search:
            stock_code = stock_name.replace(fut_search[0], "")
            expiry_date = expiry_to_date(fut_search[1])

            msg = breeze.subscribe_feeds(exchange_code=exchange, interval="1second", stock_code=stock_code, product_type="futures", strike_price="", right="", expiry_date=expiry_date)

            print(stock_name, msg)
    
    for option_stock in optInstrList:
        print(option_stock)
        split = option_stock.split(":")
        exchange = split[0]
        stock_name = split[1]
        opt_search = re.search(r"(\d{2})(\w{3})((\d+)|(\d+\.\d+))(CE|PE)", stock_name)
        print(opt_search)

        if opt_search:
            month = opt_search[2].upper()
            month = month[0] + month[1:].lower()
            
            stock_code = stock_name.replace(opt_search[0], "")
            expiry = expiry_to_date(opt_search[1]+opt_search[2])
            strike = opt_search[3]
            #right = opt_search[4]
            right = option_stock[-2:]
            right = "Put" if right == "CE" else "Call"
            print(stock_code, expiry, strike, right)
            msg = breeze.subscribe_feeds(exchange_code=exchange, interval="1second", stock_code=stock_code, product_type="options", expiry_date=expiry, strike_price=strike, right=right, get_exchange_quotes=True, get_market_depth=False)
            print(msg)

main()
