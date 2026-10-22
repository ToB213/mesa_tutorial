from statistics import mean, pstdev

from money_model import MoneyModel
from metrics import gini


def tax_agent(agent):
    """Collect one unit of tax from agents with wealth >= 5."""
    if agent.wealth >= 5:
        agent.wealth -= 1


def main():
    n = 50
    steps = 100
    runs = 50
    base_seed = 42

    results = {
        "fixed": [],
        "random": [],
    }

    for i in range(runs):
        for activation in results:
            model = MoneyModel(
                seed=base_seed + i,
                n=n,
                activation=activation,
            )

            # Run the simulation
            for _ in range(steps):
                model.step()

                # Wealth conservation
                assert model.agents.agg("wealth", sum) == n

            # Collect wealth before taxation
            wealth_before = model.agents.get("wealth")

            # Calculate Gini coefficient
            results[activation].append(
                gini(wealth_before)
            )

            # Count taxpayers
            taxpayers = model.agents.select(
                lambda agent: agent.wealth >= 5
            )
            tax_count = len(taxpayers)

            # Apply taxation
            model.agents.do(tax_agent)

            # Collect wealth after taxation
            wealth_after = model.agents.get("wealth")

            # Verify the collected tax
            assert (
                sum(wealth_before) - sum(wealth_after)
                == tax_count
            )

            # Collect agent reports
            reports = model.agents.map("report_status")

            if i == 0:
                print(f"\n=== Activation: {activation} ===")
                print(f"Tax collected: {tax_count}")

                for report in reports[:5]:
                    print(report)

    # Compare activation methods
    print("\n=== Gini Comparison (Before Tax) ===")

    for activation, gini_values in results.items():
        print(
            f"Activation: {activation}, "
            f"Mean Gini: {mean(gini_values):.4f}, "
            f"Std Gini: {pstdev(gini_values):.4f}"
        )


if __name__ == "__main__":
    main()
