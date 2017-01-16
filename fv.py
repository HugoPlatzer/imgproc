import cv2
import pywt
import numpy as np
import os
import argparse

def loadPatientMapping(filename):
    d = {}
    with open(filename) as f:
        for l in f.readlines():
            lSplit = l.split(";")
            d[lSplit[0]] = int(lSplit[1])
    return d


def convertColorspace(img, cs):
    if cs == "rgb":
        return img
    cs = eval("cv2.COLOR_BGR2{}".format(cs.upper()))
    return cv2.cvtColor(img, cs)


def procChanDWT(img, wavelet, nLevels):
    wl = pywt.Wavelet(wavelet)
    nLevels = max(nLevels, pywt.dwt_max_level(256, wl))
    wt = pywt.wavedec2(img, wavelet=wl, level=nLevels)
    fv = []
    for l in xrange(1, nLevels):
        for x in wt[l]:
            fv.append(np.std(x))
            fv.append(np.mean(np.abs(x - np.mean(x))))
    return fv
    
def procChanSWT(img, wavelet, nLevels):
    wt = pywt.swt2(img, wavelet=wavelet, level=nLevels)
    fv = []
    for l in xrange(1, nLevels):
        for x in wt[l][1]:
            fv.append(np.std(x))
            fv.append(np.mean(np.abs(x - np.mean(x))))
    return fv

def procImg(filename, colorSpace, wavelet, nLevels):
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    img = convertColorspace(img, colorSpace)
    fv = []
    for i in xrange(3):
        ic = img[:, :, i]
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        ic = clahe.apply(ic)
        ic = cv2.normalize(ic, dst=ic, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        fv += transformTypeMapping[args.transformType](ic, wavelet, nLevels)
    return fv


def processPictures(patientMapping, imageDir, patternClass):
    for imageFileName in os.listdir(imageDir):
        fv = procImg(os.path.join(imageDir, imageFileName), args.colorSpace, args.waveletFunction, int(args.nLevels))
        print("{} {} {}".format(patternClass, patientMapping[imageFileName], " ".join(str(k) for k in fv)))


dataDir = "img"
patientMapping = loadPatientMapping(os.path.join(dataDir, "patientmapping.csv"))
patternClassMapping = {"Pit Pattern I": "A", "Pit Pattern II": "A",
          "Pit Pattern III L": "B", "Pit Pattern III S": "B",
          "Pit Pattern IV": "B", "Pit Pattern V": "C"}
transformTypeMapping = {"swt" : procChanSWT, "dwt" : procChanDWT}

parser = argparse.ArgumentParser()
parser.add_argument("transformType", choices = transformTypeMapping.keys())
parser.add_argument("colorSpace")
parser.add_argument("waveletFunction")
parser.add_argument("nLevels", type = int)
args = parser.parse_args()

for patternDir, patternClass in patternClassMapping.iteritems():
    processPictures(patientMapping, os.path.join(dataDir, patternDir), patternClass)
