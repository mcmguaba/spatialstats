from alephoneHW4 import *
from pyFrag import *
import scipy
import pylab
f = open("clustersRemoteSensingK3","rb")
raster = scipy.fromfile(file=f, dtype=scipy.int32).reshape((500,500))
f.close()
[patchesRaster, patchesList] = SpatialFragmentation(raster == 1) 
plevelStats = [myPLevelMetric(),PatchYLength(),PatchXLength()] 
getFragStatistics(patchesList, plevelStats, "myFragStat.dat", True)
#f.write("Hello World\n") #Put the \ in order to put a put something on the next line.
#f.write("Hello again World\n")
#f.write(str(5)) 