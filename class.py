from random import uniform

class Classifier:
	def __init__(self, fvData):
		self.fvData = fvData
		
	def euclidDist(self, fvA, fvB):
		return sum((fvA[i] - fvB[i])**2 for i in xrange(len(fvA)))**0.5
	
	def classifyNN(self, fv):
		bestDist, bestClass = None, None
		for i, fd in enumerate(self.fvData):
			dist = self.euclidDist(fv, fd[1])
			if bestDist == None or dist < bestDist:
				bestDist = dist
				bestClass = fd[0]
		return bestClass
	
	def classifyFake(self, fv):
	    return "B"

def readFVFile(f):
	patData = {}
	for l in f.readlines():
		lSplit = l.split(" ")
		patClass = lSplit[0]
		patID = int(lSplit[1])
		patFV = [float(k) for k in lSplit[2:]]
		if patID not in patData:
		    patData[patID] = []
		patData[patID].append((patClass, patFV))
	return patData

#leave one picture out
def loov(patData):
    results = []
    fvFlat = [pp for pd in patData.values() for pp in pd]
    for i in xrange(len(fvFlat)):
        fvOther = fvFlat[:i] + fvFlat[i+1:]
        c = Classifier(fvOther)
        results.append((c.classifyNN(fvFlat[i][1]), fvFlat[i][0]))
    return results

#leave one patient out
def lopv(patData):
    results = []
    for patID, patRec in patData.iteritems():
        otherRec = [pp for pi, pr in patData.iteritems() for pp in pr if pi != patID]
        c = Classifier(otherRec)
        for pr in patRec:
            results.append((c.classifyNN(pr[1]), pr[0]))
    return results

def printResults(results):
    numCorrect, numTotal = {}, {}
    for r in results:
        if r[0] not in numCorrect:
            numCorrect[r[0]] = 0
            numTotal[r[0]] = 0
        if r[0] == r[1]:
            numCorrect[r[0]] += 1
        numTotal[r[0]] += 1
    for c, r in numCorrect.iteritems():
        print("{}: {}/{}={}".format(c, r, numTotal[c], r / float(numTotal[c])))

def printClasses(pd):
    for pr in pd.values():
        print(" ".join(pp[0] for pp in pr))

pd = None
with open("fv.txt") as f:
    pd = readFVFile(f)
    printClasses(pd)
    printResults(lopv(pd))
