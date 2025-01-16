from datetime import date
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import nasdaqdatalink
import yfinance as yf

import pandas as pd
import nasdaqdatalink

def save_btc_datas():
    # Download historical data from Quandl
    df = nasdaqdatalink.get_table("QDL/BCHAIN", api_key='rRQgKH5b9t6Bmb1z81QE', paginate=True)
    df = df[df["code"] == "MKPRU"].reset_index()
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)
    df = df[df['value'] > 0]
    
    # Save as CSV
    df.to_csv("btc_data.csv", index=False)
    print("Data saved to btc_data.csv")

# To retrieve the data
def load_btc_datas():
    df = pd.read_csv("../data/BTC-USD.csv", parse_dates=['date'])
    print("Data loaded from btc_data.csv")
    return df

  
