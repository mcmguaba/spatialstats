import scipy
import math
#from scipy import stats

def ComputeSpatialStructure(raster,dimPixel=[1,1],maxLag=None,type="variogram"):
    #if type(raster) is not scipy.ndarray : return None
    #if scipy.dtype == bool : return None
    rastShape = scipy.shape(raster)
    [nx, ny] = [rastShape[0], rastShape[1]]
    if maxLag == None:
        maxLag = [nx/2, ny/2]
    else:
        maxLag = [int(maxLag[0]/dimPixel[0]) , int(maxLag[1]/dimPixel[1])]
    varArray = scipy.zeros(maxLag)
    pairsArray = scipy.zeros(maxLag)
    raster = scipy.array(raster)
    if type == "variogram":
        for lagX in range(maxLag[0]):
            for lagY in range(maxLag[1]):
                var = 0
                pairs = 0
                var = math.pow(raster[lagX:,lagY:] - raster[:-lagX,:-lagY],2) + var 
                        pairs = pairs + 1
                varArray[lagX,lagY] = var
                pairsArray[lagX,lagY] = pairs
        return SpatialStructure(varArray,maxLag[0],maxLag[1],dimPixel,pairsArray)
    elif type == "covariance":
        rasterMean = scipy.mean(raster[scipy.isfinite(raster)])
        for lagX in range(maxLag[0]):
            for lagY in range(maxLag[1]):
                covVar = 0
                pairs = 0
                for indexX in range(nx):
                    for indexY in range(ny):
                        covVar = (raster(indexX + lagX,indexY + lagY) - rasterMean)*(raster(indexX,indexY) - rasterMean) + covVar 
                        pairs = pairs + 1
                
        return SpatialStructure(float(var)/float(pairs),maxLag[0],maxLag[1],dimPixel,pairs)
    else:
        print 'Cannot recognize type, options for this parameter are variogram or covariance'
        return

class SpatialStructure: 
    def __init__(self, var, dx, dy, dimPixel, pairs):
        self.var = var
        self.pairs = pairs
        self.dimPixel = dimPixel
    def __call__(self,dx,dy):
        dx = int(dx/self.dimPixel[0])
        dy = int(dy/self.dimPixel[1])
        return self.var[dx,dy]
    def nPairs(self,dx,dy):
        dx = int(dx/self.dimPixel[0])
        dy = int(dy/self.dimPixel[1])
        return self.pairs