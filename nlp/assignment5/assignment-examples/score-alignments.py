#!/usr/bin/env python
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("file_to_score",
                    help="Path to file with the alignments to score.")
parser.add_argument("-d", "--data",
                    default="data/hansards",
                    help="Data filename prefix (default=data/hansards).")
parser.add_argument("-e", "--english",
                    default="e",
                    help="Suffix of English filename (default=e).")
parser.add_argument("-f", "--french",
                    default="f",
                    help="Suffix of French filename (default=f).")
parser.add_argument("-a", "--alignments",
                    default="a",
                    help="Suffix of gold alignments filename (default=a).")
parser.add_argument("-n", "--num_display",
                    default=999999,
                    type=int,
                    help="Number of alignments to display.")
args = parser.parse_args()
f_data = "%s.%s" % (args.data, args.french)
e_data = "%s.%s" % (args.data, args.english)
a_data = "%s.%s" % (args.data, args.alignments)


(size_a, size_s, size_a_and_s, size_a_and_p) = (0.0, 0.0, 0.0, 0.0)
with open(args.file_to_score + ".score", mode="w") as score_file:
    for (i, (f, e, g, a)) in enumerate(zip(open(f_data), open(e_data), open(a_data), open(args.file_to_score))):
        fwords = f.strip().split()
        ewords = e.strip().split()
        sure = set([tuple(map(int, x.split("-"))) for x in filter(lambda x: x.find("-") > -1, g.strip().split())])
        possible = set([tuple(map(int, x.split("?"))) for x in filter(lambda x: x.find("?") > -1, g.strip().split())])
        alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])
        size_a += len(alignment)
        size_s += len(sure)
        size_a_and_s += len(alignment & sure)
        size_a_and_p += len(alignment & possible) + len(alignment & sure)
        if i < args.num_display:
            score_file.write("  Alignment %i  KEY: ( ) = guessed, * = sure, ? = possible\n" % i)
            score_file.write("  ")
            for j in ewords:
                score_file.write("---")
            score_file.write("\n")
            for (i, f_i) in enumerate(fwords):
                score_file.write(" |")
                for (j, _) in enumerate(ewords):
                    (left, right) = ("(", ")") if (i, j) in alignment else (" ", " ")
                    point = "*" if (i, j) in sure else "?" if (i, j) in possible else " "
                    score_file.write("%s%s%s" % (left, point, right))
                score_file.write(" | %s\n" % f_i)
            score_file.write("  ")
            for j in ewords:
                score_file.write("---")
            score_file.write("\n")
            for k in range(max(map(len, ewords))):
                score_file.write("  ")
                for word in ewords:
                    letter = word[k] if len(word) > k else " "
                    score_file.write(" %s " % letter)
                score_file.write("\n")
            score_file.write("\n")

    precision = size_a_and_p / size_a
    recall = size_a_and_s / size_s
    aer = 1 - ((size_a_and_s + size_a_and_p) / (size_a + size_s))
    score_file.write("Precision = %f\nRecall = %f\nAER = %f\n" % (precision, recall, aer))
