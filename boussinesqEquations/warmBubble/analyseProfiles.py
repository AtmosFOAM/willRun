import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.tri as tri
import matplotlib.transforms as tr
import os,sys
    
execfile( os.path.join( sys.path[0], "dependencies.py" ) )
execfile( os.path.join( sys.path[0], "fieldClass.py" ) )
execfile( os.path.join( sys.path[0], "d_plots.py" ) )
# execfile( os.path.join( sys.path[0], "d_plots_resolution.py" ) )

times = np.array([500, 1000])
times = np.array([1000])

resolutions = np.array([ 100, 200, 400, 1000, 2000, 4000, 6666, 20000, 50000, 100000, 200000 ])
resolutions = np.array([ 100, 200, 400, 1000, 2000, 4000, 6666, 20000 ])
# resolutions = np.array([ 20000 ])
domainWidth = 20000.

error_norm = np.zeros(len(resolutions))

simulations = []
simulations.append( ["1Fluid", "k"] )
simulations.append( ["2Fluid", "r"] )
# simulations.append( ["xyzData", "Test", "m"] )

folderProfiles = os.path.join(sys.path[0], "zplots_profiles")

zOneColumn = np.arange(-50.,10150.,100.)
zOneColumn[0] = 0.
zOneColumn[-1] = 10000.
zfOneColumn = np.arange(0.,10100.,100.)

# rms_error_theta(zOneColumn, resolutions, simulations, 500)
rms_error_theta(zOneColumn, resolutions, simulations, 1000)
# rms_error_ztheta(zOneColumn, dx, simulations)
# heat_transport_error_theta(zOneColumn, dx, simulations)

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
    fieldsExpected = allFields(zOneColumn, folder=folderExpected)
    
    
    for simulation in simulations:
        print simulation[0]
        simulationData = []
        
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
            simulationData.append(fields)
            
            
            # if resolution == 20000:
                # plot_all_profiles("filled", time, zOneColumn, fields, fieldsExpected, folder=folderProfiles, plotExpected=True, fillSigma=True, showTitle=True)
            
    # plot_sigma_resolution(zOneColumn, sigma, expected.sigma[1], dx, simulations[sim][0], folder=folder_sigma)
    # plot_thetaMean_resolution(zOneColumn, thetaMean, thetaMean1fluid, expected.thetaMean, dx, simulations[sim][0], folder=folder_thetaMean, col_type=folders[j])
    # plot_theta_resolution(zOneColumn, theta, thetaVar, expected.theta, expected.thetaVar, dx, simulations[sim][0], folder=folder_thetas)
    # plot_w_resolution(zOneColumn, w, wVar, expected.w, expected.wVar, dx, simulations[sim][0], folder=folder_velocities)
    # plot_dExnerdz_resolution(zOneColumn, zf_oneColumn, dExnerdz, expected.dExnerdz, dx, simulations[sim][0], folder=folder_exner)
        

# plot_all_profiles("00_expectedProfiles", zOneColumn, expected, expected, expected=False)