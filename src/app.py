import streamlit as st
import pandas as pd

from calculate_risk_metric import calculate_btc_risk_metric, calculate_risk_metric

cryptos = { 'ETH-USD':   '2016-01-01',
'OM-USD' : '2020-09-01',
'SOL-USD':   '2020-01-01',
'BNB-USD':   '2017-01-01',
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

def main():
    st.title("Cryptocurrency Risk Metrics")

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


    # Display the table
    st.write("Risk Metrics for Cryptocurrencies")
    st.table(df_results)

if __name__ == "__main__":
    main()







