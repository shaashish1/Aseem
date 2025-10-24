
# https://ttblaze.iifl.com/apimarketdata/instruments/indexlist?exchangeSegment=1
import threading
from datetime import datetime
import json
import pandas as pd
from flask import Flask, request
from Connect import XTSConnect
from MarketDataSocketClient import MDSocket_io

# Interactive API Credentials
API_KEY = "8dd7065e19e4c3316f1419"
API_SECRET = "Axfu658#Rw"
userID = "GURUSANT"

with open("iifl_api_key.txt", 'w') as file:
    file.write(API_KEY)
with open("iifl_secret_key.txt", 'w') as file:
    file.write(API_SECRET)
with open("user_id.txt", 'w') as file:
    file.write(userID)