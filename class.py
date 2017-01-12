from random import uniform
import sys
import argparse
from collections import namedtuple, defaultdict

PictureData = namedtuple("FVData", ["patternClass", "features"])
ClassificationResultData = namedtuple("ClassificationResultData",
                                     ["computedClass", "correctClass"])

class Classifier:

    def __init__(self, k, pictures):
        self.k = k
        self.pictures = pictures

    def euclidDist(self, FVa, FVb):
        return sum((FVa[i] - FVb[i]) ** 2 for i in xrange(len(FVa)))

    def classifyNN(self, FV):
        PictureDistanceData = namedtuple("PictureDistanceData", ["patternClass", "distance"])
        distances = [PictureDistanceData(picture.patternClass,
                                         self.euclidDist(FV, picture.features))
                    for picture in self.pictures]
        distances = sorted(distances, key = lambda d : d.distance)
        votes = [d.patternClass for d in distances[:self.k]]
        return max(votes, key = votes.count)

    def classifyFake(self, FV):
        return "B"

# returns mapping patientID -> [(patternClass, features)]
def loadFVFile():
    try:
        patientData = defaultdict(list)
        for l in sys.stdin:
            lSplit = l.split(" ")
            patternClass = lSplit[0]
            patientID = int(lSplit[1])
            features = [float(k) for k in lSplit[2:]]
            patientData[patientID].append(PictureData(patternClass, features))
        return patientData
    except(ValueError, AttributeError):
        print "This Feature Vector file is not supported"
        exit(1)


# leave one picture out
def loov(FVFile):
    results = []
    picturesFlat = [picture for patientPictures in FVFile.values() for picture in patientPictures]
    for i in xrange(len(picturesFlat)):
        currentPicture = picturesFlat[i]
        otherPictures = picturesFlat[:i] + picturesFlat[i + 1:]
        c = Classifier(args.k, otherPictures)
        results.append(ClassificationResultData(c.classifyNN(currentPicture.features),
                                                currentPicture.patternClass))
    return results


# leave one patient out
def lopv(FVFile):
    results = []
    for patientID, patientPictures in FVFile.iteritems():
        otherPictures = [otherPatientPictures
                            for otherPatientID, otherPatientPictures in FVFile.iteritems()
                                if otherPatientID != patientID]
        otherPicturesFlat = [picture for pictures in otherPictures for picture in pictures]
        c = Classifier(args.k, otherPicturesFlat)
        for picture in patientPictures:
            results.append(ClassificationResultData(c.classifyNN(picture.features),
                                                    picture.patternClass))
    return results

def printResults(results):
    numCorrect, numTotal = defaultdict(lambda : 0), defaultdict(lambda : 0)
    for r in results:
        if r.computedClass == r.correctClass:
            numCorrect[r.correctClass] += 1
        numTotal[r.correctClass] += 1
    for patternClass, nCorrect in sorted(numCorrect.iteritems()):
        correctness = numCorrect[patternClass] / float(numTotal[patternClass])
        print("{}: {}/{}={}".format(patternClass, nCorrect,
                                    numTotal[patternClass], correctness))
    totalNCorrect = sum(1 for r in results if r.computedClass == r.correctClass)
    totalCorrectness = totalNCorrect / float(len(results))
    print("Total: {}".format(totalCorrectness))

testMethods = {"picture" : loov, "patient" : lopv}
parser = argparse.ArgumentParser()
parser.add_argument("testMethod", choices = testMethods.keys())
parser.add_argument("k", type = int)
args = parser.parse_args()

patientData = loadFVFile()
printResults(testMethods[args.testMethod](patientData))
