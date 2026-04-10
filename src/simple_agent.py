"""
Simple reflex agent for paper buying
"""
from src.agents import Agent

class SimplePaperAgent(Agent):
    """Reflex agent that buys based on current stock only"""

    def __init__(self):
        self.spent = 0
        self.buy_history = []
        self.last_price = None

    def select_action(self, percept):
        price = percept['price']
        instock = percept['instock']
        self.last_price = price

        if instock < 10:
            tobuy = 20    # Emergency buy
        elif instock < 20:
            tobuy = 10    # Normal restock
        elif price < 200:
            tobuy = 5     # Good price
        else:
            tobuy = 0     # Price too high

        self.spent += tobuy * price
        self.buy_history.append(tobuy)
        return {'buy': tobuy}