#!/usr/bin/env python3

# Test data imposed by assignment,
EISNER_STATES = ['C','H']
EISNER_INITIAL_PROBS = {'C': 0.2, 'H': 0.8}
EISNER_TRANSITIONS = {'C': {'C':0.6, 'H': 0.4}, 'H': {'C':0.3, 'H':0.7}}
EISNER_EMISSIONS = {'C': {'1':0.5,'2':0.4,'3':0.1},'H': {'1':0.2, '2':0.4,'3':0.4}}

# Test case - should yield 'HHH'.
OBSERVATIONS = ['3', '1', '3']
HIDDEN_STATES = 'HHH'


class Node:
    '''A time-state point in the 2D Viterbi trellis.'''
    def __init__(self, state='', prob=float('NaN'), path=''):
        self.state = state
        self.prob = prob
        self.path = path  # concatinated state names


def viterbi_init(state_names, probs):
    '''Generate trellis nodes for time==0.'''
    return [Node(s, probs[s]) for s in state_names]


def viterbi_step(states, obs, a, b):
    '''
    Perform a single step of the Viterbi algorithm.
    Initial states and termination are not handled.

    nodes - a list of all Node objects for previous time step
    obs - the observation for the current time step
    a - transition probabilities, map of maps
    b - emission probabilities, map of maps
    return - a list of all Node objects for current time step
    '''
    ret = list(states)
    for curr in ret:
        probs = {prev.state:
                 prev.prob * a[prev.state][curr.state] * b[curr.state][obs]
                 for prev in states}
        best = max(probs, key=probs.get)
        curr.prob = probs[best]
        curr.path += best
    return ret


if __name__ == "__main__":
    states = viterbi_init(EISNER_STATES, EISNER_INITIAL_PROBS)
    for o in OBSERVATIONS:
        states = viterbi_step(states, o, EISNER_TRANSITIONS, EISNER_EMISSIONS)
    assert max(states, key=lambda x: x.prob).path == HIDDEN_STATES
