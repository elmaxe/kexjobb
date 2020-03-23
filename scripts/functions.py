import re

"""
Shifts all points in a data set so that the mean x-, y-, and z-values are zero. 
Parameters: points, a list of tuples of the form (x, y, z)
"""
def centerAtOrigin(points):
  mean = meanPoint(points)
  return [(x-mean[0], y-mean[1], z-mean[2]) for (x, y, z) in points]

# Computes the mean point of a dataset
def meanPoint(points):
  n = len(points)
  xTotal, yTotal, zTotal = 0, 0, 0
  for p in points:
    xTotal += p[0]
    yTotal += p[1]
    zTotal += p[2]
  return (xTotal/n, yTotal/n, zTotal/n)

# Returns a list of tuples (x, y, z) given an SWC file
def swcToPoints(filepath):
  res = []
  inputFile = open(filepath)
  for line in inputFile:
    if re.match("\s*#.*\s*", line):
      continue
    else:
      tokens = line.split()
      index, flag, parent = int(tokens[0]), int(tokens[1]), int(tokens[6])
      x, y, z, r = float(tokens[2]), float(tokens[3]), float(tokens[4]), float(tokens[5])
      res.append((x, y, z))
  return res