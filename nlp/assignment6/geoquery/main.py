#!/usr/bin/env python3


import nltk


def main():
    import semcon3
    semcon3.SWIPL='swipl'
    g = nltk.data.load('geoquery1.fcfg', cache=False)
    parses = nltk.sem.util.interpret_sents(['what is the density of texas ?'], g, semkey='sem')
#    parses = nltk.sem.util.interpret_sents(['how long is the longest river in california'], g, semkey='sem')
    for parse in parses:
        for (syn,sem) in parse:
            print(sem)
            semcon3.query(sem)


if __name__ == '__main__':
    main()
