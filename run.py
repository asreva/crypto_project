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
init_date = pd.to_datetime("2020-05-01 22:00:00")
end_date = pd.to_datetime("2020-06-01 23:00:00")

# --- Main --- #
if __name__ == "__main__":
    # Create the simulation
    simulation = CryptoSimulation(init_date, end_date, ["BTC"])

    # Add the agents
    sleep_agent = SleepingAgent("sleeper", ["BTC"], 100, {"BTC": 1})
    wait_agent = WaitIncreaseAgent("waiter", ["BTC"], 100, {"BTC": 1}, "BTC", 5.0/100)
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
