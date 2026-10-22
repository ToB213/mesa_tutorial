import numpy as np


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

    return float(
        np.sum((2 * index - n - 1) * arr)
        / (n * total)
    )
