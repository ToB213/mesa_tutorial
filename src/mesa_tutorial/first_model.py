import mesa
import numpy as np

class MoneyAgent(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def exchange(self):
        if self.wealth > 0:
            other_agent = self.random.choice(self.model.agents)

            other_agent.wealth += 1
            self.wealth -= 1

class MoneyModel(mesa.Model):
    def __init__(self, seed: int | None = None, n: int = 100):
        super().__init__(seed=seed)

        MoneyAgent.create_agents(model=self, n=n)

    def step(self):
        self.agents.shuffle_do("exchange")


if __name__ == "__main__":
    n = 100
    steps = 50
    seed = 42

    model = MoneyModel(seed=seed, n=n)

    for current_step in range(1, steps + 1):
        model.step()

        assert model.agents.agg("wealth", sum) == n

        print(f"Step {current_step} completed")
        print(f"Mean wealth: {model.agents.agg('wealth', np.mean)}")
        print(f"Max wealth: {model.agents.agg('wealth', np.max)}")
        print(f"Min wealth: {model.agents.agg('wealth', np.min)}")
        print(f"Std wealth: {model.agents.agg('wealth', np.std)}")
        print(f"Median wealth: {model.agents.agg('wealth', np.median)}")
