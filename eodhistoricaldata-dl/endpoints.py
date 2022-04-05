import io 
import requests
import pandas as pd
from dotenv import dotenv_values

config = dotenv_values(".env")
api_key = config["API_KEY"]

def get_all_tickers(exchange_code, api_key):
    url = f"https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange_code}?api_token={api_key}"
    r = requests.get(url)

    df = pd.read_csv( io.StringIO(r.text) )

    df.to_csv("output/tickers.csv", index=False)

exchange_code = "US"
get_all_tickers(exchange_code, api_key)