import random as r
import functions as f
import sys
from os import listdir
from os.path import isfile, join
from morphon import Morph


# Path where data is located
FOLDER_PATH = sys.argv[1]
# Path where output is saved
OUTPUT_DATA_FILE_PATH = sys.argv[2]
OUTPUT_QUERY_FILE_PATH = sys.argv[3]
# Length in micrometers
X_LENGTH = float(sys.argv[4])
Y_LENGTH = float(sys.argv[5])
Z_LENGTH = float(sys.argv[6])
# Neurons per cubic millimeter
DENSITY = float(sys.argv[7])
# Number of queries
QUERIES = int(sys.argv[8])
# Micrometers
QUERY_RANGE = float(sys.argv[9])

#### Script start
outputFile = open(OUTPUT_DATA_FILE_PATH, "w+")

# Get all SWC files in a folder and convert them to list of Morph objects
print("Using files: ", ", ".join([join(FOLDER_PATH, filepath) for filepath in listdir(FOLDER_PATH) if isfile(join(FOLDER_PATH, filepath)) and filepath.endswith(".swc")]))
print("Building Morph objects from files... ")
inputMorphs = [f.morphFromFile(join(FOLDER_PATH, filepath)) for filepath in listdir(FOLDER_PATH) if isfile(join(FOLDER_PATH, filepath)) and filepath.endswith(".swc")]

# Generate the data
newMorphs = f.replicate(inputMorphs, X_LENGTH, Y_LENGTH, Z_LENGTH, DENSITY)

# Convert the model into a single string and write if to a file
stringToWrite = f.morphListToString(newMorphs)
print("Writing final string to file...")
outputFile.write(stringToWrite)

# Open query file, select the neurons used for each query (with replacement, random.choices)
queriesFile = open(OUTPUT_QUERY_FILE_PATH, "w+")
queryMorphs = r.choices(newMorphs, k=QUERIES)

# For each neuron to be used for a query, select an actual point in it
for m in queryMorphs:
  x, y, z = f.randomPointInMorph(m)
  queriesFile.write("%f, %f, %f, %f\n" % (x, y, z, QUERY_RANGE))