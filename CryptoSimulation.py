"""
@aim: Implements a class that simulates the evolution of agents inside a crypto market
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
# Libraries
from CryptoMarket import CryptoMarket
from CryptoAPI import CryptoAPI
from datetime import timedelta


# --- Class definition --- #
class CryptoSimulation:
    """
    @aim: implements the simulation class that will at each step update its prices and calls the agent
          At the end it displays the performance of each agent
    @functions: - __init__ : initialise the simulation
                - add_agent : add a new agent to the simulation
                - step : does a step in the simulation
                - simulate : run the whole simulation
    @parameters:- init_date : first date of the simulation (included)
                - end_date : last date of the simulation (included)
                - current_date : date of the simulation at this step
                - market : market object from the market class to get price
                - api : api object from the api class to get the transaction
                - agent_l : list of all the agents in the simulation
                - currency : currency used to make the money transaction
                - frequency : nb of seconds between step
                - verbose : display or not text in the simulation
    """

    def __init__(self, init_date, end_date, crypto_name_l, imposition_rate=0.01,
                 currency="USD", frequency=60, verbose=True, crypto_folder="crypto_df"):
        """
        @aim: initialise the simulation
        @input: - init_date : first date of the simulation (included)
                - end_date : last date of the simulation (included)
                - crypto_name_l : list of the crypto to consider in the simulation
                - imposition_rate : tax from the API
                - currency : currency used to make the money transaction
                - frequency : frequency at which the simulation increments (in seconds)
                - verbose : display or not text in the simulation
                - crypto_folder : name of the folder with the df of the crypto price evolution
        """

        # Instantiate all the parameters of the simulation
        self.init_date = init_date
        self.end_date = end_date
        self.current_date = init_date
        self.crypto_name_l = crypto_name_l
        self.currency = currency
        self.frequency = frequency
        self.verbose = verbose
        self.agent_l = {}

        # Create the marker and the API
        self.market = CryptoMarket(crypto_name_l, init_date, end_date, currency, crypto_folder)
        self.api = CryptoAPI(self, imposition_rate)

        if verbose:
            print("Simulation will be executed from the {} to the {}".format(init_date, end_date))
            print("The following cryptos will be considered {}".format(crypto_name_l))

    def add_agent(self, agent):
        """
        @aim: add an agent in the simulation
        @input: - agent : agent object (from the agent class) to add in the simulation
        """

        # Add it in the dict
        self.agent_l[agent.name] = agent
        # Link it to this simulation
        self.agent_l[agent.name].link_to_simulation(self)

    def step(self):
        """
        @aim: makes a step in the simulation (size of the step depends on self -> frequency)
        """

        # Update the date (first step skipped -> ok to init agents with first day values)
        self.current_date = self.current_date + timedelta(seconds=self.frequency)

        # Execute agents steps
        for name, agent in self.agent_l.items():
            agent.step()

    def simulate(self):
        """
        @aim: run the whole simulation (start to end date)
        """

        print("Simulation starts\n")

        # Run the simulation
        while self.current_date < self.end_date:
            self.step()

        print("Simulation ended.")


# --- Main (just to test and see how it works) --- #
if __name__ == "__main__":
    import pandas as pd
    from agents.SleepingAgent import SleepingAgent
    from agents.WaitIncreaseAgent import WaitIncreaseAgent

    # Init the simulation
    init_date_test = pd.to_datetime("2020-05-01 22:00:00")
    end_date_test = pd.to_datetime("2020-05-03 23:00:00")
    simulation = CryptoSimulation(init_date_test, end_date_test, ["BTC"])

    # Add the agents
    sleep_agent = SleepingAgent("sleeper", ["BTC"], 100, {"BTC": 1})
    wait_agent = WaitIncreaseAgent("waiter", ["BTC"], 100, {"BTC": 1}, "BTC", 1/100)
    simulation.add_agent(sleep_agent)
    simulation.add_agent(wait_agent)

    print("\nInitial state")
    for cur_agent in simulation.agent_l.values():
        print(cur_agent.name)
        print(cur_agent.available_money)
        print(cur_agent.available_crypto_l)

    # Run the simulation
    simulation.simulate()

    print("\nFinal state")
    for cur_agent in simulation.agent_l.values():
        print(cur_agent.name)
        print(cur_agent.available_money)
        print(cur_agent.available_crypto_l)
