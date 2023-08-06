import json
import math
from os import path

import numpy as np
import pytest

from truthdiscovery.algorithm import (
    AverageLog,
    BaseIterativeAlgorithm,
    Investment,
    MajorityVoting,
    PooledInvestment,
    PriorBelief,
    Sums,
    TruthFinder
)
from truthdiscovery.exceptions import EmptyDatasetError
from truthdiscovery.input import Dataset, MatrixDataset
from truthdiscovery.utils import (
    ConvergenceIterator,
    DistanceMeasures,
    FixedIterator
)


class BaseTest:
    @pytest.fixture
    def triples(self):
        return [
            ("s1", "x", "one"),
            ("s1", "y", "nine"),
            ("s1", "z", "seven"),

            ("s2", "x", "one"),
            ("s2", "y", "eight"),

            ("s3", "z", "seven"),
        ]

    @pytest.fixture
    def data(self, triples):
        return Dataset(triples)


class TestBase(BaseTest):
    def test_empty_dataset(self):
        data = Dataset([])
        non_it = MajorityVoting()
        it = Sums()
        for alg in [non_it, it]:
            with pytest.raises(EmptyDatasetError) as excinfo:
                alg.run(data)
        err_msg = "Cannot run algorithm on empty dataset"
        assert str(excinfo.value) == err_msg

        # Test with run_iter also
        with pytest.raises(EmptyDatasetError) as excinfo2:
            _l = list(it.run_iter(data))
        assert str(excinfo2.value) == err_msg

    def test_get_parameter_names(self):
        assert MajorityVoting.get_parameter_names() == set([])
        assert PooledInvestment.get_parameter_names() == {
            "priors", "iterator", "g"
        }
        assert TruthFinder.get_parameter_names() == {
            "priors", "iterator", "influence_param", "dampening_factor",
            "initial_trust"
        }


class TestVoting(BaseTest):
    def test_basic(self, data):
        voting = MajorityVoting()
        results = voting.run(data)
        assert results.trust == {"s1": 1, "s2": 1, "s3": 1}
        assert results.belief == {
            "x": {"one": 1},
            "y": {"nine": 0.5, "eight": 0.5},
            "z": {"seven": 1}
        }


class TestBaseIterative(BaseTest):
    def test_run_fail(self, data):
        alg = BaseIterativeAlgorithm()
        with pytest.raises(NotImplementedError):
            alg.run(data)

    def test_fixed_priors(self, data):
        alg = BaseIterativeAlgorithm(priors=PriorBelief.FIXED)
        got = alg.get_prior_beliefs(data)
        # Claims are:
        # 0: x=1
        # 1: y=9
        # 2: z=7
        # 3: y=8
        expected = [0.5, 0.5, 0.5, 0.5]
        assert np.array_equal(got, expected)

    def test_voted_priors(self, data, triples):
        alg = BaseIterativeAlgorithm(priors=PriorBelief.VOTED)
        got = alg.get_prior_beliefs(data)
        expected = [1, 0.5, 1, 0.5]
        assert np.array_equal(got, expected)

        # Add a new value so that priors are different to voted...
        data2 = Dataset(triples + [("s3", "y", "eight")])
        got2 = alg.get_prior_beliefs(data2)
        expected2 = [1, 1 / 3, 1, 2 / 3]
        assert np.array_equal(got2, expected2)

    def test_uniform_priors(self, data, triples):
        alg = BaseIterativeAlgorithm(priors=PriorBelief.UNIFORM)
        got = alg.get_prior_beliefs(data)
        expected = [1, 0.5, 1, 0.5]
        assert np.array_equal(got, expected)

        # Same secondary test as for voted, but beliefs should not change here
        data2 = Dataset(triples + [("s3", "y", "eight")])
        got2 = alg.get_prior_beliefs(data2)
        expected2 = [1, 0.5, 1, 0.5]
        assert np.array_equal(got2, expected2)

    def test_invalid_priors(self, data):
        alg = BaseIterativeAlgorithm(priors="hello")
        with pytest.raises(ValueError):
            alg.get_prior_beliefs(data)


class TestSums(BaseTest):
    def test_basic(self, data):
        """
        Perform Sums on a small graph. The expected results were obtained by
        finding eigenvectors of suitable matrices (using numpy "by hand"), as
        per Kleinberg paper for Hubs and Authorities
        """
        sums = Sums(iterator=ConvergenceIterator(DistanceMeasures.L1, 0.00001))
        results = sums.run(data)
        assert np.isclose(results.trust["s1"], 1)
        assert np.isclose(results.trust["s2"], 0.53208889)
        assert np.isclose(results.trust["s3"], 0.34729636)

        assert set(results.belief["x"].keys()) == {"one"}
        assert np.isclose(results.belief["x"]["one"], 1)

        assert set(results.belief["y"].keys()) == {"eight", "nine"}
        assert np.isclose(results.belief["y"]["nine"], 0.65270364)
        assert np.isclose(results.belief["y"]["eight"], 0.34729636)

        assert set(results.belief["z"].keys()) == {"seven"}
        assert np.isclose(results.belief["z"]["seven"], 0.87938524)


class TestAverageLog(BaseTest):
    def test_basic(self, data):
        num_iterations = 20
        avlog = AverageLog(iterator=FixedIterator(num_iterations))
        results = avlog.run(data)

        t = [0, 0, 0]
        b = [0.5, 0.5, 0.5, 0.5]

        for _ in range(num_iterations):
            t[0] = math.log(3) * (b[0] + b[1] + b[3]) / 3
            t[1] = math.log(2) * (b[0] + b[2]) / 2
            t[2] = 0

            b[0] = t[0] + t[1]
            b[1] = t[0]
            b[2] = t[1]
            b[3] = t[0] + t[2]

            max_t = max(t)
            max_b = max(b)
            for i, val in enumerate(t):
                t[i] = val / max_t
            for j, val in enumerate(b):
                b[j] = val / max_b

        assert np.isclose(results.trust["s1"], t[0])
        assert np.isclose(results.trust["s2"], t[1])
        assert np.isclose(results.trust["s3"], t[2])

        assert set(results.belief["x"].keys()) == {"one"}
        assert set(results.belief["y"].keys()) == {"eight", "nine"}
        assert set(results.belief["z"].keys()) == {"seven"}

        assert np.isclose(results.belief["x"]["one"], b[0])
        assert np.isclose(results.belief["y"]["nine"], b[1])
        assert np.isclose(results.belief["y"]["eight"], b[2])
        assert np.isclose(results.belief["z"]["seven"], b[3])


class TestInvestment(BaseTest):
    def test_basic(self):
        data = Dataset([
            ("s1", "x", "one"),
            ("s2", "x", "zero"),
            ("s3", "x", "one"),

            ("s1", "y", "zero"),
            ("s3", "y", "one"),
            ("s4", "y", "one"),

            ("s2", "z", "zero"),
            ("s3", "z", "one")
        ])
        # TODO: find example that converges nicely: this one results in all
        # sources bar one having trust 0, which causes division by zero error
        num_iterations = 20
        g = 1.4
        inv = Investment(iterator=FixedIterator(num_iterations), g=g)
        results = inv.run(data)

        b = [
            2 / 3,  # x = 1
            1 / 3,  # x = 0
            2 / 3,  # y = 1
            1 / 3,  # y = 0
            1 / 2,  # z = 1
            1 / 2   # z = 0
        ]
        t = [1, 1, 1, 1]
        old_t = t[:]

        for _ in range(num_iterations):
            t[0] = (old_t[0] / 2) * (
                b[0] / ((old_t[0] / 2) + (old_t[2] / 3)) +
                b[3] / (old_t[0] / 2)
            )
            t[1] = (old_t[1] / 2) * (
                b[1] / (old_t[1] / 2) +
                b[5] / (old_t[1] / 2)
            )
            t[2] = (old_t[2] / 3) * (
                b[0] / ((old_t[0] / 2) + (old_t[2] / 3)) +
                b[2] / ((old_t[2] / 3) + old_t[3]) +
                b[4] / (old_t[2] / 3)
            )
            t[3] = old_t[3] * (
                b[2] / ((old_t[2] / 3) + old_t[3])
            )

            b[0] = ((t[0] / 2) + (t[2] / 3)) ** g
            b[1] = (t[1] / 2) ** g
            b[2] = ((t[2] / 3) + t[3]) ** g
            b[3] = (t[0] / 2) ** g
            b[4] = (t[2] / 3) ** g
            b[5] = (t[1] / 2) ** g

            max_t = max(t)
            for i, val in enumerate(t):
                t[i] = val / max_t
            old_t = t[:]

            max_b = max(b)
            for j, val in enumerate(b):
                b[j] = val / max_b

        assert np.isclose(results.trust["s1"], t[0])
        assert np.isclose(results.trust["s2"], t[1])
        assert np.isclose(results.trust["s3"], t[2])

        assert set(results.belief["x"].keys()) == {"zero", "one"}
        assert set(results.belief["y"].keys()) == {"zero", "one"}
        assert set(results.belief["z"].keys()) == {"zero", "one"}

        assert np.isclose(results.belief["x"]["one"], b[0])
        assert np.isclose(results.belief["x"]["zero"], b[1])
        assert np.isclose(results.belief["y"]["one"], b[2])
        assert np.isclose(results.belief["y"]["zero"], b[3])
        assert np.isclose(results.belief["z"]["one"], b[4])
        assert np.isclose(results.belief["z"]["zero"], b[5])

    def test_converge_to_zero(self):
        """"
        Run Investment till convergence with input that is known to cause
        problems as trust drains to zero, which causes division by zero.
        """
        data = Dataset([
            ("s1", "x", "one"),
            ("s2", "x", "zero"),
            ("s3", "x", "one"),

            ("s1", "y", "zero"),
            ("s3", "y", "one"),
            ("s4", "y", "one"),

            ("s2", "z", "zero"),
            ("s3", "z", "one")
        ])
        it = ConvergenceIterator(DistanceMeasures.L2, 0.1e-100)
        res = Investment(iterator=it).run(data)
        assert res.iterations == 41


class TestPooledInvestment(BaseTest):
    def test_basic(self):
        # Same data as Investment above
        data = Dataset([
            ("s1", "x", "one"), ("s2", "x", "zero"), ("s3", "x", "one"),
            ("s1", "y", "zero"), ("s3", "y", "one"), ("s4", "y", "one"),
            ("s2", "z", "zero"), ("s3", "z", "one")
        ])

        num_iterations = 5
        g = 1.4
        pooled_inv = PooledInvestment(
            iterator=FixedIterator(num_iterations), g=g
        )
        results = pooled_inv.run(data)

        b = [0.5] * 6
        t = [1, 1, 1, 1]
        old_t = t[:]

        for _ in range(num_iterations):
            # Note: trust update is the same as for investment
            t[0] = (old_t[0] / 2) * (
                b[0] / ((old_t[0] / 2) + (old_t[2] / 3)) +
                b[3] / (old_t[0] / 2)
            )
            t[1] = (old_t[1] / 2) * (
                b[1] / (old_t[1] / 2) +
                b[5] / (old_t[1] / 2)
            )
            t[2] = (old_t[2] / 3) * (
                b[0] / ((old_t[0] / 2) + (old_t[2] / 3)) +
                b[2] / ((old_t[2] / 3) + old_t[3]) +
                b[4] / (old_t[2] / 3)
            )
            t[3] = old_t[3] * (
                b[2] / ((old_t[2] / 3) + old_t[3])
            )

            h = [
                (t[0] / 2) + (t[2] / 3),
                t[1] / 2,
                (t[2] / 3) + t[3],
                t[0] / 2,
                t[2] / 3,
                t[1] / 2,
            ]
            g_h = [x ** g for x in h]

            b[0] = h[0] * g_h[0] / (g_h[0] + g_h[1])
            b[1] = h[1] * g_h[1] / (g_h[0] + g_h[1])
            b[2] = h[2] * g_h[2] / (g_h[2] + g_h[3])
            b[3] = h[3] * g_h[3] / (g_h[2] + g_h[3])
            b[4] = h[4] * g_h[4] / (g_h[4] + g_h[5])
            b[5] = h[5] * g_h[5] / (g_h[4] + g_h[5])

            max_t = max(t)
            for i, val in enumerate(t):
                t[i] = val / max_t
            old_t = t[:]

            max_b = max(b)
            for j, val in enumerate(b):
                b[j] = val / max_b

        assert np.isclose(results.trust["s1"], t[0])
        assert np.isclose(results.trust["s2"], t[1])
        assert np.isclose(results.trust["s3"], t[2])

        assert set(results.belief["x"].keys()) == {"zero", "one"}
        assert set(results.belief["y"].keys()) == {"zero", "one"}
        assert set(results.belief["z"].keys()) == {"zero", "one"}

        assert np.isclose(results.belief["x"]["one"], b[0])
        assert np.isclose(results.belief["x"]["zero"], b[1])
        assert np.isclose(results.belief["y"]["one"], b[2])
        assert np.isclose(results.belief["y"]["zero"], b[3])
        assert np.isclose(results.belief["z"]["one"], b[4])
        assert np.isclose(results.belief["z"]["zero"], b[5])


class TestTruthFinder(BaseTest):
    """
    Test the TruthFinder algorithm
    """
    def test_basic(self, triples):
        def imp_func(var, val1, val2):
            m = {"eight": 8, "nine": 9}
            # Make sure implication is asymmetric
            diff = m[val1] - m[val2]
            if diff > 0:
                return np.exp(-0.5 * diff * diff)
            return 0.4

        imp_data = Dataset(triples, implication_function=imp_func)
        n = 50
        t_0 = 0.4
        gamma = 0.5
        ro = 0.25

        trust = [t_0, t_0, t_0]
        belief = [0] * 4

        for _ in range(n):
            tau = [
                -np.log(1 - trust[0]),
                -np.log(1 - trust[1]),
                -np.log(1 - trust[2])
            ]
            sigma = [
                tau[0] + tau[1],
                tau[0],
                tau[1],
                tau[0] + tau[2]
            ]
            sigma_star = [
                sigma[0],
                sigma[1] + ro * sigma[2] * 0.4,
                sigma[2] + ro * sigma[1] * np.exp(-0.5),
                sigma[3]
            ]
            belief = [
                1 / (1 + np.exp(-gamma * sigma_star[0])),
                1 / (1 + np.exp(-gamma * sigma_star[1])),
                1 / (1 + np.exp(-gamma * sigma_star[2])),
                1 / (1 + np.exp(-gamma * sigma_star[3]))
            ]
            trust = [
                (belief[0] + belief[1] + belief[3]) / 3,
                (belief[0] + belief[2]) / 2,
                belief[3]
            ]

        truthfinder = TruthFinder(
            dampening_factor=gamma, influence_param=ro, initial_trust=t_0,
            iterator=FixedIterator(n)
        )
        results = truthfinder.run(imp_data)

        assert np.isclose(results.trust["s1"], trust[0])
        assert np.isclose(results.trust["s2"], trust[1])
        assert np.isclose(results.trust["s3"], trust[2])

        assert set(results.belief["x"].keys()) == {"one"}
        assert set(results.belief["y"].keys()) == {"eight", "nine"}
        assert set(results.belief["z"].keys()) == {"seven"}

        assert np.isclose(results.belief["x"]["one"], belief[0])
        assert np.isclose(results.belief["y"]["nine"], belief[1])
        assert np.isclose(results.belief["y"]["eight"], belief[2])
        assert np.isclose(results.belief["z"]["seven"], belief[3])

    def test_no_implications(self, data):
        """
        Perform the same run as above, but do not bother with implications
        between claims. This is to check that implications are ignored if no
        implication function is given
        """
        n = 50
        t_0 = 0.4
        gamma = 0.5

        trust = [t_0, t_0, t_0]
        belief = [0] * 4

        for _ in range(n):
            tau = [
                -np.log(1 - trust[0]),
                -np.log(1 - trust[1]),
                -np.log(1 - trust[2])
            ]
            sigma = [
                tau[0] + tau[1],
                tau[0],
                tau[1],
                tau[0] + tau[2]
            ]
            belief = [
                1 / (1 + np.exp(-gamma * sigma[0])),
                1 / (1 + np.exp(-gamma * sigma[1])),
                1 / (1 + np.exp(-gamma * sigma[2])),
                1 / (1 + np.exp(-gamma * sigma[3]))
            ]
            trust = [
                (belief[0] + belief[1] + belief[3]) / 3,
                (belief[0] + belief[2]) / 2,
                belief[3]
            ]

        truthfinder = TruthFinder(
            dampening_factor=gamma, initial_trust=t_0,
            iterator=FixedIterator(n)
        )
        results = truthfinder.run(data)

        assert np.isclose(results.trust["s1"], trust[0])
        assert np.isclose(results.trust["s2"], trust[1])
        assert np.isclose(results.trust["s3"], trust[2])

        assert set(results.belief["x"].keys()) == {"one"}
        assert set(results.belief["y"].keys()) == {"eight", "nine"}
        assert set(results.belief["z"].keys()) == {"seven"}

        assert np.isclose(results.belief["x"]["one"], belief[0])
        assert np.isclose(results.belief["y"]["nine"], belief[1])
        assert np.isclose(results.belief["y"]["eight"], belief[2])
        assert np.isclose(results.belief["z"]["seven"], belief[3])

    def test_trust_invalid(self):
        """
        In theory trust scores cannot be 1 for any source. In practise scores
        get so close to 1 that they are rounded to 1, which causes problems
        when we do log(1 - trust).

        This test checks that iteration stops in this case
        """
        data = MatrixDataset(np.array([
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]
        ]))
        it = FixedIterator(100)
        alg = TruthFinder(iterator=it)
        res = alg.run(data)
        # Iteration should stop after only 7 iterations, instead of 100
        assert it.it_count == 7
        assert res.iterations == 7


class TestOnLargeData:
    """
    The following are regression tests, to check that the output of each
    algorithm on a (synthetic) dataset remains the same over time
    """
    @pytest.fixture
    def data(self):
        data_path = self.get_filepath("data.csv")
        with open(data_path) as csv_file:
            return MatrixDataset.from_csv(csv_file)

    def get_filepath(self, name):
        here = path.abspath(path.dirname(__file__))
        return path.join(here, "regression", name)

    def check_results(self, alg, data, exp_results_filename):
        """
        Helper method to check results of an algorithm

        :param alg: algorithm instance
        :param data: Dataset instance
        :param exp_results_filename: filename of JSON file containing expected
                                     results (name should be relative to
                                     'truthdiscovery/test/regression' in the
                                     repo)
        """
        res = alg.run(data)
        with open(self.get_filepath(exp_results_filename)) as res_file:
            exp_res = json.load(res_file)

        for source, trust_val in exp_res["trust"].items():
            source = int(source)
            err_msg = "Incorrect trust for {}, source {}".format(
                exp_results_filename, source
            )
            assert np.isclose(res.trust[source], trust_val), err_msg

        for var, beliefs in exp_res["belief"].items():
            var = int(var)
            for val, belief_val in beliefs.items():
                val = float(val)
                err_msg = "Incorrect belief for {}, var {}, value {}".format(
                    exp_results_filename, var, val
                )
                assert np.isclose(res.belief[var][val], belief_val), err_msg

    def test_sums(self, data):
        sums = Sums(iterator=FixedIterator(20))
        self.check_results(sums, data, "sums_results.json")

    def test_average_log(self, data):
        average_log = AverageLog(iterator=FixedIterator(20))
        self.check_results(average_log, data, "average_log_results.json")

    def test_investment(self, data):
        investment = Investment(iterator=FixedIterator(20))
        self.check_results(investment, data, "investment_results.json")

    def test_pooled_investment(self, data):
        pooled_investment = PooledInvestment(iterator=FixedIterator(10))
        self.check_results(
            pooled_investment, data, "pooled_investment_results.json"
        )

    def test_truthfinder(self, data):
        it = ConvergenceIterator(DistanceMeasures.COSINE, 0.001)
        truthfinder = TruthFinder(iterator=it)

        def imp(var, val1, val2):
            diff = val1 - val2
            return np.exp(-0.5 * diff ** 2)

        data = MatrixDataset(data.sv, implication_function=imp)
        self.check_results(truthfinder, data, "truthfinder_results.json")

    def test_voting(self, data):
        voting = MajorityVoting()
        self.check_results(voting, data, "voting_results.json")


class TestIteratorsForAlgorithms:
    def test_default_iterator_types(self):
        test_data = {
            FixedIterator: (Sums, AverageLog, Investment, PooledInvestment),
            ConvergenceIterator: (TruthFinder,)
        }
        for it_cls, alg_classes in test_data.items():
            for alg_cls in alg_classes:
                obj = alg_cls()
                err_msg = ("Wrong iterator type for {}: {} instead of {}"
                           .format(alg_cls.__name__,
                                   obj.iterator.__class__.__name__,
                                   it_cls.__name__))
                assert isinstance(obj.iterator, it_cls), err_msg


class TestLoggingAlgorithm(BaseTest):
    @pytest.fixture
    def alg_classes(self):
        return [AverageLog, Investment, PooledInvestment, Sums, TruthFinder]

    @pytest.fixture
    def algs(self, alg_classes):
        return [cls() for cls in alg_classes]

    def test_final_result(self, algs, data):
        for alg in algs:
            # Get the final result normally
            final_res = alg.run(data)

            # Iterate through partial results, and check the final result is as
            # expected
            last_res = None
            for r in alg.run_iter(data):
                last_res = r

            assert last_res.trust == final_res.trust
            assert last_res.belief == final_res.belief
            assert last_res.iterations == final_res.iterations

    def test_no_logging(self, algs, data):
        for alg in algs:
            _res = alg.run(data)
            assert alg.results_log is None

    def test_partial_results(self, alg_classes, data):
        it = FixedIterator(3)
        for cls in alg_classes:
            alg = cls(iterator=it)

            log = list(alg.run_iter(data))
            assert len(log) == 4
            initial, first, second, third = log

            assert initial.iterations == 0
            assert first.iterations == 1
            assert second.iterations == 2
            assert third.iterations == 3

            # Time should be non-decreasing
            assert (
                initial.time_taken <= first.time_taken <= second.time_taken
                <= third.time_taken
            )

    def test_sums_detailed(self, data):
        it = FixedIterator(3)
        alg = Sums(iterator=it, priors=PriorBelief.FIXED)
        initial, first, second, third = alg.run_iter(data)

        assert initial.belief == {
            "x": {"one": 0.5},
            "y": {"nine": 0.5, "eight": 0.5},
            "z": {"seven": 0.5}
        }
        assert initial.trust == {"s1": 0, "s2": 0, "s3": 0}

        assert first.trust == {"s1": 1, "s2": 2 / 3, "s3": 1 / 3}
        assert first.belief == {
            "x": {"one": 1},
            "y": {"nine": 3 / 5, "eight": 2 / 5},
            "z": {"seven": 4 / 5}
        }
