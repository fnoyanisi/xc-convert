#!/bin/sh

# prefer anaconda
PYTHON='/usr/local/anaconda3/bin/pythonw'

if ! test -f "$PYTHON"; then
	PYTHON=`which python3`
elif ! test -f "$PYTHON"; then
	echo "No Python3 interpreter is found!"
	exit 1
else
  echo "DO NOT CLOSE THIS WINDOW!"
  echo " "
  echo "starting xc-convert..."
  export PYTHONPATH=`pwd`
  cd ./src
	$PYTHON xc-convert.py
fi
