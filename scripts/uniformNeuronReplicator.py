import random as r
import functions as f

QUERIES = 200
# 5 micrometers is used in the FLAT paper
QUERY_RANGE = 5.0

"""
Replicates a set of neurons randomly inside a volume, such that the center
of each neuron is drawn from a uniform 3-dimensional distribution. The centers 
of the neurons are placed s.t. x is in [0, xLen), y is in [0, yLen), and z is 
in [0, zLen). The neuron picked for placement is drawn from a uniform 
distribution as well. 

Parameters: 
  neurons: a list of lists of tuples of the form (x, y, z), such that each list represents one neuron
  xLen, yLen, zLen: the extension of the volume in which to place the neurons along each axis (in micrometers)
  density: neurons per cubic millimeter
  seed: random seed, integer

Returns: 
  a list of the same format as the neurons argument
"""
def replicate(neurons, xLen, yLen, zLen, density, seed):
  replicatedNeurons = []
  neurons = [f.centerAtOrigin(n) for n in neurons] # All neurons are origin-centered, so new pos obtained by adding random sample
  r.seed(seed)
  n = int(density*xLen*yLen*zLen/(10.0**9)) # volume is converted to mm3 by 10^-9 multiplication, then multiplied by density
  for i in range(n): 
    neuron = r.choice(neurons)
    newPos = (r.random()*xLen, r.random()*yLen, r.random()*zLen)
    newNeuron = [(x+newPos[0], y+newPos[1], z+newPos[2]) for (x, y, z) in neuron]
    replicatedNeurons.append(newNeuron)
  return replicatedNeurons


outputFile = open("../data/replicated.txt", "w+")
neuron = f.swcToPoints("../data/neuron1.swc")
newNeurons = replicate([neuron], 1000.0, 1000.0, 1000.0, 10000, r.random())
for i, n in enumerate(newNeurons): 
  for (x, y, z) in n:
    outputFile.write("%f %f %f n%d\n" % (x, y, z, i))

queriesFile = open("../data/queries.txt", "w+")
queryNeurons = r.choices(newNeurons, k=QUERIES)

for neuron in queryNeurons:
  x, y, z = r.choice(neuron)
  queriesFile.write("%f, %f, %f, %f\n" % (x, y, z, QUERY_RANGE))