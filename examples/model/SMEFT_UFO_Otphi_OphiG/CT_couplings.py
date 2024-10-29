# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 13.0.1 for Linux x86 (64-bit) (January 29, 2022)
# Date: Mon 8 Jan 2024 12:54:06


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

#### NP1 couplings from CphiG ####

UVGC_114 = Coupling(name = 'UVGC_114',
	value = '4*CphiG_CT*complex(0,1)*Lam*yt**2*2',
	order = {'NP':1, 'QED':2, 'QCD':2})

UVGC_178 = Coupling(name = 'UVGC_178',
	value = '(2*2**0.75*CphiG_CT*complex(0,1)*Lam)/cmath.sqrt(Gf)*yt**2*2',
	order = {'NP':1, 'QED':1, 'QCD':2})

UVGC_336 = Coupling(name = 'UVGC_336',
	value = '-8*CphiG_CT*Lam*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)*yt**2*2',
	order = {'NP':1, 'QED':2, 'QCD':3})

UVGC_337 = Coupling(name = 'UVGC_337',
	value = '(-4*2**0.75*CphiG_CT*Lam*cmath.sqrt(aS)*cmath.sqrt(cmath.pi))/cmath.sqrt(Gf)*yt**2*2',
	order = {'NP':1, 'QED':1, 'QCD':3})

UVGC_394 = Coupling(name = 'UVGC_394',
	value = '-16*aS*CphiG_CT*cmath.pi*complex(0,1)*Lam*yt**2*2',
	order = {'NP':1, 'QED':2, 'QCD':4})

UVGC_395 = Coupling(name = 'UVGC_395',
	value = '(-8*2**0.75*aS*CphiG_CT*cmath.pi*complex(0,1)*Lam)/cmath.sqrt(Gf)*yt**2*2',
	order = {'NP':1, 'QED':1, 'QCD':4})

#### NP1 couplings from Ctphi ####

UVGC_165 = Coupling(name = 'UVGC_165',
	value = '(Cuphi3x3_CT*complex(0,1)*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_166 = Coupling(name = 'UVGC_166',
	value = '(3*Cuphi3x3_CT*complex(0,1)*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_167 = Coupling(name = 'UVGC_167',
	value = '(Cuphi3x3_CT*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_168 = Coupling(name = 'UVGC_168',
	value = '(3*Cuphi3x3_CT*Lam)/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_177 = Coupling(name = 'UVGC_177',
	value = '(Cuphi3x3_CT*complex(0,1)*Lam)/(2.*Gf)*yt**3',
	order = {'NP':1, 'QED':1, 'QCD':2})

UVGC_212 = Coupling(name = 'UVGC_212',
	value = '(Cuphi3x3_CT*complex(0,1)*Lam)/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2, 'QCD':2})

UVGC_213 = Coupling(name = 'UVGC_213',
	value = '(3*Cuphi3x3_CT*complex(0,1)*Lam)/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2, 'QCD':2})

UVGC_214 = Coupling(name = 'UVGC_214',
	value = '(Cuphi3x3_CT*Lam)/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2, 'QCD':2})

UVGC_668 = Coupling(name = 'UVGC_668',
	value = '(-3*Lam*(Cuphi3x3_CT))/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_669 = Coupling(name = 'UVGC_669',
	value = '-((Lam*(Cuphi3x3_CT))/cmath.sqrt(2))*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_670 = Coupling(name = 'UVGC_670',
	value = '(complex(0,1)*Lam*(Cuphi3x3_CT))/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_671 = Coupling(name = 'UVGC_671',
	value = '(3*complex(0,1)*Lam*(Cuphi3x3_CT))/cmath.sqrt(2)*yt**3',
	order = {'NP':1, 'QED':3, 'QCD':2})

UVGC_672 = Coupling(name = 'UVGC_672',
	value = '(complex(0,1)*Lam*(Cuphi3x3_CT))/(2.*Gf)*yt**3',
	order = {'NP':1, 'QED':1, 'QCD':2})

UVGC_673 = Coupling(name = 'UVGC_673',
	value = '-((Lam*(Cuphi3x3_CT))/(2**0.75*cmath.sqrt(Gf)))*yt**3',
	order = {'NP':1, 'QED':2, 'QCD':2})

UVGC_674 = Coupling(name = 'UVGC_674',
	value = '(complex(0,1)*Lam*(Cuphi3x3_CT))/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2, 'QCD':2})

UVGC_675 = Coupling(name = 'UVGC_675',
	value = '(3*complex(0,1)*Lam*(Cuphi3x3_CT))/(2**0.75*cmath.sqrt(Gf))*yt**3',
	order = {'NP':1, 'QED':2, 'QCD':2})

