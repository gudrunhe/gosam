# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 13.0.1 for Linux x86 (64-bit) (January 29, 2022)
# Date: Mon 8 Jan 2024 12:54:06


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

GC_17 = Coupling(name = 'GC_17',
	value = '-(2**0.25*fmd3x3*complex(0,1)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_18 = Coupling(name = 'GC_18',
	value = '2**0.25*fmd3x3*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_35 = Coupling(name = 'GC_35',
	value = '-(2**0.25*fml3x3*complex(0,1)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_36 = Coupling(name = 'GC_36',
	value = '2**0.25*fml3x3*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_53 = Coupling(name = 'GC_53',
	value = '-(2**0.25*fmu3x3*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_54 = Coupling(name = 'GC_54',
	value = '-(2**0.25*fmu3x3*complex(0,1)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_55 = Coupling(name = 'GC_55',
	value = '-(2**0.25*complex(0,1)*Hmass**2*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_56 = Coupling(name = 'GC_56',
	value = '-3*2**0.25*complex(0,1)*Hmass**2*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_57 = Coupling(name = 'GC_57',
	value = '-(complex(0,1)*Gf*Hmass**2*cmath.sqrt(2))',
	order = {'QED':2})

GC_58 = Coupling(name = 'GC_58',
	value = '-2*complex(0,1)*Gf*Hmass**2*cmath.sqrt(2)',
	order = {'QED':2})

GC_59 = Coupling(name = 'GC_59',
	value = '-3*complex(0,1)*Gf*Hmass**2*cmath.sqrt(2)',
	order = {'QED':2})

GC_68 = Coupling(name = 'GC_68',
	value = '-(2**0.75*complex(0,1)*I1a33*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_77 = Coupling(name = 'GC_77',
	value = '2**0.75*complex(0,1)*I2a33*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_86 = Coupling(name = 'GC_86',
	value = '2**0.75*complex(0,1)*I4a33*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_95 = Coupling(name = 'GC_95',
	value = '-(2**0.75*complex(0,1)*I5a33*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_334 = Coupling(name = 'GC_334',
	value = '-2*complex(0,1)*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
	order = {'QCD':1})

GC_335 = Coupling(name = 'GC_335',
	value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
	order = {'QCD':1})

GC_335_1 = Coupling(name = 'GC_335_1',
	value = '-2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
	order = {'QCD':1})

GC_393 = Coupling(name = 'GC_393',
	value = '4*aS*cmath.pi*complex(0,1)',
	order = {'QCD':2})

GC_435 = Coupling(name = 'GC_435',
	value = '-(2**0.25*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_436 = Coupling(name = 'GC_436',
	value = '-(2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_437 = Coupling(name = 'GC_437',
	value = '2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_438 = Coupling(name = 'GC_438',
	value = '-(2**0.75*complex(0,1)*Kq1x1*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_442 = Coupling(name = 'GC_442',
	value = '-(2**0.75*complex(0,1)*Kq2x2*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_446 = Coupling(name = 'GC_446',
	value = '-(2**0.75*complex(0,1)*Kq3x3*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_447 = Coupling(name = 'GC_447',
	value = '-(2**0.75*complex(0,1)*Ul1x1*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_451 = Coupling(name = 'GC_451',
	value = '-(2**0.75*complex(0,1)*Ul2x2*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_455 = Coupling(name = 'GC_455',
	value = '-(2**0.75*complex(0,1)*Ul3x3*Wmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_456 = Coupling(name = 'GC_456',
	value = '2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_457 = Coupling(name = 'GC_457',
	value = '2*complex(0,1)*Gf*Wmass**2*cmath.sqrt(2)',
	order = {'QED':2})

GC_458 = Coupling(name = 'GC_458',
	value = '-4*complex(0,1)*Gf*Wmass**2*cmath.sqrt(2)',
	order = {'QED':2})

GC_459 = Coupling(name = 'GC_459',
	value = '-(2**0.25*Wmass**2*xiW*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_459_1 = Coupling(name = 'GC_459_1',
	value = '(2**0.25*Wmass**2*xiW*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_460 = Coupling(name = 'GC_460',
	value = '2**0.25*complex(0,1)*Wmass**2*xiW*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_460_1 = Coupling(name = 'GC_460_1',
	value = '-2**0.25*complex(0,1)*Wmass**2*xiW*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_461 = Coupling(name = 'GC_461',
	value = '2**0.25*Wmass**2*xiW*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_461_1 = Coupling(name = 'GC_461_1',
	value = '-2**0.25*Wmass**2*xiW*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_462 = Coupling(name = 'GC_462',
	value = '4*complex(0,1)*Gf*Wmass**2*cmath.sqrt(2) - (4*complex(0,1)*Gf*Wmass**4*cmath.sqrt(2))/Zmass**2',
	order = {'QED':2})

GC_463 = Coupling(name = 'GC_463',
	value = '8*complex(0,1)*Gf*Wmass**2*cmath.sqrt(2) - (8*complex(0,1)*Gf*Wmass**4*cmath.sqrt(2))/Zmass**2',
	order = {'QED':2})

GC_464 = Coupling(name = 'GC_464',
	value = '(4*complex(0,1)*Gf*Wmass**4*cmath.sqrt(2))/Zmass**2',
	order = {'QED':2})

GC_465 = Coupling(name = 'GC_465',
	value = '(-2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/Zmass',
	order = {'QED':1})

GC_465_1 = Coupling(name = 'GC_465_1',
	value = '-(-2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/Zmass',
	order = {'QED':1})

GC_466 = Coupling(name = 'GC_466',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/Zmass',
	order = {'QED':1})

GC_466_1 = Coupling(name = 'GC_466_1',
	value = '-(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/Zmass',
	order = {'QED':1})

GC_467 = Coupling(name = 'GC_467',
	value = '-(2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_468 = Coupling(name = 'GC_468',
	value = '2**0.25*Zmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_469 = Coupling(name = 'GC_469',
	value = '-(2**0.25*complex(0,1)*Wmass*xiZ*Zmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_469_1 = Coupling(name = 'GC_469_1',
	value = '(2**0.25*complex(0,1)*Wmass*xiZ*Zmass*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_470 = Coupling(name = 'GC_470',
	value = '2*2**0.25*complex(0,1)*Zmass**2*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_471 = Coupling(name = 'GC_471',
	value = '2*complex(0,1)*Gf*Zmass**2*cmath.sqrt(2)',
	order = {'QED':2})

GC_472 = Coupling(name = 'GC_472',
	value = '2**0.25*complex(0,1)*xiZ*Zmass**2*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_472_1 = Coupling(name = 'GC_472_1',
	value = '-2**0.25*complex(0,1)*xiZ*Zmass**2*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_473 = Coupling(name = 'GC_473',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/(3.*Zmass) + (2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf))/3.',
	order = {'QED':1})

GC_474 = Coupling(name = 'GC_474',
	value = '(-4*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/(3.*Zmass) + (2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf))/3.',
	order = {'QED':1})

GC_475 = Coupling(name = 'GC_475',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/(3.*Zmass) - (2*2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf))/3.',
	order = {'QED':1})

GC_476 = Coupling(name = 'GC_476',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/Zmass - 2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_477 = Coupling(name = 'GC_477',
	value = '(-4*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/(3.*Zmass) + (4*2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf))/3.',
	order = {'QED':1})

GC_478 = Coupling(name = 'GC_478',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf))/Zmass - 2*2**0.25*complex(0,1)*Zmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_479 = Coupling(name = 'GC_479',
	value = '(2*2**0.25*complex(0,1)*Wmass**3*cmath.sqrt(Gf))/Zmass - 2*2**0.25*complex(0,1)*Wmass*Zmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_480 = Coupling(name = 'GC_480',
	value = '(2*Gf*Wmass**3*cmath.sqrt(2))/Zmass - 2*Gf*Wmass*Zmass*cmath.sqrt(2)',
	order = {'QED':2})

GC_481 = Coupling(name = 'GC_481',
	value = '(2*complex(0,1)*Gf*Wmass**3*cmath.sqrt(2))/Zmass - 2*complex(0,1)*Gf*Wmass*Zmass*cmath.sqrt(2)',
	order = {'QED':2})

GC_482 = Coupling(name = 'GC_482',
	value = '(-2*Gf*Wmass**3*cmath.sqrt(2))/Zmass + 2*Gf*Wmass*Zmass*cmath.sqrt(2)',
	order = {'QED':2})

GC_483 = Coupling(name = 'GC_483',
	value = '(2*2**0.25*complex(0,1)*Wmass**3*xiW*cmath.sqrt(Gf))/Zmass - 2**0.25*complex(0,1)*Wmass*xiW*Zmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_483_1 = Coupling(name = 'GC_483_1',
	value = '-(2*2**0.25*complex(0,1)*Wmass**3*xiW*cmath.sqrt(Gf))/Zmass + 2**0.25*complex(0,1)*Wmass*xiW*Zmass*cmath.sqrt(Gf)',
	order = {'QED':1})

GC_484 = Coupling(name = 'GC_484',
	value = '(-8*complex(0,1)*Gf*Wmass**3*cmath.sqrt(2)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass**2',
	order = {'QED':2})

GC_485 = Coupling(name = 'GC_485',
	value = '(2*2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/(3.*Zmass)',
	order = {'QED':1})

GC_486 = Coupling(name = 'GC_486',
	value = '(-4*2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/(3.*Zmass)',
	order = {'QED':1})

GC_487 = Coupling(name = 'GC_487',
	value = '(-2*2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_487_1 = Coupling(name = 'GC_487_1',
	value = '-(-2*2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_488 = Coupling(name = 'GC_488',
	value = '(2*2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_488_1 = Coupling(name = 'GC_488_1',
	value = '-(2*2**0.25*complex(0,1)*Wmass*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_489 = Coupling(name = 'GC_489',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_490 = Coupling(name = 'GC_490',
	value = '(-2*Gf*Wmass**2*cmath.sqrt(2)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':2})

GC_491 = Coupling(name = 'GC_491',
	value = '(2*complex(0,1)*Gf*Wmass**2*cmath.sqrt(2)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':2})

GC_492 = Coupling(name = 'GC_492',
	value = '(2*Gf*Wmass**2*cmath.sqrt(2)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':2})

GC_493 = Coupling(name = 'GC_493',
	value = '(2*2**0.25*complex(0,1)*Wmass**2*xiW*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_493_1 = Coupling(name = 'GC_493_1',
	value = '-(2*2**0.25*complex(0,1)*Wmass**2*xiW*cmath.sqrt(Gf)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass',
	order = {'QED':1})

GC_494 = Coupling(name = 'GC_494',
	value = '-8*complex(0,1)*Gf*Wmass**2*cmath.sqrt(2) + (8*complex(0,1)*Gf*Wmass**4*cmath.sqrt(2))/Zmass**2 + 2*complex(0,1)*Gf*Zmass**2*cmath.sqrt(2)',
	order = {'QED':2})

GC_495 = Coupling(name = 'GC_495',
	value = '-4*complex(0,1)*Gf*Wmass*cmath.sqrt(2)*cmath.sqrt(-Wmass**2 + Zmass**2) + (8*complex(0,1)*Gf*Wmass**3*cmath.sqrt(2)*cmath.sqrt(-Wmass**2 + Zmass**2))/Zmass**2',
	order = {'QED':2})

GC_676 = Coupling(name = 'GC_676',
	value = '-(2**0.75*complex(0,1)*Wmass*(Kq1x1)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_680 = Coupling(name = 'GC_680',
	value = '-(2**0.75*complex(0,1)*Wmass*(Kq2x2)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_684 = Coupling(name = 'GC_684',
	value = '-(2**0.75*complex(0,1)*Wmass*(Kq3x3)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_685 = Coupling(name = 'GC_685',
	value = '-(2**0.75*complex(0,1)*Wmass*(Ul1x1)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_689 = Coupling(name = 'GC_689',
	value = '-(2**0.75*complex(0,1)*Wmass*(Ul2x2)*cmath.sqrt(Gf))',
	order = {'QED':1})

GC_693 = Coupling(name = 'GC_693',
	value = '-(2**0.75*complex(0,1)*Wmass*(Ul3x3)*cmath.sqrt(Gf))',
	order = {'QED':1})

#### NP1 couplings from CphiG ####

GC_114 = Coupling(name = 'GC_114',
	value = '4*CphiG*complex(0,1)*Lam*yt**2*2',
	order = {'NP':1, 'QED':2})

GC_178 = Coupling(name = 'GC_178',
	value = '(2*2**0.75*CphiG*complex(0,1)*Lam)/cmath.sqrt(Gf)*yt**2*2',
	order = {'NP':1, 'QED':1})

GC_336 = Coupling(name = 'GC_336',
	value = '-8*CphiG*Lam*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)*yt**2*2',
	order = {'NP':1, 'QED':2, 'QCD':1})

GC_337 = Coupling(name = 'GC_337',
	value = '(-4*2**0.75*CphiG*Lam*cmath.sqrt(aS)*cmath.sqrt(cmath.pi))/cmath.sqrt(Gf)*yt**2*2',
	order = {'NP':1, 'QED':1, 'QCD':1})

GC_394 = Coupling(name = 'GC_394',
	value = '-16*aS*CphiG*cmath.pi*complex(0,1)*Lam*yt**2*2',
	order = {'NP':1, 'QED':2, 'QCD':2})

GC_395 = Coupling(name = 'GC_395',
	value = '(-8*2**0.75*aS*CphiG*cmath.pi*complex(0,1)*Lam)/cmath.sqrt(Gf)*yt**2*2',
	order = {'NP':1, 'QED':1, 'QCD':2})

#### NP1 couplings from Ctphi ####

GC_165 = Coupling(name = 'GC_165',
	value = '(Cuphi3x3*complex(0,1)*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_166 = Coupling(name = 'GC_166',
	value = '(3*Cuphi3x3*complex(0,1)*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_167 = Coupling(name = 'GC_167',
	value = '(Cuphi3x3*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_168 = Coupling(name = 'GC_168',
	value = '(3*Cuphi3x3*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_177 = Coupling(name = 'GC_177',
	value = '(Cuphi3x3*complex(0,1)*Lam)/(2.*Gf)*yt**3',
	order = {'NP':1, 'QED':1})

GC_212 = Coupling(name = 'GC_212',
	value = '(Cuphi3x3*complex(0,1)*Lam)/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2})

GC_213 = Coupling(name = 'GC_213',
	value = '(3*Cuphi3x3*complex(0,1)*Lam)/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2})

GC_214 = Coupling(name = 'GC_214',
	value = '(Cuphi3x3*Lam)/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2})

GC_668 = Coupling(name = 'GC_668',
	value = '(-3*Lam*(Cuphi3x3))/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_669 = Coupling(name = 'GC_669',
	value = '-((Lam*(Cuphi3x3))/cmath.sqrt(2))*yt**3',
	order = {'NP':1, 'QED':3})

GC_670 = Coupling(name = 'GC_670',
	value = '(complex(0,1)*Lam*(Cuphi3x3))/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_671 = Coupling(name = 'GC_671',
	value = '(3*complex(0,1)*Lam*(Cuphi3x3))/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3})

GC_672 = Coupling(name = 'GC_672',
	value = '(complex(0,1)*Lam*(Cuphi3x3))/(2.*Gf)*yt**3',
	order = {'NP':1, 'QED':1})

GC_673 = Coupling(name = 'GC_673',
	value = '-((Lam*(Cuphi3x3))/(2**0.75*cmath.sqrt(Gf)))*yt**3',
	order = {'NP':1, 'QED':2})

GC_674 = Coupling(name = 'GC_674',
	value = '(complex(0,1)*Lam*(Cuphi3x3))/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2})

GC_675 = Coupling(name = 'GC_675',
	value = '(3*complex(0,1)*Lam*(Cuphi3x3))/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2})

