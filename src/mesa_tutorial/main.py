import mesa
import numpy as np

class MoneyAgent(mesa.Agent):
    def __init__(self, model, ethnicity):
        super().__init__(model)
        self.wealth = 1
        self.ethnicity = ethnicity

    def exchange(self):
        if self.wealth > 0:
            other_agent = self.random.choice(list(self.model.agents))

            other_agent.wealth += 1
            self.wealth -= 1

class MoneyModel(mesa.Model):
    def __init__(self, seed: int | None = None, n: int = 100):
        super().__init__(seed=seed)

        ethnicities = ["Green", "Blue", "Mixed"]

        MoneyAgent.create_agents(
            model=self,
            n=n,
            ethnicity=self.random.choices(ethnicities, k=n),
        )

    def step(self):
        self.agents.shuffle_do("exchange")

if __name__ == "__main__":
    n = 100
    step = 50
    seed = 42

    model = MoneyModel(seed=seed, n=n)

    for _ in range(step):
        model.step()
        assert model.agents.agg("wealth", sum) == n

        poor_agents = model.agents.select(
            lambda agent: agent.wealth == 0
        )

        blue_agents = model.agents.select(
            lambda agent: agent.ethnicity == "Blue"
        )

        blue_average_wealth = blue_agents.agg("wealth", np.mean)

        max_wealth = model.agents.agg("wealth", np.max)

        rich_green_agents = len(model.agents.select(
            lambda agent: agent.ethnicity == "Green" and agent.wealth >= 3
        ))

        print(
            f"Step: {_+1}, "
            f"Poor agents: {len(poor_agents)}, "
            f"Blue average wealth: {blue_average_wealth:.2f}, "
            f"Max wealth: {max_wealth}, "
            f"Rich green agents: {rich_green_agents}"
        )
