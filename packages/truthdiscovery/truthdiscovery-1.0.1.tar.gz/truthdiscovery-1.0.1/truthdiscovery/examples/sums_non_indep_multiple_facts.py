import os.path

import numpy.ma as ma

from truthdiscovery.algorithm import Sums
from truthdiscovery.input import MatrixDataset
from truthdiscovery.graphs import (
    MatrixDatasetGraphRenderer,
    ResultsGradientColourScheme
)
from truthdiscovery.utils import ConvergenceIterator, DistanceMeasures


if __name__ == "__main__":
    ds1 = MatrixDataset(ma.masked_values([
        [1, 1],
        [1, 9],
        [9, 1],
        [2, 2],
    ], 9))
    ds2 = MatrixDataset(ma.masked_values([
        [1, 1, 9, 9, 9],
        [1, 9, 9, 9, 9],
        [9, 1, 9, 9, 9],
        [2, 2, 9, 9, 9],
        [9, 9, 1, 1, 1],
        [9, 9, 1, 1, 1],
        [9, 9, 2, 2, 2],
    ], 9))

    alg = Sums(iterator=ConvergenceIterator(DistanceMeasures.L2, 0.0000001))
    res1 = alg.run(ds1)
    res2 = alg.run(ds2)

    scenarios = [(res1, ds1, "results1.png"), (res2, ds2, "results2.png")]
    for res, ds, name in scenarios:
        path = os.path.join("/tmp", name)
        rend = MatrixDatasetGraphRenderer(
            colours=ResultsGradientColourScheme(res)
        )
        with open(path, "wb") as outfile:
            rend.render(ds, outfile)

    for source, trust2 in res2.trust.items():
        trust1 = res1.trust.get(source, 9)
        print("{}: {:.4f}\t{:.4f}".format(source, trust1, trust2))
