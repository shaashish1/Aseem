import time
import datetime as dt
from fyers_apiv3 import fyersModel

# Read API credentials
app_id = open("fyers_client_id.txt", 'r').read().strip()
access_token = open("fyers_access_token.txt", 'r').read().strip()

# Initialize Fyers API
fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=app_id)

# Define the request payload
data = {
    "symbols": "NSE:NIFTY50-INDEX"
}

# Fetch LTP response
ltp = fyers.quotes(data=data)

# Print the entire response for debugging
print("LTP Full Response:", ltp)

# Safely extract the LTP value
try:
    if isinstance(ltp, dict) and 'd' in ltp and isinstance(ltp['d'], list) and len(ltp['d']) > 0:
        if 'v' in ltp['d'][0] and 'lp' in ltp['d'][0]['v']:
            a = ltp['d'][0]['v']['lp']
            print("LTP Value:", a)
        else:
            print("Unexpected structure in response:", ltp)
    else:
        print("Invalid response format:", ltp)
except Exception as e:
    print("Error extracting LTP:", e)
