"""
@aim: Code to run a full simulation of the agents in the market
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
# Libraries
import pandas as pd
from CryptoSimulation import CryptoSimulation
from agents.SleepingAgent import SleepingAgent
from agents.WaitIncreaseAgent import WaitIncreaseAgent
from agents.SlopeEstimationAgent import SlopeEstimationAgent

# Parameters
init_date = pd.to_datetime("2020-01-01 00:00:00")  # start one step before
end_date = pd.to_datetime("2021-01-01 00:00:00")  # stops one step before
crypto_list = ["BTC"]
frequency = 60 * 1 * 1  # in seconds

# Agents
agent_list = [
    SleepingAgent("Sleeper", crypto_list, 100, {"BTC": 1.0}),
    # WaitIncreaseAgent("Wait", crypto_list, 100, {"BTC": 1.0}, "BTC", 2.031 / 100),
    SlopeEstimationAgent("Sloper", crypto_list, 100, {"BTC": 1.0}, "BTC", 2.5 / 100, -0.5 / 100, 45, 120)
]

# --- Main --- #
if __name__ == "__main__":
    # Create the simulation
    simulation = CryptoSimulation(init_date, end_date, crypto_list, frequency=frequency)

    # Add the agents
    for agent in agent_list:
        simulation.add_agent(agent)

    # Run the simulation
    simulation.simulate()

    # Evaluate it
    simulation.evaluate()
