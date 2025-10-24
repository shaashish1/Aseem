from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel
from flask import Flask, request
import threading
import helper_fyers as helper

##############################################
#                   INPUT's                  #
##############################################
app_id = open("fyers_client_id.txt",'r').read()
access_token = open("fyers_access_token.txt",'r').read()
fyers = fyersModel.FyersModel(token=access_token,is_async=False,client_id=app_id)

intExpiry=helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
intExpiry_Fin = helper.getFinNiftyExpiryDate()
strikeList=[]
instrumentList = []

#NIFTY
data = {
    "symbols":"NSE:NIFTY50-INDEX"
}
ltp = fyers.quotes(data=data)
if ltp.get('s') == 'error':
    print(f"Error fetching quotes: {ltp.get('message')}")
else:
    a = ltp['d'][0]['v']['lp']
    print(a)
    for i in range(-5, 5):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)
        strikeList.append(strike+50)

    #Add Index
    instrumentList.append('NSE:NIFTY50-INDEX')

    #Add CE
    for strike in strikeList:
        ltp_option = "NSE:NIFTY" + str(intExpiry)+str(strike)+"CE"
        instrumentList.append(ltp_option)

    #Add PE
    for strike in strikeList:
        ltp_option = "NSE:NIFTY" + str(intExpiry)+str(strike)+"PE"
        instrumentList.append(ltp_option)

strikeList=[]
#BANKNIFTY
data = {
    "symbols":"NSE:NIFTYBANK-INDEX"
}
ltp = fyers.quotes(data=data)
if ltp.get('s') == 'error':
    print(f"Error fetching quotes: {ltp.get('message')}")
else:
    a = ltp['d'][0]['v']['lp']
    for i in range(-10, 10):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)

    #Add Index
    instrumentList.append('NSE:NIFTYBANK-INDEX')

    #Add CE
    for strike in strikeList:
        ltp_option = "NSE:BANKNIFTY" + str(intExpiry_BN)+str(strike)+"CE"
        instrumentList.append(ltp_option)

    #Add PE
    for strike in strikeList:
        ltp_option = "NSE:BANKNIFTY" + str(intExpiry_BN)+str(strike)+"PE"
        instrumentList.append(ltp_option)

strikeList=[]
#FINNIFTY
data = {
    "symbols":"NSE:FINNIFTY-INDEX"
}
ltp = fyers.quotes(data=data)
if ltp.get('s') == 'error':
    print(f"Error fetching quotes: {ltp.get('message')}")
else:
    a = ltp['d'][0]['v']['lp']
    print(a)
    for i in range(-5, 5):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)
        strikeList.append(strike+50)

    #Add Index
    instrumentList.append('NSE:FINNIFTY-INDEX')

    #Add CE
    for strike in strikeList:
        ltp_option = "NSE:FINNIFTY" + str(intExpiry_Fin)+str(strike)+"CE"
        instrumentList.append(ltp_option)

    #Add PE
    for strike in strikeList:
        ltp_option = "NSE:FINNIFTY" + str(intExpiry_Fin)+str(strike)+"PE"
        instrumentList.append(ltp_option)


instrumentList1 = [
    "NSE:NIFTY50-INDEX",
    "NSE:NIFTYBANK-INDEX",
    "NSE:FINNIFTY-INDEX",
    "NSE:SBIN-EQ",

]


instrumentList = instrumentList + instrumentList1
# instrumentList = instrumentList1
print("BELOW IS THE COMPLETE INSTRUMENT LIST")
print(instrumentList)
##############################################
print("!! Started getltpDict.py !!")

app = Flask(__name__)

tokenMapping = {}
ltpDict = {}

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/ltp')
def getLtp():
    global ltpDict
    print(ltpDict)
    ltp = -1
    instrument = request.args.get('instrument')  # Corrected variable name
    try:
        ltp = ltpDict[instrument]
    except Exception as e :
        print("EXCEPTION occured while getting ltpDict()")
        print(e)
    return str(ltp)

def onmessage(message):
    global ltpDict
    ltpDict[message['symbol']] = message['ltp']
    print(ltpDict)

def onerror(_):
    print("")

def onclose(message):
    print("Connection closed:", message)

def onopen():
    print("Connection opened")

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4001)

def main():
    print("Inside main()")
    t1 = threading.Thread(target=startServer)
    t1.start()

    access_token_websocket = app_id + ":" + access_token

    fyers = data_ws.FyersDataSocket(access_token=access_token_websocket,
                                    write_to_file=False,
                                    reconnect=True,
                                    on_connect=onopen,
                                    on_close=onclose,
                                    on_error=onerror,
                                    on_message=onmessage,
                                    log_path="./")

    fyers.connect()

    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # Subscribe to the specified symbols and data type
    fyers.subscribe(symbols=instrumentList, data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()

    t1.join()
    print("websocket started !!")

main()