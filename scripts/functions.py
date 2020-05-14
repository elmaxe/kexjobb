import re
import math
from morphon import Morph, Nodes
import random as r

"""
Randomly translates a morphon Morph placing the center of the neuron inside the cuboid 
defined by x in [0, xLen), y in [0, yLen), z in [0, zLen). 
"""
def randomlyTranslate(m, xLen, yLen, zLen):
  xd, yd, zd = r.random()*xLen, r.random()*yLen, r.random()*zLen
  m.translate((xd, yd, zd))

# Takes a filepath, returns morph object
def morphFromFile(filepath):
  m = Morph()
  m.load(filepath)
  return m

"""
Takes a list of Morph objects and converts them to a single string 
of the form 'x y z label' where label is 'n'+the index of the neuron.
"""
def morphListToStringList(morphs):
  return [morphToStrings(m, id) for (i, m) in enumerate(morphs)]

"""
Randomly rotates a morphon Morph object around the y-axis (0, 1, 0) with uniform distribution of rotation angles.
Adapted from Kozlov's sample code.
"""
def randomlyRotate(m):
  axis = (0, 1, 0) # the y-axis, as is appropriate for the Allen institute human pyramidal cells
  angle = math.pi*2.0*r.random() # value in range [0, 2*math.pi)
  m.rotate(axis, angle)

"""
Randomly scales a neuron by a random factor in the range [lowScale, highScale), uniform distribution
"""
def randomlyScale(m, lowScale, highScale):
  factor = r.uniform(lowScale, highScale)
  m.scale(factor)

"""
Converts a morphon Morph object into a list of strings of the form 
'x y z label', where label is an n followed immediately by the id.
Implementation based on the save function in morphon/swc. If xMin, xMax, etc 
are specified, points not satisfying these constraints are discarded.
Note: Newlines at the end of each string. 
"""
def morphToStrings(m, id, xMin=-math.inf, xMax=math.inf, yMin=-math.inf, yMax=math.inf, zMin=-math.inf, zMax=math.inf):
  data = []
  for item in m.traverse(): 
    (t, (x, y, z), r) = m.value(item)
    if(xMin <= x and x <= xMax and yMin <= y and y <= yMax and zMin <= z and z <= zMax):
      data.append("%f %f %f n%d\n" % (x, y, z, id))
  return data

# Returns a random tuple of (x, y, z) present in a morphology
def randomPointInMorph(m):
  item = r.choice([i for i in m.traverse()])
  (t, (x, y, z), radius) = m.value(item)
  return (x, y, z)

"""
Writes a morph to a file
"""
def appendMorphToFile(m, id, filepath):
  f = open(filepath, "a")
  f.write("".join(morphToStrings(m, id)))

"""
Writes (appends) a morph to a file s.t. only points within the 
specified volume are actually included in the file. Other points
are discarded.
"""
def appendMorphToFileTrimmed(m, id, filepath, xMin, xMax, yMin, yMax, zMin, zMax):
  f = open(filepath, "a")
  f.write("".join(morphToStrings(m, id, xMin, xMax, yMin, yMax, zMin, zMax)))
