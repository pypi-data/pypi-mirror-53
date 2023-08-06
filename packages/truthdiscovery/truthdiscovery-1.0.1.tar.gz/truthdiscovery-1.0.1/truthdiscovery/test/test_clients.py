import json

from flask import Flask
import numpy.ma as ma
import pytest
import yaml

from truthdiscovery.algorithm import (
    AverageLog,
    MajorityVoting,
    PooledInvestment,
    PriorBelief,
    Sums,
    TruthFinder
)
from truthdiscovery.client import BaseClient, CommandLineClient, OutputFields
from truthdiscovery.client.web import get_flask_app, route
from truthdiscovery.input import MatrixDataset, SupervisedData
from truthdiscovery.utils import (
    ConvergenceIterator,
    DistanceMeasures,
    FixedIterator
)
from truthdiscovery.test.utils import is_valid_png


class ClientTestsBase:
    @pytest.fixture
    def dataset(self):
        return MatrixDataset(ma.masked_values([
            [1, 2, 3, 2],
            [3, 0, 1, 2],
            [2, 2, 0, 0],
            [0, 1, 0, 3]
        ], 0))

    @pytest.fixture
    def csv_fileobj(self, dataset, tmpdir):
        csvfile = tmpdir.join("data.csv")
        csvfile.write(dataset.to_csv())
        return csvfile

    @pytest.fixture
    def csv_dataset(self, csv_fileobj):
        return str(csv_fileobj)


class TestBaseClient(ClientTestsBase):
    def test_get_iterator(self):
        fixed_145 = BaseClient().get_iterator("fixed-145")
        assert isinstance(fixed_145, FixedIterator)
        assert fixed_145.limit == 145

        l1_conv = BaseClient().get_iterator("l1-convergence-0.234")
        assert isinstance(l1_conv, ConvergenceIterator)
        assert l1_conv.distance_measure == DistanceMeasures.L1
        assert l1_conv.threshold == 0.234

        l2_with_limit = BaseClient().get_iterator(
            "l2-convergence-0.234-limit-9"
        )
        assert isinstance(l2_with_limit, ConvergenceIterator)
        assert l2_with_limit.distance_measure == DistanceMeasures.L2
        assert l2_with_limit.threshold == 0.234
        assert l2_with_limit.limit == 9

        # Should be too many iterations
        with pytest.raises(ValueError):
            fixed_2000 = BaseClient().get_iterator(
                "fixed-2000", max_limit=1999
            )
        with pytest.raises(ValueError):
            conv_2000 = BaseClient().get_iterator(
                "l2-convergence-1-limit-2000", max_limit=1999
            )

        invalid_it_strings = (
            "fixed",
            "fixed-",
            "fixed-hello",
            "fixed-10.0",
            "fixed--4",
            "convergence",
            "-convergence-",
            "l1-convergence-",
            "l1-convergence-l1",
            "blah-convergence-0.03",
            "l1-convergence-0.03-limit",
            "l1-convergence-0.03-limit-",
            "l1-convergence-0.03-limit-45.0"
        )
        for it_string in invalid_it_strings:
            with pytest.raises(ValueError):
                BaseClient().get_iterator(it_string)

    def test_get_algorithm_parameter(self):
        # Iterator param
        name1, val1 = BaseClient().algorithm_parameter("iterator=fixed-99")
        assert name1 == "iterator"
        assert isinstance(val1, FixedIterator)
        assert val1.limit == 99

        # Priors
        name2, val2 = BaseClient().algorithm_parameter("priors=voted")
        assert name2 == "priors"
        assert val2 == PriorBelief.VOTED

        # Anything else should be a float
        name3, val3 = BaseClient().algorithm_parameter("g=1.4")
        assert name3 == "g"
        assert val3 == 1.4

        # Extra whitespace should be allowed
        name3, val3 = BaseClient().algorithm_parameter("ppp =   3.4")
        assert name3 == "ppp"
        assert val3 == 3.4

    def test_get_output_obj(self, csv_fileobj):
        dataset = MatrixDataset.from_csv(csv_fileobj)
        alg = Sums(iterator=FixedIterator(5))
        # Default should be all fields if none are given, but not accuracy
        # unless supervised data given
        results = alg.run(dataset)
        out1 = BaseClient().get_output_obj(results)
        exp_keys = {
            f.value for f in OutputFields if f != OutputFields.ACCURACY
        }
        assert set(out1.keys()) == exp_keys

        sup_data = SupervisedData.from_csv(csv_fileobj)
        sup_results = alg.run(sup_data.data)
        out2 = BaseClient().get_output_obj(sup_results, sup_data=sup_data)
        assert set(out2.keys()) == {f.value for f in OutputFields}
        assert out2["trust"] == sup_results.trust
        assert out2["belief"] == sup_results.belief

        out3 = BaseClient().get_output_obj(
            results, output_fields=[OutputFields.TRUST]
        )
        assert set(out3.keys()) == {"trust"}

    def test_get_algorithm_params(self):
        client = BaseClient()
        params = {
            "priors": PriorBelief.VOTED, "g": 1.99,
            "dampening_factor": 0.5678
        }

        def get_p(*args):
            return client.get_algorithm_params(*args)[0]

        assert get_p(Sums, params) == {"priors": PriorBelief.VOTED}
        assert get_p(TruthFinder, params) == {
            "priors": PriorBelief.VOTED, "dampening_factor": 0.5678
        }
        assert get_p(PooledInvestment, params) == {
            "priors": PriorBelief.VOTED, "g": 1.99
        }
        assert get_p(MajorityVoting, params) == {}


class TestCommandLineClient(ClientTestsBase):
    @pytest.fixture
    def client(self):
        return CommandLineClient()

    def get_algorithm_objects(self, client, args):
        all_params = dict(args.alg_params or [])
        objs = []
        for cls in args.alg_classes:
            params, _ignored = client.get_algorithm_params(cls, all_params)
            obj = client.get_algorithm_object(cls, params)
            objs.append(obj)
        return objs

    def run(self, *args):
        client = CommandLineClient()
        client.run(args)

    def get_parsed_args(self, *args):
        return CommandLineClient().get_parser().parse_args(args)

    def test_no_commands(self, capsys):
        self.run()
        out = capsys.readouterr().out
        assert "Command-line interface to truthdiscovery library" in out

    def test_basic(self, csv_dataset):
        self.run(
            "run", "--algorithm", "sums", "-f", csv_dataset
        )

    def test_results(self, csv_dataset, csv_fileobj, capsys):
        self.run(
            "run", "-a", "average_log", "-f", csv_dataset
        )
        got_results = yaml.safe_load(capsys.readouterr().out)
        assert "average_log" in got_results
        alg_results = got_results["average_log"]
        assert isinstance(alg_results, dict)
        exp_results = AverageLog().run(MatrixDataset.from_csv(csv_fileobj))
        assert alg_results["trust"] == exp_results.trust
        assert alg_results["belief"] == exp_results.belief
        assert alg_results["iterations"] == exp_results.iterations

    def test_multiple_parameters(self, csv_dataset):
        self.run(
            "run", "--algorithm", "pooled_investment", "-p", "g=1.1234",
            "iterator=fixed-11", "priors=uniform", "-f", csv_dataset
        )

    def test_multiple_algorithms(self, capsys, csv_dataset):
        # Mirrors an identical test for web client below
        self.run(
            "run", "-a", "investment", "sums", "voting", "-f", csv_dataset,
            "-p", "iterator=fixed-11", "g=1.16"
        )
        outerr = capsys.readouterr()
        got_results = yaml.safe_load(outerr.out)

        assert set(got_results.keys()) == {"investment", "sums", "voting"}
        assert got_results["investment"]["iterations"] == 11
        assert got_results["sums"]["iterations"] == 11
        assert got_results["voting"]["iterations"] is None

        assert got_results["voting"]["trust"] == {i: 1 for i in range(4)}
        assert got_results["sums"]["trust"] == {
            0: 1.0, 1: 0.5323216608830517, 2: 0.3472167514190226,
            3: 5.9742483641484065e-05
        }
        assert got_results["investment"]["trust"] == {
            0: 1.0, 1: 0.8725062856135304, 2: 0.6845094785538429,
            3: 0.1211362221507375
        }

        # Should get warnings for the invalid parameters
        expected_warnings = {
            "WARNING: Ignored parameters for 'MajorityVoting': g, iterator",
            "WARNING: Ignored parameters for 'Sums': g"
        }
        assert set(filter(None, outerr.err.split("\n"))) == expected_warnings

    def test_get_algorithm_instance(self, client, csv_dataset):
        args = self.get_parsed_args(
            "run", "--algorithm", "voting", "truthfinder", "-p",
            "dampening_factor=0.1", "influence_param=0.77", "-f", csv_dataset
        )
        voting = self.get_algorithm_objects(client, args)[0]
        assert isinstance(voting, MajorityVoting)
        tf = self.get_algorithm_objects(client, args)[1]
        assert isinstance(tf, TruthFinder)
        assert tf.dampening_factor == 0.1
        assert tf.influence_param == 0.77

    def test_set_prior_belief(self, client, csv_dataset, capsys):
        args = self.get_parsed_args(
            "run", "--algorithm", "sums", "-p", "priors=voted", "-f",
            csv_dataset
        )
        alg = self.get_algorithm_objects(client, args)[0]
        assert isinstance(alg, Sums)
        assert alg.priors == PriorBelief.VOTED

        # Invalid prior string
        with pytest.raises(SystemExit):
            self.run(
                "run", "--algorithm", "sums", "-p", "priors=blah", "-f",
                csv_dataset
            )

        err_msg = capsys.readouterr().err
        assert "'blah' is not a valid PriorBelief" in err_msg

    def test_set_iterator(self, client, csv_dataset, capsys):
        # Fixed iterator
        raw_args1 = (
            "run", "--algorithm", "sums", "-p", "iterator=fixed-123", "-f",
            csv_dataset
        )
        args1 = self.get_parsed_args(*raw_args1)
        alg1 = self.get_algorithm_objects(client, args1)[0]
        assert isinstance(alg1, Sums)
        assert isinstance(alg1.iterator, FixedIterator)
        assert alg1.iterator.limit == 123
        self.run(*raw_args1)
        results = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert results["iterations"] == 123

        # Convergence iterator
        args2 = self.get_parsed_args(
            "run", "--algorithm", "sums", "-p",
            "iterator=cosine-convergence-0.01", "-f", csv_dataset
        )
        alg2 = self.get_algorithm_objects(client, args2)[0]
        assert isinstance(alg2.iterator, ConvergenceIterator)
        assert alg2.iterator.distance_measure == DistanceMeasures.COSINE
        assert alg2.iterator.threshold == 0.01

        # Convergence iterator with limit
        args3 = self.get_parsed_args(
            "run", "--algorithm", "sums", "-p",
            "iterator=l2-convergence-0.3-limit-99", "-f", csv_dataset
        )
        alg3 = self.get_algorithm_objects(client, args3)[0]
        assert isinstance(alg3.iterator, ConvergenceIterator)
        assert alg3.iterator.distance_measure == DistanceMeasures.L2
        assert alg3.iterator.threshold == 0.3
        assert alg3.iterator.limit == 99

        # Convergence iterator with invalid distance measure
        with pytest.raises(SystemExit):
            self.run(
                "run", "--algorithm", "sums", "-p",
                "iterator=blah-convergence-0.3-limit-99", "-f", csv_dataset
            )
        assert "invalid distance measure 'blah'" in capsys.readouterr().err

        # Invalid iterator specification
        with pytest.raises(SystemExit):
            self.run(
                "run", "--algorithm", "sums", "-p", "iterator=hello", "-f",
                csv_dataset
            )
        assert "invalid iterator specification" in capsys.readouterr().err

    def test_invalid_algorithm_parameter(self, csv_dataset, capsys):
        # Invalid format
        with pytest.raises(SystemExit):
            self.run(
                "run", "--algorithm", "truthfinder", "-p", "initial_trust 0.1",
                "-f", csv_dataset
            )
        assert "must be in the form 'key=value'" in capsys.readouterr().err

    def test_invalid_algorithm(self, csv_dataset, capsys):
        with pytest.raises(SystemExit):
            self.run(
                "run", "--algorithm", "joesalgorithm", "-f", csv_dataset
            )
        assert (
            "invalid algorithm label 'joesalgorithm'"
            in capsys.readouterr().err
        )

    def test_filter_sources_variables(self, csv_dataset, capsys):
        # Filter sources
        self.run(
            "run", "-a", "sums", "-f", csv_dataset, "--sources", "0", "3",
        )
        results1 = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results1["trust"].keys()) == {0, 3}
        assert set(results1["belief"].keys()) == {0, 1, 2, 3}

        # Filter both
        self.run(
            "run", "-a", "sums", "-f", csv_dataset, "--sources", "0", "3",
            "--variables", "1", "2"
        )
        results2 = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results2["trust"].keys()) == {0, 3}
        assert set(results2["belief"].keys()) == {1, 2}

        # Special case where only one source/variable
        self.run(
            "run", "-a", "sums", "-f", csv_dataset, "--sources", "1",
            "--variables", "0"
        )
        results3 = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results3["trust"].keys()) == {1}
        assert set(results3["belief"].keys()) == {0}

        # Unknown sources/vars should not cause trouble
        self.run(
            "run", "-a", "sums", "-f", csv_dataset, "--sources", "3", "1000",
            "--variables", "499", "666"
        )
        results3 = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results3["trust"].keys()) == {3}
        # We didn't give any valid variables: belief should be empty
        assert results3["belief"] == {}

    def test_default_output(self, csv_dataset, capsys):
        self.run("run", "-a", "voting", "-f", csv_dataset)
        results = yaml.safe_load(capsys.readouterr().out)["voting"]
        assert set(results.keys()) == {
            "time", "iterations", "trust", "belief"
        }
        assert results["iterations"] is None

    def test_custom_output(self, csv_fileobj, csv_dataset, capsys):
        self.run("run", "-a", "sums", "-f", csv_dataset, "-o", "time")
        results = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results.keys()) == {"time"}

        self.run(
            "run", "-a", "sums", "-f", csv_dataset, "-o", "time",
            "iterations"
        )
        results = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results.keys()) == {"time", "iterations"}

        self.run(
            "run", "-a", "sums", "-f", csv_dataset, "-o", "trust",
            "trust_stats"
        )
        results = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results.keys()) == {"trust", "trust_stats"}
        exp_mean, exp_stddev = (Sums().run(MatrixDataset.from_csv(csv_fileobj))
                                .get_trust_stats())
        assert results["trust_stats"] == {
            "mean": exp_mean, "stddev": exp_stddev
        }

    def test_show_most_believed_values(self, csv_dataset, capsys):
        self.run(
            "run", "-a", "voting", "-f", csv_dataset, "--output",
            "most_believed_values"
        )
        results = yaml.safe_load(capsys.readouterr().out)["voting"]
        assert results == {
            "most_believed_values": {0: [1, 2, 3], 1: [2], 2: [1, 3], 3: [2]}
        }
        # Test with variable filtering
        self.run(
            "run", "-a", "voting", "-f", csv_dataset, "-o",
            "most_believed_values", "--variables", "0", "3"
        )
        results = yaml.safe_load(capsys.readouterr().out)["voting"]
        assert "belief" not in results
        assert "most_believed_values" in results
        assert results["most_believed_values"] == {
            0: [1, 2, 3],
            3: [2]
        }

    def test_belief_stats(self, csv_dataset, csv_fileobj, capsys):
        self.run("run", "-a", "sums", "-f", csv_dataset, "-o", "belief_stats")
        results = yaml.safe_load(capsys.readouterr().out)["sums"]
        assert set(results.keys()) == {"belief_stats"}
        exp_belief_stats = (Sums().run(MatrixDataset.from_csv(csv_fileobj))
                            .get_belief_stats())
        assert results["belief_stats"] == {
            var: {"mean": mean, "stddev": stddev}
            for var, (mean, stddev) in exp_belief_stats.items()
        }

    def test_synthetic_generation(self, capsys):
        self.run(
            "synth", "--trust", "0.5", "0.6", "0.7", "--num-vars", "10",
            "--domain-size", "5"
        )
        output = capsys.readouterr().out.strip()
        lines = output.split("\n")
        assert len(lines) == 4  # first row is true values, then 3 source rows
        for line in lines:
            columns = line.split(",")
            assert len(columns) == 10
            for col in columns:
                assert col == "" or float(col) in {0, 1, 2, 3, 4}

    def test_synthetic_generation_claim_prob_1(self, capsys):
        self.run(
            "synth", "--trust", "0.5", "0.6", "0.7", "--num-vars", "10",
            "--domain-size", "2", "--claim-prob", "1"
        )
        output = capsys.readouterr().out.strip()
        lines = output.split("\n")
        assert len(lines) == 4
        for line in lines:
            columns = line.split(",")
            for col in columns:
                assert float(col) in {0, 1}

    def test_synthetic_generation_source_trust_1(self, capsys):
        self.run("synth", "--trust", "1", "--claim-prob", "1")
        output = capsys.readouterr().out.strip()
        true_vals, claims = output.split("\n")
        assert true_vals == claims

    def test_synthetic_generation_invalid_params(self, capsys):
        # Check that invalid param errors are caught by the parser, not raised
        # as Python exceptions
        with pytest.raises(SystemExit):
            self.run("synth", "--trust", "2")
        exp_err_msg = "error: Trust values must be in [0, 1]"
        assert exp_err_msg in capsys.readouterr().err

    def test_supervised_dataset_and_accuracy(self, csv_dataset, capsys):
        self.run(
            "run", "-a", "voting", "-f", csv_dataset, "--supervised", "-o",
            "trust", "belief", "accuracy"
        )
        results = yaml.safe_load(capsys.readouterr().out)["voting"]
        assert results["trust"] == {0: 1, 1: 1, 2: 1}
        assert results["belief"] == {
            0: {2: 1, 3: 1},
            1: {1: 1, 2: 1},
            2: {1: 1},
            3: {2: 1, 3: 1}
        }
        # accuracy is not deterministic when there are ties for most-believed
        # values
        assert results["accuracy"] in (1 / 3, 2 / 3, 0)

    def test_accuracy_not_supervised(self, csv_dataset, capsys):
        with pytest.raises(SystemExit):
            self.run(
                "run", "-a", "voting", "-f", csv_dataset, "-o", "accuracy"
            )
        err_msg = "cannot calculate accuracy without --supervised"
        assert err_msg in capsys.readouterr().err

    def test_accuracy_undefined(self, capsys, tmpdir):
        ds = tmpdir.join("newdata.csv")
        ds.write("\n".join((
            "1,2,3,4",
            "1,2,3,4",
        )))
        self.run("run", "-a", "voting", "-f", str(ds), "-s", "-o", "accuracy")
        results = yaml.safe_load(capsys.readouterr().out)["voting"]
        assert results["accuracy"] is None

    def test_graph_generation(self, client, csv_dataset, capsys, tmpdir):
        outfile = tmpdir.join("mypic.png")
        self.run("graph", "-f", csv_dataset, "-o", str(outfile))
        with open(str(outfile), "rb") as f:
            assert is_valid_png(f)

        # Missing dataset
        with pytest.raises(SystemExit):
            self.run("graph", "-o", str(outfile))
        assert "--dataset" in capsys.readouterr().err

        # Missing output file
        with pytest.raises(SystemExit):
            self.run("graph", "-f", csv_dataset)
        assert "--outfile" in capsys.readouterr().err

        # Renderer options
        rend1 = client.get_graph_renderer(
            self.get_parsed_args(
                "graph", "-f", csv_dataset, "-o", str(outfile), "--width",
                "200", "--node-radius", "25", "--font-size", "14", "--spacing",
                "4", "--line-width", "9", "--node-border-width", "34",
                "--one-indexed"
            )
        )
        assert rend1.width == 200
        assert rend1.node_radius == 25
        assert rend1.spacing == 4
        assert rend1.font_size == 14
        assert rend1.line_width == 9
        assert rend1.node_border_width == 34
        assert not rend1.zero_indexed

        # Check that if we only give some options, the rest are kept at the
        # defaults
        rend2 = client.get_graph_renderer(
            self.get_parsed_args(
                "graph", "-f", csv_dataset, "-o", str(outfile), "--width",
                "200"
            )
        )
        assert rend2.width == 200
        assert rend2.node_radius == 50
        assert rend2.zero_indexed


class TestWebClient(ClientTestsBase):
    @pytest.fixture
    def test_client(self):
        return get_flask_app().test_client()

    def test_routing(self):
        class ExampleClass:
            def __init__(self, x):
                self.x = x

            @route("/some-test-url/<name>/<int:age>", methods=["POST"])
            def my_view_function(self, name, age):
                return (
                    "name is {}, age is {} and x is {}"
                    .format(name, age, self.x)
                )

        app = Flask("test_routing")
        route.add_routes(app, ExampleClass(42))
        client = app.test_client()

        resp1 = client.post("/some-test-url/joe/22")
        assert resp1.status_code == 200
        assert resp1.data == b"name is joe, age is 22 and x is 42"

        # GET should not be allowed
        resp2 = client.get("/some-test-url/jim/91")
        assert resp2.status_code == 405

    def test_home(self, test_client):
        resp = test_client.get("/")
        html = resp.data.decode()
        assert "<body>" in html
        assert "truth discovery tool" in html.lower()
        assert '&#34;average_log&#34;: &#34;AverageLog&#34;' in html

    def test_run_fail(self, test_client):
        # Missing parameters
        resp1 = test_client.get("/run/")
        assert resp1.status_code == 400
        err_msg = "'algorithm' and 'matrix' parameters are required"
        assert resp1.json == {"ok": False, "error": err_msg}
        resp2 = test_client.get("/run/", query_string={"algorithm": "sums"})
        assert resp2.status_code == 400
        assert resp2.json == {"ok": False, "error": err_msg}

        # Invalid algorithm
        data = {"algorithm": "hmm", "matrix": "1,2,3"}
        resp3 = test_client.get("/run/", query_string=data)
        assert resp3.status_code == 400
        assert not resp3.json["ok"]
        assert "invalid algorithm label 'hmm'" in resp3.json["error"]

        # Invalid matrices
        invalid_matrices = (
            "hello",
            "1,2,3\n1,2,3,4",     # inconsistent shape
            "1,2,3ree\n1,2,3,4",  # non-float values
        )
        for matrix in invalid_matrices:
            data = {"algorithm": "sums", "matrix": matrix}
            resp = test_client.get("/run/", query_string=data)
            assert resp.status_code == 400
            assert not resp.json["ok"]
            assert "invalid matrix CSV" in resp.json["error"]

        # Invalid parameters
        invalid_params = (
            ("random-string", "parameters must be in the form 'key=value'"),
            ("priors=blah", "'blah' is not a valid PriorBelief"),
            ("priors=voted\nrandom-string", "in the form 'key=value'"),
        )
        for params, exp_err in invalid_params:
            data = {
                "algorithm": "sums",
                "matrix": "1,2,3\n4,5,6",
                "parameters": params
            }
            resp = test_client.get("/run/", query_string=data)
            assert resp.status_code == 400
            assert not resp.json["ok"]
            assert exp_err in resp.json["error"]

    def test_run_success(self, test_client):
        data = {
            "algorithm": "investment",
            # leading and trailing whitespace shouldn't matter
            "matrix": " 1,2,3,\n_,2,3,4   \n\n\n ",
            "parameters": "g=1.2\niterator=fixed-13"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 200
        assert resp.json["ok"]
        output = resp.json["data"]
        assert set(output.keys()) == {"investment"}
        assert output["investment"]["iterations"] == 13

    def test_run_multiple_algorithms(self, test_client, dataset):
        algorithms = ["investment", "sums", "voting"]
        data = {
            "algorithm": algorithms,
            "matrix": dataset.to_csv(),
            # Check that parameters apply to all algorithms, and are ignored if
            # not applicable
            "parameters": "iterator=fixed-11\ng=1.16"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 200
        assert resp.json["ok"]
        output = resp.json["data"]
        assert set(output.keys()) == set(algorithms)
        assert output["investment"]["iterations"] == 11
        assert output["sums"]["iterations"] == 11
        assert output["voting"]["iterations"] is None

        assert output["voting"]["trust"] == {str(i): 1 for i in range(4)}
        assert output["sums"]["trust"] == {
            "0": 1.0, "1": 0.5323216608830517, "2": 0.3472167514190226,
            "3": 5.9742483641484065e-05
        }
        assert output["investment"]["trust"] == {
            "0": 1.0, "1": 0.8725062856135304, "2": 0.6845094785538429,
            "3": 0.1211362221507375
        }

        assert "messages" in resp.json
        assert set(resp.json["messages"]) == {
            "Ignored parameters for 'MajorityVoting': g, iterator",
            "Ignored parameters for 'Sums': g",
        }

    def test_results_diff(self, test_client):
        dataset1 = MatrixDataset(ma.masked_values([
            [1, 0],
            [0, 2]
        ], 0))
        dataset2 = MatrixDataset(ma.masked_values([
            [1, 2],
            [0, 2]
        ], 0))

        request_data1 = {
            "algorithm": "voting",
            "matrix": dataset1.to_csv()
        }
        resp1 = test_client.get("/run/", query_string=request_data1)
        assert resp1.status_code == 200

        request_data2 = {
            # Test diffs with multiple algorithms
            "algorithm": ["voting", "investment"],
            "matrix": dataset2.to_csv(),
            "previous_results": json.dumps(resp1.json["data"]["voting"])
        }
        resp2 = test_client.get("/run/", query_string=request_data2)
        assert resp2.status_code == 200
        vot_out = resp2.json["data"]["voting"]
        assert "diff" in vot_out
        assert vot_out["diff"]["trust"] == {"0": 0, "1": 0}  # no trust changes
        assert vot_out["diff"]["belief"] == {
            "0": {"1.0": -0.5}, "1": {"2.0": 0}
        }
        inv_out = resp2.json["data"]["investment"]
        assert "diff" in inv_out
        assert inv_out["diff"]["trust"] == {
            "0": -0.7731216864273125, "1": 0.0
        }
        assert inv_out["diff"]["belief"] == {
            "0": {"1.0": -0.9354768146506873}, "1": {"2.0": 0.0}
        }

    def test_results_diff_invalid_previous_results(self, test_client):
        # Invalid JSON for previous results
        data1 = {
            "algorithm": "voting",
            "matrix": "1,2,3,\n_,2,3,4",
            "previous_results": "invalid json!"
        }
        resp1 = test_client.get("/run/", query_string=data1)
        assert resp1.status_code == 400
        assert not resp1.json["ok"]
        exp_err_msg = "'previous_results' is invalid: invalid JSON"
        assert exp_err_msg in resp1.json["error"]

        # Keys missing in previous results JSON
        data2 = {
            "algorithm": "voting",
            "matrix": "1,2,3,\n_,2,3,4",
            # 'belief' and others are missing
            "previous_results": '{"trust": {"0": 1}}'
        }
        resp2 = test_client.get("/run/", query_string=data2)
        assert resp2.status_code == 400
        assert not resp2.json["ok"]
        exp_err_msg = ("'previous_results' is invalid: required field "
                       "'belief' missing")
        assert exp_err_msg in resp2.json["error"]

    def test_get_json_graph(self, test_client, dataset):
        data = {
            "matrix": dataset.to_csv(),
            "algorithm": "sums"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 200
        output = resp.json
        assert "data" in output
        assert "sums" in output["data"]
        assert "imagery" in output["data"]["sums"]
        assert "graph" in output["data"]["sums"]["imagery"]
        json_string = output["data"]["sums"]["imagery"]["graph"]
        # Check the image is valid JSON
        obj = json.loads(json_string)
        # Check object is as expected
        assert "width" in obj
        assert "height" in obj
        assert "entities" in obj
        assert isinstance(obj["entities"], list)

    def test_get_json_animated_gif(self, test_client, dataset):
        data = {
            "matrix": dataset.to_csv(),
            "algorithm": "sums",
            "parameters": "iterator=fixed-4"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 200
        output = resp.json
        assert "data" in output
        assert "sums" in output["data"]
        assert "imagery" in output["data"]["sums"]
        assert "animation" in output["data"]["sums"]["imagery"]
        json_string = output["data"]["sums"]["imagery"]["animation"]
        # Check animation is valid JSON
        obj = json.loads(json_string)
        # Check object is as expected
        assert "fps" in obj
        assert "frames" in obj
        assert isinstance(obj["frames"], list)
        assert len(obj["frames"]) == 5
        assert isinstance(obj["frames"][0], dict)
        assert "width" in obj["frames"][0]
        assert "height" in obj["frames"][0]
        assert "entities" in obj["frames"][0]

    def test_voting_imagery(self, test_client, dataset):
        """
        Only the graph should be present in imagery for MajorityVoting results,
        since animation is not applicable
        """
        data = {
            "matrix": dataset.to_csv(),
            "algorithm": "voting"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 200
        output = resp.json
        assert "data" in output
        assert "voting" in output["data"]
        assert "imagery" in output["data"]["voting"]
        assert "graph" in output["data"]["voting"]["imagery"]
        assert "animation" not in output["data"]["voting"]["imagery"]

    def test_empty_dataset(self, test_client):
        data = {
            "algorithm": "sums",
            "matrix": ",,,\n,,,\n,,,\n,,,"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 400
        err_msg = "Cannot run algorithm on empty dataset"
        assert resp.json == {"ok": False, "error": err_msg}

    def test_non_convergence(self, test_client):
        data = {
            "algorithm": "sums",
            "matrix": "1,2,3\n4,5,6",
            "parameters": "iterator=l1-convergence-0-limit-25"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 500
        err_msg = "Did not converge in 25 iterations"
        assert resp.json == {"ok": False, "error": err_msg}

    def test_too_many_iterations(self, test_client):
        data = {
            "algorithm": "sums",
            "matrix": "1,2,3\n4,5,6",
            "parameters": "iterator=fixed-1000"
        }
        resp = test_client.get("/run/", query_string=data)
        assert resp.status_code == 400
        err_msg = "Cannot perform more than 200 iterations"
        assert resp.json == {"ok": False, "error": err_msg}
