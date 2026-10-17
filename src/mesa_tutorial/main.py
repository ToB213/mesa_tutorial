import mesa

class MoneyAgent(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def exchange(self):
        if self.wealth > 0:
            other_agent = self.random.choice(list(self.model.agents))

            other_agent.wealth += 1
            self.wealth -= 1

class MoneyModel(mesa.Model):
    def __init__(self, seed: int | None = None, n: int = 10):
        super().__init__(seed=seed)

        MoneyAgent.create_agents(self, n)

    def step(self):
        self.agents.shuffle_do("exchange")

if __name__ == "__main__":
    all_wealth = []
    n = 100
    step = 300
    run = 100
    seed = 42

    for i in range(run):
        model = MoneyModel(seed = seed + i, n = n)

        for _ in range(step):
            model.step()

            assert sum(agent.wealth for agent in model.agents) == n

        for agent in model.agents:
            all_wealth.append(agent.wealth)

    import matplotlib.pyplot as plt
    import seaborn as sns

    # print the average wealth of all agents over all runs
    print(f"Average wealth: {sum(all_wealth) / len(all_wealth)}")

    sns.histplot(all_wealth, discrete=True, stat="probability")

    plt.title(f"Wealth Distribution of {n} Agents after {step} Steps over {run} Runs")
    plt.xlabel("Wealth")
    plt.ylabel("Probability")

    plt.savefig("figs/wealth_distribution.png")
    plt.close()
