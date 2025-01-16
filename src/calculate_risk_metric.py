from datetime import date
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import nasdaqdatalink
import yfinance as yf
from update_data import load_btc_datas
from update_data import load_crypto_datas
from tabulate import tabulate

def calculate_btc_risk_metric():
    df = load_btc_datas()
    # Add your risk metric calculation logic here
    # get data thats not in the quandl database
    new_data = yf.download(tickers='BTC-USD', start='2024-01-01', interval='1d', progress=False)
    new_data.reset_index(inplace=True)
    # restructure yf dataframe to match the quandl one
    new_data.rename(columns={'Date': 'date', 'Open': 'value'}, inplace=True)
    new_data = new_data[['date', 'value']]
    df = pd.concat([df, new_data], ignore_index=True)
    df.drop_duplicates(subset='date', keep='first', inplace=True)
    df.sort_values(by='date', inplace=True)
    btcdata = yf.download(tickers='BTC-USD', period='1d', interval='1m', progress=False)
    btcdata.reset_index(inplace=True)
    df = df.dropna(subset=['value'])
    df = df[['date', 'value']]
    diminishing_factor = 0.395
    moving_average_days = 365
    df['MA'] = df['value'].rolling(moving_average_days, min_periods=1).mean().dropna()
    df['Preavg'] = (np.log(df.value) - np.log(df['MA'])) * df.index**diminishing_factor
    df['avg'] = (df['Preavg'] - df['Preavg'].cummin()) / (df['Preavg'].cummax() - df['Preavg'].cummin())
    # Store results
    results = []
    results.append(['BTC-USD', df['date'].iloc[-1], df['value'].iloc[-1], df['MA'].iloc[-1], df['avg'].iloc[-1]])
    return results


def calculate_risk_metric(ticker, start_date):
  # Download data
  old_data = load_crypto_datas(ticker)
  last_date = old_data['date'].iloc[-1] 
  formatted_date = last_date.strftime("%Y-%m-%d")

  df = yf.download(tickers=ticker, start=formatted_date, interval='1d', progress=False)
  df.reset_index(inplace=True)
  df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
  if 'Open' in df.columns:
      df.rename(columns={'Date': 'date', 'Open': 'value'}, inplace=True)
  elif 'value' not in df.columns:
      raise KeyError("The required columns ('date', 'value') are not found in the DataFrame.")

  df = df[['date', 'value']].copy()
  df.sort_values(by='date', inplace=True)

  df = pd.concat([old_data, df], ignore_index=True)
  df.drop_duplicates(subset='date', keep='first', inplace=True)
  df.sort_values(by='date', inplace=True) 
  
  # Calculate moving average
  moving_average_days = 365
  df['MA'] = df['value'].rolling(moving_average_days, min_periods=1).mean()

  # Ensure no NaN values
  df = df.dropna().reset_index(drop=True)

  # Calculate Preavg
  diminishing_factor = 0.395
  df['Preavg'] = (np.log(df['value']) - np.log(df['MA'])) * (np.arange(len(df)) + 1) ** diminishing_factor
  df['avg'] = (df['Preavg'] - df['Preavg'].cummin()) / (df['Preavg'].cummax() - df['Preavg'].cummin())
  price_per_risk = {
    round(risk, 1):round(np.exp(
        (risk * (df['Preavg'].cummax().iloc[-1] - (cummin := df['Preavg'].cummin().iloc[-1])) + cummin) / df.index[-1]**diminishing_factor + np.log(df['MA'].iloc[-1])
    ))
    for risk in np.arange(0.0, 1.0, 0.1)
  }

   # Store results
  results = []
  results.append([ticker, df['date'].iloc[-1], df['value'].iloc[-1], df['MA'].iloc[-1], df['avg'].iloc[-1]])

  return results


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


if __name__ == "__main__":
    all_results = []
    btc_res = calculate_btc_risk_metric()
    all_results.extend(btc_res)


    for ticker, start_date in cryptos.items():
        alt_res = calculate_risk_metric(ticker, start_date)
        all_results.extend(alt_res)


    # Create a pandas DataFrame
    df_results = pd.DataFrame(all_results, columns=['ticker', 'date', 'value', 'MA', 'avg'])
    df_results['Risk to MA'] = ((df_results['MA'].astype(float) - df_results['value'].astype(float)) / df_results['value'].astype(float)) * 100

    # Round the 'value', 'MA', 'avg', and 'Risk to MA' columns to 2 decimal places
    for col in ['avg', 'Risk to MA']:
        df_results[col] = df_results[col].round(2)
    df_results = df_results.sort_values(by=['avg', 'Risk to MA'])

    # Display the DataFrame as a table
    styled_df = df_results.style.applymap(lambda x: 'color: green' if x < 0.5 else ('color: red' if x > 0.8 else ('color: orange' if 0.6 < x < 0.8 else ('color: blue' if x < 0.2 else ''))), subset=['avg'])
    print(styled_df)
    print(tabulate(df_results, headers='keys', tablefmt='psql'))