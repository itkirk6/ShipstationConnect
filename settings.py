import os

#pathing
cwd = os.getcwd()
parent = os.path.dirname(cwd)

#parent directories
pathToImages = os.path.join(cwd, 'images')
DefaultConfidence = 0.9

VERBOSE = True
