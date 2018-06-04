#!/bin/bash


# Get first $1 lines from the household power dataset.
# The whole file is 127Mb.


set -e


URL='https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip'
TEMPDIR='/tmp/household_power_consumption_tempdir'
OUTFILE='extern/power_truncated'

BASENAME="${URL##*/}"
BASENAME="${BASENAME%.*}"

mkdir -p "$TEMPDIR"
cd "$TEMPDIR"

if [ ! -f "$BASENAME.zip" ]; then
    wget "$URL"
fi

if [ ! -f "$BASENAME.txt" ]; then
    unzip "$BASENAME.zip"
fi

if [[ "$#" -eq 0 ]]; then
    mv "$TEMPDIR/$BASENAME.txt" "$OLDPWD/$OUTFILE"
else
    head -n"$1" "$TEMPDIR/$BASENAME.txt" > "$OLDPWD/$OUTFILE"
fi
