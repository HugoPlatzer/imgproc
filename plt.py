from sys import argv
import numpy as np
import matplotlib.pyplot as plt

f1 = int(argv[2])
f2 = int(argv[3])

d1, d2 = [], []

with open(argv[1]) as f:
	for l in f.readlines():
		fv = [float(x) for x in l.split(" ")]
		d1.append(fv[f1])
		d2.append(fv[f2])

#print(d1)		
plt.scatter(d1, d2)
plt.show()
