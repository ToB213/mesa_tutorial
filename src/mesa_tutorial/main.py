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
):
    model = MoneyModel(
        n=n,
        seed=seed,
        activation="random",
        redistribution=redistribution,
    )

    for _ in range(steps):
        model.step()

        assert model.agents.agg("wealth", sum) == n

    wealth = model.agents.get("wealth")

    return {
        "poor": len(
            model.agents.select(
                lambda agent: agent.wealth == 0
            )
        ),
        "gini": gini(wealth),
    }

def main():
    n = 50
    steps = 100
    runs = 50
    base_seed = 42

    for redistribution in (False, True):
        results = [
            run_experiment(
                n=n,
                steps=steps,
                seed=base_seed + i,
                redistribution=redistribution,
            )
            for i in range(runs)
        ]

        print(
            f"Redistribution: {redistribution}, "
            f"Poor: {mean(r['poor'] for r in results):.2f} ± {pstdev(r['poor'] for r in results):.2f}, "
            f"Gini: {mean(r['gini'] for r in results):.4f} ± {pstdev(r['gini'] for r in results):.4f}"
        )

if __name__ == "__main__":
    main()
