import io 
import requests
import pandas as pd

def get_all_tickers(exchange_code, api_key):
    url = f"https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange_code}?api_token={api_key}"
    r = requests.get(url)

    df = pd.read_csv( io.StringIO(r.text) )

    df.to_csv("output/tickers.csv", index=False)

def get_fundamentals(ticker, api_key):
    url = f"https://eodhistoricaldata.com/api/fundamentals/AAPL.US?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX"
    r = requests.get(url)

    return r.json()

def get_eod_prices(ticker, api_key):
    url = f"https://eodhistoricaldata.com/api/eod/MCD.US?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX&period=d"
    r = requests.get(url)

    df = pd.read_csv( io.StringIO(r.text) )

    return df