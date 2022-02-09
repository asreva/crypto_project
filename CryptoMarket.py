"""
@aim: Implements a class that simulates the crypto market based on historical data (from the formatted df)
Assumes that the
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
# Libraries
import os
import sys
import pandas as pd


# --- Class definition --- #
class CryptoMarket:
    """
    @aim: implements the crypto market class
    @functions: - __init__ : initialise the market
                - get_price : get the price on a specific date
    @parameters:- all_df_dict : dictionary containing the df for each crypto
    """

    def __init__(self, crypto_name_l, init_date, end_date, currency="USD", crypto_folder="crypto_df"):
        """
        @aim: initialise the market
        @input: - crypto_name_l: list of the name of the cryptos to consider (BTC/...)
                - init_date, end_date: start and end date of the simulation (pd.datetime format)
                - currency: official money to consider (USD/...)
                - crypto_folder: name of the folder containing the saved df in OUR format (see crypto_data_to_df.py)
        """

        df_list = []

        # For each crypto create the filename (crypto+currency) and load the df
        for crypto_name in crypto_name_l:
            try:
                # get the df
                crypto_file = crypto_name + "_" + currency + ".csv"
                df = pd.read_csv(os.path.join(crypto_folder, crypto_file))
                df["date"] = pd.to_datetime(df["date"])
                # restrain in the correct dates
                df = df[df["date"] >= init_date]
                df = df[df["date"] <= end_date]
                df_list.append(df)
            except FileNotFoundError:
                print("{} with currency {} not found in the df.".format(crypto_name, currency))
                sys.exit()

        # Convert to dict
        self.all_df_dict = dict(zip(crypto_name_l, df_list))

        print("Market created!")

    def get_price(self, crypto_name, date):
        """
        @aim: get the price of a crypto on a specific date
        @input: - crypto_name : name of the crypto
                - date : date of the request
        @output:  price of this crypto at that moment
        """

        try:
            df = self.all_df_dict[crypto_name]
            row = df[df["date"] == date].iloc[0]  # .iloc[0] to get only the value and not the cell
            return row["value"]
        except IndexError:
            print("{} of {} was not found in the dataframe".format(date, crypto_name))
            return False

    def get_crypto_df(self, crypto_name):
        """
        @aim: get the dataframe of a specific crypto for plot purposes
        @input: - crypto_name : name of the crypto
        @output:  the dataframe
        """

        return self.all_df_dict[crypto_name]


# --- Main (just to test and see how it works) --- #
if __name__ == "__main__":
    init_date_test = pd.to_datetime("2021-10-27 22:00:00")
    end_date_test = pd.to_datetime("2021-10-27 23:00:00")
    request_date_test = pd.to_datetime("2021-10-27 22:30:00")

    market = CryptoMarket(["BTC", "BTT"], init_date_test, end_date_test, currency="USD")

    print("\n{}".format(market.get_price("BTC", request_date_test)))
    print(market.get_price("BTT", request_date_test))
