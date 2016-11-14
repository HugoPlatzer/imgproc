#!/bin/sh
for f in "$1"/*; do
	python fv.py "$f" $2 $3 $4
done
