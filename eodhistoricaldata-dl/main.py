import os
import json
import pandas as pd
from dotenv import dotenv_values

import endpoints

config = dotenv_values(".env")
api_key = config["API_KEY"]

# get a list of all tickers
exchange_code = "US"
#endpoints.get_all_tickers(exchange_code, api_key)

# create a tracking file
tracker = pd.read_csv("output/tickers.csv")
tracker = tracker[ tracker.Type == "Common Stock" ] 
tracker = tracker[["Code", "Name"]] 
tracker['retrieved_fundamentals'] = 0
tracker['retrieved_price'] = 0

tracker.to_csv("output/tracker.csv", index=False)

print(tracker.head())
print(tracker.shape)

# get data for each ticker
for index, row in tracker.iterrows():
    ticker = row['Code']

    if row['retrieved_fundamentals'] == 0:
        fundamentals = endpoints.get_fundamentals(ticker, api_key)

        os.mkdir(f"output/{index}")

        with open(f"output/{index}/fundamentals.json", "w") as f:
            json.dump(fundamentals, f)

        tracker.at[index, 'retrieved_fundamentals'] = 1

    if row['retrieved_price'] == 0:
        pass