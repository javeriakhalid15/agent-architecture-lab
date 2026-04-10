"""
Compare performance of different agent architectures
"""
from src.paper_env import TP_env
from src.simple_agent import SimplePaperAgent
from src.model_agent import ModelBasedPaperAgent
from src.enhanced_model_agent import EnhancedModelAgent
from src.agents import Simulate
from src.performance import PerformanceMetrics
import matplotlib.pyplot as plt

def run_agent_comparison(n_steps=100):
    """Run all agents and compare results"""
    agents = {
        'Simple Reflex': SimplePaperAgent(),
        'Model-Based': ModelBasedPaperAgent(),
        'Enhanced Model': EnhancedModelAgent()
    }

    results = {}
    histories = {}

    for name, agent in agents.items():
        print(f"\nRunning {name}...")
        env = TP_env()
        sim = Simulate(agent, env)
        sim.display_level = 1
        sim.go(n_steps)

        results[name] = {
            'avg_cost': PerformanceMetrics.average_cost(agent, env),
            'inv_adj_cost': PerformanceMetrics.inventory_adjusted_cost(agent, env),
            'service_level': PerformanceMetrics.service_level(agent, env),
            'final_stock': env.stock,
            'total_spent': agent.spent
        }

        histories[name] = {
            'price': env.price_history,
            'stock': env.stock_history,
            'purchases': agent.buy_history
        }

    return results, histories

def display_comparison(results):
    """Display comparison results in a formatted table"""
    print("\n" + "=" * 80)
    print("AGENT COMPARISON RESULTS")
    print("=" * 80)

    print(f"\n{'Agent Type':<20} {'Avg Cost':>12} {'Inv-Adj':>12} {'Service':>10} {'Final Stock':>12}")
    print("-" * 70)

    for name, metrics in results.items():
        print(f"{name:<20} ${metrics['avg_cost']:>10.2f} "
              f"${metrics['inv_adj_cost']:>10.2f} "
              f"{metrics['service_level']:>9.2%} "
              f"{metrics['final_stock']:>11}")

    print("\n" + "=" * 80)

    print("\n🏆 WINNERS:")
    best_cost = min(results.items(), key=lambda x: x[1]['avg_cost'])
    best_inv = min(results.items(), key=lambda x: x[1]['inv_adj_cost'])
    best_service = min(results.items(), key=lambda x: x[1]['service_level'])

    print(f"  Best Average Cost: {best_cost[0]} (${best_cost[1]['avg_cost']:.2f})")
    print(f"  Best Inventory-Adjusted: {best_inv[0]} (${best_inv[1]['inv_adj_cost']:.2f})")
    print(f"  Best Service Level: {best_service[0]} ({best_service[1]['service_level']:.2%} stockouts)")

def plot_comparison(histories):
    """Visualize agent behaviors"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    colors = {'Simple Reflex': 'blue', 'Model-Based': 'green', 'Enhanced Model': 'red'}

    # Plot 1: Price history
    ax = axes[0, 0]
    for name, history in histories.items():
        ax.plot(history['price'], label=name, color=colors[name], alpha=0.7)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Price ($)')
    ax.set_title('Price History (same for all agents)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: Stock levels
    ax = axes[0, 1]
    for name, history in histories.items():
        ax.plot(history['stock'], label=name, color=colors[name], alpha=0.7)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Stock Level (sheets)')
    ax.set_title('Inventory Levels by Agent')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)

    # Plot 3: Purchase quantities
    ax = axes[1, 0]
    for name, history in histories.items():
        ax.plot(history['purchases'], label=name, color=colors[name],
                alpha=0.7, marker='o', markersize=2)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Purchase Quantity')
    ax.set_title('Purchase Behavior by Agent')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: Cumulative spending
    ax = axes[1, 1]
    for name, history in histories.items():
        cumulative = []
        total = 0
        for i, buy in enumerate(history['purchases']):
            total += buy * histories[name]['price'][i] if i < len(histories[name]['price']) else 0
            cumulative.append(total)
        ax.plot(cumulative, label=name, color=colors[name], alpha=0.7)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Cumulative Spending ($)')
    ax.set_title('Total Cost Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/agent_comparison.png', dpi=150)
    plt.show()
    print("\nPlot saved to 'results/agent_comparison.png'")

if __name__ == "__main__":
    print("RUNNING AGENT COMPARISON...")
    print("This may take a moment...")
    results, histories = run_agent_comparison(n_steps=100)
    display_comparison(results)
    plot_comparison(histories)