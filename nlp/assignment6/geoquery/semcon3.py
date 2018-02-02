# Answers Geoquery queries.
# Tatjana Scheffler, Jan. 11, 2018
# based on a script by Alexander Koller, 10 May 2015
#
# Important functions:
#
# query(mr)
# Runs the given query using the Geoquery Prolog system and outputs
# the answers. In order to use this, you need to download two support
# files from the Geoquery website:
#
# - ftp://ftp.cs.utexas.edu/pub/mooney/nl-ilp-data/geosystem/geobase
#   (save as geobase.pl)
#
# - ftp://ftp.cs.utexas.edu/pub/mooney/nl-ilp-data/geosystem/geoquery
#   (save as geoquery.pl)
#
# You also need to install SWI Prolog for your platform
# (get it from http://www.swi-prolog.org/) and set the SWIPL variable
# below to the path of the swipl executable.

import nltk
import importlib
import tempfile
import subprocess
import os
import re

import tempfile
import subprocess
import os
import re


# paths for executing Geoquery queries
SWIPL = "/Applications/SWI-Prolog.app/Contents/MacOS/swipl"

query_template = ''':- initialization main.
main :-
  [geoquery],
  {0},
  halt(0).'''

underscore_re = re.compile(r"([a-zA-Z0-9_]*\+[a-zA-Z0-9_+]*)")


# rewrite meaning repr to Prolog query term
def to_geoquery(querystr):
    q = querystr.replace("&", ",") # replace conjunction by comma
    q = underscore_re.sub(r"'\1'", q).replace("+", " ") # replace new+mexico by 'new mexico'
    return(q)

def query(semantics):
    q = to_geoquery(str(semantics))
    file_content = query_template.format(q)

    # write Prolog query to file
    tmpfile = tempfile.mkstemp(suffix=".pl")[1]
    f = open(tmpfile, "w")
    print(file_content, file=f)
    f.close()

    # run Prolog to resolve query and collect output
    FNULL = open(os.devnull, 'w')    
    proc = subprocess.Popen([SWIPL, "-q", "-f", tmpfile], stdout=subprocess.PIPE, stderr=FNULL)
    output = proc.stdout.read()
        
    output= output.decode('utf-8')
    ans_found=False
    for line in output.split('\n'):
        if line.startswith("Answer"):
            ans_found=True
            print(line)
    if not ans_found:
        print("No answers found.")
        
