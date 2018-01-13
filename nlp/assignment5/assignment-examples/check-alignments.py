#!/usr/bin/env python
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("check_file",
                    help="Path to file with the alignments to check.")
parser.add_argument("-d", "--data",
                    default="data/hansards",
                    help="Data filename prefix (default=data/hansards).")
parser.add_argument("-e", "--english",
                    default="e",
                    help="Suffix of English filename (default=e).")
parser.add_argument("-f", "--french",
                    default="f",
                    help="Suffix of French filename (default=f).")
args = parser.parse_args()
f_data = open("%s.%s" % (args.data, args.french))
e_data = open("%s.%s" % (args.data, args.english))
check = open(args.check_file)


for (n, (f, e, a)) in enumerate(zip(f_data, e_data, check)):
    size_f = len(f.strip().split())
    size_e = len(e.strip().split())
    try:
        alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])
        for (i, j) in alignment:
            if i >= size_f or j > size_e:
                sys.stderr.write(
                    "WARNING (%s): Sentence %d, point (%d,%d) is not a valid "
                    "link\n" % (sys.argv[0], n, i, j))
            pass
    except Exception:
        sys.stderr.write("ERROR (%s) line %d is not formatted correctly:\n"
                         "  %s" % (sys.argv[0], n, a))
        sys.stderr.write(
            "Lines can contain only tokens \"i-j\", where i and j are integer "
            "indexes into the French and English sentences, respectively.\n")
        sys.exit(1)
print("Looks good I guess.")


# I commented this stuff out because it's broken as ****. Just make sure you are
# putting line breaks at the correct places in your alignments and you'll be fine...
"""
warned = False
for a in check:
    if not warned:
        sys.stderr.write("WARNING (%s): alignment file is longer than "
                         "bitext\n" % sys.argv[0])
        warned = True

try:
    if False:
        sys.stderr.write("WARNING (%s): bitext is longer than "
                         "alignment. This is likely PERFECTLY FINE if you didn't process the whole file\n" % sys.argv[0])
except StopIteration:
    pass
"""