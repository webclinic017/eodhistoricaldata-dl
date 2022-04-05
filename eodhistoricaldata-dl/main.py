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
except:
    # if this is the first time we are running this script
    now = datetime.datetime.now()
    usage = {"dt": str(now), "req": 0}

    with open("output/usage.json", "w") as f:
        json.dump(usage, f)

last_request = datetime.datetime.strptime(usage["dt"], "%Y-%m-%d %H:%M:%S.%f")
total_requests = usage["req"]

# if last_request was more than 24 hours ago, reset the counter
if (datetime.datetime.now() - last_request).total_seconds() > 86400:
    total_requests = 0
else:
    quit()
    
print(1)

# get a list of all tickers
exchange_code = "US"
#tickers_df = endpoints.get_all_tickers(exchange_code, api_key)
#tickers_df.to_csv("output/tickers.csv", index=False)

# create a tracking file
tracker = pd.read_csv("output/tickers.csv")
tracker = tracker[ tracker.Type == "Common Stock" ] 
tracker = tracker[["Code", "Name"]] 
tracker['retrieved_fundamentals'] = 0
tracker['retrieved_price'] = 0
tracker = tracker.reset_index(drop=True)

tracker.to_csv("output/tracker.csv", index=False)

print(tracker.head())
print(tracker.shape)

# get data for each ticker
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

    if row['retrieved_price'] == 0:
        eod_prices = endpoints.get_eod_prices(ticker, api_key)
        eod_prices.to_csv(f"output/{index}/prices.csv", index=False)

        tracker.at[index, 'retrieved_price'] = 1
    
    tracker.to_csv("output/tracker.csv", index=False)