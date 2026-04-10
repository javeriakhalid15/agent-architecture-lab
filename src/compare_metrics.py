"""
Compare different performance metrics
"""
from src.paper_env import TP_env
from src.simple_agent import SimplePaperAgent
from src.agents import Simulate
from src.performance import PerformanceMetrics

def evaluate_with_metrics(agent_class, env_class, n_steps=100):
    """Run agent and evaluate using all metrics"""
    env = env_class()
    agent = agent_class()

    sim = Simulate(agent, env)
    sim.display_level = 1
    sim.go(n_steps)

    results = {
        'average_cost': PerformanceMetrics.average_cost(agent, env),
        'inventory_adjusted': PerformanceMetrics.inventory_adjusted_cost(agent, env),
        'holding_cost': PerformanceMetrics.holding_cost_metric(agent, env),
        'service_level': PerformanceMetrics.service_level(agent, env),
        'composite': PerformanceMetrics.composite_score(agent, env),
        'final_stock': env.stock,
        'total_spent': agent.spent
    }
    return results

def compare_metrics():
    """Run comparison and print results"""
    print("\n" + "=" * 70)
    print("PERFORMANCE METRICS COMPARISON")
    print("=" * 70)

    results = evaluate_with_metrics(SimplePaperAgent, TP_env, n_steps=100)

    print(f"\n{'Metric':<30} {'Value':>15}")
    print("-" * 45)
    print(f"{'Average Cost per Step':<30} ${results['average_cost']:>12.2f}")
    print(f"{'Inventory-Adjusted Cost':<30} ${results['inventory_adjusted']:>12.2f}")
    print(f"{'Holding Cost Metric':<30} ${results['holding_cost']:>12.2f}")
    print(f"{'Service Level (Stockouts)':<30} {results['service_level']:>14.2%}")
    print(f"{'Composite Score':<30} {results['composite']:>15.2f}")
    print(f"\n{'Total Spent':<30} ${results['total_spent']:>12.2f}")
    print(f"{'Final Stock Level':<30} {results['final_stock']:>15} sheets")

    return results

if __name__ == "__main__":
    compare_metrics()