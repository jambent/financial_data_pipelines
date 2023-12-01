import yfinance as yf
import pandas as pd
from awswrangler import s3
from datetime import datetime as dt

def lambda_handler(event,context):
    target_time = dt.fromisoformat('2023-12-01T14:30:00Z')

    ticker_list = [
    'EURUSD=X',
    'GBPUSD=X',
    'GBPEUR=X',
    'JPY=X',
    'GBP=X',
    ]

    df = pd.DataFrame(columns= ('Open','High','Low','Close','Volume','Dividends','Stock Splits','Currency Pair'))

    for ticker in ticker_list:
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(period='1d', interval='15m')
        filtered_ticker_df = ticker_df.loc[[target_time]]

        ticker_components = ticker.split('=')
        currency_one = ''
        currency_two = ''
        if len(ticker_components[0]) == 3:
            currency_one = 'USD'
            currency_two = ticker_components[0]
        else:
            currency_one = ticker_components[0][:3]
            currency_two = ticker_components[0][3:]
        currency_pair = currency_one + '/' + currency_two
        filtered_ticker_df['Currency Pair'] = currency_pair

        df= pd.concat([df,filtered_ticker_df])

    parquet_filename = target_time + 'FX.parquet' 
    path = f's3://landing-bucket/{parquet_filename}'
    s3.to_parquet(df=df,
                path=path)
    #df.to_parquet('df.parquet')
#print(df.head())
