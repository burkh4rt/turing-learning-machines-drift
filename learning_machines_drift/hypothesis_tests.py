"""TODO PEP 257"""

from typing import Any, Callable

import numpy as np
import numpy.typing as npt
from scipy import stats
from sdmetrics.single_table import (  # type: ignore
    GMLogLikelihood,
    KSTest,
    LogisticDetection,
)

from learning_machines_drift.types import Dataset

# from sdv.evaluation import evaluate
# from sdv.metrics.tabular import KSTest


class HypothesisTests:
    """TODO PEP 257"""

    def __init__(self, reference_dataset: Dataset, registered_dataset: Dataset) -> None:
        """TODO PEP 257"""
        self.reference_dataset = reference_dataset
        self.registered_dataset = registered_dataset

    def _calc(self, func: Callable[[npt.ArrayLike, npt.ArrayLike], Any]) -> Any:
        """TODO PEP 257"""
        results = {}
        for feature in self.reference_dataset.feature_names:
            ref_col = self.reference_dataset.features[feature]
            reg_col = self.registered_dataset.features[feature]
            results[feature] = func(ref_col, reg_col)
        return results

    def scipy_kolmogorov_smirnov(self, verbose=True) -> Any:  # type: ignore
        """TODO PEP 257"""
        method = "SciPy Kolmogorov Smirnov"
        description = ""
        about_str = "\nMethods: {method}\nDescription:{description}"
        about_str = about_str.format(method=method, description=description)

        results = self._calc(stats.ks_2samp)
        if verbose:
            print(about_str)
        return results

    def sdv_kolmogorov_smirnov(self, verbose=True) -> Any:  # type: ignore
        """TODO PEP 257"""
        method = "SDV Kolmogorov Smirnov"
        description = """This metric uses the two-sample Kolmogorov–Smirnov
                        test to compare the distributions
                        of continuous columns using the empirical CDF.
                        \n The output for each column is 1 minus the KS
                        Test D statistic, which indicates the
                        maximum distance between the expected CDF and the
                        observed CDF values."""
        about_str = "\nMethod: {method}\nDescription:{description}"
        about_str = about_str.format(method=method, description=description)

        # TODO: check the computation process for KSTest unify, do we want this
        # to include the labels?
        results = KSTest.compute(
            self.reference_dataset.unify(), self.registered_dataset.unify()
        )

        if verbose:
            print(about_str)
        return results

    @staticmethod
    def _chi_square(data1: npt.ArrayLike) -> Any:
        """TODO PEP 257"""
        d1_counts = np.unique(data1, return_counts=True)
        d2_counts = np.unique(data1, return_counts=True)

        return stats.chisquare(d1_counts, d2_counts)

    def gaussian_mixture_log_likelihood(self, verbose=True) -> Any:  # type: ignore
        """TODO PEP 257"""
        method: str = "Gaussian Mixture Log Likelihood"
        description = """This metric fits multiple GaussianMixture models
        to the real data and then evaluates
        the average log likelihood of the synthetic data on them."""
        about_str = "\nMethod: {method}\nDescription:{description}"
        about_str = about_str.format(method=method, description=description)

        if verbose:
            print(about_str)

        results = GMLogLikelihood.compute(
            self.reference_dataset.unify(), self.registered_dataset.unify()
        )
        return results

    def logistic_detection(self, verbose=True) -> Any:  # type: ignore
        """TODO PEP 257"""
        method = "Logistic Detection"
        description = "Detection metric based on a LogisticRegression classifier from scikit-learn."
        about_str = "\nMethod: {method}\nDescription:{description}"
        about_str = about_str.format(method=method, description=description)

        if verbose:
            print(about_str)
        results = LogisticDetection.compute(
            self.reference_dataset.unify(), self.registered_dataset.unify()
        )
        return results

    # def sd_evaluate(self, verbose=True) -> Any:
    #     method = "SD Evaluate"
    #     description = "Detection metric based on a LogisticRegression
    #     classifier from scikit-learn"
    #     about_str = "\nMethod: {method}\nDescription:{description}"
    #     about_str = about_str.format(method=method, description=description)

    #     if verbose:
    #         print(about_str)
    #     results = evaluate(
    #         self.reference_dataset.unify(),
    #         self.registered_dataset.unify(),
    #         aggregate=False,
    #     )
    #     return results
