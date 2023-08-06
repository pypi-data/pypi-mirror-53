import numpy as np

from truthdiscovery.algorithm.base import BaseIterativeAlgorithm
from truthdiscovery.exceptions import EarlyFinishError
from truthdiscovery.utils.iterator import ConvergenceIterator, DistanceMeasures


class TruthFinder(BaseIterativeAlgorithm):
    """
    TruthFinder by Yin, Han, Yu.
    """
    influence_param = 0.5
    dampening_factor = 0.3
    initial_trust = 0.9

    def __init__(self, *args, influence_param=None, dampening_factor=None,
                 initial_trust=None, **kwargs):
        """
        :param influence_param:  A number in [0, 1] that controls how much
                                 influence related claims have on confidence
                                 scores (rho in the paper)
        :param dampening_factor: A number in (0, 1) that prevents overly high
                                 confidence when sources are not independent
                                 (gamma in the paper)
        :param initial_trust:    Initial trust value for each source
        """
        if influence_param is not None:
            self.influence_param = influence_param
        if dampening_factor is not None:
            self.dampening_factor = dampening_factor
        if initial_trust is not None:
            self.initial_trust = initial_trust

        super().__init__(*args, **kwargs)

    def get_default_iterator(self):
        """
        Use cosine convergence iterator by default, as described in the paper
        """
        return ConvergenceIterator(DistanceMeasures.COSINE, 0.001)

    @classmethod
    def get_log_trust(cls, trust):
        """
        Return the 'tau' vector as defined in the TruthFinder paper. This
        involves taking logs to convert trust in [0, 1] to [0, +inf) to prevent
        numerical underflow

        :param trust: numpy array of trust values
        :return:      tau vector
        """
        if np.any(trust == 1):
            raise EarlyFinishError(
                "Trust has become 1 for at least one source"
            )
        return -np.log(1 - trust)

    def _run(self, data):
        trust = np.zeros((data.num_sources,))

        claim_counts = data.sc @ np.ones((data.num_claims),)
        # As in Investment, use multiply() to make sure the result is sparse
        a_mat = data.sc.T.multiply(1 / claim_counts).T
        b_mat = data.sc.T + self.influence_param * (data.imp.T @ data.sc.T)

        trust = np.full((data.num_sources,), self.initial_trust)
        belief = np.zeros((data.num_claims,))
        self.log(data, trust, belief)

        while not self.iterator.finished():
            try:
                log_belief = b_mat @ self.get_log_trust(trust)
            except EarlyFinishError:
                break
            belief = 1 / (1 + np.exp(-self.dampening_factor * log_belief))
            new_trust = a_mat @ belief
            self.iterator.compare(new_trust, trust)
            trust = new_trust
            self.log(data, trust, belief)

        return trust, belief
