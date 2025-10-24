import os, sys

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from api_helper import ShoonyaApiPy
from NorenApi import NorenApi
import time
import pandas as pd
from time import sleep
import threading
from flask import Flask, request
import helper_shoonya as helper
import datetime as dt

start_time = dt.time(9, 15)
end_time = dt.time(15, 30)


while True:
    current_time = dt.datetime.now().time()
    if not (start_time <= current_time <= end_time):
        print("Waiting for market hours (09:15 to 03:30)")
        time.sleep(60)
    else:
        print("Market hours are open")
        break
##############################################
#                   INPUT's                  #
##############################################
# NSE:ACC   --> NSE|22
# NSE:NTPC  --> NSE|11630

api = NorenApi()
api.token_setter()

intExpiry=helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
intExpiry_Fin = helper.getFinNiftyExpiryDate()
strikeList=[]
symbolList = []

#NIFTY
ltp = api.get_quotes(exchange="NSE", token="Nifty 50")
a = float(ltp['lp'])

for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add Index
#symbolList.append('NSE:Nifty 50')

#Add CE
for strike in strikeList:
    ltp_option = "NFO:NIFTY" + str(intExpiry)+"C"+str(strike)
    symbolList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:NIFTY" + str(intExpiry)+"P"+str(strike)
    symbolList.append(ltp_option)

strikeList=[]
#BANKNIFTY
ltp = api.get_quotes(exchange="NSE", token="Nifty Bank")
a = float(ltp['lp'])

for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)

#Add Index
#symbolList.append('NSE:Nifty Bank')

#Add CE
for strike in strikeList:
    ltp_option = "NFO:BANKNIFTY" + str(intExpiry_BN)+"C"+str(strike)
    symbolList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:BANKNIFTY" + str(intExpiry_BN)+"P"+str(strike)
    symbolList.append(ltp_option)

strikeList=[]
#FINNIFTY
ltp = api.get_quotes(exchange="NSE", token="26037")
a = float(ltp['lp'])

for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:FINNIFTY" + str(intExpiry_Fin)+"C"+str(strike)
    symbolList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:FINNIFTY" + str(intExpiry_Fin)+"P"+str(strike)
    symbolList.append(ltp_option)



#Put all options in the beginning
symbolList1 = [
    'NSE:Nifty 50',
    'NSE:Nifty Bank',
    'NSE:Nifty Fin Service'

    # 'MCX:CRUDEOILM19AUG24',
    # 'CDS:USDJPY26APR24F'
]

symbolList = symbolList + symbolList1
# symbolList = symbolList1
print("BELOW IS THE COMPLETE INSTRUMENT LIST")
print(symbolList)

instrumentList = []
symb_token_map = {}
socket_opened = False


exch = "NFO"
token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')

for i in range(len(symbolList)):
    symbol = symbolList[i]
    exch = symbol[:3]
    name = symbol[4:]
    if exch != 'NFO':
        token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')

    print(name)
    try:
        if name == "Nifty 50":
            inst = exch + "|" + "26000"
            symb_token_map[symbolList[i]] = inst
        elif name == "Nifty Bank":
            inst = exch + "|" + "26009"
            symb_token_map[symbolList[i]] = inst
        elif name == "Nifty Fin Service":
            inst = exch + "|" + "26037"
            symb_token_map[symbolList[i]] = inst
        else:
            #for j in range(0,len(token)):
            #    if(token['TradingSymbol'][j] == name):
            #        inst = exch + "|" + str(token['Token'][j])
            #        symb_token_map[symbolList[i]] = inst
            #        time.sleep(1)
            #        print(inst)
            exchangetoken1 = str(token[token['TradingSymbol'] == name]['Token'].values[0])
            inst = exch + "|" + exchangetoken1
            symb_token_map[symbolList[i]] = inst
            print(inst)
    except IndexError as e:
        print("Skipping", name)


for symb in symbolList:
    if symb in symb_token_map:
        print(symb)
        instrumentList.append(symb_token_map[symb])


print(symb_token_map)
print('------------------------')
print(instrumentList)

##############################################
#                   SERVER                   #
##############################################
app = Flask(__name__)
LTPDICT = {}

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/ltp')
def getLtp():
    global LTPDICT
    try:
        print(LTPDICT)
        ltp = -1
        instrumet = request.args.get('instrument')
        ltp = LTPDICT[symb_token_map[instrumet]]
    except Exception as e :
        print("EXCEPTION occured while getting LTPDICT()")
        print(e)
    return str(ltp)


def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4002)

##############################################
#                  SHOONYA                   #
##############################################



# # For debugging enable this
#logging.basicConfig(level=logging.DEBUG)

#application callbacks
def event_handler_order_update(message):
    print("ORDER : {0}".format(time.strftime('%d-%m-%Y %H:%M:%S')) + str(message))

def event_handler_quote_update(tick):
    global LTPDICT
    key = tick['e'] + '|' + tick['tk']
    LTPDICT[key] = tick['lp']
    print(LTPDICT)

def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')

    # api.subscribe('NSE|11630', feed_type='d')
    api.subscribe(instrumentList)

#end of callbacks

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')
    return time.mktime(data)

def is_connection_active(timeout):
    try:
        requests.head("http://www.google.com",timeout=timeout)
        return True
    except:
        return False

def main():
    global uid
    global pwd
    global vc
    global app_key
    global imei

    #start of our program
    print(" Main Started ")
    t1 = threading.Thread(target=startServer)
    t1.start()
    sleep(1)

    ret = api.start_websocket(order_update_callback=event_handler_order_update, subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback)

    connected = True
    reconnect = False
    x = requests.get('http://localhost:4002/ltp?instrument=NSE:Nifty 50').json()
    count_same_x=0
    while True:
        current_time = dt.datetime.now().time()
        if current_time >= end_time:
            api.close_websocket()
            break
        if not connected:
            if is_connection_active(1):
                connected = True
                reconnect = True
        else:
            # Connection fine!

            # Checking if we are getting same data for 30s
            test_data = requests.get('http://localhost:4002/ltp?instrument=NSE:Nifty 50').json()
            print(test_data)
            if(x==test_data):
                count_same_x += 1
                if(count_same_x==15):
                    reconnect = True
                    print("Data Stuck! Attempting Reconnect...")
                    api.close_websocket()

            else:
                count_same_x = 0
                x=test_data

        if (reconnect):
            ret = api.start_websocket(order_update_callback=event_handler_order_update, subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback)
            reconnect = False

        if not is_connection_active(1):
            time.sleep(1)
            api.close_websocket()
            print("Network Disconnected, Waiting for connection...")
            connected = False


    sleep(2)
    while True:
        continue

    t1.join()


main()

