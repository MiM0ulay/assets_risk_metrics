from datetime import date, datetime
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import nasdaqdatalink
import yfinance as yf

import pandas as pd
import nasdaqdatalink

cryptos = { 'ETH-USD':   '2016-01-01',
            'OM-USD' : '2020-09-01',
            'SOL-USD':   '2020-01-01',
            'BNB-USD':       '2017-01-01',
            'SUI20947-USD' : '2023-05-01',
            'MNT27075-USD' : '2023-08-01',
            'RNDR-USD' : '2020-07-01',
            'VIRTUAL-USD' : '2024-03-01',
            'TAO22974-USD' : '2023-03-01',
            'NEAR-USD' : '2020-11-01',
            'APT21794-USD' : '2022-11-01',
            'XRP-USD' : '2017-12-01',
            'LINK-USD' : '2017-12-01',
            'EUR=X' : '2003-12-01',
            'HNT-USD' : '2020-07-01',
            'AI16Z-USD': '2024-12-01',
            'UNI7083-USD' : '2020-10-01',

            }

def save_btc_datas(ticker, start_date):
    if(ticker == "BTC-USD"):
        # Download historical data from Yahoo Finance
        df = yf.download(ticker, start="2010-01-01", end=date.today())
        df.reset_index(inplace=True)
        df.to_csv("BTC-USD.csv", index=False)
        print("Data saved to BTC-USD.csv")
    else:
        df = yf.download(tickers=ticker, start=start_date, interval='1d', progress=False)
          # Reset the index and flatten column names (if needed)
        df.reset_index(inplace=True)

        # Handle multi-level columns (flatten them if they exist)
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

        # Debugging: Check flattened column names

        # Rename columns for consistency
        if 'Open' in df.columns:
            df.rename(columns={'Date': 'date', 'Open': 'value'}, inplace=True)
        elif 'value' not in df.columns:
            raise KeyError("The required columns ('date', 'value') are not found in the DataFrame.")

        # Keep necessary columns
        df = df[['date', 'value']].copy()

        # Sort by date
        df.sort_values(by='date', inplace=True)
        df.to_csv(f"../data/{ticker}.csv", index=False)


# To retrieve the data
def load_btc_datas():
    df = pd.read_csv("data/BTC-USD.csv", parse_dates=['date'])
    return df

def load_crypto_datas(ticker):
    df = pd.read_csv(f"data/{ticker}.csv", parse_dates=['date'])
    return df

  
if __name__ == "__main__":
    #for ticker, start_date in cryptos.items():
    #    save_btc_datas(ticker, start_date)

    for ticker in cryptos.keys():
        df = load_crypto_datas(ticker)
        print(ticker)
        print(df.head())
        # get the last date as string just the day

        last_date = df['date'].iloc[-1]
        # Convert the string to a datetime object
        formatted_date = last_date.strftime("%Y-%m-%d")
        print(formatted_date)