"""
@aim: Code to run a full simulation of the agents in the market
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
# Libraries
import pandas as pd
from agents.SleepingAgent import SleepingAgent
from agents.WaitIncreaseAgent import WaitIncreaseAgent
from CryptoSimulation import CryptoSimulation

# Parameters
init_date = pd.to_datetime("2020-05-01 22:00:00")  # start one step before
end_date = pd.to_datetime("2020-06-01 23:00:00")  # stops one step before
crypto_list = ["BTC"]
frequency = 60 * 60 * 1  # in seconds

# --- Main --- #
if __name__ == "__main__":
    # Create the simulation
    simulation = CryptoSimulation(init_date, end_date, crypto_list, frequency=frequency)

    # Add the agents
    sleep_agent = SleepingAgent("sleeper", crypto_list, 100, {"BTC": 1.0})
    wait_agent = WaitIncreaseAgent("waiter", crypto_list, 100, {"BTC": 1.0}, "BTC", 3 / 100)
    simulation.add_agent(sleep_agent)
    simulation.add_agent(wait_agent)

    # Run the simulation
    simulation.simulate()

    # Evaluate it
    simulation.evaluate()
