import scipy
import numpy
import random

#methods to calculate distance between two vectors
def L2NormDistance(x,y):
    return scipy.real(scipy.power(x-y,2).sum())
    
def L1NormDistance(x,y):
    return scipy.real(scipy.absolute(x-y).sum())
    
def L1InfNormDistance(x,y):
    return scipy.absolute((x-y)).max()

#methods to calculate distance between a set and a point
def AveragePointSetDistance(x,C,dist=L2NormDistance):
    initialDist = numpy.zeros(len(C))
    for i in range(len(initialDist)):
        initialDist[i] = dist(x,C[i])
        return numpy.average(initialDist)
    
def MaxPointSetDistance(x,C,dist=L2NormDistance):
    initialDist = numpy.zeros(len(C))
    for i in range(len(initialDist)):
        initialDist[i] = dist(x,C[i])
    return initialDist.max()
    
def MinPointSetDistance(x,C,dist=L2NormDistance):
    initialDist = numpy.zeros(len(C))
    for i in range(len(initialDist)):
        initialDist[i] = dist(x,C[i])
    return initialDist.min()

# Employs the means point representative 
class MeansCluster:
    def __init__(self,distance,data, tolerance = 0.00001):
        self.dist = distance
        self.newCentroid = scipy.zeros(data.shape[1])
        self.n = 0
        self.epsilon = 0
        self.tolerance = tolerance
        #selects a random point that is greater than the min and smaller than the max of the data set
        self.Centroid = [random.uniform(data[:,0].min(),data[:,0].max()), random.uniform(data[:,1].min(),data[:,1].max())]

    def distanceToPoint(self,z):
        return self.dist(z,self.Centroid)
        
    def assign(self,z):
        self.newCentroid = self.newCentroid + z
        self.n = self.n + 1
    
    def update(self):
        self.newCentroid = self.newCentroid/self.n
        self.epsilon = self.dist(self.newCentroid,self.Centroid)
        self.Centroid = self.newCentroid
        self.n = 0
        self.newCentroid=scipy.zeros(self.Centroid.shape)
    
    def reachedTolerance(self):
        return self.epsilon < self.tolerance
    
#employs the set representative method
class SetCluster:
    def __init__(self, distance, data, distanceToSet, tolerance = 0.00001):
        self.dist = distance
        self.newSet = []
        self.tolerance = tolerance
        self.distanceToSet = distanceToSet
        m = data.shape[0]
        rand = random.randint(0,m-1)
        self.Set = data[rand,:]    
    
    def distanceToSet(self,z):
        return self.distanceToSet(z,self.set)

    def assign(self,z):
        self.newSet.append(z)
    
    def update(self):
        self.epsilon = self.dist(scipy.mean(self.newSet,axis = 0), scipy.mean(self.set,axis = 0))
        print self.epsilon
        self.set = self.newSet
        self.newSet=[]
    
    def reachedTolerance(self):
        return self.epsilon < self.tolerance

        
def kmeans(data,K, clusterType = "MeansPointRepresentative", distancePointToPoint = L2NormDistance, distancePointToSet = AveragePointSetDistance): # could also input tolerance
    clusters = []
    if clusterType == 'MeansPointRepresentative':
        for k in range(K): 
            clusters.append(MeansCluster(distancePointToPoint,data)) #initializes the clusters as MeansPointRepresentative
    elif clusterType == 'SetRepresentative':
        for k in range(K):
            clusters.append(SetCluster(distancePointToPoint,distancePointToSet,data)) #initializes the cluster as set representative
    else:
        print "Unknown type of cluster"
        return None
    hasConverged = False
    iterations = 0
    while not hasConverged: #continues to run until clusters converge
        conv = []
        for d in data:
            distanceFromCluster = scipy.array([c.distanceToPointOrSet(d) for c in clusters])
            indexCluster = scipy.argmin(distanceFromCluster) # i have a weird error here when I use setCluster
            clusters[indexCluster].assign(d)
        for c in clusters:
            c.update()
            conv.append(c.reachedTolerance()) #tests to see if epsilon is below tolerance
        iterations = iterations + 1
        hasConverged = all(conv)
    print "The number of iterations is: ", iterations
    clusterID =[]
    for d in data: #creates cluster ID's
        distanceFromCluster = scipy.array([c.distanceToPointOrSet(d) for c in clusters])
        indexCluster = scipy.argmin(distanceFromCluster)
        clusterID.append(indexCluster)
        
    return [clusterID, clusters]    
