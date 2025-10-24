from pya3 import *
# from datetime import datetime
#from alice_blue import *
from flask import Flask, request
import time
import re
import calendar
import pandas as pd
import helper_alice as helper
#https://github.com/jerokpradeep/pya3
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

username = open("alice_username.txt",'r').read()
apiKey = open("alice_api.txt",'r').read()
alice = Aliceblue(user_id=username,api_key=apiKey)
session = alice.get_session_id()
if session['stat'] == 'Ok':
    print("api connected successfully")
else:
    print(session['emsg'])

intExpiry=helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
intExpiry_Fin = helper.getFinNiftyExpiryDate()
strikeList=[]
instrumentList = []


#NIFTY
nifty_ltp = alice.get_scrip_info(alice.get_instrument_by_token('NSE', 26000))
a = float(nifty_ltp['LTP'])


for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:NIFTY" + str(intExpiry)+"C"+str(strike)
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:NIFTY" + str(intExpiry)+"P"+str(strike)
    instrumentList.append(ltp_option)

strikeList=[]
#BANKNIFTY
banknifty_ltp = alice.get_scrip_info(alice.get_instrument_by_token('NSE', 26009))
a = float(banknifty_ltp['LTP'])

for i in range(-10, 10):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:BANKNIFTY" + str(intExpiry_BN)+"C"+str(strike)
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:BANKNIFTY" + str(intExpiry_BN)+"P"+str(strike)
    instrumentList.append(ltp_option)

strikeList=[]
#FINNIFTY
finnifty_ltp = alice.get_scrip_info(alice.get_instrument_by_token('NSE', 26037))
a = float(finnifty_ltp['LTP'])


for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:FINNIFTY" + str(intExpiry_Fin)+"C"+str(strike)
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:FINNIFTY" + str(intExpiry_Fin)+"P"+str(strike)
    instrumentList.append(ltp_option)


instrumentList1 = [
        "NSE:SBICARD-EQ",
        "NSE:RELIANCE-EQ",
        "NSE:NIFTY 50",
        "NSE:NIFTY BANK",
        "NSE:SBIN-EQ",
        "NSE:NIFTY FIN SERVICE"
    ]


symbol_list = instrumentList1 + instrumentList
print("BELOW IS THE COMPLETE INSTRUMENT LIST")
print(symbol_list)

app = Flask(__name__)
token_symb_map = {}
ltp_dict = {}

symbols_to_subscribe = []
df_nse = pd.read_csv("NSE.csv")
df_nfo = pd.read_csv("NFO.csv")
df_cds = pd.read_csv("CDS.csv")
df_mcx = pd.read_csv("MCX.csv")

for symbol in symbol_list:
    exchange = symbol.split(":")[0]
    instrument = symbol.split(":")[1]

    tok = 0
    if instrument == "NIFTY 50":
        tok = 26000
    elif instrument == "NIFTY BANK":
        tok = 26009
    elif instrument == "NIFTY FIN SERVICE":
        tok = 26037
    elif instrument == "NIFTY MIDCAP SELECT":
        tok = 26074
    elif exchange == "NSE":
        result = df_nse[(df_nse['Group Name'] == 'EQ') & (df_nse['Trading Symbol'] == instrument)]
        if not result.empty:
            # Access the value in the 'token' column for the first matching row
            tok = result.iloc[0]['Token']
        else:
            print("MISSING", instrument)
    elif exchange == "NFO":
        result = df_nfo[(df_nfo['Trading Symbol'] == instrument)]
        if not result.empty:
            # Access the value in the 'token' column for the first matching row
            tok = result.iloc[0]['Token']
        else:
            print("MISSING", instrument)
    elif exchange == "MCX":
        result = df_mcx[(df_mcx['Trading Symbol'] == instrument)]
        if not result.empty:
            # Access the value in the 'token' column for the first matching row
            tok = result.iloc[0]['Token']
        else:
            print("MISSING", instrument)
    elif exchange == "CDS":
        result = df_cds[(df_cds['Trading Symbol'] == instrument)]
        if not result.empty:
            # Access the value in the 'token' column for the first matching row
            tok = result.iloc[0]['Token']
        else:
            print("MISSING", instrument)

    token_symb_map[tok] = symbol

    inst1 = alice.get_instrument_by_symbol(exchange,instrument)
    print(inst1)
    symbols_to_subscribe.append(inst1)

print ("symbols to sbusbribe", symbols_to_subscribe)
print("mapping", token_symb_map)

LTP = 0
socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []
def socket_open():  # Socket open callback function
    print("Connected")
    global socket_opened
    socket_opened = True
    if subscribe_flag:  # This is used to resubscribe the script when reconnect the socket.
        alice.subscribe(subscribe_list)

def socket_close():  # On Socket close this callback function will trigger
    global socket_opened, LTP
    socket_opened = False
    LTP = 0
    print("Closed")

def socket_error(message):  # Socket Error Message will receive in this callback function
    global LTP
    LTP = 0
    tok = 0
    print("Error :", message)

def feed_data(message):  # Socket feed data will receive in this callback function
    global LTP, subscribe_flag, ltp_dict, tok
    feed_message = json.loads(message)
    if feed_message["t"] == "ck":
        print("Connection Acknowledgement status :%s (Websocket Connected)" % feed_message["s"])
        subscribe_flag = True
        print("subscribe_flag :", subscribe_flag)
        print("-------------------------------------------------------------------------------")
        pass
    elif feed_message["t"] == "tk":
        print("Token Acknowledgement status :%s " % feed_message)
        tok = feed_message['tk'] if 'tk' in feed_message else tok  #
        ltp = feed_message['lp'] if 'lp' in feed_message else 0  #
        symb = token_symb_map.get(int(tok),None)
        # print(tok, ltp, symb)
        ltp_dict[symb] = float(ltp)
        print("-------------------------------------------------------------------------------")
        pass
    else:
        # print("Feed :", feed_message)
        tok = feed_message['tk'] if 'tk' in feed_message else tok  #
        symb = token_symb_map.get(int(tok),None)
        ltp = feed_message['lp'] if 'lp' in feed_message else ltp_dict[symb]  #
        # print(tok, ltp, symb)
        ltp_dict[symb] = float(ltp)
        print(ltp_dict)

# Socket Connection Request
alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True,market_depth=False)

while not socket_opened:
    pass

subscribe_list = symbols_to_subscribe
alice.subscribe(subscribe_list)
print(alice.get_balance()) # get balance / margin limits
print(alice.get_profile()) # get profile

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

def is_connection_active(timeout):
    try:
        requests.head("http://www.google.com",timeout=timeout)
        return True
    except:
        return False

connected = True
reconnect = False
x = requests.get('http://localhost:4000/ltp?instrument=NSE:NIFTY 50').json()
count_same_x=0
while True:
    current_time = dt.datetime.now().time()
    if current_time >= end_time:
        alice.stop_websocket()
        break
    if not connected:

        if is_connection_active(1):
            connected = True
            reconnect = True
    else:
        # Connection fine!

        # Checking if we are getting same data for 30s
        test_data = requests.get('http://localhost:4000/ltp?instrument=NSE:NIFTY 50').json()
        print(test_data)
        if(x==test_data):
            count_same_x += 1
            if(count_same_x==15):
                reconnect = True
                print("Data Stuck! Attempting Reconnect...")
                alice.stop_websocket()

        else:
            count_same_x = 0
            x=test_data

    if (reconnect):
        alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True,market_depth=False)
        while not socket_opened:
            pass

        subscribe_list = symbols_to_subscribe
        alice.subscribe(subscribe_list)
        reconnect = False

    if not is_connection_active(1):
        time.sleep(1)
        try:
            alice.stop_websocket()
        except:
            pass
        print("Network Disconnected, Waiting for connection...")
        connected = False

