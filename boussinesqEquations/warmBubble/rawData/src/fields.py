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
            if len(data) == 0:
                return np.zeros((length[0],length[1]))
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
    def __init__(self, zOneColumn, folder=None, oneFluid=False):
        self.sigma = fieldMultiFluid("sigma", zOneColumn, folder=folder)

        self.weightsSigma = [self.sigma.stable.field, self.sigma.buoyant.field]

        self.b = fieldMultiFluid("b", zOneColumn, folder=folder, weight=self.weightsSigma)
        # self.w = fieldMultiFluid("u", zOneColumn, folder=folder, vector=True, weight=self.weightsSigma)
        self.w = fieldMultiFluid("uz", zOneColumn, folder=folder, weight=self.weightsSigma)
        self.Pi = fieldMultiFluid("P", zOneColumn, folder=folder, weight=self.weightsSigma)


