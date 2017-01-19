import sys, ast, re, argparse

class Result:
    def __init__(self, lines):
        linePattern = "\w+: (.+)"
        self.params = ast.literal_eval(re.match(linePattern, lines[0]).group(1))
        self.params.update(ast.literal_eval(re.match(linePattern, lines[1]).group(1)))
        self.result = float(lines[5].split("=")[1])
    
    def __repr__(self):
        return "params = {}, result = {}".format(self.params, self.result)

def parseInput():
    results, lBuffer = [], []
    for l in sys.stdin:
        if l == "\n":
            results.append(Result(lBuffer))
            lBuffer = []
        else:
            lBuffer.append(l)
    return results

def emitRowColNames():
    print(" ".join(params[rowParam]))
    print(" ".join(params[colParam]))

def findResult(p):
    for r in results:
        if r.params == p:
            return r.result

def getBaseParams():
    baseParams = params.copy()
    del baseParams[rowParam]
    del baseParams[colParam]
    return baseParams
            
def emitValues():
    baseParams = getBaseParams()
    rowChoices, colChoices = params[rowParam], params[colParam]
    for rc in rowChoices:
        resultRow = []
        for cc in colChoices:
            p = baseParams.copy()
            p[rowParam] = rc
            p[colParam] = cc
            resultRow.append(findResult(p))
        print(" ".join(str(v) for v in resultRow))


parser = argparse.ArgumentParser()
parser.add_argument("paramFile")
args = parser.parse_args()
execfile(args.paramFile)
results = parseInput()
emitRowColNames()
emitValues()
