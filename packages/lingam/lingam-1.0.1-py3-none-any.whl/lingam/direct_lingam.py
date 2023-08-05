"""
Python implementation of the LiNGAM algorithms.
The LiNGAM Project: https://sites.google.com/site/sshimizu06/lingam
"""

import numpy as np
from sklearn.utils import check_array

from .base import _BaseLiNGAM


class DirectLiNGAM(_BaseLiNGAM):
    """Implementation of DirectLiNGAM Algorithm [1]_ [2]_

    References
    ----------
    .. [1] S. Shimizu, T. Inazumi, Y. Sogawa, A. Hyvärinen, Y. Kawahara, T. Washio, P. O. Hoyer and K. Bollen. 
       DirectLiNGAM: A direct method for learning a linear non-Gaussian structural equation model. Journal of Machine Learning Research, 12(Apr): 1225--1248, 2011.
    .. [2] A. Hyvärinen and S. M. Smith. Pairwise likelihood ratios for estimation of non-Gaussian structural eauation models. 
       Journal of Machine Learning Research 14:111-152, 2013. 
    """

    def __init__(self, random_state=None):
        """Construct a DirectLiNGAM model.

        Parameters
        ----------
        random_state : int, optional (default=None)
            ``random_state`` is the seed used by the random number generator.
        """
        super().__init__(random_state)

    def fit(self, X):
        """Fit the model to X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data, where ``n_samples`` is the number of samples
            and ``n_features`` is the number of features.

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        X = check_array(X)

        U = np.arange(X.shape[1])
        K = []
        X_ = np.copy(X)
        for _ in range(X.shape[1]):
            m = self._search_causal_order(X_)
            for i in range(X_.shape[1]):
                if i != m:
                    X_[:, i] = self._residual(X_[:, i], X_[:, m])
            K.append(U[m])
            U = np.delete(U, m)
            X_ = np.delete(X_, m, 1)

        self._causal_order = K
        return self._estimate_adjacency_matrix(X)

    def _residual(self, xi, xj):
        """The residual when xi is regressed on xj."""
        return xi - (np.cov(xi, xj)[0, 1] / np.var(xj)) * xj

    def _entropy(self, u):
        """Calculate entropy using the maximum entropy approximations."""
        k1 = 79.047
        k2 = 7.4129
        gamma = 0.37457
        return (1 + np.log(2 * np.pi)) / 2 - \
            k1 * (np.mean(np.log(np.cosh(u))) - gamma)**2 - \
            k2 * (np.mean(u * np.exp((-u**2) / 2)))**2

    def _diff_mutual_information(self, xi, xj):
        """Calculate the difference of the mutual informations."""
        xi_std = (xi - np.mean(xi)) / np.std(xi)
        xj_std = (xj - np.mean(xj)) / np.std(xj)
        ri_j = self._residual(xi_std, xj_std)
        rj_i = self._residual(xj_std, xi_std)
        return (self._entropy(xj_std) + self._entropy(ri_j / np.std(ri_j))) - \
            (self._entropy(xi_std) + self._entropy(rj_i / np.std(rj_i)))

    def _search_causal_order(self, X):
        """Search the causal ordering."""
        M_list = []
        for i in range(X.shape[1]):
            M = 0
            for j in np.delete(range(X.shape[1]), i):
                M += np.min([0, self._diff_mutual_information(X[:, i], X[:, j])])**2
            M_list.append(-1.0 * M)
        return np.argmax(M_list)
