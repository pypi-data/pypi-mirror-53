import quasar,os,numpy,math,argparse,seaborn
import matplotlib.pyplot as plt

def twocomps(path=quasar.path,b=quasar.dop,bfactor=quasar.bfactor,colmin=quasar.colmin,
             colmax=quasar.colmax,nratio=quasar.nratio,nbin=quasar.nbin,fwhm=quasar.fwhm,
             resolution=quasar.res,noise=quasar.noise,vsep=quasar.vsep,wbeg=quasar.wbeg,
             wend=quasar.wend,zabs=quasar.zabs,output=quasar.output,dv=quasar.dv,dw=quasar.dw,
             todo=quasar.todo):
    '''
    Generate 10 spectra with two components, one narrow and one broad.
    
    Parameters
    ----------
    path : str
      Path to run the calculation
    b : float
      Doppler parameter
    bfactor : float
      Factor between both components Doppler parameters
    colmin : float
      Minimum column density
    colmax : float
      Maximum column density
    nratio : float
      Column density ratio between both components
    nbin : float
      Number of models
    fwhm : float
      Full Width Half Maximum resolution
    resolution : float
      Resolving Power
    noise : float
      Noise
    vsep : float
      Velocity separation between 2 components
    wbeg : float
      First wavelength
    wend : float
      Last wavelength
    zabs : float
      Absorption redshift of the main component
    dv : float
      Velocity width of fitting regions
    dw : float
      Wavelength width of fitting regions
    todo : str
      Action to perform. Default is all.

    Examples
    --------
    As executable:

    >>> quasar twocomps --zabs 4 --fwhm 7 --colmin 16 --colmax 23 \\
    >>>                 --nbin 15 --dv 500 --bfactor 5 --noise 100

    As python program:

    >>> import quasar
    >>> quasar.twocomps(zabs=4,fwhm=7,colmin=16,colmax=23,nbin=15,dv=500,bfactor=5,noise=100)
    '''
    # Go to repository
    path = os.path.abspath(path)
    os.system('mkdir -p '+path)
    os.chdir(path)
    # Copy atom.dat and vp_setup.dat files
    quasar.get_atomdat()
    quasar.novars = 3
    quasar.get_vpsetup()
    # Calculate FWHM if resolution is given instead of FWHM
    fwhm = fwhm if fwhm!=None else quasar.c/resolution
    vsig = fwhm/(2.*numpy.sqrt(2.*math.log(2.)))
    # Determine redshift of shifted component
    z_main = zabs
    z_broad = z_main * (2*quasar.c+vsep) / (2*quasar.c-vsep) + 2*vsep / (2*quasar.c-vsep)
    if todo in ['all','create']:
        # Create wavelength array
        wave = [wbeg]
        while wave[-1]<wend:
            wave.append(wave[-1]*(2*quasar.c+fwhm)/(2*quasar.c-fwhm))
        numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))
        # Loop over all column densities
        for col in numpy.linspace(colmin,colmax,nbin):
            # Prepare repository and move to it
            os.system('mkdir -p %s/spec_%.2f'%(path,col))
            os.chdir('%s/spec_%.2f'%(path,col))
            # Restore symbolic links
            for link in ['atom.dat','vp_setup.dat','wave.dat']:
                if os.path.exists(link):
                    os.system('rm %s'%link)
                os.system('ln -s ../%s'%link)
            # Define column density and doppler parameters of both components
            n_main,b_main = col,b
            n_broad,b_broad = col+nratio,b*bfactor
            # Generate artificial spectrum with FeII and MgII lines, FWHM of 5 and SNR of 200
            script = open('./commands.dat','w')
            script.write('rd wave.dat \n')
            script.write('gp \n')
            script.write('H I %s %s %s \n'%(n_main,b_main,z_main))
            script.write('H I %s %s %s \n'%(n_broad,b_broad,z_broad))
            script.write('\n')
            script.write('%s \n'%fwhm)
            script.write('noise \n')
            script.write('\n')
            script.write('%s \n'%noise)
            script.write('wt spectrum.dat (all) \n')
            script.write('lo \n')
            script.close()
            os.system('rdgen < commands.dat > termout')
            os.system('rm termout')
            spectrum = numpy.loadtxt('spectrum.dat',usecols=[0,1,2])
            numpy.savetxt('spectrum.dat',spectrum)
    if todo in ['all','fit']:
        # Loop over all column densities
        for col in numpy.linspace(colmin,colmax,nbin):
            # Prepare repository and move to it
            os.chdir('%s/spec_%.2f'%(path,col))
            # Define column density and doppler parameters of both components
            n_main,b_main = col,b
            n_broad,b_broad = col+nratio,b*bfactor
            # Loop over all column densities
            for ncomp in [1,2]:
                ofile = open('fort%s.13'%ncomp,'w')
                ofile.write('   *\n')
                for i in range(len(quasar.HI)-15):
                    wmid = quasar.HI[i]['wave']
                    ion  = 'HI_%.2f'%wmid
                    cent = (1+zabs)*wmid
                    wbeg = cent-dw if dw!=None else cent*(2*quasar.c-dv)/(2*quasar.c+dv)
                    wend = cent+dw if dw!=None else cent*(2*quasar.c+dv)/(2*quasar.c-dv)
                    ofile.write('spectrum.dat   1   {0:.4f}   {1:.4f} vsig={2:.6f}  ! {3}\n'.format(wbeg,wend,vsig,ion))
                ofile.write('  *\n')
                ofile.write('   H I      %.4f     %.4f   %.4f    0.00   0.00E+00  0\n'%(n_main,zabs,b_main))
                if ncomp==2:
                    ofile.write('   H I      %.4f     %.4f   %.4f    0.00   0.00E+00  0\n'%(n_broad,z_broad,b_broad))
                ofile.close()
                open('fitcommands','w').write('f\n\n\nfort%s.13\n\n\nas\n\n\n'%ncomp+4*'\n'*len(quasar.HI)+'\n\nn\n\n')
                os.system('vpfit10 < fitcommands > termout')
                os.system('mv fort.18 fort%s.18'%ncomp)
                os.system('mv fort.26 fort%s.26'%ncomp)
                os.system('mkdir -p fort%s && mv vpfit_chunk* fort%s/'%(ncomp,ncomp))
                os.system('rm termout') 
    if todo in ['all','plot']:
        seaborn.set_context(rc={'grid.linewidth':1.2})
        fig = plt.figure(figsize=(10,8),frameon=False,dpi=300)
        fig.subplots_adjust(hspace=0.3)
        # Loop over all column densities
        for ncomp in [1,2]:
            data = numpy.empty((0,2))
            ax = plt.subplot(2,1,ncomp,sharex=None if ncomp==1 else ax,xlim=[colmin-0.1,colmax+0.1],sharey=None if ncomp==1 else ax)
            for col in numpy.linspace(colmin,colmax,nbin):
                # Define column density and doppler parameters of both components
                n_main,b_main = col,b
                n_broad,b_broad = nratio+col,b*bfactor
                if os.path.exists(path+'/spec_%.2f/fort%s.26'%(col,ncomp)):
                    f = open('spec_%.2f/fort%s.26'%(col,ncomp),'r')
                    for line in f:
                        if 'Stats' in line:
                            data = numpy.vstack((data,[col,float(line.split()[3])]))
                            break
            ax.scatter(data[:,0],data[:,1])
            ax.set_xlabel('log(N) of main component',fontsize=12)
            ax.set_ylabel('Reduced chi-squared',fontsize=12)
            ax.set_title('Two-component system fitted with %s components'%ncomp)
        plt.ticklabel_format(useOffset=False)
        plt.tight_layout()
        plt.show()
