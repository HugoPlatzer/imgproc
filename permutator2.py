import os

FVParams = {"transformType" : ["dwt", "swt"], "colorSpace" : ["rgb"], "waveletFunction" : ["db1", "db2"],
"nLevels" : ["4"]}
ClassifierParams = {"testMethod" :  ["picture"], "k" : [3]}

FVFileName = "fv_auto.txt"
FVCmdline = lambda params : "python fv.py {} {} {} {} > {}".format(
        params["transformType"], params["colorSpace"], params["waveletFunction"],
        params["nLevels"], FVFileName)
ClassifierCmdline = lambda params : "python class.py {} {} < {}".format(
        params["testMethod"],
        params["k"]
        FVFileName)

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

def generateFV(params):
    os.popen(FVCmdline(params))

def classifyFV(params):
    return os.popen(ClassifierCmdline(params))

def printOutput(pFV, pClass):
    print("FVParams : {}".format(str(pFV)))
    print("ClassifierParams : {}".format(str(pClass)))
    print()
