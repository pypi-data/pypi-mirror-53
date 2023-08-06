import matplotlib,os,sys,re,math,datetime,operator,random,ctypes,binascii,numpy
import matplotlib                    as mpl
import matplotlib.dates              as mdates
import matplotlib.pyplot             as plt
from matplotlib.pyplot               import *
from pylab                           import *
from matplotlib                      import rc
from matplotlib._png                 import read_png
from matplotlib.offsetbox            import AnnotationBbox, OffsetImage
from mpl_toolkits.axes_grid1         import make_axes_locatable
from scipy                           import optimize,stats
from scipy.optimize                  import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
from time                            import clock
from scipy.ndimage                   import gaussian_filter1d
import pandas                        as pd
from astropy.io                      import fits

class MetalPlot:
    '''
    Absorber kinematics plots
    '''
    rc('font', size=2, family='sans-serif')
    rc('axes', labelsize=8, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=10)
    rc('ytick', labelsize=10)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    home     = os.getenv('HOME')+'/ASTRO/analysis/alpha'
    here     = os.getenv('PWD')
    pathdata = os.path.abspath(__file__).rsplit('/',1)[0] + '/data/'
    c        = 299792.458
    args     = numpy.array(sys.argv, dtype='str')
    binning  = 8 if '--bin' not in sys.argv else int(args[numpy.where(args=='--bin')[0][0]+1])

    def __init__(self):

        self.atom = self.makeatomlist(pathdata+'atom.dat')
        self.plotwidth()
        self.plotwidthperion()
    
    def isfloat(self,value):
        try:
          float(value)
          return True
        except ValueError:
          return False
    
    def atominfo(self,atomID):
        '''
        Get atomic data from selected atomID
        '''
        target = [0,0,0,0,0]
        atomID = atomID.split('_')
        for i in range(len(self.atom)):
            element     = self.atom[i,0]
            wavelength  = self.atom[i,1]
            oscillator  = self.atom[i,2]
            gammavalue  = self.atom[i,3]
            qcoeff      = self.atom[i,5]
            if (len(atomID)>1 and element==atomID[0] \
                and abs(float(wavelength)-float(atomID[1]))<abs(float(target[1])-float(atomID[1]))) \
                or (len(atomID)==1 and element==atomID[0]):
               target = [element,wavelength,oscillator,gammavalue,qcoeff] 
        if target==[0,0,0,0,0]:
            print atomID,'not identifiable...'
            quit()
        return target
    
    def makeatomlist(self,atompath):
        '''
        Store data from atom.dat
        '''
        atom   = numpy.empty((0,6))
        atomdat     = numpy.loadtxt(atompath,dtype='str',delimiter='\n')
        for element in atomdat:
            l       = element.split()
            i       = 0      if len(l[0])>1 else 1
            species = l[0]   if len(l[0])>1 else l[0]+l[1]
            wave    = 0 if len(l)<i+2 else 0 if isfloat(l[i+1])==False else l[i+1]
            f       = 0 if len(l)<i+3 else 0 if isfloat(l[i+2])==False else l[i+2]
            gamma   = 0 if len(l)<i+4 else 0 if isfloat(l[i+3])==False else l[i+3]
            mass    = 0 if len(l)<i+5 else 0 if isfloat(l[i+4])==False else l[i+4]
            alpha   = 0 if len(l)<i+6 else 0 if isfloat(l[i+5])==False else l[i+5]
            if species not in ['>>','<<','<>','__']:
                atom = numpy.vstack((atom,[species,wave,f,gamma,mass,alpha]))
        return atom
    
    def getmetals(self):
    
        data = np.empty((0,9),dtype=float)
        bparamarr = []
        densityparamarr=[]
        zabsarr = []
        metals = np.array([['MgII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['FeII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['SiII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['AlII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['CrII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['NiII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['AlIII',np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)],
                           ['MnII' ,np.empty((0,1),dtype=str),np.empty((0,6),dtype=float)]
                           ],dtype=object)
        #For each metal: ['ion',[filename],[tied components, EW average over all transitions,
        # self.zabs, SNR over all transitions, number of transitions, min/max wavelength of transition]]
        fitdata =np.array([['MgII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,2),dtype=float)],
                           ['FeII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,6),dtype=float)],
                           ['SiII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,2),dtype=float)],
                           ['AlII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,1),dtype=float)],
                           ['CrII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,3),dtype=float)],
                           ['NiII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,3),dtype=float)],
                           ['AlIII',np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,2),dtype=float)],
                           ['MnII' ,np.empty((0,1),dtype=float),np.empty((0,3),dtype=float),np.empty((0,2),dtype=float)]
                           ],dtype=object)
        #For each fit: ['ion',[redshift],[z,N,b],[transitions]]
        #fitdata[a,b]
        #a is the ion number
        #b is the index where 0 is ion name, 1 is redshift array, and 2 is z,N,b array
                #print fitdata[0,2][:,0]
        snarr =  np.array([['MgII_2796' ,np.empty((0,2),dtype=float)],
                           ['FeII_2382' ,np.empty((0,2),dtype=float)],
                           ['SiII_1526' ,np.empty((0,2),dtype=float)],
                           ['AlII_1670' ,np.empty((0,2),dtype=float)]
                           ],dtype=object)
        #For each transition (strongest): ['transition',[z,snr]]
        transitions = [['MgII_2796', 'MgII_2803'],
                       ['FeII_2382', 'FeII_2600','FeII_2344','FeII_1608','FeII_2586', 'FeII_2374'],
                       ['SiII_1526', 'SiII_1808'],['AlII_1670'],['CrII_2056', 'CrII_2062', 'CrII_2066'],
                       ['NiII_1709', 'NiII_1741', 'NiII_1751'],
                       ['AlIII_1854', 'AlIII_1862'],
                       ['MnII_2594', 'MnII_2606']]
        for system in np.loadtxt(self.pathdata+'metallist.dat',dtype=str):
            self.quasar   = system.split('/')[0]
            self.zabs     = float(system.split('/')[1])
            self.sample   = system.split('/')[2]
            self.distpath = '../pubsys/'+system+'/'
            if os.path.exists(self.distpath+'chunks/vpfit_chunk001.txt')==True:
                dv   = []
                k    = 0
                tied = 0
                flag = 0
                density = []
                bparam = []
                header = np.loadtxt(self.distpath+'header.dat',dtype=str,delimiter='\n')
                fort13 = np.loadtxt(self.distpath+'turbulent.13',dtype=str,delimiter='\n')
                #fort13 = np.loadtxt(self.distpath+'thermal.13',dtype=str,delimiter='\n')
                for line in fort13:
                    vals = line.split()
                    flag = 1 if '*' in line and flag==0 else 2 if '*' in line and flag==1 else flag
                    if len(vals)==0:
                        break
                    if flag==1 and '*' not in line:
                        if 'external' not in header[k]:
                            trans = header[k].split()[0]
                            wmid  = self.atominfo(trans)[1]
                            dv.append(2*(float(vals[3])-float(vals[2]))/(float(vals[2])+float(vals[3]))*self.c)
                        k += 1
                    if flag==2 and '*' not in line:
                        # To check for b-ties. Why not do this on redshift? 
                        alpha = vals[4] if len(vals[0])==1 else vals[3]
                        zabs  = vals[3] if len(vals[0])==1 else vals[2]
                        zabs  = float(zabs[:-2]+re.compile(r'[^\d.-]+').sub('',zabs[-2:]))
                        # Checking that component is not a blend before increasing tied
                        tied  = tied + 1 if alpha[-1].islower()==True and abs(zabs-self.zabs)<0.003 else tied
                        ion   = vals[0]+vals[1] if len(vals[0])==1 else vals[0]
                        densityi = vals[2] if len(vals[0])==1 else vals[1]
                        densityi = float(densityi.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXYZ'))
                        density = density + [densityi] #TODO probably there is a better way to do this!
                        bparami = vals[4] if len(vals[0])==1 else vals[3]
                        bparami = float(bparami.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                        bparam = bparam + [bparami]
                        # transitions = [s for s in header if ion in s]
                        if ion in metals[:,0] and alpha[-1].isdigit()==False and abs(zabs-self.zabs)<0.003:
                            i = np.where(metals[:,0]==ion)[0][0]
                            transarr = np.empty(len(transitions[i]),dtype='S9')
                            for q in range(len(transarr)):
                                testtrans = transitions[i][q]
                                if testtrans in header:
                                    transarr[q] = testtrans
                                else:
                                    transarr[q] = 'False'
                            # If system not already recorded for this ion, record filename and redshift
                            # and which transitions are present
                            if system not in metals[i,1]:
                                metals[i,1] = np.vstack((metals[i,1],[str(system)]))
                                metals[i,2] = np.vstack((metals[i,2],[1,0,self.zabs,0,0,0]))
                                fitdata[i,1] = np.vstack((fitdata[i,1],[self.zabs]))
                                fitdata[i,3] = np.vstack((fitdata[i,3],[transarr]))
    
                            else:
                                j = np.where(metals[i,1]==system)[0][0]
                                metals[i,2][j,0] += 1
    
                            fitdata[i,2] = np.vstack((fitdata[i,2],[self.zabs,densityi,bparami])) 
                            # fitdata[i,2] = np.vstack((fitdata[i,2],[self.zabs,densityi,bparami]))
                ''' Equivalent widths from chunks '''
                os.system('ls '+self.distpath+'chunks/ > list')
                chunks = np.loadtxt('list',dtype=str)
                noise,ewidth,minmax = [],[],[]
                ionprev = ''
                for n in range(len(chunks)):
                    ion   = header[n].split()[0].split('_')[0]
                    chunk = np.loadtxt(self.distpath+'chunks/'+chunks[n],comments='!')
                    chunk = np.delete(chunk,np.where(chunk[:,2]==0)[0],0)
                    width = sum([(1-chunk[i,-1])*(chunk[i+1,0]-chunk[i,0])/(self.zabs+1) for i in range(len(chunk)-1)])
                    snr   = np.average(chunk[:,1]/chunk[:,2])
                    #saving S/N for strongest lines
                    a=np.where(snarr[:,0]==header[n])
                    #snarr[a[0],1] = np.array([0,0]).reshape((1,2))
                    if len(a[0])>0:
                        snarr[a[0][0],1] = np.vstack((snarr[a[0][0],1],[self.zabs,snr]))
                    #suppwidth is the distance between upper and lower wavelength where the flux falls N sigma below 1
                    sigma = 3.
                    index = np.where(1.-chunk[:,3]-sigma*chunk[:,2] > 0.)
                    if len(index[0])>0:
                        ilambdamin = index[0][0]
                        ilambdamax = index[0][-1]
                        suppwidth = (chunk[ilambdamax,0]-chunk[ilambdamin,0])/(self.zabs+1)
                    else:
                        suppwidth = 0
                    if 'external' not in header[n] and ion in metals[:,0]:
                        i = np.where(metals[:,0]==ion)[0][0]
                        if system in metals[i,1]:
                            # if the ion is the same as the previous ion, the averaging counter
                            # should not be increased (transition only split for fitting)
                            j = np.where(metals[i,1]==system)[0][0]
                            metals[i,2][j,1] += width
                            metals[i,2][j,3] += snr
                            metals[i,2][j,5] += suppwidth
                            if header[n] != ionprev : metals[i,2][j,4] += 1.
                            #print metals[i,1][j],ion, i,metals[i,2][j,4]
                    if header[n]==ionprev:
                        # if the ion is the same as the previous ion, width and suppwidth should
                        # be added to the previous width rather than appended
                        ewidth[-1] = ewidth[-1]+width
                        minmax[-1] = minmax[-1]+suppwidth
                        # Averaging S/N over the two regions. In principle this should be weighted
                        # with the length of each interval
                        noise[-1] = (noise[-1]+snr)/2.
                    else:
                        ewidth.append(width)
                        noise.append(snr)
                        minmax.append(suppwidth)
                    ionprev = header[n]
                #averaging over transitions
                for i in range(len(metals)):
                    if system in metals[i,1]:
                        j = np.where(metals[i,1]==system)[0][0]
                        if metals[i,2][j,1]>0:
                            metals[i,2][j,1] = metals[i,2][j,1] / metals[i,2][j,4]
                            metals[i,2][j,5] = metals[i,2][j,5] / metals[i,2][j,4]
                            metals[i,2][j,4] = 1
                data = np.vstack((data,np.array([float(tied),
                                                 np.mean(ewidth),
                                                 np.std(ewidth),
                                                 self.zabs,
                                                 np.mean(noise),
                                                 np.mean(dv),
                                                 np.std(dv),
                                                 np.mean(minmax),
                                                 np.std(minmax)],dtype=float)))
        os.system('rm list')
        ''' Bin data '''
        k = 1
        data = np.array(sorted(data,key=lambda col: col[3]))
        bindata = np.empty((0,9))
        for i in range(0,len(data),self.binning):
            ilim  = i+self.binning if i+self.binning<=len(data) else len(data)
            # print '\nbin',k,'\n'
            # for j in range(i,ilim):
            #     print 'z={0:<8}  |  {1:>5}  |  {2:>5} +/- {3:<6}  |  {4:<8}'.format('%.5f'%data[j,3],'%i'%data[j,0],'%.2f'%data[j,1],'%.2f'%data[j,2],'%.2f'%data[j,4])
            zabs  = np.average([float(data[j,3]) for j in range(i,ilim)])
            tied  = np.average([float(data[j,0]) for j in range(i,ilim)])
            snr   = np.average([float(data[j,4]) for j in range(i,ilim)])
            width = sum([float(data[j,1])/float(data[j,2])**2 for j in range(i,ilim)]) / sum([1/float(data[j,2])**2 for j in range(i,ilim)])
            error = 1 / np.sqrt(sum(1/float(data[j,2])**2 for j in range(i,ilim)))
            dv    = sum([float(data[j,5])/float(data[j,6])**2 for j in range(i,ilim)]) / sum([1/float(data[j,6])**2 for j in range(i,ilim)])
            dverr = 1 / np.sqrt(sum(1/float(data[j,6])**2 for j in range(i,ilim)))
    
            suppwidth = sum([float(data[j,7])/float(data[j,8])**2 for j in range(i,ilim)]) / sum([1/float(data[j,8])**2 for j in range(i,ilim)])
            supperror = 1 / np.sqrt(sum(1/float(data[j,8])**2 for j in range(i,ilim)))
            # print '----------  |  -----  |  ----------------  |  --------'
            # print 'z={0:<8}  |  {1:>5}  |  {2:>5} +/- {3:<6}  |  {4:<8}'.format('%.5f'%zabs,'%i'%tied,'%.2f'%width,'%.2f'%error,'%.2f'%snr)
            bindata   = np.vstack((bindata,[tied,width,error,zabs,snr,dv,dverr,suppwidth,supperror]))
            k += 1
        return bindata,metals,fitdata,data,snarr
    
    def plotwidth(self):
    
        def func(x,a,b):
            return a + b*x
        bindata,metals,fitdata,obsdata,snarr = getmetals()
        ''' ----------------------------------------------------- '''
        ''' Plot Average Equivalent Width vs. Velocity Dispersion '''
        ''' ----------------------------------------------------- '''
        x    = bindata[:,5]
        xerr = bindata[:,6]
        y    = bindata[:,1]
        yerr = bindata[:,2]
        zabs = bindata[:,3]
        xmax = 1.1*max(x)
        ymax = 0.2#1.1*max(y)
        fig = figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        ax = subplot(111,xlim=[0,xmax],ylim=[0,ymax])
        ax.scatter(x,y,marker='o',s=50,edgecolors='none',zorder=3,\
                c=zabs,cmap=mpl.cm.cool,vmin=min(zabs),vmax=max(zabs))
        errorbar(x,y,yerr=yerr,fmt='o',ms=0,c='0.7',zorder=1)
        xlabel('Average velocity dispersion',fontsize=12)
        ylabel('Average equivalent width',fontsize=12)
        axhline(y=0,ls='dotted',color='black')
        axvline(x=0,ls='dotted',color='black')
        '''
        SHOULD BE FITTED UNBINNED   
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,x,y)
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dotted',
                label=r'Unweighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,x,y,sigma=yerr)
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dashed',
                label=r'Weighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        leg = plt.legend(fancybox=True,loc=2,numpoints=1,handlelength=3,prop={'size':12})
        leg.get_frame().set_linewidth(0.1)
        '''    
        ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        cmap = mpl.cm.cool
        norm = mpl.colors.Normalize(vmin=min(zabs),vmax=max(zabs))
        cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        cb1.set_label('Absorption redshift',fontsize=12)
        savefig('equiwidth_vs_dispersion.pdf')
        clf()
        ''' ----------------------------------------------------------- '''
        ''' Plot Average Equivalent Width vs. Number of Tied Components '''
        ''' ----------------------------------------------------------- '''
        x    = bindata[:,0]
        y    = bindata[:,1]
        yerr = bindata[:,2]
        zabs = bindata[:,3]
        xmax = 1.1*max(x)
        ymax = 1.1*max(y)
        fig = figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        ax = subplot(111,xlim=[0,xmax],ylim=[0,ymax])
        ax.scatter(x,y,marker='o',s=50,edgecolors='none',zorder=3,\
                c=zabs,cmap=mpl.cm.cool,vmin=min(zabs),vmax=max(zabs))
        errorbar(x,y,yerr=yerr,fmt='o',ms=0,c='0.7',zorder=1)
        xlabel('Number of tied components',fontsize=12)
        ylabel('Average equivalent width',fontsize=12)
        axhline(y=0,ls='dotted',color='black')
        axvline(x=0,ls='dotted',color='black')
        ax.scatter(obsdata[:,0],obsdata[:,1],marker='o',s=20,edgecolors='none',zorder=2,\
                   c=obsdata[:,3],cmap=mpl.cm.rainbow,vmin=min(obsdata[:,3]),vmax=max(obsdata[:,3]),alpha=0.2)
        '''
        SHOULD BE FITTED UNBINNED   
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,x,y)
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dotted',
                label=r'Unweighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,x,y,sigma=yerr)
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dashed',
                label=r'Weighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        leg = plt.legend(fancybox=True,loc=2,numpoints=1,handlelength=3,prop={'size':12})
        leg.get_frame().set_linewidth(0.1)
        '''            
        ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        cmap = mpl.cm.cool
        norm = mpl.colors.Normalize(vmin=min(zabs),vmax=max(zabs))
        cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        cb1.set_label('Absorption redshift',fontsize=12)
        savefig('equiwidth_vs_tied.pdf')
        clf()
        ''' ------------------------------------------- '''
        ''' Plot Number of tied components vs. Redshift '''
        ''' ------------------------------------------- '''
        x    = bindata[:,3]
        y    = bindata[:,0]
        c    = bindata[:,4]
        xmax = 1.1*max(obsdata[:,3])
        ymax = 1.1*max(obsdata[:,0])
        fig = figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        ax = subplot(111,xlim=[0,xmax],ylim=[0,ymax])
        ax.scatter(x,y,marker='o',s=50,edgecolors='none',zorder=3,\
                   c=c,cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c),label='Binned in redshift')
        xlabel('Absorption redshift',fontsize=12)
        ylabel('Number of tied components',fontsize=12)
        axhline(y=0,ls='dotted',color='black')
        axvline(x=0,ls='dotted',color='black')
        #for i in range(len(metals)):
        #    ax.scatter(metals[i,2][:,2],metals[i,2][:,0],marker='o',s=20,edgecolors='none',
        #               zorder=2,alpha=0.2,label='Individual points')
        #               #c=obsdata[:,4],cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c),alpha=0.2)
        ax.scatter(obsdata[:,3],obsdata[:,0],marker='o',s=20,edgecolors='none',zorder=2,\
                   c=obsdata[:,4],cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c),alpha=0.2)
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,obsdata[:,3],obsdata[:,0])
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dashed',
                label=r'Unweighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        leg = plt.legend(fancybox=True,loc=2,numpoints=1,handlelength=3,prop={'size':12})
        leg.get_frame().set_linewidth(0.1)
        ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        cmap = mpl.cm.rainbow
        norm = mpl.colors.Normalize(vmin=min(c),vmax=max(c))
        cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        cb1.set_label('Signal-to-Noise ratio',fontsize=12)
        savefig('tied_vs_redshift.pdf')
        clf()
        ''' ------------------------------------------- '''
        ''' Plot b-param of strongest component vs. Redshift '''
        ''' ------------------------------------------- '''
        fig = figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        # [zabs, b parameter for max value of N, N value for max value of N]
        plotdata = np.empty((0,3))
        plotdataall = np.empty((0,3))
        for i in range(len(fitdata)):
            for j in range(0,len(fitdata[i,1]),1):
                index = np.where(fitdata[i,2][:,0]==fitdata[i,1][j])
                imax = np.argmax(fitdata[i,2][index,1])+np.min(index)
                plotdata = np.vstack((plotdata,[fitdata[i,1][j][0],fitdata[i,2][imax,1],fitdata[i,2][imax,2]]))
            for j in range(0,len(fitdata[i,2]),1):
                plotdataall=np.vstack((plotdataall,[fitdata[i,2][j,0],fitdata[i,2][j,1],fitdata[i,2][j,2]]))
        ax = subplot(111,xlim=[0,5],ylim=[0,16])
        ax.scatter(plotdataall[:,0],plotdataall[:,2],marker='o',s=20,edgecolors='none',
                   zorder=3,alpha=0.2,color='green',label='All components')
        ax.scatter(plotdata[:,0],plotdata[:,2],marker='o',s=50,edgecolors='none',
                   zorder=3,alpha=0.4,color='blue',label='Strongest component')
                   # c=c,cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c)
        bin_edges = np.arange(0,len(plotdata[:,0]),self.binning)
        bins = np.array(sorted(plotdata[:,0]))[bin_edges]
        # adding the max redshift+0.1 as bin edge
        bins = np.append(bins,[max(plotdata[:,0])+0.1])
        bin_means, bin_edges, binnumber = stats.binned_statistic(plotdata[:,0], plotdata[:,2],
                                                                 statistic='median', bins=bins)
        ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='black', zorder=4,lw=5,
                  label='Binned means for '+str(self.binning)+' points per bin')
        xlabel('Absorption redshift',fontsize=12)
        ylabel('b-parameter',fontsize=12)
        # xfit = np.arange(0,xmax,0.01)
        # coeffs,matcov = curve_fit(func,x,y)
        # yfit = func(xfit,coeffs[0],coeffs[1])
        # ax.plot(xfit,yfit,color='black',lw=3,ls='dashed',
        #        label=r'Unweighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        # leg = plt.legend(fancybox=True,loc=2,numpoints=1,handlelength=3,prop={'size':12})
        # leg.get_frame().set_linewidth(0.1)
        # ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        # cmap = mpl.cm.rainbow
        # norm = mpl.colors.Normalize(vmin=min(c),vmax=max(c))
        # cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        # cb1.set_label('Signal-to-Noise ratio',fontsize=12)
        savefig('bparam_vs_redshift.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot Average Equivalent Width vs. Redshift '''
        ''' ------------------------------------------ '''
        x    = bindata[:,3]
        y    = bindata[:,1]
        yerr = bindata[:,2]
        c    = bindata[:,4]
        xmax = 1.1*max(x)
        ymax = 1.1*max(y)
        fig = figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        ax = subplot(111,xlim=[0,xmax],ylim=[0,ymax])
        ax.scatter(x,y,marker='o',s=50,edgecolors='none',zorder=3,\
                   c=c,cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c))
        errorbar(x,y,yerr=yerr,fmt='o',ms=0,c='0.7',zorder=1)
        xlabel('Absorption redshift',fontsize=12)
        ylabel('Average Equivalent Width',fontsize=12)
        axhline(y=0,ls='dotted',color='black')
        axvline(x=0,ls='dotted',color='black')
        '''
        SHOULD BE FITTED UNBINNED   
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,x,y)
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dotted',
                label=r'Unweighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        xfit = np.arange(0,xmax,0.01)
        coeffs,matcov = curve_fit(func,x,y,sigma=yerr)
        yfit = func(xfit,coeffs[0],coeffs[1])
        ax.plot(xfit,yfit,color='black',lw=3,ls='dashed',
                label=r'Weighted fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
        leg = plt.legend(fancybox=True,loc=2,numpoints=1,handlelength=3,prop={'size':12})
        leg.get_frame().set_linewidth(0.1)
        '''            
        ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        cmap = mpl.cm.rainbow
        norm = mpl.colors.Normalize(vmin=min(c),vmax=max(c))
        cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        cb1.set_label('Signal-to-Noise ratio',fontsize=12)
        savefig('equiwidth_vs_redshift.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot Min/Max Width vs. Redshift '''
        ''' ------------------------------------------ '''
        x    = bindata[:,3]
        y    = bindata[:,7]
        yerr = bindata[:,8]
        c    = bindata[:,4]
        xmax = 1.1*max(x)
        ymax = 1.1*max(y)
        fig = figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        ax = subplot(111,xlim=[0,xmax],ylim=[0,ymax])
        ax.scatter(x,y,marker='o',s=50,edgecolors='none',zorder=3,\
                   c=c,cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c))
        errorbar(x,y,yerr=yerr,fmt='o',ms=0,c='0.7',zorder=1)
        xlabel('Absorption redshift',fontsize=12)
        ylabel('Min/max width',fontsize=12)
        axhline(y=0,ls='dotted',color='black')
        axvline(x=0,ls='dotted',color='black')
        ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        cmap = mpl.cm.rainbow
        norm = mpl.colors.Normalize(vmin=min(c),vmax=max(c))
        cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        cb1.set_label('Signal-to-Noise ratio',fontsize=12)
        savefig('minmax_vs_redshift.pdf')
        clf()
    
    def plotwidthperion(self):
    
        def func(x,a,b):
            return a + b*x
        bindata,metals,fitdata,obsdata,snarr = getmetals()
        ''' ------------------------------------------- '''
        ''' Plot number of tied components vs. redshift '''
        ''' ------------------------------------------- '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('Number of tied components vs. Absorption redshift',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = 0
        ymax = 35
        for i in range(len(metals)):
            ion   = metals[i,0]
            data  = np.array(sorted(metals[i,2],key=lambda col: col[2]))
            bdata = np.empty((0,2))
            for j in range(0,len(data),self.binning):
                jlim  = j+self.binning if j+self.binning<=len(data) else len(data)
                zabs  = np.average([float(data[k,2]) for k in range(j,jlim)])
                tied  = np.average([float(data[k,0]) for k in range(j,jlim)])
                bdata = np.vstack((bdata,[zabs,tied]))
            #ax = subplot(4,2,i+1,xlim=[0,max(bdata[:,0])],ylim=[0,max(bdata[:,1])])
            ax = subplot(4,2,i+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ax.scatter(metals[i,2][:,2],metals[i,2][:,0],marker='o',s=20,edgecolors='none',zorder=2,c='blue',alpha=0.4)
            ax.scatter(bdata[:,0],bdata[:,1],marker='o',s=40,edgecolors='none',zorder=3,c='black',alpha=0.8)
            axhline(y=0,ls='dotted',color='black')
            axvline(x=0,ls='dotted',color='black')
            if len(bdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,metals[i,2][:,2],metals[i,2][:,0])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed')
                self.linslopeval = coeffs[1]
                self.linslopeerr = np.sqrt(matcov[1][1])
                #print metals[i,0]+r': %.4f +/- %.4f'%(self.linslopeval,self.linslopeerr)
            plt.title(ion,fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
        savefig('tied_vs_redshift_per_ion.pdf')
        clf()
        ''' ----------------------------------------------------------- '''
        ''' Plot average equivalent width vs. number of tied components '''
        ''' ----------------------------------------------------------- '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('Average Equivalent Width vs. Number of tied components',fontsize=15)
        xmin = 0
        xmax = 35
        ymin = 0
        ymax = 5
        for i in range(len(metals)):
            ion   = metals[i,0]
            data  = np.array(sorted(metals[i,2],key=lambda col: col[0]))
            bdata = np.empty((0,2))
            for j in range(0,len(data),self.binning):
                jlim  = j+self.binning if j+self.binning<=len(data) else len(data)
                tied  = np.average([float(data[k,0]) for k in range(j,jlim)])
                width = np.average([float(data[k,1]) for k in range(j,jlim)])
                bdata = np.vstack((bdata,[tied,width]))
            #ax = subplot(4,2,i+1,xlim=[0,max(bdata[:,0])],ylim=[0,max(bdata[:,1])])
            ax = subplot(4,2,i+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ax.scatter(metals[i,2][:,0],metals[i,2][:,1],marker='o',s=20,edgecolors='none',zorder=2,c='blue',alpha=0.4)
            ax.scatter(bdata[:,0],bdata[:,1],marker='o',s=40,edgecolors='none',zorder=3,c='black',alpha=0.8)
            axhline(y=0,ls='dotted',color='black')
            axvline(x=0,ls='dotted',color='black')
            if len(bdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,metals[i,2][:,0],metals[i,2][:,1])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed')
            plt.title(ion,fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
        savefig('equiwidth_vs_tied_per_ion.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot average equivalent width vs. redshift '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('Average Equivalent Width vs. Absorption redshift',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = 0
        ymax = 2
        for i in range(len(metals)):
            ion   = metals[i,0]
            data  = np.array(sorted(metals[i,2],key=lambda col: col[2]))
            bdata = np.empty((0,2))
            for j in range(0,len(data),self.binning):
                jlim  = j+self.binning if j+self.binning<=len(data) else len(data)
                zabs  = np.average([float(data[k,2]) for k in range(j,jlim)])
                width = np.average([float(data[k,1]) for k in range(j,jlim)])
                bdata = np.vstack((bdata,[zabs,width]))
            #ax = subplot(4,2,i+1,xlim=[0,max(bdata[:,0])],ylim=[0,max(bdata[:,1])])
            ax = subplot(4,2,i+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ax.scatter(metals[i,2][:,2],metals[i,2][:,1],marker='o',s=20,edgecolors='none',zorder=2,c='blue',alpha=0.4)
            ax.scatter(bdata[:,0],bdata[:,1],marker='o',s=40,edgecolors='none',zorder=3,c='black',alpha=0.8)
            axhline(y=0,ls='dotted',color='black')
            axvline(x=0,ls='dotted',color='black')
            if len(bdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,metals[i,2][:,2],metals[i,2][:,1])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed')
            plt.title(ion,fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
        savefig('equiwidth_vs_redshift_per_ion.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot min/max width vs. Ntied '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('EW and min/max width [ang] vs. number of tied components',fontsize=15)
        xmin = 0
        xmax = 35
        ymin = 0
        ymax = 5
        for i in range(len(metals)):
            ax = subplot(4,2,i+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ion   = metals[i,0]
            data  = np.array(sorted(metals[i,2],key=lambda col: col[0]))
            bdata = np.empty((0,2))
            for j in range(0,len(data),self.binning):
                jlim  = j+self.binning if j+self.binning<=len(data) else len(data)
                tied  = np.average([float(data[k,0]) for k in range(j,jlim)])
                width = np.average([float(data[k,1]) for k in range(j,jlim)])
                bdata = np.vstack((bdata,[tied,width]))
            if len(bdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,metals[i,2][:,0],metals[i,2][:,1])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='black',lw=2,ls='dashed')
            datamm  = np.array(sorted(metals[i,2],key=lambda col: col[0]))
            bdatamm = np.empty((0,2))
            for j in range(0,len(datamm),self.binning):
                jlim  = j+self.binning if j+self.binning<=len(datamm) else len(datamm)
                tiedmm  = np.average([float(datamm[k,0]) for k in range(j,jlim)])
                widthmm = np.average([float(datamm[k,5]) for k in range(j,jlim)])
                bdatamm = np.vstack((bdatamm,[tiedmm,widthmm]))
            ax.scatter(metals[i,2][:,0],metals[i,2][:,1],marker='o',s=20,edgecolors='none',
                       zorder=2,c='blue',alpha=0.4,label='Equivalent width')
            ax.scatter(bdata[:,0],bdata[:,1],marker='o',s=40,edgecolors='none',zorder=3,c='black',alpha=0.8)
            ax.scatter(metals[i,2][:,0],metals[i,2][:,5],marker='o',s=20,edgecolors='none',
                       zorder=2,c='green',alpha=0.4,label='Min/max width')
            ax.scatter(bdatamm[:,0],bdatamm[:,1],marker='o',s=40,edgecolors='none',zorder=3,c='red',alpha=0.8)
            if len(bdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,metals[i,2][:,0],metals[i,2][:,5])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed')
            plt.title(ion,fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
        ax.legend(frameon=False,prop={"size":9}, loc='upper right', borderaxespad=0.2,handlelength=2.7,numpoints=1)
        savefig('minmax_vs_tied_per_ion.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot spectra for outliers '''
        ''' ------------------------------------------ '''
        # fig = figure(figsize=(8,12))
        # plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        # fig.suptitle('Outliers',fontsize=15)
        # ymin = -0.1
        # ymax = 1.1
        # i = 0
        # test = np.argmax(metals[i,2][:,5])
        # Nchuncks = 7
        # for j in range(Nchuncks):
        #     string = 'pubsys/'+metals[i,1][test][0]+'/chunks/vpfit_chunk00'+str(j+1)+'.txt'
        #     print string
        #     data = np.genfromtxt(string,comments='!')
        #     xmin,xmax = min(data[:,0]),max(data[:,0])
        #     print xmin,xmax
        #     ax = subplot(Nchuncks,1,j+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
        #     plt.ticklabel_format(useOffset=False)
        #     ax.plot(data[:,0],data[:,3])             
        #     ax.plot(data[:,0],data[:,1])
        #     ax.plot(data[:,0],data[:,2])             
        #     axhline(y=0,ls='dotted',color='black')
        #     axhline(y=1,ls='dotted',color='black')
        #     sigma = 3.
        #     index = np.where(1.-data[:,3]-sigma*data[:,2] > 0.)
        #     if len(index[0])>0:
        #         ilambdamin = index[0][0]
        #         ilambdamax = index[0][-1]
        #     axvline(x=data[ilambdamin,0])
        #     axvline(x=data[ilambdamax,0])
        #     print data[ilambdamax,0]-data[ilambdamin,0]
        # savefig('outliers.pdf')
        # clf()
        ''' ------------------------------------------ '''
        ''' Plot b for strongest component vs. redshift '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('b-parameter for strongest component vs. Absorption redshift',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = 0
        ymax = 16
        for i in range(len(fitdata)):
            ion   = fitdata[i,0]
            plotdata = np.empty((0,2))
            for j in range(0,len(fitdata[i,1]),1):
                index = np.where(fitdata[i,2][:,0]==fitdata[i,1][j])
                imax = np.argmax(fitdata[i,2][index,1])+np.min(index)
                plotdata = np.vstack((plotdata,[fitdata[i,1][j][0],fitdata[i,2][imax,2]]))
            ax = subplot(4,2,i+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ax.scatter(plotdata[:,0],plotdata[:,1],marker='o',s=40,edgecolors='none',
                       zorder=3,c='blue',alpha=0.4,label='Unbinned')
            axhline(y=0,ls='dotted',color='black')
            axvline(x=0,ls='dotted',color='black')
            bin_edges = np.arange(0,len(plotdata[:,0]),self.binning)
            bins = np.array(sorted(plotdata[:,0]))[bin_edges]
            bins = np.append(bins,[max(plotdata[:,0])+0.1]) #adding the max redshift+0.1 as bin edge
            bin_means, bin_edges, binnumber = stats.binned_statistic(plotdata[:,0], plotdata[:,1],
                                                                     statistic='median', bins=bins)
            ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='black',
                      zorder=4,lw=5, label='Binned means for '+str(self.binning)+' points per bin')
            if len(plotdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,plotdata[:,0],plotdata[:,1])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed',label='Unbinned fit')
            plt.title(ion,fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
        ax.legend(frameon=False,prop={"size":9}, loc='upper right', borderaxespad=0.2,handlelength=2.7,numpoints=1)
        savefig('bparam_vs_redshift_per_ion.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot N vs. redshift for strongest lines '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,6))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.90, hspace=0.3, wspace=0.1)
        fig.suptitle('Column density vs. Absorption redshift for specific lines',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = 7.5
        ymax = 21
        for i in range(4):
            ion = fitdata[i,0]
            plotdata = np.empty((0,3))
            plotallz = [] 
            plotallN = []
            required = ['MgII_2796','FeII_2382','SiII_1526','AlII_1670']
            for j in range(0,len(fitdata[i,1]),1):
                #a = [b for b in required[i] if b in fitdata[i,3][j]]
                #print required[i]
                #print a
                if required[i] in fitdata[i,3][j] >0:
                    index = np.where(fitdata[i,2][:,0]==fitdata[i,1][j])
                    imax = np.argmax(fitdata[i,2][index,1])+np.min(index)
                    plotallz = np.hstack((plotallz,fitdata[i,2][index,0][0]))
                    plotallN = np.hstack((plotallN,fitdata[i,2][index,1][0]))
                    summedN = np.log10(np.sum(10**fitdata[i,2][index,1][0]))
                    plotdata = np.vstack((plotdata,[fitdata[i,1][j][0],fitdata[i,2][imax,1],summedN]))
            ax = subplot(2,2,i+1,xlim=[xmin,xmax]) #ylim=[min(plotallN),max(plotallN)]
            ax.scatter(plotallz,plotallN,marker='o',s=40,edgecolors='none',zorder=3,c='grey',alpha=0.4)#,label='All')
            ax.scatter(plotdata[:,0],plotdata[:,1],marker='o',s=40,edgecolors='none',
                       zorder=3,c='blue',alpha=0.4)#,label='Strongest')
            ax.scatter(plotdata[:,0],plotdata[:,2],marker='o',s=40,edgecolors='none',
                       zorder=3,c='red',alpha=0.4,label='Summed')
            bin_edges = np.arange(0,len(plotdata[:,0]),self.binning)
            bins = np.array(sorted(plotdata[:,0]))[bin_edges]
            bins = np.append(bins,[max(plotdata[:,0])+0.1]) #adding the max redshift+0.1 as bin edge
            bin_means, bin_edges, binnumber = stats.binned_statistic(plotdata[:,0], plotdata[:,2],
                                                                     statistic='median', bins=bins)
            ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='black', zorder=4, lw=5)#, label='Binned means for '+str(self.binning)+' per bin')
            if len(plotdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,plotdata[:,0],plotdata[:,1])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed',
                        label=r'Unbinned fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
            plt.title(required[i],fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
            ax.legend(frameon=False,prop={"size":9}, loc='lower right', borderaxespad=0.2,handlelength=2.7,numpoints=1)
        savefig('N_vs_redshift_per_strong_ion.pdf')
        ''' ------------------------------------------ '''
        ''' Plot N vs. redshift '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('Column density vs. Absorption redshift',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = 7.5
        ymax = 21
        for i in range(len(fitdata)):
            ion   = fitdata[i,0]
            plotdata = np.empty((0,3))
            plotallz = [] 
            plotallN = []
            for j in range(0,len(fitdata[i,1]),1):
                index = np.where(fitdata[i,2][:,0]==fitdata[i,1][j])
                imax = np.argmax(fitdata[i,2][index,1])+np.min(index)
                plotallz = np.hstack((plotallz,fitdata[i,2][index,0][0]))
                plotallN = np.hstack((plotallN,fitdata[i,2][index,1][0]))
                summedN = np.log10(np.sum(10**fitdata[i,2][index,1][0]))
                plotdata = np.vstack((plotdata,[fitdata[i,1][j][0],fitdata[i,2][imax,1],summedN]))
            ax = subplot(4,2,i+1,xlim=[xmin,xmax],ylim=[min(plotallN),max(plotallN)])
            ax.scatter(plotallz,plotallN,marker='o',s=40,edgecolors='none',zorder=3,c='grey',alpha=0.4)#,label='All')
            ax.scatter(plotdata[:,0],plotdata[:,1],marker='o',s=40,edgecolors='none',zorder=3,c='blue',alpha=0.4)#,label='Strongest')
            ax.scatter(plotdata[:,0],plotdata[:,2],marker='o',s=40,edgecolors='none',zorder=3,c='red',alpha=0.4,label='Summed')
            bin_edges = np.arange(0,len(plotdata[:,0]),self.binning)
            bins = np.array(sorted(plotdata[:,0]))[bin_edges]
            bins = np.append(bins,[max(plotdata[:,0])+0.1]) #adding the max redshift+0.1 as bin edge
            bin_means, bin_edges, binnumber = stats.binned_statistic(plotdata[:,0], plotdata[:,2], statistic='median', bins=bins)
            ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='black', zorder=4, lw=5, label='Binned means for '+str(self.binning)+' per bin')
            if len(plotdata)>1:
                xfit = np.arange(0,xmax,0.01)
                coeffs,matcov = curve_fit(func,plotdata[:,0],plotdata[:,1])
                yfit = func(xfit,coeffs[0],coeffs[1])
                ax.plot(xfit,yfit,color='red',lw=2,ls='dashed',label=r'Unbinned fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
            plt.title(ion,fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
            ax.legend(frameon=False,prop={"size":9}, loc='lower right', borderaxespad=0.2,handlelength=2.7,numpoints=1)
        savefig('N_vs_redshift_per_ion.pdf')
        # clf()
        ''' ------------------------------------------ '''
        ''' Plot DeltaN vs. redshift '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,12))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.93, hspace=0.3, wspace=0.1)
        fig.suptitle('DeltaN/Deltaz versus z',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = -2.5
        ymax = 7
        for i in range(4):
            ion = fitdata[i,0]
            plotdata = np.empty((0,3))
            plotallz = [] 
            plotallN = []
            for j in range(0,len(fitdata[i,1]),1):
                index = np.where(fitdata[i,2][:,0]==fitdata[i,1][j])
                plotallz = np.hstack((plotallz,fitdata[i,2][index,0][0]))
                plotallN = np.hstack((plotallN,fitdata[i,2][index,1][0]))
                summedN = np.log10(np.sum(10**fitdata[i,2][index,1][0]))
                plotdata = np.vstack((plotdata,[fitdata[i,1][j][0],fitdata[i,2][imax,1],summedN]))
            #binning
            bin_edges = np.arange(0,len(plotdata[:,0]),self.binning)
            bins = np.array(sorted(plotdata[:,0]))[bin_edges]
            bins = np.append(bins,[max(plotdata[:,0])+0.1]) #adding the max redshift+0.1 as bin edge
            bin_means, bin_edges, binnumber = stats.binned_statistic(plotdata[:,0], plotdata[:,2],
                                                                     statistic='median', bins=bins)
            #differentiating
            bins_xmid = (bin_edges[1:] + bin_edges[:-1])/2
            diffN = np.diff(bin_means)
            diffz = np.diff(bins_xmid)
            binz = (bins_xmid[1:] + bins_xmid[:-1])/2
            #with threshold, binning
            threshold = 13.
            indthresh = np.where(plotdata[:,2] > threshold)
            zthres = plotdata[indthresh,0][0]
            Nthres = plotdata[indthresh,2][0]
            bintresh_edges = np.arange(0,len(zthres),self.binning)
            binsthresh = np.array(sorted(zthres))[bintresh_edges]
            binsthresh = np.append(binsthresh,[max(zthres)+0.1]) #adding the max redshift+0.1 as bin edge
            binthresh_means, binthresh_edges, binnumber = stats.binned_statistic(zthres, Nthres, statistic='median', bins=binsthresh)
            #With threshold, differentiating
            binsthresh_xmid = (binthresh_edges[1:] + binthresh_edges[:-1])/2
            diffNthresh = np.diff(binthresh_means)
            diffzthresh = np.diff(binsthresh_xmid)
            binzthresh = (binsthresh_xmid[1:] + binsthresh_xmid[:-1])/2
            #plotting DeltaN/Deltaz(z)
            ax = subplot(4,2,2*i+2,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ax.axhline(y=0,linewidth=1,color='grey')
            ax.hlines(diffN/diffz, bins_xmid[:-1], bins_xmid[1:], colors='red', zorder=4, lw=5)
            ax.hlines(diffNthresh/diffzthresh, binsthresh_xmid[:-1], binsthresh_xmid[1:], colors='blue', zorder=4, lw=5)
            ax.yaxis.tick_right()
            #plotting N(z)
            ax = subplot(4,2,2*i+1,xlim=[xmin,xmax],ylim=[10,21])
            ax.scatter(plotdata[:,0],plotdata[:,2],marker='o',s=40,edgecolors='none',zorder=3,c='red',alpha=0.4,label='Summed')
            ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='red', zorder=4, lw=5, label='Summed, binned, '+str(self.binning)+' per bin')
            ax.hlines(binthresh_means, binthresh_edges[:-1], binthresh_edges[1:], colors='blue', zorder=4, lw=5, label='Threshold, binned, '+str(self.binning)+' per bin')
            ax.axhline(y=threshold,linewidth=1,color='grey')
            ax.yaxis.set_ticks_position('both')
    #        if len(plotdata)>1:
    #            xfit = np.arange(0,xmax,0.01)
    #            coeffs,matcov = curve_fit(func,plotdata[:,0],plotdata[:,1])
    #            yfit = func(xfit,coeffs[0],coeffs[1])
    #            ax.plot(xfit,yfit,color='red',lw=2,ls='dashed',label='Unbinned fit')
            plt.title(ion,fontsize=12,color='red')
        ax.legend(frameon=False,prop={"size":9}, loc='upper right', borderaxespad=0.2,handlelength=2.7,numpoints=1)
        savefig('DeltaN_vs_redshift_per_ion.pdf')
        clf()
        ''' ------------------------------------------ '''
        ''' Plot S/N vs. redshift for strongest lines '''
        ''' ------------------------------------------ '''
        fig = figure(figsize=(8,6))
        plt.subplots_adjust(left=0.07, right=0.93, bottom=0.05, top=0.90, hspace=0.3, wspace=0.1)
        fig.suptitle('S/N vs. Absorption redshift for specific lines',fontsize=15)
        xmin = 0
        xmax = 5
        ymin = 0
        ymax = 170
        for i in range(4):
            ion   = fitdata[i,0]
            print min(snarr[i,1][:,1]),max(snarr[i,1][:,1])
            ax = subplot(2,2,i+1,xlim=[xmin,xmax],ylim=[ymin,ymax])
            ax.scatter(snarr[i,1][:,0],snarr[i,1][:,1],marker='o',s=40,edgecolors='none',zorder=3,c='grey',alpha=0.4)#,label='All')
            #bin_edges = np.arange(0,len(plotdata[:,0]),self.binning)
            #bins = np.array(sorted(plotdata[:,0]))[bin_edges]
            #bins = np.append(bins,[max(plotdata[:,0])+0.1]) #adding the max redshift+0.1 as bin edge
            #bin_means, bin_edges, binnumber = stats.binned_statistic(plotdata[:,0], plotdata[:,2], statistic='median', bins=bins)
            #ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='black', zorder=4, lw=5)#, label='Binned means for '+str(self.binning)+' per bin')
            #if len(plotdata)>1:
            #    xfit = np.arange(0,xmax,0.01)
            #    coeffs,matcov = curve_fit(func,plotdata[:,0],plotdata[:,1])
            #    yfit = func(xfit,coeffs[0],coeffs[1])
            #    ax.plot(xfit,yfit,color='red',lw=2,ls='dashed',label=r'Unbinned fit: $%.6f \pm %.6f$ '%(coeffs[1],np.sqrt(matcov[1][1])))
            plt.title(required[i],fontsize=12,color='red')
            if (i+1)%2==0:
                ax.yaxis.tick_right()
                ax.yaxis.set_ticks_position('both')
            #ax.legend(frameon=False,prop={"size":9}, loc='lower right', borderaxespad=0.2,handlelength=2.7,numpoints=1)
        savefig('SN_vs_redshift_per_strong_ion.pdf')
    
