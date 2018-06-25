#!/usr/bin/env python3


import numpy as np


# Not my code:
np.random.seed(1)
num_observations = 2000

x_class1 = np.random.multivariate_normal([0, 0], [[1, .25],[.25, 1]], num_observations)
x_class2 = np.random.multivariate_normal([1, 4], [[1, .25],[.25, 1]], num_observations)

# Training data:
X_train = np.vstack((x_class1, x_class2)).astype(np.float32)
y_train = np.hstack((np.zeros(num_observations), np.ones(num_observations))) # labels are 0, 1


def logistic_regression(X, y, num_steps, learning_rate, add_intercept):
    # X: n x d matrix of instances
    # y: vector of n labels

    if add_intercept:
        intercept = np.ones((X.shape[0], 1))
        X = np.hstack((intercept, X))

    weights = np.zeros(X.shape[1])

    for step in range(num_steps):
        scores = np.dot(X, weights)
        predictions = sigmoid(scores)

        gradient = log_likelihood_gradient(X, y, weights)
        weights -= learning_rate * gradient

        if step % 10000 == 0:
            print(log_likelihood(X, y, weights))
        if step % 20 == 0:
            print('.', end='', flush=True)

    return weights


# My code:
def log_likelihood(X, y, weights):
    # Lazy implementation - dataset needn't fit into main memory.
    ll = 0
    for xi, yi in zip(X, y):
        wx = np.dot(weights.T, xi)
        ln = np.log(1 + np.exp(wx))
        ll = ll + yi * wx - ln
    return ll


def sigmoid(scores):
    def sig(score):
        return 1 / (1 + np.exp(-score))
    s = np.array( [sig(score) for score in scores] )
    return s


def log_likelihood_gradient(X, y, weights):
    # The provided formula asks us to transpose X here,
    # but that would result in incompatible dimensions.
    s = sigmoid(np.dot(X, weights))
    gradient = np.dot(X.T, y - s)
    return gradient


logistic_regression( X=X_train
                   , y=y_train
                   , num_steps=20000
                   , learning_rate=1e-5
                   , add_intercept=False )
