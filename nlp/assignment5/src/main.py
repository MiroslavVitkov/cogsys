#!/usr/bin/env python3


# coding: utf-8
from collections import defaultdict,namedtuple
from itertools   import product,repeat
from msgpack     import pack,unpack
from sys         import stdout

import numpy as np
import math






from collections import defatultdict
from itertools import product

class IBM1:
    '''IBM1 word alignment model.'''
    def __init__(self, corpus):
        '''corpus - list(english_sentence, foreign_sentence)'''

        self.probs = dict()

        # Compute all possible alignments.
        aligns = defaultdict(set)
        for e_sen, f_sen in corpus:
            е_sen = (None,) + е_sen
            for f_word, e_word in product(f_sen, e_sen):
                aligns[e_word].add(f_word)

        # Compute uniform initial probabilities for each alignment.
        uniform_dist = lambda n: [1 / float(n)] * n
        for e_word, f_word_set in alignes.iteritems():
            prob = uniform_dist(len(f_word_set))
            for f_word in f_word_set:
                self.probs[(e_word, f_word)] = prob


    def em_iter(self, corpus, passnum=1):
        """Run a single iteration of the EM algorithm on the model"""
        likelihood = 0.0
        c1 = defaultdict(float) # ei aligned with fj
        c2 = defaultdict(float) # ei aligned with anything

        # The E-Step
        for(f, e) in corpus:
            e = IBM.nones(self.param.q0) + e
            l = len(e)
            m = len(f) + 1
            q = 1 / float(l)

            for i in range(1, m):

                num = [ q * self.t[(f[i - 1], e[j])] for j in range(0,l) ]
                den = float(sum(num))
                likelihood += math.log(den)

                for j in range(0, l):

                    delta = num[j] / den

                    c1[(f[i - 1], e[j])] += delta
                    c2[(e[j],)]          += delta

        # The M-Step
        self.t = defaultdict(float, {
            k: (v + self.param.n) / (c2[k[1:]] + (self.param.n * self.param.v))
            for k, v in c1.iteritems() if v > 0.0 })

        return likelihood


    def em_train(self, corpus, n=10, s=1):
        """Run several iterations of the EM algorithm on the model"""

        for k in range(s, n + s):
            self.em_iter(corpus, passnum=k)


    def viterbi_alignment(self, f, e):
        """Returns an alignment from the provided french sentence to the english sentence"""

        e = IBM.nones(self.param.q0) + e
        l = len(e)
        m = len(f) + 1

        # for each french word:
        #  - compute a list of indices j of words in the english sentence,
        #    together with the probability of e[j] being aligned with f[i-1]
        #  - take the index j for the word with the _highest_ probability;

        def maximum_alignment(i):
            possible_alignments = [(j, self.t[(f[i - 1], e[j])]) for j in range(0, l)]
            return max(possible_alignments, key=lambda x: x[1])[0]

        return [
            maximum_alignment(i) - self.param.q0 + 1
            for i in range(1, m)]


from os import path

import itertools
import os


def read_corpus(path):
    """Read a file as a list of lists of words."""

    with open(path,'r') as f:
        return [ ln.strip().split() for ln in f ]


def run(corpus, ibm_cls, ibm_init, packs_path, corpus_name, n):




    """Run n iterations of the EM algorithm on a certain corpus and save all intermediate and final results"""

    model = None

    if not path.isdir(packs_path):
        os.makedirs(packs_path)

    # Iterations
    for s in range(0, n + 1):
        curr_pack_path = path.join(packs_path , corpus_name + '.' + str(s  ) + '.pack')
        next_pack_path = path.join(packs_path , corpus_name + '.' + str(s+1) + '.pack')

        # Execute iteration if not already dumped to pack file
        if not path.isfile(next_pack_path) or not path.isfile(curr_pack_path):

            if path.isfile(curr_pack_path):
                with open(curr_pack_path, 'r') as stream:
                    model = ibm_cls.load(stream)
                    print ("Loaded %s" % curr_pack_path)

            else:
                if model is None:
                    model = ibm_init()
                else:
                    (likelihood, time) = model.em_iter(corpus, s)

                    # Save likelihood and time results so separate file
                    with open(path.join(packs_path, corpus_name + '.results'), "a") as results_handle:
                        results_handle.write("%d,%.4f,%.5f\n" % (s, time, likelihood))

                with open(curr_pack_path, 'w') as stream:
                    model.dump(stream)
                    print( "Dumped %s" % curr_pack_path)

            # Generate evaluation file for testing the model
            test_model(model, packs_path, corpus_name, s)

    return model


def test_model(model, eval_data_path, corpus_name, s):
    """
    Test a model against the provided test set by generating an evaluation file
    This file can be used by the provided 'wa_eval_align.pl'
    """

    test_path = path.join(path.dirname(__file__), '..', 'data', 'test')
    test_corpus_name = 'test'
    test_corpus_path = path.join(test_path, 'test', test_corpus_name)
    fr_test_corpus_path = test_corpus_path + '.f'
    en_test_corpus_path = test_corpus_path + '.e'
    test_corpus = zip(read_corpus(fr_test_corpus_path), read_corpus(en_test_corpus_path))

    if not path.isdir(eval_data_path):
        os.makedirs(eval_data_path)

    handle = open(path.join(eval_data_path, corpus_name + '.' + str(s) + '.eval'), 'w')

    for i, (f, e) in enumerate(test_corpus):

        for j, a in enumerate(model.viterbi_alignment(f, e)):
            if a > 0:
                line = "%04d %d %d" % (i+1, a, j+1)
                handle.write(line + "\n")

    handle.close()


def print_test_example(ibm):
    """Prints the alignment results of a toy example"""

    f = 'le gouvernement fait ce que veulent les Canadiens .'.split()
    e = 'the government is doing what the Canadians want .'.split()

    a = ibm.viterbi_alignment(f, e)

    print( ' '.join(e))
    print( ' '.join(f))
    e = ['NULL'] + e
    print (' '.join([e[j] for j in a]))


def main2():
    """Program entry point"""

    data_path = path.join(path.dirname(__file__), '..', 'data')
    corpus_name = 'hansards.36.2'  # hansards.36.2
    corpus_path = path.join(data_path, 'training', corpus_name)
    fr_corpus_path = corpus_path + '.f'
    en_corpus_path = corpus_path + '.e'
    en_corpus = read_corpus(en_corpus_path)
    en_vocabulary_len = len(set(itertools.chain(*en_corpus)))
    corpus = zip(read_corpus(fr_corpus_path), en_corpus)

    # Train IBM1 with random and uniform initialization
    ibm = IBM
    run(corpus, ibm, lambda: ibm.uniform(corpus), path.join(data_path, 'model', 'ibm1', 'uniform'), corpus_name, 20)


def main():
    print("kur")


if __name__ == "__main__":
    main()
