"""
Compare the speed of convergence for iterative algorithms.

This script runs iterative algorithms on a large synthetic dataset, and records
the distance between old and new trust vectors at each iteration.

These distances are then plotted, so that the convergence (or otherwise) of
each algorithm can be compared.
"""
from io import StringIO
from os import path
import sys

import matplotlib.pyplot as plt

from truthdiscovery.algorithm import (
    AverageLog,
    Investment,
    PooledInvestment,
    Sums,
    TruthFinder
)
from truthdiscovery.input import SupervisedData
from truthdiscovery.utils import ConvergenceIterator, DistanceMeasures
from truthdiscovery.exceptions import ConvergenceError


DATA_CSV = path.join(path.dirname(__file__), "large_synthetic_data.csv")
ALGORITHMS = [Sums, AverageLog, Investment, PooledInvestment, TruthFinder]
MEASURE = DistanceMeasures.L2


def main(csv_file):
    """
    Perform the test
    """
    print("Loading data...")
    sup = SupervisedData.from_csv(csv_file)
    fig, ax = plt.subplots()
    fig.suptitle(
        "Convergence experiment\n"
        "(synthetic data with {d.num_sources} sources, {d.num_variables} "
        "variables)".format(d=sup.data)
    )
    ax.set_xlabel("Iteration number")
    ax.set_ylabel(r"$\ell_2$ distance between old and new trust (log scale)")

    # map algorithm names to list of distances over time
    distances = {}
    iterator = ConvergenceIterator(MEASURE, 0, limit=100, debug=True)
    for cls in ALGORITHMS:
        name = cls.__name__
        print("running {} using {} measure".format(name, MEASURE))
        alg = cls(iterator=iterator)
        stdout = StringIO()
        sys.stdout = stdout
        try:
            _res = alg.run(sup.data)
        except ConvergenceError:
            pass
        finally:
            sys.stdout = sys.__stdout__

        distances[name] = []
        for line in stdout.getvalue().split("\n"):
            if not line:
                continue
            _, dist = line.split(",")
            distances[name].append(float(dist))

    max_its = max(len(dists) for dists in distances.values())
    x = range(1, max_its + 1)

    for name, dists in distances.items():
        while len(dists) < max_its:
            dists.append(None)
        ax.semilogy(x, dists, label=name, linewidth=3)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    with open(DATA_CSV) as csv_file:
        main(csv_file)
