"""
@aim: Implements an agent that waits for the price to increase in order to sell (and directly buys again)
@warning: only implemented to work on one crypto at the time
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
from CryptoAgent import CryptoAgent


# --- Class definition --- #
class WaitIncreaseAgent(CryptoAgent):
    """
    @aim: implements a naive agent that only sells when a fixed percentage of improvement has been reached and
    reinvest all directly. Only works on one crypto.
    @functions: - __init__ : initialise the agent
                - step : check if the percentage of increase is interesting enough, if yes sells and buys again
                - load_init_info : get the initial price of the crypto
                - others : see the parent class
    @parameters:- name_of_crypto : name of the crypto to consider (only works on one)
                - sell_th : sell threshold (in perc) to sell the crypto
                - others : see the parent class
    """

    def __init__(self, name, crypto_name_l, init_money, init_repartition, name_of_crypto, sell_th):
        """
        @aim: initialise the agent
        @input: - name_of_crypto : name of the crypto to consider (only works on one)
                - sell_th : sell threshold (in perc) to sell the crypto
                - others : see the parent class
        """

        super().__init__(name, crypto_name_l, init_money, init_repartition)
        self.name_of_crypto = name_of_crypto
        self.sell_th = sell_th
        self.last_buy_price = None

    def step(self):
        """
        @aim: the agent sells everything if the value augmented more than the threshold, and buys again all directly
        """

        # Get the price and compute the difference
        current_price = self.simulation.market.get_price(self.name_of_crypto, self.simulation.current_date)
        perc_diff = (current_price - self.last_buy_price) / self.last_buy_price

        # if it increased sell and buy again
        if perc_diff > self.sell_th:
            self.sell(self.available_crypto_l[self.name_of_crypto], self.name_of_crypto)
            self.buy(self.available_money, self.name_of_crypto)
            self.last_buy_price = current_price

    def load_init_info(self):
        """
        @aim: initialise the agent by getting the first buy price
        """

        self.last_buy_price = self.simulation.market.get_price(self.name_of_crypto, self.simulation.current_date)
