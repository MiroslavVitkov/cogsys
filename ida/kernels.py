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
#    print('Distances:\n', dp)


    return dp[t1, t2]


assert d_DTW([1, 2, 3, 3], [1, 2, 3], lambda x, y: 1 if x != y else 0) == 0.0
assert d_DTW([1, 2, 3, 4], [1, 2, 3], lambda x, y: 1 if x != y else 0) == 1.0
assert d_DTW([1, 2, 3, 2], [1, 2], lambda x, y: 1 if x != y else 0) == 1.0
assert d_DTW([], [1, 2], lambda x, y: 1 if x != y else 0) == np.infty
assert d_DTW([], [], lambda x, y: 1 if x != y else 0) == 0.0


def d1(x, x2):
    # WRITE YOU CODE HERE
    return np.abs(x-x2)

def d2(x, x2):
    # WRITE YOU CODE HERE
    return (x-x2)**2

def d3(x, x2):
    # WRITE YOU CODE HERE
    return np.abs(x-x2)**3


k1_hyp, k2_hyp, k3_hyp = [lambda lmbd: (lambda x, x2: np.exp(-lmbd * d_DTW(x, x2, d))) for d in [d1, d2, d3]]
k1 = k1_hyp(2.0)
k2 = k2_hyp(2.0)
k3 = k3_hyp(2.0)


def build_dtw_gram_matrix(xs, x2s, k):
    """
    xs: collection of sequences (vectors of possibly varying length)
    x2s: the same, needed for prediction
    k: a kernel function that maps two sequences of possibly different length to a real
    The function returns the Gram matrix with respect to k of the data xs.
    """
    t1, t2 = len(xs), len(x2s)
    K = np.empty((t1, t2))

    for i in range(t1):
        for j in range(i, t2):
            K[i, j] = k(xs[i], x2s[j])
            if i < t2 and j < t1:
                K[j, i] = K[i, j]
    return K


build_dtw_gram_matrix([[1, 2], [2, 3]], [[1, 2, 3], [4]], k1)


def L2_reg(w, lbda):
    return 0.5 * lbda * (np.dot(w.T, w)), lbda*w

def hinge_loss(h, y):
    print('hinge loss ', np.shape(h), np.shape(y))
    n = len(h)
    l = np.maximum(0, np.ones(n) - y*h)
    g = -y * (h > 0)
    return l, g


def learn_reg_kernel_ERM(X, y, lbda, k, loss=hinge_loss, reg=L2_reg, max_iter=200, tol=0.001, eta=1., verbose=False):
    """Kernel Linear Regression (default: kernelized L_2 SVM)
    X -- data, each row = instance
    y -- vector of labels, n_rows(X) == y.shape[0]
    lbda -- regularization coefficient lambda
    k -- the kernel function
    loss -- loss function, returns vector of losses (for each instance) AND the gradient
    reg -- regularization function, returns reg-loss and gradient
    max_iter -- max. number of iterations of gradient descent
    tol -- stop if norm(gradient) < tol
    eta -- learning rate
    """
    num_features = X.shape[1]
    g_old = None


    K = build_dtw_gram_matrix(X, X, k)
    w = np.array([np.random.randn(num_features) for i in range((K.shape[0]))])

    for _ in range(max_iter):
#        h = []
#        h = np.dot(X.T, w)
        h = predict(w, X, X, k)
        print('X, h = ', np.shape(X), np.shape(h))
        print('h = ', h)
        l, lg = loss(h, y)

        if verbose:
            print('training loss: ' + str(np.mean(l)))

        r, rg = reg(w, lbda)
        g = lg + rg

        def d(x1, x2):
            # Gram matrix K changes scalar product from <x, x'> = x^T x to x^T K x
            lhs = np.dot(x1.T, K)
            return np.dot(lhs, x2)
        if g_old is not None:
            eta = eta*(d(g_old, g_old))/(d((g_old - g), g_old))

        w = w - eta*g
        if (np.linalg.norm(eta*g)<tol):
            break
        g_old = g

    return w, K


def predict(alpha, X, X_train, k):
    K = build_dtw_gram_matrix(X_train, X, k)
    y_pred = np.dot(K, alpha)
    y_pred[y_pred >= 0] = 1
    y_pred[y_pred < 0] = -1
    return y_pred


import os
from scipy.io import loadmat # for matlab *.mat format, for modern once need to install hdf5

file_path = "laser_small.mat" # file path for multi os support
mat = loadmat(file_path)

X = mat['X']
y = mat['Y'].reshape(50)

print(X.shape, y.shape)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

print(X_train.shape, X_test.shape)


alpha, K = learn_reg_kernel_ERM(X_train, y_train, lbda=1, k=k2, max_iter=20000, eta=1, tol=1e-3, verbose=True)


y_pred = predict(alpha, X_train, X_train, k2)
print("Training Accuracy: {}".format(np.mean(y_train == y_pred)))
print("Test Accuracy: {}".format(np.mean(y_test == predict(alpha,X_train, X_test, k2))))
print("Shape of alpha {}".format(alpha.shape))
