import os, sys
import argparse

def FVCmdline(pFV):
    cmdline = "python fv.py {} {} {} {} > {}"
    cmdline = cmdline.format(
        pFV["transformType"], pFV["colorSpace"],
        pFV["waveletFunction"],
        pFV["nLevels"], args.FVFile)
    #print(cmdline)
    return cmdline

def classifierCmdline(pClass):
    cmdline = "python class.py {} {} < {}"
    cmdline = cmdline.format(pClass["testMethod"], 
                             pClass["k"], args.FVFile)
    #print(cmdline)
    return cmdline

def runForCombinations(params, func):
    def _run(remainingParams, currParams):
        if len(remainingParams) > 0:
            for p in remainingParams[0][1]:
                newParams = dict(currParams)
                newParams[remainingParams[0][0]] = p
                _run(remainingParams[1:], newParams)
        else:
            func(currParams)
    
    _run(params.items(), {})

def runClassifier(pClass):
    print("ClassifierParams: {}".format(str(pClass)))
    sys.stderr.write(classifierCmdline(pClass) + "\n")
    print(os.popen(classifierCmdline(pClass)).read())
    

def runForFVParam(pFV):
    print("FVParams: {}".format(str(pFV)))
    sys.stderr.write(FVCmdline(pFV) + "\n")
    os.popen(FVCmdline(pFV))
    runForCombinations(ClassifierParams, runClassifier)
    
    
parser = argparse.ArgumentParser()
parser.add_argument("paramFile")
parser.add_argument("FVFile")
args = parser.parse_args()
execfile(args.paramFile)
runForCombinations(FVParams, runForFVParam)
