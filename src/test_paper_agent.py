"""
Test script for paper buying agent
"""
from src.paper_env import TP_env
from src.simple_agent import SimplePaperAgent
from src.agents import Simulate

def test_simple_agent():
    print("=" * 60)
    print("TESTING SIMPLE PAPER BUYING AGENT")
    print("=" * 60)

    env = TP_env()
    agent = SimplePaperAgent()

    sim = Simulate(agent, env)
    sim.display_level = 2
    sim.go(20)

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Total money spent: ${agent.spent:.2f}")
    print(f"Average cost per step: ${agent.spent / env.time:.2f}")
    print(f"Final stock level: {env.stock} sheets")
    print(f"Final price: ${env.price}")

    return agent, env

if __name__ == "__main__":
    test_simple_agent()