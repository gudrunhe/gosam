# This file was automatically created from UFO model SMEFTsim_U35_MwScheme_UFO
# by applying the 'modify_UFO.py' script. Only SM vertices and those containing
# one of the following coefficients have been kept:
# cHW  cHB  cHWB 


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot


GC_1 = Coupling(name = 'GC_1',
	value = '(ee*complex(0,1))/3.',
	order = {'QED': 1})

GC_2 = Coupling(name = 'GC_2',
	value = '(-2*ee*complex(0,1))/3.',
	order = {'QED': 1})

GC_3 = Coupling(name = 'GC_3',
	value = '-(ee*complex(0,1))',
	order = {'QED': 1})

GC_4 = Coupling(name = 'GC_4',
	value = 'ee*complex(0,1)',
	order = {'QED': 1})

GC_5 = Coupling(name = 'GC_5',
	value = 'ee**2*complex(0,1)',
	order = {'QED': 2})

GC_6 = Coupling(name = 'GC_6',
	value = '-(complex(0,1)*G)',
	order = {'QCD': 1})

GC_7 = Coupling(name = 'GC_7',
	value = 'G',
	order = {'QCD': 1})

GC_8 = Coupling(name = 'GC_8',
	value = 'complex(0,1)*G**2',
	order = {'QCD': 2})

GC_9 = Coupling(name = 'GC_9',
	value = '-6*complex(0,1)*lam',
	order = {'QED': 2})

GC_22 = Coupling(name = 'GC_22',
	value = '(4*cHW*complex(0,1))/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_52 = Coupling(name = 'GC_52',
	value = '(4*cHB*cth**2*complex(0,1))/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_54 = Coupling(name = 'GC_54',
	value = '(4*cHW*cth**2*complex(0,1))/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_62 = Coupling(name = 'GC_62',
	value = '(4*cHW*ee*complex(0,1))/LambdaSMEFT**2',
	order = {'QED': 3, 'NP': 1})

GC_63 = Coupling(name = 'GC_63',
	value = '(2*cHWB*ee*complex(0,1))/LambdaSMEFT**2',
	order = {'QED': 3, 'NP': 1})

GC_68 = Coupling(name = 'GC_68',
	value = '(-4*cHW*ee**2*complex(0,1))/LambdaSMEFT**2',
	order = {'QED': 4, 'NP': 1})

GC_97 = Coupling(name = 'GC_97',
	value = '(ee**2*complex(0,1))/(2.*sth**2)',
	order = {'QED': 2})

GC_98 = Coupling(name = 'GC_98',
	value = '-((ee**2*complex(0,1))/sth**2)',
	order = {'QED': 2})

GC_99 = Coupling(name = 'GC_99',
	value = '(ee**2*complex(0,1))/(2.*cth**2*sth**2)',
	order = {'QED': 2})

GC_100 = Coupling(name = 'GC_100',
	value = '(cth**2*ee**2*complex(0,1))/sth**2',
	order = {'QED': 2})

GC_101 = Coupling(name = 'GC_101',
	value = '(4*cHW*ee**2*complex(0,1))/(LambdaSMEFT**2*sth**2)',
	order = {'QED': 4, 'NP': 1})

GC_103 = Coupling(name = 'GC_103',
	value = '(-4*cHW*cth**2*ee**2*complex(0,1))/(LambdaSMEFT**2*sth**2)',
	order = {'QED': 4, 'NP': 1})

GC_125 = Coupling(name = 'GC_125',
	value = '-((ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_126 = Coupling(name = 'GC_126',
	value = '-((CKM1x1*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_127 = Coupling(name = 'GC_127',
	value = '-((CKM1x2*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_128 = Coupling(name = 'GC_128',
	value = '-((CKM1x3*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_129 = Coupling(name = 'GC_129',
	value = '-((CKM2x1*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_130 = Coupling(name = 'GC_130',
	value = '-((CKM2x2*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_131 = Coupling(name = 'GC_131',
	value = '-((CKM2x3*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_132 = Coupling(name = 'GC_132',
	value = '-((CKM3x1*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_133 = Coupling(name = 'GC_133',
	value = '-((CKM3x2*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_134 = Coupling(name = 'GC_134',
	value = '-((CKM3x3*ee*complex(0,1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_135 = Coupling(name = 'GC_135',
	value = '-(ee*complex(0,1))/(2.*cth*sth)',
	order = {'QED': 1})

GC_136 = Coupling(name = 'GC_136',
	value = '(ee*complex(0,1))/(2.*cth*sth)',
	order = {'QED': 1})

GC_137 = Coupling(name = 'GC_137',
	value = '-((cth*ee*complex(0,1))/sth)',
	order = {'QED': 1})

GC_138 = Coupling(name = 'GC_138',
	value = '(-2*cth*ee**2*complex(0,1))/sth',
	order = {'QED': 2})

GC_158 = Coupling(name = 'GC_158',
	value = '(4*cHW*cth*ee*complex(0,1))/(LambdaSMEFT**2*sth)',
	order = {'QED': 3, 'NP': 1})

GC_159 = Coupling(name = 'GC_159',
	value = '(-2*cHWB*cth*ee*complex(0,1))/(LambdaSMEFT**2*sth)',
	order = {'QED': 3, 'NP': 1})

GC_166 = Coupling(name = 'GC_166',
	value = '(8*cHW*cth*ee**2*complex(0,1))/(LambdaSMEFT**2*sth)',
	order = {'QED': 4, 'NP': 1})

GC_195 = Coupling(name = 'GC_195',
	value = '-(ee*complex(0,1)*sth)/(3.*cth)',
	order = {'QED': 1})

GC_196 = Coupling(name = 'GC_196',
	value = '(2*ee*complex(0,1)*sth)/(3.*cth)',
	order = {'QED': 1})

GC_197 = Coupling(name = 'GC_197',
	value = '-((ee*complex(0,1)*sth)/cth)',
	order = {'QED': 1})

GC_198 = Coupling(name = 'GC_198',
	value = '(-4*cHB*cth*complex(0,1)*sth)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_200 = Coupling(name = 'GC_200',
	value = '(4*cHW*cth*complex(0,1)*sth)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_201 = Coupling(name = 'GC_201',
	value = '(-4*cHWB*cth*complex(0,1)*sth)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_202 = Coupling(name = 'GC_202',
	value = '(4*cHWB*cth*complex(0,1)*sth)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_217 = Coupling(name = 'GC_217',
	value = '(4*cHB*complex(0,1)*sth**2)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_219 = Coupling(name = 'GC_219',
	value = '(4*cHW*complex(0,1)*sth**2)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_221 = Coupling(name = 'GC_221',
	value = '(-2*cHWB*complex(0,1))/LambdaSMEFT**2 + (4*cHWB*complex(0,1)*sth**2)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_260 = Coupling(name = 'GC_260',
	value = '-6*complex(0,1)*lam*vevhat',
	order = {'QED': 1})

GC_266 = Coupling(name = 'GC_266',
	value = '(4*cHW*complex(0,1)*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_268 = Coupling(name = 'GC_268',
	value = '(4*cHB*cth**2*complex(0,1)*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_270 = Coupling(name = 'GC_270',
	value = '(4*cHW*cth**2*complex(0,1)*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_272 = Coupling(name = 'GC_272',
	value = '(4*cHW*ee*complex(0,1)*vevhat)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_273 = Coupling(name = 'GC_273',
	value = '(2*cHWB*ee*complex(0,1)*vevhat)/LambdaSMEFT**2',
	order = {'QED': 2, 'NP': 1})

GC_276 = Coupling(name = 'GC_276',
	value = '(-4*cHW*ee**2*complex(0,1)*vevhat)/LambdaSMEFT**2',
	order = {'QED': 3, 'NP': 1})

GC_283 = Coupling(name = 'GC_283',
	value = '(ee**2*complex(0,1)*vevhat)/(2.*sth**2)',
	order = {'QED': 1})

GC_284 = Coupling(name = 'GC_284',
	value = '(ee**2*complex(0,1)*vevhat)/(2.*cth**2*sth**2)',
	order = {'QED': 1})

GC_285 = Coupling(name = 'GC_285',
	value = '(4*cHW*ee**2*complex(0,1)*vevhat)/(LambdaSMEFT**2*sth**2)',
	order = {'QED': 3, 'NP': 1})

GC_287 = Coupling(name = 'GC_287',
	value = '(-4*cHW*cth**2*ee**2*complex(0,1)*vevhat)/(LambdaSMEFT**2*sth**2)',
	order = {'QED': 3, 'NP': 1})

GC_313 = Coupling(name = 'GC_313',
	value = '(4*cHW*cth*ee*complex(0,1)*vevhat)/(LambdaSMEFT**2*sth)',
	order = {'QED': 2, 'NP': 1})

GC_314 = Coupling(name = 'GC_314',
	value = '(-2*cHWB*cth*ee*complex(0,1)*vevhat)/(LambdaSMEFT**2*sth)',
	order = {'QED': 2, 'NP': 1})

GC_317 = Coupling(name = 'GC_317',
	value = '(8*cHW*cth*ee**2*complex(0,1)*vevhat)/(LambdaSMEFT**2*sth)',
	order = {'QED': 3, 'NP': 1})

GC_318 = Coupling(name = 'GC_318',
	value = '(-4*cHB*cth*complex(0,1)*sth*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_320 = Coupling(name = 'GC_320',
	value = '(4*cHW*cth*complex(0,1)*sth*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_321 = Coupling(name = 'GC_321',
	value = '(-4*cHWB*cth*complex(0,1)*sth*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_322 = Coupling(name = 'GC_322',
	value = '(4*cHWB*cth*complex(0,1)*sth*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_326 = Coupling(name = 'GC_326',
	value = '(4*cHB*complex(0,1)*sth**2*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_328 = Coupling(name = 'GC_328',
	value = '(4*cHW*complex(0,1)*sth**2*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_335 = Coupling(name = 'GC_335',
	value = '(cHWB*ee*complex(0,1)*vevhat**2)/(3.*LambdaSMEFT**2)',
	order = {'QED': 1, 'NP': 1})

GC_336 = Coupling(name = 'GC_336',
	value = '(-2*cHWB*ee*complex(0,1)*vevhat**2)/(3.*LambdaSMEFT**2)',
	order = {'QED': 1, 'NP': 1})

GC_337 = Coupling(name = 'GC_337',
	value = '-((cHWB*ee*complex(0,1)*vevhat**2)/LambdaSMEFT**2)',
	order = {'QED': 1, 'NP': 1})

GC_338 = Coupling(name = 'GC_338',
	value = '(cHWB*ee*complex(0,1)*vevhat**2)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_415 = Coupling(name = 'GC_415',
	value = '-(cHWB*cth*ee*complex(0,1)*vevhat**2)/(3.*LambdaSMEFT**2*sth)',
	order = {'QED': 1, 'NP': 1})

GC_416 = Coupling(name = 'GC_416',
	value = '(2*cHWB*cth*ee*complex(0,1)*vevhat**2)/(3.*LambdaSMEFT**2*sth)',
	order = {'QED': 1, 'NP': 1})

GC_417 = Coupling(name = 'GC_417',
	value = '-((cHWB*cth*ee*complex(0,1)*vevhat**2)/(LambdaSMEFT**2*sth))',
	order = {'QED': 1, 'NP': 1})

GC_422 = Coupling(name = 'GC_422',
	value = '(-2*cHWB*cth*ee**2*complex(0,1)*vevhat**2)/(LambdaSMEFT**2*sth)',
	order = {'QED': 2, 'NP': 1})

GC_423 = Coupling(name = 'GC_423',
	value = '(2*cHWB*cth*ee**2*complex(0,1)*vevhat**2)/(LambdaSMEFT**2*sth)',
	order = {'QED': 2, 'NP': 1})

GC_447 = Coupling(name = 'GC_447',
	value = '(-2*cHWB*complex(0,1)*vevhat)/LambdaSMEFT**2 + (4*cHWB*complex(0,1)*sth**2*vevhat)/LambdaSMEFT**2',
	order = {'QED': 1, 'NP': 1})

GC_449 = Coupling(name = 'GC_449',
	value = '(-4*cHWB*ee**2*complex(0,1)*vevhat**2)/LambdaSMEFT**2 + (2*cHWB*ee**2*complex(0,1)*vevhat**2)/(LambdaSMEFT**2*sth**2)',
	order = {'QED': 2, 'NP': 1})

GC_451 = Coupling(name = 'GC_451',
	value = '-((complex(0,1)*yb)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_509 = Coupling(name = 'GC_509',
	value = '-((complex(0,1)*yc)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_585 = Coupling(name = 'GC_585',
	value = '-((complex(0,1)*ydo)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_661 = Coupling(name = 'GC_661',
	value = '-((complex(0,1)*ye)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_756 = Coupling(name = 'GC_756',
	value = '-((complex(0,1)*ym)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_851 = Coupling(name = 'GC_851',
	value = '-((complex(0,1)*ys)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_945 = Coupling(name = 'GC_945',
	value = '-((complex(0,1)*yt)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_1113 = Coupling(name = 'GC_1113',
	value = '-((complex(0,1)*ytau)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_1244 = Coupling(name = 'GC_1244',
	value = '-((complex(0,1)*yup)/cmath.sqrt(2))',
	order = {'QED': 1})

GC_1465 = Coupling(name = 'GC_1465',
	value = '-((ee*complex(0,1)*complexconjugate(CKM1x1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_1670 = Coupling(name = 'GC_1670',
	value = '-((ee*complex(0,1)*complexconjugate(CKM1x2))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_1875 = Coupling(name = 'GC_1875',
	value = '-((ee*complex(0,1)*complexconjugate(CKM1x3))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_2080 = Coupling(name = 'GC_2080',
	value = '-((ee*complex(0,1)*complexconjugate(CKM2x1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_2285 = Coupling(name = 'GC_2285',
	value = '-((ee*complex(0,1)*complexconjugate(CKM2x2))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_2490 = Coupling(name = 'GC_2490',
	value = '-((ee*complex(0,1)*complexconjugate(CKM2x3))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_2695 = Coupling(name = 'GC_2695',
	value = '-((ee*complex(0,1)*complexconjugate(CKM3x1))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_2901 = Coupling(name = 'GC_2901',
	value = '-((ee*complex(0,1)*complexconjugate(CKM3x2))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

GC_3107 = Coupling(name = 'GC_3107',
	value = '-((ee*complex(0,1)*complexconjugate(CKM3x3))/(sth*cmath.sqrt(2)))',
	order = {'QED': 1})

