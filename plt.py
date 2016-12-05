from sys import argv, stdin
import numpy as np
import matplotlib.pyplot as plt

pClass = argv[1]
f1 = int(argv[2])
f2 = int(argv[3])

d1, d2 = [], []

for l in stdin.readlines():
	lSplit = l.split(" ")
	if lSplit[0] != pClass:
		continue
	fv = [float(x) for x in lSplit[2:]]
	d1.append(fv[f1])
	d2.append(fv[f2])
	
plt.scatter(d1, d2)
plt.show()
