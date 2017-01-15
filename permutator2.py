import os, sys
import argparse

FVParams = {"transformType" : ["dwt"],
            "colorSpace" : ['Lab'],
            "waveletFunction" : ['haar', 'db1', 'db10',  'db20', 'sym2', 'sym5', 'sym10', 'sym20', 'coif1', 'bior1.1', 'rbio1.1', 'dmey'],
            "nLevels" : ["-1"]}
            
ClassifierParams = {"testMethod" :  ["patient"],
                    "k" : [1]}

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
