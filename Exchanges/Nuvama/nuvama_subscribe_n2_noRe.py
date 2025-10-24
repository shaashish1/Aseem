from APIConnect.APIConnect import APIConnect
from constants.exchange import ExchangeEnum
from constants.order_type import OrderTypeEnum
from constants.product_code import ProductCodeENum
from constants.duration import DurationEnum
from constants.action import ActionEnum
from constants.asset_type import AssetTypeEnum
from constants.chart_exchange import ChartExchangeEnum
from constants.intraday_interval import IntradayIntervalEnum
from feed.reduced_quotes_feed import ReducedQuotesFeed
#import nuvama_login
import pandas as pd
import time
import json
from flask import Flask, request
import threading
import datetime
import helper_nuvama as helper

apiKey = open("nuvama_api_key.txt",'r').read()
api_secret_password= open("nuvama_secret_key.txt").read()
url = "https://nuvamawealth.com/api-connect/login?api_key=" + apiKey
print(url)
requestId = open("nuvama_request_key.txt",'r').read()

api_connect = APIConnect(apiKey, api_secret_password, requestId, True)

intExpiry=helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
intExpiry_Fin = helper.getFinNiftyExpiryDate()
strikeList=[]
instrumentList = []

nifty_his = helper.getHistorical("NSE:Nifty 50", 1,1,"INDEX",api_connect)
a = (nifty_his['close'].iloc[-1])
#a = 22000

for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
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

banknifty_his = helper.getHistorical("NSE:Nifty Bank", 1,1,"INDEX",api_connect)
a = (banknifty_his['close'].iloc[-1])

#a = 48000

for i in range(-10, 10):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)

#Add CE
for strike in strikeList:
    ltp_option = "NFO:BANKNIFTY" + str(intExpiry_BN)+str(strike)+"CE"
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:BANKNIFTY" + str(intExpiry_BN)+str(strike)+"PE"
    instrumentList.append(ltp_option)

strikeList=[]
# FINNIFTY
finnifty_his = helper.getHistorical("NSE:Nifty Fin Service", 1,1,"INDEX",api_connect)
a = (finnifty_his['close'].iloc[-1])
#a = 22000

for i in range(-5, 5):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike+50)


#Add CE
for strike in strikeList:
    ltp_option = "NFO:FINNIFTY" + str(intExpiry_Fin)+str(strike)+"CE"
    instrumentList.append(ltp_option)

#Add PE
for strike in strikeList:
    ltp_option = "NFO:FINNIFTY" + str(intExpiry_Fin)+str(strike)+"PE"
    instrumentList.append(ltp_option)


token_list = []
token_symb_map = {}
ltp_dict = {}
symbol_list1 = [
               'NSE:SBICARD',
               'NSE:Nifty 50',
               'NSE:Nifty Bank',
                'NSE:Nifty Fin Service',
                # 'NFO:NIFTY23NOVFUT'
               ]

symbol_list =  symbol_list1 + instrumentList
print(symbol_list)

print("!! Started getltpDict.py !!")

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/ltp')
def getLtp():
    print(ltp_dict)
    ltp = -1
    instrumet = request.args.get('instrument')
    try:
        ltp = ltp_dict[instrumet]
    except Exception as e :
        print("EXCEPTION occured while getting ltpDict()")
        print(e)
    return str(ltp)

columns_to_select = ['exchangetoken', 'tradingsymbol', 'symbolname', 'description','assettype','exchange']
token = pd.read_csv('instruments\instruments.csv',usecols=columns_to_select, index_col=False)
print("TOKEN FILE ################################")
print(token)

def get_tradingSymbol_exchangeToken(symbol_list):
    
    for symbolname in symbol_list:
        exch = symbolname[:3]
        name = symbolname[4:]

        #print(token)
        exchangetoken = ""
        try:
            if name == "Nifty 50":
                exchangetoken = "-29"
            elif name == "Nifty Bank":
                exchangetoken = "-21"
            elif name == "Nifty Fin Service":
                exchangetoken = "-40"
            elif name == "NSE Midcap 100":
                exchangetoken = "-22"
            elif exch == "NSE":
                #for j in range(0,len(token)):
                #    if(token['symbolname'][j] == name) and (token['exchange'][j] == exch):
                #        exchangetoken = str(token['exchangetoken'][j])
                exchangetoken = str(token[(token['symbolname'] == name) & (token['exchange'] == exch)]['exchangetoken'].values[0])


            elif exch == "NFO" or exch == "MCX":
                #for j in range(0,len(token)):
                #    print(token['exchange'][j] , exch)
                #    if (token['exchange'][j] == exch):
                #        print(token['tradingsymbol'][j] , name)
                #        if(token['tradingsymbol'][j] == name) :
                #            print(name)
                #            exchangetoken = str(token['exchangetoken'][j])

                exchangetoken = str(token[(token['tradingsymbol'] == name) & (token['exchange'] == exch)]['exchangetoken'].values[0])
        except IndexError as e:
            print("Skipping", symbolname, name, exch)
        token_list.append(exchangetoken)
        token_symb_map[symbolname] = exchangetoken
        print(exchangetoken)
  
get_tradingSymbol_exchangeToken(symbol_list)
print(token_list)
time.sleep(1)

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4000)

t1 = threading.Thread(target=startServer)
t1.start()

quotes_streamer = api_connect.initReducedQuotesStreaming()

def callback(resp):
    resp = json.loads(resp)
    temp_token = resp['response']['data']['sym']
    temp_ltp = resp['response']['data']['ltp']

    for key, value in token_symb_map.items():
        if value == temp_token:
            ltp_dict[key] = float(temp_ltp)

    #ltp_dict[resp['response']['data']['sym']] = resp['response']['data']['ltp']
    print(ltp_dict)

quotes_streamer.subscribeReducedQuotesFeed(symbols = token_list,  callBack = callback)