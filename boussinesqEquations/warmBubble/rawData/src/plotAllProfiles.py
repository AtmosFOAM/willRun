def plot_contour(x, y, z, filename, cmap="seismic", xlim=[], ylim=[], title="", xlabel="", ylabel="", levels=10, vmin=0., vmax=1.):
    
    plt.figure()

    triang = tri.Triangulation(x, y)
    contours = plt.tricontourf(triang, z, levels, cmap=cmap, vmin=vmin, vmax=vmax)
    
    if xlim != []:
        plt.xlim(xlim)
    
    if ylim != []:
        plt.ylim(ylim)
        
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.suptitle(title)
    
    plt.gca().set_aspect("equal")
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

#Plot row of plots for each set of variables
def plot_all_profiles(id, time, z0, fields, fieldsExpected, folder=sys.path[0], plotExpected=False, fillSigma=False, showTitle=False):
    #Show axis in km
    z = 0.001*z0
    
    ax = []
    plt.figure(figsize=(8,2.5))
    gs = gridspec.GridSpec(1, 4, height_ratios=[1])
    
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
    
    plt.xlim(-70, 50)
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
    
def n_cols(resolution, one_column_limit=20000.):
    cols = []
    for i in xrange(len(resolution)):
        n = max( int(round(one_column_limit/float(resolution[i]))), 1 )
        cols.append( str(n) )
        
    return cols
    
def rms_error_theta(z_oneColumn, dx, simulations, time):

    x = []
    y = []
    
    for sim in xrange(len(simulations)):
        x_plot = []
        y_plot = []
        b_profiles = []
        
        for i in xrange(len(dx)):
            resolution = dx[i]
            nColumns = int(round( 20000./float(resolution) ))
            
            if simulations[sim][0] == "1Fluid":
                folder = sys.path[0]
                folder = os.path.join(folder, simulations[sim][0])
                folder = os.path.join(folder, "{}col".format(nColumns))
                folder = os.path.join(folder, "conditionallyAveraged")
                folder = os.path.join(folder, "1col")
                folder = os.path.join(folder, "{}".format(time))
            else:
                folder = sys.path[0]
                folder = os.path.join(folder, simulations[sim][0])
                folder = os.path.join(folder, "{}col".format(nColumns))
                folder = os.path.join(folder, "{}".format(time))
                
            if os.path.isfile( os.path.join(folder, "b.xyz") ):
            
                x0,y0,z,b = read_xyz_1d("b.xyz", folder=folder)
                
                b = bin_data(z, z_oneColumn, b)
                
                if i == 0 and simulations[sim][0] == "1Fluid":
                    b_resolved = b
                    
                factor = 1.
                if dx[i] > 20000:
                    factor = dx[i]/20000.
                    
                
                # b = factor*( b - 300.*(factor - 1.)/factor )
                b = 300. + factor*( b - 300. )
                error_norm[i] = np.sqrt( np.sum( (b - b_resolved)**2 ) / len(z_oneColumn) )
                
                x_plot.append(dx[i])
                y_plot.append(error_norm[i])
                b_profiles.append(b)
                print "{}m resolution, Error: {}".format(resolution, error_norm[i])
                
        x.append(x_plot)
        y.append(y_plot)

    grey_zone_x = [1000,100000]
    grey_zone_y = [10,10]
    y0 = [0,0]
    
    fig = plt.figure(figsize=(9,3))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    ax1.fill_between(grey_zone_x,grey_zone_y,y0,color="#d6d6d6")
    ax1.plot([10000,10000],[0,10],"k:")
    
    for i in xrange(len(simulations)):
        # print y[i]
        
        linewidth = 1.
        marker1 = "."
        if i == 0:
            linewidth = 3.5
            marker1 = "o"
        
        ax1.plot(x[i], y[i], color=simulations[i][1], linewidth=linewidth)
        ax1.plot(x[i], y[i], color=simulations[i][1], marker=marker1, linewidth=0.)

    
    ax1.set_xlabel("Column width (m)")
    ax1.set_xscale("log")
    ax1.set_xlim(np.min(dx),np.max(dx))
    
    ax1.text(1300, 0.01, "The grey zone", va="center",color="#555555", fontsize=14)
    
    ax2.set_xscale("log")
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(x[0])
    ax2.set_xticklabels(n_cols(x[0]))
    ax2.minorticks_off()
    ax2.set_xlabel("Number of columns")
    
    ax1.set_ylim(0.,0.026)
    ax1.set_ylabel("RMS error")
    # save_legend(plt.gca(),"b_errors",ncols=1)
    plt.savefig( os.path.join( sys.path[0], "rms_error_b_{}.png".format(time) ), bbox_inches="tight", dpi=200 )
    plt.close()
    
    
    
    
def rms_error_ztheta(z_oneColumn, dx, simulations, time):

    x = []
    y = []
    
    for sim in xrange(len(simulations)):
        x_plot = []
        y_plot = []
        b_profiles = []
        
        for i in xrange(len(dx)):
            resolution = dx[i]
            nColumns = int(round( 20000./float(resolution) ))
            
            if simulations[sim][0] == "1Fluid":
                folder = sys.path[0]
                folder = os.path.join(folder, simulations[sim][0])
                folder = os.path.join(folder, "{}col".format(nColumns))
                folder = os.path.join(folder, "conditionallyAveraged")
                folder = os.path.join(folder, "1col")
                folder = os.path.join(folder, "{}".format(time))
            else:
                folder = sys.path[0]
                folder = os.path.join(folder, simulations[sim][0])
                folder = os.path.join(folder, "{}col".format(nColumns))
                folder = os.path.join(folder, "{}".format(time))
            
            if os.path.isfile( os.path.join(folder, "b.xyz") ):
            
                x0,y0,z,b = read_xyz_1d("b.xyz", folder=folder)
                
                b = bin_data(z, z_oneColumn, b)
                
                if i == 0 and simulations[sim][0] == "1Fluid":
                    zb_resolved = np.sum( z_oneColumn*b )
                    
                factor = 1.
                if dx[i] > 20000:
                    factor = dx[i]/20000.
                    
                
                # b = factor*( b - 300.*(factor - 1.)/factor )
                b = 300. + factor*( b - 300. )
                error_norm[i] = np.abs( np.sum(z_oneColumn*b) - zb_resolved ) / 1000.
                
                x_plot.append(dx[i])
                y_plot.append(error_norm[i])
                b_profiles.append(b)
                print "{}m resolution, Error: {}".format(resolution, error_norm[i])
                
        x.append(x_plot)
        y.append(y_plot)

    grey_zone_x = [1e3,1e5]
    grey_zone_y = [1e4,1e4]
    y0 = [0,0]
    
    fig = plt.figure(figsize=(9,3))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    ax1.fill_between(grey_zone_x,grey_zone_y,y0,color="#d6d6d6")
    ax1.plot([10000,10000],[0,1e4],"k:")
    
    for i in xrange(len(simulations)):
        
        linewidth = 1.
        marker1 = "."
        if i == 0:
            linewidth = 3.5
            marker1 = "o"
        
        ax1.plot(x[i], y[i], color=simulations[i][1], linewidth=linewidth)
        ax1.plot(x[i], y[i], color=simulations[i][1], marker=marker1, linewidth=0.)

    
    ax1.set_xlabel("Column width (m)")
    ax1.set_xscale("log")
    ax1.set_xlim(np.min(dx),np.max(dx))
    
    ax1.text(1300, 1, "The grey zone", va="center",color="#555555", fontsize=14)
    
    ax2.set_xscale("log")
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(x[0])
    ax2.set_xticklabels(n_cols(x[0]))
    ax2.minorticks_off()
    ax2.set_xlabel("Number of columns")
    
    ax1.set_ylim(0.,3.)
    # ax1.set_ylim(0.,0.5)
    ax1.set_ylabel("Heat transport diff.")
    # save_legend(plt.gca(),"b_errors",ncols=1)
    plt.savefig( os.path.join( sys.path[0], "rms_error_zb_{}.png".format(time) ), bbox_inches="tight", dpi=200 )
    plt.close()