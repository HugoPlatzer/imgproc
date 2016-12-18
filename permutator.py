from subprocess import call
import os
import itertools

if not os.path.exists('./data'):
    os.makedirs('./data')

def runFeatureVectorCommand(parameters):
    parameters = map(lambda p: str(p), parameters)
    vectorFile = "data/fv_" + '_'.join(parameters) + ".txt"
    command = "python fv.py " + ' '.join(parameters)+ " > " + vectorFile
    print "generating feature vectors: " + command
    call(command, shell=True)



colorSpaces = ['RGB', 'YUV', 'HSV', 'Lab']
wavelets = ['haar', 'db1', 'db10',  'db20', 'sym2', 'sym5', 'sym10', 'sym20', 'coif1', 'bior1.1', 'rbio1.1', 'dmey']
levels = range(2, 10, 1)

permutations = [colorSpaces, wavelets, levels]
permutations = itertools.product(*permutations)

map(runFeatureVectorCommand, permutations)