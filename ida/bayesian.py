#!/usr/bin/env python3


import numpy as np
from numpy.linalg import inv
#import matplotlib.pyplot as plt
from scipy.stats import uniform
from scipy.stats import norm


def uniform_generator(a, b):
    assert a <= b  # This allows a dirac delta.
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
    assert std >= 0  # Again.
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


# Following two code blocks were not written by me.
import itertools
num_gen = uniform_generator(1, 5)
numbers = [num_gen.__next__() for _ in range(1000)]
assert([1 <= num and num <= 5 for num in numbers])
def constant_generator(c):
    while True:
        yield c
data_gen = data_generator(lambda x: x**2, uniform_generator(-1, 1), constant_generator(0))
assert(all([x**2 == y for x, y in itertools.islice(data_gen, 0, 1000)]))


sigma   = 2.5 # sigma of the noise, do not change this!
data_gen = data_generator(lambda x: 5*x + 3, uniform_generator(0, 5), normal_generator(0, sigma))
data = list(itertools.islice(data_gen, 0, 100)) # list of pairs (x, y)
x, y = zip(*data) # The asterisk unpacks data; i.e., this line corresponds to x,y=zip((x[0], y[0]), ((x[1], y[1])), ...) 
X = np.column_stack((np.asarray(x), np.ones(len(x))))


def square_mat(X):
    return np.dot(np.transpose(X), X)


def num_features(X):
    return np.shape(X)[1]


def get_MAP(X, y, sigma, sigma_p):
    sigma_mat = ((sigma**2) / (sigma_p**2)) * np.eye(num_features(X))
    inverted = inv(square_mat(X) + sigma_mat)
    labels = np.dot(np.transpose(X), y)
    theta_MAP =  np.dot(inverted, labels)
    return theta_MAP


def get_posterior_distribution_parameters(X, y, sigma, sigma_p):
    theta_MAP = get_MAP(X, y, sigma, sigma_p)
    sigma_inv = (1/sigma**2)*square_mat(X) + (1/sigma_p**2)*np.eye(num_features(X))
    covariance_matrix = inv(sigma_inv)
    return theta_MAP, covariance_matrix


# Another chunk of external code.
# Those should have been externalised as a separate module,
# given sufficient time and motivation.
sigma_p = 5
theta_MAP = get_MAP(X, y, sigma=sigma, sigma_p=sigma_p)
print("theta (MAP estimate): {}".format(theta_MAP))
theta_MAP, Sigma = get_posterior_distribution_parameters(X, y, sigma, sigma_p)
