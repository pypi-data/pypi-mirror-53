from truthdiscovery import *

with open("large_synthetic_data.csv") as f:
    sup = SupervisedData.from_csv(f)

alg = TruthFinder(iterator=ConvergenceIterator(DistanceMeasures.L2, 0.001))
res = alg.run(sup.data)
print(res.time_taken)
print(res.iterations)
for s in sorted(res.trust):
    print("{}: {}".format(s, res.trust[s]))
for var in sorted(res.belief):
    bels = res.belief[var]
    for val in sorted(bels):
        print("{}={}: {}".format(var, val, bels[val]))
