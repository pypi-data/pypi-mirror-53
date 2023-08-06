import sys,math,numpy,re
from scipy import integrate

def coordinates(args):
    '''
    Convert coordinates and get distance to alpha dipole. Right ascension and
    declination are converted into different formats so that either of the
    outputs can be used for analysis.

    Parameters
    ----------
    ra : str
      Right ascension 
    dec : str
      Declination

    Notes
    -----
    This method can be run as executable using one of the following usages::

      quasar coordinates --simbad '00 15 45.2 +22 01 34'
      quasar coordinates --ra 00:15:45.2 --dec +22:01:34

    The arguments ``--dipra`` and ``--dipdec`` can be used to customize the
    location of the dipole.
    '''
    ra  = ra  if simbad==None else simbad.split()[:3]
    dec = dec if simbad==None else simbad.split()[3:]
    if len(ra)==len(dec)==3:
        # Decompose right ascension values
        ra   = float(ra[0])+float(ra[1])/60+float(ra[2])/3600
        hrs  = float(str(abs(ra)).split('.')[0])
        mins = float(str(abs(60.*(ra-hrs))).split('.')[0])
        sec1 = float(str(abs(3600.*(ra-hrs-mins/60.))).split('.')[0])
        sec2 = ('%.3f'%float(abs(3600.*(ra-hrs-mins/60.)-sec1))).split('.')[1]
        ra2  = '%02i:%02i:%02i.'%(hrs,mins,sec1)+sec2
        # Decompose declinaison values
        sign = -1 if float(dec[0])<0 else 1
        dec  = float(dec[0])+sign*float(dec[1])/60+sign*float(dec[2])/3600
        sign = '-' if dec<0 else '+'
        degs = float(str(abs(dec)).split('.')[0])
        mins = float(str(abs(60.*(abs(dec)-degs))).split('.')[0])
        sec1 = float(str(abs(3600.*(abs(dec)-degs-mins/60.))).split('.')[0])
        sec2 = ('%.3f'%float(abs(3600.*(dec-degs-mins/60.)-sec1))).split('.')[1]
        dec2 = sign+'%02i:%02i:%02i.'%(degs,mins,sec1)+sec2
        print('\n\tRA  : {0:>13} | {1:>10}h | {2:>10}d'.format(ra2,'%.6f'%ra,'%.6f'%(ra*360./24.)))
        print('\tDEC : {0:>13} | {1:>10}d | {2:>10}d'.format(dec2,'%.6f'%dec,'%.6f'%dec))
    elif ':' in ra:
        # Decompose right ascension values
        ra   = ra.split(':')
        ra   = float(ra[0])+float(ra[1])/60+float(ra[2])/3600
        hrs  = float(str(abs(ra)).split('.')[0])
        mins = float(str(abs(60.*(ra-hrs))).split('.')[0])
        sec1 = float(str(abs(3600.*(ra-hrs-mins/60.))).split('.')[0])
        sec2 = ('%.3f'%float(abs(3600.*(ra-hrs-mins/60.)-sec1))).split('.')[1]
        ra2  = '%02i:%02i:%02i.'%(hrs,mins,sec1)+sec2
        # Decompose declinaison values
        dec  = dec.split(':')
        sign = -1 if float(dec[0])<0 else 1
        dec  = float(dec[0])+sign*float(dec[1])/60+sign*float(dec[2])/3600
        sign = '-' if dec<0 else '+'
        degs = float(str(abs(dec)).split('.')[0])
        mins = float(str(abs(60.*(dec-degs))).split('.')[0])
        sec1 = float(str(abs(3600.*(dec-degs-mins/60.))).split('.')[0])
        sec2 = ('%.3f'%float(abs(3600.*(dec-degs-mins/60.)-sec1))).split('.')[1]
        dec2 = sign+'%02i:%02i:%02i.'%(degs,mins,sec1)+sec2
        print('\n\tRA  : {0:>13} | {1:>8}h | {2:>8}d'.format(ra2,'%.4f'%ra,'%.4f'%(ra*360./24.)))
        print('\tDEC : {0:>13} | {1:>8}d | {2:>8}d'.format(dec2,'%.4f'%dec,'%.4f'%dec))
    else:
        # Decompose right ascension values
        ra   = float(re.compile(r'[a-zA-Z]+').sub('',ra))
        ra   = ra if 'h' in ra else ra*24./360
        hrs  = float(str(abs(ra)).split('.')[0])
        mins = float(str(abs(60.*(ra-hrs))).split('.')[0])
        sec1 = float(str(abs(3600.*(ra-hrs-mins/60.))).split('.')[0])
        sec2 = ('%.3f'%float(abs(3600.*(ra-hrs-mins/60.)-sec1))).split('.')[1]
        ra2  = '%02i:%02i:%02i.'%(hrs,mins,sec1)+sec2
        # Decompose declinaison values
        dec  = float(re.compile(r'[a-zA-Z]+').sub('',dec))
        sign = '-' if dec<0 else '+'
        degs = float(str(abs(dec)).split('.')[0])
        mins = float(str(abs(60.*(abs(dec)-degs))).split('.')[0])
        sec1 = float(str(abs(3600.*(abs(dec)-degs-mins/60.))).split('.')[0])
        sec2 = ('%.3f'%float(abs(3600.*(abs(dec)-degs-mins/60.)-sec1))).split('.')[1]
        dec2 = sign+'%02i:%02i:%02i.'%(degs,mins,sec1)+sec2
        print('\n\tRA  : {0:>13} | {1:>8}h | {2:>8}d'.format(ra2,'%.4f'%ra,'%.4f'%(ra*360./24.)))
        print('\tDEC : {0:>13} | {1:>8}d | {2:>8}d'.format(dec2,'%.4f'%dec,'%.4f'%dec))
    ra    = ra*360./24.
    xdipp = xdipp*360/24
    xdipm = xdipp+180
    ydipm = -ydipp
    print('')
    print('\tDistance to dipole ({:>5},{:>5})      : {:>8} degrees'.format(xdipp,ydipp,'%.4f'%args.spherical_distance(ra*360./24.,dec,xdipp,ydipp)))
    print('\tDistance to anti-dipole ({:>5},{:>5}) : {:>8} degrees'.format(xdipm,ydipm,'%.4f'%args.spherical_distance(ra*360./24.,dec,xdipm,ydipm)))
    print('')
            
def distance(args):
    '''
    Spherical distance between 2 coordinates
    '''
    if args.ra1==None or args.dec1==None or args.ra2==None or args.dec2==None:
        print("")
        print("  Calculate spherical between 2 points.")
        print("")
        print("   --ra1, --dec1      Right ascension and declinaison of first object.")
        print("   --ra2, --dec2      Right ascension and declinaison of second object.")
        print("   --dipra            Right ascension in decimal hour of dipole [17.3]")
        print("   --dipdec           Declinaison in decimal degree of dipole [-61]")
        print("")
    else:
        print('\nObject 1:')
        args.ra,args.dec = args.ra1,args.dec1
        coordinates()
        args.ra1,args.dec1 = args.ra,args.dec
        print('Object 2:')
        args.ra,args.dec = args.ra2,args.dec2
        coordinates()
        args.ra2,args.dec2 = args.ra,args.dec
        print('Spherical distance between the 2 given coordinates: %.4f degrees.'%spherical_distance(args.ra1,args.dec1,args.ra2,args.dec2))
        print('')
        
def coscal(args):
    '''
    Cosmological Calculator.

    Parameters
    ----------
    z : float
      Absorption redshift
    '''
    if z==None:
        print("")
        print("  Look-back cosmological time calculation.")
        print("")
        print("   --z    Redshift at which the look back time should calculated.")
        print("")
    else:
        z = float(z)
        def e_z(z): return 1.0/math.sqrt(omega_m*((1+z)**3)+ omega_k*((1+z)**2) + omega_lambda)
        def lb_e_z(z): return 1.0/((1+z)*math.sqrt(omega_m*((1+z)**3)+ omega_k*((1+z)**2) + omega_lambda))
        H0           = 71     # 100*h Km/s/Mpc
        omega_m      = 0.27
        omega_k      = 0.
        omega_lambda = 0.73    
        H0_std = (H0/(3.08568025 * 10**19))  # sec-1
        d_h = args.c/H0    # Mpc
        e_z_int, e_z_int_err = integrate.quad(e_z,0.,z)
        d_c = d_h * e_z_int
        e_z_int2, e_z_int_err2 = integrate.quad(lb_e_z,0.,z)
        lbt = e_z_int2/H0_std/(3600*24*365.25*10**9)
        age = 13.798 - lbt
        if (omega_k==0.0):
            d_t = d_c
        elif (omega_k>0.0):
            d_t = d_h/math.sqrt(omega_k) * math.sinh(math.sqrt(omega_k)*d_c/d_h)
        else:
            d_t = d_h/math.sqrt(abs(omega_k)) * math.sinh(math.sqrt(abs(omega_k))*d_c/d_h)
        if (omega_lambda==0.0):
            d_t = d_h * 2 *(2 - (omega_m *(1-z)) - ((2-omega_m) * (math.sqrt(1+(omega_m*z))))) / (omega_m**2 * (1+z))
        d_a = d_t / (1+z)    
        d_l = (1+z) * d_t
        dm = 5.0 * numpy.log10(d_l*10**6/10)
        print('')
        print('Hubble Distance................',d_h,'Mpc')
        print('Total LOS Comoving Distance....',d_c,'Mpc')
        print('Transverse Comoving Distance...',d_t,'Mpc')
        print('Angular Diameter Distance .....',d_a,'Mpc')
        print('Luminosity Distance............',d_l,'Mpc')
        print('Distance Modulus...............',dm)
        print('Lookback Time..................',lbt,'Gyrs')
        print('Age of the Universe at z.......',age,'Gyrs')
        print('')
        
def edges(args):
    '''
    Wavelength edges around given Lyman-alpha wavelength
    '''
    if len(sys.argv)<4:
        print('Please specify central redshift and velocity dispersion')
    else:
        z  = float(sys.argv[2])
        dv = float(sys.argv[3])
        wl = 1215.67*(z+1)
        dl = wl*(dv/2)/args.c
        print('')
        print('A z =',z,'HI Lyman-alpha system corresponds to lambda:',round(wl,2))
        print('The',dv,'km/s region around that line is:',round(wl-dl,2),'-',round(wl+dl,2))
        print('')
    
def omegab(args):
    '''
    Get baryon density from D/H values
    '''
    if len(sys.argv)<4:
        print('Please specify the D/H value and its uncertainty')
        quit()

    dtoh  = float(sys.argv[2])
    delta = float(sys.argv[3])
    eta10 = 6. / 273.9 * (2.55 / dtoh)**(5./8.)
    delta = eta10 * (5./8.) * delta / dtoh

    print(100*eta10,100*delta)
        
def rydberg(args):
    '''
    Compute wavelength and energy of Rydberg atom
    '''
    me = 9.10938291 * 10**(-31)     # kg
    mp = 1.672621777 * 10**(-27)    # kg
    mn = 1.674927351 * 10**(-27)    # kg
    e  = 1.602176565 * 10**(-19)    # Coulomb
    pe = 8.854187817620 * 10**(-12) # F/m
    h  = 6.62606957 * 10**(-34)     # J.s
    c  = 299792458                  # m/s
    lambd = (me+(args.Np*mp+args.Nn*mn))/(me*(args.Np*mp+args.Nn*mn)) * (8*pe**2*h**3*c)/e**4 * 4/3
    E = (me*(args.Np*mp+args.Nn*mn))/(me+(args.Np*mp+args.Nn*mn)) * e**4/(8*pe**2*h**2) / e
    print('')
    print(args.Np,'proton and',args.Nn,'neutrons (use options for custom values):')
    print('Lambda =',lambd*10**10,'Angstrom')
    print('Energy =',E,'eV')
    print('')
            
def veldisp(args):
    '''
    Calculate velocity dispersion between 2 redshifts/wavelengths
    
    Parameters
    ----------
    wa : float
      Two wavelength values
    z : float
      Two redshift values

    Examples
    --------
      >>> quasar veldisp --wa 1215.6701 1215.3394
    '''
    if args.z!=None:
        dv = 2 * (args.z[1]-args.z[0]) / (args.z[1]+args.z[0]+2) * args.c
        print('\nThe velocity dispersion betweeen redshifts %s and %s is %s km/s\n'%(args.z[0],args.z[1],dv))
    if args.w!=None:
        dv = 2 * (args.w[1]-args.w[0]) / (args.w[1]+args.w[0]) * args.c
        print('\nThe velocity dispersion betweeen wavelengths %s and %s is %s km/s\n'%(args.w[0],args.w[1],dv))
        
def shift(args):
    '''
    Calculate shifted redshift/wavelength.

    Parameters
    ----------
    wa : float
      Wavelength
    z : float
      Redshift
    dv : float
      Velocity shift

    Examples
    --------
      >>> quasar shift --wa 1215.6701 --dv 80
      >>> quasar shift -z 1.2304 --dv 80
    '''
    if wa==None:
        shift = float(z) * (2*args.c+dv) / (2*args.c-dv) + 2*dv / (2*args.c-dv)
        print('\nThe shifted redshift is %s\n'%shift)
    else:
        shift = float(wa) * (2*args.c+dv) / (2*args.c-dv)
        print('\nThe shifted wavelength is %s\n'%shift)

def alphadist(args):
    '''
    Calculate da/a for distorted system
    '''
    c = 299792.458
    # Reproducing value from John's table
    zabs = 0
    daoa = 1e-5        # da/a value to test
    wrest,q = 2796.3550990, 211.
    # Calculate the shifted wavelength due to da/a
    wobs   = wrest*(1+zabs)                # observed wavelength
    omega  = 10**8 / wrest                 # rest-frame wavenumber
    omega  = omega-q*(daoa**2-2*daoa)      # rest-frame wavenumber with da/a added 
    wshift = 10**8 / omega                 # rest-frame wavelength with da/a added
    wshift = wshift*(1+zabs)               # observed wavelength with da/a added
    print('---------------------------')
    print('    MgII 2796')
    print('---------------------------')
    print('  domega = %.2f 1/A'%((10**8/wshift-10**8/wobs)/10**-2))
    print(' dlambda = %.2f A'%((wshift-wobs)/10**-3))
    print('      dv = %.3f km/s'%((wshift-wobs)/wobs*args.c))
    # Do calculations
    zabs      = 1
    slope     = 0.2
    wrest1,q1 = 2026.1376450, 1584.
    wobs1     = wrest1*(1+zabs)
    dv1       = slope*(wobs1-5720.)
    wshifted1 = wobs1*(1+dv1/args.c)
    daoa1     = -1/2*dv1/1000/args.c*10**8/wobs1/q1
    print('---------------------------')
    print('    ZnII 2026')
    print('---------------------------')
    print('       q = %i'%q1)
    print('   wrest = %.3f A'%wrest1)
    print('    wobs = %.3f A'%wobs1)
    print('   shift = %i m/s'%dv1)
    print('   wdist = %.3f A'%wshifted1)
    print('   alpha = %.2E'%daoa1)
    wrest2,q2 = 2066.1638990, -1360.
    wobs2     = wrest2*(1+zabs)
    dv2       = slope*(wobs2-5720.)
    wshifted2 = wobs2*(1+dv2/args.c)
    daoa2     = -1/2*dv2/1000/args.c*10**8/wobs2/q2
    print('---------------------------')
    print('    CrII 2066')
    print('---------------------------')
    print('       q = %i'%q2)
    print('   wrest = %.3f A'%wrest2)
    print('    wobs = %.3f A'%wobs2)
    print('   shift = %i m/s'%dv2)
    print('   wdist = %.3f A'%wshifted2)
    print('   alpha = %.2E A'%daoa2)
    dq    = abs(q2-q1)
    ddv   = abs(dv2-dv1)
    mean  = (wrest1+wrest2)/2.
    ddaoa = ((1-10**8/mean*ddv/1000/dq/args.c)**0.5-1)/1E-6    
    print('---------------------------')
    print('   ZnII 2026 - CrII 2066')
    print('---------------------------')
    print('   wmean = %.3f A'%mean)        # mean wavelength
    print('      dq = %i'%dq)              # q contrast
    print('      dv = %i m/s'%ddv)         # corresponding velocity shift
    print('   sigma = %.3f ppm'%ddaoa)     # estimated error
    print('---------------------------')
