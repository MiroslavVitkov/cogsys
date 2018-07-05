#!/usr/bin/env python3


# Exercises over the lecture in neural networks.


# Problem setup.
import numpy as np
from numpy.random import multivariate_normal
from numpy.random import uniform
from scipy.stats import zscore

def init_toy_data(num_samples,num_features, num_classes, seed=3):
    # num_samples: number of samples *per class*
    # num_features: number of features (excluding bias)
    # num_classes: number of class labels
    # seed: random seed
    np.random.seed(seed)
    X=np.zeros((num_samples*num_classes, num_features))
    y=np.zeros(num_samples*num_classes)
    for c in range(num_classes):
        means = uniform(low=-10, high=10, size=num_features)
        var = uniform(low=1.0, high=5, size=num_features)
        cov = var * np.eye(num_features)
        X[c*num_samples:c*num_samples+num_samples,:] = multivariate_normal(means, cov, size=num_samples)
        y[c*num_samples:c*num_samples+num_samples] = c
    return X,y

def init_model(input_size,hidden_size,num_classes, seed=3):
    # input size: number of input features
    # hidden_size: number of units in the hidden layer
    # num_classes: number of class labels, i.e., number of output units
    np.random.seed(seed)
    model = {}
    # initialize weight matrices and biases randomly
    model['W1'] = uniform(low=-1, high=1, size=(input_size, hidden_size))
    model['b1'] = uniform(low=-1, high=1, size=hidden_size)
    model['W2'] = uniform(low=-1, high=1, size=(hidden_size, num_classes))
    model['b2'] = uniform(low=-1, high=1, size=num_classes)
    return model

# create toy data
X,y= init_toy_data(2,4,3) # 2 samples per class; 4 features, 3 classes
# Normalize data
X = zscore(X, axis=0)
print('X: ' + str(X))
print('y: ' + str(y))

# initialize model
model = init_model(input_size=4, hidden_size=10, num_classes=3)

print('model: ' + str(model))
print('model[\'W1\'].shape: ' + str(model['W1'].shape))
print('model[\'W2\'].shape: ' + str(model['W2'].shape))
print('model[\'b1\'].shape: ' + str(model['b1'].shape))
print('model[\'b12\'].shape: ' + str(model['b2'].shape))
print('number of parameters: ' + str((model['W1'].shape[0] * model['W1'].shape[1]) + 
     np.sum(model['W2'].shape[0] * model['W2'].shape[1]) + 
     np.sum(model['b1'].shape[0]) +
     np.sum(model['b2'].shape[0] )))


# <b>Exercise 1</b>: Implement softmax layer.
# $softmax(x_i) = \frac{e^{x_i}}{{\sum_{j\in 1...J}e^{x_j}}}$,
def softmax_one( x ):
    e = [ np.exp( xi ) for xi in x ]
    return e / np.sum( e )


def softmax( X ):
    s = [ softmax_one( x ) for x in X ]
    return np.array( s )


# Check if everything is correct.
x = np.array([[0.1, 0.7],[0.7,0.4]])
exact_softmax = np.array([[ 0.35434369,  0.64565631],
                         [ 0.57444252,  0.42555748]])
sm = softmax(x)
difference = np.sum(np.abs(exact_softmax - sm))
assert difference < 0.000001


# <b>Exercise 2</b>: Implement the forward propagation algorithm for the model defined above.
#
# The activation function of the hidden neurons is a Rectified Linear Unit $relu(x)=max(0,x)$ (to be applied element-wise to the hidden units)
# The activation function of the output layer is a softmax function (as implemented in Exercise 1).
#
# The function should return both the activation of the hidden units
# (after having applied the $relu$ activation function)
# (shape: $(N, num\_hidden)$)$
def relu( H ):
    def f( k ):
        return ((k > 0) * k)

    try:
        ret = [ f( h ) for h in H ]
    except:
        ret = f( H )

    return ret


class NN( object ):
    def __init__( me, model ):
        me._model = model

    def in_to_hid( me, x ):
        lin = np.dot( me._model['W1'].T, x ) + me._model[ 'b1' ]
        act = relu( lin )
        return act

    def hid_to_out( me, h ):
        lin = np.dot( me._model['W2'].T, h ) + me._model[ 'b2' ]
        act = softmax_one( lin )
        return act

    def prop_one( me, x ):
        h = me.in_to_hid( x )
        y = me.hid_to_out( h )
        return h, y

    def prop_many( me, X ):
        H = []
        Y = []
        for x in X:
            h, y = me.prop_one( x )
            H.append( h )
            Y.append( y )

        return np.array( H ), np.array( Y )


def forward_prop( X, model ):
    nn = NN( model )
    return nn.prop_many( X )


acts,probs = forward_prop(X, model)
correct_probs = np.array([[0.22836388, 0.51816433, 0.25347179],
                            [0.15853289, 0.33057078, 0.51089632],
                            [0.40710319, 0.41765056, 0.17524624],
                            [0.85151353, 0.03656425, 0.11192222],
                            [0.66016592, 0.19839791, 0.14143618],
                            [0.70362036, 0.08667923, 0.20970041]])

assert probs.shape==(X.shape[0],len(set(y)))
difference =  np.sum(np.abs(probs - correct_probs))
assert difference < 0.00001


