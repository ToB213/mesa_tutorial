from statistics import mean, pstdev

from money_model import MoneyModel
from metrics import gini


def tax_agent(agent):
    """Collect one unit of tax from agents with wealth >= 5."""
    if agent.wealth >= 5:
        agent.wealth -= 1

def run_experiment(
    n: int,
    steps: int,
    seed: int,
    redistribution: bool,
    activation: str = "random"
):
    model = MoneyModel(
        n=n,
        seed=seed,
        activation=activation,
        redistribution=redistribution,
    )

    for _ in range(steps):
        model.step()

        wealth = model.agents.get("wealth")

        assert len(wealth) == n
        assert sum(wealth) == n
        assert all(w >= 0 for w in wealth)

    wealth = model.agents.get("wealth")

    return {
        "poor": len(
            model.agents.select(
                lambda agent: agent.wealth == 0
            )
        ),
        "gini": gini(wealth),
        "wealth": wealth,
    }

def main():
    n = 50
    steps = 100
    runs = 50
    base_seed = 42
    activations = [
        "random",
        "fixed",
        "simultaneous"
    ]

    for redistribution in (False, True):
        for activation in activations:
            results = [
                run_experiment(
                    n=n,
                    steps=steps,
                    seed=base_seed + i,
                    redistribution=redistribution,
                    activation=activation,
                )
                for i in range(runs)
            ]

            poor = [result["poor"] for result in results]
            gini_values = [result["gini"] for result in results]

            print(
                f"Redistribution: {redistribution}, Activation: {activation}, "
                f"Poor: {mean(poor):.2f} ± {pstdev(poor):.2f}, "
                f"Gini: {mean(gini_values):.4f} ± {pstdev(gini_values):.4f}"
            )

if __name__ == "__main__":
    main()
