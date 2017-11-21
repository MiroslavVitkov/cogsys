#!/usr/bin/env python3


'''Supervised training of a hidden markov model.'''


from collections import defaultdict
from itertools import chain


# Imposed by assignment. Copyrighted, therefore not redistributed.
CORPUS_train = "wsj_tagged/wsj_tagged_train.tt"
CORPUS_eval = "wsj_tagged/wsj_tagged_eval.tt"
CORPUS_test = "wsj_tagged/wsj_tagged_test.t"


def read_sentences(fname):
    """Read the sentences from an annotated corpus."""
    with open(fname, 'r') as f:
        sentences = [[]]
        for l in f.readlines():
            s = l.split()
            if s:
                # Next word, append to sentence.
                sentences[-1].append((s[0].lower(), s[1]))
            else:
                # Sentence has ended.
                sentences.append([])

        # Get rid of '[]' in the end.
        sentences.pop()
        return sentences


# Unused.
def calc_vocabulary_size(sentences):
    '''Return vocabulary size in (word space, POS tag space).'''
    words = set()
    tags = set()
    for s in sentences:
        [(tags.add(tag), words.add(word)) for (word, tag) in s]
    return len(words), len(tags)


def calc_initial(sentences):
    '''Return a map of tags and corresponding initial probabilities.'''
    d = defaultdict(lambda: 0)
    for s in sentences:
        # Count only the first tag in each sentence.
        tag = s[0][1]
        d[tag] += 1

    # Normalize.
    total = sum(d.values())
    return {k: v/total for k, v in d.items()}


def calc_transitions(sentences):
    '''Calculate transition probabilities from tag to tag.'''
    bigrams = []
    for s in sentences:
        [bigrams.append((tag1, tag2)) for (_, tag1), (_, tag2) in zip(s, s[1:])]

    d = defaultdict(lambda: defaultdict(lambda: 0))
    for (b1, b2) in bigrams:
        d[b1][b2] += 1

    # Normalize.
    ret = {}
    for tag, dist in d.items():
        total = sum(dist.values())
        ret[tag] = {k: v/total for k, v in dist.items()}

    return ret


def calc_emissions(sentences):
    '''Returns a family of distributions: given tag, what words could be generated.'''
    d = defaultdict(lambda: defaultdict(lambda: 0))
    for word, tag in chain.from_iterable(sentences):
        d[tag][word] += 1  # Note reversed ordering compared to the corpus!

    # Normalize.
    ret = {}
    for tag, dist in d.items():
        total = sum(dist.values())
        ret[tag] = {k: v/total for k, v in dist.items()}

    return ret

if __name__ == "__main__":
    sen = read_sentences(CORPUS_train)
    # print(calc_initial(sen))
    # print(calc_transitions(sen))
    # print(calc_vocabulary_size(sen))
    # print(calc_emissions(sen))
