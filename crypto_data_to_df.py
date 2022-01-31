"""
@aim: Convert data (.csv) from Binance to a dataframe to use in Pandas
Expecting data minute by minute from https://www.cryptodatadownload.com/data/binance/
They give headers:
unix	date	symbol	open	high	low	close	Volume BTC	Volume USDT	tradecount
We return a .csv with the header (date as Y-m-d H:M:S) and value at opening:
date value

@authors: Ivan-Daniel Sievering

@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
# Libraries
import os
import pandas as pd

# Constants
RAW_DATA_FOLDER = "crypto_data"
TREATED_DATA_FOLDER = "crypto_df"

# Parameters
filename = "Binance_XRPUSDT_minute.csv"
target_filename = "XRP_USD.csv"  # has to be crypto_money.csv

# --- Main --- #
if __name__ == "__main__":
    # Load the file
    df = pd.read_csv(os.path.join(RAW_DATA_FOLDER, filename), skiprows=1)  # first row is datasource
    print(df.sample(5))

    # Modify to our format
    df = df.drop(columns=["unix", "symbol", "high", "low", "close", "tradecount"])
    df = df.rename(columns={"open": "value"})
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop(df.columns[-1], axis=1)
    df = df.drop(df.columns[-1], axis=1)

    # Save the file
    df.to_csv(os.path.join(TREATED_DATA_FOLDER, target_filename), index=False)

    # Check the file
    df = pd.read_csv(os.path.join(TREATED_DATA_FOLDER, target_filename))
    print(df.sample(5))
