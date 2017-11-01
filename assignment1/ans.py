#!/usr/bin/python3
"""
Assignment 1 for Natural Language Processing.
Does word frequency plots, Dissociated Press generation
and Pointwise mutual information.
"""


import matplotlib.pyplot as plt
from ngram import NgramModel
import nltk
import numpy as np


# Do this if nltk.tokenize.word_tokenize() fails:
# nltk.download('punkt')


KJBIBLE = "kjbible.txt"
JBOOK = "junglebook.txt"
SETIMES_TR = "SETIMES2.bg-tr.tr"
SETIMES_BG = "SETIMES2.bg-tr.bg"
FILES = (KJBIBLE, JBOOK, SETIMES_TR, SETIMES_BG)


def tokenize(fname):
    """Return a list of all the tokens in a text file."""
    with open(fname, 'r') as f:
        text = f.read().lower()
        tokens = nltk.tokenize.word_tokenize(text)
        return tokens


def calc_freq(tokens):
    """Return descending word frequencies."""
    dist = nltk.FreqDist(tokens)
    # dist.plot(100)  # nice and informative
    freqs = np.array(list(dist.values()))  # only one copy
    freqs[::-1].sort()  # in-place
    return freqs


def plot_freqs(files=FILES):
    """Plot word frequency statistics in requested text files."""
    freqs = [calc_freq(x) for x in files]

    def plot_one(f, n):
        corpora = len(files)
        width = 2  # linlin and loglog
        plt.subplot(corpora, width, n*2+1)
        plt.plot(f)
        plt.subplot(corpora, width, n*2+2)
        plt.loglog(f)

    for i, val in enumerate(freqs):
        plot_one(val, i)
    plt.show()


def gen_disassociated_press(order=8, len=100):
    """Generate some autocorrelated text."""
    tokens = [k for k in tokenize(KJBIBLE) if k.isalpha()]
    model = NgramModel(order, tokens, nltk.probability.MLEProbDist)
    ret = ["",] * (order-1)
    for i in range(len):
        c = ret[-(order-1):]
        print(c)
        ret.append(model.generate_one(c))
    return ' '.join(ret)


if __name__ == "__main__":
    print('my name: Miroslav Vitkov')
    plot_freqs()
    print(gen_disassociated_press())  # the bible is by far the most fun to use here
