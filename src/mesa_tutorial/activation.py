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
    def __init__(
        self,
        seed: int | None = None,
        n: int = 100,
        activation: str = "random",
    ):
        super().__init__(seed=seed)

        self.activation = activation

        MoneyAgent.create_agents(model=self, n=n)

    def step(self):
        if self.activation == "random":
            self.agents.shuffle_do("exchange")
        elif self.activation == "fixed":
            self.agents.do("exchange")
        else:
            raise ValueError(f"Unknown activation: {self.activation}")


def gini(wealth: list[int]) -> float:
    """Calculate the Gini coefficient of non-negative wealth."""
    arr = np.asarray(wealth, dtype=float)

    if arr.size == 0:
        raise ValueError("Wealth must not be empty")

    if np.any(arr < 0):
        raise ValueError("Wealth must be non-negative")

    total = np.sum(arr)

    if total == 0:
        return 0.0

    arr = np.sort(arr)
    n = len(arr)
    index = np.arange(1, n + 1)

    return float(np.sum((2 * index - n - 1) * arr) / (n * total))

from statistics import mean, pstdev

if __name__ == "__main__":
    n = 50
    steps = 100
    run = 50
    seed = 42

    results = {
        "fixed": [],
        "random": [],
    }

    for seed in range(run):
        for activation in results:
            model = MoneyModel(seed=seed, n=n, activation=activation)

            for _ in range(steps):
                model.step()

            wealth = model.agents.get("wealth")
            assert np.sum(wealth)  == n

            results[activation].append(gini(wealth))

    for activation, gini_values in results.items():
        print(
            f"Activation: {activation}, "
            f"Mean Gini: {mean(gini_values):.4f}, "
            f"Std Gini: {pstdev(gini_values):.4f}"
        )
