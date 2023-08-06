# Import necessary packages
import os,sys,numpy
from matplotlib import rcParams

def get_argument(arguments):
    '''
    Extract arguments from user inputs.

    Parameters
    ----------
    args : list
      2D list of arguments

    Notes
    -----
    When sphinx is ran to create the documentation, there could
    be conflict as sphinx will use specific arguments that might
    have the same flag than the ones defined in this program. To
    avoid any conflict, we added the ``'sphinx' in sys.argv[0]``
    condition, if this is True, the default values for the parameter
    will be used.
    '''
    d = {}
    args = numpy.array(sys.argv, dtype=str)
    for i,(group,abbrev,argument,dtype,default,message) in enumerate(arguments):
        if '-h' in sys.argv or '--help' in sys.argv:
            if i==0 or arguments[i-1,0]!=group:
                print('\n'+'-'*65+'\n  '+group+'\n'+'-'*65)
            sep = ' , ' if abbrev!='' else '     '
            print('  {0}{1}{2:<14}{3}'.format(abbrev,sep,argument,message))
        arg = (abbrev!='' and abbrev in sys.argv) or (argument in sys.argv)
        if 'sphinx' in sys.argv[0] or arg==False:
            arg = default
        elif dtype==bool:
            pass
        else:
            target = abbrev if abbrev!='' and abbrev in sys.argv else argument
            idx = numpy.where(args==target)[0][0]+1
            for j,value in enumerate(args[idx:]):
                if value in arguments[:,1:3]:
                    j-=1
                    break
            arg = map(dtype,args[idx:idx+j+1])
            arg = arg[0] if len(arg)==1 else arg
        d[argument[2:]] = arg
    if '-h' in sys.argv or '--help' in sys.argv:
        print('-'*65+'\n')
    return d

# Prepare settings for interactive programs
keyMaps = [key for key in rcParams.keys() if 'keymap.' in key]
for keyMap in keyMaps:
    rcParams[keyMap] = ''
    
# Define fixed variables and arrays
c = 299792.458 # km/s
h = 6.62606957 * 10**-34  # m^2.kg/s
dhratio   = -4.55
datapath  = os.path.abspath(__file__).rsplit('/', 1)[0] + '/data/'
atompar   = numpy.loadtxt(datapath+'atompar.dat', usecols=(0,1,2,3,4,5),dtype=str)
emfreereg = numpy.array([[1280.0,1292.0],
                         [1312.0,1328.0],
                         [1345.0,1365.0],
                         [1440.0,1475.0],
                         [1680.0,1700.0],
                         [1968.0,1982.0],
                         [2020.0,2040.0],
                         [2150.0,2170.0],
                         [2190.0,2250.0]])

HI = [{'wave':1215.6701,'strength':0.416400,'gamma':6.265E8},
      {'wave':1025.7223,'strength':0.079120,'gamma':1.897E8},
      {'wave':972.53680,'strength':0.029000,'gamma':8.127E7},
      {'wave':949.74310,'strength':0.013940,'gamma':4.204E7},
      {'wave':937.80350,'strength':0.007799,'gamma':2.450E7},
      {'wave':930.74830,'strength':0.004814,'gamma':1.236E7},
      {'wave':926.22570,'strength':0.003183,'gamma':8.255E6},
      {'wave':923.15040,'strength':0.002216,'gamma':5.785E6},
      {'wave':920.96310,'strength':0.001605,'gamma':4.210E6},
      {'wave':919.35140,'strength':0.001200,'gamma':3.160E6},
      {'wave':918.12940,'strength':0.000921,'gamma':2.432E6},
      {'wave':917.18060,'strength':7.226e-4,'gamma':1.911E6},
      {'wave':916.42900,'strength':0.000577,'gamma':1.529E6},
      {'wave':915.82400,'strength':0.000469,'gamma':1.243E6},
      {'wave':915.32900,'strength':0.000386,'gamma':1.024E6},
      {'wave':914.91900,'strength':0.000321,'gamma':8.533E5},
      {'wave':914.57600,'strength':0.000270,'gamma':7.186E5},
      {'wave':914.28600,'strength':0.000230,'gamma':6.109E5},
      {'wave':914.03900,'strength':0.000197,'gamma':5.237E5},
      {'wave':913.82600,'strength':0.000170,'gamma':4.523E5},
      {'wave':913.64100,'strength':0.000148,'gamma':3.933E5},
      {'wave':913.48000,'strength':0.000129,'gamma':3.443E5},
      {'wave':913.33900,'strength':0.000114,'gamma':3.030E5},
      {'wave':913.21500,'strength':0.000101,'gamma':2.679E5},
      {'wave':913.10400,'strength':0.000089,'gamma':2.382E5},
      {'wave':913.00600,'strength':0.000080,'gamma':2.127E5},
      {'wave':912.91800,'strength':0.000071,'gamma':1.907E5},
      {'wave':912.83900,'strength':0.000064,'gamma':1.716E5},
      {'wave':912.76800,'strength':0.000058,'gamma':1.550E5},
      {'wave':912.70300,'strength':0.000053,'gamma':1.405E5},
      {'wave':912.64500,'strength':0.000048,'gamma':1.277E5}]

DI = [{'wave':1215.3394,'strength':0.416500,'gamma':6.270E8},
      {'wave':1025.4433,'strength':0.079100,'gamma':1.897E8},
      {'wave':972.27220,'strength':0.029010,'gamma':8.127E7},
      {'wave':949.48470,'strength':0.013950,'gamma':4.204E7},
      {'wave':937.54840,'strength':0.007808,'gamma':2.450E7},
      {'wave':930.49510,'strength':0.004817,'gamma':1.237E7},
      {'wave':925.97370,'strength':0.003184,'gamma':8.261E6},
      {'wave':922.89900,'strength':0.002216,'gamma':5.789E6},
      {'wave':920.71200,'strength':0.001605,'gamma':4.214E6},
      {'wave':919.10200,'strength':0.001201,'gamma':3.162E6},
      {'wave':917.87900,'strength':0.000921,'gamma':2.434E6},
      {'wave':916.93100,'strength':0.000723,'gamma':1.913E6},
      {'wave':916.17900,'strength':0.000577,'gamma':1.531E6},
      {'wave':915.57500,'strength':0.000469,'gamma':1.244E6},
      {'wave':915.08000,'strength':0.000386,'gamma':1.025E6}]

Metallist = [{'ID':'HI1215'   ,'Metalline':'HI',   'Metalwave':1215.67010},
             {'ID':'MgII2796' ,'Metalline':'MgII', 'Metalwave':2796.35000},
             {'ID':'MgII2803' ,'Metalline':'MgII', 'Metalwave':2803.53000},
             {'ID':'SiII1260' ,'Metalline':'SiII', 'Metalwave':1260.42000},
             {'ID':'SiII1526' ,'Metalline':'SiII', 'Metalwave':1526.71000},
             {'ID':'SiII1304' ,'Metalline':'SiII', 'Metalwave':1304.37000},
             {'ID':'SiII1808' ,'Metalline':'SiII', 'Metalwave':1808.01000},
             {'ID':'SiIV1393' ,'Metalline':'SiIV', 'Metalwave':1393.76000},
             {'ID':'SiIV1402' ,'Metalline':'SiIV', 'Metalwave':1402.77000},
             {'ID':'CI945'    ,'Metalline':'CI',   'Metalwave': 945.18800},
             {'ID':'CII1334'  ,'Metalline':'CII',  'Metalwave':1334.53000},
             {'ID':'CII1036'  ,'Metalline':'CII',  'Metalwave':1036.34000},
             {'ID':'CIV1548'  ,'Metalline':'CIV',  'Metalwave':1548.20000},
             {'ID':'CIV1550'  ,'Metalline':'CIV',  'Metalwave':1550.78000},
             {'ID':'OI1302'   ,'Metalline':'OI',   'Metalwave':1302.17000},
             {'ID':'OI988'    ,'Metalline':'OI',   'Metalwave': 988.77000},
             {'ID':'OI1039'   ,'Metalline':'OI',   'Metalwave':1039.23000},
             {'ID':'FeII2382' ,'Metalline':'FeII', 'Metalwave':2382.76000},
             {'ID':'FeII2600' ,'Metalline':'FeII', 'Metalwave':2600.17000},
             {'ID':'FeII2344' ,'Metalline':'FeII', 'Metalwave':2344.21000},
             {'ID':'FeII1144' ,'Metalline':'FeII', 'Metalwave':1144.94000},
             {'ID':'FeII2586' ,'Metalline':'FeII', 'Metalwave':2586.65000},
             {'ID':'FeII1608' ,'Metalline':'FeII', 'Metalwave':1608.45000},
             {'ID':'FeII2374' ,'Metalline':'FeII', 'Metalwave':2374.46000},
             {'ID':'FeII1081' ,'Metalline':'FeII', 'Metalwave':1081.87000},
             {'ID':'FeII1112' ,'Metalline':'FeII', 'Metalwave':1112.05000},
             {'ID':'FeII2260' ,'Metalline':'FeII', 'Metalwave':2260.78000},
             {'ID':'FeII1611' ,'Metalline':'FeII', 'Metalwave':1611.20000},
             {'ID':'AlIII1854','Metalline':'AlIII','Metalwave':1854.72000},
             {'ID':'AlIII1862','Metalline':'AlIII','Metalwave':1862.79000},
             {'ID':'ZnII2026' ,'Metalline':'ZnII', 'Metalwave':2026.13709},
             {'ID':'ZnII2062' ,'Metalline':'ZnII', 'Metalwave':2062.66045},
             {'ID':'NIII989'  ,'Metalline':'NIII', 'Metalwave': 989.79900}]

H2I = [{'wave':1108.1280000,'strength':0.001730,'gamma':2.000E8},
       {'wave':1092.1950000,'strength':0.005960,'gamma':2.000E8},
       {'wave':1077.1380000,'strength':0.011900,'gamma':2.000E8},
       {'wave':1062.8830000,'strength':0.018200,'gamma':2.000E8},
       {'wave':1049.3660000,'strength':0.023500,'gamma':2.000E8},
       {'wave':1036.5460000,'strength':0.027100,'gamma':2.000E8},
       {'wave':1024.3640000,'strength':0.028800,'gamma':2.000E8},
       {'wave':1012.8220000,'strength':0.029700,'gamma':2.000E8},
       {'wave':1001.8260000,'strength':0.026600,'gamma':2.000E8},
       {'wave': 991.3940000,'strength':0.025900,'gamma':2.000E8},
       {'wave': 981.4410000,'strength':0.020400,'gamma':2.000E8},
       {'wave': 971.9840000,'strength':0.019700,'gamma':2.000E8},
       {'wave': 962.9780000,'strength':0.012900,'gamma':2.000E8},
       {'wave': 954.4190000,'strength':0.013800,'gamma':2.000E8},
       {'wave': 946.1700000,'strength':0.001100,'gamma':2.000E8},
       {'wave': 938.4680000,'strength':0.009190,'gamma':2.000E8},
       {'wave': 931.0630000,'strength':0.010200,'gamma':2.000E8},
       {'wave': 923.9860000,'strength':0.005900,'gamma':2.000E8},
       {'wave': 917.2450000,'strength':0.005870,'gamma':2.000E8},
       {'wave': 914.8200000,'strength':0.003660,'gamma':2.000E8},
       {'wave': 904.7090000,'strength':0.002480,'gamma':2.000E8},
       {'wave':1008.5530000,'strength':0.044800,'gamma':2.000E8},
       {'wave': 985.6320000,'strength':0.069600,'gamma':2.000E8},
       {'wave': 964.9880000,'strength':0.068800,'gamma':2.000E8},
       {'wave': 946.4250000,'strength':0.062100,'gamma':2.000E8},
       {'wave': 929.5340000,'strength':0.033900,'gamma':2.000E8},
       {'wave': 914.3980000,'strength':0.024000,'gamma':2.000E8},
       {'wave': 900.8040000,'strength':0.016200,'gamma':2.000E8}]

H2I = [{'wave':1313.37643,'strength':0.0494,'gamma':2.000E8},
       {'wave':1324.59501,'strength':0.0538,'gamma':2.000E8},
       {'wave':1345.17788,'strength':0.0508,'gamma':2.000E8},
       {'wave':1356.48760,'strength':0.0821,'gamma':2.000E8},
       {'wave':1371.42241,'strength':0.0816,'gamma':2.000E8},
       {'wave':1389.59379,'strength':0.0816,'gamma':2.000E8},
       {'wave':1410.64800,'strength':0.0821,'gamma':2.000E8},
       {'wave':1383.65916,'strength':0.0739,'gamma':2.000E8},
       {'wave':1403.98260,'strength':0.0765,'gamma':2.000E8},
       {'wave':1427.01340,'strength':0.0793,'gamma':2.000E8}]

def print_group(message=None,title=False):
    if '-h' in sys.argv or '--help' in sys.argv:
        print('\n'+'-'*65+'\n  '+message+'\n'+'-'*65)
        if title:
            print('    >>> quasar operation [--arg1] [--arg2]')

print_group('Quasar Astronomy Research Tool',title=True)
operation = None if len(sys.argv)==1 else sys.argv[1]
group1 = 'Fine-structure constant parameters'
group2 = 'Coordinates parameters'
group3 = 'Voigt profile parameters'
group4 = 'Plotting parameters'
group5 = 'Spectral arguments'
group6 = 'File name parameters'
group7 = 'Other parameters'
group8 = 'VPFIT vp_setup.dat parameters'
args = numpy.array([[group1,'-a','--alpha'       ,float,               0,'Fine-structure constant value'               ],
                    [group1,''  ,'--xdipp'       ,float,            17.3,'Right ascension of alpha dipole'             ],
                    [group1,''  ,'--ydipp'       ,float,             -61,'Declination of alpha dipole'                 ],
                    [group2,''  ,'--ra'          ,str  ,            None,'Right ascension'                             ],
                    [group2,''  ,'--ra1'         ,str  ,            None,'Right ascension of first point'              ],
                    [group2,''  ,'--ra2'         ,str  ,            None,'Right ascension of second point'             ],
                    [group2,''  ,'--dec'         ,str  ,            None,'declination'                                 ],
                    [group2,''  ,'--dec1'        ,str  ,            None,'Declination of first point'                  ],
                    [group2,''  ,'--dec2'        ,str  ,            None,'Declination of second point'                 ],
                    [group2,''  ,'--simbad'      ,str  ,            None,'Coordinates from SIMBAD'                     ],
                    [group3,'-w','--wa'          ,float,            None,'Wavelength(s)'                               ],
                    [group3,'-z','--z'           ,float,            None,'Redshift of the object'                      ],
                    [group3,''  ,'--zabs'        ,float,            None,'Absorption redshift'                         ],
                    [group3,''  ,'--zem'         ,float,            None,'Emission redshift'                           ],
                    [group3,'-n','--col'         ,float,              19,'Column density'                              ],
                    [group3,'-b','--dop'         ,float,              15,'Doppler parameter'                           ],
                    [group3,''  ,'--bfactor'     ,float,              10,'Factor between Doppler parameters'           ],
                    [group3,''  ,'--colmin'      ,float,              15,'Minimum column density'                      ],
                    [group3,''  ,'--colmax'      ,float,              21,'Maximum column density'                      ],
                    [group3,''  ,'--nratio'      ,float,            -5.3,'Column density ratio between both components'],
                    [group3,''  ,'--vsep'        ,float,             82.,'Velocity sepration between both components'  ],
                    [group4,''  ,'--model'       ,bool ,           False,'Use model'                                   ],
                    [group4,''  ,'--nbin'        ,float,               6,'Number of models'                            ],
                    [group4,''  ,'--xmin'        ,float,            None,'Minimum X axis value'                        ],
                    [group4,''  ,'--xmax'        ,float,            None,'Maximum X axis value'                        ],
                    [group4,''  ,'--ymin'        ,float,            None,'Minimum Y axis value'                        ],
                    [group4,''  ,'--ymax'        ,float,            None,'Maximum Y axis value'                        ],
                    [group5,''  ,'--wbeg'        ,float,           4000.,'First wavelength'                            ],
                    [group5,''  ,'--wend'        ,float,           7000.,'Last wavelength'                             ],
                    [group5,''  ,'--dw'          ,float,            None,'Wavelength separation'                       ],
                    [group5,''  ,'--fwhm'        ,float,             7.0,'Full Width Half Maximum resolution'          ],
                    [group5,''  ,'--noise'       ,float,             80.,'Noise'                                       ],
                    [group5,'-v','--dv'          ,float,            500.,'Velocity dispersion of the absorption system'],
                    [group5,''  ,'--midflx'      ,float,            None,'Reference flux to calculate full width'      ],
                    [group5,'-r','--res'         ,float,           45000,'Spectral resolution'                         ],
                    [group5,''  ,'--snr'         ,float,            None,'Signal-to-Noise Ratio'                       ],
                    [group6,'-f','--filename'    ,str  ,            None,'Quasar spectrum file'                        ],
                    [group6,'-l','--qsolist'     ,str  ,            None,'Quasar list file'                            ],
                    [group6,'-o','--output'      ,str  ,            None,'Output file name'                            ],
                    [group6,''  ,'--metals'      ,str  ,            None,'List of metal transitions'                   ],
                    [group7,''  ,'--Nn'          ,int  ,               0,'Total number of neutrons'                    ],
                    [group7,''  ,'--Np'          ,int  ,               1,'Total number of protons'                     ],
                    [group7,''  ,'--path'        ,str  ,            './','Target path'                                 ],
                    [group7,''  ,'--powerlaw'    ,bool ,           False,'Initialise powerlaw continuum'               ],
                    [group7,''  ,'--slope'       ,float,            None,'Distortion slope'                            ],
                    [group7,''  ,'--todo'        ,str  ,           'all','Action to perform'                           ],
                    [group7,''  ,'--version'     ,float,              10,'Distortion slope'                            ],
                    [group8,''  ,'--lastchtied'  ,str  ,             'w',''                                            ],
                    [group8,''  ,'--bvalmax'     ,str  ,'2500.0 50000.0',''                                            ],
                    [group8,''  ,'--bvalmin'     ,str  ,   '0.300 0.300',''                                            ],
                    [group8,''  ,'--bltdrop'     ,str  ,          '0.05',''                                            ],
                    [group8,''  ,'--clogltdrop'  ,str  ,          '13.3',''                                            ],
                    [group8,''  ,'--bgtdrop'     ,str  ,        '50001.',''                                            ],
                    [group8,''  ,'--fcollallzn'  ,str  ,      '4.162e22',''                                            ],
                    [group8,''  ,'--sigscalemult',str  ,           '1.0',''                                            ],
                    [group8,''  ,'--date'        ,str  ,              '',''                                            ],
                    [group8,''  ,'--dots'        ,str  ,             '1',''                                            ],
                    [group8,''  ,'--gcursor'     ,str  ,              '',''                                            ],
                    [group8,''  ,'--adsplit'     ,str  ,           '2.5',''                                            ],
                    [group8,''  ,'--maxadrem'    ,str  ,            '75',''                                            ],
                    [group8,''  ,'--absigp'      ,str  ,          '10.0',''                                            ],
                    [group8,''  ,'--adcontf'     ,str  ,'2.210 5.0 12.5',''                                            ],
                    [group8,''  ,'--vform'       ,str  ,              '',''                                            ],
                    [group8,''  ,'--nsubmin'     ,str  ,            '11',''                                            ],
                    [group8,''  ,'--nsubmax'     ,str  ,            '21',''                                            ],
                    [group8,''  ,'--nfwhmp'      ,str  ,            '10',''                                            ],
                    [group8,''  ,'--pcvals'      ,str  ,              '',''                                            ],
                    [group8,''  ,'--verbose'     ,bool ,           False,'Print verbose'                               ],
                    [group8,''  ,'--chisqthres'  ,str  , '1E-4 5.0 1E-2',''                                            ],
                    [group8,''  ,'--novars'      ,str  ,             '4',''                                            ],
                    [group8,''  ,'--fdbstep'     ,str  ,           '0.1',''                                            ],
                    [group8,''  ,'--fdzstep'     ,str  ,          '1E-6',''                                            ],
                    [group8,''  ,'--fdcdstep'    ,str  ,         '0.005',''                                            ],
                    [group8,''  ,'--fdx4step'    ,str  ,          '1e-6',''                                            ]])

locals().update(get_argument(args))
