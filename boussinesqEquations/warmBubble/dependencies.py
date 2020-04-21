def resort_array(arr):
    arr = np.array(arr)
    arr_new = np.zeros((len(arr[0]),len(arr)))
    for i in xrange(len(arr_new)):
        arr_new[i] = arr[:,i]
    return arr_new
    
def read_xyz_1d(filename, folder="", length=[4,1]):
    if folder == "":
        folder = sys.path[0]
        
    filename = os.path.join(folder, filename)
    
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
                    data_row = row.split("  ")
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
    
def bin_data(z, z_ref, data, weight=False):
    if type(weight) == bool:
        weight = np.ones(len(data))
        
    binned_data = np.zeros(len(z_ref))
    binned_data_tally = np.zeros(len(z_ref))
    
    for k in xrange(len(z)):
        dz = z_ref - z[k]
        z_index = np.argmin( np.abs(dz) )
        
        binned_data[z_index] += weight[k]*data[k]
        binned_data_tally[z_index] += weight[k]
        
    for k in xrange(len(binned_data_tally)):
        binned_data_tally[k] = max( binned_data_tally[k], 1e-16 )
        
    binned_data *= 1./binned_data_tally
    
    return binned_data
    
def bin_data_variance(z, z_ref, data, weight=False):
    if type(weight) == bool:
        weight = np.ones(len(data))
    
    data_mean = bin_data(z, z_ref, data, weight=weight)
    
    binned_data = np.zeros(len(z_ref))
    binned_data_tally = np.zeros(len(z_ref))
    
    for k in xrange(len(z)):
        dz = z_ref - z[k]
        z_index = np.argmin( np.abs(dz) )
        
        binned_data[z_index] += weight[k]*(data[k]-data_mean[z_index])**2
        binned_data_tally[z_index] += weight[k]
        
    for k in xrange(len(binned_data_tally)):
        binned_data_tally[k] = max( binned_data_tally[k], 1e-16 )
        
    binned_data *= 1./binned_data_tally
    
    return binned_data
    
def bin_data_minmax(z, z_ref, data):
    minimum =  999.*np.ones(len(z_ref))
    maximum = -999.*np.ones(len(z_ref))
    
    for k in xrange(len(z)):
        dz = z_ref - z[k]
        z_index = np.argmin( np.abs(dz) )
        
        if data[k] > maximum[z_index]:
            maximum[z_index] = data[k]
        if data[k] < minimum[z_index]:
            minimum[z_index] = data[k]
            
    return [minimum,maximum]
    
def save_legend(gca,name,ncols=4):
    legend_fig = plt.figure(figsize=(26,26))
    legend = plt.figlegend(*gca.get_legend_handles_labels(), loc='center', ncol=ncols, frameon=False)
    # legend = plt.legend(handles=gca, loc='center', ncol=ncols, frameon=False)
    legend_fig.canvas.draw()
    bbox = legend.get_window_extent().transformed(legend_fig.dpi_scale_trans.inverted())
    ll, ur = bbox.get_points()
    x0, y0 = ll
    x1, y1 = ur
    w, h = x1 - x0, y1 - y0
    x1, y1 = x0 + w * 1.1, y0 + h * 1.1
    bbox = tr.Bbox(np.array(((x0, y0),(x1, y1))))
    legend_fig.savefig(os.path.join(sys.path[0],'legend_%s.png' % (name)),bbox_inches=bbox)
    plt.close()

    
def append_hor(file1,file2,file3):
    "Horizontally add file2 to the right of file1."
    
    file1 = os.path.join(sys.path[0],file1)
    file2 = os.path.join(sys.path[0],file2)
    file3 = os.path.join(sys.path[0],file3)
    os.system("magick convert +append {} {} {}".format(file1,file2,file3))

def append_ver(files,output_file):
    "Vertically add file2 to the bottom of file1."
    temp_file = os.path.join(sys.path[0],"temp.png")
    
    for i in xrange(len(files)-1):
        file1 = temp_file
        if i == 0:
            file1 = os.path.join(sys.path[0],files[i])

        file2 = os.path.join(sys.path[0],files[i+1])

        file3 = temp_file
        if i == len(files)-2:
            file3 = os.path.join(sys.path[0],output_file)
    
        os.system("magick convert -append {} {} {}".format(file1,file2,file3))
        
    #Clean up phase
    if os.path.isfile( temp_file ):
        os.remove( temp_file )
    for i in xrange(len(files)):
        os.remove( os.path.join(sys.path[0],files[i]) )
        
        
def read_dat(filename, folder=""):
    if folder == "":
        filename = os.path.join(sys.path[0], filename)
    else:
        filename = os.path.join(folder, filename)
    
    file = open(filename, "r+")
    file_contents = file.read()
    file.close()
    
    dat_list = []
    
    file_lines = file_contents.split("\n")
    for line in file_lines:
        if len(line) > 0:
            if line[0] != "#":
                line = line.replace("  ", " ")
                dat_list.append( line.split(" ") )
            
    return dat_list