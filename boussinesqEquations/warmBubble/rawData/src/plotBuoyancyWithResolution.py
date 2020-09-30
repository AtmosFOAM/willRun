#Plot row of plots for each set of variables
def plot_buoyancy(id, time, z0, resolutions, fields, fieldsOneFluid, fieldsExpected, folder=sys.path[0], showTitle=True):
    #Show axis in km
    z = 0.001*z0
    xmin = -0.005
    xmax = 0.025
    
    nPlots = len(resolutions)
    ax = []
    plt.figure(figsize=(1.5*nPlots, 3.))
    # gs = gridspec.GridSpec(1, nPlots, height_ratios=[1, 1])
    gs = gridspec.GridSpec(1, nPlots)
    
    ##############################
    # Plot buoyancy              #
    ##############################
    for i in xrange(nPlots):
        resolution = resolutions[i]
        nColumns = max( int(round(20000./float(resolution))), 1 )
        ax.append(plt.subplot(gs[i]))
        
        b = fields[i].b.mean.mean
        bExpected = fieldsExpected.b.mean.mean
        bOneFluid = fieldsOneFluid[i].b.mean.mean
        
        ax[i].plot(bExpected, z, color="black", linewidth=1., linestyle=":")
        ax[i].plot(bOneFluid, z, color="black", linewidth=1., linestyle="--")
        ax[i].plot(b, z, color="black", linewidth=1.5, linestyle="-")
        
        plt.xlim(xmin, xmax)
        plt.ylim(0., 10.)
        plt.xlabel("$b$ (m s$^{-2}$)")
        if i == 0:
            plt.ylabel("Height (km)")
        plt.locator_params(nbins=4,axis="x")
        
        dx = "{:.1f}".format(resolution/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(0.5*(xmax+xmin), 9.2, "$\\Delta x = %s $km" % (dx), ha="center", va="center",color="#555555", fontsize=10, bbox=background_panel)
        if showTitle:
            if nColumns == 1:
                plt.title("1 column", fontsize=11.)
            else:
                plt.title("{} columns".format(nColumns), fontsize=11.)
    
    
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
        
    # plt.tight_layout()
    plt.subplots_adjust(wspace=.0)
    plt.savefig( os.path.join( folder, "buoyancyMean_{}_{}.png".format(time,id) ), bbox_inches="tight", dpi=200 )
    plt.close()