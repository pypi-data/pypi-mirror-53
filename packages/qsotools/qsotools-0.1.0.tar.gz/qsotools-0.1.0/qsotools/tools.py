import quasar
import matplotlib.pyplot as plt
from astropy.io import fits

def header():
    '''
    Show FITS header
    '''
    for i in range (len(self.qsolist)):
        hdulist = fits.open(self.qsolist[i])
        prihdr = hdulist[0].header
        if '--key' in sys.argv:
            print prihdr[self.key]
        else:
            print repr(prihdr)

def preview(qsolist=quasar.qsolist,spectrum=quasar.filename,fname=quasar.output):
    '''
    Plot spectrum and save as JPG
    '''
    qsolist = numpy.loadtxt(qsolist,dtype=str) if qsolist!=None else [spectrum]
    plt.rc('font', size=5, family='serif')
    plt.rc('axes', labelsize=12, linewidth=1)
    plt.rc('legend', fontsize=12, handlelength=10)
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    plt.rc('lines', lw=1, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    for i in range (0,len(qsolist)):
        qsoname  = qsolist[i].split('/')[-1].split('.')[0]
        datatype = qsolist[i].split('/')[-1].split('.')[-1]
        wa,fl,er = quasar.get_data(qsolist[i]) 
        fig = plt.figure(figsize=(20,2.5))
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0.)
        ax = plt.subplot(111,xlim=[4500,6000],ylim=[-0.2,1.2])
        plt.axis('off')
        #title(qsoname,fontsize=20)
        plt.plot(wa,fl,'black',drawstyle='steps',lw=1)
        #plot(wa,er,'cyan',drawstyle='steps')
        plt.xlabel('Observed Wavelength $\AA$',fontsize=12)
        plt.ylabel('Flux',fontsize=12)
        plt.text(3700,250,'J0745+4734\nz=3.22',fontsize=15)
        #ax.axhline(y=0, color='red', lw=0.5)
        #ax.axhline(y=1, color='red', lw=0.5)
        plt.show() if fname==None else plt.savefig(fname)
    
def show(spectrum=quasar.filename):
    '''
    Plot spectrum within IDLE window
    '''
    spec = quasar.get_data(spectrum)
    ymax = sorted(spec.fl)[int(0.95*len(spec.fl))]
    fig  = plt.figure()
    ax   = fig.add_subplot(111,xlim=[5000,5500],ylim=[-0.2,1.2])
    ax.plot(spec.wa,spec.fl,color='black',lw=1)
    ax.plot(spec.wa,spec.er,color='cyan',lw=1)
    ax.axhline(y=0, color='red', lw=0.2)
    ax.set_xlim([spec.wa[0],spec.wa[-1]])
    ax.set_ylim([0,ymax])
    plt.show()
    
def stack():
    '''
    Plot spectra from the same object on top of each other.
    QSpec stack Keck/Q1009p2956.fits Subaru/Q1009p2956.fits VLT/J101155+294141.fits
    '''
    fig = figure(figsize=(50,10*(len(self.qsolist))))
    subplots_adjust(left=0.03, right=0.97, bottom=0.08, top=0.95, hspace=0, wspace=0.05)
    xmid = (self.xmin+self.xmax)/2
    for i in range (0,len(self.qsolist)):
        spectrum   = self.qsolist[i]
        qsoname    = spectrum.split('/')[-1].split('.')[0]
        datatype   = spectrum.split('/')[-1].split('.')[-1]
        wa,fl,er,cont,sky,z = self.get_data(spectrum)
        ax = subplot(len(self.qsolist),1,i+1,xlim=[self.xmin,self.xmax],ylim=[-.5,1.5])
        ax.set_xlabel('Wavelength')
        ax.set_ylabel('Normalised Flux')
        ax.text(xmid,1.3,self.qsolist[i],color='blue',horizontalalignment='center',fontsize=30)
        ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        ax.plot(wa,fl,color='black',lw=0.2)
        ax.plot(wa,er,color='cyan',lw=0.2)
        ax.axhline(y=1, color='red', lw=0.2)
        ax.axhline(y=0, color='red', lw=0.2)
        if i<len(self.qsolist)-1:
            plt.setp(ax.get_xticklabels(), visible=False)
    savefig(qsoname+'.pdf')
    
def rest():
    '''
    Plot spectra on top of each other in restframe wavelength (redshift needed!).
    QSpec rest J000345-232355.dat:2.280:1100 J012403+004431.dat:3.83408:600
    '''
    alist = np.empty((0,3))
    for i in range (len(self.qsolist)):
        if len(self.qsolist[i].split(':'))==3:
            alist = np.vstack([alist,[self.qsolist[i].split(':')[0],
                                      self.qsolist[i].split(':')[1],
                                      self.qsolist[i].split(':')[2]]])
        elif len(self.qsolist[i].split(':'))==2:
            alist = np.vstack([alist,[self.qsolist[i].split(':')[0],
                                      self.qsolist[i].split(':')[1],1]])
        else:
            alist = np.vstack([alist,[self.qsolist[i].split(':')[0],1,1]])
    data.plotrest(alist)
    fig = figure(figsize=(50,10*(len(self.qsolist))))
    subplots_adjust(left=0.03, right=0.97, bottom=0.08, top=0.95, hspace=0, wspace=0.05)
    for i in range (0,len(self.qsolist)):
        spectrum = self.qsolist[i,0]
        maxflux  = float(self.qsolist[i,2])
        qsoname  = spectrum.split('/')[-1].split('.')[0]
        datatype = spectrum.split('/')[-1].split('.')[-1]
        self.get_data(spectrum)
        zem      = float(self.qsolist[i,1]) if z==0 else z
        print qsoname
        ax  = fig.add_subplot(len(self.qsolist),1,i+1,xlim=[950,1300],ylim=[0,1])
        ax.yaxis.set_major_locator(NullLocator())
        if (i!=len(self.qsolist)-1):
            ax.xaxis.set_major_locator(NullLocator())
        else:
            xlabel("Emitted wavelength in $\AA$")
        plot(wa/(zem+1),fl/maxflux,color='black',lw=0.2)
        text(1050,0.8,qsoname+'     $z_{em}$='+str(zem),color='blue')
    savefig('restframespec.pdf')
    
def normascii():
    '''
    Create normalised ASCII spectra using continuum fourth column
    '''
    self.qsolist = np.loadtxt(sys.argv[2][1:],dtype='string',comments='!') if sys.argv[2][0]==':' else [sys.argv[2]]
    qso = read()
    for j in range(0,len(self.qsolist)):
        table = np.loadtxt(self.qsolist[j])
        norm  = open('norm_'+self.qsolist[j],'w')
        for i in range(0,len(table)):
            norm.write(str(table[i,0])+'\t'+str(table[i,1]/table[i,3])+'\t'+str(table[i,2]/table[i,3])+'\n')
        norm.close()
    
def dat2fits():
    '''
    Create FITS file from ASCII data format
    '''
    self.qsolist = np.loadtxt(sys.argv[2],dtype='string',comments='!')
    name  = sys.argv[2].split('.')[0]
    data  = np.loadtxt(sys.argv[2])
    wave  = data[:,0].T
    col   = fits.Column(name='wavelength', format='E', array=wave)
    cols  = fits.ColDefs([col])
    tbhdu = fits.new_table(cols)
    hdu   = fits.PrimaryHDU()
    hdu.data = wave
    hdu.writeto(name+'.wav.fits',clobber=True)
    flux  = data[:,1].T#/data[:,2].T
    col   = fits.Column(name='flux', format='E', array=flux)
    cols  = fits.ColDefs([col])
    tbhdu = fits.new_table(cols)
    hdu = fits.PrimaryHDU()
    hdu.data = flux
    hdu.writeto(name+'.fits',clobber=True)
    error = data[:,2].T#/data[:,3].T
    col   = fits.Column(name='error', format='E', array=error)
    cols  = fits.ColDefs([col])
    tbhdu = fits.new_table(cols)
    hdu = fits.PrimaryHDU()
    hdu.data = error
    hdu.writeto(name+'.sig.fits',clobber=True)
    #cont  = np.array([1 for j in range (len(data))]).T
    #col   = fits.Column(name='continuum', format='E', array=cont)
    #cols  = fits.ColDefs([col])
    #tbhdu = fits.new_table(cols)
    #hdu = fits.PrimaryHDU()
    #hdu.data = cont
    #hdu.writeto(name+'.cont.fits',clobber=True)

def fits2dat():
    '''
    Create ASCII file from FITS data format
    '''
    self.qsolist = np.loadtxt(sys.argv[2][1:],dtype='string',comments='!') if sys.argv[2][0]==':' else [sys.argv[2]]
    for j in range(0,len(self.qsolist)):
        specfile = self.qsolist[j]
        if os.path.exists(specfile.replace('fits','sig.fits'))==False:
            spectrum   = specfile
            qsoname    = spectrum.split('/')[-1].split('.')[0]
            datatype   = spectrum.split('/')[-1].split('.')[-1]
            self.get_data(spectrum)
            out = open(specfile.split('/')[-1].replace('fits','dat'),'w')
            for i in range (0,len(self.fl)):
                wave  = '%.20f'%self.wa[i]
                flux  = '%.20f'%self.fl[i]
                error = '%.20f'%self.er[i]
                pixel = "{wave:>30}{flux:>30}{error:>30}".format(wave=wave,flux=flux,error=error)
                out.write(pixel+'\n')
            out.close()
        else:
            fh = fits.open(specfile)
            hd = fh[0].header
            d  = fh[0].data
            wa = hd['CRVAL1'] + (hd['CRPIX1'] - 1 + np.arange(hd['NAXIS1']))*hd['CDELT1']
            fl = d[:]
            specfile = specfile.replace('fits','sig.fits')
            fh = fits.open(specfile)
            hd = fh[0].header
            d  = fh[0].data
            er = d[:]
            out = open(specfile.split('/')[-1].replace('sig.fits','dat'),'w')
            for i in range (0,len(fl)):
                wave  = '%.7f'%wa[i]
                flux  = '%.7E'%fl[i]
                error = '%.7E'%er[i]
                pixel = "{wave:>15}{flux:>20}{error:>20}".format(wave=wave,flux=flux,error=error)
                out.write(pixel+'\n')
            out.close()

def kodiaq():
    '''
    Convert multi-1D spectra of KODIAQ sample into on single ASCII file
    '''
    quasars = []
    for spectrum in self.qsolist:
        if ':' in spectrum:
            print spectrum
            qsoname  = spectrum.split('/')[1]
            namelist = ['SDSSJ155814'] if qsoname=='J155814+405337' else [qsoname+'A',qsoname+'B'] if qsoname=='J014516-094517' else [qsoname]
            for qsoname in namelist:
                wa,fl,er,cont,sky,z = self.get_data(spectrum.replace(':','/')+qsoname+'_f.fits')
                ncall = 0 if qsoname not in quasars else len(np.where(np.array(quasars)==qsoname)[0])
                filename = qsoname+'_%1.f'%ncall if ncall!=0 else qsoname
                out = open(filename+'.dat','w')
                for i in range (0,len(fl)):
                    wave  = '%.7f'%wa[i]
                    flux  = '%.7E'%fl[i]
                    error = '%.7E'%er[i]
                    pixel = "{wave:>15}{flux:>20}{error:>20}".format(wave=wave,flux=flux,error=error)
                    out.write(pixel+'\n')
                out.close()
                quasars.append(qsoname)

def powerlaw():
    '''
    Create power law normalised spectrum and plot result
    '''
    def func(x,a,b,c):
        return a + b*x + c*x*x
    for i in range (0,len(self.qsolist)):
        spectrum   = self.qsolist[i]
        qsoname    = spectrum.split('/')[-1].split('.')[0]
        datatype   = spectrum.split('/')[-1].split('.')[-1]
        wa,fl,er,cont,sky,z = self.get_data(spectrum)
        print qsoname
        # Perform power law continuum fitting and save newly normalised spectrum
        spec_log = np.empty((0,2))
        for i in range(0, len(emfreereg)):
            istart = abs(wa-(1+z)*emfreereg[i][0]).argmin()
            iend   = abs(wa-(1+z)*emfreereg[i][1]).argmin()
            for j in range(istart,iend):
                spec_log = np.vstack([spec_log,[math.log10(wa[j]),math.log10(abs(fl[j]))]])
        coeff = optimize.curve_fit(func, spec_log[:,0], spec_log[:,1])[0]
        co = []
        for i in range(0,len(wa)):
            (co).append(10**(func(math.log10(wa[i]), coeff[0], coeff[1], coeff[2])))
        out = open(qsoname+'.dat','w')
        for i in range (0,len(fl)):
            wave  = str(wa[i]).split('.') if '.' in str(wa[i]) else str(wa[i]).replace('e','.e')
            flux  = str(fl[i]/co[i]).split('.') if '.' in str(fl[i]/co[i]) else str(fl[i]/co[i]).replace('e','.e')
            error = str(er[i]/co[i]).split('.') if '.' in str(er[i]/co[i]) else str(er[i]/co[i]).replace('e','.e')
            pixel = "{wave[0]:>4}.{wave[1]:<20} {flux[0]:>4}.{flux[1]:<20} {error[0]:>4}.{error[1]:<20}".format(wave=wave,flux=flux,error=error)
            out.write(pixel+'\n')
        out.close()
        ''' Plot initial spectrum with power law continuum '''
        fig = figure(figsize=(8,10))
        subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.96, wspace=0, hspace=0)
        f, (ax1, ax2) = plt.subplots(2, sharex=True)
        for i in range (len(emfreereg)):
            ax1.axvspan((1.0 + z)*emfreereg[i][0], (1.0 + z)*emfreereg[i][1],facecolor='b',alpha=0.3,lw=0)
        ax1.set_title(qsoname,fontsize=7)
        ax1.plot(wa,fl,color='black',lw=0.1,zorder=1)
        ax1.plot(wa,co,color='red',lw=1,zorder=2)
        ax1.set_xlim([wa[0],wa[-1]])
        ax1.set_ylim([-.5,sorted(fl)[int(0.98*len(fl))]])
        ax2.plot(wa,fl/co,color='blue',lw=0.1,zorder=1)
        co = [1 for x in fl]
        ax2.plot(wa,co,color='red',lw=1,zorder=2)
        ax2.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        ax2.axhline(y=1,color='grey',ls='dotted')
        ax2.axhline(y=0,color='grey',ls='dotted')
        ax2.set_xlim([wa[0],wa[-1]])
        ax2.set_ylim([-.5,1.5])
        f.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        savefig(qsoname+'.pdf')
            
def absfreq():
    '''
    Plots Lyman frequency for saturated pixels
    '''
    wa,fl,er,cont,sky,z = self.get_data(sys.argv[2])
    irange = 8
    freq = []
    for i in range (len(wa)-irange,irange,-1):
        medianleft    = sorted(fl[i-irange:i])[int(len(fl[i-irange:i])/2)]
        medianlefter  = sorted(er[i-irange:i])[int(len(er[i-irange:i])/2)]
        medianright   = sorted(fl[i:i+irange])[int(len(fl[i:i+irange])/2)]
        medianrighter = sorted(er[i:i+irange])[int(len(er[i:i+irange])/2)]
        if i==0 or np.average(er[i-irange:i+irange])>0.2:
            freq.append(0)
            print i,wa[i],0
        elif (medianleft/medianlefter < 4):
            freq.append(1)
            print i,wa[i],1
        else:
            freq.append(0)
            print i,wa[i],0
    fig = figure(figsize=(8,11))
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0.2, wspace=0)
    ax1 = plt.subplot(211,xlim=[4200,5000],ylim=[-0.1,1.2])
    ax1.plot(wa,fl)
    ax1.plot(wa,er,color='red')
    ax1.axhline(y=0,ls='dotted',color='black')
    ax2 = plt.subplot(212,xlim=[4200,5000],ylim=[-0.1,1.2])
    ax2.plot(wa[irange:-irange],freq)
    ax1.axhline(y=0,ls='dotted',color='black')
    show()

def ebce():
    '''
    Error based continuum estimator
    '''
    rc('xtick', labelsize=10)
    rc('ytick', labelsize=10)

    dvbin1  = 600  #km/s
    dvbin2  = 10*dvbin1  #km/s
    
    wa,fl,er,cont,sky,z = self.get_data(sys.argv[2])
    spec = np.vstack((np.array(wa),np.array(fl),np.array(er))).T
    
    fig = figure()
    ax = fig.add_subplot(111,ylim=[-0.5,sorted(fl)[len(fl)-10]])
    
    plot(wa,fl,drawstyle='steps',color='0.8',lw=1,zorder=1)
    plot(wa,er,drawstyle='steps',color='cyan',lw=1,zorder=2)

    for dvbin in [dvbin1,dvbin2]:
    
        cont  = np.empty((0,2))
        imin  = 0
        wmin  = wa[imin]
        last  = wa[-1] * (2*self.c-dvbin) / (2*self.c+dvbin)
        i     = 0
        while wa[i] < last:
            wmax  = wmin * (2*self.c+dvbin) / (2*self.c-dvbin)
            imax  = abs(wa-wmax).argmin()
            cent  = (wa[imin]+wa[imax])/2.
            meder = sorted(er[imin:imax])[0] if dvbin==dvbin1 else np.median(co[imin:imax])
            cont  = np.vstack((cont,[cent,meder]))
            imin  = imax
            wmin  = wa[imin]
            i     = imax

        color = 'lime' if dvbin==dvbin1 else 'red'
        f = interp1d(cont[:,0],cont[:,1],kind='cubic')
        imin = abs(wa-cont[0,0]).argmin()
        imax = abs(wa-cont[-1,0]).argmin()
        plot(wa[imin+1:imax-1],2*f(wa[imin+1:imax-1]),color=color,lw=1)
        wa,co = wa[imin+1:imax-1],f(wa[imin+1:imax-1])

    ax.axhline(y=0, color='red', lw=0.2)
    ax.axhline(y=0.2, color='orange', lw=0.2)
    show()

def example():
    '''
    Create spectrum plot for website presentation
    '''
    rc('font', size=2)
    rc('axes', labelsize=8, linewidth=0)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=6)
    rc('ytick', labelsize=6)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    fig = figure(figsize=(50,3))
    subplots_adjust(left=0.02, right=0.99, bottom=0.07, top=0.96, hspace=0, wspace=0.05)
    ax = subplot(111,ylim=[-0.1,1.1])
    
    fh = fits.open(sys.argv[2])
    d = fh[0].data
    d.shape
    hd = fh[0].header
    wa = 10**(hd['CRVAL1'] + (hd['CRPIX1'] - 1 + np.arange(hd['NAXIS1']))*hd['CDELT1'])
    fl = d[0,:]
    
    ibeg = abs(wa - 3500).argmin()
    iend = abs(wa - 5500).argmin()
    
    plot(wa[ibeg:iend],fl[ibeg:iend],'black',lw=1)
    xlabel('Wavelength')
    ylabel('Normalised Flux')
    ax.axhline(y=1, color='red', lw=0.2)
    ax.axhline(y=0, color='red', lw=0.2)
    savefig(sys.argv[2].split('.')[0]+'.jpg')

def whole():
    '''
    Plot the whole spectrum and save as PDF
    '''
    for j in range(len(self.qsolist)):

        rc('font', size=10, family='serif')
        rc('axes', labelsize=10, linewidth=0.2)
        rc('legend', fontsize=10, handlelength=10)
        rc('xtick', labelsize=10)
        rc('ytick', labelsize=10)
        rc('lines', lw=0.2, mew=0.2)
        rc('grid', linewidth=0.2)
        
        spectrum = self.qsolist[j]
        print spectrum
        qsoname  = spectrum.split('/')[-1].split('.')[0]
        datatype = spectrum.split('/')[-1].split('.')[-1]
        self.get_data(spectrum)

        Nrows = 9

        fig = figure(figsize=(20,30))
        axis('off')
        title(spectrum+'\n',fontsize=15)
        subplots_adjust(left=0.04, right=0.96, bottom=0.04, top=0.96, hspace=.2, wspace=0.05)

        ''' Plot whole spectrum '''

        wmin,wmax   = self.wa[0],self.wa[-1]
        ymin,ymax   =  -0.5,1.5
        #ymin1,ymax1 = -1,sorted(fl)[int(0.99*len(fl))]+0.5
        #ymin2,ymax2 = -1,max(fl/er)

        ax = fig.add_subplot(Nrows,1,1)
        ax.plot(self.wa,self.fl,'black',lw=0.1)
        ax.plot(self.wa,self.er,'cyan',lw=0.1)
        ax.set_xlim([wmin,wmax])
        ax.set_ylim([-1,2])
        ax.text(self.wa[0]+0.8*(self.wa[-1]-self.wa[0]),0.8*ymax,'Whole spectrum',weight='bold',size=20,color='blue')
        ax.set_ylabel('Flux')
        ax.axhline(y=0,ls='dotted')
        ax.axhline(y=1,ls='dotted')

        if '--snr' in sys.argv:
            ax = ax.twinx()
            ax.plot(self.wa,self.fl/self.er,color='red',lw=0.1)
            ax.set_xlim([wmin,wmax])
            ax.set_ylim([ymin2,ymax2])
            ax.set_ylabel('Signal-to-noise')

        ''' Plot separate range of the spectrum '''

        waveint = (self.wa[-1]-self.wa[0])/(Nrows-1)

        istart  = 0
        wmin    = self.wa[istart]
        wmax    = self.wa[istart] + waveint
        iend    = abs(self.wa - wmax).argmin()

        for i in range(2,Nrows+1):

            ax = fig.add_subplot(Nrows,1,i)
            y1 = self.fl[istart:iend]
            #ymax1 = sorted(y1)[int(0.99*len(y1))]
            #ymax1 = sorted(y1)[int(0.99*len(y1))]
            ax.plot(self.wa[istart:iend],self.fl[istart:iend],'black',lw=0.1)
            ax.plot(self.wa[istart:iend],self.er[istart:iend],'cyan',lw=0.1)
            ax.set_xlim([wmin,wmax])
            ax.set_ylim([ymin,ymax])
            ax.set_ylabel('Flux')
            ax.axhline(y=0,color='red',ls='dashed',lw=3)
            ax.axhline(y=1,color='red',ls='dashed',lw=3)

            if '--snr' in sys.argv:
                ax = ax.twinx()
                ax.plot(self.wa[istart:iend],self.fl[istart:iend]/self.er[istart:iend],color='lime',lw=0.1)
                ax.set_xlim([wmin,wmax])
                ax.set_ylim([ymin2,ymax2])
                ax.set_ylabel('Signal-to-noise')

            istart = iend
            wmin   = wmax
            wmax   = wmin + waveint
            iend   = abs(self.wa - wmax).argmin()
        plt.savefig(qsoname+'.pdf')
        
def fitsmodif():
    '''
    Modify flux value in FITS file if equal to -1
    '''
    hdulist = fits.open(sys.argv[2])
    tbdata  = hdulist[1].data

class Normalise:
    '''
    Quick & Dirty manual normalisation using spline interpolation.
    '''
    def __init__(self):
        rc('font', size=5, family='serif')
        rc('axes', labelsize=10, linewidth=0.2)
        rc('legend', fontsize=10, handlelength=10)
        rc('xtick', labelsize=10)
        rc('ytick', labelsize=10)
        rc('lines', lw=0.2, mew=0.2)
        rc('grid', linewidth=0.2)
        self.c = 299792.458    
        self.wasep = 30
        self.z = 0
        self.qsoname = sys.argv[2].split('/')[-1].split('.')[0]
        argcheck()
        process()
    
    def press(self,event):
    
        if event.key==' ':
            fitcont(event)
            self.fig.canvas.draw()
        if event.key=='s':
            print '|- Points and normalised spectrum saved!'
            outpts = open(self.qsoname+'_pts.dat','w')
            for i in range (len(self.points)):
                wave  = '%.7f'%self.points[i,0]
                flux  = '%.7E'%self.points[i,1]
                pixel = "{wave:>15}{flux:>20}".format(wave=wave,flux=flux)
                outpts.write(pixel+'\n')
            outpts.close()
            outspec = open(self.qsoname+'_norm.dat','w')
            for i in range (len(self.wa)):
                wave  = '%.7f'%self.wa[i]
                flux  = '%.7E'%(self.fl[i]/self.co[i])
                error = '%.7E'%(self.er[i]/self.co[i])
                pixel = "{wave:>15}{flux:>20}{error:>20}".format(wave=wave,flux=flux,error=error)
                outspec.write(pixel+'\n')
            outspec.close()
        if event.key=='q':
            quit()
            
    def argcheck(self):
        
        argument = np.array(sys.argv, dtype='str')
        if len(argument)<2:
            print 'Please enter a spectrum file.'
            quit()
        else:
            self.readspectrum(argument[2])
            self.co = [1 for x in self.fl]
            if '--list' in argument:
                i = np.where(argument=='--list')[0][0]
                self.points = np.loadtxt(argument[i+1],dtype='float')
            else:
                delta = int((self.wa[-1]-self.wa[0])/self.wasep)
                self.points = np.array([[self.wa[0]+i*self.wasep,0] for i in range(delta+1)])
                self.points = np.vstack((self.points,[self.wa[-1],0.0000001]))
        
    def readspectrum(self,spectrum):
        
        datatype = spectrum.split('.')[-1]
        if datatype=='fits':
            hdu = fits.open(spectrum)
            for i in range (len(hdu[0].header)):
                if ('UVES' or 'POPLER') in str(hdu[0].header[i]):
                    specformat = 'UVES'
                elif ('Keck' or 'HIRES') in str(hdu[0].header[i]):
                    specformat = 'HIRES'
                elif 'SDSS' in str(hdu[0].header[i]):
                    specformat = 'SDSS'
            if specformat=='HIRES':
                hd = hdu[0].header
                self.wa = hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+np.arange(hd['NAXIS1']))
                if len(fh[0].data.shape)==1:
                    fl  = hdu[0].data[:]
                    hdu = fits.open(spectrum.replace('fits','sig.fits'))
                    self.er = hdu[0].data[:]
                else:
                    self.fl = d[0,:]
                    self.er = d[1,:]
            elif specformat=='UVES':
                hd  = hdu[0].header
                self.wa = 10**(hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+np.arange(hd['NAXIS1'])))
                self.fl = hdu[0].data[0,:]
                self.er = hdu[0].data[1,:]
            elif specformat=='SDSS':
                hdu0 = hdu[0].header
                hdu1 = hdu[1].header
                self.z  = float(hdu[2].data['Z'])
                self.wa = 10.**(hdu0['coeff0'] + hdu0['coeff1'] * np.arange(hdu1['naxis2']))
                self.fl = hdu[1].data['flux']
                self.er = hdu[1].data['ivar']
        else:
            d  = np.loadtxt(spectrum,dtype='float')
            self.wa = d[:,0]
            self.fl = d[:,1]
            self.er = d[:,2]
    
        self.wa = [round(i,7) for i in self.wa]
        self.fl = [round(i,7) for i in self.fl]
        self.er = [round(i,7) for i in self.er]
            
    def process(self):
    
        self.co = interp1d(self.points[:,0],self.points[:,1],kind='cubic')(self.wa)
        self.fig = figure()
        subplots_adjust(left=0.05, right=0.95, bottom=0.02, top=0.95, hspace=0.2, wspace=0)
    
        ymax = sorted(self.fl)[int(0.98*len(self.fl))]
        
        ax1 = plt.subplot2grid((4,1), (0, 0), rowspan=3)
        ax1.set_xlim(self.wa[0],self.wa[-1])
        ax1.set_ylim(-0.5,ymax)
        ax1.plot(self.wa,self.fl,color='black',lw=0.3,zorder=2)
        ax1.axhline(y=0,color='grey',ls='dashed',zorder=2,lw=2,alpha=0.7)
        self.cont1  = ax1.scatter(self.points[:,0],self.points[:,1],marker='x',color='red',zorder=4)
        self.cont2, = ax1.plot(self.wa,self.co,color='red',lw=1,zorder=3)
        self.ax1 = ax1
    
        ax2 = plt.subplot2grid((4,1), (3, 0),sharex=ax1)
        ax2.set_xlim(self.wa[0],self.wa[-1])
        ax2.set_ylim(-0.3,1.3)
        self.norm, = ax2.plot(self.wa,self.fl/self.co,color='black',lw=0.3,zorder=1)
        ax2.axhline(y=0,color='grey',ls='dashed',zorder=2,lw=2,alpha=0.7)
        ax2.axhline(y=1,color='grey',ls='dashed',zorder=2,lw=2,alpha=0.7)
        self.ax2 = ax2
        
        self.fig.canvas.mpl_connect('key_press_event', press)
        show()
    
    def fitcont(self,event):
    
        i = abs(self.points[:,0]-event.xdata).argmin()
        x = self.wa[0] if i==0 else self.wa[-1] if i==len(self.points)-1 else event.xdata
        self.points[i] = [x,event.ydata]
        self.co = interp1d(self.points[:,0],self.points[:,1],kind='cubic')(self.wa)
        self.cont1.remove()
        self.cont1 = self.ax1.scatter(self.points[:,0],self.points[:,1],marker='x',color='red',zorder=4)
        self.cont2.remove()
        self.cont2, = self.ax1.plot(self.wa,self.co,color='red',lw=1,zorder=3)
        self.norm.remove()
        self.norm, = self.ax2.plot(self.wa,self.fl/self.co,color='black',lw=0.3,zorder=1)
