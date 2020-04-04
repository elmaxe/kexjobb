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
Implementation based on the save function in morphon/swc. 
Note: Newlines at the end of each string. 
"""
def morphToStrings(m, id):
  data = []
  for item in m.traverse(): 
    (t, (x, y, z), r) = m.value(item)
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
Replicates a set of neurons randomly inside a volume, such that the center
of each neuron is drawn from a uniform 3-dimensional distribution. The centers 
of the neurons are placed s.t. x is in [0, xLen), y is in [0, yLen), and z is 
in [0, zLen). The neuron picked for placement is drawn from a uniform 
distribution as well. Before placement, the neurons are randomly rotated around the 
y-axis (0, 1, 0) and randomly scaled by a factor of 0.8 to 1.2. 

Parameters: 
  neurons: a list of lists of tuples of the form (x, y, z), such that each list represents one neuron
  xLen, yLen, zLen: the extension of the volume in which to place the neurons along each axis (in micrometers)
  density: neurons per cubic millimeter

Returns: 
  A list of the resulting morphon Morph objects. 

"""
def replicate(morphs, xLen, yLen, zLen, density):

  LOW_SCALE = 0.8
  HIGH_SCALE = 0.8

  # Function applied to every copied neuron.
  # All neurons are origin-centered, so new pos obtained by randomly rotating, scaling, and translating.
  def processSingleMorph(m):
    randomlyRotate(m)
    randomlyScale(m, LOW_SCALE, HIGH_SCALE)
    randomlyTranslate(m, xLen, yLen, zLen)
  
  # volume is converted to mm3 by 10^-9 multiplication, then multiplied by density, to produce number of neurons in model
  n = int(density*xLen*yLen*zLen/(10.0**9)) 

  # Generate n randomly copied neurons, with replacement
  indices = range(len(morphs)) 
  print("Copying morphologies...")
  morphCopies = [morphs[i].copy() for i in r.choices(indices, k=n)] 

  # Apply the processing function to each neuron
  print("Applying processing function to each neuron...")
  for m in morphCopies: 
    processSingleMorph(m)

  return morphCopies
