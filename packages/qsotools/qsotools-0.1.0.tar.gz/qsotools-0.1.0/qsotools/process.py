from .settings import *

class aiptalk(object):
    '''
    Plots for AIP Postgraduate Award talk at UNSW
    '''
    def __init__(self):
        #os.system('cd ./ && convert -delay 5 -density 170 -loop 0 0001*.pdf 0002*.pdf 0003*.pdf results3.gif')
        #quit()
        rc('font', size=2, family='serif')
        rc('axes', labelsize=8, linewidth=0.2)
        rc('legend', fontsize=2, handlelength=10)
        rc('xtick', labelsize=6)
        rc('ytick', labelsize=6)
        rc('lines', lw=0.2, mew=0.2)
        rc('grid', linewidth=0.2)
        setup.atom = np.loadtxt(setup.datapath+'atomlist.dat',dtype='str',comments='!')
        self.createlist()
        fortlist = np.loadtxt('fortlist.dat',dtype='str')
        h = 0
        for i in range (len(fortlist)):
            header   = fortlist[i,0]+'/original/header.dat'
            os.environ['ATOMDIR']  = setup.datapath+'atom_v10.dat'
            os.environ['VPFSETUP'] = setup.datapath+'vp_setup_v10.dat'
            readfort13(fortlist[i,0],header)
            createchunks('fort.13')
            i = 0
            while (i<len(setup.table1)):
                if np.average(np.loadtxt('chunks/vpfit_chunk'+'%03d'%(i+1)+'.txt',comments='!')[:,3])!=1:
                    fig = figure(facecolor='black')
                    #axis('off')
                    #subplots_adjust(left=0.1, right=0.9, bottom=0.06, top=0.96, wspace=0, hspace=0)
                    ax = fig.add_subplot(111,xlim=[-setup.dv,setup.dv],ylim=[-0.6,2.1])
                    ax.spines['bottom'].set_color('white')
                    ax.spines['top'].set_color('white')
                    ax.xaxis.label.set_color('white')
                    ax.tick_params(axis='x', colors='white')
                    ax.spines['left'].set_color('white')
                    ax.spines['right'].set_color('white')
                    ax.yaxis.label.set_color('white')
                    ax.tick_params(axis='y', colors='white')
                    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
                    ax.set_xlabel('Velocity relative to $z_{abs}$ (km/s)',fontsize=10)
                    readspec(i)
                    checkshift(i)
                    plotfit(i)
                    savefig('%04d'%h+'.pdf',facecolor=fig.get_facecolor(),transparent=True)
                    h = h + 1
                i = i + 1
            os.system('rm -rf fort.13 data')

    def createlist(self):
    
        keck    = ['HIRES_jaiswal','HIRES_murphy_A','HIRES_murphy_B1','HIRES_murphy_B2','HIRES_murphy_C']
        vlt     = ['UVES_dumont','UVES_jaiswal','UVES_king','UVES_valdenaire']
        fitdir  = '/Users/vincent/ASTRO/analysis/alpha/systems/'
        publist = np.loadtxt(setup.datapath+'published.dat',dtype='str',comments='!')
        os.system('ls '+fitdir+'*/* > list')
        allsys = np.loadtxt('list',dtype='str')
        outfile = open('fortlist.dat','w')
        for line in allsys:
            if ':' in line:
                sample  = line.split('/')[-2]
                quasar  = line.split('/')[-1].replace(':','')
                syspath = line.replace(':','/')
            elif 'data' not in line and sample+'/'+quasar+'/'+line in publist[:,0]:
                outfile.write(syspath+line+'\t'+sample+'\t'+quasar+'\t'+line+'\n')
        outfile.close()
        os.system('rm list')
        
    def atominfo(atomID):     # Get atomic data from selected atomID
    
        if len(np.where(setup.atom[:,7]==atomID)[0])==0:
            print atomID,'not in atom.dat!'
            quit()
        k = np.where(setup.atom[:,7]==atomID)[0][0]
        element     = setup.atom[k,0]
        wavelength  = setup.atom[k,1]
        oscillator  = setup.atom[k,2]
        gammavalue  = setup.atom[k,3]
        atomicmass  = setup.atom[k,5]
        qcoeff      = setup.atom[k,5]
        qcoeff_err  = setup.atom[k,6]
    
        return [element,wavelength,oscillator,gammavalue,qcoeff,qcoeff_err]
    
    def p_voigt(n,b,wave,lambdao,gamma,f):
        
        c = 299792458.
        b = (b+0) * 1000
        nn = float(10**n)
        u = (c/b)*(lambdao/wave-1)
        wave=wave*(10**(-10))
        lambdao=lambdao*10**(-10)
        a=lambdao*gamma/(4*pi*b)
        H=voigt(a,u)
        tau=0
        wave=(wave*10**(10))    # in Angstrom
        b=(b/1000)              # in km/s
        tau=(1.497*10**(-15)*nn*f*wave*H/b)
        lambdao=(lambdao*10**(10))
        return np.exp(-tau)
    
    def readfort13(fortrep,header):
    
        fort = open(fortrep+'/fort.13','r')
        line13 = []
        for line in fort:
            if len(line.split())==0: break
            elif line[0]!='!': line13.append(line.replace('\n',''))
        # Prepare table1, initialise atomic header array, and get mid redshift of the system
        headlist = np.loadtxt(header,dtype='str',comments='!',delimiter='\n') if header!='headinfort' else None
        # [element,wavelength,oscillator,gammavalue,qcoeff,qcoeff_err]
        setup.header  = np.empty((0,6))
        # [headerline,comment,wamid]
        setup.comment = np.empty((0,3))
        setup.table1  = []
        i = 1
        while line13[i].split()[0]!='*':
            l = line13[i].split()
            print fortrep
            if '../' in l[0]:
                os.system('ln -s '+fortrep+'/../data/ ./data')
                os.system('sed s,../,, '+fortrep+'/fort.13 > fort.13')
            else:
                os.system('ln -s '+fortrep+'/data/ ./data')
                os.system('cp '+fortrep+'/fort.13 fort.13')
            headinfo = line13[i].split('!')[-1] if header=='headinfort' else headlist[i-1]
            setup.header  = np.vstack([setup.header,atominfo(headinfo.split()[0])])
            setup.comment = np.vstack([setup.comment,[headinfo,'-',0]])
            setup.table1.append([l[0].replace('../',''),                   # filename
                                float(l[1]),                              # position
                                float(l[2]),                              # lambinit
                                float(l[3]),                              # lambfina
                                float(l[4].split('=')[1].split('!')[0])]) # sigvalue
            i=i+1
        self.getzmid()
        self.getdv()
        setup.dv = 150 if setup.dv<150 else setup.dv
        # Prepare table2 listing all the components
        setup.table2 = []
        i=i+1
        p = 1
        while i<len(line13):
            l = line13[i].split()
            s = line13[i].split('!')
            # If the species is 1 letter (H,C,S) and fort.13 DOES have varying alpha column
            if len(l[0])==1 and len(s[0].split())==9:
                # metalref / coldensit / redshift / dopparam / transind / numbcomp
                setup.table2.append([l[0]+l[1],l[2],l[3],l[4],float(l[8]),p])
            # If the species is 1 letter (H,C,S) and fort.13 has NO varying alpha column      
            if len(l[0])==1 and len(s[0].split())==8:
                # metalref / coldensit / redshift / dopparam / transind / numbcomp
                setup.table2.append([l[0]+l[1],l[2],l[3],l[4],float(l[7]),p])
            # If the species is 2 letters (Al,Mg,Fe) and fort.13 DOES have varying alpha column
            if len(l[0])>1  and len(s[0].split())==8:
                # metalref / coldensit / redshift / dopparam / transind / numbcomp
                setup.table2.append([l[0],l[1],l[2],l[3],float(l[7]),p])
            # If the species is 2 letters (Al,Mg,Fe) and fort.13 has NO varying alpha column      
            if len(l[0])>1  and len(s[0].split())==7:
                # metalref / coldensit / redshift / dopparam / transind / numbcomp
                setup.table2.append([l[0],l[1],l[2],l[3],float(l[6]),p])
            i=i+1
            p=p+1
                    
    def createchunks(fortfile):
        
        opfile = open('fitcommands','w')
        initialise = '\ny\nas\n\n\n' if len(setup.table1)==1 else '\ny\n\nas\n\n\n'
        opfile.write('d\n\n\n'+fortfile+initialise)
        for i in range (1,len(setup.table1)):
            opfile.write('\n\n\n\n')
            i=i+1
        opfile.write('n\nn\n')
        opfile.close()
        os.system('vpfit < fitcommands')
        
        if os.path.exists('chunks')==False:
            os.system('mkdir chunks')
        os.system('mv vpfit_chunk* chunks/')
    
    def readspec(i):
    
        specfile = setup.table1[i][0]
        datatype = specfile.split('.')[-1]
        if datatype == 'fits':
            fh = fits.open(specfile)
            hd = fh[0].header
            d  = fh[0].data
            if ('CTYPE1' in hd and hd['CTYPE1'] in ['LAMBDA','LINEAR']) or ('DC-FLAG' in hd and hd['DC-FLAG']=='0'):
                setup.wa = hd['CRVAL1'] + (hd['CRPIX1'] - 1 + np.arange(hd['NAXIS1']))*hd['CDELT1']
            else:
                setup.wa = 10**(hd['CRVAL1'] + (hd['CRPIX1'] - 1 + np.arange(hd['NAXIS1']))*hd['CDELT1'])
            if len(d.shape)==1:
                setup.fl = d[:]
            else:
                setup.fl = d[0,:]
        else:
            os.system('sed s/,// '+specfile+' > spec.dat')
            d = np.loadtxt('spec.dat',comments='!')
            setup.wa = d[:,0]
            setup.fl = d[:,1]
    
    def checkshift(i):
    
        setup.shift,setup.cont,setup.zero = 0,1,0
        # Read all fit results and create Voigt profile models
        for j in range(0,len(setup.table2)):
            z = float(re.compile(r'[^\d.-]+').sub('',setup.table2[j][2]))
            N = float(re.compile(r'[^\d.-]+').sub('',setup.table2[j][1]))
            b = float(re.compile(r'[^\d.-]+').sub('',setup.table2[j][3]))
            if setup.table2[j][0]==">>" and (setup.table2[j][4]==i+1 or \
                                             (setup.table2[j][4]==0 and \
                                              setup.table1[i][2]<1215.6701*(z+1)<setup.table1[i][3])):
                # text(-.5*setup.dv,-.43,'>> '+str(b)+' km/s',color='blue',fontsize=5)
                setup.shift = -b
            if setup.table2[j][0]=="<>" and (setup.table2[j][4]==i+1 or \
                                             (setup.table2[j][4]==0 and \
                                              setup.table1[i][2]<1215.6701*(z+1)<setup.table1[i][3])):
                # text(-.5*setup.dv,-.28,'<> '+str(N),color='blue',fontsize=5)
                setup.cont = 1./N
            if setup.table2[j][0]=="__" and (setup.table2[j][4]==i+1 or \
                                             (setup.table2[j][4]==0 and \
                                              setup.table1[i][2]<1215.6701*(z+1)<setup.table1[i][3])):
                # text(-.3*setup.dv,-.28,'__ '+str(N),color='blue',fontsize=5)
                setup.zero = -N
    
    def plotfit(i):
                    
        print setup.header[i,0],setup.header[i,1],setup.table1[i][0],'chunks/vpfit_chunk'+'%03d'%(i+1)
    
        pos  = abs(setup.wa-(setup.table1[i][2]+setup.table1[i][3])/2).argmin()
        pix1 = setup.wa[pos]
        pix2 = (setup.wa[pos]+setup.wa[pos-1])/2
        dempix = 2*(pix1-pix2)/(pix1+pix2)*setup.c
        # Plot data
        wamid = float(setup.comment[i,2])
        pos   = abs(setup.wa-wamid).argmin()
        vel   = 2*(setup.wa-wamid)/(setup.wa+wamid)*setup.c
        plot(vel+setup.shift+dempix,setup.fl*setup.cont+setup.zero,drawstyle='steps',lw=0.2,color="white")
        text(-.97*setup.dv,-.4,str(setup.header[i,0])+' '+str('%.2f'%float(setup.header[i,1])),
             color='blue',fontsize=10,horizontalalignment='left')
        #text(.1*setup.dv,-.28,' f = '+str("%.4f"%round(float(setup.header[i,2]),4)),
        #     color='blue',fontsize=5,horizontalalignment='left')
        #text(.1*setup.dv,-.43,'q = '+str(setup.header[i,4])+' $\pm$ '+str(setup.header[i,5]),
        #     color='blue',fontsize=5,horizontalalignment='left')
        #text(.97*setup.dv,-.4,str(i+1)+' - '+str(setup.table1[i][0].split('/')[-1]),
        #     color='blue',fontsize=7,horizontalalignment='right')
        if setup.comment[i,1] != '-':
            text(.97*setup.dv,.3,'Overlapping system:\n'+setup.comment[i,1],
                 color='darkorange',weight='bold',fontsize=6,horizontalalignment='right')
        axhline(y=1,color='black',ls='dotted')
        axhline(y=0,color='black',ls='dotted')
        # Prepare and plot wavelength and velocity array for the model
        spec = np.loadtxt('chunks/vpfit_chunk'+'%03d'%(i+1)+'.txt',comments='!')
        wabeg = abs(spec[:,0]-setup.table1[i][2]).argmin()+1
        waend = abs(spec[:,0]-setup.table1[i][3]).argmin()-1
        wave  = spec[wabeg:waend,0]
        flux  = spec[wabeg:waend,1]
        error = spec[wabeg:waend,2]
        model = spec[wabeg:waend,3]
        vel   = 2*(wave-wamid)/(wave+wamid)*setup.c
        plot(vel+setup.shift,model*setup.cont+setup.zero,lw=1,color="lime")
        plot(vel+dempix+setup.shift,error,lw=.1,drawstyle='steps',color="cyan")
        # Prepare and plot wavelength and velocity array for the residual
        axhline(y=1.6,color='magenta')
        axhline(y=1.7,color='magenta',ls='dotted')
        axhline(y=1.8,color='magenta')
        if '-nores' not in sys.argv:
            res = (flux-model)/error/10+1.7
            plot(vel+dempix+setup.shift,res,lw=0.1,drawstyle='steps',c='magenta')
        val = 1
        wa1 = np.arange(wave[0],wave[-1],0.001)
        vel = 2*(wa1-wamid)/(wa1+wamid)*setup.c
        model = 1
        for k in range(0,len(setup.table2)):
            for p in range(len(setup.atom)):
                z = float(re.compile(r'[^\d.-]+').sub('',setup.table2[k][2]))
                N = float(re.compile(r'[^\d.-]+').sub('',setup.table2[k][1]))
                b = float(re.compile(r'[^\d.-]+').sub('',setup.table2[k][3]))
                cond1 = setup.table2[k][0]==setup.atom[p,0]
                cond2 = setup.table2[k][0] not in ['<>','>>','__','<<']
                cond3 = setup.table1[i][2]-10 < (1+z)*float(setup.atom[p,1]) < setup.table1[i][3]+10
                if cond1 and cond2 and cond3:
                    if '-details' in sys.argv:
                        profile = p_voigt(N,b,wa1/(z+1),float(setup.atom[p,1]),
                                          float(setup.atom[p,3]),float(setup.atom[p,2]))
                        center  = int(len(wa1)/2)
                        dv      = (wa1[center]-wa1[center-1])/((wa1[center]+wa1[center-1])/2)*setup.c
                        vsig    = setup.table1[i][4]/dv
                        profile = gaussian_filter1d(profile,vsig)
                        model   = model*profile
                        plot(vel+setup.shift,profile,lw=0.1,color="orange")
                    lobs  = float(setup.atom[p,1])*(z+1)
                    vobs  = 2*(lobs-wamid)/(lobs+wamid)*setup.c
                    pos   = 1.08 if val%2==0 else 1.25
                    color = 'red' if abs(2*(z-setup.zmid)/(z+setup.zmid)) < 0.01 \
                            else 'purple' if setup.atom[p,0] in ['HI','??'] else 'darkorange'
                    axvline(x=vobs,ls='dotted',color=color,lw=.6)
                    if setup.table2[k][2][-1].isdigit()==True:
                        text(vobs,pos,str(setup.table2[k][-1]),color=color,weight='bold',
                             fontsize=7,horizontalalignment='center')
                    elif setup.table2[k][2][-1].isdigit()==False:
                        text(vobs,pos,str(setup.table2[k][2][-1].upper()),color=color,
                             weight='bold',fontsize=7, horizontalalignment='center')
                    val = val + 1
        if '-details' in sys.argv:
            plot(vel+setup.shift,model,lw=1,color="orange",alpha=.6)            
    
    def getzmid():
        '''
        Calculate mid wavelength for all fitting regions
        '''
        zreg = np.empty((0,2))
        for j in range (len(setup.table1)):
            comment = setup.comment[j,0].split()
            if 'external' not in comment:
                zmin = float(setup.table1[j][2])/float(setup.header[j,1])-1
                zmax = float(setup.table1[j][3])/float(setup.header[j,1])-1
            else:
                # Get redshit edges of the external fitting region
                wref = float(setup.header[j,1])
                wmin = setup.table1[j][2]
                wmax = setup.table1[j][3]
                zmin = float(wmin)/wref-1
                zmax = float(wmax)/wref-1
                # Get wavelength edges of the associated tied region
                wref = float(atominfo(comment[2])[1])
                wmin = wref*(zmin+1)
                wmax = wref*(zmax+1)
                # Get redshift edges of the corresponding overlapping region
                wref = float(atominfo(gettrans(comment[2]))[1])
                zmin = float(wmin)/wref-1
                zmax = float(wmax)/wref-1
            zreg = np.vstack([zreg,[zmin,zmax]])
        setup.zmid = (min(zreg[:,0])+max(zreg[:,1]))/2.
    
    def getdv():
        '''
        Calculate maximum velocity dispersions
        '''
        setup.dv = 0
        for j in range (len(setup.header)):
            comment = setup.comment[j,0].split()
            if 'external' in comment:
                wref    = float(setup.header[j,1])
                # Wavelength at setup.zmid in the overlapping region
                reg     = float(atominfo(gettrans(comment[2]))[1])*(setup.zmid+1)
                # Transition wavelength of the overlapping element
                atom    = float(atominfo(comment[2])[1])
                # Central wavelength of external tied transition for the overlapped system
                wamid   = wref*(reg/atom)
                text    = comment[0]+' at z='+str(round(wamid/float(setup.header[j,1])-1,6))
                dvmin   = abs(2*(setup.table1[j][2]-wamid)/(setup.table1[j][2]+wamid))*setup.c
                dvmax   = abs(2*(setup.table1[j][3]-wamid)/(setup.table1[j][3]+wamid))*setup.c
                setup.dv = max(setup.dv,dvmin,dvmax)
            elif 'overlap' in comment:
                wamid   = float(setup.header[j,1])*(setup.zmid+1)
                text    = comment[2]+' at z='+str(round(wamid/float(atominfo(comment[2])[1])-1,6))
                dvmin   = abs(2*(setup.table1[j][2]-wamid)/(setup.table1[j][2]+wamid))*setup.c
                dvmax   = abs(2*(setup.table1[j][3]-wamid)/(setup.table1[j][3]+wamid))*setup.c
                setup.dv = max(setup.dv,dvmin,dvmax)
            else:
                wamid   = float(setup.header[j,1])*(setup.zmid+1)
                text    = '-'
                dvmin   = abs(2*(setup.table1[j][2]-wamid)/(setup.table1[j][2]+wamid))*setup.c
                dvmax   = abs(2*(setup.table1[j][3]-wamid)/(setup.table1[j][3]+wamid))*setup.c
                setup.dv = max(setup.dv,dvmin,dvmax)
            setup.comment[j,1:] = [text,wamid]
    
    def gettrans(overlaptrans):
        '''
        Get which of the system's transition overlaps with the external system
        '''
        for k in range (len(setup.comment)):
            headline = setup.comment[k,0].split()
            if 'overlap' in headline and headline[2]==overlaptrans:
                break
            
        return headline[0]
    
def E140():
    '''
    Normalise E140 spectrum from spectrum G191-B2B
    '''
    spectrum = sys.argv[2]
    def func(x, a, b, c, d):
        return a + b*x + c*x*x + d*x*x*x
    rc('font', size=2)
    rc('axes', labelsize=8, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=6)
    rc('ytick', labelsize=6)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    table = np.loadtxt(spectrum)
    fig = figure(figsize=(12,8))
    ax = fig.add_subplot(111,xlim=[table[0,0],table[-1,0]],ylim=[0,max(table[:,1])])
    bint  = 700
    skbeg = 1190
    skend = 1250
    i     = 0
    while i < len(table):
        p = i
        if table[i,0] < skbeg or table[i,0] > skend:
            flpoint = []
            while i < len(table) and i < p+bint:
                if  table[i,0] < skbeg or table[i,0] > skend:
                    flpoint.append(table[i,1])
                i = i + 1
            middle = int(len(flpoint)/2)
            median = sorted(flpoint)[middle]
            newmed = np.array([[table[p+middle,0],median]])
            if p < bint:
                medval = newmed
            else:
                medval = np.concatenate((medval,newmed))
        i = i + 1
    plot(table[:,0],table[:,1],'black',lw=.5,zorder=1)
    scatter(medval[:,0],medval[:,1],c='green',s=15,edgecolors='none',zorder=3)
    xdata = medval[:,0]
    ydata = medval[:,1]
    x0    = np.array([0.0, 0.0, 0.0, 0.0])
    popt, pcov = optimization.curve_fit(func, xdata, ydata, x0)
    x = table[:,0]
    y = func(x,popt[0],popt[1],popt[2],popt[3])
    plot(x,y,'red',lw=2,zorder=2)
    opfile = open(spectrum.replace('.dat','_norm.dat'),'w')
    for i in range (0,len(y)):
        opfile.write(str(table[i,0])+'\t'+str(table[i,1]/y[i])+'\t'+str(table[i,2]/y[i])+'\n')
    opfile.close()
    savefig('E140.pdf')

def E230():
    '''
    Normalise E230 spectrum from spectrum G191-B2B
    '''
    spectrum = sys.argv[2]
    def func(x, a, b, c, d, e, f):
        return a + b*x + c*x*x + d*x*x*x + e*x*x*x*x + f*x*x*x*x*x
    rc('font', size=2)
    rc('axes', labelsize=8, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=6)
    rc('ytick', labelsize=6)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    table = np.loadtxt(spectrum)
    fig = figure(figsize=(12,8))
    ax = fig.add_subplot(111,xlim=[table[0,0],table[-1,0]],ylim=[0,max(table[:,1])])
    bint  = 1000
    i     = 0
    while i < len(table):
        p = i
        flpoint = []
        while i < len(table) and i < p+bint:
            flpoint.append(table[i,1])
            i = i + 1
        middle = int(len(flpoint)/2)
        median = sorted(flpoint)[middle]
        newmed = np.array([[table[p+middle,0],median]])
        if p < bint:
            medval = newmed
        else:
            medval = np.concatenate((medval,newmed))
        i = i + 1
    plot(table[:,0],table[:,1],'black',lw=.5,zorder=1)
    scatter(medval[:,0],medval[:,1],c='green',s=15,edgecolors='none',zorder=3)
    xdata = medval[:,0]
    ydata = medval[:,1]
    x0    = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    popt, pcov = optimization.curve_fit(func, xdata, ydata, x0)
    x = table[:,0]
    y = func(x,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
    plot(x,y,'red',lw=2,zorder=2)
    opfile = open(spectrum.replace('.dat','_norm.dat'),'w')
    for i in range (0,len(y)):
        opfile.write(str(table[i,0])+'\t'+str(table[i,1]/y[i])+'\t'+str(table[i,2]/y[i])+'\n')
    opfile.close()
    savefig('E230.pdf')
    
def getinfo():
    '''
    Get wavelength array and info from HIRES Murphy's spectra
    '''
    if '--sargent' in sys.argv:
    
        os.system('ls '+sys.argv[2]+'/data/Norm-*.fits > list')
        qsolist = np.loadtxt('list',dtype=str)
        for qso in qsolist:
            if 'e.fits' not in qso:
                hdulist = fits.open(qso)
                prihdr = hdulist[0].header
                word   = np.empty((0,2))
                for key in prihdr:
                    if 'WV_0' in key:
                        order = int(key.split('_')[-1])-1
                        npix  = len(hdulist[0].data[order])
                        coef  = np.array(prihdr[key].split()+prihdr[key.replace('WV_0','WV_4')].split(),dtype=float)
                        wave  = np.array([ sum( [ coef[n]*i**n for n in range(len(coef)) ] ) for i in range(npix) ] )
                        word  = np.vstack((word,[wave[0],wave[-1]]))
                        #print wave[0],wave[-1]
                xdis = '-' if 'XDISPERS' not in prihdr else prihdr['XDISPERS']
                date = prihdr['DATE-OBS'].split('/')
                date = prihdr['DATE-OBS'] if '/' not in prihdr['DATE-OBS'] else '19'+date[2]+'-'+date[1]+'-'+date[0]
                print sys.argv[2].replace('/','')+\
                    '\t'+str(prihdr['OBSNUM'])+\
                    '\t'+str(prihdr['RA2000'])+\
                    '\t'+str(prihdr['DEC2000'])+\
                    '\t'+date+\
                    '\t'+str(prihdr['ELAPTIME'])+\
                    '\t'+xdis+\
                    '\t'+str(prihdr['ECHANGL'])+\
                    '\t'+str(prihdr['XDANGL'])+\
                    '\t'+str(word[0,0])+\
                    '\t'+str((word[0,0]+word[-1,-1])/2.)+\
                    '\t'+str(word[-1,-1])
                
    if '--churchill' in sys.argv:
    
        os.system('ls '+sys.argv[2]+'/*.fits > list')
        qsolist = np.loadtxt('list',dtype=str)
        for qso in qsolist:
            hdulist = fits.open(qso)
            prihdr = hdulist[0].header
            print hdulist[0].data[-1]
            #word   = np.empty((0,2))
            #for key in prihdr:
            #    if 'WV_0' in key:
            #        order = int(key.split('_')[-1])-1
            #        npix  = len(hdulist[0].data[order])
            #        coef  = np.array(prihdr[key].split()+prihdr[key.replace('WV_0','WV_4')].split(),dtype=float)
            #        wave  = np.array([ sum( [ coef[n]*i**n for n in range(len(coef)) ] ) for i in range(npix) ] )
            #        word  = np.vstack((word,[wave[0],wave[-1]]))
            #        #print wave[0],wave[-1]
            #xdis = '-' if 'XDISPERS' not in prihdr else prihdr['XDISPERS']
            #date = prihdr['DATE-OBS'].split('/')
            #date = prihdr['DATE-OBS'] if '/' not in prihdr['DATE-OBS'] else '19'+date[2]+'-'+date[1]+'-'+date[0]
            #print sys.argv[2].replace('/','')+\
            #    '\t'+str(prihdr['OBSNUM'])+\
            #    '\t'+str(prihdr['RA2000'])+\
            #    '\t'+str(prihdr['DEC2000'])+\
            #    '\t'+date+\
            #    '\t'+str(prihdr['ELAPTIME'])+\
            #    '\t'+xdis+\
            #    '\t'+str(prihdr['ECHANGL'])+\
            #    '\t'+str(prihdr['XDANGL'])+\
            #    '\t'+str(word[0,0])+\
            #    '\t'+str((word[0,0]+word[-1,-1])/2.)+\
            #    '\t'+str(word[-1,-1])

def sortqso():
    '''
    Find QSO spectrum in BOSS list given coordinates
    '''
    xdipp = 17.3*360/24
    ydipp = -61
    xdipm = xdipp+180
    ydipm = -ydipp

    def getcoord(ra,dec):

        val  = ra.split(':')
        ra   = (360/24)*(float(val[0])+float(val[1])/60+float(val[2])/3600)
        val  = dec.split(':')
        if (val[0][0]=='-'):
            dec = float(val[0])-float(val[1])/60-float(val[2])/3600
        else:
            dec = float(val[0])+float(val[1])/60+float(val[2])/3600
            
        return ra,dec
    
    def cd(lon1,lat1,lon2,lat2):
    
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

    if '--sdss' in sys.argv:

        if os.path.exists('./qsolist.dat')==False:

            fh = fits.open('/Users/vincent/ASTRO/library/lists/SDSS/SDSS_QSO_DR12.fits')
            d  = fh[1].data
            hd = fh[1].header
            outfile = open('./qsolist.dat','w')
            for i in range(len(d)):
                print i+1,'/',len(d)
                ZEM       = float(d[hd['TTYPE9']][i])
                RA        = float(d[hd['TTYPE2']][i])
                DEC       = float(d[hd['TTYPE3']][i])
                MJD       = str(d[hd['TTYPE6']][i]).zfill(5)
                PLATE     = str(d[hd['TTYPE5']][i]).zfill(4)
                FIBERID   = str(d[hd['TTYPE7']][i]).zfill(4)
                PSFMAG_u  = float(d[hd['TTYPE79']][i][0])
                PSFMAG_g  = float(d[hd['TTYPE79']][i][1])
                PSFMAG_r  = float(d[hd['TTYPE79']][i][2])
                PSFMAG_i  = float(d[hd['TTYPE79']][i][3])
                PSFMAG_z  = float(d[hd['TTYPE79']][i][4])
                distance  = cd(RA,DEC,xdipm,ydipm)
                outfile.write('{0:<20}  '.format('%i'%int(PLATE)))
                outfile.write('{0:<20}  '.format('%i'%int(MJD)))
                outfile.write('{0:<20}  '.format('%i'%int(FIBERID)))
                outfile.write('{0:<20}  '.format('%.12f'%float(ZEM)))
                outfile.write('{0:<20}  '.format('%.12f'%float(RA)))
                outfile.write('{0:<20}  '.format('%.12f'%float(DEC)))
                outfile.write('{0:<20}  '.format('%.12f'%float(PSFMAG_u)))
                outfile.write('{0:<20}  '.format('%.12f'%float(PSFMAG_g)))
                outfile.write('{0:<20}  '.format('%.12f'%float(PSFMAG_r)))
                outfile.write('{0:<20}  '.format('%.12f'%float(PSFMAG_i)))
                outfile.write('{0:<20}  '.format('%.12f'%float(PSFMAG_z)))
                outfile.write('{0:>20}\n'.format('%.12f'%float(distance)))
            outfile.close()
            
        qsolist = np.loadtxt('./qsolist.dat',dtype=float)
        qsolist = np.array(sorted(qsolist, key=operator.itemgetter(4)))
        outfile  = open('./qsosorted.dat','w')
        outfile.write('{0:<25}  '.format('filename'))
        outfile.write('{0:>20}  '.format('z_em'))
        outfile.write('{0:>20}  '.format('ra'))
        outfile.write('{0:>20}  '.format('dec'))
        outfile.write('{0:>20}  '.format('mag_u'))
        outfile.write('{0:>20}  '.format('mag_g'))
        outfile.write('{0:>20}  '.format('mag_r'))
        outfile.write('{0:>20}  '.format('mag_i'))
        outfile.write('{0:>20}  '.format('mag_z'))
        outfile.write('{0:>20}  '.format('distance'))
        outfile.write('{0:<20}\n'.format('weblink'))
        k = 1
        for i in range(len(qsolist)):
            cond0 = True
            #cond1 = 5 <= float(qsolist[i,3])
            #cond2 = float(qsolist[i,5]) <= 0
            #cond3 = float(qsolist[i,8]) <= 20
            if cond0:# and cond1 and cond2 and cond3:
                plate    = '%04i'%qsolist[i,0]
                mjd      = '%05i'%qsolist[i,1]
                fiberid  = '%04i'%qsolist[i,2]
                filename = 'spec-'+plate+'-'+mjd+'-'+fiberid+'.fits'
                weblink  = 'http://dr12.sdss3.org/spectrumDetail?mjd='+mjd+'&fiber='+fiberid+'&plateid='+plate
                print '{0:>4} - {1:<4}'.format(str(k),filename)
                outfile.write('{0:<25}  '.format(filename))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,3])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,4])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,5])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,6])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,7])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,8])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,9])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,10])))
                outfile.write('{0:>20}  '.format('%.12f'%float(qsolist[i,11])))
                outfile.write('{0:<20}\n'.format(weblink))
                k += 1
        outfile.close()

    if '--2df' in sys.argv:

        if os.path.exists('./qsolist.dat')==False:

            data = np.loadtxt(os.getenv('HOME')+'/ASTRO/library/lists/2QZ/2QZ_6QZ_pubcat.txt',dtype=object)
            outfile  = open('./qsolist.dat','w')
            for i in range(len(data)):
                print i+1,'/',len(data)
                name   = data[i,0]
                zem    = float(data[i,25])
                ra     = data[i,1]+':'+data[i,2]+':'+data[i,3]
                dec    = data[i,4]+':'+data[i,5]+':'+data[i,6]
                ra,dec = getcoord(ra,dec)
                mag    = float(data[i,21])
                dist   = cd(ra,dec,xdipp,ydipp)
                outfile.write('{0:<25}  '.format(name))
                outfile.write('{0:<20}  '.format('%.12f'%float(zem)))
                outfile.write('{0:<20}  '.format('%.12f'%float(ra)))
                outfile.write('{0:<20}  '.format('%.12f'%float(dec)))
                outfile.write('{0:<20}  '.format('%.12f'%float(mag)))
                outfile.write('{0:>20}\n'.format('%.12f'%float(dist)))
            outfile.close()

        #qsolist = np.loadtxt('./qsolist.dat',dtype=object)
        #qsolist = np.array(sorted(qsolist, key=operator.itemgetter(5)))
        #outfile  = open('./qsosorted.dat','w')
        #outfile.write('{0:<25}  '.format('filename'))
        #outfile.write('{0:<20}  '.format('z_em'))
        #outfile.write('{0:<20}  '.format('ra'))
        #outfile.write('{0:<20}  '.format('dec'))
        #outfile.write('{0:<20}  '.format('mag'))
        #outfile.write('{0:<20}\n'.format('distance'))
        #k = 1
        #for i in range(len(qsolist)):
        #    cond = float(qsolist[i,-1])>115
        #    if cond:
        #        print '{0:>4} - {1:<4}'.format(str(k),qsolist[i,0])
        #        outfile.write('{0:<25}  '.format(qsolist[i,0]))
        #        outfile.write('{0:<20}  '.format('%.12f'%float(qsolist[i,1])))
        #        outfile.write('{0:<20}  '.format('%.12f'%float(qsolist[i,2])))
        #        outfile.write('{0:<20}  '.format('%.12f'%float(qsolist[i,3])))
        #        outfile.write('{0:<20}  '.format('%.12f'%float(qsolist[i,4])))
        #        outfile.write('{0:<20}  '.format('%.12f'%float(qsolist[i,5])))
        #        outfile.write('{0:<20}\n'.format('%.12f'%float(qsolist[i,6])))
        #        k += 1
        #outfile.close()        

def wavecorr():
    '''
    Wavelength correction
    '''
    mainpath = '/Users/vincent/ASTRO/analysis/alpha/tests/sargent_data/test2/'
    os.chdir(mainpath)
    fort13 = np.loadtxt('original/fort.13',dtype=str,delimiter='\n')
    trans = np.empty((0,2),dtype=float)
    flag,header,content = 0,[],[]
    for row in fort13:
        if '*' in row:
            flag += 1  
        if flag==1 and '*' not in row:
            header.append(row)
            wmin = float(row.split()[2])
            wmax = float(row.split()[3])
            trans = np.vstack((trans,[wmin,wmax]))
        if flag==2 and '*' not in row:
            content.append(row)
    for wrange in [7,15]:
        testpath = mainpath+'spread%02i'%wrange
        if os.path.exists(testpath)==False:
            os.system('mkdir '+testpath)
        os.chdir(testpath)
        os.system('cp ../original/atom.dat .')
        os.system('cp ../original/vp_setup.dat .')
        os.system('cp ../original/header.dat .')
        fortfile = open('fort.13','w')
        fortfile.write('  *\n')
        for i in range(len(trans)):
            fortfile.write(header[i].replace(header[i].split()[0],'region%02i'%i)+'\n')
            flux  = np.loadtxt('../original/q0000.dat')
            error = np.loadtxt('../original/q0000.sig.dat')
            imin  = abs(flux[:,0]-((trans[i,0]+trans[i,1])/2-wrange)).argmin()
            imax  = abs(flux[:,0]-((trans[i,0]+trans[i,1])/2+wrange)).argmin()
            datafile = open('region%02i.dat'%i,'w')
            for j in range(imin,imax):
                datafile.write('{0:>20} {1:>20}\n'.format('%.8f'%flux[j,0],'%.8f'%flux[j,1]))
            datafile.close()
            datafile = open('region%02i.sig.dat'%i,'w')
            for j in range(imin,imax):
                datafile.write('{0:>20} {1:>20}\n'.format('%.8f'%flux[j,0],'%.8f'%error[j,1]))
            datafile.close()
            filelist = open('in','w').write('region%02i.dat\nregion%02i.sig.dat\n'%(i,i))
            commands = open('command','w').write('\n\n')
            os.system('makeecor < command > termout')
        fortfile.write('  *\n')
        for line in content:
            fortfile.write(line+'\n')
        fortfile.close()
        os.system('rm in command termout')

def vltprop():
    '''
    Plot figure for 2016B VLT proposal
    '''
    def readspec(spectrum):
        hdu = fits.open(spectrum)
        hdu0 = hdu[0].header
        hdu1 = hdu[1].header
        wa   = 10.**(hdu0['coeff0'] + hdu0['coeff1'] * np.arange(hdu1['naxis2']))
        fl   = hdu[1].data['flux']
        er   = [1/np.sqrt(hdu[1].data['ivar'][i]) if hdu[1].data['ivar'][i]!=0 else 10**32 for i in range (len(fl))]
        badpixel = np.append( (np.where(fl > 4.5)[0]) , (np.where(fl < -1)[0]))
        wa = np.delete(wa,badpixel,0)
        fl = np.delete(fl,badpixel,0)
        er = np.delete(er,badpixel,0)
        return wa,fl,er
    rc('font', size=5, family='serif')
    rc('axes', labelsize=10, linewidth=1)
    rc('legend', fontsize=10, handlelength=10)
    rc('xtick', labelsize=10)
    rc('ytick', labelsize=10)
    rc('lines', lw=1, mew=0.2)
    rc('grid', linewidth=0.2)
    xmin,xmax = 3800,9000
    fig = figure(figsize=(8,6))
    subplots_adjust(left=0.06, right=0.97, bottom=0.06, top=0.96, wspace=0.2, hspace=0)
    ax1 = plt.subplot(211,ylim=[-1,5])
    wa,fl,er = readspec('./spec-4235-55451-0152.fits')
    ax1.plot(wa,fl,color='black',lw=0.1,alpha=0.8)
    ax1.axhline(y=0,color='red',ls='dashed')
    ax1.set_xlim([xmin,xmax])
    ax1.yaxis.set_major_locator(plt.FixedLocator([0,1,2,3,4]))
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.text(8700,4,'J021043.16-001818.4\nz$_\mathrm{em}$=4.730',color='red',fontsize=12,va='center',ha='right')
    ax3  = axes([0.06, .8, 0.297, .16], axisbg='#e5ffcc')
    imin = abs(wa-3800).argmin()
    imax = abs(wa-5500).argmin()
    wa1  = wa[imin:imax]
    fl1  = fl[imin:imax]
    er1  = er[imin:imax]
    wa2  = np.array([wa[i] for i in range(imin,imax,10)])
    res  = spec.rebin(wa1,fl1,er1,wa=wa2)
    ax3.plot(res.wa,res.fl,color='black',lw=0.1,alpha=0.8)
    ax3.xaxis.set_major_locator(plt.FixedLocator([4150,5150]))
    ax3.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    ax3.yaxis.set_ticks_position('right')
    ax3.axhline(y=0,color='red',ls='dotted')
    ax3.axvline(x=4150,color='blue',ls='dashed')
    ax3.axvline(x=5150,color='blue',ls='dashed')
    ax2 = plt.subplot(212,ylim=[-1,5])
    wa,fl,er = readspec('./spec-4202-55445-0316.fits')
    ax2.plot(wa,fl,color='black',lw=0.1,alpha=0.8)
    ax2.axhline(y=0,color='red',ls='dashed')
    ax2.set_xlim([xmin,xmax])
    ax2.yaxis.set_major_locator(plt.FixedLocator([0,1,2,3,4]))
    ax2.text(8700,4,'J222509.19-001406.8\nz$_\mathrm{em}$=4.890',color='red',fontsize=12,va='center',ha='right')
    ax4  = axes([0.06, .35, 0.297, .16], axisbg='#e5ffcc')
    imin = abs(wa-3800).argmin()
    imax = abs(wa-5500).argmin()
    wa1  = wa[imin:imax]
    fl1  = fl[imin:imax]
    er1  = er[imin:imax]
    wa2  = np.array([wa[i] for i in range(imin,imax,15)])
    res  = spec.rebin(wa1,fl1,er1,wa=wa2)
    ax4.plot(res.wa,res.fl,color='black',lw=0.1,alpha=0.8)
    ax4.xaxis.set_major_locator(plt.FixedLocator([4600,5100]))
    ax4.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    ax4.yaxis.set_ticks_position('right')
    ax4.axhline(y=0,color='red',ls='dotted')
    ax4.axvline(x=4600,color='blue',ls='dashed')
    ax4.axvline(x=5100,color='blue',ls='dashed')
    plt.savefig('spectra.pdf')

def online():
    '''
    Create online applet to visualise spectra
    '''
    rc('font', size=5, family='sans-serif')
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=10, handlelength=10)
    rc('xtick', labelsize=15)
    rc('ytick', labelsize=15)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    for i in range (0,len(self.qsolist)):
        print self.qsolist[i]
        spectrum = self.qsolist[i]
        qsoname  = spectrum.split('/')[-1].split('.')[0]
        datatype = spectrum.split('/')[-1].split('.')[-1]
        wa,fl,er,cont,sky,z = self.readspec(spectrum) 
        fig = figure(figsize=(50,10))
        subplots_adjust(left=0.02, right=0.99, bottom=0.07, top=0.96, hspace=0, wspace=0.05)
        ax = subplot(111,xlim=[wa[0],wa[-1]],ylim=[self.ymin,self.ymax])
        title(qsoname,fontsize=20)
        plot(wa,fl,'black',drawstyle='steps')
        plot(wa,er,'cyan',drawstyle='steps')
        xlabel('Wavelength',fontsize=15)
        ylabel('Normalised Flux',fontsize=15)
        ax.axhline(y=0, color='red', lw=0.5)
        ax.axhline(y=1, color='red', lw=0.5)
        savefig(qsoname+'.jpg')
        fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
        N = 100        
        scatter = ax.scatter(np.random.normal(size=N),
                             np.random.normal(size=N),
                             c=np.random.random(size=N),
                             s=1000 * np.random.random(size=N),
                             alpha=0.3,
                             cmap=plt.cm.jet)
        ax.grid(color='white', linestyle='solid')
        ax.set_title('Scatter Plot (with tooltips!)', size=20)
        labels = ['point {0}'.format(i + 1) for i in range(N)]
        tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
        mpld3.plugins.connect(fig, tooltip)
        mpld3.show()

def systems():
    '''
    Classification of Lyman forest systems
    '''
    fig = figure(figsize=(8,10))
    rc('font', size=2)
    rc('axes', labelsize=2, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=4)
    rc('ytick', labelsize=4)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    subplots_adjust(left=0.04, right=0.96, bottom=0.02, top=0.95, wspace=None, hspace=None)
    dhratio  = -4.55
    atompar  = n.loadtxt('atompar.dat', usecols=(2,4,3))
    table1   = n.loadtxt(self.datapath+'J024008-230916.dat', usecols=(0,1))
    table2   = n.loadtxt(self.datapath+'J193957-100241.dat', usecols=(0,1))
    table3   = n.loadtxt(self.datapath+'J091614+070225.dat', usecols=(0,1))
    letter   = [r'$\alpha$',r'$\beta$',r'$\gamma$',r'$\delta$',r'$\epsilon$',r'$\zeta$',r'$\eta$',r'$\theta$']
    idx_type = ['Lyman alpha forest system','Lyman limit system','Damped Lyman alpha system']
    idx_name = ['J024008.01-230916.70','J193957.23-100241.14','J091614.05+070225.19']
    idx_tab  = [table1,table2,table3]
    zqso     = [2.225,3.787,2.785]
    zabs     = [2.19796,3.57225,2.6184]
    col      = [16,17.85,20.3]
    dop      = [23,19,15]
    mx_flx   = [1700,2700,1400]
    p        = 0
    while (p < 3):
        i        = 0
        j        = 7
        idx      = p + 1
        table    = idx_tab[p]
        ax = fig.add_subplot(9,3,idx,xlim=[table[0,0],(zqso[p]+1)*1215.67],ylim=[0,mx_flx[p]])
        plot(table[:,0],table[:,1],color='black',lw=0.2)
        axvline(x=(zabs[p]+1)*atompar[0,0],ls='dotted',color='red',lw=0.4)
        axvline(x=(zabs[p]+1)*atompar[1,0],ls='dotted',color='green',lw=0.4)
        axvline(x=(zabs[p]+1)*atompar[2,0],ls='dotted',color='blue',lw=0.4)
        axvline(x=(zabs[p]+1)*atompar[3,0], ls='dotted',color='purple',lw=0.4)
        axvline(x=(zabs[p]+1)*912.3240,color='yellow',lw=0.4)
        title(idx_type[p]+'\n'+idx_name[p]+'\n'+'\n'+'$z_{abs}=$'+str(zabs[p])+'\t log($N_{HI}$)='+str(col[p])+'\t $b$='+str(dop[p]),fontsize=7)
        idx = idx + 24
        while ((i < len(table)) and (j >= 0)):
            ref  = (zabs[p]+1)*atompar[j,0]
            diff = (table[i,0]-ref)/(ref)*c
            if (abs(diff) < 300):               # if read wavelength less than 300km/s on the right of the line
                ax = fig.add_subplot(9,3,idx,xlim=[-300,200],ylim=[-0.15,1.4])
                waend  = ref*(1+300/c)
                v = []
                a = i
                while table[i,0] < waend:
                    v.append((table[i,0]-ref)/(ref)*c)
                    i = i + 1
                b = i
                flux = table[a:b,1]/sorted(table[a:b,1])[int(0.99*len(table[a:b,1]))]
                wave       = np.arange(atompar[j,0]*(1-300/c),atompar[j,0]*(1+200/c),0.01)
                vel        = (wave-atompar[j,0])/(atompar[j,0])*c
                vhfit      = self.p_voigt(col[p],dop[p],wave,atompar[j,0],atompar[j,1],atompar[j,2])
                vdfit      = self.p_voigt(col[p]+dhratio,dop[p],wave,atompar[j+328,0],atompar[j+328,1],atompar[j+328,2])
                flx_voigt1 = vhfit*vdfit
                vhfit      = self.p_voigt(16.5,10,wave,atompar[j,0],atompar[j,1],atompar[j,2])
                vdfit      = self.p_voigt(16.5+dhratio,10,wave,atompar[j+328,0],atompar[j+328,1],atompar[j+328,2])
                flx_voigt2 = vhfit*vdfit
                plot(v,flux,color='black',lw=0.2)
                plot(vel,flx_voigt1,color='red',lw=0.2)
                plot(vel,flx_voigt2,color='green',lw=0.2)
                ax.yaxis.set_major_locator(NullLocator())
                axvline(x=0, ls='dotted',color='grey',lw=0.2)
                axvline(x=-82, ls='dotted',color='grey',lw=0.2)
                axhline(y=0, ls='dotted',color='grey',lw=0.2)
                axhline(y=1, ls='dotted',color='grey',lw=0.2)
                text(-280,1.1,'Ly-'+letter[j],color='blue',fontsize=8)
                idx = idx - 3
                j = j - 1
            if (diff > 300):                     # if readen wavelength more than 300km/s on the left of the line
                ax = fig.add_subplot(9,3,idx,xlim=[-300,200],ylim=[-0.15,1.4])
                ax.yaxis.set_major_locator(NullLocator())
                idx = idx - 3
                j = j - 1
            i = i + 1
        p = p + 1
    savefig('PyD_profile_lyforestclass.pdf')
