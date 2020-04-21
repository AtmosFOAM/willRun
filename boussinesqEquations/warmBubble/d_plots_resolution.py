    
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||        SIGMA          ||||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_sigma_resolution(z, sigma, sigma_resolved, resolutions, filename, folder=sys.path[0]):
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        factor = 1.
        if resolutions[i] > 20000:
            factor = resolutions[i]/20000.
        sigma_resolved_adjusted = sigma_resolved/factor
        xmin = 0.
        xmax = 1./factor
        
        ax.append(plt.subplot(gs[i]))
        
        ax[i].fill_betweenx(z/1000., sigma[i], 0*sigma[i]+1., facecolor="b", linewidth=0.)
        ax[i].fill_betweenx(z/1000., sigma[i], 0*sigma[i], facecolor="r", linewidth=0.)
        ax[i].plot(sigma_resolved_adjusted, z/1000., color="k", linestyle=":")
        ax[i].plot(sigma[i], z/1000., color="k", linestyle="-", linewidth=2.)
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$\\sigma_i$")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.1*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        ax[i].xaxis.set_ticks( np.array([0.25/factor, 0.75/factor]) )
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_sigma_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()
    
    
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       MEAN THETA      ||||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_thetaMean_resolution(z, theta, theta1fluid, theta_resolved, resolutions, filename, folder=sys.path[0], col_type="oneCol"):
    
    col_factor = 1.
    if col_type == "threeCols":
        col_factor = 3.
    
    plt.figure(figsize=(2*len(resolutions),5))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        factor = 1.
        if resolutions[i] >= 20000:
            factor = col_factor*resolutions[i]/20000.
        theta_resolved_adjusted = (theta_resolved + 300.*(factor - 1.))/factor
        xmin = -0.1/factor
        xmax = 0.4/factor
        
        ax.append(plt.subplot(gs[i]))
        
        ax[i].plot(theta_resolved_adjusted-300., z/1000., color="k", linewidth=2.5, alpha=0.2)
        ax[i].plot(theta1fluid[i]-300., z/1000., color="k", linestyle="--", linewidth=1.)
        ax[i].plot(theta[i]-300., z/1000., color="k", linestyle="-", linewidth=2.5)

        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$\\overline{\\theta}$ (+300K)")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(0.5*(xmax+xmin), 9.2, "$\\Delta x = %s $km" % (resolution), ha="center", va="center",color="#555555", fontsize=10, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        # ax[i].xaxis.set_ticks( np.array([0., xmax/2., xmax]) )
        ax[i].xaxis.set_ticks( np.array([0., 0.3/factor]) )
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_thetaMean_dx_{}.png".format(filename) ) , bbox_inches="tight", dpi=200 )
    plt.close()
    
    
    
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       FLUID THETAS      ||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_theta_resolution(z, theta, thetaVar, theta_resolved, thetaVar_resolved, resolutions, filename, folder=sys.path[0]):
    z = z.copy()/1000.
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        xmin = 300. - 0.3
        xmax = 300. + 1.5
        
        ax.append(plt.subplot(gs[i]))
                
        '''
        Expected profiles
        '''
        theta0_under = theta_resolved[0] - np.sqrt(thetaVar_resolved[0])
        theta0_over  = theta_resolved[0] + np.sqrt(thetaVar_resolved[0])
        theta1_under = theta_resolved[1] - np.sqrt(thetaVar_resolved[1])
        theta1_over  = theta_resolved[1] + np.sqrt(thetaVar_resolved[1])
        
        ax[i].fill_betweenx(z, theta0_under, theta0_over, facecolor=(0.,0.,0.5), linewidth=0., alpha=0.1)
        ax[i].fill_betweenx(z, theta1_under, theta1_over, facecolor=(0.5,0.,0.), linewidth=0., alpha=0.1)
        ax[i].plot(theta_resolved[0], z, color=(0.,0.,0.5), linewidth=2.5, alpha=0.1)
        ax[i].plot(theta_resolved[1], z, color=(0.5,0.,0.), linewidth=2.5, alpha=0.1)
        
        '''
        Obtained profiles
        '''
        theta0_under = theta[i][0] - np.sqrt(thetaVar[i][0])
        theta0_over  = theta[i][0] + np.sqrt(thetaVar[i][0])
        theta1_under = theta[i][1] - np.sqrt(thetaVar[i][1])
        theta1_over  = theta[i][1] + np.sqrt(thetaVar[i][1])
        
        ax[i].fill_betweenx(z, theta0_under, theta0_over, facecolor=(0.,0.,1.), linewidth=0., alpha=0.5)
        ax[i].fill_betweenx(z, theta1_under, theta1_over, facecolor=(1.,0.,0.), linewidth=0., alpha=0.5)
        
        ax[i].plot(theta[i][0], z, color=(0.,0.,1.), linewidth=2.5)
        ax[i].plot(theta[i][1], z, color=(1.,0.,0.), linewidth=2.5)
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$\\theta_i$ (K)")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.1*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        ax[i].xaxis.set_ticks( np.array([300., 301.]) )
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_theta_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()
    
   
   
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       FLUID VELOCITIES  ||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_w_resolution(z, w, wVar, w_resolved, wVar_resolved, resolutions, filename, folder=sys.path[0]):
    z = z.copy()/1000.
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        xmin = -15.
        xmax = 15.
        
        ax.append(plt.subplot(gs[i]))
                
        '''
        Expected profiles
        '''
        w0_under = w_resolved[0] - np.sqrt(wVar_resolved[0])
        w0_over  = w_resolved[0] + np.sqrt(wVar_resolved[0])
        w1_under = w_resolved[1] - np.sqrt(wVar_resolved[1])
        w1_over  = w_resolved[1] + np.sqrt(wVar_resolved[1])
        
        ax[i].fill_betweenx(z, w0_under, w0_over, facecolor=(0.,0.,0.5), linewidth=0., alpha=0.1)
        ax[i].fill_betweenx(z, w1_under, w1_over, facecolor=(0.5,0.,0.), linewidth=0., alpha=0.1)
        ax[i].plot(w_resolved[0], z, color=(0.,0.,0.5), linewidth=2.5, alpha=0.1)
        ax[i].plot(w_resolved[1], z, color=(0.5,0.,0.), linewidth=2.5, alpha=0.1)
        
        '''
        Obtained profiles
        '''
        w0_under = w[i][0] - np.sqrt(wVar[i][0])
        w0_over  = w[i][0] + np.sqrt(wVar[i][0])
        w1_under = w[i][1] - np.sqrt(wVar[i][1])
        w1_over  = w[i][1] + np.sqrt(wVar[i][1])
        
        # ax[i].fill_betweenx(z, w0_under, w0_over, facecolor=(0.,0.,1.), linewidth=0., alpha=0.5)
        # ax[i].fill_betweenx(z, w1_under, w1_over, facecolor=(1.,0.,0.), linewidth=0., alpha=0.5)
        
        # ax[i].plot(w[i][0], z, color=(0.,0.,1.), linewidth=2.5)
        # ax[i].plot(w[i][1], z, color=(1.,0.,0.), linewidth=2.5)
        
        ax[i].plot( 50*( np.roll(w[i][0],1)-w[i][0] ),  z, color=(0.,0.,1.), linewidth=2.5, linestyle="--")
        ax[i].plot( 50*( np.roll(w[i][1],1)-w[i][1] ),  z, color=(1.,0.,0.), linewidth=2.5, linestyle="--")
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$w_i$ (ms$^{-1}$)")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.1*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        ax[i].xaxis.set_ticks( np.array([-10., 0., 10.]) )
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_w_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()
    
    
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       PRESSURE GRADIENTS      ||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_dExnerdz_resolution(z, zf, dExnerdz, dExnerdz_resolved, resolutions, filename, folder=sys.path[0]):
    z = z.copy()/1000.
    zf = zf.copy()/1000.
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    xmin = np.min(dExnerdz_resolved[1][2:-2])
    xmax = np.max(dExnerdz_resolved[1][2:-2])
    
    for i in xrange(len(resolutions)):
        
        ax.append(plt.subplot(gs[i]))
                
        '''
        Expected profiles
        '''
        ax[i].plot(dExnerdz_resolved[0], z, color=(0.,0.,0.5), linewidth=2.5, alpha=0.1)
        ax[i].plot(dExnerdz_resolved[1], z, color=(0.5,0.,0.), linewidth=2.5, alpha=0.1)
        
        '''
        Obtained profiles
        '''
        ax[i].plot(dExnerdz[i][0], zf, color=(0.,0.,1.), linewidth=2.5)
        ax[i].plot(dExnerdz[i][1], zf, color=(1.,0.,0.), linewidth=2.5)
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$\\theta_i$ (K)")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.1*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        # ax[i].xaxis.set_ticks( np.array([300., 301.]) )
        plt.locator_params(nbins=3,axis="x")
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_dExnerdz_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()
    
    
    
    
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       INTERNAL ENERGY   ||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_internalEnergy_resolution(z, internalEnergy, resolutions, filename, folder=sys.path[0]):
    z = z.copy()/1000.
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        xmin = -5e-4 * 1e3
        xmax =  5e-4 * 1e3
        
        ax.append(plt.subplot(gs[i]))
                
        '''
        Obtained profiles
        '''
        # ax[i].plot(0*internalEnergy[i][0], z, "k:")
        ax[i].plot(1e3*internalEnergy[i][0], z, color=(0.,0.,0.), linewidth=2.5)
        # ax[i].plot(internalEnergy[i][1], z, color=(1.,0.,0.), linewidth=2.5)
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$E_I$")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.5*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , ha="center", color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        # ax[i].xaxis.set_ticks( np.array([-0.2,0.,0.2]) )
        plt.locator_params(nbins=4,axis="x")
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_internalEnergy_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()
    
    

'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       POTENTIAL ENERGY   ||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_potentialEnergy_resolution(z, potentialEnergy, resolutions, filename, folder=sys.path[0]):
    z = z.copy()/1000.
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        xmin = -1.5e-4 * 1e3
        xmax =  1.5e-4 * 1e3
        
        ax.append(plt.subplot(gs[i]))
                
        '''
        Obtained profiles
        '''
        # ax[i].plot(0*potentialEnergy[i][0], z, "k:")
        ax[i].plot(1e3*potentialEnergy[i][0], z, color=(0.,0.,0.), linewidth=2.5)
        # ax[i].plot(potentialEnergy[i][1], z, color=(1.,0.,0.), linewidth=2.5)
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$E_P$")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.5*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , ha="center", color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        # ax[i].xaxis.set_ticks( np.array([-0.2,0.,0.2]) )
        plt.locator_params(nbins=4,axis="x")
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_potentialEnergy_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()
    
    
    
'''''''''''''''''''''''''''''''''''''''''''''''''''
||||||||||||       POTENTIAL ENERGY   ||||||||||||||
'''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_dryStaticEnergy_resolution(z, internalEnergy, potentialEnergy, resolutions, filename, folder=sys.path[0]):
    z = z.copy()/1000.
    
    plt.figure(figsize=(2*len(resolutions),7))
    
    gs = gridspec.GridSpec(1, len(resolutions), height_ratios=[1, 1])
    ax = []
    
    for i in xrange(len(resolutions)):
        
        xmin = -1.5e-4 * 1e3
        xmax =  1.5e-4 * 1e3
        
        ax.append(plt.subplot(gs[i]))
                
        '''
        Obtained profiles
        '''
        print resolutions[i], np.sum( (internalEnergy[i][0]+potentialEnergy[i][0])**2 )
        # ax[i].plot(0*potentialEnergy[i][0], z, "k:")
        ax[i].plot(1e3*(internalEnergy[i][0]+potentialEnergy[i][0]), z, color=(0.,0.,0.), linewidth=2.5)
        # ax[i].plot(potentialEnergy[i][1], z, color=(1.,0.,0.), linewidth=2.5)
        
        plt.xlim(xmin,xmax)
        plt.ylim(0.,10.)
        plt.xlabel("$E_I+E_P$")
        if i == 0:
            plt.ylabel("$z$ (km)")
        
        resolution = "{:.1f}".format(resolutions[i]/1000.)
        background_panel = dict(facecolor='w', alpha=0.8)
        plt.text(xmin+0.5*(xmax-xmin), 9., "$\\Delta x = %s $km" % (resolution) , ha="center", color="#888888", fontsize=14, bbox=background_panel)
        
        title = "{} columns".format( max(int(round(20000./resolutions[i])), 1) )
        if title == "1 columns":
            title = "1 column"
        plt.title( title )
        
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        # ax[i].xaxis.set_ticks( np.array([-0.2,0.,0.2]) )
        plt.locator_params(nbins=4,axis="x")
    
    for i in xrange(1,len(resolutions)):
        plt.setp(ax[i].get_yticklabels(), visible=False)
    
    plt.subplots_adjust(wspace=.0)
    
    plt.savefig( os.path.join( folder, "z_dryStaticEnergy_dx_{}.png".format(filename) ) , bbox_inches="tight" )
    plt.close()