from collections import namedtuple
import sys

InputData = namedtuple("InputData", ["rowNames", "columnNames", "values"])

def readInput():
    rowNames = sys.stdin.readline().split(" ")
    columnNames = sys.stdin.readline().split(" ")
    values = []
    for l in sys.stdin:
        values.append(float(v) for v in l.split(" "))
    return InputData(rowNames, columnNames, values)

def emitBegin(f):
    beginLines = [
        "\\documentclass{article}",
        "\\usepackage{colortbl}",
        "\\begin{document}",
        "\\pagestyle{empty}"
    ]
    f.write("\n".join(l for l in beginLines) + "\n")

def emitTableBegin(f, columnNames):
    tabularLine = "\\begin{{tabular}}{{l | {}}}".format("".join("c" for cn in columnNames))
    f.write(tabularLine + "\n")
    firstRow = "& {} \\\\ \\hline".format(" & ".join(cn for cn in columnNames))
    f.write(firstRow + "\n")

def cellColor(value):
    colors = [
    (0.35, (0.0, 0.0, 1.0)),
    (0.5, (0.3, 1.0, 0.3)),
    (0.65, (1.0, 1.0, 0.0))]
    
    i = 0
    while i < len(colors) and colors[i][0] < value:
        i += 1
    if i == 0:
        return colors[0][1]
    if i == len(colors):
        return colors[len(colors) - 1][1]
    colorA = colors[i - 1]
    colorB = colors[i]
    factor = (value - colorA[0]) / (colorB[0] - colorA[0])
    return [factor * colorB[1][i] + (1 - factor) * colorA[1][i] for i in xrange(3)]

def cellStr(value):
    color = cellColor(value)
    colorStr = ", ".join(str(x) for x in color)
    brightness = (0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2])
    valueStr = ""
    if brightness < 0.4:
        valueStr = "\\textcolor{{white}} {{{0:.3f}}}".format(value)
    else:
        valueStr = "{0:.3f}".format(value)
    s = "\\cellcolor[rgb]{{{}}} {}".format(colorStr, valueStr)
    return s

def emitTableRow(f, rowName, rowValues):
    row = "{} & {} \\\\".format(rowName, (" & ".join(cellStr(v) for v in rowValues)))
    f.write(row + "\n")

def emitEnd(f):
    endLines = [
        "\\end{tabular}",
        "\\end{document}"
    ]
    f.write("\n".join(l for l in endLines) + "\n")

def writeTex(inData):
        emitBegin(sys.stdout)
        emitTableBegin(sys.stdout, inData.columnNames)
        for i in xrange(len(inData.rowNames)):
            emitTableRow(sys.stdout, inData.rowNames[i], inData.values[i])
        emitEnd(sys.stdout)

inData = readInput()
writeTex(inData)
