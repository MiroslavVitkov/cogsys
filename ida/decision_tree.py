#!/usr/bin/env python3


# Problem setup
# Problem setup and tests written by Scheffer, Prasse, Makowski, Jaeger.
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# Entropy of a vector of labels
from collections import Counter
def entropy(y):
    p = [ count / len(y) for count in Counter(y).values() ]
    S = -sum( [ pi * np.log2(pi) for pi in p ] )
    return S


# Tests
def equal(a, b):
    epsilon = 1e-6
    return abs(a - b) < epsilon

assert( entropy(np.array([1,1,0,0])) == 1 )
assert( entropy(np.array([0,0])) == 0 )
assert( equal(entropy(np.array([1,1,0,0,1,1])), 0.91829586029052734) )


# Information gain of a binary split of labels.
def split(vals, labels, predicate):
    '''Return labels of left and right partution.'''
    left = [ l for v, l in zip(vals, labels) if predicate(v) ]
    right = [ l for v, l in zip(vals, labels) if not predicate(v) ]
    return left, right

def info_gain(x,y,t):
    left, right = split(x, y, lambda val: val > t)
    term = lambda l: - len(l)*(1/len(y))*entropy(l)
    S = entropy(y) + term(left) + term(right)
    return S


# Tests
assert( equal(info_gain(np.array([1,2,3,4,5,6,7,8,9,10]),np.array([1,1,1,1,1,0,0,0,0,0]),1), 0.10803163030328733) )
assert( equal(info_gain(np.array([1,2,3,4,5,6,7,8,9,10]),np.array([1,1,1,1,1,0,0,0,0,0]),3), 0.39581562117481894) )
assert( equal(info_gain(np.array([1,2,3,4,5,6,7,8,9,10]),np.array([1,1,1,1,1,0,0,0,0,0]),5), 1) )
assert( equal(info_gain(np.array([1,2,3,4,5,6,7,8,9,10]),np.array([1,1,1,1,1,0,0,0,0,0]),6), 0.60998651623672373) )


# Simulate and visualize measurements in two classes.
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples=500, centers=((0,0),(3,3)))
plt.scatter(X[:,0], X[:,1], c=y)

# Search for an optimal split along a single variable/parameter/input dimension.
def find_best_split(x, y):
    def gain_ratio(vals, labels, split_val):
        gr = info_gain(vals, labels, split_val) / entropy(y)
        return gr

    gr = { xi: gain_ratio(x, y, xi) for xi in x }
    treshold = max(gr, key=gr.get)
    return treshold


# Tests
assert find_best_split(np.array([1,2,3,4,5,6,7,8,9,10]),np.array([1,1,1,1,1,0,0,0,0,0])) == 5
assert find_best_split(np.array([1,2,2,4,5,6,7,8,9,10]),np.array([1,1,0,0,1,0,0,1,0,0])) == 8 


# Split a 2-feature dataset by each of the features and chose the beer one.
label = y
x_best = find_best_split(X[:,0],label)
y_best = find_best_split(X[:,1],label)
plt.scatter(X[:,0], X[:,1], c=y)
plt.axvline(x_best)
plt.axhline(y_best)

from sklearn.metrics import accuracy_score as acc
print(acc(y, tuple(1 if v > x_best else 0 for v in X[:,0]) ) )
print(acc(y, tuple(1 if v > y_best else 0 for v in X[:,1]) ) )


# Problem setup.
from sklearn.tree import DecisionTreeClassifier

clf_tree = DecisionTreeClassifier(criterion='entropy', max_depth=1)
clf_tree.fit(X, y)


# Plot misqualified instances.
predicted = clf_tree.predict(X)
plt.scatter(X[:,0], X[:,1], c=y+10*(predicted==y))


# Experiment with better parameters.
clf_tree = DecisionTreeClassifier(criterion='entropy', max_depth=4)
clf_tree.fit(X, y)
predicted = clf_tree.predict(X)
plt.scatter(X[:,0], X[:,1], c=y+10*(predicted==y))
