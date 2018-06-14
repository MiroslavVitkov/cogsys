#!/usr/bin/env python3


# Boilerplate and tests not written by me.


import numpy as np


def d_DTW(x, x2, dist):
    t1, t2 = len(x), len(x2)

    if x == [] and x2 == []:
        return 0.0
    elif (x == []) or (x2 == []):
        return np.infty

    dp = np.empty((t1+1, t2+1))
    dp[0, 0] = 0

    for i in range(1, t1+1):
        dp[i, 0] = np.infty
    for j in range(1, t2+1):
        dp[0, j] = np.infty

    # WRITE YOU CODE HERE
    def calc_cell(i, j):
        if i == 0 and j == 0:
            return 0
        try:
            # (i, j) coordinates shifted from dp[]
            sample1 = x[i-1]
            sample2 = x2[j-1]
        except:
            return np.infty
        neighbours = (dp[i-1, j-1], dp[i-1, j], dp[i, j-1])
        return dist(sample1, sample2) + np.min(neighbours)

    for i in range(1, np.shape(dp)[0]):
        for j in range(1, np.shape(dp)[1]):
            dp[i, j] = calc_cell(i, j)
    assert dp[0, 0] == 0, 'Don`t overwrite (0,0)!'
    print('Distances:\n', dp)


    return dp[t1, t2]


assert d_DTW([1, 2, 3, 3], [1, 2, 3], lambda x, y: 1 if x != y else 0) == 0.0
assert d_DTW([1, 2, 3, 4], [1, 2, 3], lambda x, y: 1 if x != y else 0) == 1.0
assert d_DTW([1, 2, 3, 2], [1, 2], lambda x, y: 1 if x != y else 0) == 1.0
assert d_DTW([], [1, 2], lambda x, y: 1 if x != y else 0) == np.infty
assert d_DTW([], [], lambda x, y: 1 if x != y else 0) == 0.0
