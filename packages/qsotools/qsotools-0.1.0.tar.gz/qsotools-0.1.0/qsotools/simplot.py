import os,numpy,math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator,FixedLocator
import constants as const
from barak import spec

def binning(fname=None):
    '''
    Compare Voigt profiles with different binning
    '''
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(1,figsize=(12,8))
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.1, top=0.9, hspace=.25, wspace=0.2)
    plt.title('Voigt profile example from J042214-384452\n')
    plt.axis('off')
    N = 11.67779
    z = 3.0877602
    b = 0.3382
    info = numpy.array([['SiII_1260',1260.42210,1.180,2.95E9,5151.00,5153.00],
                        ['SiII_1526',1526.70698,0.133,1.13E9,6240.00,6243.00]],dtype=object)
    for i in range(len(info)):
        curve = []
        label = []
        ax    = fig.add_subplot(1,2,i+1,xlim=[-10,10],ylim=[-0.1,1.1])
        chunk = numpy.loadtxt('vpfit_chunk'+'%03d'%(i+1)+'.txt',comments='!')
        wabeg = abs(chunk[:,0]-info[i,4]).argmin()+1
        waend = abs(chunk[:,0]-info[i,5]).argmin()-1
        wave  = chunk[wabeg:waend,0]
        flux  = chunk[wabeg:waend,1]
        error = chunk[wabeg:waend,2]
        model = chunk[wabeg:waend,3]
        wamid = info[i,1]*(z+1)
        ''' Plot Data '''
        pos   = abs(wave-(info[i,4]+info[i,5])/2).argmin()
        pix1  = wave[pos]
        pix2  = (wave[pos]+wave[pos-1])/2
        dpix  = 2*(pix1-pix2)/(pix1+pix2)*const.c
        vel   = 2*(wave-wamid)/(wave+wamid)*const.c
        p1,   = plt.plot(vel+dpix,flux,lw=2,color='black',drawstyle='steps',alpha=0.7)
        p2,   = plt.plot(vel+dpix,model,lw=2,color='black',ls='dashed',drawstyle='steps',alpha=0.7,zorder=2)
        curve = curve+[p1,p2]
        label = label+['Data','Model from VPFIT chunk']
        ''' Plot high resolution model '''
        wav2  = numpy.arange(wave[0],wave[-1],0.001)
        vel2  = 2*(wav2-wamid)/(wav2+wamid)*const.c
        mod2  = quasar.voigt_model(N,b,wav2/(z+1),info[i,1],info[i,3],info[i,2])
        p,    = plt.plot(vel2,mod2,lw=2,color='red',alpha=0.7)
        curve.append(p)
        label.append('High resolution Voigt profile\nmodel from fort.13 results')
        ''' Plot rebinned model from high to low resolution'''
        wav3  = wave
        vel3  = 2*(wav3-wamid)/(wav3+wamid)*const.c
        mod3  = spec.rebin(wav2,mod2,mod2,wa=wav3).fl
        p,    = plt.plot(vel3+dpix,mod3,lw=4,color='red',drawstyle='steps',ls='dashed',alpha=0.7,zorder=1)
        curve.append(p)
        label.append('High resolution model\nrebinned to data resolution')
        ax.legend(curve,label,numpoints=2,handlelength=3,frameon=False,
                  prop={'size':8},loc='lower left',bbox_to_anchor=[0.01,0.12],ncol=1)
        ax.axhline(y=0,ls='dotted',color='black')
        ax.axvline(x=0,ls='dotted',color='black')
        ax.axhline(y=1,ls='dotted',color='black')
        ax.set_xlabel('Velocity relative to $z_{abs}='+str(z)+'$ (km/s)',fontsize=10)
        ax.set_ylabel('Flux')
        ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    plt.show() if fname==None else plt.savefig(fname)
    plt.close(fig)

def coaddition():
    '''
    Co-added Voigt profile with and without distortion correction
    '''
    fig = plt.figure(figsize=(8,10))
    subplots_adjust(left=0.1,right=0.9,bottom=0.1,top=0.93,wspace=0,hspace=0)
    plt.rc('font',   size=10, family='sans-serif')
    plt.rc('axes',   labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=5)
    plt.rc('xtick',  labelsize=10)
    plt.rc('ytick',  labelsize=10)
    plt.rc('lines',  lw=0.2, mew=0.2)
    plt.rc('grid',   linewidth=0.2) 
    dv         = 1
    dv_correct = -0.5
    e_wave     = 2796.3521
    e_strength = 0.62900
    e_gamma    = 2.6120e+08
    wmin       = e_wave*(1-500./const.c)
    wmax       = e_wave*(1+500./const.c)
    wa1        = numpy.arange(wmin,wmax,0.001)    
    v1         = (wa1-e_wave)/e_wave*const.c
    fl1        = quasar.p_voigt(12.5,10,wa1,e_wave,e_gamma,e_strength)
    er1        = [1E-12 for i in range (len(wa1))]
    da1        = spec.rebin(wa1,fl1,er1,wa=wa1)
    wa2        = wa1 * (2*const.c+dv) / (2*const.c-dv)
    v2         = (wa2-e_wave)/e_wave*const.c
    fl2        = const.p_voigt(12.5,10,wa1,e_wave,e_gamma,e_strength)
    er2        = [1E-12 for i in range (len(wa2))]
    da2        = spec.rebin(wa2,fl2,er2,wa=wa1)
    da3        = spec.combine([da1,da2])
    wa3        = da3.wa * (2*const.c+dv_correct) / (2*const.c-dv_correct)
    fl3        = da3.fl
    v3         = (wa3-e_wave)/e_wave*const.c
    flmin      = min(fl3)
    idx        = numpy.where(fl3==flmin)[0][0]
    v3min      = v3[idx]
    ax = fig.add_subplot(211,xlim=[-50,50],ylim=[-0.15,1.3])
    plt.plot(v1,fl1,lw=0.5,color='blue',label='Non-shifted MgII 2796 line')
    plt.plot(v2,fl2,lw=0.5,color='red',label='Shifted MgII 2796 line')
    lg = ax.legend(loc=(0.03,0.15),handlelength=2)
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    ylabel("Normalised flux")
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    axvline(x=0, ls='dotted',color='grey',lw=0.2)
    axhline(y=0, ls='dotted',color='grey',lw=0.2)
    axhline(y=1, ls='dotted',color='grey',lw=0.2)
    text(0,1.1,'Shift of '+'%.3f'%dv+' km/s',ha='center')
    #==============================================================================================================
    ax = fig.add_subplot(212,xlim=[-50,50],ylim=[-0.15,1.3])
    plt.plot(v1,fl1,lw=3,color='black',label='Correction done BEFORE co-addition')
    plt.plot(v3,fl3,lw=.5,color='yellow',label='Correction done AFTER co-addition')
    lg = ax.legend(loc=(0.03,0.15),handlelength=2)
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    xlabel(r"Velocity relative to $\lambda$="+str(e_wave)+" $\AA$ (in km/s)")
    ylabel("Normalised flux")
    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    axvline(x=0, ls='dotted',color='grey',lw=0.2)
    axhline(y=0, ls='dotted',color='grey',lw=0.2)
    axhline(y=1, ls='dotted',color='grey',lw=0.2)
    text(0,1.1,'Shift of '+'%.3f'%v3min+' km/s',ha='center')
    plt.savefig('distcor.pdf') if tbs else plt.show()
    #==============================================================================================================
    # Second figure: show that coaddition of different SNR will be dominated by high SNR
    #==============================================================================================================
    # Setup values
    disp  = 1.3    #km/s (pixel size of the spectrum)
    fwhm  = 5.0    #resolution
    wbeg  = 4000.  #A
    wend  = 7020.  #A
    wmid  = (wbeg+wend)/2.  #A
    slope = 5    #m/s/A
    zabs  = 1.5
    dv    = 100     #km/s (half of velocity region to fit for each transition)
    wref  = 2382.7641975*(zabs+1)
    # Create wavelength array with velocity dispersion of 1.3 km/s
    wave = [wbeg]
    while wave[-1]<wend:
        wave.append(wave[-1]*(2*const.c+disp)/(2*const.c-disp))
    numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))
    # Generate artificial spectrum with FeII and SNR of 50
    noise = 20.
    script = open('./commands.dat','w')
    script.write('rd wave.dat \n')
    script.write('gp \n')
    script.write('FeII 13.7 5 '+str(zabs)+' \n')
    script.write('\n')
    script.write(str(fwhm)+' \n')
    script.write('noise \n')
    script.write('\n')
    script.write(str(noise)+' \n')
    script.write('wt spec1.dat (all) \n')
    script.write('lo \n')
    script.close()
    os.system('rdgen < commands.dat > termout')
    os.system('rm termout')
    # Generate artificial spectrum with FeII and SNR of 200
    noise = 70.
    script = open('./commands.dat','w')
    script.write('rd wave.dat \n')
    script.write('gp \n')
    script.write('FeII 13.7 5 '+str(zabs)+' \n')
    script.write('\n')
    script.write(str(fwhm)+' \n')
    script.write('noise \n')
    script.write('\n')
    script.write(str(noise)+' \n')
    script.write('wt spec2.dat (all) \n')
    script.write('lo \n')
    script.close()
    os.system('rdgen < commands.dat > termout')
    os.system('rm termout')
    # Create 2 artificial spectra distorted of opposite sign
    spec1 = numpy.loadtxt('spec1.dat')
    wa1   = numpy.array(spec1[:,0])
    fl1   = numpy.array(spec1[:,1])
    er1   = numpy.array(spec1[:,2]) 
    shift = -7#-slope*(wa1-wmid)/1000.
    wa1   = wa1*(2*const.c+shift)/(2*const.c-shift)
    v1    = (wa1-wref)/wref*const.c
    spec2 = numpy.loadtxt('spec2.dat')
    wa2   = numpy.array(spec2[:,0])
    fl2   = numpy.array(spec2[:,1])
    er2   = numpy.array(spec2[:,2]) 
    shift = 7#slope*(wa2-wmid)/1000.
    wa2   = wa2*(2*const.c+shift)/(2*const.c-shift)
    v2    = (wa2-wref)/wref*const.c
    data = spec.rebin(wa1,fl1,er1,wa=wa1)
    #for i in range(5):
    #    rebin = spec.rebin(wa1,fl1,er1,wa=wa1)
    #    data  = spec.combine([data,rebin])
    rebin = spec.rebin(wa2,fl2,er2,wa=wa1)
    data  = spec.combine([data,rebin])
    v3    = (data.wa-wref)/wref*const.c
    # Plot spectra
    fig = plt.figure(figsize=(10,4))
    plt.subplots_adjust(left=0.08, right=0.98, bottom=0.13, top=0.95, hspace=0, wspace=0)
    # Plotting settings
    plt.rc('font',   size=10, family='sans-serif')
    plt.rc('axes',   labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=5)
    plt.rc('xtick',  labelsize=10)
    plt.rc('ytick',  labelsize=10)
    plt.rc('lines',  lw=0.2, mew=0.2)
    plt.rc('grid',   linewidth=0.2) 
    # New subplot
    ax = fig.add_subplot(131,xlim=[-50,50],ylim=[-0.15,1.5])
    ax.plot(v1,fl1,label='Spectrum',color='black')
    ax.axhline(y=0,ls='dotted',lw=0.1,color='black')
    ax.axhline(y=1,ls='dotted',lw=0.1,color='black')
    ax.axvline(x=0,ls='dotted',lw=0.1,color='black')
    ax.set_ylabel('Normalized flux',fontsize=10)
    ax.set_xlabel('Velocity relative to $z_{abs}=%.1f$ (km/s)'%zabs,fontsize=10)
    ax.yaxis.set_major_locator(plt.FixedLocator([0,0.2,0.4,0.6,0.8,1]))
    t1 = ax.text(0,1.3,'Low-resolution',fontsize=12,ha='center')
    t1.set_bbox(dict(color='white', alpha=0.7, edgecolor=None))
    # New subplot
    ax = fig.add_subplot(132,xlim=[-50,50],ylim=[-0.15,1.5])
    ax.plot(v2,fl2,label='Spectrum',color='black')
    ax.axhline(y=0,ls='dotted',lw=0.1,color='black')
    ax.axhline(y=1,ls='dotted',lw=0.1,color='black')
    ax.axvline(x=0,ls='dotted',lw=0.1,color='black')
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.set_xlabel('Velocity relative to $z_{abs}=%.1f$ (km/s)'%zabs,fontsize=10)
    ax.yaxis.set_major_locator(plt.FixedLocator([0,0.2,0.4,0.6,0.8,1]))
    t1 = ax.text(0,1.3,'High-resolution',fontsize=12,ha='center')
    t1.set_bbox(dict(color='white', alpha=0.7, edgecolor=None))
    # New subpot
    ax = fig.add_subplot(133,xlim=[-50,50],ylim=[-0.15,1.5])
    ax.plot(v3,data.fl,label='Spectrum',color='black')
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.axhline(y=0,ls='dotted',lw=0.1,color='black')
    ax.axhline(y=1,ls='dotted',lw=0.1,color='black')
    ax.axvline(x=0,ls='dotted',lw=0.1,color='black')
    ax.set_xlabel('Velocity relative to $z_{abs}=%.1f$ (km/s)'%zabs,fontsize=10)
    ax.yaxis.set_major_locator(plt.FixedLocator([0,0.2,0.4,0.6,0.8,1]))
    t1 = ax.text(0,1.3,'Combined',fontsize=12,ha='center')
    t1.set_bbox(dict(color='white', alpha=0.7, edgecolor=None))
    plt.savefig('coaddition.pdf') if tbs else plt.show()
    
def findabs(fname=None):
    '''
    Absorption detection from 0 flux level upward
    '''
    plt.rc('font', size=2, family='serif')
    plt.rc('axes', labelsize=7, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=5)
    plt.rc('ytick', labelsize=5)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)        
    fig = plt.figure(figsize=(8,4))
    ax = plt.subplot(111)
    ax.xaxis.set_major_locator(NullLocator())
    ax.yaxis.set_major_locator(FixedLocator([0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]))
    ref   = 1215.67
    start = ref / (1-(-300)/299792.458)
    end   = ref / (1-(300)/299792.458)
    wave  = numpy.arange(start,end,0.01)
    f = 0
    v = []
    while (f < len(wave)):
        velocity = 299792.458*(wave[f]-ref)/wave[f]
        v.append(velocity)
        f = f + 1
    flux_const1 = wave/wave * .1
    flux_const2 = wave/wave * .4
    flux_const3 = wave/wave * .5
    flux_const4 = wave/wave * .9
    flux1 = quasar.p_voigt(14.1,40,wave,1215.67,6.2650e+08,0.4164) * \
            quasar.p_voigt(13.5,25,wave,1215.3394,6.2650e+08,0.4164)
    plt.plot(v,flux1,lw=0.2,color='blue')
    plt.fill_between(v,flux1,flux_const4,where=flux_const4>=flux1,color='#FFF2F2')
    plt.fill_between(v,flux1,flux_const3,where=flux_const3>=flux1,color='white')
    plt.fill_between(v,flux1,flux_const2,where=flux_const2>=flux1,color='#E6F5EB')
    plt.fill_between(v,flux1,flux_const1,where=flux_const1>=flux1,color='white')
    plt.xlim(-300,300)
    plt.ylim(0,1)
    plt.ylabel('Flux')
    plt.annotate("",xy=(-250,.5),xytext=(-250,.9),arrowprops=dict(fc="red",ec="none"))
    plt.axhline(y=.5, color='red',lw=0.2)
    plt.axhline(y=.9, color='red',lw=0.2)
    plt.axhline(y=1,ls='dotted', color='grey',lw=0.2)
    plt.text(160,.91,'1 detection',fontsize=7,color='red')
    plt.text(160,.51,'2 detections',fontsize=7,color='red')
    #plt.text(-250,1.1,'Initial assumption:',fontsize=7,color='red',style='italic')
    #plt.text(-100,1.1,'Everything is just one huge single absorption!',fontsize=7,color='red')
    plt.axhspan(ymin=-.05, ymax=-.2, facecolor='0.9',lw=0)
    plt.annotate("",xy=(-250,.4),xytext=(-250,.1),arrowprops=dict(fc="green",ec="none"))
    plt.axhline(y=0,ls='dotted', color='grey',lw=0.2)
    plt.axhline(y=.1, color='green',lw=0.2)
    plt.axhline(y=.4, color='green',lw=0.2)
    plt.text(160,.11,'1 detection',fontsize=7,color='green')
    plt.text(160,.41,'2 detections',fontsize=7,color='green')
    #plt.text(-250,-.14,'Initial assumption:',fontsize=7,color='green',style='italic')
    #plt.text(-100,-.14,'There is no absorption at all',fontsize=7,color='green')
    plt.axhspan(ymin=1.05, ymax=1.2, facecolor='0.9',lw=0)
    plt.show() if fname==None else plt.savefig(fname)
    plt.close(fig)

def lyman_alpha():
    '''
    Plot Lyman alpha Voigt profiles in N,b space.
    '''
    plt.rc('font', size=2)
    plt.rc('axes', labelsize=2, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=4)
    plt.rc('ytick', labelsize=4)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(figsize=(8,10))
    subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98, wspace=None, hspace=None)
    col    = [14,17,19,21]
    dop    = [10,20,30,40,50,60]
    vrange = [200,400,900,6000]
    index = 1
    i = 0
    while (i < len(dop)):
        j = 0
        while (j < len(col)):
            wmin = 1215.6701 / (1 + (vrange[j]/300000.))
            wmax = 1215.6701 / (1 - (vrange[j]/300000.))
            wave = numpy.arange(wmin,wmax,0.0002)
            v    = (wave-1215.6701)/wave*300000.
            flux = quasar.p_voigt(col[j],dop[i],wave,1215.67,6.2650e+08,0.4164)
            ax = fig.add_subplot(6,4,index,xlim=[-vrange[j],vrange[j]],ylim=[-0.15,1.3])
            plt.plot(v,flux,lw=0.2)
            ax.yaxis.set_major_locator(NullLocator())
            axvline(x=0, ls='dotted',color='grey',lw=0.2)
            axhline(y=0, ls='dotted',color='grey',lw=0.2)
            axhline(y=1, ls='dotted',color='grey',lw=0.2)
            text(-2*(vrange[j]/3),1.1,'log($N_{HI}$)='+str(col[j]),fontsize=5)
            text(vrange[j]/3,1.1,'b='+str(dop[i]),fontsize=5)
            index = index + 1
            j = j + 1
        i = i + 1
    plt.savefig('lymanalpha.pdf') if tbs else plt.show()

def lyman_series():
    '''
    Plot Voigt profile for all Lyman series
    '''
    plt.rc('font', size=6, family='sans-serif')
    plt.rc('axes', labelsize=6, linewidth=0.2)
    plt.rc('legend', fontsize=6, handlelength=10)
    plt.rc('xtick', labelsize=6)
    plt.rc('ytick', labelsize=6)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(figsize=(12,8))
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.05, top=0.95, hspace=.25, wspace=0.15)
    axis('off')
    ''' Create overlapping Lyman series '''
    dv    = 500. #1250.
    wave  = numpy.arange(900,1300,0.001)
    N,b,z = 19.,10.,0.
    model = 1.
    for i in range(len(const.HI)):
        lambda0  = const.HI[i]['wave']
        gamma    = const.HI[i]['gamma']
        strength = const.HI[i]['strength']
        model    = model*quasar.model(N,b,wave/(z+1),lambda0,gamma,strength)
    for i in range(len(const.HI)-1):
        print('Plot Lyman',i+1)
        lambda0  = const.HI[i]['wave']
        gamma    = const.HI[i]['gamma']
        strength = const.HI[i]['strength']
        profile  = quasar.model(N,b,wave/(z+1),lambda0,gamma,strength)
        vel      = 2*(wave-lambda0)/(wave+lambda0)*const.c
        ax       = fig.add_subplot(5,6,i+1,xlim=[-dv,dv],ylim=[-0.1,1.3])
        for j in range(len(const.HI)):
            lambda0    = const.HI[j]['wave']
            gamma      = const.HI[j]['gamma']
            strength   = const.HI[j]['strength']
            individual = quasar.model(N,b,wave/(z+1),lambda0,gamma,strength)
            plt.plot(vel,individual,lw=0.1,color='grey',alpha=0.5)
        plt.plot(vel,model,lw=1,color='black')
        plt.plot(vel,profile,lw=1,color='red')
        ax.axvline(x=0,ls='dotted',color='black')
        ax.axhline(y=0,ls='dotted',color='black')
        ax.axhline(y=1,ls='dotted',color='black')
        ax.xaxis.set_major_locator(plt.FixedLocator([-1000,-500,0,500,1000]))
        ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        ax.text(0,1.1,'Lyman-'+str(i+1),ha='center',color='red')
    plt.savefig('lymanseries.pdf') if tbs else plt.show()
    plt.close(fig)
    
def fluxwidth():
    '''
    Voigt profile full width at different flux levels
    '''
    plt.rc('font', size=2, family='serif')
    plt.rc('axes', labelsize=7, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=5)
    plt.rc('ytick', labelsize=5)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)        
    fig = plt.figure(figsize=(8,4))
    ax = plt.subplot(111)
    ax.xaxis.set_major_locator(NullLocator())
    ax.yaxis.set_major_locator(FixedLocator([0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]))
    ref   = 1215.67
    start = ref / (1-(-300)/299792.458)
    end   = ref / (1-(300)/299792.458)
    wave  = numpy.arange(start,end,0.01)
    f = 0
    v = []
    while (f < len(wave)):
        velocity = 299792.458*(wave[f]-ref)/wave[f]
        v.append(velocity)
        f = f + 1
    flux = quasar.p_voigt(14,30,wave,1215.67,6.2650e+08,0.4164)
    plt.plot(v,flux,lw=0.2)
    plt.xlim(-100,100)
    plt.ylim(0,1)
    axvline(x=0, ls='dotted',color='grey',lw=0.2)
    xlabel('Velocity dispersion, in km/s')
    ylabel('Flux')
    minim=[.455,.4,.37,.35,.33,.31,.29,.267,.233]
    maxim=[.545,.6,.63,.65,.67,.69,.71,.733,.767]
    i = 0
    ypos = 0.1
    while (i < len(minim)):
        min_wave = minim[i]*200
        max_wave = maxim[i]*200
        axhline(y=ypos, ls='dotted', color='grey',lw=0.2)
        axhline(y=ypos, xmin=minim[i],xmax=maxim[i], marker='|', color='red',lw=0.3)
        text(0,ypos+0.01,'$'+str(max_wave-min_wave)+'$'+' km/s',fontsize=6,ha='center')
        ypos = ypos + .1
        i = i + 1
    text(-90,.22,'$\log(N_{HI})=14$ $cm^{-2}$'+'\n'+'$b=30$ $km/s$',fontsize=7)
    annotate("",xy=(-21,.2),xytext=(30,.15),arrowprops=dict(arrowstyle="fancy, head_length=2, head_width=1, tail_width=0.8",fc="black",ec="none"))
    annotate("",xy=(20,.2),xytext=(30,.15),arrowprops=dict(arrowstyle="fancy, head_length=2, head_width=1, tail_width=0.8",fc="black",ec="none"))
    text(30,.13,'Equal flux points',fontsize=7)
    plt.savefig('PyD_profile_prog2.pdf') if tbs else plt.show()
    plt.close(fig)

class show_profile:
    '''
    Show Voigt profiles or parabolic curves
    '''
    def __init__(self):
        plt.rc('xtick', labelsize=10)
        plt.rc('ytick', labelsize=10)
        quasar.xdata = numpy.arange(-100,100,0.001)
        quasar.ydata = numpy.array([1]*len(quasar.xdata))
        quasar.fig   = plt.figure(figsize=(12,8))
        quasar.ax    = plt.subplot(111,xlim=[-100,100],ylim=[-0.2,1.2])    
        quasar.prof, = quasar.ax.plot(quasar.xdata,quasar.ydata,color='red',lw=1)
        quasar.ax.axhline(y=0,ls='dotted',lw=1,color='black')
        quasar.fig.canvas.mpl_connect('key_press_event', press)
        plt.show()

    def press(self,event):
        if event.xdata!=None:
            if event.key=='v':
                quasar.addvoigt(event)
                quasar.fig.canvas.draw()
            if event.key=='p':
                quasar.addparab(event)
                quasar.fig.canvas.draw()
            if event.key=='d':
                quasar.delete(event)
                quasar.fig.canvas.draw()
    
    def addvoigt(self):
    
        l    = 988.57780
        f    = 0.000553
        g    = 6.29E6
        N    = 15.34062
        z    = 3.0881097
        b    = 2.2731
        vsig = 2.65
        wmin = l*(z+1)*(1-100/const.c)
        wmax = l*(z+1)*(1+100/const.c)
        wave = numpy.arange(wmin,wmax,0.01)
        v    = (wave-l*(z+1))/wave*const.c
        fl   = quasar.p_voigt(N,b,wave/(z+1),l,g,f)
        cent = int(len(wave)/2)
        dv   = 2*(wave[cent]-wave[cent-1])/(wave[cent]+wave[cent-1])*const.c
        sig  = vsig/dv
        fl   = gaussian_filter1d(fl,sig)
        quasar.voigt, = quasar.ax.plot(v,fl,drawstyle='steps',color='black',lw=1)
        
    def addparab(self,event):
    
        quasar.ydata = quasar.ydata + (quasar.xdata-event.xdata)**2
        quasar.prof.remove()
        quasar.prof, = quasar.ax.plot(quasar.xdata,quasar.ydata,color='red',lw=1)
        quasar.ax.set_ylim(min(quasar.ydata),max(quasar.ydata))
    
def combined():
    '''
    Investigate impact of SNR on combined spectrum and velocity shift
    '''
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig      = plt.figure(1,figsize=(12,8))
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.1, top=0.95, hspace=.25, wspace=0.2)
    disp     = 1.3
    wave     = [3130]
    while wave[-1]<3150:
        wave.append(wave[-1]*(2*const.c+disp)/(2*const.c-disp))
    numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))        
    specinfo = numpy.array([[200,'high'],[20,'low']])
    for i in range(len(specinfo)):
        script   = open('./commands.dat','w')
        script.write('rd wave.dat \n')
        script.write('gp \n')
        script.write('FeII 14 8 0.94910 \n')
        script.write('\n')
        script.write('5.0 \n')
        script.write('noise \n')
        script.write('\n')
        script.write(specinfo[i,0]+'\n')
        script.write('wt '+specinfo[i,1]+'.dat (all)\n')
        script.write('lo\n')
        script.close()
        os.system('rdgen < commands.dat > termout')
        os.system('rm termout')
    wamid = 1608.4506440*(0.94910+1)
    shift = +5
    spec1 = numpy.loadtxt('high.dat')
    wa1   = spec1[:,0]*(2*const.c+shift)/(2*const.c-shift)
    v1    = 2*(wa1-wamid)/(wa1+wamid)*const.c
    fl1   = spec1[:,1]
    er1   = spec1[:,2]
    shift = -5
    spec2 = numpy.loadtxt('low.dat')
    wa2   = spec2[:,0]*(2*const.c+shift)/(2*const.c-shift)
    v2    = 2*(wa2-wamid)/(wa2+wamid)*const.c
    fl2   = spec2[:,1]
    er2   = spec2[:,2]
    ax    = fig.add_subplot(3,1,1,xlim=[-100,100],ylim=[0,1.2])
    ax.plot(v1,fl1,label='SNR=200 pix$^{-1}$\n1 science exposure')
    ax.axvline(x=0,ls='dotted')
    lg = ax.legend(loc=(0.03,0.15),handlelength=2)
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    ax    = fig.add_subplot(3,1,2,xlim=[-100,100],ylim=[0,1.2])
    ax.plot(v2,fl2,label='SNR=20 pix$^{-1}$\n20 science exposures')
    ax.axvline(x=0,ls='dotted')
    lg = ax.legend(loc=(0.03,0.15),handlelength=2)
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    ''' Single high SNR spectrum '''
    ax    = fig.add_subplot(3,1,3,xlim=[-100,100],ylim=[0,1.2])
    data0 = spec.rebin(wa1,fl1,er1,wa=wa1)
    wave  = data0.wa
    vel   = 2*(wave-wamid)/(wave+wamid)*const.c
    flux  = data0.fl
    ax.plot(vel,flux,color='green',label='Single high SNR spectrum')
    data1 = spec.rebin(wa2,fl2,er2,wa=wa1)
    for i in range(20):
        data2 = spec.rebin(wa2,fl2,er2,wa=wa1)
        data1 = spec.combine([data1,data2])
    wave  = data1.wa
    vel   = 2*(wave-wamid)/(wave+wamid)*const.c
    flux  = data1.fl
    ax.plot(vel,flux,color='red',label='Combined low SNR spectra')
    data  = spec.combine([data0,data1])
    wave  = data.wa
    vel   = 2*(wave-wamid)/(wave+wamid)*const.c
    flux  = data.fl
    ax.plot(vel,flux,color='blue',label='Final co-added spectrum')
    ax.axvline(x=0,ls='dotted')
    lg = ax.legend(loc=(0.03,0.15),handlelength=2)
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    plt.savefig('plot.pdf') if tbs else plt.show()
    plt.close(fig)

def continuum():
    '''
    Comparison between over and underfitted continuum
    '''
    atompar  = numpy.loadtxt('atompar.dat', usecols=(0,1,2,3,4,5),dtype='string')
    plt.rc('font', size=2)
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=4)
    plt.rc('ytick', labelsize=4)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(figsize=(8,10))
    subplots_adjust(left=0.05, right=0.95, bottom=0.02, top=0.98, wspace=None, hspace=None)
    continuum = 500
    dhratio   = -4.55
    lhi       = float(atompar[0,2])
    ldi       = float(atompar[328,2])
    gammahi   = float(atompar[0,4])
    gammadi   = float(atompar[328,4])
    fhi       = float(atompar[0,3])
    fdi       = float(atompar[328,3])
    width     = [150,150,150,150,200,400,600]
    col_arr   = [12,13,14,16,17,18,18.5]
    h_under_col = [11.3,12.96,14,16,17,17.97,18.5]
    d_under_col = [11.3,12.96,14,14,16.85,18,18.5]
    h_exact_col = [12,13,14,16,17,18,18.5]
    d_exact_col = [12,13,14,16,17,18,18.5]
    h_over_col  = [12.25,13.03,14,16,17,18,18.5]
    d_over_col  = [12.25,13.03,14,16.57,17.1,18.01,18.5]
    p = len(col_arr)
    i = 0
    k = 0
    while (i < len(col_arr)):
        col,hcol1,hcol2,hcol3, = col_arr[i],h_under_col[i],h_exact_col[i],h_over_col[i]
        col,dcol1,dcol2,dcol3, = col_arr[i],d_under_col[i],d_exact_col[i],d_over_col[i]
        inter = width[i]
        k = k + 1
        ax2  = fig.add_subplot(p,3,k,xlim=[-inter,inter],ylim=[0,1.2])
        ax2.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        ref   = lhi
        start = ref / (1-(-inter)/299792.458)
        end   = ref / (1-(inter)/299792.458)
        wave  = numpy.arange(start,end,0.01)
        f = 0
        v = []
        while (f < len(wave)):
            velocity = 299792.458*(wave[f]-ref)/wave[f]
            v.append(velocity)
            f = f + 1
        flx_voigt = quasar.p_voigt(col,15,wave,lhi,gammahi,fhi)*continuum*quasar.p_voigt(col+dhratio,15,wave,ldi,gammadi,fdi)
        fit_voigt = quasar.p_voigt(hcol1,15,wave,lhi,gammahi,fhi)*quasar.p_voigt(dcol1+dhratio,15,wave,ldi,gammadi,fdi)
        plt.plot(v,flx_voigt/(continuum-20),color='black',label='Normalized profile',lw=0.2)
        plt.plot(v,fit_voigt,color='red',label='Best fit with under-estimated continuum',lw=0.2)
        axhline(y=1  , ls='dotted', color='grey', lw=0.2)
        if (i == 0):
            lg = legend(loc=(0.03,0.1),handlelength=2,prop={"size":6})
            fr = lg.get_frame()
            fr.set_lw(0.0)
            title('Under-estimated Voigt profile',fontsize=7)
        if (i < 3):
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,0.4,'log($N_{HI}$)='+str(hcol1),color='red',fontsize=6)
        if (i == 3):
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            axvline(x=-82  , ls='dotted',color='grey', lw=0.2)
            ax2.annotate("",xy=(-82,0.9),xytext=(-82,0.6),arrowprops=dict(fc="red",ec="none"))
            text(-125,0.45,'deuterium',color='red',fontsize=6,weight='bold')
            text(-105,0.35,'lost',color='red',fontsize=6,weight='bold')
            text(3*inter/10,0.4,'log($N_{HI}$)='+str(hcol1),color='red',fontsize=6)
        if (i > 3):
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            axvline(x=-82  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,0.4,'log($N_{HI}$)='+str(hcol1),color='red',fontsize=6)
            text(3*inter/10,0.25,'log(D/H)='+str(dcol1+dhratio-hcol1),color='red',fontsize=6)
        k = k + 1
        ax  = fig.add_subplot(p,3,k,xlim=[-inter,inter],ylim=[0,continuum+100])
        ax.yaxis.set_major_locator(plt.FixedLocator([0,continuum]))
        ref   = lhi
        start = ref / (1-(-inter)/299792.458)
        end   = ref / (1-(inter)/299792.458)
        wave  = numpy.arange(start,end,0.01)
        f = 0
        v = []
        while (f < len(wave)):
            velocity = 299792.458*(wave[f]-ref)/wave[f]
            v.append(velocity)
            f = f + 1
        flx_voigt = quasar.p_voigt(col,15,wave,lhi,gammahi,fhi)*continuum*quasar.p_voigt(col+dhratio,15,wave,ldi,gammadi,fdi)
        axhline(y=continuum  , ls='dashed',label='Best continuum', color='blue', lw=0.2)
        plt.plot(v,flx_voigt,'black',label='Non-normalized profile',lw=0.2)
        axhline(y=continuum-20  , ls='dashed',label='Under-estimated continuum (4% below)', color='red', lw=0.2)
        axhline(y=continuum+20  , ls='dashed',label='Over-estimated continuum (4% above)', color='green', lw=0.2)
        if (i == 0):
            lg = legend(loc=(0.03,0.1),handlelength=2,prop={"size":6})
            fr = lg.get_frame()
            fr.set_lw(0.0)
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,350,'log($N_{HI}$)='+str(col),color='black',fontsize=6)
            title('Non-normalized Voigt profile',fontsize=7)
        if ((i > 0) and (i < 3)):
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,200,'log($N_{HI}$)='+str(col),color='black',fontsize=6)
        if (i >= 3):
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            axvline(x=-82  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,200,'log($N_{HI}$)='+str(col),color='black',fontsize=6)
            text(3*inter/10,130,'log(D/H)='+str(col+dhratio-col),color='black',fontsize=6)
        k = k + 1
        ax4  = fig.add_subplot(p,3,k,xlim=[-inter,inter],ylim=[0,1.2])
        ax4.yaxis.set_major_locator(plt.FixedLocator([0,1]))
        ref   = lhi
        start = ref / (1-(-inter)/299792.458)
        end   = ref / (1-(inter)/299792.458)
        wave  = numpy.arange(start,end,0.01)
        f = 0
        v = []
        while (f < len(wave)):
            velocity = 299792.458*(wave[f]-ref)/wave[f]
            v.append(velocity)
            f = f + 1
        flx_voigt = quasar.p_voigt(col,15,wave,lhi,gammahi,fhi)*continuum*quasar.p_voigt(col+dhratio,15,wave,ldi,gammadi,fdi)
        fit_voigt = quasar.p_voigt(hcol3,15,wave,lhi,gammahi,fhi)*quasar.p_voigt(dcol3+dhratio,15,wave,ldi,gammadi,fdi)
        plt.plot(v,flx_voigt/(continuum+20),color='black',label='Normalized profile',lw=0.2)
        plt.plot(v,fit_voigt,color='green',label='Best fit with over-estimated continuum',lw=0.2)
        axhline(y=1  , ls='dotted', color='grey', lw=0.2)
        if (i == 0):
            lg = legend(loc=(0.03,0.1),handlelength=2,prop={"size":6})
            fr = lg.get_frame()
            fr.set_lw(0.0)
            title('Over-estimated Voigt profile',fontsize=7)
        if (i < 3):
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,0.4,'log($N_{HI}$)='+str(hcol3),color='green',fontsize=6)
        else:
            axvline(x=0  , ls='dotted',color='grey', lw=0.2)
            axvline(x=-82  , ls='dotted',color='grey', lw=0.2)
            text(3*inter/10,0.4,'log($N_{HI}$)='+str(hcol3),color='green',fontsize=6)
            text(3*inter/10,0.25,'log(D/H)='+str(dcol3+dhratio-hcol3),color='green',fontsize=6)
        i = i + 1
    plt.savefig('PyD_profile_D2Hcontinuum.pdf') if tbs else plt.show()
    plt.close(fig)

def zoom():
    '''
    Zoom plot of inequal continuum normalised regions
    '''
    atompar  = numpy.loadtxt(quasar.datapath+'atompar.dat', usecols=(0,1,2,3,4,5),dtype='string')
    locator_params(tight=True, nbins=12)
    ###### parameters for plot ########
    plt.rc('font', size=2)
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)        
    fig = plt.figure(figsize=(8,10))
    ax  = fig.add_subplot(3,1,1)
    ###### plot all spectrum ######
    table    = numpy.loadtxt('PyD_profile_zoom/J095500-013004.dat', usecols=(0,1))
    idx_name = 'J095500-013004'
    z_em     = 4.500
    k = 0
    y_temp = []
    while (k < len(table)):
        y_temp.append(table[k,1])
        k = k + 1
    y_temp.sort()
    max_flx = y_temp[len(y_temp)-5]
    max_flx = 2000
    plt.plot(table[:,0],table[:,1],color='black',lw=0.2)
    #xlim([min(table[:,0]),max(table[:,0])])
    plt.xlim(4500,7500)
    xlabel("Emitted wavelength in $\AA$")
    plt.ylim([0,max_flx])
    ylabel("Flux")
    letter = [r'$\alpha$',r'$\beta$',r'$\gamma$',r'$\delta$',r'$\epsilon$',r'$\zeta$',r'$\eta$',r'$\theta$']
    #axvline(x=(z_em+1)*float(atompar[0,2]),ls='dotted',color='red',lw=0.2,label='Lyman-'+letter[0]+', 1215.67')
    #axvline(x=(z_em+1)*float(atompar[1,2]),ls='dotted',color='green',lw=0.2,label='Lyman-'+letter[1]+', 1025.72')
    #axvline(x=(z_em+1)*float(atompar[2,2]),ls='dotted',color='blue',lw=0.2,label='Lyman-'+letter[2]+', 972.54')
    #axvline(x=(z_em+1)*float(atompar[3,2]),ls='dotted',color='purple',lw=0.2,label='Lyman-'+letter[3]+', 949.74')
    #axvline(x=(z_em+1)*float(atompar[38,2]),color='yellow',lw=0.2,label='Lyman limit'+', 912.32')
    #text(6500,1720,idx_name+'     $z_{em}$='+str(z_em),color='blue',fontsize=10)
    #ax.yaxis.set_major_locator(pylab.NullLocator())
    #title(idx_name+'     $z_{em}$='+str(z_em),fontsize=10)
    #lg = legend(loc=(0.57,0.45),handlelength=2,prop={"size":7})
    #fr = lg.get_frame()
    #fr.set_lw(0.0)
    axhline(y=280,ls='dotted',color='red')
    axvline(x=4778.86,color='red')
    axvline(x=5830.56,color='red')
    ax.yaxis.set_major_locator(plt.FixedLocator([0,280,500,1000,2000]))
    text(4900,1600,idx_name,color='blue',fontsize=10)
    a = axes([.197,.73,.272,.08])
    plt.plot(table[:,0],table[:,1],color='black',lw=0.2)
    setp(a, xlim=(4778.86,5830.56),ylim=(0,16), xticks=[])
    axhline(y=9,ls='dotted',color='red')    
    plt.savefig('PyD_profile_zoom.pdf') if tbs else plt.show()
    plt.close(fig)

def gamma():
    '''
    Profile comparison for different Gamma values
    '''
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    test  = numpy.array([[2.68E+08,0.68E+08],
                      [2.68E+08,1.68E+08],
                      [2.68E+08,3.68E+08],
                      [2.68E+08,4.68E+08]])
    fig = plt.figure(1,figsize=(12,8))
    plt.subplots_adjust(left=0.06, right=0.96, bottom=0.1, top=0.9, hspace=.25, wspace=0.15)
    title('Voigt profile testing with different $\Gamma$ parameter for MgII 2796\n')
    axis('off')
    lambda0  = 2796.3550990
    strength = 0.486245
    N,b      = 12,10
    for i in range(len(test)):
        dv    = 250
        wmin  = lambda0 / (1 + (dv/const.c))
        wmax  = lambda0 / (1 - (dv/const.c))
        wave  = numpy.arange(wmin,wmax,0.0002)
        v     = (wave-lambda0)/wave*300000.
        ax    = fig.add_subplot(2,2,i+1,xlim=[-200,200],ylim=[-0.1,1.6])
        ''' Plotting Voigt profile using published gamma value '''
        gamma = test[i,0]
        flx1  = quasar.p_voigt(N,b,wave,lambda0,gamma,strength)
        p1,   = plt.plot(v,flx1,lw=4,color='red',alpha=0.7)
        ''' Plotting Voigt profile using customised gamma value '''
        gamma = test[i,1]
        flx2  = quasar.p_voigt(N,b,wave,lambda0,gamma,strength)
        p2,   = plt.plot(v,flx2,lw=2,color='black',alpha=0.7)
        ''' Plot residuals '''
        diff  = flx2-flx1
        delta = max([abs(j) for j in diff])
        diff  = diff/delta/10+1.4        
        p3,   = plt.plot(v,diff,lw=1,color='magenta',alpha=0.7)
        ''' Setup axis and labels '''
        text(25,0.3,'N=%.2f & b=%.2f'%(N,b),ha='left',fontsize=10)
        ax.text(-200,1.3,r'$-%.5f$ '%delta,ha='right',va='center',size=8)
        ax.text(-200,1.5,r'$+%.5f$ '%delta,ha='right',va='center',size=8)
        curve = [p1,p2,p3]
        label = [r'$\Gamma=%.2E$'%test[i,0],
                 r'$\Gamma=%.2E$'%test[i,1],
                 'Residuals']
        ax.legend(curve,label,numpoints=2,handlelength=3,frameon=False,
                  prop={'size':8},loc='lower left',bbox_to_anchor=[0.01,0.12],ncol=1)
        ax.axhline(y=0,ls='dotted',color='black')
        ax.axvline(x=0,ls='dotted',color='black')
        ax.axhline(y=1,ls='dotted',color='black')
        ax.axhline(y=1.3,ls='dotted',color='magenta')
        ax.axhline(y=1.4,ls='dotted',color='magenta')
        ax.axhline(y=1.5,ls='dotted',color='magenta')
        ax.set_ylabel('Flux')
        ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    plt.savefig('gamma.pdf') if tbs else plt.show()
    plt.close(fig)    

def gamma2():
    '''
    Profile comparison for different Gamma values
    '''
    plt.rc('font', size=10)
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111,xlim=[-200,200],ylim=[-0.1,1.1])
    lambda0  = 1215.6701
    strength = 0.4164
    dv       = 250
    wmin     = lambda0 / (1 + (dv/const.c))
    wmax     = lambda0 / (1 - (dv/const.c))
    wave     = numpy.arange(wmin,wmax,0.0002)
    v        = (wave-lambda0)/wave*300000.
    gamma    = 4.2650e+08
    flux     = quasar.p_voigt(17,20,wave,lambda0,gamma,strength)
    plt.plot(v,flux,lw=2.5,color='red',label=r'$\Gamma=%.4E$'%gamma,alpha=0.6)
    gamma    = 6.2650e+08
    flux     = quasar.p_voigt(17,20,wave,lambda0,gamma,strength)
    plt.plot(v,flux,lw=2.5,color='black',label=r'$\Gamma=%.4E$ (real)'%gamma,alpha=0.6)
    gamma    = 8.2650e+08
    flux     = quasar.p_voigt(17,20,wave,lambda0,gamma,strength)
    plt.plot(v,flux,lw=2.5,color='green',label=r'$\Gamma=%.4E$'%gamma,alpha=0.6)
    lg = ax.legend(loc=(0.03,0.15),handlelength=2,prop={"size":10})
    fr = lg.get_frame()
    lg.get_frame().set_fill(False)
    fr.set_lw(0.0)
    axvline(x=0, ls='dotted',color='grey',lw=0.2)
    axhline(y=0, ls='dotted',color='grey',lw=0.2)
    axhline(y=1, ls='dotted',color='grey',lw=0.2)
    savefig('gamma.pdf') if tbs else plt.show()

def isotope():
    '''
    Voigt profile of simulated isotopic lines
    '''
    plt.rc('font', size=10, family='sans-serif')
    plt.rc('axes', labelsize=10, linewidth=0.2)
    plt.rc('legend', fontsize=10, handlelength=10)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(1,figsize=(12,8))
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.1, top=0.95, hspace=.25, wspace=0.2)
    wave  = numpy.arange(1460,1470,0.0001)
    data  = numpy.loadtxt('isoprof.dat')
    i,k   = 0,1
    while i<len(data):
        j = 0
        model = 1
        ax = fig.add_subplot(2,2,k,xlim=[-5,5],ylim=[0,1])
        wamid = data[i+2,0]
        v  = 2*(wave-wamid)/(wave+wamid)*const.c
        ypos = 0.3
        while j<4:
            w = data[i,0]
            f = data[i,1]
            g = data[i,2]
            m = data[i,3]
            a = data[i,-1]
            profile = quasar.p_voigt(12.5,2,wave,w,g,f)
            ax.plot(v,profile,color='black',lw=2,alpha=0.7)
            ax.axvline(x=2*(w-wamid)/(w+wamid)*const.c,color='black',ls='dotted')
            model = model*profile
            ax.text(-4.5,ypos,'$\lambda_{%.0f}=%.4f$ ; $a_{%.0f}=%.4f$'%(m,w,m,a),fontsize=10)
            i = i + 1
            j = j + 1
            ypos = ypos - 0.07
        ax.plot(v,model,color='red',lw=2,alpha=0.7)
        xmin = v[abs(model-min(model)).argmin()]
        ax.axvline(x=xmin,color='red',ls='dashed')
        ax.text(0.6,0.12,'Minimum of the convolved\nmodel at %.3f km/s'%xmin,fontsize=10)
        ax.set_xlabel('Velocity relative to $\lambda_{56}$ (km/s)',fontsize=12)
        k = k + 1
    plt.savefig('isoprof.pdf') if tbs else plt.show()

def landscape():
    '''
    Combined DI/HI profiles down to Lyman 14
    '''
    plt.rc('font', size=7, family='serif')
    plt.rc('axes', labelsize=7, linewidth=0.2)
    plt.rc('legend', fontsize=7, handlelength=5)
    plt.rc('xtick', labelsize=5)
    plt.rc('ytick', labelsize=5)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2) 
    col   = [15,16.5,17.5,19.5,21,22]
    dop   = [10,20,30,40]
    fig   = plt.figure(figsize=(12,20))
    title = 'PyD_profile_D2H.pdf'
    shape = 'landscape'
    subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98, wspace=None, hspace=None)
    letter  = [r'$\alpha$',r'$\beta$',r'$\gamma$',r'$\delta$',r'$\epsilon$',r'$\zeta$',r'$\eta$',r'$\theta$','8','9','10','11','12','13','14']
    i       = 0
    while (i < len(col)):                   # for each column density...
        j = 0
        idx = i + 1
        while (j < len(quasar.HI)):                      # ...and each transition...
            ax = fig.add_subplot(len(quasar.HI),len(col),idx,xlim=[-300,200],ylim=[-0.15,1.3])
            text(-270,1.1,'Ly-'+letter[j],fontsize=8)
            text(10,1.1,'log($N_{HI}$)='+str(col[i]),fontsize=5)
            wmin = quasar.HI[j]['wave']*(1-500/const.c)
            wmax = quasar.HI[j]['wave']*(1+500/const.c)
            wave = numpy.arange(wmin,wmax,0.01)
            v    = (wave-quasar.HI[j]['wave'])/quasar.HI[j]['wave']*const.c
            k = 0
            while (k < len(dop)):           # ...plot the different profiles for each b values
                vhfix  = quasar.p_voigt(col[i],dop[k],wave,quasar.HI[j]['wave'],quasar.HI[j]['gamma'],quasar.HI[j]['strength'])
                center = int(len(wave)/2)
                dv     = (wave[center]-wave[center-1])/((wave[center]+wave[center-1])/2)*const.c
                val    = 2.5*1/dv
                vhfix  = gaussian_filter1d(vhfix,val)
                vdfix = quasar.p_voigt(col[i]+quasar.dhratio,dop[k],wave,quasar.DI[j]['wave'],quasar.DI[j]['gamma'],quasar.DI[j]['strength'])
                center = int(len(wave)/2)
                dv     = (wave[center]-wave[center-1])/((wave[center]+wave[center-1])/2)*const.c
                val    = 2.5*1/dv
                vdfix  = gaussian_filter1d(vdfix,val)
                flux = vhfix*vdfix
                plt.plot(v,flux,lw=1,label='b='+str(dop[k]))
                lg = ax.legend(loc=(0.03,0.15),handlelength=2,prop={"size":4})
                fr = lg.get_frame()
                lg.get_frame().set_fill(False)
                fr.set_lw(0.0)
                ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
                axvline(x=-82, ls='dotted',color='grey',lw=0.2)
                axvline(x=0, ls='dotted',color='grey',lw=0.2)
                axhline(y=0, ls='dotted',color='grey',lw=0.2)
                axhline(y=1, ls='dotted',color='grey',lw=0.2)
                k = k + 1
            idx = idx + len(col)
            j = j + 1
        i = i + 1
    savefig(title,orientation=shape,transparent='True') if tbs else plt.show()

def molecular(args):
    '''
    Show artificial spectrum of molecular lines and do stacking
    '''
    plt.rc('font', size=9, family='sans-serif')
    plt.rc('axes', labelsize=9, linewidth=0.2)
    plt.rc('legend', fontsize=9, handlelength=9)
    plt.rc('xtick', labelsize=9)
    plt.rc('ytick', labelsize=9)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)
    fig = plt.figure(1,figsize=(12,6))
    plt.subplots_adjust(left=0.05, right=0.96, bottom=0.1, top=0.95, hspace=0, wspace=0)
    R    = 20000.
    disp = const.c/R/(2*numpy.sqrt(2*math.log(2)))
    fwhm = const.c/R
    wave = [1140]
    while wave[-1]<1450:
        wave.append(wave[-1]*(2*const.c+disp)/(2*const.c-disp))
    numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))        
    N,b,z = 13.3,8.,0
    script = open('./commands.dat','w')
    script.write('rd wave.dat \n')
    script.write('gp \n')
    script.write('H2I %f %f %f \n'%(N,b,z))
    script.write('\n')
    script.write('%f \n'%fwhm)
    script.write('noise \n')
    script.write('\n')
    script.write('10\n')
    script.write('wt spec.dat (all)\n')
    script.write('lo\n')
    script.close()
    os.system('rdgen < commands.dat > termout')
    os.system('rm termout')
    H2I   = numpy.loadtxt('atom.dat',usecols=(1,2,3),dtype=float)
    data  = numpy.loadtxt('spec.dat')
    wave  = data[:,0]
    flux  = data[:,1]
    error = data[:,2]
    print('|- Plot whole spectrum...')
    ax    = fig.add_subplot(4,1,1,xlim=[wave[0],wave[-1]],ylim=[-0.2,1.4])
    ax.plot(wave,flux,color='black')
    ax.axvline(x=0,color='black',ls='dotted')
    ax.axhline(y=0,color='black',ls='dotted')
    ax.axhline(y=1,color='black',ls='dotted')
    ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
    plt.xlabel(r'Wavelength (in $\AA$)')
    for i in range(len(H2I)):
        ax.plot([H2I[i,0],H2I[i,0]],[1.2,1.3],color='red',lw=0.1)
    print('|- Combine molecular line...')
    n     = 0
    pos   = [9,10,11,12,13,17,18,19,20,21]
    wmin  = H2I[0,0]-10
    wmid  = H2I[0,0]
    wmax  = H2I[0,0]+10
    imin  = abs(wave-wmin).argmin()
    imax  = abs(wave-wmax).argmin()    
    zmid  = 2000./wmid-1
    wave0 = wave[imin:imax]*(zmid+1)
    data  = spec.rebin(wave0,flux[imin:imax],error[imin:imax],wa=wave0)
    for i in range(len(H2I)):
        print('{0:>5} / {1:<5}'.format(i+1,len(H2I)))
        wmin  = H2I[i,0]-10
        wmid  = H2I[i,0]
        wmax  = H2I[i,0]+10
        imin  = abs(wave-wmin).argmin()
        imax  = abs(wave-wmax).argmin()    
        zmid  = 2000./wmid-1
        wave1 = wave[imin:imax]*(zmid+1)
        rebin = spec.rebin(wave1,flux[imin:imax],error[imin:imax],wa=wave0)
        data  = spec.combine([data,rebin])
        if H2I[i,0] in [1313.37643,1324.59501,1345.17788,1356.48760,1371.42241,
                        1389.59379,1410.64777,1383.65916,1403.98260,1427.01340]:
            zlist = wave1/2000.-1
            vlist = (((zlist+1)**2-1)/((zlist+1)**2+1))*const.c
            ax = fig.add_subplot(3,8,pos[n],xlim=[-75,75],ylim=[-0.2,1.4])
            ax.plot(vlist,flux[imin:imax],color='black')
            ax.axvline(x=0,color='black',ls='dotted')
            ax.axhline(y=0,color='black',ls='dotted')
            ax.axhline(y=1,color='black',ls='dotted')
            ax.text(0,1.2,'H2I %.2f'%H2I[i,0],ha='center',va='bottom',fontsize=8,color='blue')
            ax.xaxis.set_major_locator(plt.FixedLocator([-50,0,50]))
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
            if pos[n] not in [9,17]:
                plt.setp(ax.get_yticklabels(), visible=False)
            if pos[n] in [9,10,11,12,13,14]:
                plt.setp(ax.get_xticklabels(), visible=False)
            if pos[n]==19:
                plt.xlabel(r'Velocity dispersion (in km/s)')
            n += 1
    print('|- Plot stacked molecular line')
    ax    = plt.subplot2grid((3,6),(1,4),rowspan=2,colspan=2,xlim=[-75,75],ylim=[0.9,1.02])
    zlist = data.wa/2000.-1
    vlist = (((zlist+1)**2-1)/((zlist+1)**2+1))*const.c
    ax.plot(vlist,data.fl,color='black',label='Stack molecular line regions')    
    ax.xaxis.set_major_locator(plt.FixedLocator([-50,-25,0,25,50]))
    ax.axvline(x=0,color='black',ls='dotted')
    ax.axhline(y=0,color='black',ls='dotted')
    ax.axhline(y=1,color='black',ls='dotted')
    plt.xlabel(r'Velocity dispersion (in km/s)')
    plt.savefig('plot.pdf')

def saturation():
    '''
    Lyman series saturation for Lyman alpha forest type system
    '''
    plt.rc('font', size=2)
    plt.rc('axes', labelsize=2, linewidth=.4)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=4)
    plt.rc('ytick', labelsize=4)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)        
    fig = plt.figure(figsize=(5,2))
    subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98, wspace=0, hspace=0)
    atompar  = numpy.loadtxt(quasar.datapath+'atompar.dat', usecols=(0,1,2,3,4,5),dtype='string')
    dhratio = -4.55
    #pos_plot = [1,6,11,2,7,12,3,8,13,4,9,14,5,10,15]
    pos_plot = [1,5,9,2,6,10,3,7,11,4,8,12]
    letter   = [r'$\alpha$',r'$\beta$',r'$\gamma$',r'$\delta$',r'$\epsilon$','$6$','$7$','$8$','$9$','$10$','$11$','$12$','$13$','$14$','$15$']
    p = 0
    while (p < 12):
        ref   = float(atompar[p,2])
        start = ref / (1-(-200)/299792.458)
        end   = ref / (1-(200)/299792.458)
        wave  = numpy.arange(start,end,0.01)
        f = 0
        v = []
        while (f < len(wave)):
            velocity = 299792.458*(wave[f]-ref)/wave[f]
            v.append(velocity)
            f = f + 1
        lhi     = float(atompar[p,2])
        ldi     = float(atompar[p+328,2])
        gammahi = float(atompar[p,4])
        gammadi = float(atompar[p+328,4])
        fhi     = float(atompar[p,3])
        fdi     = float(atompar[p+328,3])
        flux = quasar.p_voigt(16.5,10,wave,lhi,gammahi,fhi)*quasar.p_voigt(16.5+dhratio,10,wave,ldi,gammadi,fdi)
        ax = fig.add_subplot(3,4,pos_plot[p],xlim=[-150,150],ylim=[0,1.4])
        plt.plot(v,flux,color='blue',lw=.5)
        ax.yaxis.set_major_locator(pylab.NullLocator())
        ax.xaxis.set_major_locator(pylab.NullLocator())
        axvline(x=-82, ls='dotted',color='grey',lw=.6)
        axvline(x=0, ls='dotted',color='grey',lw=.6)
        axhline(y=1, color='grey',lw=.6)
        #text1 = str(atompar[p,1]).split('_')
        #l_pos = "$"+str('%4.2f'%float(atompar[p,2]))+"$"
        text(0,1.12,'Ly-'+letter[p],color='black',fontsize=9,ha='center')
        #text(0,1.1,text1[0]+' '+l_pos,color='black',fontsize=9)
        p = p + 1
    savefig('PyD_profile_sat.pdf',transparent='True') if tbs else plt.show()

def separated():
    '''
    Individual and combined DI and HI profiles
    '''
    fig = plt.figure(figsize=(8,10))
    plt.rc('font', size=2)
    plt.rc('axes', labelsize=2, linewidth=0.2)
    plt.rc('legend', fontsize=2, handlelength=10)
    plt.rc('xtick', labelsize=4)
    plt.rc('ytick', labelsize=4)
    plt.rc('lines', lw=0.2, mew=0.2)
    plt.rc('grid', linewidth=0.2)        
    subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98, wspace=None, hspace=None)
    dhratio = -4.55
    atompar = n.loadtxt('atompar.dat', usecols=(2,4,3))
    letter  = [r'$\alpha$',r'$\beta$',r'$\gamma$',r'$\delta$',r'$\epsilon$',r'$\zeta$',r'$\eta$',r'$\theta$']
    col     = [17,17.5,18,18.5]
    dop     = [10,14,18,22,26,30]
    i       = 0
    while (i < len(col)):
        j = 0
        idx = i+1
        while (j < len(dop)):
            ax = fig.add_subplot(6,4,idx,xlim=[-300,300],ylim=[-0.15,1.3])
            wabeg = atompar[0,0]*(1-500/const.c)
            waend = atompar[0,0]*(1+500/const.c)
            wave  = numpy.arange(wabeg,waend,0.01)
            v     = (wave-atompar[0,0])/atompar[0,0]*const.c
            vhfix = quasar.p_voigt(col[i],dop[j],wave,atompar[0,0],atompar[0,1],atompar[0,2])
            vdfix = quasar.p_voigt(col[i]+dhratio,dop[j],wave,atompar[328,0],atompar[328,1],atompar[328,2])
            flux1 = vhfix*vdfix
            flux2 = quasar.p_voigt(col[i],dop[j],wave,atompar[0,0],atompar[0,1],atompar[0,2])
            flux3 = quasar.p_voigt(col[i]+dhratio,dop[j],wave,atompar[328,0],atompar[328,1],atompar[328,2])
            plt.plot(v,flux1,lw=0.2,label='DI+HI')
            plt.plot(v,flux2,lw=0.2,label='HI')
            plt.plot(v,flux3,lw=0.2,label='DI')
            lg = ax.legend(loc=(0.03,0.15),handlelength=2,prop={"size":4})
            fr = lg.get_frame()
            fr.set_lw(0.0)
            ax.yaxis.set_major_locator(NullLocator())
            axvline(x=-82, ls='dotted',color='grey',lw=0.2)
            axvline(x=0, ls='dotted',color='grey',lw=0.2)
            axhline(y=0, ls='dotted',color='grey',lw=0.2)
            axhline(y=1, ls='dotted',color='grey',lw=0.2)        
            text(-300,1.1,'   log($N_{HI}$)='+str(col[i])+'                              b='+str(dop[j]),fontsize=5)
            idx = idx + 4
            j = j + 1
        i = i + 1
    savefig('PyD_profile_D2Hseparated.pdf') if tbs else plt.show()

