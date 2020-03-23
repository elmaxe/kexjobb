import sys
import re

inputFile = open(sys.argv[1], "r")
coordsFile = open(sys.argv[2], "w")
queryFile = open(sys.argv[3], "w")

for line in inputFile:
  if re.match("\s*#.*\s*", line):
    continue
  else:
    tokens = line.split()
    index, flag, parent = int(tokens[0]), int(tokens[1]), int(tokens[6])
    x, y, z, r = float(tokens[2]), float(tokens[3]), float(tokens[4]), float(tokens[5])
    coordsFile.write("%f, %f, %f, Neuron point\n" % (x, y, z))
    queryFile.write("%f, %f, %f, 5.0\n" % (x, y, z))
    