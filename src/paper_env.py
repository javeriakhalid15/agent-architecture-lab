"""
Paper buying environment implementation
Based on Example 2.1 from Poole and Mackworth [2023]
"""
import random
import math
from src.agents import Environment

class TP_env(Environment):
    """Paper buying environment with stochastic price and consumption"""
    
    price_delta = [0, 0, 0, 21, 0, 20, 0, -64, 0, 0, 23, 0, 0, 0, -35,
                   0, 76, 0, -41, 0, 0, 0, 21, 0, 5, 0, 5, 0, 0, 0, 5]
    sd = 5

    def __init__(self):
        self.time = 0
        self.stock = 20
        self.stock_history = []
        self.price_history = []
        self.price = None

    def initial_percept(self):
        self.stock_history.append(self.stock)
        self.price = round(234 + self.sd * random.gauss(0, 1))
        self.price_history.append(self.price)
        return {'price': self.price, 'instock': self.stock}

    def select_from_dist(self, distribution):
        rand_val = random.random()
        cumulative = 0
        for value, prob in distribution.items():
            cumulative += prob
            if rand_val < cumulative:
                return value
        return list(distribution.keys())[-1]

    def do(self, action):
        used = self.select_from_dist({6: 0.1, 5: 0.1, 4: 0.1, 3: 0.3, 2: 0.2, 1: 0.2})
        bought = action.get('buy', 0)
        self.stock = self.stock + bought - used
        self.stock_history.append(self.stock)
        self.time += 1
        delta_index = self.time % len(self.price_delta)
        self.price = round(self.price + self.price_delta[delta_index] +
                          self.sd * random.gauss(0, 1))
        self.price_history.append(self.price)
        return {'price': self.price, 'instock': self.stock}