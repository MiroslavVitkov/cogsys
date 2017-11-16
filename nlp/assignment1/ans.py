#!/usr/bin/python3
"""
Assignment 1 for Natural Language Processing.
Does word frequency plots, Dissociated Press generation
and Pointwise mutual information.
"""


from collections import Counter
import matplotlib.pyplot as plt
from ngram import NgramModel
from nltk import word_tokenize  # on error, do 'nltk.download('punkt')'
from nltk import MLEProbDist


KJBIBLE = "kjbible.txt"
JBOOK = "junglebook.txt"
SETIMES_TR = "SETIMES2.bg-tr.tr"
SETIMES_BG = "SETIMES2.bg-tr.bg"
FILES = (KJBIBLE, JBOOK, SETIMES_TR, SETIMES_BG)


def tokenize(fname):
    """Return a list of all the tokens in a text file."""
    with open(fname, 'r') as f:
        text = f.read().lower()
        tokens = word_tokenize(text)
        return tokens


def plot_freqs(files=FILES):
    """Plot word frequency statistics in requested text files."""
    def calc_freqs(f):
        t = tokenize(f)
        dist = Counter(t)
        return sorted(dist.values(), reverse=True)
    freqs = [calc_freqs(f) for f in files]

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


def gen_disassociated_press(file=KJBIBLE, order=3, len=100):
    """Generate some autocorrelated text."""
    tokens = [k for k in tokenize(file) if k.isalpha()]
    model = NgramModel(order, tokens, MLEProbDist)
    ret = ['',] * (order-1)
    for i in range(len):
        tail = ret[-(order-1):]
        ret.append(model.generate_one(tail))
    return ' '.join(ret[(order-1):])


def calc_pmi(file=KJBIBLE, min_w_freq=10):
    """
    Calculate Pointwise Mutal Information.

    Find common digraphs in a text file; compute their pmi.
    pmi = f(w1,w2)N / f(w1)f(w2)
    Return a map of tuples to numbers.
    """
    tokens = tokenize(file)
    w_freqs = Counter(tokens)
    goodwords = [k for k,v in w_freqs.items() if v >= min_w_freq]

    # Throw away all pairs of words, where one is rare.
    bigrams = [x for x in zip(tokens, tokens[1:])
               if x[0] in goodwords and x[1] in goodwords]
    N = len(tokens)
    b_freqs = Counter(bigrams)
    pmi = {k:(v*N)/(w_freqs[k[0]]*w_freqs[k[1]]) for k,v in b_freqs.items()}
    return pmi


def get_20_20_pmi(pmi):
    l = [(k,v) for k,v in pmi.items()]
    l.sort(key=lambda x: x[1], reverse=True)
    return l[:19] + l[-19:]


if __name__ == "__main__":
    print('name: 794678 Miroslav Vitkov')

    print('task1:')
    plot_freqs()
    print('comment:')
    print('Zipf`s law holds. Low word frequencies are visible as jumps in the log graph.')
    print()

    print('task2:')
    for n in range(2, 5):
        print('n=' + str(n))
        print(gen_disassociated_press(order=n))
    print('comment:')
    print('Larger context introduces a plot to the story.')
    print()

    print('task 3:')
    print(get_20_20_pmi(calc_pmi()))
    print('comment:')
    print('pmi seems to measure a word`s specificity: '
          'high pmi suggests the word is only found in this concrete context.')
