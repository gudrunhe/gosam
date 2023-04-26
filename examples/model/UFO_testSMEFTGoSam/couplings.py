# This file was automatically created by FeynRules 2.3.47
# Mathematica version: 12.1.1 for Linux x86 (64-bit) (June 19, 2020)
# Date: Mon 20 Feb 2023 15:47:51


from .object_library import all_couplings, Coupling

from .function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



GC_1 = Coupling(name = 'GC_1',
                value = '(CtG*complex(0,1))/cmath.sqrt(2)',
                order = {'NP':2,'QCD':1,'QED':2,'QL':1,'QQ':3})

GC_2 = Coupling(name = 'GC_2',
                value = '-(ee*complex(0,1))/3.',
                order = {'QED':1})

GC_3 = Coupling(name = 'GC_3',
                value = '(2*ee*complex(0,1))/3.',
                order = {'QED':1})

GC_4 = Coupling(name = 'GC_4',
                value = '-(ee*complex(0,1))',
                order = {'QED':1})

GC_5 = Coupling(name = 'GC_5',
                value = 'ee*complex(0,1)',
                order = {'QED':1})

GC_6 = Coupling(name = 'GC_6',
                value = 'ee**2*complex(0,1)',
                order = {'QED':2})

GC_7 = Coupling(name = 'GC_7',
                value = '-G',
                order = {'QCD':1,'QQ':1})

GC_8 = Coupling(name = 'GC_8',
                value = 'complex(0,1)*G',
                order = {'QCD':1,'QQ':1})

GC_9 = Coupling(name = 'GC_9',
                value = '-((CtG*G)/cmath.sqrt(2))',
                order = {'NP':2,'QCD':2,'QED':2,'QL':1,'QQ':4})

GC_10 = Coupling(name = 'GC_10',
                 value = 'complex(0,1)*G**2',
                 order = {'QCD':2,'QQ':2})

GC_11 = Coupling(name = 'GC_11',
                 value = '-24*complex(0,1)*normh4',
                 order = {'QED':2,'QQ':2})

GC_12 = Coupling(name = 'GC_12',
                 value = '-24*chhhh*complex(0,1)*normh4',
                 order = {'NP':2,'QED':2,'QQ':2})

GC_13 = Coupling(name = 'GC_13',
                 value = '-((ee**2*complex(0,1))/sw**2)',
                 order = {'QED':2})

GC_14 = Coupling(name = 'GC_14',
                 value = '(cw**2*ee**2*complex(0,1))/sw**2',
                 order = {'QED':2})

GC_15 = Coupling(name = 'GC_15',
                 value = '(ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_16 = Coupling(name = 'GC_16',
                 value = '-(cw*ee*complex(0,1))/(2.*sw)',
                 order = {'QED':1})

GC_17 = Coupling(name = 'GC_17',
                 value = '(cw*ee*complex(0,1))/(2.*sw)',
                 order = {'QED':1})

GC_18 = Coupling(name = 'GC_18',
                 value = '(cw*ee*complex(0,1))/sw',
                 order = {'QED':1})

GC_19 = Coupling(name = 'GC_19',
                 value = '(-2*cw*ee**2*complex(0,1))/sw',
                 order = {'QED':2})

GC_20 = Coupling(name = 'GC_20',
                 value = '-(ee*complex(0,1)*sw)/(6.*cw)',
                 order = {'QED':1})

GC_21 = Coupling(name = 'GC_21',
                 value = '(ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})

GC_22 = Coupling(name = 'GC_22',
                 value = '(cw*ee*complex(0,1))/(2.*sw) + (ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})

GC_23 = Coupling(name = 'GC_23',
                 value = '(4*cgghh*complex(0,1)*G**2)/(loop*v**2)',
                 order = {'NP':2,'QCD':2,'QED':2,'QL':1,'QQ':4})

GC_24 = Coupling(name = 'GC_24',
                 value = '(4*cgghh*G**3)/(loop*v**2)',
                 order = {'NP':2,'QCD':3,'QED':2,'QL':1,'QQ':5})

GC_25 = Coupling(name = 'GC_25',
                 value = '(-4*cgghh*complex(0,1)*G**4)/(loop*v**2)',
                 order = {'NP':2,'QCD':4,'QED':2,'QL':1,'QQ':6})

GC_26 = Coupling(name = 'GC_26',
                 value = '(2*cgg*complex(0,1)*G**2)/(loop*v)',
                 order = {'NP':2,'QCD':2,'QED':1,'QL':1,'QQ':3})

GC_27 = Coupling(name = 'GC_27',
                 value = '(2*cgg*G**3)/(loop*v)',
                 order = {'NP':2,'QCD':3,'QED':1,'QL':1,'QQ':4})

GC_28 = Coupling(name = 'GC_28',
                 value = '(-2*cgg*complex(0,1)*G**4)/(loop*v)',
                 order = {'NP':2,'QCD':4,'QED':1,'QL':1,'QQ':5})

GC_29 = Coupling(name = 'GC_29',
                 value = '(4*cV*complex(0,1)*MW**2)/v',
                 order = {'NP':2,'QED':1,'QQ':1})

GC_30 = Coupling(name = 'GC_30',
                 value = '(4*cV*complex(0,1)*MZ**2)/v',
                 order = {'NP':2,'QED':1,'QQ':1})

GC_31 = Coupling(name = 'GC_31',
                 value = '(CtG*complex(0,1)*v)/cmath.sqrt(2)',
                 order = {'NP':2,'QCD':1,'QED':1,'QL':1,'QQ':2})

GC_32 = Coupling(name = 'GC_32',
                 value = '-((CtG*G*v)/cmath.sqrt(2))',
                 order = {'NP':2,'QCD':2,'QED':1,'QL':1,'QQ':3})

GC_33 = Coupling(name = 'GC_33',
                 value = '-6*complex(0,1)*normh3*v',
                 order = {'QED':1,'QQ':1})

GC_34 = Coupling(name = 'GC_34',
                 value = '-6*chhh*complex(0,1)*normh3*v',
                 order = {'NP':2,'QED':1,'QQ':1})

GC_35 = Coupling(name = 'GC_35',
                 value = '-(complex(0,1)*yyt)',
                 order = {'QED':1,'QQ':1})

GC_36 = Coupling(name = 'GC_36',
                 value = '-(ct*complex(0,1)*yyt)',
                 order = {'NP':2,'QED':1,'QQ':1})

GC_37 = Coupling(name = 'GC_37',
                 value = '(-2*cthh*complex(0,1)*yyt)/v',
                 order = {'NP':2,'QED':2,'QQ':2})

