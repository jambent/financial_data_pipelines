import yfinance as yf
import pandas as pd
from datetime import datetime as dt

TICKER_LIST = [
    'EURUSD=X',
    'GBPUSD=X',
    'GBPEUR=X',
    'JPY=X',
    'GBP=X',
]

DATAFRAME_COLUMNS = [
    'Open',
    'High',
    'Low',
    'Close',
    'Volume',
    'Dividends',
    'Stock Splits',
    'Ticker']


BATCH_TIMES = [
    '06:00:00',
    '16:30:00',
    '20:00:00'
]

   

def load_fx_data(ticker_list):
    """
    Generates DataFrame containing FX data corresponding to
    latest,specific batch indicated in BATCH_TIMES

    Args:
        ticker_list: target yfinance FX tickers
    Returns:
        DataFrame containing FX data from latest batch 
    Raises:
        TypeError if ticker_list is not a list
    """
    if not isinstance(ticker_list, list):
        raise TypeError(
            ('ticker_list must be a list: fx tickers'))
    
    df = generate_empty_dataframe_for_fx_data(DATAFRAME_COLUMNS)
    
    target_batch_time = find_target_batch_time()
    
    for ticker in ticker_list:
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(period='1d', interval='30m')
        filtered_ticker_df = ticker_df.loc[[target_batch_time]]

        df = pd.concat([df, filtered_ticker_df])
    
    return df


def generate_empty_dataframe_for_fx_data(dataframe_columns):
    """
    Generates empty DataFrame to which FX data will be appended

    Args:
        dataframe_columns: column names for generated DataFrame
    Returns:
        Empty DataFrame with required column names 
    Raises:
        TypeError if dataframe_columns is not a list
    """
    if not isinstance(dataframe_columns, list):
        raise TypeError(
            ('dataframe_columns must be a list: fx DataFrame'))
    
    df = pd.DataFrame(columns=(dataframe_columns))
    return df


def find_target_batch_time():
    """
    Determine required batch time by comparing time when function invoked
    to list of required BATCH_TIMES, and select most recent BATCH_TIME

    Returns:
        String of required batch time, to match index format
        of yfinance DataFrame 
    """
    time_now = dt.now()
    date_today = str(time_now.date())

    batch_time_strings_today = [date_today + ' ' + batch_time for batch_time in BATCH_TIMES] 
    batch_time_dt_objects_today = [dt.strptime(batch_time_string, "%Y-%m-%d %H:%M:%S")
        for batch_time_string in batch_time_strings_today
    ]
    
    time_deltas = [(time_now - batch_time).seconds for batch_time in batch_time_dt_objects_today]

    batch_delta_record = dict(zip(time_deltas,batch_time_dt_objects_today))
    min_batch_delta = min(batch_delta_record)
    target_batch_string = str(batch_delta_record[min_batch_delta]) + '+00:00'
    
    return target_batch_string

    
    