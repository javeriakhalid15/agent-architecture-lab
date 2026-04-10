"""
Model-based agent that maintains internal state and estimates trends
Based on TP_agent from page 5
"""
from src.agents import Agent

class ModelBasedPaperAgent(Agent):
    """
    Agent that maintains:
    - Running average of prices (exponential smoothing)
    - Spending tracking
    - Stock level awareness
    """

    def __init__(self):
        self.spent = 0
        self.buy_history = []
        self.avg_price = None
        self.last_price = None
        self.instock = None
        self.price_history = []

    def select_action(self, percept):
        """Decision using internal model (page 5, lines 61-75)"""
        self.last_price = percept['price']
        self.instock = percept['instock']

        # Update running average with exponential smoothing (α = 0.05)
        if self.avg_price is None:
            self.avg_price = self.last_price
        else:
            self.avg_price = self.avg_price + (self.last_price - self.avg_price) * 0.05

        self.price_history.append(self.last_price)

        # Buy in bulk when price is 10% below average AND stock is low
        if self.last_price < 0.9 * self.avg_price and self.instock < 60:
            tobuy = 48   # Bulk purchase
        elif self.instock < 12:
            tobuy = 12   # Emergency restock
        else:
            tobuy = 0    # Hold

        self.spent += tobuy * self.last_price
        self.buy_history.append(tobuy)
        return {'buy': tobuy}

    def get_statistics(self):
        """Return agent statistics for analysis"""
        return {
            'avg_price': self.avg_price,
            'total_spent': self.spent,
            'total_bought': sum(self.buy_history),
            'num_purchases': len([b for b in self.buy_history if b > 0])
        }