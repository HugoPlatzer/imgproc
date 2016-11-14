class Classifier:
	def __init__(self, classes, fvs):
		self.classes = classes
		self.fvs = fvs
		
	def euclidDist(self, fvA, fvB):
		return sum((fvA[i] - fvB[i])**2 for i in xrange(len(fvA)))**0.5
	
	def classifyNN(self, fv):
		bestDist, bestClass = None, None
		for i, fvA in enumerate(self.fvs):
			dist = self.euclidDist(fv, fvA)
			if bestDist == None or dist < bestDist:
				bestDist = dist
				bestClass = classes[i]
		return bestClass

def readFVFile(f):
	fvs = []
	for l in f.readlines():
		fvs.append([float(k) for k in l.split(" ")])
	return fvs

def readFVFiles(names):
	classes, fvs = [], []
	for i, n in enumerate(names):
		with open(n) as f:
			newFVs = readFVFile(f)
			classes += [i] * len(newFVs)
			fvs += newFVs
	return (classes, fvs)

def loov(classes, fvs):
	results = []
	for i in xrange(len(classes)):
		oClasses = classes[:i] + classes[i+1:]
		oFVs = fvs[:i] + fvs[i+1:]
		classifier = Classifier(oClasses, oFVs)
		c = classifier.classifyNN(fvs[i])
		results.append((c, classes[i]))
	numCorrect = sum(1 for x in results if x[0] == x[1])
	print("{}/{}".format(numCorrect, len(results)))

classes, fvs = readFVFiles(["p1.txt", "p5.txt"])
loov(classes, fvs)
