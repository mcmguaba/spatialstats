import scipy
from alephoneHW2forHW3 import *
import math
import numpy
from scipy.linalg import inv,det

#could not get SetCluster working properly from last assignment, so tested my code with someone elses SetCLuster
#Input a working SetCluster class to run this code

# Quadratic Discriminant Analysis class 
class QuadraticDiscriminantAnalysis:
    def __init__ (self,dataTraining, classID, proportions = None): 
        self.dataTraining = dataTraining
        #get the number of labels (since numbering goes form 0 to K-1, set class ID equal to K)
        nClasses= int(classID.max() + 1)
        #get the stats for each labels
        self.means = []
        self.invVarCovarMatrix = []
        self.constant = [] #last 3 terms in equation
        for  i in range(nClasses):
            id = classID == i #array of bools
            proportions = id.mean() #ratio of trues:fales (sum of ones/# of entries)
            self.means.append(dataTraining[id, :].mean(axis= 0))
            varCovarMatrix = scipy.cov(dataTraining[id,:],rowvar=0)
            self.invVarCovarMatrix.append(inv(varCovarMatrix))
            self.constant.append(-0.5*scipy.dot(scipy.dot(self.means[-1],self.invVarCovarMatrix[-1]),scipy.transpose(self.means[-1]))
                                 +math.log(proportions) - 0.5*math.log(scipy.linalg.det(varCovarMatrix)))

    def classify(self,data):
        if type(data) is not scipy.ndarray: #ensures input data is in the right format
            print "The input data is of the wrong type, it should be an array"
            return None
        qdaMax = []
        for d in data:
            disc = []
            if len(d) == self.dataTraining.shape[1]: #ensures each observation has the correct number of variables
                for m,c,z in zip(self.means, self.invVarCovarMatrix,self.constant): #loops three variables simultaneously
                #employs qda discriminant function, constant (z) previously computed
                    disc.append(-.5*(scipy.dot(scipy.dot(d,c),scipy.transpose(d))) + scipy.dot(scipy.dot(d,c),scipy.transpose(m)) + z)
                qdaMax.append(scipy.argmax(disc))
        return qdaMax
               
# Nearest Neighbor class             
class NearestNeighborClassifier:
    def __init__(self, dataTraining, classID, proportions = None):
        #get the number of labels (since numbering goes form 0 to k-1, set class ID equal to k)
        nClasses = int(classID.max()+1)
        self.clusterLabel = []
        for i in range(nClasses) :
            dummyData = scipy.zeros(dataTraining.shape[1]) 
            self.clusterLabel.append(SetCluster(L2NormDistance,AveragePointSetDistance,dummyData))
            id = classID == i 
            for d in dataTraining[id,:]:
                self.clusterLabel[-1].assign(d)
            self.clusterLabel[-1].update()     
            
    def classify(self,data):
        if type(data) is not scipy.ndarray:
            print "The input data is of the wrong type, it should be an array"
            return None
        nnMinDistance = []
        for d in data :
            if len(d) == self.dataTraining.shape[1]:  #ensures each observation has the correct number of variables
                distance = []
                distance.append(scipy.array([c.distanceToSet(d) for c in self.clusterLabel])) #employs previously written SetCLuster class
                nnMinDistance.append(scipy.argmin(distance))
        return nnMinDistance
