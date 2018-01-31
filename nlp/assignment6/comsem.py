#!/usr/bin/env python3


# Code imposed by the assignment.
import nltk
grammar = nltk.data.load('grammars/sample_grammars/sem2.fcfg')
# print(grammar)
results = nltk.sem.util.interpret_sents(['Mary chases a dog'], grammar, semkey='SEM')
for result in results:
    for (synrep, semrep) in result:
        print(semrep)


from nltk.grammar import FeatureGrammar


def extend_grammar(g, p):
    '''Extend a FeatureGrammar object with a new (string represented) production.'''
    start = g._start
    old = g._productions
    new = FeatureGrammar.fromstring(p)._productions
    ret = FeatureGrammar(start, old + new)
    return ret




def main():
    print(extend_grammar(grammar, 'V -> N'))


if __name__ == '__main__':
    main()
