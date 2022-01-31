"""
@aim: Implements a class that simulates a crypto API (take taxes in input and output)
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""


# --- Class definition --- #
class CryptoAPI:
    """
    @aim: implements the crypto API class (to sell/buy crypto)
    @functions: - __init__ : initialise the API
                - buy_crypto_from_api : buy a certain amount of crypto from the API
                - sell_crypto_to_api: sell a certain amount of crypto to the API
    @parameters:- market : market object from the simulation (to get the value of the crypto)
                - imposition_rate : percentage of money kept by the API
    """

    def __init__(self, simulation, imposition_rate=0.01):
        """
        @aim: initialise the API
        @input: - simulation : simulation to which belongs the API (to get the date and the market)
                - imposition_rate : imposition rate of the API
        """

        self.simulation = simulation
        self.imposition_perc = 1 - imposition_rate
        print("API created!")

    def buy_crypto_from_api(self, money, crypto_name):
        """
        @aim: buy for a certain amount of money crypto
        @input: - money : for how much money buy
                - crypto_name : name of the crypto that we want to buy
        @output:  quantity of crypto that we get
        """

        money *= self.imposition_perc
        crypto_qte = money / self.simulation.market.get_price(crypto_name, self.simulation.current_date)
        return crypto_qte

    def sell_crypto_to_api(self, crypto_qte, crypto_name):
        """
        @aim: sell a certain amount of crypto for money
        @input: - crypto_qte : quantity of crypto that we want to sell
                - crypto_name : name of the crypto that we want to sell
        @output:  money that we get back
        """

        money = crypto_qte * self.simulation.market.get_price(crypto_name, self.simulation.current_date)
        money *= self.imposition_perc
        return money


# --- Main (just to test and see how it works) --- #
if __name__ == "__main__":
    import pandas as pd
    from CryptoMarket import CryptoMarket

    # Init the market
    init_date_test = pd.to_datetime("2021-10-27 22:00:00")
    end_date_test = pd.to_datetime("2021-10-27 23:00:00")
    market_test = CryptoMarket(["BTC"], init_date_test, end_date_test, currency="USD")
    request_date_test = pd.to_datetime("2021-10-27 22:30:00")

    # Create a fake simulation class just for the example
    class Simulation:
        def __init__(self, market, current_date):
            self.market = market
            self.current_date = current_date

    # Init the simulation
    simulation_test = Simulation(market_test, request_date_test)

    # Init the API
    api = CryptoAPI(simulation_test, imposition_rate=0.01)

    # Make a test
    print("\nBTC price: {}\n".format(market_test.get_price("BTC", request_date_test)))

    print("Money earned when selling 1 BTC {}".format(api.sell_crypto_to_api(1, "BTC")))
    print("Money earned when selling 2 BTC {}".format(api.sell_crypto_to_api(2, "BTC")))
    print("Money earned when selling 0.5 BTC {}".format(api.sell_crypto_to_api(0.5, "BTC")))
    print("Money earned when selling 1/0.99 BTC {}".format(api.sell_crypto_to_api(1 / 0.99, "BTC")))

    print("\nBTC earned with 1 dollar {}".format(api.buy_crypto_from_api(1, "BTC")))
    print("BTC earned with 2 dollar {}".format(api.buy_crypto_from_api(2, "BTC")))
    print("BTC earned with 0.5 dollar {}".format(api.buy_crypto_from_api(0.5, "BTC")))
    print("BTC earned with 1/0.99 dollar {}".format(api.buy_crypto_from_api(1 / 0.99, "BTC")))
