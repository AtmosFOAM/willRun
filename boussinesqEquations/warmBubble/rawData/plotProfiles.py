import os,sys
import numpy as np
import matplotlib
#Needed for some unix environments
if os.environ.get("DISPLAY", "") == "":
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.tri as tri
import matplotlib.transforms as tr

folderMain = os.path.dirname(os.path.realpath(__file__))
folderSrc = os.path.join(folderMain, "src")
folderProfiles = os.path.join(folderMain, "plots")
if not os.path.exists( folderProfiles ):
    os.makedirs( folderProfiles )

execfile( os.path.join( folderSrc, "utilities.py" ) )
execfile( os.path.join( folderSrc, "fields.py" ) )
execfile( os.path.join( folderSrc, "plotAllProfiles.py" ) )
execfile( os.path.join( folderSrc, "plotBuoyancyWithResolution.py" ) )

times = np.array([500, 1000])
# times = np.array([1000])

resolutions = np.array([ 100, 200, 400, 1000, 2000, 4000, 6666, 20000])
resolutions = np.array([ 4000, 6666, 20000 ])

simulations = []
simulations.append( ["1Fluid", "k"] )
simulations.append( ["2Fluid_DEFAULT", "r"] )
# simulations.append( ["2Fluid_gammaZero", "r"] )
# simulations.append( ["2Fluid_gammaZero_noTransfer", "r"] )
# simulations.append( ["2Fluid_noTransfer", "r"] )
# simulations.append( ["2Fluid_gaussianTransfer", "r"] )
# simulations.append( ["2Fluid_cosineSquaredTransfer", "r"] )
# simulations.append( ["2Fluid_wMeanTransfer", "r"] )
# simulations.append( ["2Fluid_wMeanCellTransfer", "r"] )


# z-coordinates needed for 
domainWidth = 20000.
zOneColumn = np.arange(-50.,10150.,100.)
zOneColumn[0] = 0.
zOneColumn[-1] = 10000.
zfOneColumn = np.arange(0.,10100.,100.)

# RMS errors for buoyancy profile and heat transport
# rms_error_theta(zOneColumn, resolutions, simulations, 500)
# rms_error_theta(zOneColumn, resolutions, simulations, 1000)
# rms_error_ztheta(zOneColumn, resolutions, simulations, 500)
# rms_error_ztheta(zOneColumn, resolutions, simulations, 1000)

for time in times:
    '''
    Initial & Expected profiles
    '''
    folderExpected = sys.path[0]
    folderExpected = os.path.join(folderExpected, "1Fluid")
    folderExpected = os.path.join(folderExpected, "200col")
    folderExpected = os.path.join(folderExpected, "conditionallyAveraged")
    folderExpected = os.path.join(folderExpected, "1col")
    folderExpected = os.path.join(folderExpected, str(time))
    fieldsExpected = allFields(zOneColumn, folder=folderExpected, oneFluid=True)
    
    
    for simulation in simulations:
        print "Plotting {} at t={}s".format(simulation[0], time)
        listFields = []
        
        for resolution in resolutions:
            nColumns = int(round( domainWidth/float(resolution) ))
            
            '''
            Obtained profiles
            '''
            
            if simulation[0] == "1Fluid":
                folder = sys.path[0]
                folder = os.path.join(folder, simulation[0])
                folder = os.path.join(folder, "{}col".format(nColumns))
                folder = os.path.join(folder, "conditionallyAveraged")
                folder = os.path.join(folder, "1col")
                folder = os.path.join(folder, "{}".format(time))
            else:
                folder = sys.path[0]
                folder = os.path.join(folder, simulation[0])
                folder = os.path.join(folder, "{}col".format(nColumns))
                folder = os.path.join(folder, "{}".format(time))
            
            fields = allFields(zOneColumn, folder=folder)
            listFields.append(fields)
            
            #Plot volume fraction, buoyancy, velocity and pressure side by side
            id = "{}_{}col".format(simulation[0], nColumns)
            plot_all_profiles(id, time, zOneColumn, fields, fieldsExpected, folder=folderProfiles, plotExpected=True, fillSigma=True, showTitle=True)
            
        if simulation[0] == "1Fluid":
            listFieldsOneFluid = listFields
        
        #Plot buoyancy profile variation with resolution
        plot_buoyancy(simulation[0], time, zOneColumn, resolutions, listFields, listFieldsOneFluid, fieldsExpected, folder=folderProfiles)
        
