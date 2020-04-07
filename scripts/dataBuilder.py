"""
This script generates neuromorphological data in the form of points. It needs to 
be run from the directory in which it is located (i.e., using 'python3 dataBuilder.py')
"""
import random as r
import functions as f
import sys
from os import listdir
from os.path import isfile, join
from morphon import Morph

# See Kozlov's email (he refers to Markram 2015)
LOW_SCALE = 0.8
HIGH_SCALE = 1.2

# Path where data is located
INPUT_FOLDER_PATH = sys.argv[1]
# Folder where output is saved, MUST NOT END WITH A SLASH / 
OUTPUT_FOLDER_FILE_PATH = sys.argv[2]
# Length in micrometers
X_LENGTH = float(sys.argv[3])
Y_LENGTH = float(sys.argv[4])
Z_LENGTH = float(sys.argv[5])
# Neurons per cubic millimeter
DENSITY = float(sys.argv[6])
# Number of queries
QUERIES = int(sys.argv[7])
# Micrometers
EUCLID_QUERY_RANGE = float(sys.argv[8])
CHEBYSHEV_QUERY_RANGE = float(sys.argv[9])

# Function applied to every copied neuron.
# All neurons are origin-centered, so new pos obtained by randomly rotating, scaling, and translating.
def processSingleMorph(m, id):
  fp = OUTPUT_FOLDER_FILE_PATH+("/data-%d.txt"%DENSITY)
  f.randomlyRotate(m)
  f.randomlyScale(m, LOW_SCALE, HIGH_SCALE)
  f.randomlyTranslate(m, X_LENGTH, Y_LENGTH, Z_LENGTH)
  f.appendMorphToFileTrimmed(m, id, fp, 0, X_LENGTH, 0, Y_LENGTH, 0, Z_LENGTH)

# #### Script start
# queriesFileEuclid = open(OUTPUT_FOLDER_FILE_PATH + "/queries-%d-euclid.txt" % DENSITY, "w+")
# queriesFileChebyshev = open(OUTPUT_FOLDER_FILE_PATH + "/queries-%d-chebyshev.txt" % DENSITY, "w+")

# Get all SWC files in a folder and convert them to list of Morph objects
print("Using files: ", ", ".join([join(INPUT_FOLDER_PATH, filepath) for filepath in listdir(INPUT_FOLDER_PATH) if isfile(join(INPUT_FOLDER_PATH, filepath)) and filepath.endswith(".swc")]))
print("Building Morph objects from files... ", end="")
inputMorphs = [f.morphFromFile(join(INPUT_FOLDER_PATH, filepath)) for filepath in listdir(INPUT_FOLDER_PATH) if isfile(join(INPUT_FOLDER_PATH, filepath)) and filepath.endswith(".swc")]
print(" done.")

# volume is converted to mm3 by 10^-9 multiplication, then multiplied by density, to produce number of neurons in model
n = int(DENSITY*X_LENGTH*Y_LENGTH*Z_LENGTH/(10.0**9)) 

for i in range(n):
  m = r.choice(inputMorphs)
  processSingleMorph(m, i)
  if(i > 0 and (i+1) % 100 == 0):
    print("%d/%d neurons placed" % (i+1, n))
print("All neurons placed.")
