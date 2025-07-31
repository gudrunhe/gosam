# This file was automatically created from UFO model SMEFTsim_U35_MwScheme_UFO
# by applying the 'modify_UFO.py' script. Only SM vertices and those containing
# one of the following coefficients have been kept:
# cHW  cHB  cHWB 


from object_library import all_parameters, Parameter
from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

CKM1x3 = Parameter(name = 'CKM1x3',
	nature = 'internal',
	type = 'complex',
	value = 'CKMA*CKMlambda**3*(CKMrho - CKMeta*complex(0,1))',
	texname = '\\text{CKM1x3}',
	lhablock = 'None',
	lhacode = None)

MZ = Parameter(name = 'MZ',
	nature = 'external',
	type = 'real',
	value = '91.1876',
	texname = '\\text{MZ}',
	lhablock = 'MASS',
	lhacode = [ 23 ])

CKM2x1 = Parameter(name = 'CKM2x1',
	nature = 'internal',
	type = 'complex',
	value = '-CKMlambda',
	texname = '\\text{CKM2x1}',
	lhablock = 'None',
	lhacode = None)

Me = Parameter(name = 'Me',
	nature = 'external',
	type = 'real',
	value = '0.000511',
	texname = '\\text{Me}',
	lhablock = 'MASS',
	lhacode = [ 11 ])

CKM2x2 = Parameter(name = 'CKM2x2',
	nature = 'internal',
	type = 'complex',
	value = '1 - CKMlambda**2/2.',
	texname = '\\text{CKM2x2}',
	lhablock = 'None',
	lhacode = None)

MMU = Parameter(name = 'MMU',
	nature = 'external',
	type = 'real',
	value = '0.10566',
	texname = '\\text{MMU}',
	lhablock = 'MASS',
	lhacode = [ 13 ])

CKM2x3 = Parameter(name = 'CKM2x3',
	nature = 'internal',
	type = 'complex',
	value = 'CKMA*CKMlambda**2',
	texname = '\\text{CKM2x3}',
	lhablock = 'None',
	lhacode = None)

MTA = Parameter(name = 'MTA',
	nature = 'external',
	type = 'real',
	value = '1.777',
	texname = '\\text{MTA}',
	lhablock = 'MASS',
	lhacode = [ 15 ])

CKM3x1 = Parameter(name = 'CKM3x1',
	nature = 'internal',
	type = 'complex',
	value = 'CKMA*CKMlambda**3*(1 - CKMrho - CKMeta*complex(0,1))',
	texname = '\\text{CKM3x1}',
	lhablock = 'None',
	lhacode = None)

MU = Parameter(name = 'MU',
	nature = 'external',
	type = 'real',
	value = '0.00216',
	texname = 'M',
	lhablock = 'MASS',
	lhacode = [ 2 ])

CKM3x2 = Parameter(name = 'CKM3x2',
	nature = 'internal',
	type = 'complex',
	value = '-(CKMA*CKMlambda**2)',
	texname = '\\text{CKM3x2}',
	lhablock = 'None',
	lhacode = None)

MC = Parameter(name = 'MC',
	nature = 'external',
	type = 'real',
	value = '1.27',
	texname = '\\text{MC}',
	lhablock = 'MASS',
	lhacode = [ 4 ])

CKM3x3 = Parameter(name = 'CKM3x3',
	nature = 'internal',
	type = 'complex',
	value = '1',
	texname = '\\text{CKM3x3}',
	lhablock = 'None',
	lhacode = None)

MT = Parameter(name = 'MT',
	nature = 'external',
	type = 'real',
	value = '172.76',
	texname = '\\text{MT}',
	lhablock = 'MASS',
	lhacode = [ 6 ])

ZERO = Parameter(name = 'ZERO',
	nature = 'internal',
	type = 'real',
	value = '0.0',
	texname = '0',
	lhablock = 'None',
	lhacode = None)

MD = Parameter(name = 'MD',
	nature = 'external',
	type = 'real',
	value = '0.00467',
	texname = '\\text{MD}',
	lhablock = 'MASS',
	lhacode = [ 1 ])

MZ1 = Parameter(name = 'MZ1',
	nature = 'internal',
	type = 'real',
	value = 'MZ',
	texname = '\\text{MZ}\'',
	lhablock = 'None',
	lhacode = None)

CKMlambda = Parameter(name = 'CKMlambda',
	nature = 'external',
	type = 'real',
	value = '0.2265',
	texname = '\\text{CKMlambda}',
	lhablock = 'CKMBLOCK',
	lhacode = [ 2 ])

MS = Parameter(name = 'MS',
	nature = 'external',
	type = 'real',
	value = '0.093',
	texname = '\\text{MS}',
	lhablock = 'MASS',
	lhacode = [ 3 ])

MH1 = Parameter(name = 'MH1',
	nature = 'internal',
	type = 'real',
	value = 'MH',
	texname = '\\text{MH}\'',
	lhablock = 'None',
	lhacode = None)

CKMA = Parameter(name = 'CKMA',
	nature = 'external',
	type = 'real',
	value = '0.79',
	texname = '\\text{CKMA}',
	lhablock = 'CKMBLOCK',
	lhacode = [ 3 ])

MB = Parameter(name = 'MB',
	nature = 'external',
	type = 'real',
	value = '4.18',
	texname = '\\text{MB}',
	lhablock = 'MASS',
	lhacode = [ 5 ])

MT1 = Parameter(name = 'MT1',
	nature = 'internal',
	type = 'real',
	value = 'MT',
	texname = '\\text{MT}\'',
	lhablock = 'None',
	lhacode = None)

MH = Parameter(name = 'MH',
	nature = 'external',
	type = 'real',
	value = '125.09',
	texname = '\\text{MH}',
	lhablock = 'MASS',
	lhacode = [ 25 ])

WZ1 = Parameter(name = 'WZ1',
	nature = 'internal',
	type = 'real',
	value = 'WZ',
	texname = '\\text{WZ}\'',
	lhablock = 'None',
	lhacode = None)

WZ = Parameter(name = 'WZ',
	nature = 'external',
	type = 'real',
	value = '2.4952',
	texname = '\\text{WZ}',
	lhablock = 'DECAY',
	lhacode = [ 23 ])

WW1 = Parameter(name = 'WW1',
	nature = 'internal',
	type = 'real',
	value = 'WW',
	texname = '\\text{WW}\'',
	lhablock = 'None',
	lhacode = None)

WW = Parameter(name = 'WW',
	nature = 'external',
	type = 'real',
	value = '2.085',
	texname = '\\text{WW}',
	lhablock = 'DECAY',
	lhacode = [ 24 ])

WH1 = Parameter(name = 'WH1',
	nature = 'internal',
	type = 'real',
	value = 'WH',
	texname = '\\text{WH}\'',
	lhablock = 'None',
	lhacode = None)

WT = Parameter(name = 'WT',
	nature = 'external',
	type = 'real',
	value = '1.33',
	texname = '\\text{WT}',
	lhablock = 'DECAY',
	lhacode = [ 6 ])

WT1 = Parameter(name = 'WT1',
	nature = 'internal',
	type = 'real',
	value = 'WT',
	texname = '\\text{WT}\'',
	lhablock = 'None',
	lhacode = None)

WH = Parameter(name = 'WH',
	nature = 'external',
	type = 'real',
	value = '0.00407',
	texname = '\\text{WH}',
	lhablock = 'DECAY',
	lhacode = [ 25 ])

cth = Parameter(name = 'cth',
	nature = 'internal',
	type = 'real',
	value = 'cmath.sqrt(1 - sth2)',
	texname = 'c_{\\theta }',
	lhablock = 'None',
	lhacode = None)

MW1 = Parameter(name = 'MW1',
	nature = 'internal',
	type = 'real',
	value = 'MWsm',
	texname = '\\text{MW}\'',
	lhablock = 'None',
	lhacode = None)

sth = Parameter(name = 'sth',
	nature = 'internal',
	type = 'real',
	value = 'cmath.sqrt(sth2)',
	texname = 's_{\\theta }',
	lhablock = 'None',
	lhacode = None)

ee = Parameter(name = 'ee',
	nature = 'internal',
	type = 'real',
	value = '2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)',
	texname = 'e',
	lhablock = 'None',
	lhacode = None)

yb = Parameter(name = 'yb',
	nature = 'internal',
	type = 'real',
	value = '(ymb*cmath.sqrt(2))/vevhat',
	texname = '\\text{yb}',
	lhablock = 'None',
	lhacode = None)

yc = Parameter(name = 'yc',
	nature = 'internal',
	type = 'real',
	value = '(ymc*cmath.sqrt(2))/vevhat',
	texname = '\\text{yc}',
	lhablock = 'None',
	lhacode = None)

ydo = Parameter(name = 'ydo',
	nature = 'internal',
	type = 'real',
	value = '(ymdo*cmath.sqrt(2))/vevhat',
	texname = '\\text{ydo}',
	lhablock = 'None',
	lhacode = None)

ye = Parameter(name = 'ye',
	nature = 'internal',
	type = 'real',
	value = '(yme*cmath.sqrt(2))/vevhat',
	texname = '\\text{ye}',
	lhablock = 'None',
	lhacode = None)

ym = Parameter(name = 'ym',
	nature = 'internal',
	type = 'real',
	value = '(ymm*cmath.sqrt(2))/vevhat',
	texname = '\\text{ym}',
	lhablock = 'None',
	lhacode = None)

ys = Parameter(name = 'ys',
	nature = 'internal',
	type = 'real',
	value = '(yms*cmath.sqrt(2))/vevhat',
	texname = '\\text{ys}',
	lhablock = 'None',
	lhacode = None)

CKMrho = Parameter(name = 'CKMrho',
	nature = 'external',
	type = 'real',
	value = '0.141',
	texname = '\\text{CKMrho}',
	lhablock = 'CKMBLOCK',
	lhacode = [ 4 ])

yt = Parameter(name = 'yt',
	nature = 'internal',
	type = 'real',
	value = '(ymt*cmath.sqrt(2))/vevhat',
	texname = '\\text{yt}',
	lhablock = 'None',
	lhacode = None)

CKMeta = Parameter(name = 'CKMeta',
	nature = 'external',
	type = 'real',
	value = '0.357',
	texname = '\\text{CKMeta}',
	lhablock = 'CKMBLOCK',
	lhacode = [ 5 ])

ytau = Parameter(name = 'ytau',
	nature = 'internal',
	type = 'real',
	value = '(ymtau*cmath.sqrt(2))/vevhat',
	texname = '\\text{ytau}',
	lhablock = 'None',
	lhacode = None)

LambdaSMEFT = Parameter(name = 'LambdaSMEFT',
	nature = 'external',
	type = 'real',
	value = '1000',
	texname = '\\Lambda',
	lhablock = 'SMEFTcutoff',
	lhacode = [ 1 ])

yup = Parameter(name = 'yup',
	nature = 'internal',
	type = 'real',
	value = '(ymup*cmath.sqrt(2))/vevhat',
	texname = '\\text{yup}',
	lhablock = 'None',
	lhacode = None)

MW = Parameter(name = 'MW',
	nature = 'external',
	type = 'real',
	value = '80.387',
	texname = '\\text{MW}',
	lhablock = 'SMINPUTS',
	lhacode = [ 1 ])

Gf = Parameter(name = 'Gf',
	nature = 'external',
	type = 'real',
	value = '1.1663787e-05',
	texname = 'G_f',
	lhablock = 'SMINPUTS',
	lhacode = [ 2 ])

aS = Parameter(name = 'aS',
	nature = 'external',
	type = 'real',
	value = '0.1179',
	texname = '\\alpha _s',
	lhablock = 'SMINPUTS',
	lhacode = [ 3 ])

ymdo = Parameter(name = 'ymdo',
	nature = 'external',
	type = 'real',
	value = '0.00467',
	texname = '\\text{ymdo}',
	lhablock = 'YUKAWA',
	lhacode = [ 1 ])

MWsm = Parameter(name = 'MWsm',
	nature = 'internal',
	type = 'real',
	value = 'MW',
	texname = '\\text{MWsm}',
	lhablock = 'None',
	lhacode = None)

ymup = Parameter(name = 'ymup',
	nature = 'external',
	type = 'real',
	value = '0.00216',
	texname = '\\text{ymup}',
	lhablock = 'YUKAWA',
	lhacode = [ 2 ])

cHW = Parameter(name = 'cHW',
	nature = 'external',
	type = 'real',
	value = '0',
	texname = 'c_{\\text{HW}}',
	lhablock = 'SMEFT',
	lhacode = [ 7 ])

aEW = Parameter(name = 'aEW',
	nature = 'internal',
	type = 'real',
	value = '(Gf*MW**2*(1 - MW**2/MZ**2)*cmath.sqrt(2))/cmath.pi',
	texname = '\\alpha _{\\text{EW}}',
	lhablock = 'None',
	lhacode = None)

yms = Parameter(name = 'yms',
	nature = 'external',
	type = 'real',
	value = '0.093',
	texname = '\\text{yms}',
	lhablock = 'YUKAWA',
	lhacode = [ 3 ])

cHB = Parameter(name = 'cHB',
	nature = 'external',
	type = 'real',
	value = '0',
	texname = 'c_{\\text{HB}}',
	lhablock = 'SMEFT',
	lhacode = [ 8 ])

vevhat = Parameter(name = 'vevhat',
	nature = 'internal',
	type = 'real',
	value = '1/(2**0.25*cmath.sqrt(Gf))',
	texname = '\\hat{v}',
	lhablock = 'None',
	lhacode = None)

ymc = Parameter(name = 'ymc',
	nature = 'external',
	type = 'real',
	value = '1.27',
	texname = '\\text{ymc}',
	lhablock = 'YUKAWA',
	lhacode = [ 4 ])

cHWB = Parameter(name = 'cHWB',
	nature = 'external',
	type = 'real',
	value = '0',
	texname = 'c_{\\text{HWB}}',
	lhablock = 'SMEFT',
	lhacode = [ 9 ])

lam = Parameter(name = 'lam',
	nature = 'internal',
	type = 'real',
	value = '(Gf*MH**2)/cmath.sqrt(2)',
	texname = '\\text{lam}',
	lhablock = 'None',
	lhacode = None)

ymb = Parameter(name = 'ymb',
	nature = 'external',
	type = 'real',
	value = '4.18',
	texname = '\\text{ymb}',
	lhablock = 'YUKAWA',
	lhacode = [ 5 ])

G = Parameter(name = 'G',
	nature = 'internal',
	type = 'real',
	value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
	texname = 'G',
	lhablock = 'None',
	lhacode = None)

ymt = Parameter(name = 'ymt',
	nature = 'external',
	type = 'real',
	value = '172.76',
	texname = '\\text{ymt}',
	lhablock = 'YUKAWA',
	lhacode = [ 6 ])

sth2 = Parameter(name = 'sth2',
	nature = 'internal',
	type = 'real',
	value = '1 - MW**2/MZ**2',
	texname = '\\text{sth2}',
	lhablock = 'None',
	lhacode = None)

yme = Parameter(name = 'yme',
	nature = 'external',
	type = 'real',
	value = '0.000511',
	texname = '\\text{yme}',
	lhablock = 'YUKAWA',
	lhacode = [ 11 ])

CKM1x1 = Parameter(name = 'CKM1x1',
	nature = 'internal',
	type = 'complex',
	value = '1 - CKMlambda**2/2.',
	texname = '\\text{CKM1x1}',
	lhablock = 'None',
	lhacode = None)

ymm = Parameter(name = 'ymm',
	nature = 'external',
	type = 'real',
	value = '0.10566',
	texname = '\\text{ymm}',
	lhablock = 'YUKAWA',
	lhacode = [ 13 ])

CKM1x2 = Parameter(name = 'CKM1x2',
	nature = 'internal',
	type = 'complex',
	value = 'CKMlambda',
	texname = '\\text{CKM1x2}',
	lhablock = 'None',
	lhacode = None)

ymtau = Parameter(name = 'ymtau',
	nature = 'external',
	type = 'real',
	value = '1.777',
	texname = '\\text{ymtau}',
	lhablock = 'YUKAWA',
	lhacode = [ 15 ])

