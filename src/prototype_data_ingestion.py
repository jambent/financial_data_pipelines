import yfinance as yf
from datetime import datetime as dt

target_time = dt.fromisoformat('2023-11-28T16:30:00Z')

ticker_list = [
    'GBPUSD=X',
    'GBPEUR=X'
]
for ticker in ticker_list:
    ticker_data = yf.Ticker(ticker)
    df = ticker_data.history(period='1d', interval='15m')
    filtered_df = df.loc[[target_time]]
    print(filtered_df.head(24))
