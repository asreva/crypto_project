"""
@aim: Implements an agent that does nothing
@authors: Ivan-Daniel Sievering
@date: 2022/01/31
"""

# --- Libraries, constants and parameters --- #
from CryptoAgent import CryptoAgent


# --- Class definition --- #
class SleepingAgent(CryptoAgent):
    """
    @aim: implements an agent that nothing
    @functions: - __init__ : initialise the agent
                - step : does nothing but needed because abstract function
                - load_init_info : loads nothing but needed because abstract function
                - others : see the parent class
    @parameters:- others : see the parent class
    """

    def __init__(self, name, crypto_name_l, init_money, init_repartition):
        """
        @aim: initialise the agent
        @input: - others : see the parent class
        """

        super().__init__(name, crypto_name_l, init_money, init_repartition)

    def step(self):
        """
        @aim: the agent does nothing
        """

        pass

    def load_init_info(self):
        """
        @aim: initialise the agent (needs nothing)
        """

        pass
