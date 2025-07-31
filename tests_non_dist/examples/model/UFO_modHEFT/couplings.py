# This file was automatically created by FeynRules 2.3.32
# Mathematica version: 8.0 for Linux x86 (64-bit) (October 10, 2011)
# Date: Wed 7 Jul 2021 13:14:47


from .object_library import all_couplings, Coupling

from .function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



GC_1 = Coupling(name = 'GC_1',
                value = '-(ee*complex(0,1))/3.',
                order = {'QED':1})

GC_2 = Coupling(name = 'GC_2',
                value = '(2*ee*complex(0,1))/3.',
                order = {'QED':1})

GC_3 = Coupling(name = 'GC_3',
                value = '-(ee*complex(0,1))',
                order = {'QED':1})

GC_4 = Coupling(name = 'GC_4',
                value = 'ee*complex(0,1)',
                order = {'QED':1})

GC_5 = Coupling(name = 'GC_5',
                value = 'ee**2*complex(0,1)',
                order = {'QED':2})

GC_6 = Coupling(name = 'GC_6',
                value = '-G',
                order = {'QCD':1,'QQ':1})

GC_7 = Coupling(name = 'GC_7',
                value = 'complex(0,1)*G',
                order = {'QCD':1,'QQ':1})

GC_8 = Coupling(name = 'GC_8',
                value = 'complex(0,1)*G**2',
                order = {'QCD':2,'QQ':2})



GC_9 = Coupling(name = 'GC_9',
                value = 'GC9SM + GC9DIM6*Lambdam2',
                order = {'QED':2,'QQ':2})

GC9SM = Coupling(name = 'GC9SM',
                value = '-24*complex(0,1)*normh4',
                order = {'QED':2,'QQ':2})

GC9DIM6 = Coupling(name = 'GC9DIM6',
                value = '- 24*chhhh*complex(0,1)*normh4',
                order = {'QED':2,'QQ':2})



GC_10 = Coupling(name = 'GC_10',
                 value = '-((ee**2*complex(0,1))/sw**2)',
                 order = {'QED':2})

GC_11 = Coupling(name = 'GC_11',
                 value = '(cw**2*ee**2*complex(0,1))/sw**2',
                 order = {'QED':2})

GC_12 = Coupling(name = 'GC_12',
                 value = '(ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_13 = Coupling(name = 'GC_13',
                 value = '(CKM1x1*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_14 = Coupling(name = 'GC_14',
                 value = '(CKM1x2*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_15 = Coupling(name = 'GC_15',
                 value = '(CKM1x3*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_16 = Coupling(name = 'GC_16',
                 value = '(CKM2x1*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_17 = Coupling(name = 'GC_17',
                 value = '(CKM2x2*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_18 = Coupling(name = 'GC_18',
                 value = '(CKM2x3*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_19 = Coupling(name = 'GC_19',
                 value = '(CKM3x1*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_20 = Coupling(name = 'GC_20',
                 value = '(CKM3x2*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_21 = Coupling(name = 'GC_21',
                 value = '(CKM3x3*ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_22 = Coupling(name = 'GC_22',
                 value = '(cw*ee*complex(0,1))/sw',
                 order = {'QED':1})

GC_23 = Coupling(name = 'GC_23',
                 value = '(-2*cw*ee**2*complex(0,1))/sw',
                 order = {'QED':2})

GC_24 = Coupling(name = 'GC_24',
                 value = '(ee*complex(0,1)*sw)/(3.*cw)',
                 order = {'QED':1})

GC_25 = Coupling(name = 'GC_25',
                 value = '(-2*ee*complex(0,1)*sw)/(3.*cw)',
                 order = {'QED':1})

GC_26 = Coupling(name = 'GC_26',
                 value = '(ee*complex(0,1)*sw)/cw',
                 order = {'QED':1})

GC_27 = Coupling(name = 'GC_27',
                 value = '-(cw*ee*complex(0,1))/(2.*sw) - (ee*complex(0,1)*sw)/(6.*cw)',
                 order = {'QED':1})

GC_28 = Coupling(name = 'GC_28',
                 value = '(cw*ee*complex(0,1))/(2.*sw) - (ee*complex(0,1)*sw)/(6.*cw)',
                 order = {'QED':1})

GC_29 = Coupling(name = 'GC_29',
                 value = '-(cw*ee*complex(0,1))/(2.*sw) + (ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})

GC_30 = Coupling(name = 'GC_30',
                 value = '(cw*ee*complex(0,1))/(2.*sw) + (ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})



GC_31 = Coupling(name = 'GC_31',
                 value = 'GC31DIM6*Lambdam2',
                 order = {'QCD':2,'QED':2,'QL':1,'QQ':4})

GC31DIM6 = Coupling(name = 'GC31DIM6',
                 value = '(4*cgghh*complex(0,1)*G**2)/(loop*v**2)',
                 order = {'QCD':2,'QED':2,'QL':1,'QQ':4})

GC_32 = Coupling(name = 'GC_32',
                 value = 'GC32DIM6*Lambdam2',
                 order = {'QCD':3,'QED':2,'QL':1,'QQ':5})

GC32DIM6 = Coupling(name = 'GC32DIM6',
                 value = '(4*cgghh*G**3)/(loop*v**2)',
                 order = {'QCD':3,'QED':2,'QL':1,'QQ':5})

GC_33 = Coupling(name = 'GC_33',
                 value = 'GC33DIM6*Lambdam2',
                 order = {'QCD':4,'QED':2,'QL':1,'QQ':6})

GC33DIM6 = Coupling(name = 'GC33DIM6',
                 value = '(-4*cgghh*complex(0,1)*G**4)/(loop*v**2)',
                 order = {'QCD':4,'QED':2,'QL':1,'QQ':6})

GC_34 = Coupling(name = 'GC_34',
                 value = 'GC34DIM6*Lambdam2',
                 order = {'QCD':2,'QED':1,'QL':1,'QQ':3})

GC34DIM6 = Coupling(name = 'GC34DIM6',
                 value = '(2*cgg*complex(0,1)*G**2)/(loop*v)',
                 order = {'QCD':2,'QED':1,'QL':1,'QQ':3})

GC_35 = Coupling(name = 'GC_35',
                 value = 'GC35DIM6*Lambdam2',
                 order = {'QCD':3,'QED':1,'QL':1,'QQ':4})

GC35DIM6 = Coupling(name = 'GC35DIM6',
                 value = '(2*cgg*G**3)/(loop*v)',
                 order = {'QCD':3,'QED':1,'QL':1,'QQ':4})

GC_36 = Coupling(name = 'GC_36',
                 value = 'GC36DIM6*Lambdam2',
                 order = {'QCD':4,'QED':1,'QL':1,'QQ':5})

GC36DIM6 = Coupling(name = 'GC36DIM6',
                 value = '(-2*cgg*complex(0,1)*G**4)/(loop*v)',
                 order = {'QCD':4,'QED':1,'QL':1,'QQ':5})



GC_37 = Coupling(name = 'GC_37',
                 value = '(2*cV*complex(0,1)*MW**2)/v',
                 order = {'QED':1,'QQ':1})

GC_38 = Coupling(name = 'GC_38',
                 value = '(2*cV*complex(0,1)*MZ**2)/v',
                 order = {'QED':1,'QQ':1})



GC_39 = Coupling(name = 'GC_39',
                 value = 'GC39SM + GC39DIM6*Lambdam2',
                 order = {'QED':1,'QQ':1})

GC39SM = Coupling(name = 'GC39SM',
                 value = '-6*complex(0,1)*normh3*v',
                 order = {'QED':1,'QQ':1})

GC39DIM6 = Coupling(name = 'GC39DIM6',
                 value = '- 6*chhh*complex(0,1)*normh3*v',
                 order = {'QED':1,'QQ':1})

GC_40 = Coupling(name = 'GC_40',
                 value = 'GC40DIM6*Lambdam2',
                 order = {'QED':2,'QQ':2})

GC40DIM6 = Coupling(name = 'GC40DIM6',
                 value = '(-2*cthh*complex(0,1)*yyt)/v',
                 order = {'QED':2,'QQ':2})

GC_41 = Coupling(name = 'GC_41',
                 value = 'GC41SM + GC41DIM6*Lambdam2',
                 order = {'QED':1,'QQ':1})

GC41SM = Coupling(name = 'GC41SM',
                 value = '-(complex(0,1)*yyt)',
                 order = {'QED':1,'QQ':1})

GC41DIM6 = Coupling(name = 'GC41DIM6',
                 value = '- ct*complex(0,1)*yyt',
                 order = {'QED':1,'QQ':1})



GC_42 = Coupling(name = 'GC_42',
                 value = '(ee*complex(0,1)*complexconjugate(CKM1x1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_43 = Coupling(name = 'GC_43',
                 value = '(ee*complex(0,1)*complexconjugate(CKM1x2))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_44 = Coupling(name = 'GC_44',
                 value = '(ee*complex(0,1)*complexconjugate(CKM1x3))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_45 = Coupling(name = 'GC_45',
                 value = '(ee*complex(0,1)*complexconjugate(CKM2x1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_46 = Coupling(name = 'GC_46',
                 value = '(ee*complex(0,1)*complexconjugate(CKM2x2))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_47 = Coupling(name = 'GC_47',
                 value = '(ee*complex(0,1)*complexconjugate(CKM2x3))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_48 = Coupling(name = 'GC_48',
                 value = '(ee*complex(0,1)*complexconjugate(CKM3x1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_49 = Coupling(name = 'GC_49',
                 value = '(ee*complex(0,1)*complexconjugate(CKM3x2))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_50 = Coupling(name = 'GC_50',
                 value = '(ee*complex(0,1)*complexconjugate(CKM3x3))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})
