import scipy
import numpy
import pylab
import variogram


fid = open("landsatBand1.dat",'rb') 
data = scipy.fromfile(file=fid, dtype=scipy.float32).reshape((500,500)) 
fid.close()
fid = open("landsatBand1Nan.dat",'rb') 
datanan = scipy.fromfile(file=fid, dtype=scipy.float32).reshape((500,500)) 
fid.close()
#pylab.figure() 
#pylab.subplot(121) 
#pylab.imshow(data,interpolation='nearest') 
#pylab.subplot(122) 
#pylab.imshow(datanan,interpolation='nearest') 
#pylab.show()
vario = variogram.ComputeSpatialStructure(data,[30,30], [90,90]) 
print vario(30,30)
#print vario(0,90), vario.nPairs(0,90) 
#print vario(120,0), vario.nPairs(120,0)