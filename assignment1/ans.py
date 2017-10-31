#!/usr/bin/python3
"""Assignment 1 for Natural Language Processing.
Does word frequency plots, 
"""


import matplotlib.pyplot as plt
import nltk
import numpy as np


# Do this if nltk.tokenize.word_tokenize() fails:
# nltk.download('punkt')


KJBIBLE = "res/kjbible.txt"
JBOOK = "res/junglebook.txt"
SETIMES_TR = "res/SETIMES2.bg-tr.tr"
SETIMES_BG = "res/SETIMES2.bg-tr.bg"
FILES = (KJBIBLE, JBOOK, SETIMES_TR, SETIMES_BG)


def calc_freq(fname):
    """fname - path to a plaintext UTF8 file
    returns - np.array of sorted word frequencies
    """
    with open(fname, 'r') as f:
        text = f.read().lower()
        tokens = nltk.tokenize.word_tokenize(text)
        dist = nltk.FreqDist(tokens)
        # dist.plot(100)  # nice and informative
        return dist_to_sorted_list(dist)


def dist_to_sorted_list(dist):
    """d - a FreqDist object
    returns - descending sorted np.array
    """
    freqs = np.array(list(dist.values()))  # only one copy
    freqs[::-1].sort()  # in-place
    return freqs


def plot_freq(freqs, n=0):
    """freqs - list of integer magnitudes
    n - plot counter, 0-based
    returns - None
    side effects - plots linear and log graphs
    """
    corpora = len(FILES)
    width = 2  # linlin and loglog
    plt.subplot(corpora, width, n*2+1)
    plt.plot(freqs)
    plt.subplot(corpora, width, n*2+2)
    plt.loglog(freqs)


def plot_all_freqs():
    """
    """
    freqs = [calc_freq(x) for x in FILES]
    for i, val in enumerate(freqs):
        plot_freq(val, i)
    plt.show()


if __name__ == "__main__":
    print('my name: Miroslav Vitkov')
    plot_all_freqs()
    print('first assignment presented')
