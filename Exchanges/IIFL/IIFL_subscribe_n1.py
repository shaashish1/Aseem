# https://ttblaze.iifl.com/apimarketdata/instruments/indexlist?exchangeSegment=1
import threading
import datetime as dt
import time
import json
import pandas as pd
from flask import Flask, request
from Connect import XTSConnect
from MarketDataSocketClient import MDSocket_io

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

# MarketData API Credentials
API_KEY = "26f19be39f043cb383a"
API_SECRET = "Ixdk865@o"
source = "WEBAPI"

with open("iifl_market_api_key.txt", 'w') as file:
    file.write(API_KEY)
with open("iifl_market_secret_key.txt", 'w') as file:
    file.write(API_SECRET)

# Initialise
xt = XTSConnect(API_KEY, API_SECRET, source)
# Login for authorization token
response = xt.marketdata_login()

# Store the token and userid
set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID']
with open('user_id.txt','w') as f:
    f.write(str(set_muserID))
print("Login: ", response)

resmaster = xt.get_master( ["NSECM","NSECD","NSEFO","BSECM","BSEFO","MCXFO"])

id_to_symbol_dict = {}
symbol_to_id_dict = {}
segments_dict = {"NSECM": 1, "NSEFO": 2, "NSECD": 3, "BSECM": 11, "BSEFO": 12, "MCXFO": 51}

master_data = resmaster['result'].split('\n')
for i in range(0,len(master_data)):
    single_row = master_data[i].split('|')
    id_to_symbol_dict[str(segments_dict[single_row[0]])+"|"+str(single_row[1])] = single_row[4]
    symbol_to_id_dict[single_row[4]] = str(segments_dict[single_row[0]])+"|"+str(single_row[1])

id_to_symbol_dict['1|26000'] = 'Nifty 50'
id_to_symbol_dict['1|26001'] = 'Nifty Bank'
id_to_symbol_dict['1|26034'] = 'Nifty Fin Service'
symbol_to_id_dict['Nifty 50'] = '1|26000'
symbol_to_id_dict['Nifty Bank'] = '1|26001'
symbol_to_id_dict['Nifty Fin Service'] = '1|26034'

with open('symbol_mapping.txt', 'w') as f:
    f.write(str([symbol_to_id_dict]))
import helper_iifl as helper

# Add symbols to subscribe
symbols = [#'CRUDEOIL24APRFUT',
         #  'SILVERMIC24JUNFUT',
         #  'FINNIFTY24APRFUT',
         #  'BANKNIFTY2441045700CE',
           'Nifty 50',
           'Nifty Bank',
           'Nifty Fin Service']
# Adding different strikes to subscribe
intExpiry=helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
intExpiry_Fin = helper.getFinNiftyExpiryDate()
strikeList=[]
symbolList = []

response = xt.get_index_list(exchangeSegment=xt.EXCHANGE_NSEFO)
print('Index List:', str(response))

#NIFTY
a = helper.manualLTP('Nifty 50',xt)


for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add Index
#symbolList.append('NSE:Nifty 50')

#Add CE
for strike in strikeList:
    ltp_option = "NIFTY" + str(intExpiry)+str(strike)+"CE"
    symbols.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NIFTY" + str(intExpiry)+str(strike)+"PE"
    symbols.append(ltp_option)
a=0
strikeList=[]
#BANKNIFTY
a = helper.manualLTP('Nifty Bank',xt)
# print(a)
for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)

#Add Index
#symbolList.append('NSE:Nifty Bank')

#Add CE
for strike in strikeList:
    ltp_option = "BANKNIFTY" + str(intExpiry_BN)+str(strike)+"CE"
    symbols.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "BANKNIFTY" + str(intExpiry_BN)+str(strike)+"PE"
    symbols.append(ltp_option)

strikeList=[]
a=0
#FINNIFTY
a = helper.manualLTP('Nifty Fin Service',xt)
for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add CE
for strike in strikeList:
    ltp_option = "FINNIFTY" + str(intExpiry_Fin)+str(strike)+"CE"
    symbols.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "FINNIFTY" + str(intExpiry_Fin)+str(strike)+"PE"
    symbols.append(ltp_option)



# nifty_ltp = helper.manualLTP('FINNIFTY24APRFUT',xt)
# print(nifty_ltp)

# nifty_hist = helper.getHistorical('Nifty 50',5,5,xt)
# print(nifty_hist)
# quit()




# Connecting to Marketdata socket
soc = MDSocket_io(set_marketDataToken, set_muserID)

# Instruments for subscribing
Instruments = []
for symbol in symbols:
    try:
        sid = symbol_to_id_dict[symbol].split('|')
        Instruments.append({'exchangeSegment':sid[0],'exchangeInstrumentID':sid[1]})
    except:
        print("Skipping ",symbol)

print(symbols)
print(Instruments)
app = Flask(__name__)
# token_symb_map = {}
ltp_dict = {}


@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/ltp')
def getLtp():
    print(ltp_dict)
    ltp = -1
    instrument = request.args.get('instrument')
    try:
        ltp = ltp_dict[instrument]
    except Exception as e :
        print("EXCEPTION occured while getting ltpDict()")
        print(e)
    return str(ltp)

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4000)

t1 = threading.Thread(target=startServer)
t1.start()

# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')

    # # Subscribe to instruments
    print('Sending subscription request for Instruments - \n' + str(Instruments))
    response = xt.send_subscription(Instruments, 1501)
    print('Sent Subscription request!')
    print("Subscription response: ", response)

# Callback on receiving message
def on_message(data):
    print('I received a message!')

# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    # print('I received a 1501 Touchline message!' + data)
    data_json = json.loads(data)
    exchangesegment = data_json['ExchangeSegment']
    instrumentid = data_json['ExchangeInstrumentID']
    # instrumentname = xt.search_by_instrumentid(Instruments=instrumentid)
    try:
        ltp = data_json['Touchline']['LastTradedPrice']
    # open     = data_json['Touchline']['Open']
    # high = data_json['Touchline']['High']
    # low = data_json['Touchline']['Low']
        ltp_dict[id_to_symbol_dict[str(exchangesegment)+"|"+str(instrumentid)]] = ltp
        print(ltp_dict)
    except:
        print("No data found.")

    # print(exchangesegment, instrumentid, ltp,open,high,low)

# Callback for message code 1502 FULL
def on_message1502_json_full(data):
    print('I received a 1502 Market depth message!' + data)

# Callback for message code 1505 FULL
def on_message1505_json_full(data):
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1507 FULL
def on_message1507_json_full(data):
    print('I received a 1507 MarketStatus data message!' + data)

# Callback for message code 1510 FULL
def on_message1510_json_full(data):
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1512 FULL
def on_message1512_json_full(data):
    print('I received a 1512 Level1,LTP message!' + data)

# Callback for message code 1105 FULL
def on_message1105_json_full(data):
    return
    print('I received a 1105, Instrument Property Change Event message!' + data)


# Callback for message code 1501 PARTIAL
def on_message1501_json_partial(data):
    return
    print('I received a 1501, Touchline Event message!' + data)

# Callback for message code 1502 PARTIAL
def on_message1502_json_partial(data):
    return
    print('I received a 1502 Market depth message!' + data)

# Callback for message code 1505 PARTIAL
def on_message1505_json_partial(data):
    return
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1510 PARTIAL
def on_message1510_json_partial(data):
    return
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1512 PARTIAL
def on_message1512_json_partial(data):
    return
    print('I received a 1512, LTP Event message!' + data)



# Callback for message code 1105 PARTIAL
def on_message1105_json_partial(data):
    return
    print('I received a 1105, Instrument Property Change Event message!' + data)

# Callback for disconnection
def on_disconnect():
    print('Market Data Socket disconnected!')
    print("Connecting again.")
    soc.connect()


# Callback for error
def on_error(data):
    """Error from the socket."""
    print('Market Data Error', data)


# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_message1502_json_full = on_message1502_json_full
soc.on_message1505_json_full = on_message1505_json_full
soc.on_message1507_json_full = on_message1507_json_full
soc.on_message1510_json_full = on_message1510_json_full
soc.on_message1501_json_full = on_message1501_json_full
soc.on_message1512_json_full = on_message1512_json_full
soc.on_message1105_json_full = on_message1105_json_full
soc.on_message1502_json_partial = on_message1502_json_partial
soc.on_message1505_json_partial = on_message1505_json_partial
soc.on_message1510_json_partial = on_message1510_json_partial
soc.on_message1501_json_partial = on_message1501_json_partial
soc.on_message1512_json_partial = on_message1512_json_partial
soc.on_message1105_json_partial = on_message1105_json_partial
soc.on_disconnect = on_disconnect
soc.on_error = on_error


# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('1501-json-full', on_message1501_json_full)
el.on('1502-json-full', on_message1502_json_full)
el.on('1507-json-full', on_message1507_json_full)
el.on('1512-json-full', on_message1512_json_full)
el.on('1105-json-full', on_message1105_json_full)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
soc.connect()

