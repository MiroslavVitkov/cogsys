#!/usr/bin/env python3


import numpy as np
#import matplotlib.pyplot as plt
from scipy.stats import uniform
from scipy.stats import norm


def uniform_generator(a, b):
    assert a <= b
    while True:
        # No idea where does scipy get its seed from,
        # but every two unseeded uniform distributions
        # seem to produce unindentical results.

        # 'This distribution is constant between loc and loc + scale.'
        loc = a
        scale = b - loc
        d = uniform(loc=loc, scale=scale)
        yield d.rvs()


def normal_generator(mean, std):
    assert std >= 0
    while True:
        # 'The location (loc) keyword specifies the mean.
        # The scale (scale) keyword specifies the standard deviation.'
        d = norm(loc=mean, scale=std)
        yield d.rvs()


def data_generator(f, x_gen, noise_gen):
    while True:
        x = x_gen.__next__()
        e = noise_gen.__next__()
        y = f(x) + e
        yield x, y


# This code block was not written by me.
import itertools
num_gen = uniform_generator(1, 5)
numbers = [num_gen.__next__() for _ in range(1000)]
assert([1 <= num and num <= 5 for num in numbers])
def constant_generator(c):
    while True:
        yield c
data_gen = data_generator(lambda x: x**2, uniform_generator(-1, 1), constant_generator(0))
assert(all([x**2 == y for x, y in itertools.islice(data_gen, 0, 1000)]))
