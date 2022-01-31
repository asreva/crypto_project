"""
@aim: Implements the generic class of an agent interacting with the crypto market
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
# Libraries
import sys
from abc import ABC, abstractmethod


# --- Class definition --- #
class CryptoAgent(ABC):
    """
    @aim: implements the CryptoAgent class (template to create agent that will buy/sell crypto)
    @functions: - __init__ : initialise the agent
                - link_to_simulation : link the agent to the simulation
                - step : decision of the agent on one step (i.e. 1 minute)
                - buy : action for the agent to buy crypto
                - sell : action for the agent to sell crypto
                - load_init_info : to add information before launching the simulation (for example, previous values)
    @parameters:- name : name of the agent (str)
                - available_crypto_l : dict with the qte of each crypto that the agent has
                - available_money : money that the agent has
                - earned_money : money that the agent has earned (will never be used again)
                - init_money : money that the agent has at the beginning
                - init_repartition : initial repartition of the money along cryptos
                                    [0.75, 0.1] means 75% in the first crypto, 10% in the second and 15% still in money
                - simulation : ref to the current simulation (to get prices, api, ...)

    """

    def __init__(self, name, crypto_name_l, init_money, init_repartition):
        """
        @aim: initialise the agent
        @input: - name : name of the agent (str)
                - crypto_name_l : list of all the crypto to consider by this agent
                - init_money : money that the agent has at the beginning
                - init_repartition : dict of initial repartition of the money along cryptos
                                    ["BTC":0.75, "BTT":0.1] means 75% in the BTC, 10% in BTT and 15% still in money
        """

        self.name = name

        self.available_crypto_l = dict(zip(crypto_name_l, [0] * len(crypto_name_l)))
        self.available_money = init_money
        self.earned_money = 0
        self.init_repartition = init_repartition

        self.simulation = None

        print("CryptoAgent {} ready!".format(self.name))

    def link_to_simulation(self, simulation):
        """
        @aim: create the links between the agent and the simulation (and the API), also buys the first crypto
        @input: - simulation : the simulation class that host the agent
        """

        # Create links
        self.simulation = simulation

        # Buy initial crypto
        for crypto_name in self.available_crypto_l.keys():
            self.buy(self.available_money * self.init_repartition[crypto_name], crypto_name)

        self.load_init_info()

    @abstractmethod
    def step(self):
        """
        @aim: implements the decision to make on a specific step (has to be implemented for the specific agent)
        """

        print("Agent step has to be implemented.")
        sys.exit()

    def buy(self, money, crypto_name):
        """
        @aim: buy for a certain amount of crypto (deal with removing money and adding crypto)
        @input: - money : quantity of money to invest
                - crypto_name : name of the crypto
        """

        # Check that it as money to do so
        if money <= self.available_money:
            # Buy crypto to API and modify intern variables
            crypto_qte = self.simulation.api.buy_crypto_from_api(money, crypto_name)
            self.available_money -= money
            self.available_crypto_l[crypto_name] += crypto_qte
        else:
            print("Agent {} is trying to buy more than it has money.".format(self.name))
            sys.exit()

    def sell(self, crypto_qte, crypto_name):
        """
        @aim: sell for a certain amount of crypto (deal with adding money and removing crypto)
        @input: - crypto_qte : quantity of crypto to sell
                - crypto_name : name of the crypto
        """

        # Check that it has crypto to do so
        if crypto_qte <= self.available_crypto_l[crypto_name]:
            # Sell crypto to API and modify intern variables
            money = self.simulation.api.sell_crypto_to_api(crypto_qte, crypto_name)
            self.available_crypto_l[crypto_name] -= crypto_qte
            self.available_money += money
        else:
            print("Agent {} is trying to sell more than it has {}.".format(self.name, crypto_name))
            sys.exit()

    @abstractmethod
    def load_init_info(self):
        """
        @aim: get some specific information from the simulation after linking (to implement if needed)
        """

        print("No specific initialisation needed.")


# --- Main (just to test and see how it works) --- #
if __name__ == "__main__":
    import datetime
    import pandas as pd
    from CryptoMarket import CryptoMarket
    from CryptoAPI import CryptoAPI

    # Init the market
    init_date_test = pd.to_datetime("2021-10-27 22:00:00")
    end_date_test = pd.to_datetime("2021-10-27 23:00:00")
    request_date_test = pd.to_datetime("2021-10-27 22:30:00")

    # Create a fake simulation class just for the example
    class Simulation:
        def __init__(self, current_date):
            self.market = CryptoMarket(["BTC"], init_date_test, end_date_test, currency="USD")
            self.api = CryptoAPI(self, imposition_rate=0.01)
            self.current_date = current_date
            self.agent = None

        def add_agent(self, agent):
            self.agent = agent
            self.agent.link_to_simulation(self)

        def step(self):
            self.current_date = self.current_date + datetime.timedelta(seconds=60)
            self.agent.step()


    # Init the simulation
    simulation_test = Simulation(request_date_test)

    # Implement a very simple agent that sells, then buys, than does nothing then sells, then buys, ..
    class TestAgent(CryptoAgent, ABC):
        def __init__(self, name, crypto_name_l, init_money, init_repartition):
            super().__init__(name, crypto_name_l, init_money, init_repartition)
            self.state = 0

        def step(self):
            # Always sell and buy the first crypto
            name_of_crypto = list(self.available_crypto_l.keys())[-1]

            if self.state == 0:  # sell all the first crypto
                self.sell(self.available_crypto_l[name_of_crypto], name_of_crypto)
                self.state = 1
            elif self.state == 1:
                self.buy(self.available_money, name_of_crypto)
                self.state = 2
            else:
                self.state = 0

        def load_init_info(self):
            print("Not needed")


    test_agent = TestAgent("Test", ["BTC"], 100, {"BTC": 1})
    simulation_test.add_agent(test_agent)

    print("\nInitial state")
    print(simulation_test.agent.available_money)
    print(simulation_test.agent.available_crypto_l)

    for i in range(0, 10):
        simulation_test.step()
        print("\nStep {}".format(i))
        print(simulation_test.agent.available_money)
        print(simulation_test.agent.available_crypto_l)
