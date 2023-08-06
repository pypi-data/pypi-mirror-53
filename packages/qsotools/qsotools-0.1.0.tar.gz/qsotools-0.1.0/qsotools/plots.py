import quasar,numpy
import matplotlib.pyplot as plt

def abundances():
    '''
    Primordial abundances vs number of sterile neutrinos
    '''
    rc('font', size=10)
    rc('axes', labelsize=15, linewidth=0.2)
    rc('legend', fontsize=15, handlelength=5)
    rc('xtick', labelsize=10)
    rc('ytick', labelsize=10)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    fig = figure(figsize=(8,10))
    subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.96, hspace=0, wspace=0.05)
    text(1,0.3,'Constraints from observations',fontsize=20,color='#FFFFFF',weight='bold')
    qsolist  = numpy.loadtxt(setup.datapath+'abn.dat')
    plot(qsolist[:,1],qsolist[:,3],'red',lw=1,label=r'$Y_p$')
    plot(qsolist[:,1],qsolist[:,4]*10**4,'black',lw=1,label=r'$10^4 [D/H]_p$')
    plot(qsolist[:,1],qsolist[:,5]*10**9,'orange',lw=1,label=r'$10^9 [^7Li/H]_p$')
    axhspan(0.275, 0.327, facecolor='0.9',lw=0)
    legend(loc='upper right',frameon=False,labelspacing=0.2)
    ylabel("Primordial abundance")
    xlabel(r'$N_S$')    
    savefig('PyD_plot_abundances.pdf')

def alignment():
    '''
    Alignment of several dipoles and antipoles
    '''
    code = Basemap()
    rc('font', size=2, family='serif')
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=7)
    rc('ytick', labelsize=7)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    # List of galactic coordinates
    dipole = numpy.array([[282.00 , 282.00-180 , 11.70 ,   6.00 ,  -6.00 ,  6.00],           # Bulk Flow
                       [320.50 , 320.50-180 , 11.80 , -11.70 ,  11.70 ,  7.50],           # Alpha
                       [309.40 , 309.40-180 , 18.00 , -15.10 ,  15.10 , 11.50],           # Dark Energy from SN1a
                       [331.90 , 331.90-180 ,  7.30 ,  -9.60 ,   9.60 ,  7.30],            # WMAP
                       [307.00 , 307.00-180 ,  5.00 ,   9.00 ,  -9.00 ,  5.00],
                       ],dtype='float')                    
    color  = ['red','blue','green','yellow','purple']
    # Plot whole sky map
    fig = figure(figsize=(11.69,8.27))
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.95, hspace=0, wspace=0)
    m = Basemap(projection='moll',lat_0=0,lon_0=180)
    m.drawparallels(numpy.arange(-90.,90,10.))
    m.drawmeridians(numpy.arange(0,360,20))
    for i in range (len(dipole)):
        m.ellipse(dipole[i,0],dipole[i,3],dipole[i,2]/2,dipole[i,5]/2,100,facecolor=color[i],alpha=0.5,linewidth=0)
        xpt,ypt = m(dipole[i,0],dipole[i,3])
        scatter(xpt,ypt,color='black',edgecolor='none',s=5)
        m.ellipse(dipole[i,1],dipole[i,4],dipole[i,2]/2,dipole[i,5]/2,100,facecolor=color[i],alpha=0.5,linewidth=0)
        xpt,ypt = m(dipole[i,1],dipole[i,4])
        scatter(xpt,ypt,color='black',edgecolor='none',s=10)
    x,y = m(0,0)
    text(x,y,'(0,0)',color='grey',fontsize=10,va='center',ha='right')
    x,y = m(180,-90)
    text(x,y,'(180,-90)',color='grey',fontsize=10,va='top',ha='center')
    x,y = m(180,90)
    text(x,y,'(180,90)',color='grey',fontsize=10,va='bottom',ha='center')
    x,y = m(360,0)
    text(x,y,'(360,0)',color='grey',fontsize=10,va='center',ha='left')
    title('Apparent dipoles alignments\n\n',fontsize=15)
    savefig('PyD_plot_alignment.pdf')
    clf()

def bmass():
    '''
    b squared vs inverse atomic mass
    '''
    def b_square(temp,mass,bturb):
        k         = 1.3806503e-23 * 1e-6
        unit_mato = 1.66053892e-27
        btemp     = 2*k/(numpy.double(mass)*unit_mato)
        btot      = btemp*temp+bturb**2
        return btot
    plt.rc('font', size=2)
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    ax = plt.subplot(111)
    bturb = 5
    ax.yaxis.set_minor_locator(plt.FixedLocator([0,bturb**2],100))
    mass = [1.0079,2.0136,15.9990]
    inv_mass = [1/1.0079,1/2.0136,1/15.9990]
    plt.scatter(inv_mass,b_square(10000,mass,bturb),color='blue',lw=0)
    plt.scatter(inv_mass,b_square(5000,mass,bturb),color='green',lw=0)
    plt.scatter(inv_mass,b_square(3000,mass,bturb),color='red',lw=0)
    inv_mass  = numpy.arange(1e-10,1.1,0.01)
    mass      = 1/inv_mass
    plt.plot(inv_mass,b_square(10000,mass,bturb),label='T = 10,000 K',color='blue')
    plt.plot(inv_mass,b_square(5000,mass,bturb),label='T = 5,000 K',color='green')
    plt.plot(inv_mass,b_square(3000,mass,bturb),label='T = 3,000 K',color='red')
    ax.annotate("",xy=(0.0625,120),xytext=(0.0625,160),arrowprops=dict(fc="#C4C4C4",ec="none"))
    ax.annotate("",xy=(0.4966,170),xytext=(0.4966,210),arrowprops=dict(fc="#C4C4C4",ec="none"))
    ax.annotate("",xy=(0.9922,220),xytext=(0.9922,260),arrowprops=dict(fc="#C4C4C4",ec="none"))
    plt.text(0.0625,170,'OI',color='#C4C4C4',fontsize=17,ha='center',weight='bold')
    plt.text(0.4966,220,'DI',color='#C4C4C4',fontsize=17,ha='center',weight='bold')
    plt.text(0.9922,270,'HI',color='#C4C4C4',fontsize=17,ha='center',weight='bold')
    ax.annotate("",xy=(0,bturb**2),xytext=(0.1,80),arrowprops=dict(arrowstyle="fancy, head_length=2, head_width=1, tail_width=0.8",fc="black",ec="none"))
    plt.text(0.08,85,'$b_{turb}^2='+str(bturb**2)+' (km/s)^2$',color='black',fontsize=10)
    lg = ax.legend(loc=(0.13,0.75),handlelength=2,prop={"size":8})
    fr = lg.get_frame()
    fr.set_lw(0.0)
    plt.axvline(x=1/1.0079,ls='dotted',color='grey',lw=0.2)
    plt.axvline(x=1/2.0136,ls='dotted',color='grey',lw=0.2)
    plt.axvline(x=1/15.9990,ls='dotted',color='grey',lw=0.2)
    plt.xlabel('1/mass in atomic mass units', fontsize=10)
    plt.ylabel('Intrinsic line width b$^2$ in (km/s)$^2$', fontsize=10)
    plt.xlim(0,1.05)
    plt.ylim(0,300)
    plt.savefig('PyD_plot_equivalentwidth.pdf',orientation='landscape',transparent='True')

def candidates():
    '''
    Spherical distance between 2 coordinates
    '''
    rc('font', size=2, family='serif')
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=7)
    rc('ytick', labelsize=7)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    snap    = open(setup.datapath+'candidates.dat', 'r')
    z_arr,col_arr,dop_arr   = [],[],[]
    a,b,c,d = 0,0,0,0
    low,med,high = 0,0,0
    for line in snap:
        linesplit1 = line.split('/')
        linesplit2 = linesplit1[6].split('_')
        z_abs      = linesplit2[1].replace('z=','')
        col        = linesplit2[2].replace('N=','')
        dop        = linesplit2[3].replace('b=','')
        dop        = dop.replace('.jpg','')
        z_arr.append(float(z_abs))
        if (float(z_abs) <= 2.6):
            low = low + 1
        if ((float(z_abs) > 2.6) and (float(z_abs) < 3.4)):
            med = med + 1
        if (float(z_abs) >= 3.4):
            high = high + 1
        col_arr.append(float(col))
        if (float(col) < 16):
            a = a + 1
        if ((float(col) >= 16) and (float(col) < 17)):
            b = b + 1
        if ((float(col) >= 17) and (float(col) < 20)):
            c = c + 1
        if (float(col) >= 20):
            d = d + 1
        dop_arr.append(float(dop))
    locator_params(tight=True, nbins=12)
    ax = subplot(111)
    xlim(13,22)
    ylim([0,150])
    scatter(col_arr,dop_arr,marker='o',c=z_arr,s=6,vmin=2,vmax=4,edgecolors='none')
    axvline(x=16,color='red',lw=0.2)
    axvline(x=17,ls='dotted',color='grey',lw=0.2)
    axvline(x=20,ls='dotted',color='grey',lw=0.2)
    ax.xaxis.set_minor_locator(plt.FixedLocator([500,2000]))
    xlabel("$\log(N_{HI})$  in cm$^{-2}$")
    ylabel("$b$  in km/s")
    ax.annotate("",xy=(14,112),xytext=(16,112),arrowprops=dict(fc="red",ec="none"))
    text(13.3,98,'No direct deuterium'+'\n'+'detection possible',color='red',fontsize=9,weight='bold')
    text(13.3,93,'stacking method needed',color='orange',fontsize=8,style='italic')
    text(14,120,str(a)+' systems',fontsize=7)
    text(16.33,122,str(b),fontsize=7)
    text(16.13,118,'systems',fontsize=7)
    text(18,120,str(c)+' systems',fontsize=7)
    text(20.5,120,str(d)+' systems',fontsize=7)
    text(13.5,130,'Ly-'+r'$\alpha$'+' forest',fontsize=20,color='#C4C4C4',weight='bold')
    text(18,130,'LLS',fontsize=20,color='#C4C4C4',weight='bold')
    text(20.4,130,'DLA',fontsize=20,color='#C4C4C4',weight='bold')
    text(19.75,12.5,'Number of  absorbers\nper redshift range:\n\n\n\n',color='black',fontsize=6.5,
         bbox=dict(facecolor='0.95',lw=.2,color='black',alpha=0.8))
    text(19.8,19,'$'+str('%4.0f'%(float(low)*100./len(z_arr)))+'\%$ at $z\leq2.6$',color='blue',fontsize=7)
    text(19.8,15,'$'+str('%4.0f'%(float(med)*100./len(z_arr)))+'\%$ at $2.6<z<3.4$',color='green',fontsize=7)
    text(19.8,11,'$'+str('%4.0f'%(float(high)*100./len(z_arr)))+'\%$ at $z\geq3.4$',color='red',fontsize=7)
    figtext(.85, 0.5, "$z_{abs}$",rotation='vertical',fontsize=12)
    clim(2,4)
    colorbar()
    savefig('PyD_plot_D2Hcandidates.pdf',orientation='landscape',transparent='True')

def ccdplot():
    '''
    Create 3D plot of CCD FITS file.
    '''
    rc('font', size=2, family='serif')
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=7)
    rc('ytick', labelsize=7)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    arr=fits.open(setup.datapath+'B1obj2066.fits')[0].data
    X = range(1176)
    Y = range(280)
    X, Y = numpy.meshgrid(X, Y)
    Z = arr
    surf = ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3, lw=0)
    cset = ax.contour(X, Y, Z, zdir='z', offset=-400)
    cset = ax.contour(X, Y, Z, 10, zdir='x', offset=-200)
    X = range(1176)
    Ybis = range(8)
    X, Ybis = numpy.meshgrid(X, Ybis)
    Zbis = arr[126:134, :]
    cset = ax.contour(X, Ybis, Zbis, 3, zdir='y', offset=300)
    ax.set_xlabel('Pixeles (columnas)')
    ax.set_xlim(-200, 1200)
    ax.set_ylabel("Pixeles (lineas)")
    ax.set_ylim(0, 300)
    ax.set_zlabel('ADU (cuenta de fotones)')
    ax.set_zlim(-400, 500)
    ax.view_init(30, -25)
    savefig('plot.pdf',transparent='True')

def dtohlist():
    '''
    Plot of most trustworthy D/H measurements in literature
    '''
    name  = ['Q0105+162',
             'Q0349-381  ',
             'Q0913+072',
             'Q1009+299',
             'Q1243+307',
             'Q1558-003  ',
             'Q1937-101  ',
             'Q2206-199  ',
             'Q0407-441  ',
             'Q1358+652',]
    paper = ["O'Meara et al. (2001)",
             "D'Odorico et al. (2001)",
             "Pettini et al. (2008)",
             "Burles & Tytler (1998b)",
             "Kirkman et al. (2003)",
             "O'Meara et al. (2006)",
             "Burles & Tytler (1998a)",
             "Pettini & Bowen (2001)",
             "Noterdaeme et al. (2012)",
             "Cooke et al. (2013)"]
    z_em  = ['2.640','3.222','2.785','2.640','2.558','2.823','3.787','2.559','3.02000','3.19706']
    z_abs = [2.536,3.025,2.618,2.504,2.526,2.703,3.572,2.076,2.62100,3.06726]
    x     = [19.42,20.63,20.34,17.39,19.73,20.67,17.86,20.43,20.45,20.21]
    xerr  = [0.01,0.09,0.04,0.06,0.04,0.05,0.02,0.04,0.10,0.06]
    y     = [-4.6,-4.65,-4.56,-4.4,-4.62,-4.48,-4.48,-4.78,-4.5867,-4.59688]
    yerr  = [0.04,0.05,0.04,0.07,0.05,0.06,0.04,0.09,0.0259,0.00692]
    bary  = log(2.67/(10**5*10**double(y))*6**1.6)/log(1.6)/273.9
    rc('font', size=2, family='serif')
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=7)
    rc('ytick', labelsize=7)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    subplot(111)
    errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o',ms=0,c='black')
    scatter(x,y,c=z_abs,s=100,vmin=2,vmax=4,edgecolors='none')
    xlabel("log HI column density in cm$^{-2}$")
    ylabel("$\log(D/H)$")
    xlim(16,22)
    ylim(-5,-4.2)
    text(16.7,-4.67,"  1  -  "+name[3]+"   "+paper[3],fontsize=6)
    text(16.7,-4.70,"  2  -  "+name[6]+"   "+paper[6],fontsize=6)
    text(16.7,-4.73,"  3  -  "+name[0]+"   "+paper[0],fontsize=6)
    text(16.7,-4.76,"  4  -  "+name[4]+"   "+paper[4],fontsize=6)
    text(16.7,-4.79,"  5  -  "+name[2]+"   "+paper[2],fontsize=6)
    text(16.7,-4.82,"  6  -  "+name[7]+"   "+paper[7],fontsize=6)
    text(16.7,-4.85,"  7  -  "+name[1]+"   "+paper[1],fontsize=6)
    text(16.7,-4.88,"  8  -  "+name[5]+"   "+paper[5],fontsize=6)
    text(16.7,-4.91,"  9  -  "+name[8]+"   "+paper[8],fontsize=6)
    text(16.7,-4.94,"10  -  "+name[9]+"   "+paper[9],fontsize=6)
    text(17.51,-4.39,"1",fontsize=6,color='grey')
    text(18,-4.47,"2",fontsize=6,color='grey')
    text(19.2,-4.62,"3",fontsize=6,color='grey')
    text(19.8,-4.65,"4",fontsize=6,color='grey')
    text(20.1,-4.57,"5",fontsize=6,color='grey')
    text(20.52,-4.77,"6",fontsize=6,color='grey')
    text(20.73,-4.63,"7",fontsize=6,color='grey')
    text(20.8,-4.47,"8",fontsize=6,color='grey')
    text(20.5,-4.57,"9",fontsize=6,color='grey')
    text(20.0,-4.61,"10",fontsize=6,color='grey')
    axhline(y=-4.515, ls='dotted',color='black',lw=0.2)
    axhline(y=-4.55,color='black',lw=0.2)
    axhline(y=-4.585, ls='dotted',color='black',lw=0.2)
    clim(2,3.6)
    colorbar()
    figtext(.85, 0.55, '$z_{abs}$',rotation='vertical',fontsize=12)
    annotate("",xy=(21.5,-4.515),xytext=(21.5,-4.42),arrowprops=dict(fc="grey",ec="none",arrowstyle="fancy, head_length=2, head_width=1, tail_width=0.8"))
    annotate("",xy=(21.5,-4.585),xytext=(21.5,-4.68),arrowprops=dict(fc="grey",ec="none",arrowstyle="fancy, head_length=2, head_width=1, tail_width=0.8"))
    text(21.445,-4.7, 'Planck $2$'+r'$\sigma$'+' limit',rotation='vertical',color='grey',fontsize=8)
    savefig('PyD_plot_D2Hmeasurements.pdf',orientation='landscape',transparent='True')

def flatlinear():
    '''
    Plot linearity plot between 2 flat field frames
    '''
    hdu   = fits.open('HI.20041105.5s3os.fits')
    hd    = hdu[0].header
    t1    = float(5)#float(hd['EXPTIME'])
    ccd1  = hdu[0].data[:]
    pix1a = ccd1.ravel()
    pix1b = numpy.array([i for i in numpy.arange(1,len(ccd1[0])+1)]*len(ccd1))
    pix1c = numpy.array([[i]*len(ccd1[0]) for i in numpy.arange(1,len(ccd1)+1)]).ravel()
    pix1  = numpy.vstack((pix1a,pix1b,pix1c)).T
    print 'First flat,',t1,'seconds,',len(pix1),'pixels, min',min(pix1[:,0]),', max',max(pix1[:,0])
    
    hdu  = fits.open('HI.20041105.40s3os.fits')
    hd   = hdu[0].header
    t2   = float(40)#float(hd['EXPTIME'])
    ccd2 = hdu[0].data[:]
    pix2a = ccd2.ravel()
    pix2b = numpy.array([i for i in numpy.arange(1,len(ccd2[0])+1)]*len(ccd2))
    pix2c = numpy.array([[i]*len(ccd2[0]) for i in numpy.arange(1,len(ccd2)+1)]).ravel()
    pix2 = numpy.vstack((pix2a,pix2b,pix2c)).T
    print 'Second flat,',t2,'seconds,',len(pix2),'pixels, min',min(pix2[:,0]),', max',max(pix2[:,0])

#    for i in range(len(pix1)):
#        print '{0:>10} {1:>5} {2:>10} {3:>5} {4:>10} {5:>10}'.format('%.3f'%pix1[i],'%i'%t1,'%.3f'%pix2[i],'%i'%t2,'%.3f'%(pix1[i]-(t1/t2)*pix2[i]),'%.3f'%(pix2[i]-(t2/t1)*pix1[i]))

    binning = 50
    
    i = numpy.where(pix1[:,2]%binning==0)[0]
    x1 = numpy.array(pix1[i,0])
    
    i = numpy.where(pix2[:,2]%binning==0)[0]
    x2 = numpy.array(pix2[i,0])
    
    y1 = x1 - (t1/t2) * x2
    y2 = x2 - (t2/t1) * x1

#    x1,x2,binning = [],[],1.
#    for i in numpy.arange(0,len(pix1)-binning,binning):
#        print '{0:>5} {1:>5} {2:>5} {3:>5} {4:>5} {5:>5} {6:>10}'.format('%i'%pix1a[i],'%i'%pix1b[i],'%i'%pix1c[i],'%i'%pix2a[i],'%i'%pix2b[i],'%i'%pix2c[i],'%.3f'%(pix1a[i]-(t1/t2)*pix2a[i]))
#        if i==binning*11:
#            quit()
#        x1.append(pix1[i,0])
#        x2.append(pix2[i,0])
#        print i
#    quit()
#    x1 = pix1[:,0]
#    x2 = pix2[:,0]

    print 'Show data...'

    rc('font', size=5, family='serif')
    rc('axes', labelsize=12, linewidth=1)
    rc('legend', fontsize=12, handlelength=10)
    rc('xtick', labelsize=12)
    rc('ytick', labelsize=12)
    rc('lines', lw=1, mew=0.2)
    rc('grid', linewidth=0.2)
    
    fig = figure(figsize=(8,12))
    subplots_adjust(left=0.17, right=0.95, bottom=0.15, top=0.95, hspace=0.2, wspace=0.)
    
    ax = subplot(111)
    ax.scatter(x1,y1,color='black',s=2,alpha=0.5)
#    ax.set_xscale('log')
    grid()
    xlabel(r'f$_e$(%is) [e$^-$]'%t1)
    ylabel(r'dL$_\mathrm{%i-%i}$ = f$_e$(%is)$-$f$_e$(%is)$\times$%i/%i [e$^-$]'%(t1,t2,t1,t2,t1,t2))

#    ax = subplot(212)
#    ax.scatter(x2,y2,color='black',s=2,alpha=0.5)
#    ax.set_xscale('log')
#    grid()
#    xlabel(r'f$_e$(%is) [e$^-$]'%t2)
#    ylabel(r'dL$_\mathrm{%i-%i}$ = f$_e$(%is)$-$f$_e$(%is)$\times$%i/%i [e$^-$]'%(t2,t1,t2,t1,t2,t1))

    savefig('diff.pdf')
    
def forest():
    '''
    Relative number of Lyman systems vs HI column density
    '''
    rc('font', size=2)
    rc('axes', labelsize=10, linewidth=1)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=8)
    rc('ytick', labelsize=8)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    locator_params(tight=True, nbins=12)
    ax = subplot(111)
    col  = numpy.arange(12,22,0.01)
    num  = 4.9*10**7 * (10**(col))**(-1.46)
    loglog(10**(col),num,lw=1)
    xlabel("HI column density in cm$^{-2}$")
    ylabel("Relative Number")
    axvline(x=10**(17), ymin=0, ymax=1, ls='dashed',color='black',lw='1')
    axvline(x=10**(20.3), ymin=0, ymax=1, ls='dashed',color='black',lw='1')
    annotate('', xy=(10**(15.8), 10**(-15.6)),  xycoords='data',
                    xytext=(-50, -50), textcoords='offset points',
                    size=20,
                    #bbox=dict(boxstyle="round", fc="0.8"),
                    arrowprops=dict(arrowstyle="fancy",
                                    fc="0.6", ec="none",
                                    connectionstyle="arc3,rad=-0.3"),
                    )
    ax.xaxis.set_minor_locator(plt.FixedLocator([50,500,2000]))
    ax.yaxis.set_minor_locator(plt.FixedLocator([50,500,2000]))
    text(10**(13.5),10**(-18.2),'Number per unit redshift',fontsize=9)
    text(10**(13.5),10**(-18.7),'per unit HI column density',fontsize=9)
    text(10**(14),10**(-11),'Lyman-'+r'$\alpha$'+' forest',fontsize=13)
    text(10**(18.2),10**(-11),'LLS',fontsize=13)
    text(10**(20.7),10**(-11),'DLA',fontsize=13)
    savefig('PyD_plot_lyforestdistrib.pdf',orientation='landscape',transparent='True')

def growth():
    '''
    Equivalent width vs HI column density
    '''
    rc('font', size=2)
    rc('axes', labelsize=10, linewidth=1)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=8)
    rc('ytick', labelsize=8)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    locator_params(tight=True, nbins=12)
    ax = subplot(111)
    col   = numpy.arange(12,22,0.2)
    dop   = [15,25,55,95]
    color = ['green','black','blue','red']
    i     = 0
    while (i < len(dop)):
        equi_width  = []
        k = 0
        while (k < len(col)):
            ref     = 1215.67
            wave    = numpy.arange(ref-65,ref+65,0.0002)
            flux    = setup.p_voigt(col[k],dop[i],wave,1215.67,6.2650e+08,0.41640)
            center  = int(len(wave)/2)
            idx_min = center
            idx_max = center 
            j       = 0
            area1   = 0
            while (j < center-1):
                area1 = area1 + (wave[idx_min]-wave[idx_min-1])*(1-flux[idx_min]) + (wave[idx_max+1]-wave[idx_max])*(1-flux[idx_max])
                idx_min = idx_min - 1
                idx_max = idx_max + 1
                j = j + 1
            idx_min = center
            idx_max = center
            area2   = 0
            while (area2 < area1):
                area2   = wave[idx_max] - wave[idx_min]
                idx_min = idx_min - 1
                idx_max = idx_max + 1
            equi_width.append(area2)
            print col[k],area2
            k = k + 1
        loglog(10**col,equi_width,color=color[i],lw=1,label='b = '+str(dop[i])+' km/s')
        i = i + 1
    axvline(x=10**(17), ymin=0, ymax=1, ls='dashed',color='black',lw='1')
    axvline(x=10**(20.3), ymin=0, ymax=1, ls='dashed',color='black',lw='1')
    lg = legend(loc=(0.23,0.15),handlelength=2,prop={"size":8})
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    ax.xaxis.set_minor_locator(plt.FixedLocator([500,2000]))
    ax.yaxis.set_minor_locator(plt.FixedLocator([500,2000]))
    xlabel("HI column density in cm$^{-2}$")
    ylabel("Equivalent width in $\AA$")
    text(10**(13.5),8,'Lyman-'+r'$\alpha$'+' forest',fontsize=10)
    text(10**(18.2),8,'LLS',fontsize=10)
    text(10**(20.7),8,'DLA',fontsize=10)
    text(10**(12.3),0.01,'A',fontsize=14,weight='bold')
    text(10**(16),0.7,'B',fontsize=14,weight='bold')
    text(10**(21),20,'C',fontsize=14,weight='bold')
    savefig('PyD_plot_curveofgrowth.pdf',orientation='landscape',transparent='True')

def ionisation():
    '''
    Ionisation potentials for different species
    '''
    table = numpy.array([['1' ,'H' ,13.598434005136],
                      ['1' ,'D' ,13.602134041842],
                      ['1' ,'T' ,13.603365124],
                      [ '6','C' ,11.2602960,24.384500,47.88778, 64.49358,392.0905,489.993177],
                      [ '8','O' ,13.6180540,35.121110,54.93554, 77.41350,113.8990,138.118900],#,739.32678,871.40983],
                      ['12','Mg', 7.6462350,15.035267,80.14360,109.26500,141.3300,186.760000],#,225.02000,265.92400,327.99,367.489,1761.80478,1962.66350],
                      ['13','Al', 5.9857680,18.828550,28.44764,119.99200,153.8250,190.490000],#,241.76000,284.64000,330.21,398.650,442.00500,2085.97689,2304.13990],
                      ['14','Si', 8.1516830,16.345850,33.49300, 45.14179,166.7670,205.267000],#,246.32000,303.66000,351.10,401.380,476.18000, 523.41500,2437.65804,2673.1774],
                      ['16','S' ,10.3600100,23.337880,34.86000, 47.22200, 72.5945, 88.052900],#,280.95400,328.79400,379.84],
                      ['22','Ti', 6.8281200,13.575500,27.49171, 43.26717, 99.2990,119.530000],#,140.68000,170.50000,192.10,215.920,265.07000, 291.50000, 787.67000, 864.0000, 944.500,1042,1130,1220.0,1346.3,1425.257,6249.0222,6625.8069],
                      ['24','Cr', 6.7665100,16.485700,30.95900, 49.16000, 69.4600, 90.634900],#,160.29000,184.76000,209.54,244.500,270.80000, 296.70000, 354.66000, 384.1630,1012.000,1097,1188,1294.8,1394.5,1495.100,1634.1000,1721.1830,7481.8623,7894.7987],
                      ['25','Mn', 7.4340180,15.639990,33.66800, 51.20000, 72.4100, 95.604000],#,119.20000,195.50000,221.89,248.640,286.10000, 314.40000, 343.60000, 402.9500, 435.172,1134,1224,1320.3,1430.9,1537.200,1643.2000,1788.7000,1879.8730,8140.7867,8571.9483],
                      ['26','Fe', 7.9024678,16.199200,30.65100, 54.91000, 75.0000, 98.985000],#,124.98000,151.06000,233.60,262.100,290.90000],
                      ['28','Ni', 7.6398770,18.168837,35.18700, 54.92000, 76.0600,108.000000],#,132.00000,162.00000,193.20,224.700],
                      ['30','Zn', 9.3941990,17.964390,39.72330, 59.57300, 82.6000,108.000000]])#,133.90000,173.90000,203.00]]
    
    romlet = ['I','II','III','IV','V','VI']#,'VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXIII','XXIV','XXV']
    
    fig = figure(figsize=(12,8))
    subplots_adjust(left=0.07, right=0.95, bottom=0.1, top=0.96, hspace=0, wspace=0.05)
    ypos,yname = [],[]
    ax = subplot(111,ylim=[-1,len(table)],xlim=[4,700])
    for j in range (len(table)):
        x = [float(i) for i in table[j][2:]]
        y = [j]*(len(table[j])-2)
        #axhline(y=j,color='gray',ls='dotted',lw=.2)
        semilogx(x,y,marker='o',mec='none',ms=5)
        for k in range (len(x)):
            val = 0.25# if k%2==0 else -0.2
            text(x[k],j+val,romlet[k],ha='center',va='center',fontsize=10)
        ypos.append(j)
        yname.append('$_{'+table[j][0]+'}$'+table[j][1])
    #ax.set_xscale('log')
    grid(b=True, which='major',lw=1)
    grid(b=True, which='minor')
    xlabel('Ionization Energy (eV)',fontsize=14)
    ylabel('Species',fontsize=14)
    yticks(ypos,yname)
    savefig('ionisation.pdf')

def qplot():
    '''
    Plot q-coefficient as a function of rest-wavelength
    '''
    rc('font', size=10)
    rc('axes', labelsize=15, linewidth=0.2)
    rc('legend', fontsize=15, handlelength=5)
    rc('xtick', labelsize=10)
    rc('ytick', labelsize=10)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    
    fig = figure(figsize=(8,5))
    subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.96, hspace=0, wspace=0)
    xlist = [float(i) for i in setup.qlistfev[:,1]]
    ylist = [float(i) for i in setup.qlistfev[:,2]]
    scatter(xlist,ylist,color='black')
    xlabel('rest-wavelength')
    ylabel('q-coefficient')
    savefig('qlistfev.pdf')

    fig = figure(figsize=(8,5))
    subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.96, hspace=0, wspace=0)
    cmap  = plt.get_cmap('jet')
    names = [str(i) for i in setup.qlistall[:,0]]
    color = cmap(numpy.linspace(0, 1, len(names)))
    xlist = [float(i) for i in setup.qlistall[:,1]]
    ylist = [float(i) for i in setup.qlistall[:,2]]
    scatter(xlist,ylist,color=color)
    legend(loc='upper right',frameon=False,labelspacing=0.2)
    xlabel('rest-wavelength')
    ylabel('q-coefficient')
    savefig('qlistall.pdf')
    
def zhist():
    '''
    Redshift histogram of UVES quasars
    '''
    rc('font', size=2)
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=7)
    rc('ytick', labelsize=7)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    fig = figure(figsize=(8,3))
    ax = subplot(111)
    opfile2 = open('/Users/vincent/pymod/masfig/input/list_z.dat', 'r')
    qso_name,qso_z = [],[]
    for line in opfile2:
        linesplit  = line.split()
    #    name       = linesplit[0]+linesplit[1]+linesplit[2]+linesplit[3]+linesplit[4]+linesplit[5]
        redshift   = linesplit[1]
     #   qso_name.append(qso_name)
        qso_z.append(float(redshift))
    opfile1    = open('/Users/vincent/pymod/masfig/input/values.dat', 'r')
    abs_name,abs_z,abs_col,abs_dop = [],[],[],[]
    for line in opfile1:
        linesplit1 = line.split('/')
        linesplit2 = linesplit1[3].split('_')
        name       = linesplit2[0].replace('J','')
        name       = name.replace('.dat','')
        z_abs      = linesplit2[1].replace('z=','')
        col        = linesplit2[2].replace('N=','')
        dop        = linesplit2[3].replace('b=','')
        dop        = dop.replace('.jpg\n','')
        abs_name.append(name)
        abs_z.append(float(z_abs))
        abs_col.append(float(col))
        abs_dop.append(float(dop))
    print max(qso_z)
    subplot(111)
    axvline(x=1.6, ymin=0, ymax=1,color='red',lw=2,ls='dashed')
    #axvspan(xmin=0.6, xmax=1.4, ymin=0, ymax=1, facecolor='0.9',lw=0)
    #axvspan(xmin=2.2, xmax=2.9, ymin=0, ymax=1, facecolor='0.9',lw=0)
    xlabel("Redshift")
    hist(qso_z,70,cumulative=False,color='blue',histtype='step')
    ax.xaxis.set_major_locator(plt.FixedLocator([0,1,1.6,2,3,4,5,6]))
    xlim(xmax=6.4)
    ylim(ymax=23)
    text(1.7,19,'Atmospheric cut-off for Ly-'+r'$\alpha$',color='red',fontsize=11)
    savefig('pthist.pdf')
    clf()
    
