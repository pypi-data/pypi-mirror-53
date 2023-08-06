import quasar,numpy

def dr7_list():
    '''
    Find SDSS spectra with DLA in DR7 release
    '''
    lyalpha  = 1215.6701
    lybeta   = 1025.7223
    qsolist  = numpy.loadtxt(sys.argv[1],dtype='str',comments='#')
    dlatable = numpy.loadtxt('SDSS_DLA_DR7.dat',dtype='str',usecols=(1,2,3),comments='#')
    opfile2  = open('selection.dat','w')
    zmin     = 2.2
    redshift = []
    g,l = 0,0
    for i in range(0,len(qsolist)):
        if i % 500 == 0:
            print i
        dlaflag = 0
        qsoinfo = qsolist[i].split('.')[0].split('-')[1:]
        MJD     = str(qsoinfo[0])
        PLATE   = str(qsoinfo[1])
        FIBERID = str(qsoinfo[2])
        idname  = PLATE+'-'+MJD+'-'+FIBERID
        if idname in dlatable[:,0]:
            index = numpy.where(dlatable[:,0]==idname)[0]
            Z_VI  = float(dlatable[index[0],1])
            lyb   = (Z_VI+1)*1025.72
            za    = lyb/1215.67-1
            for k in range (len(index)):
                if float(dlatable[index[k],2])>za:
                    dlaflag = 1
                    print idname,'Contaminating DLAs',l
                    l=l+1
                    break
        if dlaflag==0:
            opfile2.write(qsolist[i]+'\n')
    opfile2.close()

def dr10_newlist():
    '''
    Create list of SDSS DR10 quasar names only.
    '''
    qsolist = numpy.loadtxt(sys.argv[1],dtype='str')
    opfile  = open('newlist','w')
    flag    = 0
    for i in range (0,len(qsolist)):
        qsoname = qsolist[i].split('/')[-1]
        if os.path.exists(datapath+qsoname)==False:
            opfile.write(qsolist[i]+'\n')
            p = i
    opfile.close()

def dr10_list():
    '''
    Find SDSS spectra with DLA in DR10 release    
    '''
    BOSSlimit = 3600
    lyalpha   = 1215.6701
    lybeta    = 1025.7223
    dlatable  = numpy.loadtxt('SDSS_DLA_DR10.dat',dtype='str',usecols=(1,9),comments='#')
    zmin      = 2.2
    zmax      = 4.5
    fh        = fits.open('SDSS_QSO_DR10.fits')
    d         = fh[1].data
    hd        = fh[1].header
    opfile1   = open('qsoall.dat','w')
    opfile2   = open('selection.dat','w')
    opfile3   = open('sample_even.dat','w')
    opfile4   = open('sample_odd.dat','w')
    redshift  = []
    g,l       = 0,0
    for i in range(0,len(d)):
        if i % 500 == 0:
            print i
        bal = dla = 0
        RA        = float(fh[1].data[hd['TTYPE2']][i])
        DEC       = float(fh[1].data[hd['TTYPE3']][i])
        MJD       = str(fh[1].data[hd['TTYPE6']][i]).zfill(5)
        PLATE     = str(fh[1].data[hd['TTYPE5']][i]).zfill(4)
        FIBERID   = str(fh[1].data[hd['TTYPE7']][i]).zfill(4)
        Z_VI      = float(fh[1].data[hd['TTYPE8']][i])
        BALFLAG   = int(fh[1].data[hd['TTYPE50']][i])
        filename  = 'spec-'+PLATE+'-'+MJD+'-'+FIBERID+'.fits'
        idname    = MJD+'-'+PLATE+'-'+FIBERID
        if BALFLAG==1:
            bal = Z_VI
        if idname in dlatable[:,0]:
            lyb = (Z_VI+1)*1025.72
            za  = lyb/1215.67-1
            index = numpy.where(dlatable[:,0]==idname)[0]
            for k in range (len(index)):
                if float(dlatable[index[k],1])>za:
                    dla = Z_VI
                    l=l+1
                    break
        # BOSSlimit < (float(Z_VI)+1)*lybeta
        if zmin<float(Z_VI) and bal==0 and dla==0 and os.path.exists(datapath+filename)==True and 0>DEC:
            opfile2.write(datapath+filename+'\n')
            redshift.append(Z_VI)
            g = g + 1
            print 'spectra found:',g
            if g % 2:
                opfile3.write(datapath+filename+'\n')
            else:
                opfile4.write(datapath+filename+'\n')                
        if zmin<float(Z_VI) and (bal!=0 or dla!=0):
            opfile1.write(filename+'\t'+str('%.5f'%Z_VI)+'\t'+str('%.5f'%bal)+'\t'+str('%.5f'%dla)+'\n')
        else:
            opfile1.write(filename+'\t'+str('%.5f'%Z_VI)+'\t'+'0.00000'+'\t'+'0.00000'+'\n')
    print len(redshift),min(redshift),max(redshift),l
    opfile1.close()
    opfile2.close()
    opfile3.close()
    opfile4.close()

def dr10_hist():
    '''
    Output qsoall.dat from dr10_list is needed!
    '''
    dlalist = numpy.loadtxt('../SDSS_DLA_DR10.dat',dtype='str',usecols=(1,9),comments='#')
    qsolist = numpy.loadtxt(sys.argv[1],dtype='str')
    print len(numpy.where(qsolist[:,2]!='0.00000')[0]),'BALs'
    print len(numpy.where(qsolist[:,3]!='0.00000')[0]),'DLAs'
    qso = numpy.empty((0,3))
    label = []
    z = 2.2
    while z < 6:
        numbal = numdla = total = 0
        for i in range(len(qsolist)):
            if z<float(qsolist[i,1])<z+0.2:
                total = total + 1
            if z<float(qsolist[i,2])<z+0.2:
                numbal = numbal + 1
            if z<float(qsolist[i,3])<z+0.2:
                numdla = numdla + 1
        qso = numpy.vstack((qso,[numbal/float(total),numdla/float(total),total]))
        label.append(str(z)+' - '+str(z+.2))
        z = z + 0.2
    dla = numpy.empty((0,2))
    z = 2.2
    while z < 6:
        print z
        numdla = total = 0
        for i in range(len(qsolist)):
            redshift = float(qsolist[i,1])
            lybeta   = (redshift+1)*1025.72
            zalpha   = lybeta/1215.67-1
            if z<redshift and zalpha<z+0.2:
                total = total + 1
            if float(qsolist[i,3])!=0:
                qsoname = qsolist[i,0].replace('spec-','').replace('.fits','').split('-')
                qsoname = qsoname[1]+'-'+qsoname[0]+'-'+qsoname[2]
                index   = numpy.where(dlalist[:,0]==qsoname)[0]
                for k in range(len(index)):
                    if z < float(dlalist[index[k],1]) < z+0.2 and zalpha < float(dlalist[index[k],1]):
                        numdla = numdla + 1
        dla = numpy.vstack((dla,[numdla/float(total),total]))
        z = z + 0.2
    fig = figure(figsize=(20,10))
    ax = plt.subplot(111)
    index = numpy.arange(len(qso))
    bar_width = 0.33
    opacity = 0.4
    rects1 = plt.bar(index,qso[:,0],bar_width,alpha=opacity,color='cyan',label='QSOs identified as BAL, normalised by the total number of QSOs with zem located within the redshift bin (blue value).',lw=0)
    rects2 = plt.bar(index+bar_width,qso[:,1],bar_width,alpha=opacity,color='magenta',label='QSOs with DLAs between the Lyman alpha and beta emission lines, normalised by the number of QSOs with zem located within the redshift bin (blue value).',lw=0)
    rects3 = plt.bar(index+2*bar_width,dla[:,0],bar_width,alpha=opacity,color='lime',label='Number of DLAs with zabs falling into the redshift bin, normalised by the total number of Ly-a to Ly-b emission lines regions falling into the bin (red value).',lw=0)
    plt.xlabel('Redshift bins',labelpad=20)
    plt.ylabel('Ratio per redshift bin')
    plt.title('Fractional number of BAL quasars and DLAs per redshift bin in SDSS DR10',fontsize=10)
    plt.xticks(index+3*bar_width,[])
    axhline(y=1,color='black',ls='dotted')
    lg = legend(prop={'size':10},loc='upper left')
    fr = lg.get_frame().set_alpha(0)
    ylim(0,1.17)
    xlim(0,len(qso))
    for i in range (len(qso)):
        text(i+1.5*bar_width,1.025,int(qso[i,-1]),color='blue',fontsize=10,ha='center')
        text(i+1.5*bar_width,1.005,int(dla[i,-1]),color='red',fontsize=10,ha='center')
        vlines(x=i+3*bar_width, ymin=0, ymax=1,linestyles='dotted', color='black')
        text(i+1.5*bar_width,-.01,label[i],color='black',fontsize=8,va='top',ha='center')
    savefig('plot.pdf')
    clf()

def dr10_primsel():
    '''
    Find SDSS spectra with DLA in DR10 release    
    '''
    SDSS_BOSS_walimit = 3600
    lyalpha = 1215.6701
    lybeta  = 1025.7223
    zmin = 2.2
    zmax = 4.5
    dlatable = numpy.loadtxt('SDSS_DLA_DR10.dat',dtype='str',usecols=(1,9))
    fh = fits.open('SDSS_QSO_DR10.fits')
    d  = fh[1].data
    hd = fh[1].header
    opfile = open('qsolist','w')
    redshift = []
    for i in range(0,len(d)):
        RA      = float(fh[1].data[hd['TTYPE2']][i])
        DEC     = float(fh[1].data[hd['TTYPE3']][i])
        PLATE   = int(fh[1].data[hd['TTYPE5']][i])
        MJD     = int(fh[1].data[hd['TTYPE6']][i])
        FIBERID = int(fh[1].data[hd['TTYPE7']][i])
        Z_VI    = float(fh[1].data[hd['TTYPE8']][i])
        BALFLAG = int(fh[1].data[hd['TTYPE50']][i])
        # print  MJD+'-'+PLATE+'-'+FIBERID
        # initially SDSS_BOSS_walimit < (Z_VI+1)*lybeta to select only spectra with lybeta
        if SDSS_BOSS_walimit < (Z_VI+1)*lybeta and zmin<Z_VI<zmax \
           and str(MJD)+'-'+str(PLATE)+'-'+str(FIBERID) not in dlatable[:,0] and BALFLAG!=1:
            # Additional path for download: 'http://data.sdss3.org/sas/dr10/boss/spectro/redux/v5_5_12/spectra/'
            path = 'spec-'+str(PLATE)+'-'+str(MJD)+'-'+str("%04d" % int(FIBERID))+'.fits'
            opfile.write(path+'\n')
        if str(MJD)+'-'+str(PLATE)+'-'+str(FIBERID) in dlatable[:,0]:
            path = str(MJD)+'-'+str(PLATE)+'-'+str(FIBERID)
            k = numpy.where(path==dlatable[:,0])[0]
            for j in range (len(k)):
                zabs = dlatable[k[j],1]
                print 'spec-'+str(PLATE)+'-'+str(MJD)+'-'+str("%04d" % int(FIBERID))+'.fits',zabs
        redshift.append(Z_VI)
    opfile.close()
    print 'Minimum redshift:',min(redshift)

def dr12_dla():
    '''
    List SDSS quasar with DLA in DR12
    '''
    dlatable = numpy.genfromtxt(self.pathlist+'SDSS_DLA_DR12.dat',names=True,dtype=object,comments='!')
    distlist = numpy.empty((0,7))
    for i in range(len(dlatable)):
        mjd   = int(dlatable['mjd'][i])
        plate = int(dlatable['plate'][i])
        fiber = int(dlatable['fiber'][i])
        ra1   = float(dlatable['ra'][i])
        dec1  = float(dlatable['dec'][i])
        ra2   = self.alphara*360/24     # in degrees
        dec2  = self.alphadec           # in degrees
        dist  = self.calc_spheredist(ra1,dec1,ra2,dec2)
        distlist = numpy.vstack((distlist,[mjd,plate,fiber,ra1,dec1,dist,0]))
    columns = 'PLATE MJD FIBERID EXPMAG'.split()
    d = fitsio.read(self.pathdata+'DR12/spAll-DR12.fits', 1, columns=columns)
    for i in range(len(d)):
        print d['EXPMAG'][i]
    binwidth = 1
    fig = figure(figsize=(10,5))
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.95, hspace=0, wspace=0)
    ax = subplot(111)
    ax.hist(distlist, numpy.arange(min(distlist),max(distlist)+binwidth,binwidth), stacked=True, fill=True,alpha=0.5)
    ax.set_title('Distribution of distance to alpha dipole for SDSS DR12 detected DLAs',fontsize=10)
    savefig('dr12_alpha_dist.pdf')
    clf()
