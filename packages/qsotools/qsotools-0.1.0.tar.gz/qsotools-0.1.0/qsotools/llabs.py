import quasar

def noise():
    '''
    Plot blue end spectral noise for paper purpose
    '''
    fig = figure(figsize=(12,8))
    subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.97, hspace=0.12, wspace=0)
    ax = subplot(311,xlim=[4570,4900],ylim=[-0.1,2])
    readspec('/Users/vincent/ASTRO/data/UVES/reduced/J033413-161205.fits')
    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    ax.plot(setup.wa,setup.fl,color='black',lw=0.1)
    ax.plot(setup.wa,setup.er,color='cyan',lw=0.1)
    ylabel('Flux',fontsize=12)
    ax = subplot(312,xlim=[3040,3500],ylim=[-0.1,2])
    readspec('/Users/vincent/ASTRO/data/UVES/reduced/J021857+081727.fits')
    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    ax.plot(setup.wa,setup.fl,color='black',lw=0.1)
    ax.plot(setup.wa,setup.er,color='cyan',lw=0.1)
    ylabel('Flux',fontsize=12)
    ax = subplot(313,xlim=[3270,3900],ylim=[-0.1,2])
    readspec('/Users/vincent/ASTRO/data/UVES/reduced/J162116-004250.fits')
    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    ax.plot(setup.wa,setup.fl,color='black',lw=0.1)
    ax.plot(setup.wa,setup.er,color='cyan',lw=0.1)
    ylabel('Flux',fontsize=12)
    xlabel(r'Wavelength ($\mathrm{\AA}$)',fontsize=12)
    savefig('test.pdf')

def twospecs():
    '''
    Comparison plot between 2 simulated spectra with
    different DLA velocity structure in them.
    '''
    rc('font', size=10, family='sans-serif')
    rc('axes', labelsize=20, linewidth=0.2)
    rc('legend', fontsize=20, handlelength=10)
    rc('xtick', labelsize=20)
    rc('ytick', labelsize=20)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    spec1 = numpy.loadtxt(setup.datapath+'J115411+063426.dat')
    spec2 = numpy.loadtxt(setup.datapath+'J220852-194359.dat')
    fig = figure(figsize=(12,8))
    subplots_adjust(left=0.05, right=0.95, bottom=0.01, top=0.93, hspace=0, wspace=0.05)
    ax = subplot(611,xlim=[2560,3700],ylim=[-0.1,1.2])
    ax.plot(spec1[:,0],spec1[:,1],color='green')
    ax.plot(spec2[:,0],spec2[:,1],color='red')
    ax = subplot(613,xlim=[2600,2800],ylim=[-0.1,1.2])
    #ax.plot(spec1[:,0],spec1[:,1],color='green')
    ax.plot(spec2[:,0],spec2[:,1],color='red')
    #ax = subplot(611,xlim=[-6000,6000],ylim=[-0.1,1.2])
    #ax.plot(spec1[:,0],spec1[:,1],color='green')
    #ax.plot(spec2[:,0],spec2[:,1],color='red')
    savefig('test.pdf')

def overlaps():
    '''
    Checking for overlap DLA between samples
    '''
    print 'ID                     SDSS      zabs            high-res      inst'
    print '-------------------------------------------------------------------'
    a=numpy.loadtxt('./zlist.dat',dtype=str)
    t=numpy.loadtxt('./crosscheck.dat',dtype=str)
    k=1
    for i in range(len(a)):
        sdss = a[i,0]+'.fits'
        if sdss in t[:,3]:
            j = numpy.where(t[:,3]==a[i,0]+'.fits')[0][0]
            highres = t[j,0]+'.fits'
            cond1 = os.path.exists('/Users/vincent/ASTRO/data/SDSS/DR10_dla/'+sdss)
            cond2 = os.path.exists('/Users/vincent/ASTRO/data/UVES/finished/'+highres)
            cond3 = os.path.exists('/Users/vincent/ASTRO/data/HIRES/finished/'+highres)
            inst  = 'UVES+HIRES' if cond2==cond3==True else ''
            inst  = 'UVES' if cond2==True and cond3==False else inst
            inst  = 'HIRES' if cond2==False and cond3==True else inst
            if inst!='':
                print '{0:>2}{1:>25}{2:>10}{3:>20}{4:>10}'.format(k,a[i,0],a[i,1],t[j,0],inst)
                k+=1

def limit():
    '''
    Overplot of Lyman-limit from different DLA systems
    '''
    vsig  = 1.5
    disp  = 0.01
    wave  = np.arange(900,1300,disp)
    wamid = setup.HI[-1]['wave']
    vel   = 2*(wave-wamid)/(wave+wamid)*setup.c
    fig   = figure(figsize=(8,5))
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0, wspace=0.1)
    for N in [17.,20.,23.]:
        model = 1
        for i in range(len(setup.HI)-1):
            lam   = setup.HI[i]['wave']
            osc   = setup.HI[i]['strength']
            gam   = setup.HI[i]['gamma']
            model *= voigt_model(N,10.,wave,lam,gam,osc)
        #model = gaussian_filter1d(model,vsig/disp)
        ax    = subplot(111,xlim=[-100,5000],ylim=[-0.2,1.2])
        plot(vel,model,lw=2,alpha=0.7)
    savefig('limits.pdf')
    clf()
        
def sysrecov():

    datapath = '/Users/vincent/ASTRO/data/UVES/reduced/'

    met1 = [{'ID':'SiIV1393' ,'Metalline':'SiIV', 'Metalwave':1393.76000},
            {'ID':'SiIV1402' ,'Metalline':'SiIV', 'Metalwave':1402.77000},
            {'ID':'CII1334'  ,'Metalline':'CII',  'Metalwave':1334.53000}]
    
    spectra  = np.array([['J193957-100241.fits',3.5722, 338.13, 36.14,-100, 500, -50, 50,met1],
                         ['J042214-384452.fits',3.0870,1737.44,244.90,-400,3000,-200,200,met1],
                         ['J091613+070224.fits',2.6194,1738.08,231.17,-400,3000,-200,200,met1],
                         ['J040718-441013.fits',2.6220,1899.09,253.21,-400,3000,-200,200,met1]])
    
    fig = figure(figsize=(8,10))
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0, wspace=0.1)
    for i in range(len(spectra)):
        print spectra[i,0]
        metallist = spectra[i,-1]
        nrows = len(setup.HI)#+len(metallist)+1
        readspec(datapath+spectra[i,0])
        for j in range(len(setup.HI)):
            vmin,vmax = spectra[i,4],spectra[i,5]
            wamid = setup.HI[j]['wave']*(1+float(spectra[i,1]))
            wabeg = wamid*(1+vmin/setup.c)
            waend = wamid*(1+vmax/setup.c)
            ibeg  = abs(setup.wa-wabeg).argmin()
            iend  = abs(setup.wa-waend).argmin()
            v     = setup.c*((setup.wa-wamid)/wamid)
            ax    = subplot(nrows,4,i+1+4*j,xlim=[vmin,vmax],ylim=[-0.5,1.5])
            plot(v[ibeg:iend],setup.fl[ibeg:iend],color='black')
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
            ax.axvspan(-float(spectra[i,3])/2,float(spectra[i,3])/2,color='red',alpha=0.1)
            ax.axvline(0,color='red',lw=1,alpha=0.5,zorder=3)
            if i>0: ax.xaxis.set_major_locator(plt.FixedLocator([0,1000,2000]))
            else: ax.xaxis.set_major_locator(plt.FixedLocator([0,200,400]))
            if j==0: ax.set_title(spectra[i,0].split('.')[0]+'\n'+str(spectra[i,2])+' km/s',fontsize=10)
                #text((vmin+vmax)/2,0.5,,fontsize=12,weight='bold',ha='center',color='orange',
                #                              bbox=dict(facecolor='0.95',lw=.2,color='white',alpha=0.4))
            if j<len(setup.HI)-1: plt.setp(ax.get_xticklabels(), visible=False)
            else:
                ax.axvline(float(spectra[i,2]),color='orange',lw=2,alpha=0.8,zorder=3)
                ax.annotate("",xy=(float(spectra[i,2]),0.3),xytext=(0,0.3),arrowprops=dict(fc="orange",ec="none",lw=2,alpha=0.7))
            plt.setp(ax.get_yticklabels(), visible=False)
        #for j in range(len(metallist)):
        #    vmin,vmax = spectra[i,6],spectra[i,7]
        #    wamid = metallist[j]['Metalwave']*(1+float(spectra[i,1]))
        #    wabeg = wamid*(1+vmin/setup.c)
        #    waend = wamid*(1+vmax/setup.c)
        #    ibeg  = abs(setup.wa-wabeg).argmin()
        #    iend  = abs(setup.wa-waend).argmin()
        #    v     = setup.c*((setup.wa-wamid)/wamid)
        #    ax    = subplot(nrows,4,4+4*len(setup.HI)+i+1+4*j,xlim=[vmin,vmax],ylim=[-0.5,1.5])
        #    plot(v[ibeg:iend],setup.fl[ibeg:iend],color='black')
        #    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        #    ax.axvline(0,color='red',lw=1,alpha=0.5,zorder=3)
        #    ax.axvspan(-float(spectra[i,3])/2,float(spectra[i,3])/2,color='red',alpha=0.1)
        #    if j<32: plt.setp(ax.get_xticklabels(), visible=False)
        #    else: ax.xaxis.set_major_locator(plt.FixedLocator([-150,-50,0,50,150]))
        #    plt.setp(ax.get_yticklabels(), visible=False)
    fig.text(0.02, 0.5, 'Normalized Flux', va='center', rotation='vertical',fontsize=10)
    fig.text(0.5, 0.01, 'Velocity relative to central redshift (km/s)', ha='center',fontsize=10)
    savefig('sysrecov.pdf')
    clf()

def llfind():
    '''
    Search test for observed Lyman-limit. Different
    criteria can be tested. The most successful one will
    be implemented in the LLabs code.
    '''
    fig = figure(1,figsize=(20,6))
    plt.subplots_adjust(left=0.04, right=0.95, bottom=0.1, top=0.87, hspace=.3, wspace=0.05)
    plt.axis('off')
    if setup.qso=='infile.dat':
        speclist = numpy.loadtxt(setup.qso,dtype='str',comments='!',ndmin=1)
    else:
        speclist = [setup.qso]
    for idx in range(len(speclist)):
        spectrum   = speclist[idx]
        instrument = spectrum.split('/')[-3].lower()
        qsoname    = re.split(r'[/.]',spectrum)[-2]
        readspec(spectrum)
        wa,fl,er = setup.wa,setup.fl,setup.er
        # Creating median, average, and variance arrays
        bin  = 500
        step = 500
        i    = abs(wa - (wa[0]*(1.+bin/2/setup.c))).argmin()
        iend = abs(wa - (wa[-1]*(1.-bin/2/setup.c))).argmin()
        wave = []
        medflx,mederr,medsnr = [],[],[]
        avgflx,avgerr,avgsnr = [],[],[]
        varflx,varerr,varsnr = [],[],[]
        while i<iend:
            wave.append(wa[i])
            ibeg = abs(wa - (wa[i]*(1.-bin/2/setup.c))).argmin()+1
            ifin = abs(wa - (wa[i]*(1.+bin/2/setup.c))).argmin()-1
            medflx.append(numpy.median(fl[ibeg:ifin]))
            mederr.append(numpy.median(er[ibeg:ifin]))
            medsnr.append(numpy.median(fl[ibeg:ifin]/er[ibeg:ifin]))
            avgflx.append(numpy.average(fl[ibeg:ifin]))
            avgerr.append(numpy.average(er[ibeg:ifin]))
            avgsnr.append(numpy.average(fl[ibeg:ifin]/er[ibeg:ifin]))
            varflx.append(numpy.var(fl[ibeg:ifin]))
            varerr.append(numpy.var(er[ibeg:ifin]))
            varsnr.append(numpy.var(fl[ibeg:ifin]/er[ibeg:ifin]))
            i = abs(wa - (wa[i]*(1.+step/setup.c))).argmin()+1
        medspecerr = numpy.median(er)
        avgspecsnr = numpy.average(fl/er)
        medspecsnr = numpy.median(fl/er)
        varspecsnr = numpy.var(fl/er)
        #medflx = [abs(val) for val in medflx/max(medflx)]
        #mederr = [abs(val) for val in mederr/max(mederr)]
        #medsnr = [abs(val) for val in medsnr/max(medsnr)]
        #avgflx = [abs(val) for val in avgflx/max(avgflx)]
        #avgerr = [abs(val) for val in avgerr/max(avgerr)]
        #avgsnr = [abs(val) for val in avgsnr/max(avgsnr)]
        #varflx = [abs(val) for val in varflx/max(varflx)]
        #varerr = [abs(val) for val in varerr/max(varerr)]
        #varsnr = [abs(val) for val in varsnr/max(varsnr)]
        ''' Locate Lyman limit '''
        npix  = 6
        dv    = 100
        llpos = None
        for i in range(len(wave)):
            ''' First set of conditions '''
            #cond1 = numpy.average(medsnr[:i])         < 0.01
            #cond2 = numpy.average(medsnr[i-npix:i])   < 0.01
            #cond3 = numpy.average(medflx[i-npix:i])   < 0.05
            #cond4 = numpy.average(medsnr[i+1:i+npix]) > 0.03
            #cond5 = numpy.median(medflx[i:i+npix])    > 2*numpy.median(medflx[i-npix:i])
            #cond6 = numpy.median(varsnr[i:i+npix])    > 2*numpy.median(varsnr[i-npix:i])
            ''' New set of conditions '''
            cond1 = len(numpy.where(numpy.array(medflx[i:i+npix])/numpy.array(mederr[i:i+npix])>2)[0]) > 0.6*npix
            cond2 = len(numpy.where(numpy.array(medflx[i-npix:i])/numpy.array(mederr[i-npix:i])<2)[0]) > 0.6*npix
            #cond2 = len(numpy.where(numpy.array(medflx[:i])/numpy.array(mederr[:i])<2)[0]) > 0.6*i
            cond3 = len(numpy.where(numpy.array(mederr[i:i+npix])/medspecerr<2)[0]) > 0.6*npix
            cond4 = len(numpy.where(numpy.array(medflx[i-npix:i])<0.2)[0]) > 0.6*npix
            #cond4 = numpy.median(medflx[i:i+npix])    > 2*numpy.median(medflx[i-npix:i])
            #cond5 = numpy.median(varsnr[i:i+npix])    > 2*numpy.median(varsnr[i-npix:i])
            if cond1 and cond2 and cond3 and cond4:
                llpos = wave[i]
                i = abs(wa-wave[i]).argmin()
                for j in range(i,len(wa)):
                    jend = abs(wa - (wa[j]*(1.+dv/setup.c))).argmin()
                    if numpy.median(fl[j:jend])>3*numpy.median(er[j:jend]):
                        llpos = wa[j]
                        break
                break
        if llpos==None:
            print '{0:<15} - Average SNR:{1:>8} - No Lyman limit found'.format(qsoname,'%.4f'%numpy.average(fl/er))
        else:
            print '{0:<15} - Average SNR:{1:>8} - Limit found at {2:<10}'.format(qsoname,'%.4f'%numpy.average(fl/er),'%.4f'%llpos)
        # Plot flux
        curves,label = [],[]
        xmin = wa[0] if '--xmin' not in sys.argv else setup.xmin
        xmax = setup.xmax if '--xmax' in sys.argv else 2*llpos-wa[0] if llpos!=None else wa[-1]
        ymax = setup.ymax if '--ymax' in sys.argv else sorted(fl)[int(0.99*len(fl))]
        host = host_subplot(111, axes_class=AA.Axes)
        host.set_xlim(xmin,xmax)
        host.set_ylim(0,ymax)
        p, = host.plot(wa,fl,color='black',alpha=0.5,lw=1.5)
        host.plot(wa,er,color='cyan')
        host.set_xlabel('Wavelength')
        host.set_ylabel('Flux')
        host.set_title(spectrum+'\n\n',fontsize=10)
        host.yaxis.label.set_color(p.get_color())
        if llpos!=None:
            p = host.axvline(x=llpos,color='black',ls='dashed',lw=3)
            curves.append(p)
            label.append('Lyman Limit')
        # Plot median curves
        data = numpy.array([[medsnr,'Median SNR'    ,'blue' ,'solid' ],
                            [medflx,'Median Flux'   ,'blue' ,'dashed'],
                            [mederr,'Median Error'  ,'blue' ,'dotted'],
                            [avgsnr,'Average SNR'   ,'green','solid' ],
                            [avgflx,'Average Flux'  ,'green','dashed'],
                            [avgerr,'Average Error' ,'green','dotted'],
                            [varsnr,'Variance SNR'  ,'red'  ,'solid' ],
                            [varflx,'Variance Flux' ,'red'  ,'dashed'],
                            [varerr,'Variance Error','red'  ,'dotted']])
        for i in range(len(data)):
            ydata  = data[i,0]
            ylabel = data[i,1]
            ycolor = data[i,2]
            ystyle = data[i,3]
            ax     = host#.twinx()
            ax.set_xlim(xmin,xmax)
            ax.set_ylim(0,ymax)
            p, = ax.plot(wave,ydata,color=ycolor,marker='o',ms=3,alpha=0.8,lw=0.1,ls=ystyle,mew=0)
            #ax.get_yaxis().set_ticks([]) if i!=1 else None
            curves.append(p)
            label.append(data[i,1])
        p = ax.axhline(y=medspecerr,color='magenta',ls='dashed',lw=2)
        curves.append(p)
        label.append('Median Spectral SNR')
        #t = host.text(xmax-0.05*(xmax-xmin),0.90*ymax,'Median Spectral SNR: %.4f'%medspecsnr,fontsize=10,ha='right')
        #t.set_bbox(dict(color='white', alpha=0.7, edgecolor=None))
        ax.legend(curves,label,numpoints=2,handlelength=3,frameon=False,
                  prop={'size':8},loc='center',bbox_to_anchor=[0.5,1.04],ncol=len(data)+3)
        if llpos==None:
            if os.path.exists('./found/'+qsoname+'.pdf')==True:
                os.system('rm ./found/'+qsoname+'.pdf')
            os.system('mkdir -p ./notfound/')
            plt.savefig('./notfound/'+qsoname+'.pdf')
        else:
            if os.path.exists('./notfound/'+qsoname+'.pdf')==True:
                os.system('rm ./notfound/'+qsoname+'.pdf')
            os.system('mkdir -p ./found/')
            plt.savefig('./found/'+qsoname+'.pdf')
        if '.dat' in sys.argv[2]:
            os.system("sed -i '' 's,"+spectrum+",!"+spectrum+",' "+sys.argv[2])
        clf()
        #new_fixed_axis = ax.get_grid_helper().new_fixed_axis
        #ax.axis['right'] = new_fixed_axis(loc='right',axes=ax,offset=(60,0))
        #ax.axis['right'].toggle(all=True)
        #host.axis['right'].label.set_color(p.get_color())

def llfind_criteria1():
    '''
    Search for Lyman limit using first criteria
    '''
    setup.vbin = 500
    npix = 6
    dv   = 100
    i    = abs(setup.wa - (setup.wa[0]*(1.+setup.vbin/2/setup.c))).argmin()
    iend = abs(setup.wa - (setup.wa[-1]*(1.-setup.vbin/2/setup.c))).argmin()
    wave,medsnr,medflx,mederr,varsnr = [],[],[],[],[]
    medspecerr = np.median(setup.er)
    avgspecsnr = np.average(setup.fl/setup.er)
    medspecsnr = np.median(setup.fl/setup.er)
    varspecsnr = np.var(setup.fl/setup.er)
    while i<iend:
        wave.append(setup.wa[i])
        ibeg = abs(setup.wa - (setup.wa[i]*(1.-setup.vbin/2/setup.c))).argmin()+1
        ifin = abs(setup.wa - (setup.wa[i]*(1.+setup.vbin/2/setup.c))).argmin()-1
        medflx.append(np.median(setup.fl[ibeg:ifin]))
        mederr.append(np.median(setup.er[ibeg:ifin]))
        medsnr.append(np.median(setup.fl[ibeg:ifin]/setup.er[ibeg:ifin]))
        varsnr.append(np.var(setup.fl[ibeg:ifin]/setup.er[ibeg:ifin]))
        i = abs(setup.wa - (setup.wa[i]*(1.+setup.vbin/setup.c))).argmin()+1
    if wave!=[]:
        medflx = [abs(val/max(medflx)) for val in medflx]
        mederr = [abs(val/max(mederr)) for val in mederr]
        medsnr = [abs(val/max(medsnr)) for val in medsnr]
        varsnr = [abs(val/max(varsnr)) for val in varsnr]
    for j in range(len(wave)):
        if setup.criteria==1:
            cond1 = np.average(medsnr[:j])         < 0.01
            cond2 = np.average(medsnr[j-npix:j])   < 0.01
            cond3 = np.average(medflx[j-npix:j])   < 0.05
            cond4 = np.average(medsnr[j+1:j+npix]) > 0.03
            cond5 = np.median(medflx[j:j+npix])    > 2*np.median(medflx[j-npix:j])
            cond6 = np.median(varsnr[j:j+npix])    > 2*np.median(varsnr[j-npix:j])
            conds = cond1 and cond2 and cond3 and cond4 and cond5 and cond6
        if setup.criteria==2:
            cond1 = len(np.where(np.array(medflx[j:j+npix])/np.array(mederr[j:j+npix])>2)[0]) > 0.6*npix
            cond2 = len(np.where(np.array(medflx[j-npix:j])/np.array(mederr[j-npix:j])<2)[0]) > 0.6*npix
            cond3 = len(np.where(np.array(mederr[j:j+npix])/medspecerr<2)[0]) > 0.6*npix
            cond4 = len(np.where(np.array(medflx[j-npix:j])<0.2)[0]) > 0.6*npix
            conds = cond1 and cond2 and cond3 and cond4
        if conds==True:
            setup.ill  = abs(setup.wa-wave[j-1]).argmin()
            for i in range(setup.ill,len(setup.wa)):
                iend = abs(setup.wa - (setup.wa[i]*(1.+dv/setup.c))).argmin()
                if np.median(setup.fl[i:iend])>3*np.median(setup.er[i:iend]):
                    terminate(i)
                    break
            break

def llfind_criteria3():
    '''
    Search for Lyman limit using third criteria
    '''
    setup.npix = 20
    avgfl,avger,flag,limit = [],[],0,3
    i = istart + setup.npix
    while i<iend-20:
        flux   = setup.fl[i-setup.npix:i+setup.npix]
        error  = abs(setup.er[i-setup.npix:i+setup.npix])
        badpix = np.where(error>10000)[0]
        flux   = np.delete(flux,badpix,0)
        error  = np.delete(error,badpix,0)
        avgfl  = np.average(flux)
        avger  = np.average(error)
        if (avgfl >= limit*avger):
            setup.ill = i
            setup.wallobs1 = setup.wa[setup.ill]
            terminate(i)
            break
        i = i + 1
