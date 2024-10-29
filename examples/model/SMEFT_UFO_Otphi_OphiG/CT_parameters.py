# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 13.0.1 for Linux x86 (64-bit) (January 29, 2022)
# Date: Mon 8 Jan 2024 12:54:06



from object_library import all_parameters, Parameter, all_CTparameters, CTParameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot


CphiG_CT = CTParameter(name = 'CphiG_CT',
                  type = 'real',
                  value = {
                     -1: 'aS/2/cmath.pi*(-7/2*CphiG)',
                     0: {'const': 'dred*aS/2/cmath.pi*(CphiG/2)', 'log': 'aS/2/cmath.pi*(-7/2*CphiG)'}
                  },
                  texname = '\\delta\\text{CphiG\\_CT}')

Cuphi3x3_CT = CTParameter(name = 'Cuphi3x3_CT',
                     type = 'real',
                     value = {
                     -1:'aS/2/cmath.pi*(-2*Cuphi3x3+16*CphiG)',
                     0:{'const': 'dred*aS/2/cmath.pi*(-2/3*Cuphi3x3+16/3*CphiG)', 'log': 'aS/2/cmath.pi*(-2*Cuphi3x3+16*CphiG)'}
                     },
                     texname = '\\delta\\text{Cuphi3x3\\_CT}')
