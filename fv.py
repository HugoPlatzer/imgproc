import cv2
import pywt
import numpy as np
import os
from sys import argv

def convertColorspace(img, cs):
	if cs == "rgb":
		return img
	cs = eval("cv2.COLOR_BGR2{}".format(cs.upper()))
	return cv2.cvtColor(img, cs)

def procChan(img, wavelet, nLevels):
	wt = pywt.wavedec2(img, wavelet = wavelet, level = nLevels)
	fv = []
	for l in xrange(1, nLevels + 1):
		for x in wt[l]:
			fv.append(np.std(x))
			fv.append(np.mean(np.abs(x - np.mean(x))))
	return fv

def procImg(filename, colorSpace, wavelet, nLevels):
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	img = convertColorspace(img, colorSpace)
	fv = []
	for i in xrange(3):
		ic = img[:,:,i]
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
		ic = clahe.apply(ic)
		ic = cv2.normalize(ic, dst = ic, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
		fv += procChan(ic, wavelet, nLevels)
	return fv

def processFiles(dirname):
	for fn in os.listdir(dirname):
		fv = procImg(os.path.join(dirname, fn), argv[2], argv[3], int(argv[4]))
		print(" ".join(str(k) for k in fv))

processFiles(argv[1])
