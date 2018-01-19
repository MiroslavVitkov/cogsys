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









from collections import defaultdict
import copy
from functools import reduce
import itertools
import operator


class IBM1:
    def __init__(vikings, sentences_f, sentences_e):
        vikings.sentences_f = sentences_f
        vikings.sentences_e = sentences_e

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


    def run(vikings):
        while vikings.conditional_probs_old != vikings.conditional_probs:
            vikings.conditional_probs_old = copy.copy(vikings.conditional_probs)
            vikings.em_iter()
        return vikings.conditional_probs


    def em_iter(vikings):
        '''Do a single iteration of the EM algorithm.'''
        alignment_probs = {
            i: {
                tuple(alignment):
                reduce(operator.mul, [vikings.conditional_probs[pair]
                                      for pair in alignment])
                for alignment in sentence_alignments
            }

            for i, sentence_alignments in enumerate(vikings.alignments)
        }

        # Normalize alignment probabilities
        for sentence_idx, sentence_alignments in alignment_probs.items():
            total = float(sum(sentence_alignments.values()))
            probs = {alignment: value / total
                        for alignment, value in sentence_alignments.items()}
            alignment_probs[sentence_idx] = probs

        # Now join all alignments and begin the maximization step: group
        # by target-language word and collect corresponding
        # source-language probabilities
        word_translations = defaultdict(lambda: defaultdict(float))
        for sentence_alignments in alignment_probs.values():
            for word_pairs, prob in sentence_alignments.items():
                for word_f, word_e in word_pairs:
                    word_translations[word_e][word_f] += prob

        # Now calculate new conditional probability mapping, ungrouping
        # the `word_translations` tree and normalizing values into
        # conditional probabilities
        vikings.conditional_probs = {}
        for word_e, translations in word_translations.items():
            total = float(sum(translations.values()))
            for word_f, score in translations.items():
                vikings.conditional_probs[word_f, word_e] = score / total


def main():
    sen_f = ['mi casa verde'.split(), 'casa verde'.split(), 'la casa'.split()]
    sen_e = ['my green house'.split(), 'green house'.split(), 'the house'.split()]
    ibm = IBM1(sen_f, sen_e)
    print(ibm.run())


if __name__ == "__main__":
    main()
