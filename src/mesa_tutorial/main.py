import mesa
import numpy as np

class MoneyAgent(mesa.Agent):
    def __init__(self, model, ethnicity):
        super().__init__(model)
        self.wealth = 1
        self.ethnicity = ethnicity

    def exchange(self):
        if self.wealth > 0:
            other_agent = self.random.choice(self.model.agents)

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


def wealth_group(agent):
    if agent.wealth == 0:
        return "Poor"
    elif agent.wealth <= 2:
        return "Middle"
    else:
        return "Rich"


if __name__ == "__main__":
    n = 100
    steps = 50
    seed = 42

    model = MoneyModel(seed=seed, n=n)

    for current_step in range(1, steps + 1):
        model.step()

        assert model.agents.agg("wealth", sum) == n

        print(f"Step {current_step} completed")

    groups = model.agents.groupby("ethnicity")

    for ethnicity, agents in groups:
        print(
            f"{ethnicity}, "
            f"N: {len(agents)}, "
            f"Average wealth: {agents.agg('wealth', np.mean):.2f}, "
            f"Poor agents: {len(agents.select(lambda agent: agent.wealth == 0))}"
        )

    count_wealth_group = model.agents.groupby(wealth_group).count()

    print(
        f"Poor: {count_wealth_group.get('Poor', 0)}, "
        f"Middle: {count_wealth_group.get('Middle', 0)}, "
        f"Rich: {count_wealth_group.get('Rich', 0)}"
    )

    top5 = model.agents.sort("wealth").select(at_most=5)

    for rank, agent in enumerate(top5, start=1):
        print(
            f"Top {rank}, "
            f"Agent id: {agent.unique_id}, "
            f"Ethnicity: {agent.ethnicity}, "
            f"Wealth: {agent.wealth}"
        )

    worst5 = (
        model.agents
        .sort("wealth", ascending=True)
        .select(at_most=5)
    )

    for rank, agent in enumerate(worst5, start=1):
        print(
            f"Worst {rank}, "
            f"Agent id: {agent.unique_id}, "
            f"Ethnicity: {agent.ethnicity}, "
            f"Wealth: {agent.wealth}"
        )

    assert sum(model.agents.groupby("ethnicity").agg("wealth", sum).values()) == n

    total_before = model.agents.agg("wealth", sum)

    poor_agents = model.agents.select(lambda agent: agent.wealth == 0)

    subsidy_count = len(poor_agents)

    poor_agents.set("wealth", 1)

    total_after = model.agents.agg("wealth", sum)
    print(f"Distributed subsidy: {total_after - total_before}")

    assert total_after - total_before == subsidy_count
    assert len(model.agents.select(lambda agent: agent.wealth == 0)) == 0
