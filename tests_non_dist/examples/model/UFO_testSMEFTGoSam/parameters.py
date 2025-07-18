# This file was automatically created by FeynRules 2.3.47
# Mathematica version: 12.1.1 for Linux x86 (64-bit) (June 19, 2020)
# Date: Mon 20 Feb 2023 15:47:51



from .object_library import all_parameters, Parameter


from .function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
aEWM1 = Parameter(name = 'aEWM1',
                  nature = 'external',
                  type = 'real',
                  value = 127.9,
                  texname = '\\text{aEWM1}',
                  lhablock = 'SMINPUTS',
                  lhacode = [ 1 ])

Gf = Parameter(name = 'Gf',
               nature = 'external',
               type = 'real',
               value = 0.0000116637,
               texname = 'G_f',
               lhablock = 'SMINPUTS',
               lhacode = [ 2 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.1184,
               texname = '\\alpha _s',
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

ymdo = Parameter(name = 'ymdo',
                 nature = 'external',
                 type = 'real',
                 value = 0.,
                 texname = '\\text{ymdo}',
                 lhablock = 'YUKAWA',
                 lhacode = [ 1 ])

ymup = Parameter(name = 'ymup',
                 nature = 'external',
                 type = 'real',
                 value = 0.,
                 texname = '\\text{ymup}',
                 lhablock = 'YUKAWA',
                 lhacode = [ 2 ])

yms = Parameter(name = 'yms',
                nature = 'external',
                type = 'real',
                value = 0.,
                texname = '\\text{yms}',
                lhablock = 'YUKAWA',
                lhacode = [ 3 ])

ymc = Parameter(name = 'ymc',
                nature = 'external',
                type = 'real',
                value = 0.,
                texname = '\\text{ymc}',
                lhablock = 'YUKAWA',
                lhacode = [ 4 ])

ymb = Parameter(name = 'ymb',
                nature = 'external',
                type = 'real',
                value = 4.7,
                texname = '\\text{ymb}',
                lhablock = 'YUKAWA',
                lhacode = [ 5 ])

ymt = Parameter(name = 'ymt',
                nature = 'external',
                type = 'real',
                value = 173,
                texname = '\\text{ymt}',
                lhablock = 'YUKAWA',
                lhacode = [ 6 ])

yme = Parameter(name = 'yme',
                nature = 'external',
                type = 'real',
                value = 0.,
                texname = '\\text{yme}',
                lhablock = 'YUKAWA',
                lhacode = [ 11 ])

ymm = Parameter(name = 'ymm',
                nature = 'external',
                type = 'real',
                value = 0.,
                texname = '\\text{ymm}',
                lhablock = 'YUKAWA',
                lhacode = [ 13 ])

ymtau = Parameter(name = 'ymtau',
                  nature = 'external',
                  type = 'real',
                  value = 1.777,
                  texname = '\\text{ymtau}',
                  lhablock = 'YUKAWA',
                  lhacode = [ 15 ])

CtG = Parameter(name = 'CtG',
                nature = 'external',
                type = 'real',
                value = 1,
                texname = 'C_{\\text{tG}}',
                lhablock = 'FRBlock',
                lhacode = [ 1 ])

Lambdam2 = Parameter(name = 'Lambdam2',
                     nature = 'external',
                     type = 'real',
                     value = 1,
                     texname = '\\text{Lambda}^{-2}',
                     lhablock = 'FRBlock',
                     lhacode = [ 2 ])

ct = Parameter(name = 'ct',
               nature = 'external',
               type = 'real',
               value = 0,
               texname = 'c_t',
               lhablock = 'FRBlock',
               lhacode = [ 3 ])

cgg = Parameter(name = 'cgg',
                nature = 'external',
                type = 'real',
                value = 0,
                texname = 'c_{\\text{gg}}',
                lhablock = 'FRBlock',
                lhacode = [ 4 ])

cgghh = Parameter(name = 'cgghh',
                  nature = 'external',
                  type = 'real',
                  value = 0,
                  texname = 'c_{\\text{gghh}}',
                  lhablock = 'FRBlock',
                  lhacode = [ 5 ])

cthh = Parameter(name = 'cthh',
                 nature = 'external',
                 type = 'real',
                 value = 0,
                 texname = 'c_{\\text{thh}}',
                 lhablock = 'FRBlock',
                 lhacode = [ 6 ])

chhh = Parameter(name = 'chhh',
                 nature = 'external',
                 type = 'real',
                 value = 0,
                 texname = 'c_{\\text{hhh}}',
                 lhablock = 'FRBlock',
                 lhacode = [ 7 ])

chhhh = Parameter(name = 'chhhh',
                  nature = 'external',
                  type = 'real',
                  value = 0,
                  texname = 'c_{\\text{hhhh}}',
                  lhablock = 'FRBlock',
                  lhacode = [ 8 ])

cV = Parameter(name = 'cV',
               nature = 'external',
               type = 'real',
               value = 1,
               texname = 'c_V',
               lhablock = 'FRBlock',
               lhacode = [ 9 ])

cb = Parameter(name = 'cb',
               nature = 'external',
               type = 'real',
               value = 1,
               texname = 'c_b',
               lhablock = 'FRBlock',
               lhacode = [ 10 ])

ctau = Parameter(name = 'ctau',
                 nature = 'external',
                 type = 'real',
                 value = 1,
                 texname = 'c_{\\tau }',
                 lhablock = 'FRBlock',
                 lhacode = [ 11 ])

cgaga = Parameter(name = 'cgaga',
                  nature = 'external',
                  type = 'real',
                  value = 0,
                  texname = 'c_{\\text{gaga}}',
                  lhablock = 'FRBlock',
                  lhacode = [ 12 ])

cZga = Parameter(name = 'cZga',
                 nature = 'external',
                 type = 'real',
                 value = 0,
                 texname = 'c_{\\text{Zga}}',
                 lhablock = 'FRBlock',
                 lhacode = [ 13 ])

cVhh = Parameter(name = 'cVhh',
                 nature = 'external',
                 type = 'real',
                 value = 1,
                 texname = 'c_{\\text{Vhh}}',
                 lhablock = 'FRBlock',
                 lhacode = [ 14 ])

MZ = Parameter(name = 'MZ',
               nature = 'external',
               type = 'real',
               value = 91.1876,
               texname = '\\text{MZ}',
               lhablock = 'MASS',
               lhacode = [ 23 ])

Me = Parameter(name = 'Me',
               nature = 'external',
               type = 'real',
               value = 0.000511,
               texname = '\\text{Me}',
               lhablock = 'MASS',
               lhacode = [ 11 ])

MMU = Parameter(name = 'MMU',
                nature = 'external',
                type = 'real',
                value = 0.10566,
                texname = '\\text{MMU}',
                lhablock = 'MASS',
                lhacode = [ 13 ])

MTA = Parameter(name = 'MTA',
                nature = 'external',
                type = 'real',
                value = 1.777,
                texname = '\\text{MTA}',
                lhablock = 'MASS',
                lhacode = [ 15 ])

MU = Parameter(name = 'MU',
               nature = 'external',
               type = 'real',
               value = 0.00216,
               texname = 'M',
               lhablock = 'MASS',
               lhacode = [ 2 ])

MC = Parameter(name = 'MC',
               nature = 'external',
               type = 'real',
               value = 1.27,
               texname = '\\text{MC}',
               lhablock = 'MASS',
               lhacode = [ 4 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 173.,
               texname = '\\text{MT}',
               lhablock = 'MASS',
               lhacode = [ 6 ])

MD = Parameter(name = 'MD',
               nature = 'external',
               type = 'real',
               value = 0.00467,
               texname = '\\text{MD}',
               lhablock = 'MASS',
               lhacode = [ 1 ])

MS = Parameter(name = 'MS',
               nature = 'external',
               type = 'real',
               value = 0.093,
               texname = '\\text{MS}',
               lhablock = 'MASS',
               lhacode = [ 3 ])

MB = Parameter(name = 'MB',
               nature = 'external',
               type = 'real',
               value = 4.7,
               texname = '\\text{MB}',
               lhablock = 'MASS',
               lhacode = [ 5 ])

WZ = Parameter(name = 'WZ',
               nature = 'external',
               type = 'real',
               value = 2.4952,
               texname = '\\text{WZ}',
               lhablock = 'DECAY',
               lhacode = [ 23 ])

WW = Parameter(name = 'WW',
               nature = 'external',
               type = 'real',
               value = 2.085,
               texname = '\\text{WW}',
               lhablock = 'DECAY',
               lhacode = [ 24 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.33,
               texname = '\\text{WT}',
               lhablock = 'DECAY',
               lhacode = [ 6 ])

Wh = Parameter(name = 'Wh',
               nature = 'external',
               type = 'real',
               value = 0.00407,
               texname = '\\text{Wh}',
               lhablock = 'DECAY',
               lhacode = [ 5000000 ])

aEW = Parameter(name = 'aEW',
                nature = 'internal',
                type = 'real',
                value = '1/aEWM1',
                texname = '\\alpha _{\\text{EW}}')

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
              texname = 'G')

CKM1x1 = Parameter(name = 'CKM1x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '1',
                   texname = '\\text{CKM1x1}')

CKM1x2 = Parameter(name = 'CKM1x2',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM1x2}')

CKM1x3 = Parameter(name = 'CKM1x3',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM1x3}')

CKM2x1 = Parameter(name = 'CKM2x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM2x1}')

CKM2x2 = Parameter(name = 'CKM2x2',
                   nature = 'internal',
                   type = 'complex',
                   value = '1',
                   texname = '\\text{CKM2x2}')

CKM2x3 = Parameter(name = 'CKM2x3',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM2x3}')

CKM3x1 = Parameter(name = 'CKM3x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM3x1}')

CKM3x2 = Parameter(name = 'CKM3x2',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM3x2}')

CKM3x3 = Parameter(name = 'CKM3x3',
                   nature = 'internal',
                   type = 'complex',
                   value = '1',
                   texname = '\\text{CKM3x3}')

loop = Parameter(name = 'loop',
                 nature = 'internal',
                 type = 'real',
                 value = '16*cmath.pi**2',
                 texname = 'L_f')

Mh = Parameter(name = 'Mh',
               nature = 'internal',
               type = 'real',
               value = '125.',
               texname = '\\text{Mh}')

MW = Parameter(name = 'MW',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(MZ**2/2. + cmath.sqrt(MZ**4/4. - (aEW*cmath.pi*MZ**2)/(Gf*cmath.sqrt(2))))',
               texname = 'M_W')

ee = Parameter(name = 'ee',
               nature = 'internal',
               type = 'real',
               value = '2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)',
               texname = 'e')

sw2 = Parameter(name = 'sw2',
                nature = 'internal',
                type = 'real',
                value = '1 - MW**2/MZ**2',
                texname = '\\text{sw2}')

cw = Parameter(name = 'cw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(1 - sw2)',
               texname = 'c_w')

sw = Parameter(name = 'sw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(sw2)',
               texname = 's_w')

g1 = Parameter(name = 'g1',
               nature = 'internal',
               type = 'real',
               value = 'ee/cw',
               texname = 'g_1')

gw = Parameter(name = 'gw',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw',
               texname = 'g_w')

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = '(2*MW*sw)/ee',
                texname = '\\text{vev}')

v = Parameter(name = 'v',
              nature = 'internal',
              type = 'real',
              value = '(2*MW*sw)/ee',
              texname = 'v')

yb = Parameter(name = 'yb',
               nature = 'internal',
               type = 'real',
               value = '(ymb*cmath.sqrt(2))/vev',
               texname = '\\text{yb}')

yc = Parameter(name = 'yc',
               nature = 'internal',
               type = 'real',
               value = '(ymc*cmath.sqrt(2))/vev',
               texname = '\\text{yc}')

ydo = Parameter(name = 'ydo',
                nature = 'internal',
                type = 'real',
                value = '(ymdo*cmath.sqrt(2))/vev',
                texname = '\\text{ydo}')

ye = Parameter(name = 'ye',
               nature = 'internal',
               type = 'real',
               value = '(yme*cmath.sqrt(2))/vev',
               texname = '\\text{ye}')

ym = Parameter(name = 'ym',
               nature = 'internal',
               type = 'real',
               value = '(ymm*cmath.sqrt(2))/vev',
               texname = '\\text{ym}')

ys = Parameter(name = 'ys',
               nature = 'internal',
               type = 'real',
               value = '(yms*cmath.sqrt(2))/vev',
               texname = '\\text{ys}')

yt = Parameter(name = 'yt',
               nature = 'internal',
               type = 'real',
               value = '(ymt*cmath.sqrt(2))/vev',
               texname = '\\text{yt}')

ytau = Parameter(name = 'ytau',
                 nature = 'internal',
                 type = 'real',
                 value = '(ymtau*cmath.sqrt(2))/vev',
                 texname = '\\text{ytau}')

yup = Parameter(name = 'yup',
                nature = 'internal',
                type = 'real',
                value = '(ymup*cmath.sqrt(2))/vev',
                texname = '\\text{yup}')

normh3 = Parameter(name = 'normh3',
                   nature = 'internal',
                   type = 'real',
                   value = 'Mh**2/(2.*v**2)',
                   texname = '\\text{normh3}')

normh4 = Parameter(name = 'normh4',
                   nature = 'internal',
                   type = 'real',
                   value = 'Mh**2/(8.*v**2)',
                   texname = '\\text{normh4}')

yyb = Parameter(name = 'yyb',
                nature = 'internal',
                type = 'real',
                value = 'ymb/v',
                texname = 'y_b')

yyt = Parameter(name = 'yyt',
                nature = 'internal',
                type = 'real',
                value = 'ymt/v',
                texname = 'y_t')

yytau = Parameter(name = 'yytau',
                  nature = 'internal',
                  type = 'real',
                  value = 'ymtau/v',
                  texname = 'y_{\\tau }')

