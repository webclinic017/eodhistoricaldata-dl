import os
import json
import datetime
import endpoints
import pandas as pd
from dotenv import dotenv_values

config = dotenv_values(".env")
api_key = config["API_KEY"]

try:
    os.mkdir(f"output")
except:
    pass # already exists

try:
    # If we are in the middle of another download
    with open("output/usage.json", "r") as f:
        usage = json.load(f)
    
    last_request = datetime.datetime.strptime(usage["dt"], "%Y-%m-%d %H:%M:%S.%f")
    
    if (datetime.datetime.now() - last_request).total_seconds() < 86400 and usage["count"] > 10000:
        print("Already downloaded today")
        exit()
except:
    # First time we are running this script
    now = datetime.datetime.now()
    usage = {"dt": str(now), "count": 0}

    with open("output/usage.json", "w") as f:
        json.dump(usage, f)

total_requests = usage["count"]

# see if tickers.csv exists in output
try:
    with open("output/tickers.csv", "r") as f:
        pass
except:
    # get a list of all tickers
    exchange_code = "US"
    tickers_df = endpoints.get_all_tickers(exchange_code, api_key)
    tickers_df.to_csv("output/tickers.csv", index=False)

# create a tracking file
tracker = pd.read_csv("output/tickers.csv")
tracker = tracker[ tracker.Type == "Common Stock" ] 
tracker = tracker[["Code", "Name"]] 
tracker['retrieved_fundamentals'] = 0
tracker['retrieved_price'] = 0
tracker = tracker.reset_index(drop=True)

tracker.to_csv("output/tracker.csv", index=False)

# get data for each ticker
while usage["count"] < 10000:

    for index, row in tracker.iterrows():
        ticker = row['Code'] + ".US"
        
        try:
            os.mkdir(f"output/{index}")
        except:
            pass # already exists
        
        if row['retrieved_fundamentals'] == 0:
            fundamentals = endpoints.get_fundamentals(ticker, api_key)

            with open(f"output/{index}/fundamentals.json", "w") as f:
                json.dump(fundamentals, f)

            tracker.at[index, 'retrieved_fundamentals'] = 1
            usage["count"] += 1
            
            tracker.to_csv("output/tracker.csv", index=False)
        
            with open("output/usage.json", "w") as f:
                json.dump(usage, f)

        
        if row['retrieved_price'] == 0:
            eod_prices = endpoints.get_eod_prices(ticker, api_key)
            eod_prices.to_csv(f"output/{index}/prices.csv", index=False)

            tracker.at[index, 'retrieved_price'] = 1
            usage["count"] += 1

            tracker.to_csv("output/tracker.csv", index=False)

            with open("output/usage.json", "w") as f:
                json.dump(usage, f)
