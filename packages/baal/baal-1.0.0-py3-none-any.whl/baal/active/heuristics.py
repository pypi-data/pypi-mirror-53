import numpy as np
import scipy.stats
from scipy.special import softmax
from torch import Tensor


def _shuffle_subset(data: np.ndarray, shuffle_prop: float) -> np.ndarray:
    to_shuffle = np.nonzero(np.random.rand(data.shape[0]) < shuffle_prop)[0]
    data[to_shuffle, ...] = data[np.random.permutation(to_shuffle), ...]
    return data


def require2d(fn):
    """
    Will take the mean of the iterations if needed.
    Args:
        fn: Heuristic function with args
            probabilities , shuffle_prop=0.0, threshold=None

    Returns:
        fn : Array -> Float -> Array

    """

    def wrapper(self, probabilities):
        if probabilities.ndim == 3:
            # Expected shape : [n_sample, n_classes, n_iterations]
            probabilities = probabilities.mean(-1)
        return fn(self, probabilities)

    return wrapper


def requireprobs(fn):
    """Will convert logits to probs if needed"""

    def wrapper(self, probabilities):
        bounded = np.min(probabilities) < 0 or np.max(probabilities) > 1.
        if bounded or not np.allclose(probabilities.sum(1), 1):
            probabilities = softmax(probabilities, 1)
        return fn(self, probabilities)

    return wrapper


class AbstractHeuristic:
    def __init__(self, shuffle_prop=0.0, threshold=None, reverse=False):
        """
        Abstract class that defines a Heuristic
        Args:
            shuffle_prop: float, shuffle proportion
            threshold: Optional(float), threshold the probabilities (NOT USED)
            reverse: bool, True if the most uncertain sample has the hightest value.
        """
        self.shuffle_prop = shuffle_prop
        self.threshold = threshold
        self.reversed = reverse

    def compute_score(self, predictions):
        """
        Compute the score according to the heuristic.
        Args:
            predictions:

        Returns:

        """
        raise NotImplementedError

    def get_uncertainties(self, predictions):
        """Get the uncertainties"""
        if isinstance(predictions, Tensor):
            predictions = predictions.numpy()
        return self.compute_score(predictions)

    def get_ranks(self, predictions):
        """Rank the predictions according to their uncertainties."""
        scores = self.get_uncertainties(predictions)
        ranks = np.argsort(scores, -1)
        if self.threshold:
            ranks = np.asarray([idx for idx in ranks if np.amax(predictions[idx]) > self.threshold])
        if self.reversed:
            ranks = ranks[::-1]
        ranks = _shuffle_subset(ranks, self.shuffle_prop)
        return ranks

    def __call__(self, predictions):
        """Rank the predictions according to their uncertainties."""
        return self.get_ranks(predictions)


class BALD(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        """Sort by the highest acquisition function value"""
        super().__init__(shuffle_prop=shuffle_prop, threshold=threshold, reverse=True)

    @requireprobs
    def compute_score(self, predictions):
        assert predictions.ndim == 3

        expected_entropy = - np.mean(np.sum(predictions * np.log(predictions + 1e-10), axis=1),
                                     axis=-1)  # [batch size]
        expected_p = np.mean(predictions, axis=-1)  # [batch_size, n_classes]
        entropy_expected_p = - np.sum(expected_p * np.log(expected_p + 1e-10),
                                      axis=-1)  # [batch size]
        bald_acq = entropy_expected_p - expected_entropy
        return bald_acq


class Variance(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        """Sort by the highest variance"""
        super().__init__(shuffle_prop=shuffle_prop, threshold=threshold, reverse=True)

    def compute_score(self, predictions):
        assert predictions.ndim == 3
        return np.var(predictions, -1)


class Entropy(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        """Sort by the highest entropy"""
        super().__init__(shuffle_prop=shuffle_prop, threshold=threshold, reverse=True)

    @require2d
    @requireprobs
    def compute_score(self, predictions):
        return scipy.stats.entropy(predictions.T)


class Margin(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        """Sort by the lowest maergin"""
        super().__init__(shuffle_prop=shuffle_prop, threshold=threshold, reverse=False)

    @require2d
    @requireprobs
    def compute_score(self, predictions):
        sort_arr = np.sort(predictions, axis=1)
        return sort_arr[:, -1] - sort_arr[:, -2]


class Certainty(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        """Sort by the lowest certainty"""
        super().__init__(shuffle_prop=shuffle_prop, threshold=threshold, reverse=False)

    @require2d
    def compute_score(self, predictions):
        return np.max(predictions, axis=1)


class Random(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        """Random heuristic."""
        super().__init__(1.0, threshold, False)

    @require2d
    def compute_score(self, predictions):
        return np.arange(predictions.shape[0])


class Epistemic(AbstractHeuristic):
    def __init__(self, shuffle_prop=0.0, threshold=None):
        super().__init__(shuffle_prop, threshold, reverse=True)

    @requireprobs
    def compute_score(self, predictions):
        mean = predictions.mean(-1)
        var = -1. * np.sum(np.log(mean + 1e-5) * mean, 1)

        return var
