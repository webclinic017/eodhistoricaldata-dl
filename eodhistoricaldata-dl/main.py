import os
import json
import datetime
import endpoints
import pandas as pd
from tqdm import tqdm
from dotenv import dotenv_values

config = dotenv_values(".env")
api_key = config["API_KEY"]
api_limit = 15

try:
    os.mkdir(f"output")
except:
    pass # already exists

print("🔎 Looking for an existing download.")

try:
    # If we are in the middle of another download
    with open("output/usage.json", "r") as f:
        usage = json.load(f)
    
    last_request = datetime.datetime.strptime(usage["dt"], "%Y-%m-%d %H:%M:%S.%f")
    
    if (datetime.datetime.now() - last_request).total_seconds() < 86400 and usage["count"] >= api_limit:
        # Don't need to do anything, the api_limit with trigger a break in the loop below.
        pass
    else:
        # reset counter
        print("Resuming download")

        now = datetime.datetime.now()
        usage = {"dt": str(now), "count": 0}
except:
    # First time we are running this script
    print("No existing download found, starting a new one.")

    now = datetime.datetime.now()
    usage = {"dt": str(now), "count": 0}

    with open("output/usage.json", "w") as f:
        json.dump(usage, f)

# see if tickers.csv exists in output
try:
    with open("output/tickers.csv", "r") as f:
        pass
except:
    # get a list of all tickers
    print("📃 Downloading tickers list.")

    exchange_code = "US"
    tickers_df = endpoints.get_all_tickers(exchange_code, api_key)
    tickers_df.to_csv("output/tickers.csv", index=False)

# see if tracker.csv exists in output
try:
    with open("output/tracker.csv", "r") as f:
        pass

    tracker = pd.read_csv("output/tracker.csv")
except:
    # create a tracking file
    tracker = pd.read_csv("output/tickers.csv")
    tracker = tracker[ tracker.Type == "Common Stock" ] 
    tracker = tracker[["Code", "Name"]] 
    tracker["retrieved_fundamentals"] = 0
    tracker["retrieved_price"] = 0
    tracker = tracker.reset_index(drop=True)

    tracker.to_csv("output/tracker.csv", index=False)

# get data for each ticker
for index, row in tqdm(tracker.iterrows(), total=tracker.shape[0]):
    ticker = row["Code"] + ".US"
    
    try:
        os.mkdir(f"output/{index}")
    except:
        pass # already exists
    
    if row["retrieved_fundamentals"] == 0 and usage["count"] < api_limit:
        fundamentals = endpoints.get_fundamentals(ticker, api_key)

        with open(f"output/{index}/fundamentals.json", "w") as f:
            json.dump(fundamentals, f)

        tracker.at[index, "retrieved_fundamentals"] = 1       
        tracker.to_csv("output/tracker.csv", index=False)
        
        usage["count"] += 1
        with open("output/usage.json", "w") as f:
            json.dump(usage, f)

    
    if row["retrieved_price"] == 0 and usage["count"] < api_limit:
        eod_prices = endpoints.get_eod_prices(ticker, api_key)
        eod_prices.to_csv(f"output/{index}/prices.csv", index=False)

        tracker.at[index, "retrieved_price"] = 1
        tracker.to_csv("output/tracker.csv", index=False)
        
        usage["count"] += 1
        with open("output/usage.json", "w") as f:
            json.dump(usage, f)

    if usage["count"] >= api_limit:
        print("🔴 Reached API limit for today.")
        break