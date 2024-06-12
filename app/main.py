import os
import boto3
import pandas as pd
import yfinance as yf
from multiprocessing import Pool
import tempfile
from functools import partial
from utils.dynamo_functions import send_to_health_check
from datetime import datetime, timedelta


def parallelize(items, function, n_process=os.cpu_count()):
    if n_process > 1:
        with Pool(n_process) as pool:
            tmp = pool.map(function, items)
    else:
        tmp = [item for item in items]
    return tmp
    
def download_yesterday_data(symbol):
    try:
        data = yf.download(symbol, period="1d")
        data["Symbol"] = symbol
    except KeyError:
        print(f"No existe el ticker {symbol}, se continua con el siguiente..")
        data = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Adj Close", "Volume", "Symbol"])
        return data
         
    return data
        

def upload_to_s3(data, bucket_name, path, temppath):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url=os.getenv("ENDPOINT_URL"),
        region_name='us-east-1'
    )
    s3.upload_file(Filename=temppath, Bucket=bucket_name, Key=path)

if __name__ == "__main__":
    try:
        bucket_name = "financial-data"
        yesterday = datetime.now() - timedelta(days=1)
        year, month, day = yesterday.strftime("%Y"), yesterday.strftime("%m"), yesterday.strftime("%d")

        path = f"{year}/{month}/{day}/yesterday_data.parquet"


        symbols = pd.read_html("https://www.cboe.com/us/equities/market_statistics/listed_symbols/")
        symbols = symbols[0]["Symbol"].to_list()
        
        
        data = parallelize(symbols, download_yesterday_data)
        
        data = pd.concat(data)
        
        # Save data to a file before uploading
        temppath = f"{tempfile.gettempdir()}/yesterday_data.parquet"
        data.to_parquet(temppath)

        upload_to_s3(data, bucket_name, path, temppath)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_to_health_check(now, 0, "Download data succesfully", 
                             os.getenv("AWS_ACCESS_KEY_ID"), 
                             os.getenv("AWS_SECRET_ACCESS_KEY"),
                             os.getenv("ENDPOINT_URL"))
    except Exception as e:
        send_to_health_check(now, 1, f"Download data failed. Error: {e}", 
                             os.getenv("AWS_ACCESS_KEY_ID"), 
                             os.getenv("AWS_SECRET_ACCESS_KEY"),
                             os.getenv("ENDPOINT_URL"))
