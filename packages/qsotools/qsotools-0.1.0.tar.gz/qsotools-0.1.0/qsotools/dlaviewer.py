import quasar,numpy,seaborn
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator,FixedLocator

class dlaviewer(object):
    
    """
    Velocity plot of HI and metal regions of given absorption system.
    """
    
    def showhelp(self):
        
        print ""
        print "-------------------------------------------------------------------------"
        print ""
        print "description:"
        print ""
        print "  Velocity plot of HI and metal regions of given absorption system."
        print ""
        print "required arguments:"
        print ""
        print "   --qso      Path to the quasar spectrum to use."
        print "   --zabs     Redshift of the absorption system."
        print ""
        print "-------------------------------------------------------------------------"
        print ""
        quit()
        
    def __init__(self):
        
        if '-h' in sys.argv or '--help' in sys.argv: self.showhelp()
        elif '--qso' not in sys.argv or '--zabs' not in sys.argv:
            print 'ERROR: arguments --qso and/or --zabs not specified.'
            quit()
        # If metal list selected, discard non-listed transitions
        metlist = [Metallist[i]['ID'] for i in range(len(Metallist))]
        metlist = metlist if metals==None else numpy.loadtxt(metals,dtype=str)
        for i in range(len(Metallist)):
            if Metallist[i]['ID'] not in metlist:
                Metallist = numpy.delete(Metallist,i,0)
        rc('font', size=2, family='sans-serif')
        rc('axes', labelsize=8, linewidth=0.2)
        rc('legend', fontsize=2, handlelength=10)
        rc('xtick', labelsize=6)
        rc('ytick', labelsize=6)
        rc('lines', lw=0.2, mew=0.2)
        rc('grid', linewidth=0.2)
        fig = figure(figsize=(8.27,11.69))
        axis('off'),xticks(()),yticks(())
        subplots_adjust(left=0.05, right=0.95, bottom=0.01, top=0.95, hspace=0, wspace=0.05)
        plt.title(quasar.qso+'\n',fontsize=7)
        qsoname = re.split(r'[/.]',quasar.qso)
        readspec(quasar.qso)
        self.dla_specplot(fig)
        start_time = time.time()
        for Ntrans in range(0,31,1):
          Nplot=(2*Ntrans-1)+8
          self.dla_Hplot(fig,Ntrans,Nplot=Nplot)
        print 'HI plots prepared in',round(float(time.time()-start_time),3),'seconds.'
        start_time = time.time()
        for Ntrans in range(0,31,1):
            Nplot=(2*Ntrans-1)+9
            if Ntrans<len(quasar.Metallist):
                self.dla_metalplot(fig,Ntrans,Nplot=Nplot)
        print 'Metal plots prepared in',round(float(time.time()-start_time),3),'seconds.'
        savefig(qsoname[-2]+'.pdf')
        
    def dla_specplot(self,fig):
        
        """
        Plot the spectrum region from the detected Lyman-limit to the detected Lyman-alpha
        fig:   Figure to be plotted on
        Ncol:   Number of columns to plot over
        Nplot: Plot number
        """
        
        ymin   = -0.1
        ymax   = 1.2
        wmin   = (quasar.zabs+1)*quasar.HI[-1]['wave']-10
        wmax   = (quasar.zabs+1)*quasar.HI[0]['wave']+10
        ax = fig.add_subplot(20,1,1,xlim=[wmin,wmax],ylim=[ymin,ymax])
        ax.yaxis.set_major_locator(NullLocator())
        ax.xaxis.set_major_locator(NullLocator())
        ax.plot(quasar.wa,quasar.fl,'black',lw=0.2)
        ax.plot(quasar.wa,quasar.er,'cyan',lw=0.2)
        ax.axhline(y=0,ls='dotted',color='grey',lw=0.2)
        ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
        ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
        for trans in quasar.HI:
            ax.axvline(x=(quasar.zabs+1)*trans['wave'], color='red', lw=0.5)
        xmin = 10*round(wmin/10)
        xmax = 10*round(wmax/10)
        if 10*round((xmax-xmin)/100)>0:
            ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(xmin,xmax,10*round((xmax-xmin)/100))))
        else:
            ax.xaxis.set_major_locator(plt.FixedLocator([xmin,xmax]))            
    
    def dla_Hplot(self,fig,Ntrans,vmin=-5000.,vmax=5000.,Ncol=2,Nplot=10):
        
        """
        Plot the HI lines
        fig:     Figure to be plotted on
        Ntrans:  Transition number
        vmin:    Minimum velocity on plot in km/s
        vmax:    Maximum velocity on plot in km/s
        Ncol:    Number of columns to plot over
        Nplot:   Plot number
        """
        
        Nrows   = 36
        ymin    = 0
        ymax    = 1.2
        watrans = quasar.HI[Ntrans]['wave']*(quasar.zabs+1)    # observed wavelength of transition
        v       = (quasar.c*((quasar.wa-watrans)/quasar.wa))
        istart  = abs(v-vmin).argmin()
        iend    = abs(v-vmax).argmin()
        if istart<iend:
            ymax   = sorted(quasar.fl[istart:iend])[int(0.98*len(quasar.fl[istart:iend]))]
        if Ntrans==0:
            self.ax = fig.add_subplot(Nrows,Ncol,Nplot,xlim=[vmin,vmax],ylim=[ymin,ymax])
        else:
            self.ax = fig.add_subplot(Nrows,Ncol,Nplot,ylim=[ymin,ymax],sharex=self.ax)
        self.ax.set_xlim([vmin,vmax])
        self.ax.set_ylim([ymin,ymax])
        self.ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(-5000,5000,1000)))
        self.ax.yaxis.set_major_locator(NullLocator())
        self.ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
        if ('--nonoise' not in sys.argv) or ('--nonoise' in sys.argv and np.average(quasar.er[istart:iend]) < quasar.limfl):
            self.ax.plot(v,quasar.fl,'black',drawstyle='default',lw=0.2)
            self.ax.plot(v,quasar.er,'cyan',drawstyle='default',lw=0.2)
        self.ax.axvline(x=0,color='red',lw=2,alpha=0.5)
        if Ntrans<30:
            plt.setp(self.ax.get_xticklabels(), visible=False)
        else:
            self.ax.set_xlabel('Velocity relative to $z_{abs}='+str(round(quasar.zabs,6))+'$ (km/s)',fontsize=7)
    
    def dla_metalplot(self,fig,Ntrans,vmin=-5000.,vmax=5000.,Ncol=2,Nplot=11):
        
        """
        Plot the HI lines
        fig:     Figure to be plotted on
        Ntrans:  Transition number
        vmin:    Minimum velocity on plot in km/s
        vmax:    Maximum velocity on plot in km/s
        Ncol:    Number of columns to plot over
        Nplot:   Plot number
        """
        
        Nrows   = 36
        ymin    = 0
        ymax    = 1.2
        watrans = (quasar.zabs+1.)*quasar.Metallist[Ntrans]['Metalwave']
        v       = (quasar.c*((quasar.wa-watrans)/quasar.wa))
        istart  = abs(v-vmin).argmin()
        iend    = abs(v-vmax).argmin()
        if istart<iend:
            ymax   = sorted(quasar.fl[istart:iend])[int(0.98*len(quasar.fl[istart:iend]))]
        if Ntrans==0:
            self.ax = fig.add_subplot(Nrows,Ncol,Nplot,xlim=[vmin,vmax],ylim=[ymin,ymax])
        else:
            self.ax = fig.add_subplot(Nrows,Ncol,Nplot,ylim=[ymin,ymax],sharex=self.ax)
        self.ax.set_xlim([vmin,vmax])
        self.ax.set_ylim([ymin,ymax])
        self.ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(-5000,5001,1000)))
        self.ax.yaxis.set_major_locator(NullLocator())
        self.ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
        self.ax.plot(v,quasar.fl,'black',drawstyle='default',lw=0.2)
        self.ax.plot(v,quasar.er,'cyan',drawstyle='default',lw=0.2)
        t = self.ax.text(0.9*vmin,0.2*ymax,quasar.Metallist[Ntrans]['Metalline']+'_'+str(int(quasar.Metallist[Ntrans]['Metalwave'])),color='blue',fontsize=7)
        t.set_bbox(dict(color='white', alpha=0.9, edgecolor=None))    
        self.ax.axvline(x=0,color='red', lw=2,alpha=0.5)
        if Ntrans<30:
            plt.setp(self.ax.get_xticklabels(), visible=False)
        else:
            self.ax.set_xlabel('Velocity relative to $z_{abs}='+str(round(quasar.zabs,6))+'$ (km/s)',fontsize=7)

def dla_lyman():
    
    '''
    Evolution of full width at 0.2 vs order of Lyman series.
    Plot the evolution of the FWHM along the orders of the Lyman series, and write the values on
    an ASCII file. The file will be used by LLabs.py to estimate the column density of the Lyman
    alpha, and the FWHM of the next orders. In the ASCII file, each row represents different
    column densities and each column different order of the Lyman series. The plot shows that,
    for a given column density, the FWHM is not constant throughout the orders, which suggests 
    that the curve of growth is not valid for all Lyman transitions.
    '''

    if self.zabs==None:
        print 'ERROR: Make sure you specify the absorption redshift [--zabs]'
        quit()
    
    fig = figure(figsize=(10,8))
    op = open('DLAtrans.dat','w')
    col = np.arange(20,25.1,.2)
    dv = 5000
    for i in range (0,len(col)):
        print col[i]
        fwhm  = []
        order = []
        ordnb = 0
        for trans in self.HI:
            ref    = trans['wave']*(self.zabs+1)
            wmin   = ref * (1 - (dv/self.c))
            wmax   = ref * (1 + (dv/self.c))
            wave   = np.arange(wmin,wmax,0.01)
            flux   = p_voigt(col[i],25,wave,ref,trans['gamma'],trans['strength'])
            center = abs(wave-ref).argmin()
            midflx = 1-(1-flux[center])/2 if self.midflx==None else self.midflx
            first  = flux[0:center]
            second = flux[center:(len(flux)-1)]
            a      = abs(first - midflx).argmin()
            b      = abs(second - midflx).argmin()
            width  = (wave[center+b]-wave[a])/wave[center+b]*self.c
            order.append(ordnb)
            fwhm.append(width)
            op.write(str(width)+' ')
            ordnb  = ordnb+1
        op.write('\n')
        ax = fig.add_subplot(1,1,1,xlim=[0,30],ylim=[0,1000])
        if round(col[i],1)==20:
            plot(order,fwhm,'blue',lw=0.5,label='$N_{HI}=20$')
        elif round(col[i],1)==25:
            plot(order,fwhm,'red',lw=0.5,label='$N_{HI}=25$')
        else:
            plot(order,fwhm,'black',lw=0.2)
        xlabel('Order of the Lyman series')
        ylabel('Full width at '+str(midflx)+' of the saturated high column density line')
        leg = legend(loc='upper right')
        leg.get_frame().set_alpha(0)
        i = i + 1
    savefig('plot_lyman.pdf')
    clf()
    op.close()

def dla_coldens():
    
    '''
    Evolution of FWHM vs column density with b=25.
    Plot the evolution of the FWHM with the column density for each order of the Lyman series.
    '''

    fig = figure(figsize=(10,8))
    col = np.arange(15,27,.01)
    dv = 5000.
    for trans in self.HI:
        fwhm = []
        i = 0
        print trans['wave']
        while (i < len(col)):
            ref    = trans['wave']*(z+1)
            wmin   = ref * (1 - (dv/self.c))
            wmax   = ref * (1 + (dv/self.c))
            wave   = np.arange(wmin,wmax,0.01)
            flux   = p_voigt(col[i],25,wave,ref,trans['gamma'],trans['strength'])
            center = abs(wave-ref).argmin()
            midflx = 1-(1-flux[center])/2 if len(sys.argv)==2 else 0.005 if float(sys.argv[2])==0 else float(sys.argv[2])
            first  = flux[0:center]
            second = flux[center:-1]
            a      = abs(first - midflx).argmin()                   # red position when the absorption intersect the midflux
            b      = abs(second - midflx).argmin()                  # blue position when the absorption intersect the midflux
            fwhm.append((wave[center+b]-wave[a])/wave[center+b]*self.c)  # width of the line at midflux position
            i = i + 1
        ax = fig.add_subplot(1,1,1,xlim=[15.5,26.5],ylim=[0,1000])
        if trans['wave']==1215.6701:
            plot(col,fwhm,'blue',lw=0.2,label='HI 1215.6701')
        elif trans['wave']==912.645:
            plot(col,fwhm,'red',lw=0.2,label='HI 912.645')
        else:
            plot(col,fwhm,'black',lw=0.2)
    xlabel('Column Density')
    ylabel('FWHM')
    leg = legend(loc='upper left')
    leg.get_frame().set_alpha(0)
    savefig('plot_coldens.pdf')
    clf()

def dla_profile():

    '''
    Lyman series for 2 systems, same N, different b.
    Plot all the Lyman transitions for 2 systems with same high column density, but different b
    values in order to show that the FWHM is different for higher order of Lyman series. This
    confirms that the curve of growth is only verified for Lyman-alpha, i.e. same FWHM for 
    different b for high column density systems.
    '''

    fig = figure(figsize=(8,10))
    subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.96, hspace=0, wspace=0.05)
    dv = 500
    col= 19.5
    k = 1
    dop = [20,30]
    for trans in self.HI:
        for i in range(0,len(dop)):
            print trans['wave']
            ref   = trans['wave']*(z+1)
            wmin  = ref * (1 - (dv/self.c))
            wmax  = ref * (1 + (dv/self.c))
            wave  = np.arange(wmin,wmax,0.0001)
            flux  = p_voigt(col,dop[i],wave,ref,trans['gamma'],trans['strength'])
            flux  = gaussian_filter1d(flux,1.5)
            vel   = ((wave - ref) / ref) * self.c
            ax    = fig.add_subplot(len(self.HI),len(dop),k,xlim=[-dv,dv],ylim=[0,1])
            plot(vel,flux,'black',lw=0.2)
            ax.xaxis.set_major_locator(NullLocator())
            ax.yaxis.set_major_locator(NullLocator())
            ax.axvline(x=0, color='blue', lw=0.2)
            if ((k == 1) or (k == 2)):
                title('log N(HI)='+str(col)+', b='+str(dop[i])+" km/s",fontsize=7)
            text(-9*dv/10,0.5,'Ly_'+str(round(trans['wave'],2)),color='blue',fontsize=7)
            if ((k == 2*len(self.HI)) or (k == 2*len(self.HI)-1)):
                plt.xticks((np.arange(-dv,dv,100)))
            k = k + 1
    savefig('plot_profile.pdf')

def dla_ascii():

    '''
    Tabulate full width for different profile in N,b parameter space.
    Create, for each order, an ASCII file with the N,b parameter space since the FWHM changes
    for different b values at higher orders of the Lyman series. For each ASCII file, each row
    represents the column density, and each column, the b values.
    '''

    dv = 20000
    tn = 0
    for trans in self.HI:
        op  = open('HI'+str(tn)+'.dat','w')
        col = np.arange(19.5,23,0.01)
        for i in range (0,len(col)):
            dop = np.arange(10,50,1)
            for k in range (0,len(dop)):
                ref    = trans['wave']*(z+1)
                wmin   = ref * (1 - (dv/self.c))
                wmax   = ref * (1 + (dv/self.c))
                wave   = np.arange(wmin,wmax,0.01)
                vprof  = p_voigt(col[i],dop[k],wave/(z+1),trans['wave'],trans['gamma'],trans['strength'])
                flux   = gaussian_filter1d(vprof,1.5)
                center = abs(wave-ref).argmin()
                midflx = 1-(1-flux[center])/2 if len(sys.argv)==2 else 0.005 if float(sys.argv[2])==0 else float(sys.argv[2])
                first  = flux[0:center]
                second = flux[center:(len(flux)-1)]
                a      = abs(first - midflx).argmin()
                b      = abs(second - midflx).argmin()
                width  = (wave[center+b]-wave[a])/wave[a]*self.c
                op.write(str('{:>15}'.format('%.4f'%width)))
                print trans['wave'],col[i],dop[k],width
            op.write('\n')
        op.close()
        tn = tn + 1

def dla_all():
    
    '''
    Plotting N,b parameter space profiles.
    Same as func4 but plotting the profiles instead of creating ASCII files.
    '''

    pdf_pages = PdfPages('plot_all.pdf')
    dv = 20000
    tn = 0
    for trans in self.HI:
        fig = figure(figsize=(10,8))
        subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
        col = np.arange(19.5,23,0.1)
        for i in range (0,len(col)):
            dop = np.arange(10,20,1)
            for k in range (0,len(dop)):
                pos  = i*len(dop)+k+1
                ax   = fig.add_subplot(len(col),len(dop),pos,xlim=[-20000,20000],ylim=[0,1])
                print trans['wave'],col[i],dop[k]
                ref  = trans['wave']*(z+1)
                wmin = ref * (1 - (dv/self.c))
                wmax = ref * (1 + (dv/self.c))
                wave = np.arange(wmin,wmax,0.01)
                flux = p_voigt(col[i],dop[k],wave/(z+1),trans['wave'],trans['gamma'],trans['strength'])
                vel  = ((wave - ref) / ref) * self.c
                plot(vel,flux,'black',lw=0.2)
                ax.xaxis.set_major_locator(NullLocator())
                ax.yaxis.set_major_locator(NullLocator())
                ax.axvline(x=0, color='blue', lw=0.2)
                text(-9*dv/10,0.5,str(col[i]),color='red',fontsize=5,horizontalalignment='left')
                text(9*dv/10 ,0.5,str(dop[k]),color='red',fontsize=5,horizontalalignment='right')
        tn = tn + 1
        pdf_pages.savefig(fig)
    pdf_pages.close()

def plot_lyman(spectrum=quasar.filename,zabs=quasar.zabs,dv=quasar.dv,output=quasar.output,model=quasar.model):
    '''
    Velocity plot of HI of given absorption system.

    Parameters
    ----------
    spectrum : str
      Path to quasar spectrum file
    zabs : float
      Absorption redshift
    dv : float
      Velocity dispersion of absorption system
    output : str
      Output file name
    model : bool
      Overplot model

    Examples
    --------

    >>> quasar plot_lyman -f spectrum.dat --zabs 4
    '''
    fig = plt.figure(figsize=(10,12),frameon=False,dpi=300)
    plt.axis('off')
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.3, wspace=0.05)
    plt.title(spectrum,fontsize=7)
    spec = quasar.get_data(spectrum)
    ymin = -0.1
    ymax = 1.2
    wmin = (zabs+1)*quasar.HI[-1]['wave']-10
    wmax = (zabs+1)*quasar.HI[0]['wave']+10
    ax = fig.add_subplot(20,1,1,xlim=[wmin,wmax],ylim=[ymin,ymax])
    ax.yaxis.set_major_locator(NullLocator())
    ax.xaxis.set_major_locator(NullLocator())
    ax.plot(spec.wa,spec.fl,'black',lw=0.2)
    ax.plot(spec.wa,spec.er,'cyan',lw=0.2)
    ax.axhline(y=0,ls='dotted',color='grey',lw=0.2)
    ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
    ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
    for trans in quasar.HI:
        ax.axvline(x=(zabs+1)*trans['wave'], color='red', lw=0.5)
    xmin = 10*round(wmin/10)
    xmax = 10*round(wmax/10)
    if 10*round((xmax-xmin)/100)>0:
        ax.xaxis.set_major_locator(plt.FixedLocator(numpy.arange(xmin,xmax,10*round((xmax-xmin)/100))))
    else:
        ax.xaxis.set_major_locator(plt.FixedLocator([xmin,xmax]))
    for i in range(0,30,1):
        iref    = 4 if i<10 else 5 if i<20 else 6
        nstep   = i if i<10 else i-10 if i<20 else i-20
        idx     = iref+3*nstep
        watrans = quasar.HI[i]['wave']*(zabs+1)
        v       = (quasar.c*((spec.wa-watrans)/spec.wa))
        istart  = abs(v+dv/2).argmin()
        iend    = abs(v-dv/2).argmin()
        ax = fig.add_subplot(11,3,idx)
        ax.set_title('HI %.2f'%quasar.HI[i]['wave'],fontsize=8)
        ax.set_xlim([-dv/2,dv/2])
        ax.set_ylim([-0.1,1.1])
        ax.axhline(y=0,ls='dotted',color='grey',lw=0.2)
        ax.axhline(y=1,ls='dotted',color='grey',lw=0.2)
        ax.plot(v,spec.fl,'black',drawstyle='default',lw=0.2)
        ax.plot(v,spec.er,'cyan',drawstyle='default',lw=0.2)
        if model:
            ax.plot(v,spec.mo,'orange',drawstyle='default',lw=0.5)
        ax.axvline(x=0,color='red',lw=1.5,alpha=0.5)
        if i in [9,19,29]:
            ax.set_xlabel('Velocity relative to $z_{abs}='+str(round(zabs,6))+'$ (km/s)',fontsize=7)
        else:
            plt.setp(ax.get_xticklabels(), visible=False)
        if i<10:
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        else:
            ax.yaxis.set_major_locator(NullLocator())
    plt.show() if output==None else savefig('lyman.pdf')
