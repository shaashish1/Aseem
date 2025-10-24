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

from breeze_connect import BreezeConnect
import urllib


######PIVOT POINTS##########################
####################__INPUT__#####################
api_key = "T64987#r17926343Q420~96^77V12T3n"
secret_key = "62579224n30z7s*926g2h37y1948o1d3"
session_key = "31798535"

###NO NEED TO ENTER ANYTHING HERE
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
breeze = BreezeConnect(api_key=api_key)
print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(api_key))

breeze.generate_session(api_secret=secret_key, session_token=session_key)
print(breeze)

with open("icici_api_key.txt", 'w') as file:
    file.write(api_key)
with open("icici_secret_key.txt", 'w') as file:
    file.write(secret_key)
with open("icici_session_key.txt", 'w') as file:
    file.write(session_key)

