#pip install urllib3==1.26.6
#pip install requests==2.26.0
#pip install APIConnect==2.0.0

from APIConnect.APIConnect import APIConnect
from constants.exchange import ExchangeEnum
from constants.order_type import OrderTypeEnum
from constants.product_code import ProductCodeENum
from constants.duration import DurationEnum
from constants.action import ActionEnum
import helper_nuvama as helper

apiKey = 's_kZYD4QpWaYyg'
api_secret_password= '7fS!il@sFGpc0ht0'
url = "https://nuvamawealth.com/api-connect/login?api_key=" + apiKey
#url = https://nuvamawealth.com/api-connect/login?api_key=s_kZYD4QpWaYyg
loginid = 45777021
print(url)
#requestId = input("Please add request id: ", )
requestId = ""

api_connect = APIConnect(apiKey, api_secret_password, requestId, True)
print(api_connect)
print(api_connect.Limits())

with open("nuvama_api_key.txt", 'w') as file:
    file.write(apiKey)
with open("nuvama_secret_key.txt", 'w') as file:
    file.write(api_secret_password)
with open("nuvama_request_key.txt", 'w') as file:
    file.write(requestId)