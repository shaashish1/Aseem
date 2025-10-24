import time
import csv
from fyers_apiv3 import fyersModel
import helper_fyers as helper
import datetime as dt

# Import access credentials from access_token.py
from access_token import client_id, access_token  # New Change

# Enable/Disable market hours validation
ENABLE_MARKET_HOURS = False  # Set to False to disable market hours restriction and Set to True to disable market hours restriction

start_time = dt.time(9, 15)
end_time = dt.time(15, 30)

if ENABLE_MARKET_HOURS:
    # Wait until market hours ⏳
    while True:
        current_time = dt.datetime.now().time()
        if not (start_time <= current_time <= end_time):
            print("⏳ Waiting for market hours (09:15 to 15:30)...")
            time.sleep(60)
        else:
            print("✅ Market hours are open!")
            break
else:
    print("⚠️ Market hours validation is DISABLED. Running script immediately.")

##############################################
#                   INPUT's                  #
##############################################

print("📡 Connecting to Fyers API...")
fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=client_id)

intExpiry = helper.getNiftyExpiryDate()
intExpiry_BN = helper.getBankNiftyExpiryDate()
intExpiry_Fin = helper.getFinNiftyExpiryDate()

strikeList = []
niftyList = []
bankNiftyList = []
finNiftyList = []

# NIFTY
print("📊 Fetching NIFTY data...")
data = {"symbols": "NSE:NIFTY50-INDEX"}
ltp = fyers.quotes(data=data)
a = ltp["d"][0]["v"]["lp"]
print(f"✅ NIFTY LTP: {a}")

for i in range(-20, 20):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike + 50)

niftyList.append("NSE:NIFTY50-INDEX")

for strike in strikeList:
    niftyList.append(f"NSE:NIFTY{intExpiry}{strike}CE")
    niftyList.append(f"NSE:NIFTY{intExpiry}{strike}PE")

strikeList = []
# BANKNIFTY
print("📊 Fetching BANKNIFTY data...")
data = {"symbols": "NSE:NIFTYBANK-INDEX"}
ltp = fyers.quotes(data=data)
a = ltp["d"][0]["v"]["lp"]

for i in range(-20, 20):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)

bankNiftyList.append("NSE:NIFTYBANK-INDEX")

for strike in strikeList:
    bankNiftyList.append(f"NSE:BANKNIFTY{intExpiry_BN}{strike}CE")
    bankNiftyList.append(f"NSE:BANKNIFTY{intExpiry_BN}{strike}PE")

strikeList = []
# FINNIFTY
print("📊 Fetching FINNIFTY data...")
data = {"symbols": "NSE:FINNIFTY-INDEX"}
ltp = fyers.quotes(data=data)
a = ltp["d"][0]["v"]["lp"]
print(f"✅ FINNIFTY LTP: {a}")

for i in range(-20, 20):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike + 50)

finNiftyList.append("NSE:FINNIFTY-INDEX")

for strike in strikeList:
    finNiftyList.append(f"NSE:FINNIFTY{intExpiry_Fin}{strike}CE")
    finNiftyList.append(f"NSE:FINNIFTY{intExpiry_Fin}{strike}PE")

print("✅ BELOW ARE THE COMPLETE INSTRUMENT LISTS")
print("📌 NIFTY Instruments:", niftyList)
print("📌 BANKNIFTY Instruments:", bankNiftyList)
print("📌 FINNIFTY Instruments:", finNiftyList)

##############################################
#              Save to Separate CSV Files    #
##############################################

file_map = {
    "NIFTY50": ("instrument_data_n2_nifty50.csv", niftyList),
    "BANKNIFTY": ("instrument_data_n2_banknifty.csv", bankNiftyList),
    "FINNIFTY": ("instrument_data_n2_finnifty.csv", finNiftyList),
}

for name, (filename, instrument_list) in file_map.items():
    print(f"💾 Saving {name} instrument data to {filename}...")

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Instrument", "LTP"])  # Write header

        for instrument in instrument_list:
            try:
                data = {"symbols": instrument}
                response = fyers.quotes(data=data)
                ltp = response["d"][0]["v"]["lp"] if "d" in response else "N/A"
                print(f"✅ {name} - {instrument}: {ltp}")
            except Exception as e:
                print(f"❌ Error fetching LTP for {instrument}: {e}")
                ltp = "Error ❌"

            writer.writerow([instrument, ltp])

    print(f"✅ Data saved successfully in {filename} 💾")

print("🚀 All data saved successfully!")
