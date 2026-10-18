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
    def wealth_group(agent):
        if agent.wealth == 0:
            return "Poor"
        elif agent.wealth <= 2:
            return "Middle"
        else:
            return "Rich"

    n = 100
    step = 50
    seed = 42

    model = MoneyModel(seed=seed, n=n)

    for _ in range(step):
        model.step()
        assert model.agents.agg("wealth", np.sum) == n

        groups = model.agents.groupby("ethnicity")

        for ethnicity, agents in groups:
            print(
                f"{ethnicity}, "
                f"N: {len(agents)}, "
                f"Average wealth: {agents.agg('wealth', np.mean):.2f}, "
                f"Poor agents: {len(agents.select(lambda agent: agent.wealth == 0))}"
            )

        cuont_wealth_group = model.agents.groupby(wealth_group).count()
        print(
            f"Poor: {cuont_wealth_group.get('Poor')}, "
            f"Middle: {cuont_wealth_group.get('Middle')}, "
            f"Rich: {cuont_wealth_group.get('Rich')}"
        )

        assert sum(model.agents.groupby('ethnicity').agg('wealth', np.sum).values()) == n
