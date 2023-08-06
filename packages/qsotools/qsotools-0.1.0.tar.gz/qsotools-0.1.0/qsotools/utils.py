import quasar,os,sys,math,numpy
#from mpl_toolkits.basemap import Basemap
from astropy.io import fits

def spherical_distance(lon1,lat1,lon2,lat2):
    '''
    Calculate distance
    '''
    theta1   = lon1*math.pi/180
    phi1     = math.pi/2-lat1*math.pi/180
    x1       = math.sin(phi1)*math.cos(theta1)
    y1       = math.sin(phi1)*math.sin(theta1)
    z1       = math.cos(phi1)
    theta2   = lon2*math.pi/180
    phi2     = math.pi/2-lat2*math.pi/180
    x2       = math.sin(phi2)*math.cos(theta2)
    y2       = math.sin(phi2)*math.sin(theta2)
    z2       = math.cos(phi2)
    distance = math.acos(x1*x2+y1*y2+z1*z2)
    distance = distance*180/math.pi
    return distance

def get_data(spectrum):
    '''
    Read spectrum file and store data.
    '''
    data = type('v', (), {})()
    datatype = spectrum.split('/')[-1].split('.')[-1]
    z = mo = sky = None
    if datatype=='fits':
        hdu = fits.open(spectrum)
        specformat = 'nothing'
        for i in range (len(hdu[0].header)):
            if ('UVES' in str(hdu[0].header[i])) or ('POPLER' in str(hdu[0].header[i])):
                specformat = 'UVES'
                break
            elif ('Keck' in str(hdu[0].header[i])) or ('HIRES' in str(hdu[0].header[i])):
                specformat = 'HIRES'
                break
            elif 'SDSS' in str(hdu[0].header[i]):
                specformat = 'SDSS'
                break
            elif 'CRIRES' in str(hdu[0].header[i]):
                specformat = 'CRIRES'
                break
        if specformat=='HIRES':
            if os.path.exists(spectrum.replace('.fits','e.fits')):
                hd      = hdu[0].header
                data.wa = 10**(hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+numpy.arange(hd['NAXIS1'])))
                data.fl = hdu[0].data
                hdu     = fits.open(spectrum.replace('.fits','e.fits'))
                data.er = hdu[0].data                
            elif '_f.fits' in spectrum:
                hd      = hdu[0].header
                data.wa = 10**(hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+numpy.arange(hd['NAXIS1'])))
                data.fl = hdu[0].data
                hdu     = fits.open(spectrum.replace('_f.fits','_e.fits'))
                data.er = hdu[0].data                
            elif os.path.exists(spectrum.replace('fits','sig.fits'))==True:
                hd      = hdu[0].header
                data.wa = 10**(hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+numpy.arange(hd['NAXIS1'])))
                data.fl = hdu[0].data
                hdu     = fits.open(spectrum.replace('fits','sig.fits'))
                data.er = hdu[0].data
            else:
                hd      = hdu[0].header
                data.wa = hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+numpy.arange(hd['NAXIS1']))
                data.fl = hdu[0].data[0,:]
                data.er = hdu[0].data[1,:]
        elif specformat=='UVES':
            hd      = hdu[0].header
            data.wa = 10**(hd['CRVAL1'] + hd['CDELT1'] * ((hd['CRPIX1']-1)+numpy.arange(hd['NAXIS1'])))
            data.fl = hdu[0].data[0,:]
            data.er = hdu[0].data[1,:]
        elif specformat=='SDSS':
            hdu0     = hdu[0].header
            hdu1     = hdu[1].header
            z        = float(hdu[2].data['Z'])
            data.wa  = 10.**(hdu0['coeff0'] + hdu0['coeff1'] * numpy.arange(hdu1['naxis2']))
            data.fl  = hdu[1].data['flux']
            data.er  = [1/numpy.sqrt(hdu[1].data['ivar'][i]) if hdu[1].data['ivar'][i]!=0 else 10**32 for i in range (len(data.fl))]
            data.mo  = hdu[1].data['model']
            data.sky = hdu[1].data['sky']
        else:
            print 'Spectrum format not recognized...'
            quit()
    else:
        spec    = numpy.loadtxt(spectrum,dtype='float',comments='!')
        data.wa = spec[:,0]
        data.fl = spec[:,1]
        data.er = spec[:,2]
        if len(spec[0,:])>3:
            data.mo = spec[:,3]
    #badpixel = numpy.append( (numpy.where(abs(er) < 1e-10)[0]) , (numpy.where(abs(er) > 1e+10)[0]))
    #wa = numpy.delete(wa,badpixel,0)
    #fl = numpy.delete(fl,badpixel,0)
    #er = numpy.delete(er,badpixel,0)
    return data
    
def fit_linear(x,y,xmin,xmax,yerr=None):
    '''
    Fir linear curve
    '''
    xfit = numpy.arange(xmin,xmax,0.001)
    if 'numpy' in str(type(yerr)):
        def func(func,a,b):
            return a + b*x
        #pars,cov = curve_fit(func,x,y)
        #self.linslopeval_unweight = pars[1]
        #self.linslopeerr_unweight = numpy.sqrt(cov[1][1])
        #yfit = pars[0] + pars[1]*xfit
        #plot(xfit,yfit,color='blue',ls='dashed',lw=1)
        #print 'Linear slope (unweighted): %.6f+/-%.6f'%(pars[1],numpy.sqrt(cov[1][1]))
        pars,cov = curve_fit(func,x,y,sigma=yerr)
        self.linslopeval = pars[1]
        self.linslopeerr = numpy.sqrt(cov[1][1])
        yfit = pars[0] + pars[1]*xfit
        plot(xfit,yfit,color='red',lw=1)
        self.xfit,self.yfit = xfit,yfit
        print 'Linear slope (weighted): %.6f+/-%.6f'%(pars[1],numpy.sqrt(cov[1][1]))
        self.alphafit = pars[0] + pars[1]*self.xmid
        
    else:
        a,b = polyfit(x,y,1)

def fit_parabola(x,y):
    '''
    Fit the parabola and plot the model
    '''
    A      = numpy.vander(x,3)
    (coeffs, residuals, rank, sing_vals) = numpy.linalg.lstsq(A,y)
    f      = numpy.poly1d(coeffs)
    xfit   = numpy.arange(min(x),max(x),0.001)
    yfit   = f(xfit)
    imid   = abs(yfit-min(yfit)).argmin()
    xmid   = round(xfit[imid],7)
    fmin   = f(xfit[0:imid])
    fmax   = f(xfit[imid:-1])
    xm1sig = round(xfit[abs(fmin-(min(yfit)+1)).argmin()],3) if len(fmin)>0 and max(fmin)>min(yfit)+1 else 0
    xp1sig = round(xfit[imid+abs(fmax-(min(yfit)+1)).argmin()],3) if len(fmax)>0 and max(fmax)>min(yfit)+1 else 0
    plot(xfit,yfit,color='red',lw=1)
    print 'Best Distortion Slope: %.4f+/-%.4f'%(xmid,abs(max(xm1sig,xp1sig)-xmid))
    self.xmid   = xmid
    self.xm1sig = xm1sig
    self.xp1sig = xp1sig
    
def get_atomdat(path=quasar.path,version=quasar.version):
    '''
    Copy requested atom.dat file into given repository.
    '''
    data = os.path.abspath(__file__).rsplit('/', 1)[0] + '/data/'    
    if version==10:
        os.system('cp %s/atom_v%i.dat %s/atom.dat'%(data,version,path))
    
def get_vpsetup():
    '''
    Create vp_setup.dat file from default or user-defined values.

    Examples
    --------
    As executable:

    >>> quasar make_vpsetup --fdzstep 1e-5

    As python script:

    >>> import quasar
    >>> quasar.fdzstep=1e-5
    >>> quasar.verbose=True
    >>> quasar.make_vpsetup()
    '''
    fout = open(quasar.path+'/vp_setup.dat','w')
    fout.write('bvalmax       %s\n'%quasar.bvalmax)
    fout.write('bvalmin       %s\n'%quasar.bvalmin)
    fout.write('bltdrop       %s\n'%quasar.bltdrop)
    fout.write('clogltdrop    %s\n'%quasar.clogltdrop)
    fout.write('bgtdrop       %s\n'%quasar.bgtdrop)
    fout.write('fcollallzn    %s\n'%quasar.fcollallzn)
    fout.write('sigscalemult  %s\n'%quasar.sigscalemult)
    fout.write('date          %s\n'%quasar.date)
    fout.write('dots          %s\n'%quasar.dots)
    fout.write('gcursor       %s\n'%quasar.gcursor)
    fout.write('adsplit       %s\n'%quasar.adsplit)
    fout.write('maxadrem      %s\n'%quasar.maxadrem)
    fout.write('absigp        %s\n'%quasar.absigp)
    fout.write('adcontf       %s\n'%quasar.adcontf)
    fout.write('vform         %s\n'%quasar.vform)
    fout.write('nsubmin       %s\n'%quasar.nsubmin)
    fout.write('nsubmax       %s\n'%quasar.nsubmax)
    fout.write('nfwhmp        %s\n'%quasar.nfwhmp)
    fout.write('pcvals        %s\n'%quasar.pcvals)
    if quasar.verbose:
        fout.write('verbose\n')
    fout.write('chisqthres    %s\n'%quasar.chisqthres)
    fout.write('NOVARS        %s\n'%quasar.novars)
    fout.write('fdbstep       %s\n'%quasar.fdbstep)
    fout.write('fdzstep       %s\n'%quasar.fdzstep)
    fout.write('fdcdstep      %s\n'%quasar.fdcdstep)
    fout.write('fdx4step      %s\n'%quasar.fdx4step)
    fout.close()
'''
class Basemap(Basemap):
    def ellipse(self, x0, y0, a, b, n, ax=None, **kwargs):
        """
        Draws a polygon centered at ``x0, y0``. The polygon approximates an
        ellipse on the surface of the Earth with semi-major-axis ``a`` and 
        semi-minor axis ``b`` degrees longitude and latitude, made up of 
        ``n`` vertices.

        For a description of the properties of ellipsis, please refer to [1].

        The polygon is based upon code written do plot Tissot's indicatrix
        found on the matplotlib mailing list at [2].

        Extra keyword ``ax`` can be used to override the default axis instance.

        Other \**kwargs passed on to matplotlib.patches.Polygon

        RETURNS
            poly : a maptplotlib.patches.Polygon object.

        REFERENCES
            [1] : http://en.wikipedia.org/wiki/Ellipse
        """
        
        ax = kwargs.pop('ax', None) or self._check_ax()
        g = pyproj.Geod(a=self.rmajor, b=self.rminor)
        # Gets forward and back azimuths, plus distances between initial
        # points (x0, y0)
        azf, azb, dist = g.inv([x0, x0], [y0, y0], [x0+a, x0], [y0, y0+b])
        tsid = dist[0] * dist[1] # a * b

        # Initializes list of segments, calculates \del azimuth, and goes on 
        # for every vertex
        seg = [self(x0+a, y0)]
        AZ = numpy.linspace(azf[0], 360. + azf[0], n)
        for i, az in enumerate(AZ):
            # Skips segments along equator (Geod can't handle equatorial arcs).
            if numpy.allclose(0., y0) and (numpy.allclose(90., az) or
                numpy.allclose(270., az)):
                continue

            # In polar coordinates, with the origin at the center of the 
            # ellipse and with the angular coordinate ``az`` measured from the
            # major axis, the ellipse's equation  is [1]:
            #
            #                           a * b
            # r(az) = ------------------------------------------
            #         ((b * cos(az))**2 + (a * sin(az))**2)**0.5
            #
            # Azymuth angle in radial coordinates and corrected for reference
            # angle.
            azr = 2. * numpy.pi / 360. * (az + 90.)
            A = dist[0] * numpy.sin(azr)
            B = dist[1] * numpy.cos(azr)
            r = tsid / (B**2. + A**2.)**0.5
            lon, lat, azb = g.fwd(x0, y0, az, r)
            x, y = self(lon, lat)

0D            # Add segment if it is in the map projection region.
            if x < 1e20 and y < 1e20:
                seg.append((x, y))

        poly = Polygon(seg, **kwargs)
        ax.add_patch(poly)

        # Set axes limits to fit map region.
        self.set_axes_limits(ax=ax)

        return poly

'''
