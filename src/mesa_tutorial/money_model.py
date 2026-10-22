import mesa


class MoneyAgent(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def exchange(self):
        if self.wealth > 0:
            other_agent = self.random.choice(self.model.agents)

            other_agent.wealth += 1
            self.wealth -= 1

    def report_status(self):
        return {
            "id": self.unique_id,
            "wealth": self.wealth,
        }


class MoneyModel(mesa.Model):
    def __init__(
        self,
        seed: int | None = None,
        n: int = 100,
        activation: str = "random",
    ):
        super().__init__(seed=seed)

        if activation not in ("random", "fixed"):
            raise ValueError(f"Unknown activation: {activation}")

        self.activation = activation

        MoneyAgent.create_agents(model=self, n=n)

    def step(self):
        if self.activation == "random":
            self.agents.shuffle_do("exchange")
        elif self.activation == "fixed":
            self.agents.do("exchange")
