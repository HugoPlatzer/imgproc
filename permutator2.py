import os

FVParams = {"transformType" : ["dwt"], "colorSpace" : ["rgb"], "waveletFunction" : ["db1"],
"nLevels" : ["4"]}
ClassifierParams = {"testMethod" :  ["picture"], "k" : [3]}

FVFileName = "fv_auto.txt"
FVCmdline = lambda params : "python fv.py {} {} {} {} > {}".format(
        params["transformType"], params["colorSpace"], params["waveletFunction"],
        params["nLevels"])
ClassifierCmdline = lambda params : "python class.py {} {} < {}".format(
        params["testMethod"],
        params["k"])

s = os.popen("cat permutator2.py").read()
s = s.split("\n")
print(s)
