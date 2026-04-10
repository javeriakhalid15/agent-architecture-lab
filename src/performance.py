"""
Performance metrics for agent evaluation
Addresses Exercise 2.1 from page 6
"""
class PerformanceMetrics:
    """Collection of performance measures for fair agent comparison"""

    @staticmethod
    def average_cost(agent, env):
        """
        Simple average cost per time step
        WARNING: Unfair to agents that build inventory!
        """
        return agent.spent / env.time

    @staticmethod
    def inventory_adjusted_cost(agent, env):
        """
        Adjust cost by value of remaining inventory
        Fairer metric: agents aren't penalized for unused paper
        """
        final_stock_value = env.stock * env.price
        return (agent.spent - final_stock_value) / env.time

    @staticmethod
    def holding_cost_metric(agent, env, holding_rate=0.02):
        """
        Include holding costs for inventory over time
        Realistic metric that balances purchasing and storage
        """
        total_holding_cost = 0
        for stock_level in env.stock_history:
            total_holding_cost += stock_level * holding_rate
        return (agent.spent + total_holding_cost) / env.time

    @staticmethod
    def service_level(agent, env):
        """
        Measure how often stock ran out (stockout rate)
        Lower is better (0 = never out of stock)
        """
        stockouts = sum(1 for stock in env.stock_history if stock < 0)
        return stockouts / len(env.stock_history)

    @staticmethod
    def composite_score(agent, env, weights=None):
        """
        Weighted composite of multiple metrics
        weights: dict with keys 'cost', 'inventory', 'service'
        """
        if weights is None:
            weights = {'cost': 0.4, 'inventory': 0.3, 'service': 0.3}

        cost_score = PerformanceMetrics.average_cost(agent, env)
        inventory_score = PerformanceMetrics.inventory_adjusted_cost(agent, env)
        service_score = PerformanceMetrics.service_level(agent, env)

        return (weights['cost'] * cost_score +
                weights['inventory'] * abs(inventory_score) +
                weights['service'] * service_score * 1000)