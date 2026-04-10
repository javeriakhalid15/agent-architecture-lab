from src.display import Displayable

class Agent(Displayable):
    """Abstract agent class - implements select_action method"""
    
    def initial_action(self, percept):
        """Return the initial action"""
        return self.select_action(percept)

    def select_action(self, percept):
        """Return the next action given percept"""
        raise NotImplementedError("Subclasses must implement select_action")


class Environment(Displayable):
    """Abstract environment class - implements do method"""
    
    def initial_percept(self):
        """Returns the initial percept for the agent"""
        raise NotImplementedError("Subclasses must implement initial_percept")

    def do(self, action):
        """Does the action in the environment, returns next percept"""
        raise NotImplementedError("Subclasses must implement do")


class Simulate(Displayable):
    """Simulator that chains agent and environment together"""
    
    def __init__(self, agent, environment):
        self.agent = agent
        self.env = environment
        self.percept = self.env.initial_percept()
        self.percept_history = [self.percept]
        self.action_history = []

    def go(self, n):
        """Run simulation for n time steps"""
        for i in range(n):
            action = self.agent.select_action(self.percept)
            self.display(2, f"i={i} action={action}")
            self.percept = self.env.do(action)
            self.display(2, f" percept={self.percept}")
            self.action_history.append(action)
            self.percept_history.append(self.percept)
        return self.percept_history