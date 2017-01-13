import os, sys

FVParams = {"transformType" : ["dwt"],
            "colorSpace" : ["rgb", "hsv", "lab"],
            "waveletFunction" : ["db1", "db2"],
            "nLevels" : ["4"]}
            
ClassifierParams = {"testMethod" :  ["picture"],
                    "k" : [3]}

FVFileName = "fv_auto.txt"



def FVCmdline(pFV):
    cmdline = "python fv.py {} {} {} {} > {}"
    cmdline = cmdline.format(
        pFV["transformType"], pFV["colorSpace"],
        pFV["waveletFunction"],
        pFV["nLevels"], FVFileName)
    #print(cmdline)
    return cmdline

def classifierCmdline(pClass):
    cmdline = "python class.py {} {} < {}"
    cmdline = cmdline.format(pClass["testMethod"], 
                             pClass["k"], FVFileName)
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
    print(os.popen(classifierCmdline(pClass)).read())
    

def runForFVParam(pFV):
    print("FVParams: {}".format(str(pFV)))
    os.popen(FVCmdline(pFV))
    runForCombinations(ClassifierParams, runClassifier)

runForCombinations(FVParams, runForFVParam)
