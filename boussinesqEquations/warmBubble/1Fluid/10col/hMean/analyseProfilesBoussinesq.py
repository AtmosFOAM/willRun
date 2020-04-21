import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import os,sys

#Get command line arguments.
def readConsole(name, argv, default="0"):
    value = default
    if name in argv:
        index = argv.index(name)
        if len(argv) > index + 1:
            value = argv[index+1]
    return value


#Object for a field variable. 
#If not a multi-fluid field, leave weight as False.
class field:
    def __init__(self, name, zOneColumn, folder=None, vector=False, weight=False):
        if folder == None:
            folder = os.path.dirname(os.path.realpath(__file__))
        
        self.name = name
        self.filename = name + ".xyz"
        self.folder = folder
        self.zOneColumn = zOneColumn
        self.vector = vector
        self.weight = weight
        
        if vector == False:
            self.x, self.y, self.z, self.field = self.read_xyz(length=[4,len(zOneColumn)])
        else:
            self.x, self.y, self.z, u, v, self.field = self.read_xyz(length=[6,len(zOneColumn)])
            
        self.mean = self.conditionallyAverage()
        self.var = self.conditionallyAverageVariance()
        
    def read_xyz(self, length=[4,1]):

        filename = os.path.join(self.folder, self.filename)
        
        #If file does not exist, create array of zeros instead
        if not os.path.isfile(filename):
            return np.zeros((length[0],length[1]))
        else:
        
            #Read file and split into rows
            file = open(filename, "r+")
            string = file.read()
            file.close()
            
            rows = string.split("\n")
            
            data = []
            
            #Remove comment rows and sort into float data columns.
            for row in rows:
                if row != "":
                    if row[0] != "#":
                        data_row = row.replace("  ", " ")
                        data_row = data_row.split(" ")
                        for i in xrange(len(data_row)):
                            data_row[i] = float(data_row[i])
                            
                        data.append(data_row)
                    
            #Flip dimensions of data array so that 1 row of "data" is a single variable
            data_temp = np.array(data)
            data = np.zeros((len(data_temp[0]),len(data_temp)))
            for i in xrange(len(data)):
                data[i] = data_temp[:,i]
                
            #Sort all variables by z-axis position (data[2]).
            index_array = data[2].argsort()
            for i in xrange(len(data)):
                data[i] = data[i][index_array[::-1]]
                
            return data
            
    def conditionallyAverage(self):
        if type(self.weight) == bool:
            self.weight = np.ones(len(self.field))
            
        binned_data = np.zeros(len(self.zOneColumn))
        binned_data_tally = np.zeros(len(self.zOneColumn))
        
        for k in xrange(len(self.z)):
            dz = self.zOneColumn - self.z[k]
            z_index = np.argmin( np.abs(dz) )
            
            binned_data[z_index] += self.weight[k]*self.field[k]
            binned_data_tally[z_index] += self.weight[k]
            
        for k in xrange(len(binned_data_tally)):
            binned_data_tally[k] = max( binned_data_tally[k], 1e-16 )
            
        binned_data *= 1./binned_data_tally
        
        return binned_data
        
    def conditionallyAverageVariance(self):
        if type(self.weight) == bool:
            self.weight = np.ones(len(self.field))
        
        binned_data = np.zeros(len(self.zOneColumn))
        binned_data_tally = np.zeros(len(self.zOneColumn))
        
        for k in xrange(len(self.z)):
            dz = self.zOneColumn - self.z[k]
            z_index = np.argmin( np.abs(dz) )
            
            binned_data[z_index] += self.weight[k]*(self.field[k]-self.mean[z_index])**2
            binned_data_tally[z_index] += self.weight[k]
            
        for k in xrange(len(binned_data_tally)):
            binned_data_tally[k] = max( binned_data_tally[k], 1e-16 )
            
        binned_data *= 1./binned_data_tally
        
        return binned_data

#Object which contains conditionally averaged variables as well as the mean field.
class fieldMultiFluid:
    def __init__(self, name, zOneColumn, folder=None, vector=False, weight=[False,False]):
        self.name = name
        self.mean = field(self.name, zOneColumn, folder=folder, vector=vector, weight=False)
        self.stable = field(self.name+".stable", zOneColumn, folder=folder, vector=vector, weight=weight[0])
        self.buoyant = field(self.name+".buoyant", zOneColumn, folder=folder, vector=vector, weight=weight[1])

#Object which contains all of the fields required by the user.
class allFields:
    def __init__(self, zOneColumn, folder=None):
        self.sigma = fieldMultiFluid("sigma", zOneColumn, folder=folder)

        self.weightsSigma = [self.sigma.stable.field, self.sigma.buoyant.field]

        self.b = fieldMultiFluid("b", zOneColumn, folder=folder, weight=self.weightsSigma)
        # self.w = fieldMultiFluid("u", zOneColumn, folder=folder, vector=True, weight=self.weightsSigma)
        self.w = fieldMultiFluid("uz", zOneColumn, folder=folder, weight=self.weightsSigma)
        self.Pi = fieldMultiFluid("Pi", zOneColumn, folder=folder, weight=self.weightsSigma)
    
    
#Plot row of plots for each set of variables
def plot_all_profiles(id, time, z0, fields, fieldsExpected, folder=sys.path[0], plotExpected=False, fillSigma=False, showTitle=False):
    #Show axis in km
    z = 0.001*z0
    
    ax = []
    plt.figure(figsize=(8,4.5))
    gs = gridspec.GridSpec(1, 4, height_ratios=[1, 1])
    
    ##############################
    # Plot sigma                 #
    ##############################
    ax.append(plt.subplot(gs[0]))
    
    sigmaBuoyant = fields.sigma.buoyant.mean
    sigmaBuoyantColor = "black"
    
    if fillSigma:
        sigmaBuoyantColor = "white"
        ax[0].fill_betweenx(z, 0*sigmaBuoyant, sigmaBuoyant,   facecolor="red", linewidth=0.)
        ax[0].fill_betweenx(z, sigmaBuoyant, 0*sigmaBuoyant+1, facecolor="blue", linewidth=0.)
    
    if plotExpected:
        ax[0].plot(fieldsExpected.sigma.buoyant.mean, z, color=sigmaBuoyantColor, linewidth=1., linestyle="--")
    
    ax[0].plot(sigmaBuoyant, z, color=sigmaBuoyantColor, linewidth=1.)
    
    plt.xlim(0., 1.)
    plt.ylim(0., 10.)
    plt.xlabel("$\\sigma_1$")
    plt.ylabel("Height (km)")
    if showTitle:
        plt.title("Vol. fraction")
        
    
    ##############################
    # Plot buoyancy              #
    ##############################
    ax.append(plt.subplot(gs[1]))
    
    if plotExpected:
        b = fieldsExpected.b.mean.mean
        bStable = fieldsExpected.b.stable.mean
        bBuoyant = fieldsExpected.b.buoyant.mean
        
        ax[1].plot(bStable, z, color="blue", linewidth=1., linestyle="--")
        ax[1].plot(bBuoyant, z, color="red", linewidth=1., linestyle="--")
        ax[1].plot(b, z, color="black", linewidth=1., linestyle="--")
    
    b = fields.b.mean.mean
    bStable = fields.b.stable.mean
    bBuoyant = fields.b.buoyant.mean
    
    ax[1].plot(bStable, z, color="blue", linewidth=1.)
    ax[1].plot(bBuoyant, z, color="red", linewidth=1.)
    ax[1].plot(b, z, color="black", linewidth=1.)
    
    plt.xlim(-0.005, 0.025)
    plt.ylim(0., 10.)
    plt.xlabel("$b_i$")
    plt.locator_params(nbins=4,axis="x")
    if showTitle:
        plt.title("Buoyancy")
    
    
    ##############################
    # Plot vertical velocity     #
    ##############################
    ax.append(plt.subplot(gs[2]))
    
    if plotExpected:
        w = fieldsExpected.w.mean.mean
        wStable = fieldsExpected.w.stable.mean
        wBuoyant = fieldsExpected.w.buoyant.mean
        
        ax[2].plot(wStable, z, color="blue", linewidth=1., linestyle="--")
        ax[2].plot(wBuoyant, z, color="red", linewidth=1., linestyle="--")
        ax[2].plot(w, z, color="black", linewidth=1., linestyle="--")
    
    w = fields.w.mean.mean
    wStable = fields.w.stable.mean
    wBuoyant = fields.w.buoyant.mean
    
    ax[2].plot(wStable, z, color="blue", linewidth=1.)
    ax[2].plot(wBuoyant, z, color="red", linewidth=1.)
    ax[2].plot(w, z, color="black", linewidth=1.)
    
    plt.xlim(-9, 9)
    plt.ylim(0., 10.)
    plt.xlabel("$w_i$")
    plt.locator_params(nbins=4,axis="x")
    if showTitle:
        plt.title("Vert. velocity")
    
    
    ##############################
    # Plot pressure              #
    ##############################
    ax.append(plt.subplot(gs[3]))
    
    if plotExpected:
        PiStable = fieldsExpected.Pi.stable.mean
        PiBuoyant = fieldsExpected.Pi.buoyant.mean
        
        ax[3].plot(PiStable, z, color="blue", linewidth=1., linestyle="--")
        ax[3].plot(PiBuoyant, z, color="red", linewidth=1., linestyle="--")
    
    PiStable = fields.Pi.stable.mean
    PiBuoyant = fields.Pi.buoyant.mean
    
    ax[3].plot(PiStable, z, color="blue", linewidth=1.)
    ax[3].plot(PiBuoyant, z, color="red", linewidth=1.)
    
    plt.xlim(-50, 20)
    plt.ylim(0., 10.)
    plt.xlabel("$P_i$")
    plt.locator_params(nbins=4,axis="x")
    if showTitle:
        plt.title("Pressure anom.")
    
    
    ##############################
    # Format figure              #
    ##############################
    # if showTitle:
        # plt.suptitle( "Profiles after {}s".format(time), fontsize=18 )
    # plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    
    for i in xrange(1, len(ax)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    for i in xrange(len(ax)):
        xticks = ax[i].xaxis.get_major_ticks()
        xticks[0].label1.set_visible(False)
        xticks[-1].label1.set_visible(False)
        
        for tick in ax[i].xaxis.get_major_ticks():
            tick.label.set_fontsize(8) 
        
    plt.tight_layout()
    plt.subplots_adjust(wspace=.0)
    plt.savefig( os.path.join( folder, "profiles_{}_{}.png".format(time,id) ), bbox_inches="tight", dpi=200 )
    plt.close()


    
def main():
    time = readConsole("-time", sys.argv, default=1000)
    expectedProfilesPath = readConsole("-expectedProfiles", sys.argv, default="./")
    folderBase = os.path.dirname(os.path.realpath(__file__))
    
    #Cell-centred co-ordinates for z axis in range [0, 10]km with 100m grid spacing.
    #Make more general from command line in future versions.
    zOneColumn = np.arange(-50.,10150.,100.)
    zOneColumn[0] = 0.
    zOneColumn[-1] = 10000.
    
    #Initial & Expected profiles
    folder = os.path.join(folderBase, str(time))
    fields = allFields(zOneColumn, folder=folder)
    
    folderExpected = os.path.join(folderBase, expectedProfilesPath)
    fieldsExpected = allFields(zOneColumn, folder=folderExpected)

    plot_all_profiles("standard", time, zOneColumn, fields, fieldsExpected, folder=folderBase, plotExpected=True)
    plot_all_profiles("filled", time, zOneColumn, fields, fieldsExpected, folder=folderBase, plotExpected=True, fillSigma=True, showTitle=True)

main()