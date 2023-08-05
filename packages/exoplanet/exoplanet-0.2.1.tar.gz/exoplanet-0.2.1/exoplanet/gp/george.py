# -*- coding: utf-8 -*-

__all__ = ["GeneralGP"]

import numpy as np
import theano.tensor as tt

from ..theano_ops.celerite.diag_dot import DiagDotOp

diag_dot = DiagDotOp()


class GeneralGP:
    def __init__(self, kernel, X, diag, model=None):
        self.kernel = kernel
        self.X = tt.as_tensor_variable(X)
        if self.X.ndim < 2:
            self.X = tt.shape_padright(self.X, 2 - self.X.ndim)
        elif self.X.ndim > 2:
            raise ValueError("Input must be 2D")
        self.diag = tt.as_tensor_variable(diag)

        self._K = self.kernel.value(self.X, self.X)
        self._K += tt.diag(self.diag)
        self._factor = tt.slinalg.cholesky(self._K)
        self._log_det = 2 * tt.sum(tt.log(tt.diag(self._factor)))
        self._L_inv_diag = tt.slinalg.solve_lower_triangular(
            self._factor, self.diag
        )

    def apply_inverse(self, y):
        y = tt.as_tensor_variable(y)
        z = tt.slinalg.solve_lower_triangular(self._factor, y)
        return tt.slinalg.solve_upper_triangular(self._factor.T, z)

    def _solve_triangular(self, y):
        y = tt.as_tensor_variable(y)
        return tt.slinalg.solve_lower_triangular(self._factor, y)

    def _log_likelihood(self, z):
        return -0.5 * (
            tt.sum(tt.square(z)) + self._log_det + z.size * np.log(2 * np.pi)
        )

    def log_likelihood(self, y):
        z = self._solve_triangular(y)
        return self._log_likelihood(z)

    def _predict(
        self, y, z, t=None, return_var=False, return_cov=False, kernel=None
    ):
        mu = None
        if t is None and kernel is None:
            mu = y - self._L_inv_diag * z
            if not (return_var or return_cov):
                return mu

        if kernel is None:
            kernel = self.kernel

        if t is None:
            t = self.X
            Kxs = kernel.value(self.X, self.X)
            KxsT = Kxs
            Kss = Kxs
        else:
            t = tt.as_tensor_variable(t)
            KxsT = kernel.value(t, self.X)
            Kxs = tt.transpose(KxsT)
            Kss = kernel.value(t, t)

        if mu is None:
            mu = tt.dot(
                Kxs, tt.slinalg.solve_upper_triangular(self.factor.T, z)
            )

        if not (return_var or return_cov):
            return mu

        KinvKxsT = self.apply_inverse(KxsT)
        if return_var:
            var = -diag_dot(Kxs, KinvKxsT)  # tt.sum(KxsT*KinvKxsT, axis=0)
            var += kernel.value_diagonal(t, t)
            return mu, var

        cov = Kss - tt.dot(Kxs, KinvKxsT)
        return mu, cov

    def predict(
        self, y, t=None, return_var=False, return_cov=False, kernel=None
    ):
        z = self._solve_triangular(y)
        return self._predict(
            y,
            z,
            t=t,
            return_var=return_var,
            return_cov=return_cov,
            kernel=kernel,
        )

    def log_likelihood_and_predict(self, y, **kwargs):
        z = self._solve_triangular(y)
        loglike = self._log_likelihood(z)
        predict = self._predict(y, z, **kwargs)
        return loglike, predict
