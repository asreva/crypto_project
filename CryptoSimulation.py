"""
@aim: Implements a class that simulates the evolution of agents inside a crypto market
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import seaborn as sns
from CryptoMarket import CryptoMarket
from CryptoAPI import CryptoAPI
from datetime import timedelta

sns.set(style="whitegrid")


# --- Class definition --- #
class CryptoSimulation:
    """
    @aim: implements the simulation class that will at each step update its prices and calls the agent
          At the end it displays the performance of each agent
    @functions: - __init__ : initialise the simulation
                - add_agent : add a new agent to the simulation
                - step : does a step in the simulation
                - simulate : run the whole simulation
                - evaluate : evaluates the different agent and calls other functions to plot the performances
                    - plot_summary_table : summary of the benefice / qte of each crypto
                    - plot_money_evolution : plot the evolution of the money that the agent accumulated
                    - plot_crypto_qte_evolution : plot the evolution of the qte of each crypto that the agent has
                    - plot_crypto_market_evolution : plot the evolution of the price of the crypto
                    - add_agent_actions : adds to some axis a line indicating that an agent did an action
    @parameters:- init_date : first date of the simulation (included)
                - end_date : last date of the simulation (included)
                - current_date : date of the simulation at this step
                - market : market object from the market class to get price
                - api : api object from the api class to get the transaction
                - agent_l : list of all the agents in the simulation
                - currency : currency used to make the money transaction
                - frequency : nb of seconds between step
                - verbose : display or not text in the simulation
                - crypto_name_l : list of the crypto that are used in the simulation
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
        # Add the initial state
        self.agent_l[agent.name].add_state(self.current_date, "start", "-", "-")

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

        # Run the simulation (check that next step in frequency will before or at the end date)
        while self.current_date + timedelta(seconds=self.frequency - 1) <= self.end_date:
            self.step()

        # Save the end state of each agent
        for agent in self.agent_l.values():
            agent.add_state(self.current_date, "end", "-", "-")

        print("Simulation ended.")

    def plot_summary_table(self, axis, color_agent_dict):
        """
        @aim: print a summary table with the initial money of each agent and its final balance
        @input: - axis : axis on which print the results
                - color_agent_dict : dict of color associated to each agent
        """

        # Prepare the axis and the table
        axis.axis("off")
        row_labels = ["Total Value", "Init Value", "Balance", "Money", "Earned Money"]
        for crypto_name in self.crypto_name_l:
            row_labels.append(crypto_name)
        col_labels = []
        for agent in self.agent_l.values():
            col_labels.append(agent.name)
        cell_text = np.zeros((len(row_labels), len(col_labels)))

        # Fill the table array
        for i, agent in enumerate(self.agent_l.values()):
            cell_text[0, i] = agent.state_hist[-1]["total_value"]
            cell_text[1, i] = agent.init_money
            cell_text[2, i] = agent.state_hist[-1]["total_value"] - agent.init_money
            cell_text[3, i] = agent.state_hist[-1]["available_money"]
            cell_text[4, i] = agent.state_hist[-1]["earned_money"]
            for j, crypto_name in enumerate(self.crypto_name_l):
                cell_text[5 + j, i] = agent.state_hist[-1]["available_cryptos"][crypto_name]

        # Print the array in the table
        table = axis.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels, cellLoc='center',
                           loc='upper center',
                           rowColours=["lightgrey"] * len(row_labels),
                           colColours=["lightgrey"] * len(col_labels), bbox=(0, 0, 1, 1))

        # Add the title and the color of each agent
        axis.set_title('Final performance of the agents.')
        for i, agent in enumerate(self.agent_l.values()):
            table[(0, i)].set_facecolor(color_agent_dict[agent.name])

    def plot_money_evolution(self, axis, color_agent_dict, history_agent_df_dict):
        """
        @aim: show the evolution of the money that each agent possess
        @input: - axis : axis on which print the results
                - color_agent_dict : dict of color associated to each agent
                - history_agent_df_dict : a dict giving for each agent a dataframe containing the state of each one
        """

        # Plot for each agent the evolution
        for agent_name, agent_df in history_agent_df_dict.items():
            sns.lineplot(data=agent_df, ax=axis, x="date", y="total_value", linestyle="solid",
                         color=color_agent_dict[agent_name])
            sns.lineplot(data=agent_df, ax=axis, x="date", y="available_money", linestyle="dashed",
                         color=color_agent_dict[agent_name])
            sns.lineplot(data=agent_df, ax=axis, x="date", y="earned_money", linestyle="dotted",
                         color=color_agent_dict[agent_name])

        # Add the tile and axis
        axis.set_title("Real money value along time")
        axis.set_xlabel("Date")
        axis.set_ylabel("Value in {}".format(self.currency))

        # Add the legend
        legend_patch_l = [Line2D([0], [0], color="grey", label='Available', linestyle='dashed'),
                          Line2D([0], [0], color="grey", label='Earned', linestyle='dotted'),
                          Line2D([0], [0], color="grey", label='Value')]
        axis.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=legend_patch_l)

    def plot_crypto_qte_evolution(self, axis_l, color_agent_dict, history_agent_df_dict):
        """
        @aim: show the evolution of the qte of crypto of each agent
        @input: - axis_l : list of axis on which print the results (has to be the same nb as the nb of crypto)
                - color_agent_dict : dict of color associated to each agent
                - history_agent_df_dict : a dict giving for each agent a dataframe containing the state of each one
        """

        # For each agent and crypto display the evolution
        for j, crypto_name in enumerate(self.crypto_name_l):
            for i, agent in enumerate(self.agent_l.values()):
                sns.lineplot(data=history_agent_df_dict[agent.name], ax=axis_l[j], x="date", y=crypto_name,
                             label=agent.name, color=color_agent_dict[agent.name])

            axis_l[j].set_xlabel("Date")
            axis_l[j].set_title("Evolution of qte of {} along time".format(crypto_name))
            axis_l[j].set_ylabel("{} in {}".format(crypto_name, self.currency))

    def plot_crypto_market_evolution(self, axis_l):
        """
        @aim: show the evolution of the price of the crypto of each agent (has to be the same nb as the nb of crypto)
        @input: - axis_l : list of axis on which print the results (has to be the same nb as the nb of crypto)
        """

        # For each crypto show the price evolution
        for j, crypto_name in enumerate(self.crypto_name_l):
            df_crypto = self.market.get_crypto_df(crypto_name)
            df_crypto["date"] = pd.to_datetime(df_crypto["date"])
            sns.lineplot(data=df_crypto, ax=axis_l[j], x=df_crypto["date"], y=df_crypto["value"])

            axis_l[j].set_xlabel("Date")
            axis_l[j].set_title("Value of {} along time".format(crypto_name))
            axis_l[j].set_ylabel("Qte {}".format(crypto_name))

    def add_agent_actions(self, axis_l, color_agent_dict, history_agent_df_dict):
        """
        @aim: adds vertical lines to indicate the action of an agent on this date and the kind of action
        @input: - axis_l : list of axis on which print the actions
                - color_agent_dict : dict of color associated to each agent
                - history_agent_df_dict : a dict giving for each agent a dataframe containing the state of each one
        """

        # For each axis print the action of each agent
        for j, ax in enumerate(axis_l):
            for i, agent in enumerate(self.agent_l.values()):
                for _, action_row in history_agent_df_dict[agent.name].iterrows():
                    if action_row["action_type"] == "buy" \
                            and self.crypto_name_l[j // 2] in action_row["action_crypto"]:
                        ax.axvline(x=action_row["date"], linestyle='dotted', color=color_agent_dict[agent.name])
                    if action_row["action_type"] == "sell" and \
                            self.crypto_name_l[j // 2] in action_row["action_crypto"]:
                        ax.axvline(x=action_row["date"], linestyle='dashed', color=color_agent_dict[agent.name])
                    if action_row["action_type"] == "both" and \
                            self.crypto_name_l[j // 2] in action_row["action_crypto"]:
                        ax.axvline(x=action_row["date"], color=color_agent_dict[agent.name])

            # Add the legend on the axis
            legend_patch_l = [Line2D([0], [0], color="grey", label='Sell', linestyle='dashed'),
                              Line2D([0], [0], color="grey", label='Buy', linestyle='dotted'),
                              Line2D([0], [0], color="grey", label='Both')]
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=legend_patch_l)

    def evaluate(self):
        """
        @aim: evaluates the different agent and calls other functions to plot the performances
                - plot_summary_table : summary of the benefice / qte of each crypto
                - plot_money_evolution : plot the evolution of the money that the agent accumulated
                - plot_crypto_qte_evolution : plot the evolution of the qte of each crypto that the agent has
                - plot_crypto_market_evolution : plot the evolution of the price of the crypto
                - add_agent_actions : adds to some axis a line indicating that an agent did an action
        """

        # Define the general figure
        eval_fig, eval_axs = plt.subplots(2 + 2 * len(self.crypto_name_l),
                                          sharex="all")  # table, all money, 2 plot for each crypto
        eval_fig.suptitle('Simulation results')

        # Associate a color to each agent
        colors = cm.rainbow(np.linspace(0, 1, len(self.agent_l)))
        color_agent_dict = {}
        for i, agent in enumerate(self.agent_l.values()):
            color_agent_dict[agent.name] = colors[i]

        # Prepare the history of actions of each agent
        history_agent_df_dict = {}
        for i, agent in enumerate(self.agent_l.values()):
            # Convert the list of dict of this agent to a df
            agent_hist = agent.state_hist
            df_tmp = pd.DataFrame.from_dict(agent_hist)

            # Explode the list of available cryptos to different columns
            df_tmp[self.crypto_name_l] = df_tmp["available_cryptos"].apply(pd.Series)

            # If sell and bought at the same point, only take the last one
            duplicated_mask = df_tmp["date"].duplicated(keep=False)  # take all duplicates
            df_tmp.loc[duplicated_mask, "action_type"] = "both"
            df_tmp = df_tmp.drop_duplicates(subset="date", keep="last")

            # Add the df to the dict
            history_agent_df_dict[agent.name] = df_tmp

        # Plots
        self.plot_summary_table(eval_axs[0], color_agent_dict)
        self.plot_money_evolution(eval_axs[1], color_agent_dict, history_agent_df_dict)
        self.plot_crypto_qte_evolution([eval_axs[2 + 2 * i] for i in range(0, len(self.crypto_name_l))],
                                       color_agent_dict, history_agent_df_dict)
        self.plot_crypto_market_evolution([eval_axs[3 + 2 * i] for i in range(0, len(self.crypto_name_l))])
        self.add_agent_actions(eval_axs[2:], color_agent_dict, history_agent_df_dict)

        # Format the figure
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gca().set_xlim([self.init_date, self.end_date])
        plt.gca().tick_params(rotation=15)
        plt.show()
