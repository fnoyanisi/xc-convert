#!/bin/sh

# prefer anaconda
PYTHON='/usr/local/anaconda3/bin/python3'

if ! test -f "$PYTHON"; then
	PYTHON=`which python3`
elif ! test -f "$PYTHON"; then
	echo "No Python3 interpreter is detected!"
	exit 1
else
  echo "DO NOT CLOSE THIS WINDOW!"
  echo " "
  echo "starting xc-convert..."
	$PYTHON ./src/xc-convert.py
fi
