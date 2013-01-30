import scipy
import pylab
import numpy

class myPLevelMetric:
    "Determines the area of the smallest circumscribing circle of the patch"
    def __call__(self,patchesList):  
        return scipy.array([0.5*scipy.pi*numpy.maximum(p.dx,p.dy)*numpy.maximum(p.dx,p.dy) for p in  patchesList])
    def name(self):
        return "MyPLevelMeticsCircleArea"
    def description(self):
        return "Area of the smallest circumscribing circle"

def getFragStatistics(patchList, plevelList, filename, showPlot = True):
    f = open(filename,"w")
    index = 0
    for p in plevelList :
        f.write("--------------------------------------------\n")
        f.write(p.name()+"\n")
        f.write(p.description()+"\n")
        metrics = p(patchList)
        #computes the class level statistics
        ave = metrics.mean()
        med = numpy.median(metrics)
        stdDev = numpy.std(metrics)
        min = numpy.min(metrics)
        max = numpy.max(metrics)
        range = max - min
        #writes the class level statistics to a data file
        f.write("Average: "+str(ave)+"\n")
        f.write("Median: "+str(med)+"\n")
        f.write("Standard Deviation: "+str(stdDev)+"\n")
        f.write("Minimum: "+str(min)+"\n")
        f.write("Maximum: "+str(max)+"\n")
        f.write("Range: "+str(range)+"\n")
        if(showPlot) :
            pylab.figure(index)
            pylab.hist(p(patchList), log = True) #used a log plot because frequency for smaller values is 
            #order of magnitudes larger than the frequency for larger values
            pylab.text(max*(2.0/3.0), 100,'Mean: '+str(round(ave,3))+"\n"+"Median: "+str(round(med,3))+"\n"
            "Standard Deviation: " +str(round(stdDev,3)) +"\n"+ "Minimum: "+str(round(min,3))+"\n"
            "Maximum: "+str(round(max,3)), horizontalalignment='left', bbox=dict(facecolor='none', alpha=0.5))
            pylab.title(p.name())
            index = index+1
    pylab.show()
    f.close()
        