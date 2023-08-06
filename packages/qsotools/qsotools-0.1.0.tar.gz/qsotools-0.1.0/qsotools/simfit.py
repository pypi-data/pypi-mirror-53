import os,quasar,numpy,math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator,FixedLocator

def blend():
    '''
    Study blend between ZnII 2026 and CrII 2026 lines
    '''
    # Setup values
    disp  = 1.3    #km/s (pixel size of the spectrum)
    fwhm  = 5.0    #resolution 
    noise = 5000.
    wbeg  = 5000.  #A
    wend  = 5200.  #A
    zabs  = 1.5
    dv    = 100     #km/s (half of velocity region to fit for each transition)
    trans = ['CrII    2026.2686000    0.001300    2.00E+008    52       0',
             'CrII    2066.1638990    0.051200    2.00E+008    52   -1360',
             'ZnII    2026.1376450    0.243486    3.36E+008    64    2479']
    b_zn = 8.
    b_cr = b_zn*numpy.sqrt(64./52.)
    n_zn = 13.3
    n_cr = 13.9
    # Create wavelength array with velocity dispersion of 1.3 km/s
    wave = [wbeg]
    while wave[-1]<wend:
        wave.append(wave[-1]*(2*quasar.c+disp)/(2*quasar.c-disp))
    numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))        
    # Generate artificial spectrum with FeII and MgII lines, FWHM of 5 and SNR of 200
    outfile = open('atom.dat','w')
    for i in range(len(trans)):
        outfile.write(trans[i]+'\n')
    outfile.close()
    print 'Generate articial spectrum...'
    script = open('./commands.dat','w')
    script.write('rd wave.dat \n')
    script.write('gp \n')
    script.write('ZnII %.4f %.4f '%(n_zn,b_zn)+str(zabs)+' \n')
    script.write('CrII %.4f %.4f '%(n_cr,b_cr)+str(zabs)+' \n')
    script.write('\n')
    script.write(str(fwhm)+' \n')
    script.write('noise \n')
    script.write('\n')
    script.write(str(noise)+' \n')
    script.write('wt spec.dat (all) \n')
    script.write('lo \n')
    script.close()
    os.system('rdgen < commands.dat > termout')
    os.system('rm termout')
    spec  = numpy.loadtxt('spec.dat')
    wave  = numpy.array(spec[:,0])
    flux  = numpy.array(spec[:,1])
    error = numpy.array(spec[:,2])
    spec1 = numpy.vstack((wave,flux,error)).T
    os.system('rm spec.dat')
    numpy.savetxt('spec.dat',spec1)
    # Create fort.13 with and without applied shift
    print 'Create and fit both fort.13 files...'
    for mode in ['with','without']:
        init = 0 if mode=='with' else 1
        outfile = open('atom.dat','w')
        for i in range(init,len(trans)):
            outfile.write(trans[i]+'\n')
        outfile.close()
        ofile = open('fort_'+mode+'.13','w')
        ofile.write('   *\n')
        for i in range(1,len(trans)):
            ion  = trans[i].split()[0]
            wmid = float(trans[i].split()[1])
            cent = (1+zabs)*wmid
            wbeg = cent*(2*quasar.c-dv)/(2*quasar.c+dv)
            wend = cent*(2*quasar.c+dv)/(2*quasar.c-dv)
            ofile.write('spec.dat       1   {0:.4f}   {1:.4f} vfwhm={2:.1f}  ! {3:<1}_{4:.0f}\n'.format(wbeg,wend,fwhm,ion,wmid))
        ofile.write('  *\n')
        ofile.write('   ZnII     %.4f     %.4fa   %.4fb    0.000q     0.00   0.00E+00  0\n'%(n_zn,zabs,b_zn))
        ofile.write('   CrII     %.4f     %.4fA   %.4fB    0.000Q     0.00   0.00E+00  0\n'%(n_cr,zabs,b_cr))
        ofile.close()
        open('fitcommands','w').write('f\n\n\nfort_'+mode+'.13\n\n\nas\n\n\n'+4*'\n'*len(trans)+'n\n\n')
        os.system('vpfit10 < fitcommands > termout')
        os.system('mv fort.18 fort_'+mode+'.18')
        os.system('mv fort.26 fort_'+mode+'.26')
        os.system('mkdir -p fort_'+mode+' && mv vpfit_chunk* fort_'+mode+'/')
        os.system('rm fitcommands termout')
    # Plots
    print 'Plot results...'
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(1,figsize=(12,8),frameon=False)
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.07, top=0.93, hspace=0, wspace=0.15)
    for i in range(1,len(trans)):
        ion  = trans[i].split()[0]
        wmid = float(trans[i].split()[1])
        for mode in ['with','without']:
            k   = 1 if mode=='with' else 2
            ax  = fig.add_subplot(2,2,k+(i-1)*2,xlim=[-50,50],ylim=[-0.1,1.6])
            fit = numpy.loadtxt('fort_'+mode+'/vpfit_chunk%03i.txt'%i,comments='!')
            mid = (1+zabs)*wmid
            vel = 2*(fit[:,0]-mid)/(fit[:,0]+mid)*quasar.c
            ax.plot(vel,fit[:,3],label='Final model',lw=4,color='red',alpha=0.7)
            ax.plot(vel,fit[:,1],label='Spectrum',lw=2,color='black',alpha=0.7)
            diff = (fit[:,1]-fit[:,3])/fit[:,2]/10.+1.4
            ax.plot(vel,diff,lw=1,label='Residuals',color='magenta',alpha=0.7)
            ax.text(-50,1.5,r'+1$\sigma$ ',ha='right',va='center',size=8)
            ax.text(-50,1.3,r'-1$\sigma$ ',ha='right',va='center',size=8)
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
            ax.axhline(y=0,ls='dotted',color='black')
            ax.axvline(x=0,ls='dotted',color='black')
            ax.axhline(y=1,ls='dotted',color='black')
            ax.axhline(y=1.3,ls='dotted',color='magenta')
            ax.axhline(y=1.4,ls='dotted',color='magenta')
            ax.axhline(y=1.5,ls='dotted',color='magenta')
            lg = ax.legend(loc=(0.03,0.15),handlelength=2)
            fr = lg.get_frame()
            lg.get_frame().set_fill(False)
            fr.set_lw(0.0)
            fort18 = numpy.loadtxt('fort_'+mode+'.18',delimiter='\n',dtype=str)
            for k in range(len(fort18)-1,0,-1):
                if 'q' in fort18[k].split()[7]:
                    alpha = float(fort18[k].split()[7].replace('q',''))
                    error = float(fort18[k].split()[8].replace('q',''))
                    chisq = float(fort18[k-17].split()[2])
                    break
            ions = ion+'_%.0f'%wmid+' + CrII_2026' if mode=='with' and ion=='ZnII' else ion+'_%.0f'%wmid
            t = text(10,0.5,ions,color='black',weight='bold',fontsize=10)
            t = text(10,0.4,'da/a=%.2f+/-%.2f ppm'%(alpha,error),color='black',fontsize=10)
            t = text(10,0.3,'chisq_nu=%.2f'%chisq,color='black',fontsize=10)
            if i==1 and mode=='with':    ax.set_title('With CrII 2026',ha='center',fontsize=10,weight='bold')
            if i==1 and mode=='without': ax.set_title('Without CrII 2026',ha='center',fontsize=10,weight='bold')
            if i<len(trans)-1: plt.setp(ax.get_xticklabels(), visible=False)
            else: ax.set_xlabel('Velocity in km/s relative to $z_{abs}=%.1f$'%zabs,fontsize=10)
            ax.set_ylabel('Flux',fontsize=10)
    plt.show()
    plt.close(fig)
    
def dispersion():
    '''
    Compare Voigt profiles with different velocity dispersion
    '''
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    xmin  = -20
    xmax  = +20
    disp  = 0.02
    test  = numpy.array([[13.27343,5.2143],[12.93114,4.9866],[13.13910,3.9601],[12.93356,8.7214]])
    #test  = numpy.array([[11.67779,0.3382],[12,0.5],[12,1],[13,1]])
    spe   = 'SiII_1526'
    lam   = 1526.70698
    osc   = 0.133
    gam   = 1.13E9
    z     = 2
    ''' Take 50km/s region around SiII 1526 '''
    dv    = 100
    wamid = lam*(z+1)
    start = wamid * (2*quasar.c-dv) / (2*quasar.c+dv)
    end   = wamid * (2*quasar.c+dv) / (2*quasar.c-dv)
    ''' Create high-dispersion data '''
    wave  = numpy.arange(start,end,disp)
    wave1 = numpy.array(['%.4f'%i for i in wave],dtype='str')
    flux  = numpy.array(['1.0000' for i in wave],dtype='str')
    error = numpy.array(['0.0001' for i in wave],dtype='str')
    ofile = open('spectrum.dat','w')
    for i in range(len(wave)):
        ofile.write(wave1[i]+'   '+flux[i]+'   '+error[i]+'\n')
    ofile.close()
    fig = plt.figure(1,figsize=(12,8))
    plt.subplots_adjust(left=0.06, right=0.96, bottom=0.1, top=0.9, hspace=.25, wspace=0.15)
    title('VP generator comparison for SiII1526 with a velocity dispersion of '+str(disp)+' $\AA$\n')
    axis('off')
    for i in range(len(test)):
        N     = test[i,0]
        b     = test[i,1]
        ax    = fig.add_subplot(2,2,i+1,xlim=[xmin,xmax],ylim=[-0.1,1.6])
        ''' Create fort.13, run VPFIT '''
        ofile = open('fort.13','w')
        ofile.write('*\n')
        ofile.write('  spectrum.dat     1   %.2f  %2.f   vsig=0.0001\n'%(start+1,end-1))
        ofile.write('*\n')
        ofile.write('   SiII     %.5f     %.7f    %.4f        0.00   0.00E+00  0\n'%(N,z,b))
        ofile.close()
        ofile = open('fitcommands','w')
        ofile.write('d\n\n\n\ny\nas\n\n\nn\n\n')
        ofile.close()
        print 'adkbdnsvsmf',i
        os.system('vpfit10 < fitcommands')
        ''' Plotting high-dispersion Voigt profile from VPFIT '''
        chunk = numpy.loadtxt('vpfit_chunk001.txt',comments='!')
        wave1 = chunk[:,0]
        vel1  = 2*(wave1-wamid)/(wave1+wamid)*quasar.c
        flux1 = chunk[:,3]
        p1,   = plt.plot(vel1,flux1,lw=4,color='red',alpha=0.7)
        #''' Plotting high-dispersion Voigt profile from ALIS '''
        #
        #wave2 = numpy.arange(start,end,disp)
        #vel2  = 2*(wave2-wamid)/(wave2+wamid)*quasar.c
        #flux2 = quasar.model(N,b,wave2/(z+1),lam,gam,osc)
        #p2,   = plt.plot(vel2,flux2,lw=2,color='black',alpha=0.7)
        ''' Plotting high-dispersion Voigt profile from ALIS with sub-binning beforehand '''
        wave0 = numpy.arange(start,end,disp/25)
        flux0 = quasar.model(N,b,wave0/(z+1),lam,gam,osc)
        wave2 = numpy.arange(start,end,disp)
        flux2 = spec.rebin(wave0,flux0,flux0,wa=wave2).fl
        vel2  = 2*(wave2-wamid)/(wave2+wamid)*quasar.c
        p2,   = plt.plot(vel2,flux2,lw=2,color='black',alpha=0.7)
        ''' Plot residuals '''
        i1    = abs(wave2-wave1[0]).argmin()
        i2    = abs(wave2-wave1[-1]).argmin()+1
        wave  = wave2[i1:i2]
        vel   = 2*(wave-wamid)/(wave+wamid)*quasar.c
        diff  = (flux2[i1:i2]-flux1)
        delta = max([abs(j) for j in diff])
        diff  = diff/delta/10+1.4        
        p3,   = plt.plot(vel,diff,lw=1,color='magenta',alpha=0.7)
        ''' Setup axis and labels '''
        text(5,0.3,'N=%.2f & b=%.2f'%(N,b),ha='left',fontsize=10)
        ax.text(xmin,1.3,r'$-%.5f$ '%delta,ha='right',va='center',size=8)
        ax.text(xmin,1.5,r'$+%.5f$ '%delta,ha='right',va='center',size=8)
        curve = [p1,p2,p3]
        label = ['VPFIT model','ALIS model','Residuals']
        ax.legend(curve,label,numpoints=2,handlelength=3,frameon=False,
                  prop={'size':8},loc='lower left',bbox_to_anchor=[0.01,0.12],ncol=1)
        ax.axhline(y=0,ls='dotted',color='black')
        ax.axvline(x=0,ls='dotted',color='black')
        ax.axhline(y=1,ls='dotted',color='black')
        ax.axhline(y=1.3,ls='dotted',color='magenta')
        ax.axhline(y=1.4,ls='dotted',color='magenta')
        ax.axhline(y=1.5,ls='dotted',color='magenta')
        ax.set_xlabel('Velocity relative to $z_{abs}=%.4f$ (km/s)'%z,fontsize=10)
        ax.set_ylabel('Flux')
        ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    plt.savefig('voigtcomp.pdf') if tbs else plt.show()
    plt.close(fig)    

def distortion(slope=0):
    '''
    Check chi-square curves for distorted Voigt profiles
    '''
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    trans = numpy.array([['FeII',1608.4506440,0.052969,2.00E+008,-1300,14.,9.,2.]],dtype=object)
    #trans = numpy.array([['FeII',2382.7641975,0.293760,2.00E+008, 1460,14.,9.,2.],
    #                  ['FeII',1608.4506440,0.052969,2.00E+008,-1300,14.,9.,2.],
    #                  ['MgII',2796.3550990,0.486245,2.68E+008,  211,13.,8.,2.],
    #                  ['MgII',2803.5322972,0.241582,2.68E+008,  120,13.,8.,2.]],dtype=object)
    #trans = numpy.array([['FeII',1608.4506440,0.052969,2.00E+008,-1300,14.,9.,2.],
    #                  ['MgII',2796.3550990,0.486245,2.68E+008,  211,13.,8.,2.]],dtype=object)
    #trans = numpy.array([['FeII',1608.4506440,0.052969,2.00E+008,-1300,14.,9.,2.]],dtype=object)
    #trans = numpy.array([['FeII',2382.7641975,0.293760,2.00E+008, 1460,14.,9.,2.],
    #                  ['FeII',1608.4506440,0.052969,2.00E+008,-1300,14.,9.,2.]],dtype=object)
    here   = os.getenv('PWD')
    dist   = numpy.arange(-0.5,0.5,0.01)
    ''' --------------------------------------------------------------------------- '''
    ''' Store 100km/s high-resolution region around both FeII regions in ascii file '''
    ''' --------------------------------------------------------------------------- '''
    dv,disp = 500,0.05
    for i in range(len(trans)):
        os.system('mkdir -p regions')
        N,b,z      = trans[i,5],trans[i,6],trans[i,7]
        lambda0    = trans[i,1]
        start      = lambda0 * (z+1) * (2*quasar.c-dv) / (2*quasar.c+dv)
        end        = lambda0 * (z+1) * (2*quasar.c+dv) / (2*quasar.c-dv)
        wave       = [start-2]
        while wave[-1]<end+2:
            wave.append(wave[-1]*(2*quasar.c+disp)/(2*quasar.c-disp))
        wave       = numpy.array(wave)
        q          = trans[i,4]
        wavenum    = 1./(lambda0*10**(-8))
        wavenum    = wavenum - q*(quasar.alpha**2-2*quasar.alpha)
        lambda0    = 1./wavenum*10**(8)
        strength   = trans[i,2]
        gamma      = trans[i,3]
        flux       = quasar.model(N,b,wave/(z+1),lambda0,gamma,strength)
        vsig       = 2.5/disp
        model      = gaussian_filter1d(flux,vsig)
        opfile     = open('regions/region'+str(i+1)+'.dat','w')
        model      = numpy.array(model)+numpy.random.normal(0,0.0001,len(model))
        for j in range(len(wave)):
            shift = quasar.slope*(trans[i,1]*(z+1)-6000.)/1000.
            lambd = wave[j]*(2*quasar.c+shift)/(2*quasar.c-shift)
            opfile.write('%.7f   %.7f   %.7f\n'%(lambd,model[j],0.0001))
        opfile.close()
    if '--nofit' not in sys.argv:
        print '\n{0:>5}{1:>15}{2:>15}{3:>15}\n'.format('slope','alpha','error','chisqnu')
        for slope in dist:
            slstr   = '0.000' if round(slope,3)==0 else str('%.3f'%slope).replace('-','m') if '-' in str(slope) else 'p'+str('%.3f'%slope)
            distrep = './distortion/'+slstr
            os.system('mkdir -p '+distrep)
            os.chdir(distrep)
            ''' ---------------------------------------------------------------- '''
            ''' Prepare distortion folder, update the fort.13 and fit the system '''
            ''' ---------------------------------------------------------------- '''
            shifts = []
            opfile = open('fort_ini.13','w')
            opfile.write('*\n')
            for i in range(len(trans)):
                lambda0 = trans[i,1]
                start   = lambda0 * (z+1) * (2*quasar.c-dv) / (2*quasar.c+dv)
                end     = lambda0 * (z+1) * (2*quasar.c+dv) / (2*quasar.c-dv)
                opfile.write('  ../../regions/region'+str(i+1)+'.dat     1   %.2f  %.2f   vsig=2.5\n'%(start+1,end-1))
                shifts.append(slope*(lambda0*(z+1)-6000.)/1000.)
            opfile.write('*\n')
            opfile.write('   FeII     %.5f     %.7fa     %.4f        0.000q     0.00   0.00E+00   0\n'%(14.1,2,9.1))
            #opfile.write('   MgII     %.5f     %.7fA     %.4f        0.000Q     0.00   0.00E+00   0\n'%(13.1,2,8.1))
            for i in range(len(shifts)):
                opfile.write('   >>         1.0000FF   0.0000000FF  {0:>8}FF      0.000FF    0.00   0.00E+00  {1:>2}\n'.format('%.4f'%shifts[i],'%.0f'%(i+1)))
            opfile.close()
            if os.path.exists('./atom.dat')==False:
                os.system('ln -s ../../../atom.dat     .')
                os.system('ln -s ../../../vp_setup.dat .')
                os.system('ln -s ../../header.dat   .')
            os.environ['ATOMDIR']='./atom.dat'
            os.environ['VPFSETUP']='./vp_setup.dat'
            open('fitcommands','w').write('f\n\n\nfort_ini.13\nn\nn\n')
            os.system('vpfit10 < fitcommands > termout')
            final = open('fort_fit.13','w')
            final.write('   *\n')
            line26 = numpy.loadtxt('fort.26',dtype='str',delimiter='\n')
            for i in range(len(line26)):
                if line26[i][0:2]!='%%':
                    break
                else:
                    final.write(line26[i].replace('%% ','')+'\n')
            final.write('  *\n')
            line18 = numpy.loadtxt('fort.18',dtype='str',delimiter='\n')
            for i in range(len(line18)-1,0,-1):
                if 'chi-squared' in line18[i]:
                    a = i + 2
                    break
            for i in range(a,len(line18)):
                if len(line18[i])==1:
                    break
                final.write(line18[i]+'\n')
            final.close()
            fort18 = numpy.loadtxt('fort.18',dtype='str',delimiter='\n')
            for i in range(len(fort18)-1,0,-1):
                if 'arameter errors:' in fort18[i]:
                    for j in range(i+1,len(fort18)):
                        line = fort18[j]
                        s = 1 if len(line.split()[0])==1 else 0
                        if 'statistics' in line:
                            break
                        elif 'q' in str(line.split()[4+s]):
                            error = float(line.split()[4+s].split('q')[0])
                            break
                if 'chi-squared :' in fort18[i]:
                    chisq   = float(fort18[i].split()[-3].replace(',',''))
                    ndf     = float(fort18[i].split()[-2])
                    chisqnu = chisq/ndf
                    for j in range(i+2,len(fort18)):
                        line = fort18[j]
                        s    = 1 if len(line.split()[0])==1 else 0
                        if 'errors' in line:
                            break
                        if 'q' in str(line.split()[4+s]):
                            alpha = float(line.split()[4+s].split('q')[0])
                            break
                    break
            print '{0:>5}{1:>15}{2:>15}{3:>15}'.format('%.2f'%slope,'%.4f'%(alpha*10**5),'%.4f'%(error*10**5),'%.7f'%chisqnu)
            os.chdir(here)
    ''' ----------------------------------------- '''
    ''' Retrieve results from all distortion fits '''
    ''' ----------------------------------------- '''
    results = numpy.empty((0,4))
    for slope in dist:
        slopestr = '0.000' if round(slope,3)==0 else str('%.3f'%slope).replace('-','m') if '-' in str(slope) else 'p'+str('%.3f'%slope)
        fortpath = './distortion/'+slopestr+'/fort.18'
        fort18   = numpy.loadtxt(fortpath,dtype='str',delimiter='\n')
        for i in range(len(fort18)-1,0,-1):
            if 'arameter errors:' in fort18[i]:
                for j in range(i+1,len(fort18)):
                    line = fort18[j]
                    s = 1 if len(line.split()[0])==1 else 0
                    if 'statistics' in line:
                        break
                    elif 'q' in str(line.split()[4+s]):
                        error = float(line.split()[4+s].split('q')[0])/10**(-5)
                        break
            if 'chi-squared :' in fort18[i]:
                chisq   = float(fort18[i].split()[-3].replace(',',''))
                ndf     = float(fort18[i].split()[-2])
                chisqnu = chisq/ndf
                for j in range(i+2,len(fort18)):
                    line = fort18[j]
                    s    = 1 if len(line.split()[0])==1 else 0
                    if 'errors' in line:
                        break
                    if 'q' in str(line.split()[4+s]):
                        alpha = float(line.split()[4+s].split('q')[0])/10**(-5)
                        break
                break
        results = numpy.vstack((results,[slope,alpha,error,chisqnu]))
    ''' ------------------------------------- '''
    ''' Plots all alpha and chi-square values '''
    ''' ------------------------------------- '''
    fig = plt.figure(figsize=(6,8))
    plt.subplots_adjust(left=0.14, right=0.95, bottom=0.08, top=0.9, hspace=0, wspace=0.2)
    ax = plt.subplot(4,1,1,xlim=[3000,9000])
    title('Initials: da/a=%.2f ; distortion=%.2f\n'%(quasar.alpha/10**(-5),quasar.slope),fontsize=10)
    for slope in dist:
        x0 = 6000
        x = numpy.arange(3000,9000,1)
        y = -slope*x0 + slope*x
        ax.plot(x,y,'grey',lw=0.1,zorder=2,alpha=0.7)
    ax.axhline(y=0,ls='dotted',color='black')
    ylabel('Shift (m/s)')
    xlabel('Wavelength range')
    ymin,ymax = min(results[:,3]),max(results[:,3])
    ax = plt.subplot(3,1,3,xlim=[min(dist),max(dist)])
    ax.errorbar(results[:,0],results[:,3],fmt='o',ms=4,markeredgecolor='none',ecolor='grey',alpha=0.8,color='black')
    ax.axhline(y=0,ls='dotted',color='black')
    ylabel('Reduced $\chi^2$\n',fontsize=8)
    xlabel('Distortion slope (m/s/$\AA$)',fontsize=8)
    #fitparabola(results[:,0],results[:,3])
    ax.axvline(x=0,color='black')
    #ax.axvline(x=quasar.xmid,color='red',lw=1,ls='dashed')
    #t = ax.text(0,ymin+0.75*(ymax-ymin),'Min. $\chi^2$\n%.3f +/- %.3f'%(quasar.xmid,quasar.xp1sig-quasar.xmid),fontsize=8,color='red',ha='center')
    #t.set_bbox(dict(color='white', alpha=0.8, edgecolor=None))
    ymin,ymax = min(results[:,1]),max(results[:,1])
    minyerr,maxyerr = min(results[:,1]-results[:,2]),max(results[:,1]+results[:,2])
    ax = plt.subplot(3,1,2,xlim=[min(dist),max(dist)],ylim=[0-max(minyerr,maxyerr),0+max(minyerr,maxyerr)])
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.errorbar(results[:,0],results[:,1],yerr=results[:,2],fmt='o',ms=4,markeredgecolor='none',ecolor='grey',alpha=0.8,color='black')
    ax.axhline(y=0,ls='dotted',color='black')
    ylabel('da/a $(10^{-5})$\n',fontsize=8)
    #fitlinear(results[:,0],results[:,1],-0.5,0.5,yerr=results[:,2])
    ax.axvline(x=0,color='black')
    ax.axvline(x=0,ls='dotted',color='black')
    #ax.axvline(x=quasar.xmid,color='red',lw=1,ls='dashed')
    #ax.axhline(y=quasar.alphafit,color='red',lw=1,ls='dashed')
    #t = ax.text(0,ymin+0.75*(ymax-ymin),'Alpha at min. $\chi^2$\n%.3f'%(quasar.alphafit),fontsize=8,color='red',ha='center')
    #t.set_bbox(dict(color='white', alpha=0.8, edgecolor=None))
    plt.savefig('plot.pdf') if tbs else plt.show()
    plt.close(fig)    

def distshift(output=quasar.output):
    '''
    Investigate impact on da/a for shifted model and data. The procedure is the
    following:

    1. Create wavelength array
    2. Generate artificial spectrum with FeII and MgII lines using RDGEN
    3. Create 2 artificial spectra with non-distorted and distorted wavelength array.
    4. Create fort.13 with applied shift
    5. Create fort.13 without applied shift
    6. Fit shifted model with non-distorted spectrum
    7. Fit non-shifted model with distorted spectrum
    8. Plot results

    Examples
    --------

    >>> quasar distshift

    .. image:: ../_images/example_simplot_distshift.png
    '''
    # Copy atom.dat vp_setup.dat files
    os.system('cp %s/atom.dat .'%quasar.datapath)
    os.system('cp %s/vp_setup_v10.dat vp_setup.dat'%quasar.datapath)
    # Setup values
    disp  = 1.3    #km/s (pixel size of the spectrum)
    fwhm  = 5.0    #resolution 
    noise = 80.
    wbeg  = 4000.  #A
    wend  = 7020.  #A
    wmid  = (wbeg+wend)/2.  #A
    slope = 5    #m/s/A
    zabs  = 1.5
    dv    = 100     #km/s (half of velocity region to fit for each transition)
    # Create wavelength array with velocity dispersion of 1.3 km/s
    wave = [wbeg]
    while wave[-1]<wend:
        wave.append(wave[-1]*(2*quasar.c+disp)/(2*quasar.c-disp))
    numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))        
    # Generate artificial spectrum with FeII and MgII lines, FWHM of 5 and SNR of 200
    print 'Generate articial spectrum...'
    script = open('./commands.dat','w')
    script.write('rd wave.dat \n')
    script.write('gp \n')
    script.write('FeII 13.7 5 '+str(zabs)+' \n')
    script.write('MgII 13.0 4 '+str(zabs)+' \n')
    script.write('\n')
    script.write(str(fwhm)+' \n')
    script.write('noise \n')
    script.write('\n')
    script.write(str(noise)+' \n')
    script.write('wt spec.dat (all) \n')
    script.write('lo \n')
    script.close()
    os.system('rdgen < commands.dat > termout')
    os.system('rm termout')
    # Create 2 artificial spectra, one original and one distorting the wavelength array.
    print 'Create distorted spectrum...'
    spec  = numpy.loadtxt('spec.dat')
    wave  = numpy.array(spec[:,0])
    flux  = numpy.array(spec[:,1])
    error = numpy.array(spec[:,2])
    spec1 = numpy.vstack((wave,flux,error)).T
    shift = slope*(spec[:,0]-wmid)/1000.
    wave  = wave*(2*quasar.c+shift)/(2*quasar.c-shift)
    spec2 = numpy.vstack((wave,flux,error)).T
    numpy.savetxt('spec_norm.dat',spec1)
    numpy.savetxt('spec_dist.dat',spec2)
    os.system('rm spec.dat')
    # Create fort.13 with and without applied shift
    print 'Create fort.13 files...'
    trans = numpy.array([['FeII',2344.2128814],['FeII',1608.4506440],['MgII',2796.3550990],['MgII',2803.5322972]],dtype=object)
    for mode in ['norm','dist']:
        ofile = open('fort_'+mode+'.13','w')
        ofile.write('   *\n')
        for i in range(len(trans)):
            cent  = (1+zabs)*trans[i,1]
            wbeg  = cent*(2*quasar.c-dv)/(2*quasar.c+dv)
            wend  = cent*(2*quasar.c+dv)/(2*quasar.c-dv)
            ofile.write('spec_'+mode+'.dat       1   {0:.4f}   {1:.4f} vfwhm={2:.1f}  ! {3:<1}_{4:.0f}\n'.format(wbeg,wend,fwhm,trans[i,0],trans[i,1]))
        ofile.write('  *\n')
        ofile.write('   FeII     13.70000     1.5000000a     5.0000       0.000q       0.00   0.00E+00  0\n')
        ofile.write('   MgII     13.00000     1.5000000A     4.0000       0.000Q       0.00   0.00E+00  0\n')
        if mode=='norm':
            for i in range(len(trans)):
                cent  = (1+zabs)*trans[i,1]
                shift = '%.4f'%(-slope*(cent-wmid)/1000.)
                ofile.write('   >>        1.00000FF   0.0000000FF  {0:>8}FF     0.000FF      0.00   0.00E+00  {1:.0f}\n'.format(shift,i+1))
        ofile.close()
    # Fit shifted model with non-distorted spectrum and non-shifted model with distorted spectrum
    print 'Fit first guesses...'
    for mode in ['norm','dist']:
        open('fitcommands','w').write('d\n\n\nfort_'+mode+'.13\n\n\nas\n\n\n'+4*'\n'*len(trans)+'n\n\n')
        os.system('vpfit10 < fitcommands > termout')
        os.system('mkdir -p fort_'+mode+'_ini && mv vpfit_chunk* fort_'+mode+'_ini/')
        os.system('rm fitcommands termout') 
        open('fitcommands','w').write('f\n\n\nfort_'+mode+'.13\n\n\nas\n\n\n'+4*'\n'*len(trans)+'n\n\n')
        os.system('vpfit10 < fitcommands > termout')
        os.system('mv fort.18 fort_'+mode+'.18')
        os.system('mv fort.26 fort_'+mode+'.26')
        os.system('mkdir -p fort_'+mode+'_fit && mv vpfit_chunk* fort_'+mode+'_fit/')
        os.system('rm fitcommands termout')
    # Plots
    print 'Plot results...'
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(1,figsize=(12,8))
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.07, top=0.93, hspace=0, wspace=0.15)
    for i in range(len(trans)):
        for mode in ['norm','dist']:
            k   = 1 if mode=='norm' else 2
            ax  = fig.add_subplot(4,2,k+i*2,xlim=[-50,50],ylim=[-0.1,1.1])
            ini = numpy.loadtxt('fort_'+mode+'_ini/vpfit_chunk%03i.txt'%(i+1),comments='!')
            fit = numpy.loadtxt('fort_'+mode+'_fit/vpfit_chunk%03i.txt'%(i+1),comments='!')
            mid = (1+zabs)*trans[i,1]
            vel = 2*(ini[:,0]-mid)/(ini[:,0]+mid)*quasar.c
            ax.plot(vel,ini[:,1],label='Spectrum',color='black',lw=0.8)
            ax.plot(vel,ini[:,3],label='Fitting model',color='blue',lw=0.8)
            ax.plot(vel,fit[:,3],label='Final model',color='green',lw=0.8,ls='dashed')
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
            ax.axhline(y=0,ls='dotted',lw=.2)
            ax.axhline(y=1,ls='dotted',lw=.2)
            ax.axvline(x=0,ls='dotted',lw=.2)
            lg = ax.legend(loc=(0.03,0.15),handlelength=2)
            fr = lg.get_frame()
            lg.get_frame().set_fill(False)
            fr.set_lw(0.0)
            fort18 = numpy.loadtxt('fort_'+mode+'.18',delimiter='\n',dtype=str)
            for k in range(len(fort18)-1,0,-1):
                if 'q' in fort18[k].split()[7]:
                    alpha = float(fort18[k].split()[7].replace('q',''))/10
                    error = float(fort18[k].split()[8].replace('q',''))/10
                    break
            t = ax.text(20,0.4,'da/a=%.1f+/-%.1f'%(alpha,error),color='black',fontsize=10)
            t = ax.text(20,0.5,trans[i,0]+'_%.0f'%trans[i,1],color='black',weight='bold',fontsize=10)
            if i==0 and mode=='norm': ax.text(0,1.2,'Distorted model',ha='center',fontsize=10,weight='bold')
            #if i==0 and mode=='norm': text(0,1.15,'Noise %.0f px$^{-1}$ - Pixel size %.1f km/s - FWHM %.0f km/s'%(noise,disp,fwhm),ha='center',fontsize=10)
            if i==0 and mode=='dist': ax.text(0,1.2,'Distorted spectrum',ha='center',fontsize=10,weight='bold')
            #if i==0 and mode=='dist': text(0,1.15,'Noise %.0f px$^{-1}$ - Pixel size %.1f km/s - FWHM %.0f km/s'%(noise,disp,fwhm),ha='center',fontsize=10)
            if i<len(trans)-1: plt.setp(ax.get_xticklabels(), visible=False)
            else: ax.set_xlabel('Velocity in km/s relative to $z_{abs}=%.1f$'%zabs,fontsize=10)
            ax.set_ylabel('Flux',fontsize=10)
    plt.show() if output==None else plt.savefig('distshift.pdf')
    plt.close(fig)

