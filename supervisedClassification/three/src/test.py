from three import *
import scipy
import numpy
import random
import pickle
import pylab

#Load Training Data
fidT = open("mixtureGaussianTraining.pckl","r")
dataTraining = pickle.load(fidT)
fidT.close()
#Create the label vectors
classID = scipy.zeros(40)
classID[20:] = 1
#Load the "unknown" data
fid = open("mixtureGaussian.pckl","r")
data = pickle.load( fid )
fid.close()
#The real labels for the data the first 100 are label 0 and
# and the second half label 1

qdaClassifier = QuadraticDiscriminantAnalysis(dataTraining, classID)
qdaLabels = qdaClassifier.classify(data)
print qdaLabels
print len(qdaLabels)

#nnClassifier = NearestNeighborClassifier(dataTraining, classID)
#nnLabels = nnClassifier.classify(data)
#print nnLabels
