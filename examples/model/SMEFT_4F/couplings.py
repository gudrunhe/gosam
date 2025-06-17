from __future__ import absolute_import
# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.1.0 for Linux x86 (64-bit) (July 16, 2024)
# Date: Mon 16 Jun 2025 14:37:51


from .object_library import all_couplings, Coupling

from .function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



GC_1 = Coupling(name = 'GC_1',
                value = 'Cqb1*complex(0,1)',
                order = {'NP':1})

GC_2 = Coupling(name = 'GC_2',
                value = 'Cqb8*complex(0,1)',
                order = {'NP':1})

GC_3 = Coupling(name = 'GC_3',
                value = '-(Cqtqb1*complex(0,1))',
                order = {'NP':1})

GC_4 = Coupling(name = 'GC_4',
                value = 'Cqtqb1*complex(0,1)',
                order = {'NP':1})

GC_5 = Coupling(name = 'GC_5',
                value = '-(Cqtqb8*complex(0,1))',
                order = {'NP':1})

GC_6 = Coupling(name = 'GC_6',
                value = 'Cqtqb8*complex(0,1)',
                order = {'NP':1})

GC_7 = Coupling(name = 'GC_7',
                value = '-0.3333333333333333*(ee*complex(0,1))',
                order = {'QED':1})

GC_8 = Coupling(name = 'GC_8',
                value = '(2*ee*complex(0,1))/3.',
                order = {'QED':1})

GC_9 = Coupling(name = 'GC_9',
                value = '-(ee*complex(0,1))',
                order = {'QED':1})

GC_10 = Coupling(name = 'GC_10',
                 value = 'ee*complex(0,1)',
                 order = {'QED':1})

GC_11 = Coupling(name = 'GC_11',
                 value = 'ee**2*complex(0,1)',
                 order = {'QED':2})

GC_12 = Coupling(name = 'GC_12',
                 value = '2*ee**2*complex(0,1)',
                 order = {'QED':2})

GC_13 = Coupling(name = 'GC_13',
                 value = '-0.5*ee**2/cw',
                 order = {'QED':2})

GC_14 = Coupling(name = 'GC_14',
                 value = '(ee**2*complex(0,1))/(2.*cw)',
                 order = {'QED':2})

GC_15 = Coupling(name = 'GC_15',
                 value = 'ee**2/(2.*cw)',
                 order = {'QED':2})

GC_16 = Coupling(name = 'GC_16',
                 value = '-G',
                 order = {'QCD':1})

GC_17 = Coupling(name = 'GC_17',
                 value = 'complex(0,1)*G',
                 order = {'QCD':1})

GC_18 = Coupling(name = 'GC_18',
                 value = 'complex(0,1)*G**2',
                 order = {'QCD':2})

GC_19 = Coupling(name = 'GC_19',
                 value = '-2*complex(0,1)*lam',
                 order = {'QED':2})

GC_20 = Coupling(name = 'GC_20',
                 value = '-4*complex(0,1)*lam',
                 order = {'QED':2})

GC_21 = Coupling(name = 'GC_21',
                 value = '-6*complex(0,1)*lam',
                 order = {'QED':2})

GC_22 = Coupling(name = 'GC_22',
                 value = '(ee**2*complex(0,1))/(2.*sw**2)',
                 order = {'QED':2})

GC_23 = Coupling(name = 'GC_23',
                 value = '-((ee**2*complex(0,1))/sw**2)',
                 order = {'QED':2})

GC_24 = Coupling(name = 'GC_24',
                 value = '(cw**2*ee**2*complex(0,1))/sw**2',
                 order = {'QED':2})

GC_25 = Coupling(name = 'GC_25',
                 value = '-0.5*ee/sw',
                 order = {'QED':1})

GC_26 = Coupling(name = 'GC_26',
                 value = '-0.5*(ee*complex(0,1))/sw',
                 order = {'QED':1})

GC_27 = Coupling(name = 'GC_27',
                 value = '(ee*complex(0,1))/(2.*sw)',
                 order = {'QED':1})

GC_28 = Coupling(name = 'GC_28',
                 value = '(ee*complex(0,1))/(sw*cmath.sqrt(2))',
                 order = {'QED':1})

GC_29 = Coupling(name = 'GC_29',
                 value = '-0.5*(cw*ee*complex(0,1))/sw',
                 order = {'QED':1})

GC_30 = Coupling(name = 'GC_30',
                 value = '-((cw*ee*complex(0,1))/sw)',
                 order = {'QED':1})

GC_31 = Coupling(name = 'GC_31',
                 value = '(cw*ee*complex(0,1))/sw',
                 order = {'QED':1})

GC_32 = Coupling(name = 'GC_32',
                 value = '-0.5*ee**2/sw',
                 order = {'QED':2})

GC_33 = Coupling(name = 'GC_33',
                 value = '-0.5*(ee**2*complex(0,1))/sw',
                 order = {'QED':2})

GC_34 = Coupling(name = 'GC_34',
                 value = 'ee**2/(2.*sw)',
                 order = {'QED':2})

GC_35 = Coupling(name = 'GC_35',
                 value = '(-2*cw*ee**2*complex(0,1))/sw',
                 order = {'QED':2})

GC_36 = Coupling(name = 'GC_36',
                 value = '(ee*complex(0,1)*sw)/(3.*cw)',
                 order = {'QED':1})

GC_37 = Coupling(name = 'GC_37',
                 value = '(ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})

GC_38 = Coupling(name = 'GC_38',
                 value = '(-2*ee*complex(0,1)*sw)/(3.*cw)',
                 order = {'QED':1})

GC_39 = Coupling(name = 'GC_39',
                 value = '-0.5*(cw*ee)/sw - (ee*sw)/(2.*cw)',
                 order = {'QED':1})

GC_40 = Coupling(name = 'GC_40',
                 value = '-0.5*(cw*ee*complex(0,1))/sw - (ee*complex(0,1)*sw)/(6.*cw)',
                 order = {'QED':1})

GC_41 = Coupling(name = 'GC_41',
                 value = '(cw*ee*complex(0,1))/(2.*sw) - (ee*complex(0,1)*sw)/(6.*cw)',
                 order = {'QED':1})

GC_42 = Coupling(name = 'GC_42',
                 value = '-0.5*(cw*ee*complex(0,1))/sw + (ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})

GC_43 = Coupling(name = 'GC_43',
                 value = '(cw*ee*complex(0,1))/(2.*sw) + (ee*complex(0,1)*sw)/(2.*cw)',
                 order = {'QED':1})

GC_44 = Coupling(name = 'GC_44',
                 value = '(cw*ee**2*complex(0,1))/sw - (ee**2*complex(0,1)*sw)/cw',
                 order = {'QED':2})

GC_45 = Coupling(name = 'GC_45',
                 value = '-(ee**2*complex(0,1)) + (cw**2*ee**2*complex(0,1))/(2.*sw**2) + (ee**2*complex(0,1)*sw**2)/(2.*cw**2)',
                 order = {'QED':2})

GC_46 = Coupling(name = 'GC_46',
                 value = 'ee**2*complex(0,1) + (cw**2*ee**2*complex(0,1))/(2.*sw**2) + (ee**2*complex(0,1)*sw**2)/(2.*cw**2)',
                 order = {'QED':2})

GC_47 = Coupling(name = 'GC_47',
                 value = '-0.5*(ee**2*vev)/cw',
                 order = {'QED':1})

GC_48 = Coupling(name = 'GC_48',
                 value = '(ee**2*vev)/(2.*cw)',
                 order = {'QED':1})

GC_49 = Coupling(name = 'GC_49',
                 value = '-2*complex(0,1)*lam*vev',
                 order = {'QED':1})

GC_50 = Coupling(name = 'GC_50',
                 value = '-6*complex(0,1)*lam*vev',
                 order = {'QED':1})

GC_51 = Coupling(name = 'GC_51',
                 value = '-0.25*(ee**2*vev)/sw**2',
                 order = {'QED':1})

GC_52 = Coupling(name = 'GC_52',
                 value = '-0.25*(ee**2*complex(0,1)*vev)/sw**2',
                 order = {'QED':1})

GC_53 = Coupling(name = 'GC_53',
                 value = '(ee**2*complex(0,1)*vev)/(2.*sw**2)',
                 order = {'QED':1})

GC_54 = Coupling(name = 'GC_54',
                 value = '(ee**2*vev)/(4.*sw**2)',
                 order = {'QED':1})

GC_55 = Coupling(name = 'GC_55',
                 value = '-0.5*(ee**2*vev)/sw',
                 order = {'QED':1})

GC_56 = Coupling(name = 'GC_56',
                 value = '(ee**2*vev)/(2.*sw)',
                 order = {'QED':1})

GC_57 = Coupling(name = 'GC_57',
                 value = '-0.25*(ee**2*vev)/cw - (cw*ee**2*vev)/(4.*sw**2)',
                 order = {'QED':1})

GC_58 = Coupling(name = 'GC_58',
                 value = '(ee**2*vev)/(4.*cw) - (cw*ee**2*vev)/(4.*sw**2)',
                 order = {'QED':1})

GC_59 = Coupling(name = 'GC_59',
                 value = '-0.25*(ee**2*vev)/cw + (cw*ee**2*vev)/(4.*sw**2)',
                 order = {'QED':1})

GC_60 = Coupling(name = 'GC_60',
                 value = '(ee**2*vev)/(4.*cw) + (cw*ee**2*vev)/(4.*sw**2)',
                 order = {'QED':1})

GC_61 = Coupling(name = 'GC_61',
                 value = '-0.5*(ee**2*complex(0,1)*vev) - (cw**2*ee**2*complex(0,1)*vev)/(4.*sw**2) - (ee**2*complex(0,1)*sw**2*vev)/(4.*cw**2)',
                 order = {'QED':1})

GC_62 = Coupling(name = 'GC_62',
                 value = 'ee**2*complex(0,1)*vev + (cw**2*ee**2*complex(0,1)*vev)/(2.*sw**2) + (ee**2*complex(0,1)*sw**2*vev)/(2.*cw**2)',
                 order = {'QED':1})

GC_63 = Coupling(name = 'GC_63',
                 value = '-yb',
                 order = {'QED':1})

GC_64 = Coupling(name = 'GC_64',
                 value = 'yb',
                 order = {'QED':1})

GC_65 = Coupling(name = 'GC_65',
                 value = '-(yb/cmath.sqrt(2))',
                 order = {'QED':1})

GC_66 = Coupling(name = 'GC_66',
                 value = '-((complex(0,1)*yb)/cmath.sqrt(2))',
                 order = {'QED':1})

GC_67 = Coupling(name = 'GC_67',
                 value = '-yt',
                 order = {'QED':1})

GC_68 = Coupling(name = 'GC_68',
                 value = 'yt',
                 order = {'QED':1})

GC_69 = Coupling(name = 'GC_69',
                 value = '-(yt/cmath.sqrt(2))',
                 order = {'QED':1})

GC_70 = Coupling(name = 'GC_70',
                 value = '-((complex(0,1)*yt)/cmath.sqrt(2))',
                 order = {'QED':1})

GC_71 = Coupling(name = 'GC_71',
                 value = 'yt/cmath.sqrt(2)',
                 order = {'QED':1})

GC_72 = Coupling(name = 'GC_72',
                 value = '-ytau',
                 order = {'QED':1})

GC_73 = Coupling(name = 'GC_73',
                 value = 'ytau',
                 order = {'QED':1})

GC_74 = Coupling(name = 'GC_74',
                 value = '-(ytau/cmath.sqrt(2))',
                 order = {'QED':1})

GC_75 = Coupling(name = 'GC_75',
                 value = '-((complex(0,1)*ytau)/cmath.sqrt(2))',
                 order = {'QED':1})

GC_76 = Coupling(name = 'GC_76',
                 value = 'ytau/cmath.sqrt(2)',
                 order = {'QED':1})

