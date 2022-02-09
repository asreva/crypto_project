"""
@aim: Implements an agent that looks for the slope of the data to decide to buy or not
@warning: only implemented to work on one crypto at the time
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
from CryptoAgent import CryptoAgent
from collections import deque
from scipy.stats import linregress
import numpy as np


# --- Class definition --- #
class SlopeEstimationAgent(CryptoAgent):
    """
    @aim: ???
    @functions: ???
    @parameters: ???
    """

    def __init__(self, name, crypto_name_l, init_money, init_repartition, name_of_crypto, sell_th, buy_th, slope_th, memory_size):
        """
        @aim: initialise the agent
        @input: - name_of_crypto : name of the crypto to consider (only works on one)
                - sell_th : sell threshold (in perc) to sell the crypto (compared to sell price)
                - buy_th : buy threshold (in perc) to buy to crypto (compared to buy price)
                - slope_th : threshold of the slope (in perc) to consider that we are at a maxima
                - memory_size : nb of samples to keep in memory
                - others : see the parent class
        """

        super().__init__(name, crypto_name_l, init_money, init_repartition)
        self.name_of_crypto = name_of_crypto
        self.sell_th = sell_th
        self.buy_th = buy_th
        self.slope_th = slope_th
        self.last_transaction_price = None
        self.enough_data_gathered = False  # at the beginning the algo does not have enough information
        self.memory = []  # memory of the previous values of the agent (element [0] is the oldest and [-1] the newest)
        self.mode = "has_to_sell"
        self.memory_size = memory_size

    def step(self):
        """
        @aim: ???
        """

        # Get the price
        current_price = self.simulation.market.get_price(self.name_of_crypto, self.simulation.current_date)

        # Check that enough data has been accumulated
        if not self.enough_data_gathered:
            # if this is not the case, just store data
            self.memory.append(current_price)
            self.enough_data_gathered = len(self.memory) >= self.memory_size
        else:
            # if enough data, add the new information and remove the old one
            memory_tmp = deque(self.memory)
            memory_tmp.popleft()
            memory_tmp.append(current_price)
            self.memory = memory_tmp

            # compute the current slope
            perc_diff = (current_price - self.last_transaction_price) / self.last_transaction_price
            lr = linregress(np.arange(self.memory_size), self.memory)
            angle_lr = 360*np.arctan(lr.slope)/(2*np.pi)

            if self.mode == "has_to_sell":
                if perc_diff > self.sell_th and angle_lr < -self.slope_th:
                    self.last_transaction_price = current_price
                    self.sell(self.available_crypto_l[self.name_of_crypto], self.name_of_crypto)
                    self.mode = "has_to_buy"
                    if self.simulation.verbose:
                        print("Sell action by {} on {} (slope {})".format(self.name, self.simulation.current_date, angle_lr))
            elif self.mode == "has_to_buy":
                if perc_diff < self.buy_th and angle_lr > self.slope_th:
                    self.last_transaction_price = current_price
                    self.buy(self.available_money, self.name_of_crypto)
                    self.mode = "has_to_sell"
                    if self.simulation.verbose:
                        print("Buy action by {} on {} (slope {})".format(self.name, self.simulation.current_date, angle_lr))

    def load_init_info(self):
        """
        @aim: initialise the agent by getting the first buy price
        """

        self.last_transaction_price = self.simulation.market.get_price(self.name_of_crypto,
                                                                       self.simulation.current_date)
        self.memory.append(self.last_transaction_price)
