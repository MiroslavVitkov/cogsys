#!/usr/bin/env python3


# An excercise on the Logistic Regression classification algorith.


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
    return ll1(X, y, weights)


def ll1(X, y, weights):
    # Iterative implementation.
    ll = 0
    for xi, yi in zip(X, y):
        wx = np.dot(weights.T, xi)
        ln = np.log(1 + np.exp(wx))
        ll = ll + yi * wx - ln
    return ll


def ll2(X, y, weights):
    # Matrix product implementation.
    cost = np.dot( y.T, np.dot(weights, X.T))
    WX = np.dot( weights, X.T )
    ln = - np.log( 1 + np.exp( WX ) )
    reg = np.dot( ln, [1,] * X.shape[0] )  # Sum the column vector.
    return cost + reg


def sigmoid(scores):
    return np.array( [1 / (1 + np.exp(-s)) for s in scores] )


def log_likelihood_gradient(X, y, weights):
    # The provided formula asks us to transpose X here,
    # but that would result in incompatible dimensions.
    s = sigmoid(np.dot(X, weights))
    gradient = np.dot(X.T, y - s)
    return gradient


iterations = int(1e3)
weights = logistic_regression( X=X_train
                             , y=y_train
                             , num_steps=iterations
                             , learning_rate=1e-4
                             , add_intercept=True )
print()

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression( max_iter=iterations, C=1000 )
clf.fit( X_train, y_train )

# Weights
print( weights )
print( clf.intercept_, clf.coef_ )

# Predictions on training data.
# sigmoid() is larger than 0.5 for positive parameter.
# The decision treshold probability for binary labels is 0.5.
# Therefore, for classification we only need to look at the sign of (x.T w).
bias = weights[0]
w = weights[1:]
preds = np.sign( bias + np.dot( X_train, w.T ) )
preds = [ (p+1)/2 for p in preds ]  # [-1; 1] -> [0; 1]
print( 'Your accuracy: {0}'.format((preds == y_train).sum().astype(float) / len(preds)) )
print( 'Sklearn\'s accuracy: {0}'.format(clf.score(X_train, y_train)) )

