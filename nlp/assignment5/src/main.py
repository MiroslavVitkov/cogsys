#!/usr/bin/env python3
class A:
    def viterbi_alignment(self, f, e):
        """Returns an alignment from the provided french sentence to the english sentence"""

        e = (None,) + e
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


from collections import defaultdict
import copy
from functools import reduce
import itertools
import operator


class IBM1:
    def __init__(vikings, sentences_f, sentences_e):
        vocabulary_f = set(itertools.chain.from_iterable(sentences_f))
        vocabulary_e = set(itertools.chain.from_iterable(sentences_e))

        # Uniform initial probabilities.
        uniform_prob = 1.0 / len(vocabulary_f)
        vikings.conditional_probs_old = None
        vikings.conditional_probs = {(word_f, word_e): uniform_prob
                                     for word_f in vocabulary_f
                                     for word_e in vocabulary_e}

        vikings.alignments = [[list(zip(f, perm_e))
                               for perm_e in itertools.permutations(e)]
                              for f, e in zip(sentences_f, sentences_e)]


    def train(vikings):
        '''Returns a mapping `(word_f, word_e) => p` where p is $P(t1|t2)$.
        '''
        while vikings.conditional_probs_old != vikings.conditional_probs:
            vikings.conditional_probs_old = copy.copy(vikings.conditional_probs)
            vikings._em_iter()
        return vikings.conditional_probs


    def _em_iter(vikings):
        '''Perform a single iteration of the EM algorithm.'''
        alignment_probs = {
            i: {
                tuple(alignment):
                reduce(operator.mul, [vikings.conditional_probs[pair]
                                      for pair in alignment])
                for alignment in sentence_alignments
            }

            for i, sentence_alignments in enumerate(vikings.alignments)
        }

        # Normalize alignment probabilities.
        for sentence_idx, sentence_alignments in alignment_probs.items():
            total = float(sum(sentence_alignments.values()))
            probs = {alignment: value / total
                        for alignment, value in sentence_alignments.items()}
            alignment_probs[sentence_idx] = probs

        # Now join all alignments and begin the maximization step: group
        # by target-language word and collect corresponding
        # source-language probabilities.
        word_translations = defaultdict(lambda: defaultdict(float))
        for sentence_alignments in alignment_probs.values():
            for word_pairs, prob in sentence_alignments.items():
                for word_f, word_e in word_pairs:
                    word_translations[word_e][word_f] += prob

        # Now calculate new conditional probability mapping, ungrouping
        # the `word_translations` tree and normalizing values into
        # conditional probabilities.
        vikings.conditional_probs = {}
        for word_e, translations in word_translations.items():
            total = float(sum(translations.values()))
            for word_f, score in translations.items():
                vikings.conditional_probs[word_f, word_e] = score / total


def read_corpus(path):
    '''Read a file as a list of lists of words.'''
    with open(path,'r') as f:
        a = [ ln.strip().split() for ln in f ]
        return a[1:2]


def main():
    corpus_path = '../data/hansards'
    corpus_f = read_corpus(corpus_path + '.f')
    corpus_e = read_corpus(corpus_path + '.e')
    ibm = IBM1(corpus_f, corpus_e)
    res = ibm.train()
    print(res)


if __name__ == "__main__":
    main()
