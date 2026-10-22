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

    def donate(self, recipients):
        if self.wealth < 3:
            return

        eligible = recipients.select(
            lambda agent: agent.wealth == 0
        )

        if len(eligible) == 0:
            return

        recipient = self.random.choice(eligible)
        recipient.wealth += 1
        self.wealth -= 1


class MoneyModel(mesa.Model):
    def __init__(
        self,
        seed: int | None = None,
        n: int = 100,
        activation: str = "random",
        redistribution: bool = False,
    ):
        super().__init__(seed=seed)

        if activation not in ("random", "fixed"):
            raise ValueError(f"Unknown activation: {activation}")

        self.activation = activation
        self.redistribution = redistribution

        MoneyAgent.create_agents(model=self, n=n)

    def step(self):
        if self.activation == "random":
            self.agents.shuffle_do("exchange")
        elif self.activation == "fixed":
            self.agents.do("exchange")

        if self.redistribution:
            rich = self.agents.select(
                lambda agent: agent.wealth >= 3
            )
            poor = self.agents.select(
                lambda agent: agent.wealth == 0
            )

            if len(rich) > 0 and len(poor) > 0:
                rich.shuffle_do("donate", recipients=poor)
