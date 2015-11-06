# This file was automatically created by FeynRules 2.3.9
# Mathematica version: 10.2.0 for Linux x86 (64-bit) (July 6, 2015)
# Date: Wed 23 Sep 2015 13:54:43


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



UVGC_100_1 = Coupling(name = 'UVGC_100_1',
                      value = {-1:'(-9*G**3)/(128.*cmath.pi**2)'},
                      order = {'QCD':3})

UVGC_100_2 = Coupling(name = 'UVGC_100_2',
                      value = {-1:'G**3/(128.*cmath.pi**2)'},
                      order = {'QCD':3})

UVGC_101_3 = Coupling(name = 'UVGC_101_3',
                      value = {-1:'(3*G**4)/(512.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_101_4 = Coupling(name = 'UVGC_101_4',
                      value = {-1:'(-3*G**4)/(512.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_102_5 = Coupling(name = 'UVGC_102_5',
                      value = {-1:'(3*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_102_6 = Coupling(name = 'UVGC_102_6',
                      value = {-1:'(-3*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_104_7 = Coupling(name = 'UVGC_104_7',
                      value = {-1:'-(complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_104_8 = Coupling(name = 'UVGC_104_8',
                      value = {-1:'(complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_105_9 = Coupling(name = 'UVGC_105_9',
                      value = {-1:'(-3*complex(0,1)*G**4)/(256.*cmath.pi**2)'},
                      order = {'QCD':4})

UVGC_105_10 = Coupling(name = 'UVGC_105_10',
                       value = {-1:'(3*complex(0,1)*G**4)/(256.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_106_11 = Coupling(name = 'UVGC_106_11',
                       value = {-1:'-(complex(0,1)*G**4)/(24.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_106_12 = Coupling(name = 'UVGC_106_12',
                       value = {-1:'(47*complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_107_13 = Coupling(name = 'UVGC_107_13',
                       value = {-1:'(-253*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_107_14 = Coupling(name = 'UVGC_107_14',
                       value = {-1:'(5*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_108_15 = Coupling(name = 'UVGC_108_15',
                       value = {-1:'( 0 if MB else (complex(0,1)*G**3)/(48.*cmath.pi**2) )'},
                       order = {'QCD':3})

UVGC_108_16 = Coupling(name = 'UVGC_108_16',
                       value = {-1:'( 0 if MC else (complex(0,1)*G**3)/(48.*cmath.pi**2) )'},
                       order = {'QCD':3})

UVGC_108_17 = Coupling(name = 'UVGC_108_17',
                       value = {-1:'(complex(0,1)*G**3)/(48.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_108_18 = Coupling(name = 'UVGC_108_18',
                       value = {-1:'(-19*complex(0,1)*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_108_19 = Coupling(name = 'UVGC_108_19',
                       value = {-1:'-(complex(0,1)*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_108_20 = Coupling(name = 'UVGC_108_20',
                       value = {-1:'( 0 if MT else (complex(0,1)*G**3)/(48.*cmath.pi**2) )'},
                       order = {'QCD':3})

UVGC_108_21 = Coupling(name = 'UVGC_108_21',
                       value = {-1:'(complex(0,1)*G**3)/(12.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_111_22 = Coupling(name = 'UVGC_111_22',
                       value = {-1:'(ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_111_23 = Coupling(name = 'UVGC_111_23',
                       value = {-1:'-(ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_112_24 = Coupling(name = 'UVGC_112_24',
                       value = {-1:'( (complex(0,1)*G**2)/(6.*cmath.pi**2) if MB else -(complex(0,1)*G**2)/(12.*cmath.pi**2) ) + (complex(0,1)*G**2)/(12.*cmath.pi**2)',0:'( (5*complex(0,1)*G**2)/(12.*cmath.pi**2) - (complex(0,1)*G**2*reglog(MB/MU_R))/(2.*cmath.pi**2) if MB else (complex(0,1)*G**2)/(12.*cmath.pi**2) ) - (complex(0,1)*G**2)/(12.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_113_25 = Coupling(name = 'UVGC_113_25',
                       value = {-1:'( (ee*complex(0,1)*G**2)/(18.*cmath.pi**2) if MB else -(ee*complex(0,1)*G**2)/(36.*cmath.pi**2) )',0:'( (5*ee*complex(0,1)*G**2)/(36.*cmath.pi**2) - (ee*complex(0,1)*G**2*reglog(MB/MU_R))/(6.*cmath.pi**2) if MB else (ee*complex(0,1)*G**2)/(36.*cmath.pi**2) ) - (ee*complex(0,1)*G**2)/(36.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_114_26 = Coupling(name = 'UVGC_114_26',
                       value = {-1:'( -(complex(0,1)*G**3)/(6.*cmath.pi**2) if MB else (complex(0,1)*G**3)/(12.*cmath.pi**2) )',0:'( (-5*complex(0,1)*G**3)/(12.*cmath.pi**2) + (complex(0,1)*G**3*reglog(MB/MU_R))/(2.*cmath.pi**2) if MB else -(complex(0,1)*G**3)/(12.*cmath.pi**2) ) + (complex(0,1)*G**3)/(12.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_115_27 = Coupling(name = 'UVGC_115_27',
                       value = {-1:'( (complex(0,1)*G**2*MB)/(6.*cmath.pi**2) if MB else -(complex(0,1)*G**2*MB)/(3.*cmath.pi**2) ) + (complex(0,1)*G**2*MB)/(3.*cmath.pi**2)',0:'( (5*complex(0,1)*G**2*MB)/(6.*cmath.pi**2) - (complex(0,1)*G**2*MB*reglog(MB/MU_R))/cmath.pi**2 if MB else (complex(0,1)*G**2*MB)/(6.*cmath.pi**2) ) - (complex(0,1)*G**2*MB)/(6.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_116_28 = Coupling(name = 'UVGC_116_28',
                       value = {-1:'( (cw*ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2) if MB else -(cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) ) + (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2)',0:'( (5*cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (5*ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) - (cw*ee*complex(0,1)*G**2*reglog(MB/MU_R))/(4.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw*reglog(MB/MU_R))/(12.*cw*cmath.pi**2) if MB else (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) ) - (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_117_29 = Coupling(name = 'UVGC_117_29',
                       value = {-1:'( -(ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) if MB else (ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2) ) - (ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2)',0:'( (-5*ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2) + (ee*complex(0,1)*G**2*sw*reglog(MB/MU_R))/(6.*cw*cmath.pi**2) if MB else -(ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2) ) + (ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_118_30 = Coupling(name = 'UVGC_118_30',
                       value = {-1:'( (complex(0,1)*G**2*MB)/(6.*cmath.pi**2*vev) if MB else -(complex(0,1)*G**2*MB)/(3.*cmath.pi**2*vev) ) + (complex(0,1)*G**2*MB)/(3.*cmath.pi**2*vev)',0:'( (5*complex(0,1)*G**2*MB)/(6.*cmath.pi**2*vev) - (complex(0,1)*G**2*MB*reglog(MB/MU_R))/(cmath.pi**2*vev) if MB else (complex(0,1)*G**2*MB)/(6.*cmath.pi**2*vev) ) - (complex(0,1)*G**2*MB)/(6.*cmath.pi**2*vev)'},
                       order = {'QCD':2,'QED':1})

UVGC_119_31 = Coupling(name = 'UVGC_119_31',
                       value = {-1:'( -(G**2*MB)/(6.*cmath.pi**2*vev) if MB else (G**2*MB)/(3.*cmath.pi**2*vev) ) - (G**2*MB)/(3.*cmath.pi**2*vev)',0:'( (-5*G**2*MB)/(6.*cmath.pi**2*vev) + (G**2*MB*reglog(MB/MU_R))/(cmath.pi**2*vev) if MB else -(G**2*MB)/(6.*cmath.pi**2*vev) ) + (G**2*MB)/(6.*cmath.pi**2*vev)'},
                       order = {'QCD':2,'QED':1})

UVGC_120_32 = Coupling(name = 'UVGC_120_32',
                       value = {-1:'( (complex(0,1)*G**2)/(6.*cmath.pi**2) if MC else -(complex(0,1)*G**2)/(12.*cmath.pi**2) ) + (complex(0,1)*G**2)/(12.*cmath.pi**2)',0:'( (5*complex(0,1)*G**2)/(12.*cmath.pi**2) - (complex(0,1)*G**2*reglog(MC/MU_R))/(2.*cmath.pi**2) if MC else (complex(0,1)*G**2)/(12.*cmath.pi**2) ) - (complex(0,1)*G**2)/(12.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_121_33 = Coupling(name = 'UVGC_121_33',
                       value = {-1:'( -(ee*complex(0,1)*G**2)/(9.*cmath.pi**2) if MC else (ee*complex(0,1)*G**2)/(18.*cmath.pi**2) )',0:'( (-5*ee*complex(0,1)*G**2)/(18.*cmath.pi**2) + (ee*complex(0,1)*G**2*reglog(MC/MU_R))/(3.*cmath.pi**2) if MC else -(ee*complex(0,1)*G**2)/(18.*cmath.pi**2) ) + (ee*complex(0,1)*G**2)/(18.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_122_34 = Coupling(name = 'UVGC_122_34',
                       value = {-1:'( -(complex(0,1)*G**3)/(6.*cmath.pi**2) if MC else (complex(0,1)*G**3)/(12.*cmath.pi**2) )',0:'( (-5*complex(0,1)*G**3)/(12.*cmath.pi**2) + (complex(0,1)*G**3*reglog(MC/MU_R))/(2.*cmath.pi**2) if MC else -(complex(0,1)*G**3)/(12.*cmath.pi**2) ) + (complex(0,1)*G**3)/(12.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_123_35 = Coupling(name = 'UVGC_123_35',
                       value = {-1:'( (complex(0,1)*G**2*MC)/(6.*cmath.pi**2) if MC else -(complex(0,1)*G**2*MC)/(3.*cmath.pi**2) ) + (complex(0,1)*G**2*MC)/(3.*cmath.pi**2)',0:'( (5*complex(0,1)*G**2*MC)/(6.*cmath.pi**2) - (complex(0,1)*G**2*MC*reglog(MC/MU_R))/cmath.pi**2 if MC else (complex(0,1)*G**2*MC)/(6.*cmath.pi**2) ) - (complex(0,1)*G**2*MC)/(6.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_124_36 = Coupling(name = 'UVGC_124_36',
                       value = {-1:'( -(ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw*cmath.sqrt(2)) if MC else (ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) )',0:'( (-5*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) + (ee*complex(0,1)*G**2*reglog(MC/MU_R))/(4.*cmath.pi**2*sw*cmath.sqrt(2)) if MC else -(ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) ) + (ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_125_37 = Coupling(name = 'UVGC_125_37',
                       value = {-1:'( -(cw*ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2) if MC else (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) ) - (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2)',0:'( (-5*cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (5*ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) + (cw*ee*complex(0,1)*G**2*reglog(MC/MU_R))/(4.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw*reglog(MC/MU_R))/(12.*cw*cmath.pi**2) if MC else -(cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) ) + (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_126_38 = Coupling(name = 'UVGC_126_38',
                       value = {-1:'( (ee*complex(0,1)*G**2*sw)/(9.*cw*cmath.pi**2) if MC else -(ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) ) + (ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2)',0:'( (5*ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) - (ee*complex(0,1)*G**2*sw*reglog(MC/MU_R))/(3.*cw*cmath.pi**2) if MC else (ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) ) - (ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_127_39 = Coupling(name = 'UVGC_127_39',
                       value = {-1:'( (G**2*MC)/(6.*cmath.pi**2*vev) if MC else -(G**2*MC)/(3.*cmath.pi**2*vev) ) + (G**2*MC)/(3.*cmath.pi**2*vev)',0:'( (5*G**2*MC)/(6.*cmath.pi**2*vev) - (G**2*MC*reglog(MC/MU_R))/(cmath.pi**2*vev) if MC else (G**2*MC)/(6.*cmath.pi**2*vev) ) - (G**2*MC)/(6.*cmath.pi**2*vev)'},
                       order = {'QCD':2,'QED':1})

UVGC_128_40 = Coupling(name = 'UVGC_128_40',
                       value = {-1:'( (complex(0,1)*G**2*MC)/(6.*cmath.pi**2*vev) if MC else -(complex(0,1)*G**2*MC)/(3.*cmath.pi**2*vev) ) + (complex(0,1)*G**2*MC)/(3.*cmath.pi**2*vev)',0:'( (5*complex(0,1)*G**2*MC)/(6.*cmath.pi**2*vev) - (complex(0,1)*G**2*MC*reglog(MC/MU_R))/(cmath.pi**2*vev) if MC else (complex(0,1)*G**2*MC)/(6.*cmath.pi**2*vev) ) - (complex(0,1)*G**2*MC)/(6.*cmath.pi**2*vev)'},
                       order = {'QCD':2,'QED':1})

UVGC_129_41 = Coupling(name = 'UVGC_129_41',
                       value = {-1:'( (G**2*MC)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MC else (-7*G**2*MC)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (5*G**2*MC)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) - (3*G**2*MC*reglog(MC/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MC else (G**2*MC)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) ) - (G**2*MC)/(4.*cmath.pi**2*vev*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_129_42 = Coupling(name = 'UVGC_129_42',
                       value = {-1:'-(G**2*MC)/(12.*cmath.pi**2*vev*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_129_43 = Coupling(name = 'UVGC_129_43',
                       value = {-1:'(G**2*MC*cmath.sqrt(2))/(3.*cmath.pi**2*vev)'},
                       order = {'QCD':2,'QED':1})

UVGC_130_44 = Coupling(name = 'UVGC_130_44',
                       value = {-1:'( -(G**2*MC)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MC else (7*G**2*MC)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (-5*G**2*MC)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) + (3*G**2*MC*reglog(MC/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MC else -(G**2*MC)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) ) + (G**2*MC)/(4.*cmath.pi**2*vev*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_130_45 = Coupling(name = 'UVGC_130_45',
                       value = {-1:'(G**2*MC)/(12.*cmath.pi**2*vev*cmath.sqrt(2))'},
                       order = {'QCD':2,'QED':1})

UVGC_130_46 = Coupling(name = 'UVGC_130_46',
                       value = {-1:'-(G**2*MC*cmath.sqrt(2))/(3.*cmath.pi**2*vev)'},
                       order = {'QCD':2,'QED':1})

UVGC_131_47 = Coupling(name = 'UVGC_131_47',
                       value = {-1:'( 0 if MB else (complex(0,1)*G**2)/(24.*cmath.pi**2) ) - (complex(0,1)*G**2)/(24.*cmath.pi**2)',0:'( (complex(0,1)*G**2*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':2})

UVGC_131_48 = Coupling(name = 'UVGC_131_48',
                       value = {-1:'( 0 if MC else (complex(0,1)*G**2)/(24.*cmath.pi**2) ) - (complex(0,1)*G**2)/(24.*cmath.pi**2)',0:'( (complex(0,1)*G**2*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':2})

UVGC_131_49 = Coupling(name = 'UVGC_131_49',
                       value = {-1:'( 0 if MT else (complex(0,1)*G**2)/(24.*cmath.pi**2) ) - (complex(0,1)*G**2)/(24.*cmath.pi**2)',0:'( (complex(0,1)*G**2*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':2})

UVGC_132_50 = Coupling(name = 'UVGC_132_50',
                       value = {-1:'( 0 if MB else -G**3/(16.*cmath.pi**2) ) + G**3/(24.*cmath.pi**2)',0:'( -(G**3*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':3})

UVGC_132_51 = Coupling(name = 'UVGC_132_51',
                       value = {-1:'( 0 if MC else -G**3/(16.*cmath.pi**2) ) + G**3/(24.*cmath.pi**2)',0:'( -(G**3*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':3})

UVGC_132_52 = Coupling(name = 'UVGC_132_52',
                       value = {-1:'-G**3/(48.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_132_53 = Coupling(name = 'UVGC_132_53',
                       value = {-1:'(51*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_132_54 = Coupling(name = 'UVGC_132_54',
                       value = {-1:'( 0 if MT else -G**3/(16.*cmath.pi**2) ) + G**3/(24.*cmath.pi**2)',0:'( -(G**3*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':3})

UVGC_133_55 = Coupling(name = 'UVGC_133_55',
                       value = {-1:'(21*G**3)/(64.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_133_56 = Coupling(name = 'UVGC_133_56',
                       value = {-1:'G**3/(64.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_134_57 = Coupling(name = 'UVGC_134_57',
                       value = {-1:'(33*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_134_58 = Coupling(name = 'UVGC_134_58',
                       value = {-1:'(3*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_135_59 = Coupling(name = 'UVGC_135_59',
                       value = {-1:'( 0 if MB else G**3/(16.*cmath.pi**2) ) - G**3/(24.*cmath.pi**2)',0:'( (G**3*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':3})

UVGC_135_60 = Coupling(name = 'UVGC_135_60',
                       value = {-1:'( 0 if MC else G**3/(16.*cmath.pi**2) ) - G**3/(24.*cmath.pi**2)',0:'( (G**3*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':3})

UVGC_135_61 = Coupling(name = 'UVGC_135_61',
                       value = {-1:'G**3/(48.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_135_62 = Coupling(name = 'UVGC_135_62',
                       value = {-1:'(-33*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_135_63 = Coupling(name = 'UVGC_135_63',
                       value = {-1:'(-3*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_135_64 = Coupling(name = 'UVGC_135_64',
                       value = {-1:'( 0 if MT else G**3/(16.*cmath.pi**2) ) - G**3/(24.*cmath.pi**2)',0:'( (G**3*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':3})

UVGC_136_65 = Coupling(name = 'UVGC_136_65',
                       value = {-1:'(-21*G**3)/(64.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_136_66 = Coupling(name = 'UVGC_136_66',
                       value = {-1:'-G**3/(64.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_137_67 = Coupling(name = 'UVGC_137_67',
                       value = {-1:'(-51*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_137_68 = Coupling(name = 'UVGC_137_68',
                       value = {-1:'-G**3/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_138_69 = Coupling(name = 'UVGC_138_69',
                       value = {-1:'( 0 if MB else -(complex(0,1)*G**4)/(12.*cmath.pi**2) ) + (complex(0,1)*G**4)/(12.*cmath.pi**2)',0:'( -(complex(0,1)*G**4*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':4})

UVGC_138_70 = Coupling(name = 'UVGC_138_70',
                       value = {-1:'( 0 if MC else -(complex(0,1)*G**4)/(12.*cmath.pi**2) ) + (complex(0,1)*G**4)/(12.*cmath.pi**2)',0:'( -(complex(0,1)*G**4*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':4})

UVGC_138_71 = Coupling(name = 'UVGC_138_71',
                       value = {-1:'(147*complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_138_72 = Coupling(name = 'UVGC_138_72',
                       value = {-1:'(3*complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_138_73 = Coupling(name = 'UVGC_138_73',
                       value = {-1:'( 0 if MT else -(complex(0,1)*G**4)/(12.*cmath.pi**2) ) + (complex(0,1)*G**4)/(12.*cmath.pi**2)',0:'( -(complex(0,1)*G**4*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':4})

UVGC_139_74 = Coupling(name = 'UVGC_139_74',
                       value = {-1:'(147*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_139_75 = Coupling(name = 'UVGC_139_75',
                       value = {-1:'(21*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_140_76 = Coupling(name = 'UVGC_140_76',
                       value = {-1:'( 0 if MB else -(complex(0,1)*G**4)/(12.*cmath.pi**2) )',0:'( -(complex(0,1)*G**4*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':4})

UVGC_140_77 = Coupling(name = 'UVGC_140_77',
                       value = {-1:'( 0 if MC else -(complex(0,1)*G**4)/(12.*cmath.pi**2) )',0:'( -(complex(0,1)*G**4*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':4})

UVGC_140_78 = Coupling(name = 'UVGC_140_78',
                       value = {-1:'-(complex(0,1)*G**4)/(12.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_140_79 = Coupling(name = 'UVGC_140_79',
                       value = {-1:'(523*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_140_80 = Coupling(name = 'UVGC_140_80',
                       value = {-1:'(13*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_140_81 = Coupling(name = 'UVGC_140_81',
                       value = {-1:'( 0 if MT else -(complex(0,1)*G**4)/(12.*cmath.pi**2) )',0:'( -(complex(0,1)*G**4*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':4})

UVGC_141_82 = Coupling(name = 'UVGC_141_82',
                       value = {-1:'( 0 if MB else (complex(0,1)*G**4)/(12.*cmath.pi**2) ) - (complex(0,1)*G**4)/(24.*cmath.pi**2)',0:'( (complex(0,1)*G**4*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':4})

UVGC_141_83 = Coupling(name = 'UVGC_141_83',
                       value = {-1:'( 0 if MC else (complex(0,1)*G**4)/(12.*cmath.pi**2) ) - (complex(0,1)*G**4)/(24.*cmath.pi**2)',0:'( (complex(0,1)*G**4*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':4})

UVGC_141_84 = Coupling(name = 'UVGC_141_84',
                       value = {-1:'(complex(0,1)*G**4)/(24.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_141_85 = Coupling(name = 'UVGC_141_85',
                       value = {-1:'(-341*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_141_86 = Coupling(name = 'UVGC_141_86',
                       value = {-1:'(-11*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_141_87 = Coupling(name = 'UVGC_141_87',
                       value = {-1:'( 0 if MT else (complex(0,1)*G**4)/(12.*cmath.pi**2) ) - (complex(0,1)*G**4)/(24.*cmath.pi**2)',0:'( (complex(0,1)*G**4*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':4})

UVGC_142_88 = Coupling(name = 'UVGC_142_88',
                       value = {-1:'(-83*complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_142_89 = Coupling(name = 'UVGC_142_89',
                       value = {-1:'(-5*complex(0,1)*G**4)/(128.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_143_90 = Coupling(name = 'UVGC_143_90',
                       value = {-1:'( 0 if MB else (complex(0,1)*G**4)/(12.*cmath.pi**2) )',0:'( (complex(0,1)*G**4*reglog(MB/MU_R))/(12.*cmath.pi**2) if MB else 0 )'},
                       order = {'QCD':4})

UVGC_143_91 = Coupling(name = 'UVGC_143_91',
                       value = {-1:'( 0 if MC else (complex(0,1)*G**4)/(12.*cmath.pi**2) )',0:'( (complex(0,1)*G**4*reglog(MC/MU_R))/(12.*cmath.pi**2) if MC else 0 )'},
                       order = {'QCD':4})

UVGC_143_92 = Coupling(name = 'UVGC_143_92',
                       value = {-1:'(complex(0,1)*G**4)/(12.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_143_93 = Coupling(name = 'UVGC_143_93',
                       value = {-1:'(-85*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_143_94 = Coupling(name = 'UVGC_143_94',
                       value = {-1:'(-19*complex(0,1)*G**4)/(512.*cmath.pi**2)'},
                       order = {'QCD':4})

UVGC_143_95 = Coupling(name = 'UVGC_143_95',
                       value = {-1:'( 0 if MT else (complex(0,1)*G**4)/(12.*cmath.pi**2) )',0:'( (complex(0,1)*G**4*reglog(MT/MU_R))/(12.*cmath.pi**2) if MT else 0 )'},
                       order = {'QCD':4})

UVGC_144_96 = Coupling(name = 'UVGC_144_96',
                       value = {-1:'( (complex(0,1)*G**2)/(6.*cmath.pi**2) if MT else -(complex(0,1)*G**2)/(12.*cmath.pi**2) ) + (complex(0,1)*G**2)/(12.*cmath.pi**2)',0:'( (5*complex(0,1)*G**2)/(12.*cmath.pi**2) - (complex(0,1)*G**2*reglog(MT/MU_R))/(2.*cmath.pi**2) if MT else (complex(0,1)*G**2)/(12.*cmath.pi**2) ) - (complex(0,1)*G**2)/(12.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_145_97 = Coupling(name = 'UVGC_145_97',
                       value = {-1:'( -(ee*complex(0,1)*G**2)/(9.*cmath.pi**2) if MT else (ee*complex(0,1)*G**2)/(18.*cmath.pi**2) )',0:'( (-5*ee*complex(0,1)*G**2)/(18.*cmath.pi**2) + (ee*complex(0,1)*G**2*reglog(MT/MU_R))/(3.*cmath.pi**2) if MT else -(ee*complex(0,1)*G**2)/(18.*cmath.pi**2) ) + (ee*complex(0,1)*G**2)/(18.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_146_98 = Coupling(name = 'UVGC_146_98',
                       value = {-1:'( -(complex(0,1)*G**3)/(6.*cmath.pi**2) if MT else (complex(0,1)*G**3)/(12.*cmath.pi**2) )',0:'( (-5*complex(0,1)*G**3)/(12.*cmath.pi**2) + (complex(0,1)*G**3*reglog(MT/MU_R))/(2.*cmath.pi**2) if MT else -(complex(0,1)*G**3)/(12.*cmath.pi**2) ) + (complex(0,1)*G**3)/(12.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_147_99 = Coupling(name = 'UVGC_147_99',
                       value = {-1:'( (complex(0,1)*G**2*MT)/(6.*cmath.pi**2) if MT else -(complex(0,1)*G**2*MT)/(3.*cmath.pi**2) ) + (complex(0,1)*G**2*MT)/(3.*cmath.pi**2)',0:'( (5*complex(0,1)*G**2*MT)/(6.*cmath.pi**2) - (complex(0,1)*G**2*MT*reglog(MT/MU_R))/cmath.pi**2 if MT else (complex(0,1)*G**2*MT)/(6.*cmath.pi**2) ) - (complex(0,1)*G**2*MT)/(6.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_148_100 = Coupling(name = 'UVGC_148_100',
                        value = {-1:'( -(ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw*cmath.sqrt(2)) if MB else (ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) )',0:'( (-5*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) + (ee*complex(0,1)*G**2*reglog(MB/MU_R))/(4.*cmath.pi**2*sw*cmath.sqrt(2)) if MB else -(ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) ) + (ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_148_101 = Coupling(name = 'UVGC_148_101',
                        value = {-1:'( -(ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw*cmath.sqrt(2)) if MT else (ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) )',0:'( (-5*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) + (ee*complex(0,1)*G**2*reglog(MT/MU_R))/(4.*cmath.pi**2*sw*cmath.sqrt(2)) if MT else -(ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2)) ) + (ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_149_102 = Coupling(name = 'UVGC_149_102',
                        value = {-1:'( -(cw*ee*complex(0,1)*G**2)/(12.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(36.*cw*cmath.pi**2) if MT else (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) ) - (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2)',0:'( (-5*cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (5*ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) + (cw*ee*complex(0,1)*G**2*reglog(MT/MU_R))/(4.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw*reglog(MT/MU_R))/(12.*cw*cmath.pi**2) if MT else -(cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) + (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2) ) + (cw*ee*complex(0,1)*G**2)/(24.*cmath.pi**2*sw) - (ee*complex(0,1)*G**2*sw)/(72.*cw*cmath.pi**2)'},
                        order = {'QCD':2,'QED':1})

UVGC_150_103 = Coupling(name = 'UVGC_150_103',
                        value = {-1:'( (ee*complex(0,1)*G**2*sw)/(9.*cw*cmath.pi**2) if MT else -(ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) ) + (ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2)',0:'( (5*ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) - (ee*complex(0,1)*G**2*sw*reglog(MT/MU_R))/(3.*cw*cmath.pi**2) if MT else (ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2) ) - (ee*complex(0,1)*G**2*sw)/(18.*cw*cmath.pi**2)'},
                        order = {'QCD':2,'QED':1})

UVGC_151_104 = Coupling(name = 'UVGC_151_104',
                        value = {-1:'( (G**2*MB)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else (-7*G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (5*G**2*MB)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) - (3*G**2*MB*reglog(MB/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else (G**2*MB)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) ) - (G**2*MB)/(4.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_151_105 = Coupling(name = 'UVGC_151_105',
                        value = {-1:'( (G**2*MB)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else -(G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (5*G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) - (G**2*MB*reglog(MT/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else (G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) ) - (G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_151_106 = Coupling(name = 'UVGC_151_106',
                        value = {-1:'(G**2*MB*cmath.sqrt(2))/(3.*cmath.pi**2*vev)'},
                        order = {'QCD':2,'QED':1})

UVGC_152_107 = Coupling(name = 'UVGC_152_107',
                        value = {-1:'( -(G**2*MB)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else (7*G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (-5*G**2*MB)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) + (3*G**2*MB*reglog(MB/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else -(G**2*MB)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) ) + (G**2*MB)/(4.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_152_108 = Coupling(name = 'UVGC_152_108',
                        value = {-1:'( -(G**2*MB)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else (G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (-5*G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) + (G**2*MB*reglog(MT/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else -(G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) ) + (G**2*MB)/(12.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_152_109 = Coupling(name = 'UVGC_152_109',
                        value = {-1:'-(G**2*MB*cmath.sqrt(2))/(3.*cmath.pi**2*vev)'},
                        order = {'QCD':2,'QED':1})

UVGC_153_110 = Coupling(name = 'UVGC_153_110',
                        value = {-1:'( (G**2*MT)/(6.*cmath.pi**2*vev) if MT else -(G**2*MT)/(3.*cmath.pi**2*vev) ) + (G**2*MT)/(3.*cmath.pi**2*vev)',0:'( (5*G**2*MT)/(6.*cmath.pi**2*vev) - (G**2*MT*reglog(MT/MU_R))/(cmath.pi**2*vev) if MT else (G**2*MT)/(6.*cmath.pi**2*vev) ) - (G**2*MT)/(6.*cmath.pi**2*vev)'},
                        order = {'QCD':2,'QED':1})

UVGC_154_111 = Coupling(name = 'UVGC_154_111',
                        value = {-1:'( (complex(0,1)*G**2*MT)/(6.*cmath.pi**2*vev) if MT else -(complex(0,1)*G**2*MT)/(3.*cmath.pi**2*vev) ) + (complex(0,1)*G**2*MT)/(3.*cmath.pi**2*vev)',0:'( (5*complex(0,1)*G**2*MT)/(6.*cmath.pi**2*vev) - (complex(0,1)*G**2*MT*reglog(MT/MU_R))/(cmath.pi**2*vev) if MT else (complex(0,1)*G**2*MT)/(6.*cmath.pi**2*vev) ) - (complex(0,1)*G**2*MT)/(6.*cmath.pi**2*vev)'},
                        order = {'QCD':2,'QED':1})

UVGC_155_112 = Coupling(name = 'UVGC_155_112',
                        value = {-1:'( (G**2*MT)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else -(G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (5*G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) - (G**2*MT*reglog(MB/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else (G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) ) - (G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_155_113 = Coupling(name = 'UVGC_155_113',
                        value = {-1:'( (G**2*MT)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else (-7*G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (5*G**2*MT)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) - (3*G**2*MT*reglog(MT/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else (G**2*MT)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) ) - (G**2*MT)/(4.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_155_114 = Coupling(name = 'UVGC_155_114',
                        value = {-1:'(G**2*MT*cmath.sqrt(2))/(3.*cmath.pi**2*vev)'},
                        order = {'QCD':2,'QED':1})

UVGC_156_115 = Coupling(name = 'UVGC_156_115',
                        value = {-1:'( -(G**2*MT)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else (G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (-5*G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) + (G**2*MT*reglog(MB/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MB else -(G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) ) + (G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_156_116 = Coupling(name = 'UVGC_156_116',
                        value = {-1:'( -(G**2*MT)/(6.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else (7*G**2*MT)/(12.*cmath.pi**2*vev*cmath.sqrt(2)) )',0:'( (-5*G**2*MT)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) + (3*G**2*MT*reglog(MT/MU_R))/(2.*cmath.pi**2*vev*cmath.sqrt(2)) if MT else -(G**2*MT)/(4.*cmath.pi**2*vev*cmath.sqrt(2)) ) + (G**2*MT)/(4.*cmath.pi**2*vev*cmath.sqrt(2))'},
                        order = {'QCD':2,'QED':1})

UVGC_156_117 = Coupling(name = 'UVGC_156_117',
                        value = {-1:'-(G**2*MT*cmath.sqrt(2))/(3.*cmath.pi**2*vev)'},
                        order = {'QCD':2,'QED':1})

UVGC_80_118 = Coupling(name = 'UVGC_80_118',
                       value = {-1:'(ee*complex(0,1)*G**2)/(36.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_81_119 = Coupling(name = 'UVGC_81_119',
                       value = {-1:'(-13*complex(0,1)*G**3)/(48.*cmath.pi**2)'},
                       order = {'QCD':3})

UVGC_82_120 = Coupling(name = 'UVGC_82_120',
                       value = {-1:'-(ee*complex(0,1)*G**2)/(18.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_84_121 = Coupling(name = 'UVGC_84_121',
                       value = {-1:'-(complex(0,1)*G**2)/(12.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_85_122 = Coupling(name = 'UVGC_85_122',
                       value = {-1:'-(ee*complex(0,1)*G**2)/(36.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_96_123 = Coupling(name = 'UVGC_96_123',
                       value = {-1:'(ee*complex(0,1)*G**2)/(18.*cmath.pi**2)'},
                       order = {'QCD':2,'QED':1})

UVGC_98_124 = Coupling(name = 'UVGC_98_124',
                       value = {-1:'(3*complex(0,1)*G**2)/(64.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_98_125 = Coupling(name = 'UVGC_98_125',
                       value = {-1:'(-3*complex(0,1)*G**2)/(64.*cmath.pi**2)'},
                       order = {'QCD':2})

UVGC_99_126 = Coupling(name = 'UVGC_99_126',
                       value = {-1:'(9*G**3)/(128.*cmath.pi**2)'},
                       order = {'QCD':3})

