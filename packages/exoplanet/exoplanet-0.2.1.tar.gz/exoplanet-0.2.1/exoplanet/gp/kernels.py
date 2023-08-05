# -*- coding: utf-8 -*-

__all__ = []

import numpy as np

import theano
import theano.tensor as tt


class Kernel:

    parameter_names = tuple()

    def __init__(self, **kwargs):
        self.dtype = kwargs.pop("dtype", theano.config.floatX)
        for name in self.parameter_names:
            if name not in kwargs and "log_" + name not in kwargs:
                raise ValueError(
                    (
                        "Missing required parameter {0}. "
                        "Provide {0} or log_{0}"
                    ).format(name)
                )
            value = (
                kwargs[name]
                if name in kwargs
                else tt.exp(kwargs["log_" + name])
            )
            setattr(self, name, tt.cast(value, self.dtype))

    def __add__(self, b):
        dtype = theano.scalar.upcast(self.dtype, b.dtype)
        return KernelSum(self, b, dtype=dtype)

    def __radd__(self, b):
        dtype = theano.scalar.upcast(self.dtype, b.dtype)
        return KernelSum(b, self, dtype=dtype)

    def __mul__(self, b):
        dtype = theano.scalar.upcast(self.dtype, b.dtype)
        return KernelProduct(self, b, dtype=dtype)

    def __rmul__(self, b):
        dtype = theano.scalar.upcast(self.dtype, b.dtype)
        return KernelProduct(b, self, dtype=dtype)


class KernelSum(Kernel):
    def __init__(self, *terms, **kwargs):
        self.terms = terms
        super(KernelSum, self).__init__(**kwargs)


class KernelProduct(Kernel):
    def __init__(self, *terms, **kwargs):
        self.terms = terms
        super(KernelProduct, self).__init__(**kwargs)


class TestKernel(Kernel):

    parameter_names = ("tau",)

    def value(self, X1, X2):
        return tt.exp(
            -0.5
            * tt.sum(
                tt.square(tt.shape_padaxis(X1, 1) - tt.shape_padaxis(X2, 0)),
                axis=-1,
            )
            / self.tau ** 2
        )
