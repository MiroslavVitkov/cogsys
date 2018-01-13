#!/usr/bin/env python
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data",
                    default="data/hansards",
                    help="Data filename prefix (default=data/hansards).")
parser.add_argument("-e", "--english",
                    default="e",
                    help="Suffix of English filename (default=e).")
parser.add_argument("-f", "--french",
                    default="f",
                    help="Suffix of French filename (default=f).")
parser.add_argument("-o", "--out",
                    default="dice.a",
                    help="Output path (default=dice.a).")
parser.add_argument("-t", "--threshold",
                    default=0.5,
                    type=float,
                    help="Threshold for aligning with Dice's coefficient "
                          "(default=0.5).")
parser.add_argument("-n", "--num_sentences",
                    default=999999,
                    type=int,
                    help="Number of sentences to use for training and "
                          "alignment.")
args = parser.parse_args()
f_data = "%s.%s" % (args.data, args.french)
e_data = "%s.%s" % (args.data, args.english)


print("Training with Dice's coefficient...")
print("\tCounting...")
bitext = [[sentence.strip().split() for sentence in pair] for
          pair in zip(open(f_data), open(e_data))][:args.num_sentences]
f_count = defaultdict(int)
e_count = defaultdict(int)
fe_count = defaultdict(int)
for n, (f, e) in enumerate(bitext):
    for f_i in set(f):
        f_count[f_i] += 1
        for e_j in set(e):
            fe_count[(f_i, e_j)] += 1
    for e_j in set(e):
        e_count[e_j] += 1
    if n % 500 == 0:
        print("Went through {} sentence pairs...".format(n))


print("\tComputing coefficients...")
dice = defaultdict(int)
for (k, (f_i, e_j)) in enumerate(fe_count.keys()):
    dice[(f_i, e_j)] = 2 * fe_count[(f_i, e_j)] / (f_count[f_i] +
                                                   e_count[e_j])
    if k % 5000 == 0:
        print("Went through {} word pairs...".format(k))
print()

print("Computing alignments...")
with open(args.out, mode="w") as out_file:
    for n, (f, e) in enumerate(bitext):
        for (i, f_i) in enumerate(f):
            for (j, e_j) in enumerate(e):
                if dice[(f_i, e_j)] >= args.threshold:
                    out_file.write("%i-%i " % (i, j))
        if n % 500 == 0:
            print("Went through {} sentence pairs...".format(n))
        out_file.write("\n")
