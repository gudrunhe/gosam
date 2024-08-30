# vim: ts=3:sw=3:expandtab
#@modelproperty: supports ewchoose
from golem.model.particle import Particle
from golem.model import MODEL_OPTIONS
import golem.util.tools
from math import sqrt

import logging
logger = logging.getLogger(__name__)

model_name = "Standard Model in Feynman Gauge (Diagonal CKM)"
#---#[ particles:
particles = {
   'U':       Particle('U',        1,   'mU',  3, 'Ubar',  '0',        2,     2.0),
   'Ubar':    Particle('Ubar',    -1,   'mU', -3, 'U',     '0',       -2,     2.0),
   'D':       Particle('D',        1,   'mD',  3, 'Dbar',  '0',        1,    -1.0),
   'Dbar':    Particle('Dbar',    -1,   'mD', -3, 'D',     '0',       -1,    -1.0),
   'S':       Particle('S',        1,   'mS',  3, 'Sbar',  '0',        3,    -1.0),
   'Sbar':    Particle('Sbar',    -1,   'mS', -3, 'S',     '0',       -3,    -1.0),
   'C':       Particle('C',        1,   'mC',  3, 'Cbar',  '0',        4,     2.0),
   'Cbar':    Particle('Cbar',    -1,   'mC', -3, 'C',     '0',       -4,     2.0),
   'T':       Particle('T',        1,   'mT',  3, 'Tbar', 'wT',        6,     2.0),
   'Tbar':    Particle('Tbar',    -1,   'mT', -3, 'T',    'wT',       -6,     2.0),
   'B':       Particle('B',        1,   'mB',  3, 'Bbar', 'wB',        5,    -1.0),
   'Bbar':    Particle('Bbar',    -1,   'mB', -3, 'B',    'wB',       -5,    -1.0),
   'gh':      Particle('gh',       0,      0,  8, 'ghbar', '0',  9000001,     0.0),
   'ghbar':   Particle('ghbar',    0,      0,  8, 'gh',    '0', -9000001,     0.0),
   'g':       Particle('g',        2,      0,  8, None,    '0',       21,     0.0),
   'A':       Particle('A',        2,      0,  1, None,    '0',       22,     0.0),
   'Z':       Particle('Z',        2,   'mZ',  1, None,   'wZ',       23,     0.0),
   'Wm':      Particle('Wm',       2,   'mW',  1, 'Wp',   'wW',      -24,    -3.0),
   'Wp':      Particle('Wp',       2,   'mW',  1, 'Wm',   'wW',       24,     3.0),

   'em':      Particle('em',       1,   'me',  1, 'ep',    '0',       11,    -3.0),
   'ep':      Particle('ep',      -1,   'me',  1, 'em',    '0',      -11,    -3.0),
   'ne':      Particle('ne',       1,      0,  1, 'nebar', '0',       12,     0.0),
   'nebar':   Particle('nebar',   -1,      0,  1, 'ne',    '0',      -12,     0.0),

   'mum':     Particle('mum',      1,  'mmu',  1, 'mup',   '0',       13,    -3.0),
   'mup':     Particle('mup',     -1,  'mmu',  1, 'mum',   '0',      -13,    -3.0),
   'nmu':     Particle('nmu',      1,      0,  1, 'nmubar', '0',      14,     0.0),
   'nmubar':  Particle('nmubar',  -1,      0,  1, 'nmu',   '0',      -14,     0.0),

   'taum':    Particle('taum',     1, 'mtau',  1, 'taup', 'wtau',     15,    -3.0),
   'taup':    Particle('taup',    -1, 'mtau',  1, 'taum', 'wtau',    -15,    -3.0),
   'ntau':    Particle('ntau',     1,      0,  1, 'ntaubar', '0',     16,     0.0),
   'ntaubar': Particle('ntaubar', -1,      0,  1, 'ntau',   '0',     -16,     0.0),

   'H':       Particle('H',        0,   'mH',  1, 'H',      'wH',     25,     0.0),
   'phim':    Particle('phim',     0,   'mW',  1, 'phip', 'wphi',   -251,    -3.0),
   'phip':    Particle('phip',     0,   'mW',  1, 'phim', 'wphi',    251,     3.0),
   'chi':     Particle('chi',      0,   'mZ',  1, 'chi',  'wchi',    250,     0.0),

   'ghA':     Particle('ghA',      0,      0,  1, 'ghAbar', '0', 9000002,     0.0),
   'ghAbar':  Particle('ghAbar',   0,      0,  1, 'ghA',   '0', -9000002,     0.0),
   'ghZ':     Particle('ghZ',      0,   'mZ',  1, 'ghZbar', 'wghZ',
                                                            9000003,     0.0),
   'ghZbar':  Particle('ghZbar',   0,   'mZ',  1, 'ghZ',    'wghZ',
                                                           -9000003,     0.0),
   'ghWp':    Particle('ghWp',     0,   'mW',  1, 'ghWpbar', 'wghWp',
                                                       9000004,     3.0),
   'ghWpbar': Particle('ghWpbar',  0,   'mW',  1, 'ghWp',    'wghWp',
                                                      -9000004,    -3.0),
   'ghWm':    Particle('ghWm',     0,   'mW',  1, 'ghWmbar', 'wghWm',
                                                       9000005,    -3.0),
   'ghWmbar': Particle('ghWmbar',  0,   'mW',  1, 'ghWm',    'wghWm',
                                                      -9000005,     3.0)
}
#---#] particles:
#---#[ mnemonics:
mnemonics = {
   'e+': particles['ep'],
   'e-': particles['em'],
   'positron': particles['ep'],
   'electron': particles['em'],
   'mu+': particles['mup'],
   'mu-': particles['mum'],
   'tau+': particles['taup'],
   'tau-': particles['taum'],
   'photon': particles['A'],
   'gamma': particles['A'],
   'W+': particles['Wp'],
   'W-': particles['Wm'],
   'gluon': particles['g'],
   'u': particles['U'],
   'u~': particles['Ubar'],
   'd': particles['D'],
   'd~': particles['Dbar'],
   'c': particles['C'],
   'c~': particles['Cbar'],
   's': particles['S'],
   's~': particles['Sbar'],
   'b': particles['B'],
   'b~': particles['Bbar'],
   't': particles['T'],
   't~': particles['Tbar'],
   'higgs': particles['H'],
   'h': particles['H'],
   'phi-': particles['phim'],
   'phi+': particles['phip'],
   'ne~': particles['nebar'],
   'nmu~': particles['nmubar'],
   'ntau~': particles['ntaubar']
}
#---#] mnemonics:
#---#[ parameters:
# Parameters from the Particle Data Booklet 2008
# see http://pdg.lbl.gov/
# <---- indicates deviations from the PDG table
# Masses in GeV
parameters = {
   'NC': '3.0',
   'gs': '1.0', # <----
   'me': '0.000510998910',
   'mmu': '0.105658367',
   'mtau': '1.77684',
   'mU': '0.0', # <----
   'mD': '0.0', # <----
   'mS': '0.104',
   'mC': '1.27',
   'mB': '4.20',
   'mBMS': '4.20', # MSbar mass used in Higgs coupling
   'mT': '171.2',
   'mH': '125.0', # <----
   # Widths <----
   'wB': '0.0',
   'wT': '0.0',
   'wZ': '2.4952',
   'wW': '2.124',
   'wtau': '0.0',
   'wchi': '0.0',
   'wphi': '0.0',
   'wH': '0.0',
   'wghZ': '0.0',
   'wghWp': '0.0',
   'wghWm': '0.0',
   # Number of flavours, not really a model parameter
   # but needed:
   'Nf': '5.0',
   'Nfgen': '-1.0'
}
#---#] parameters:
#---#[ latex_parameters:
latex_parameters = {
   'NC': 'N_C',
   'e': 'e',
   'alpha': "\\alpha",
   'GF': "G_F",
   'gs': 'g_s',
   'me': 'm_e',
   'mmu': 'm_\\mu',
   'mtau': 'm_\\tau',
   'mU': 'm_u', 'mD': 'm_d', 'mS': 'm_s', 'mC': 'm_c', 'mB': 'm_b',
   'mBMS': 'm_b^{MS}', 'mT': 'm_t',
   'mZ': 'm_Z', 'mW': 'm_W',
   'mH': 'm_H',
   'sw': 's_w',
   'cw': 'c_w',
   'wB': '\\Gamma_b', 'wT': '\\Gamma_t',
   'wZ': '\\Gamma_Z', 'wW': '\\Gamma_W',
   'wtau': '\\Gamma_\\tau',
   'wchi': '\\Gamma_\\chi',
   'wphi': '\\Gamma_\\phi',
   'wH': '\\Gamma_H',
   'wghZ': '\\Gamma_{u_Z}',
   'wghWp': '\\Gamma_{u_W^+}',
   'wghWm': '\\Gamma_{u_W^-}',
   'Nf': 'N_f',
   'Nfgen': 'N_f^{gen}',
   'NA': 'N_A',
   'Nfrat': 'N_f^{rat}',
   'gUv': 'v_u', 'gUa': 'a_u', 'gDv': 'v_d', 'gDa': 'a_d',
   'gCv': 'v_c', 'gCa': 'a_c', 'gSv': 'v_s', 'gSa': 'a_s',
   'gTv': 'v_t', 'gTa': 'a_t', 'gBv': 'v_b', 'gBa': 'a_b',
   'gnev': 'v_{\\nu_e}', 'gnea': 'a_{\\nu_e}',
   'gnmuv': 'v_{\\nu_\\mu}', 'gnmua': 'a_{\\nu_\\mu}',
   'gntauv': 'v_{\\nu_\\tau}', 'gntaua': 'a_{\\nu_\\tau}',
   'gev': 'v_e', 'gea': 'a_e',
   'gmuv': 'v_\\mu', 'gmua': 'a_\\mu', 'gtauv': 'v_\\tau',
   'gtaua': 'a_\\tau',
   'gWWZZ': 'g_{W^+W^-ZZ}', 'gWWAZ': 'g_{W^+W^-\\gamma Z}',
   'gWWAA': 'g_{W^+W^-\\gamma\\gamma}', 'gWWWW': 'g_{W^+W^-W^+W^-}',
   'gWWZ': 'g_{W^+W^-Z}',
   'gHHHH': 'g_{HHHH}', 'gXXXX': 'g_{\\chi\\chi\\chi\\chi}',
   'gHHXX': 'g_{HH\\chi\\chi}',
   'gHHPP': 'g_{HH\\phi^+\\phi^-}',
   'gXXPP': 'g_{\\chi\\chi\\phi^+\\phi^-}',
   'gPPPP': 'g_{\\phi^+\\phi^-\\phi^+\\phi^-',
   'gHHH': 'g_{HHH}',
   'gHXX': 'g_{H\\chi\\chi}',
   'gHPP': 'g_{H\\phi^+\\phi^-}',

   'gZZHH': 'g_{ZZHH}',
   'gZZXX': 'g_{ZZ\\chi\\chi}',
   'gWWHH': 'g_{W^+W^-HH}',
   'gWWXX': 'g_{W^+W^-\\chi\\chi}',
   'gWWPP': 'g_{W^+W^-\\phi^+\\phi^-}',
   'gAAPP': 'g_{\\gamma\\gamma\\phi^+\\phi^-}',
   'gAZPP': 'g_{\\gamma Z\\phi^+\\phi^-}',
   'gZZPP': 'g_{ZZ\\phi^+\\phi^-}',
   'gWAPH': 'g_{W^+A\\phi^-H}',
   'gWZPH': 'g_{W^+Z\\phi^-H}',
   'gWZPX': 'g_{W^+Z\\phi^-X}',
   'gWAPX': 'g_{W^+A\\phi^-X}',

   'gZXH': 'g_{ZH\\chi}',
   'gAPP': 'g_{\\gamma\\phi^+\\phi^-}',
   'gZPP': 'g_{Z\\phi^+\\phi^-}',
   'gWPH': 'g_{W^+\\phi^-H}',
   'gWPX': 'g_{W^+\\phi^-\\chi}',

   'gHZZ': 'g_{HZZ}',
   'gHWW': 'g_{HW^+W^-}',
   'gPWA': 'g_{\\phi^+W^-\\gamma}',
   'gPWZ': 'g_{\\phi^+W^-Z}',

   'gHU': 'y_{u}',
   'gHD': 'y_{d}',
   'gHC': 'y_{c}',
   'gHS': 'y_{s}',
   'gHB': 'y_{b}',
   'gHT': 'y_{t}',
   'gHe': 'y_{e}',
   'gHmu': 'y_{\\mu}',
   'gHtau': 'y_{\\tau}',
   'gXU': 'g_{u\\chi}',
   'gXD': 'g_{d\\chi}',
   'gXC': 'g_{c\\chi}',
   'gXS': 'g_{s\\chi}',
   'gXB': 'g_{b\\chi}',
   'gXT': 'g_{t\\chi}',
   'gXe': 'g_{e\\chi}',
   'gXmu': 'g_{\\mu\\chi}',
   'gXtau': 'g_{\\tau\\chi}',
   'gPU': 'g_{U\\phi}^\\pm',
   'gPD': 'g_{D\\phi^\\pm}',
   'gPC': 'g_{C\\phi^\\pm}',
   'gPS': 'g_{S\\phi^\\pm}',
   'gPB': 'g_{B\\phi^\\pm}',
   'gPT': 'g_{T\\phi^\\pm}',
   'gPe': 'g_{e\\phi^\\pm}',
   'gPmu': 'g_{\\mu\\phi^\\pm}',
   'gPtau': 'g_{\\tau\\phi^\\pm}',
   'gGWX': 'g_{\\chi u_{W^+}}',
   'gGWH': 'g_{H u_{W^+}}',
   'gGZH': 'g_{Hu_{Z}}',
   'gGZWP': 'g_{\\bar{u}_{Z}u_{W^\\pm}\\phi^{\\mp}}',
   'gGWZP': 'g_{\\bar{u}_{W^\\pm}u_{Z}\\phi^{\\mp}}',

   'gZ': 'g_Z',
   'gW': 'g_W'
}
#---#] latex_parameters:

#---#[ functions:
functions = {
   'NA': 'NC*NC-1',
   'gZ': '1/cw/sw',
   'gW': '1/sqrt2/sw',

   'gUv':    ' gZ*(1/4 - 2/3*sw^2)',
   'gCv':    ' gZ*(1/4 - 2/3*sw^2)',
   'gTv':    ' gZ*(1/4 - 2/3*sw^2)',

   'gDv':    '-gZ*(1/4 - 1/3*sw^2)',
   'gSv':    '-gZ*(1/4 - 1/3*sw^2)',
   'gBv':    '-gZ*(1/4 - 1/3*sw^2)',

   'gUa':    ' gZ*(1/4)',
   'gCa':    ' gZ*(1/4)',
   'gTa':    ' gZ*(1/4)',

   'gDa':    '-gZ*(1/4)',
   'gSa':    '-gZ*(1/4)',
   'gBa':    '-gZ*(1/4)',

   'gev':    '-gZ*(1/4 - sw^2)',
   'gmuv':   '-gZ*(1/4 - sw^2)',
   'gtauv':  '-gZ*(1/4 - sw^2)',

   'gnev':   ' gZ*(1/4)',
   'gnmuv':  ' gZ*(1/4)',
   'gntauv': ' gZ*(1/4)',

   'gea':    '-gZ*(1/4)',
   'gmua':   '-gZ*(1/4)',
   'gtaua':  '-gZ*(1/4)',

   'gnea':   ' gZ*(1/4)',
   'gnmua':  ' gZ*(1/4)',
   'gntaua': ' gZ*(1/4)',

   'gUl':    'gUv+gUa',
   'gCl':    'gCv+gCa',
   'gTl':    'gTv+gTa',

   'gDl':    'gDv+gDa',
   'gSl':    'gSv+gSa',
   'gBl':    'gBv+gBa',

   'gUr':    'gUv-gUa',
   'gCr':    'gCv-gCa',
   'gTr':    'gTv-gTa',

   'gDr':    'gDv-gDa',
   'gSr':    'gSv-gSa',
   'gBr':    'gBv-gBa',

   'gel':    'gev+gea',
   'gmul':    'gmuv+gmua',
   'gtaul':    'gtauv+gtaua',

   'ger':    'gev-gea',
   'gmur':    'gmuv-gmua',
   'gtaur':    'gtauv-gtaua',

   'gnel':    'gnev+gnea',
   'gner':    'gnev-gnea',

   'gnmul':    'gnmuv+gnmua',
   'gnmur':    'gnmuv-gnmua',

   'gntaul':    'gntauv+gntaua',
   'gntaur':    'gntauv-gntaua',

   'gWWZZ': '-(cw^2/sw^2)',
   'gWWAZ': ' (cw/sw)',
   'gWWAA': '-1',
   'gWWWW': ' (1/sw^2)',
   'gWWZ': '-(cw/sw)',

   'gHHHH': '- 3/(4*sw*sw) * mH*mH/mW/mW',
   'gXXXX': '- 3/(4*sw*sw) * mH*mH/mW/mW',
   'gHHXX': '- mH*mH/mW/mW/(4*sw*sw)',
   'gHHPP': '- mH*mH/mW/mW/(4*sw*sw)',
   'gXXPP': '- mH*mH/mW/mW/(4*sw*sw)',
   'gPPPP': '- 2*mH*mH/mW/mW/(4*sw*sw)',
   'gHHH': '- 3/2/sw * mH*mH/mW',
   'gHXX': '- 1/2/sw * mH*mH/mW',
   'gHPP': '- 1/2/sw * mH*mH/mW',

   'gZZHH': '1/2/cw/cw/sw/sw',
   'gZZXX': '1/2/cw/cw/sw/sw',
   'gWWHH': '1/2/sw/sw',
   'gWWXX': '1/2/sw/sw',
   'gWWPP': '1/2/sw/sw',
   'gAAPP': '2',
   'gAZPP': '- (cw*cw-sw*sw)/cw/sw',
   'gZZPP': '((cw*cw-sw*sw)/cw/sw)^2/2',
   'gWAPH': '- 1/2/sw',
   'gWZPH': '- 1/2/cw',
   'gWAPX': '- i_/2/sw',
   'gWZPX': '- i_/2/cw',

   'gZXH': '- i_/2/cw/sw',
   'gAPP': '-1',
   'gZPP': '(cw*cw-sw*sw)/(2*sw*cw)',
   'gWPH': '-1/2/sw',
   'gWPX': '-i_/2/sw',

   'gHZZ': '  mW/(cw^2*sw)',
   'gHWW': '  mW/sw',
   'gPWA': '- mW',
   'gPWZ': '- mW * sw/cw',

   'gHU': '- mU/mW / 2/sw',
   'gHD': '- mD/mW / 2/sw',
   'gHC': '- mC/mW / 2/sw',
   'gHS': '- mS/mW / 2/sw',
   'gHB': '- mBMS/mW / 2/sw',
   'gHT': '- mT/mW / 2/sw',
   'gHe': '- me/mW / 2/sw',
   'gHmu': '- mmu/mW / 2/sw',
   'gHtau': '- mtau/mW / 2/sw',
   'gXU': '- mU/mW * (+1/2)/sw',
   'gXD': '- mD/mW * (-1/2)/sw',
   'gXC': '- mC/mW * (+1/2)/sw',
   'gXS': '- mS/mW * (-1/2)/sw',
   'gXB': '- mBMS/mW * (-1/2)/sw',
   'gXT': '- mT/mW * (+1/2)/sw',
   'gXe': '- me/mW * (-1/2)/sw',
   'gXmu': '- mmu/mW * (-1/2)/sw',
   'gXtau': '- mtau/mW * (-1/2)/sw',
   'gPU': 'mU/mW/sqrt2/sw',
   'gPD': 'mD/mW/sqrt2/sw',
   'gPC': 'mC/mW/sqrt2/sw',
   'gPS': 'mS/mW/sqrt2/sw',
   'gPB': 'mBMS/mW/sqrt2/sw',
   'gPT': 'mT/mW/sqrt2/sw',
   'gPe': 'me/mW/sqrt2/sw',
   'gPmu': 'mmu/mW/sqrt2/sw',
   'gPtau': 'mtau/mW/sqrt2/sw',

   'gGWX': '- i_*mW/2/sw',
   'gGWH': '- mW/2/sw',
   'gGZH': '- mW/(2*cw*cw*sw)',
   'gGWZP': '- (cw*cw-sw*sw)/(2*cw*sw)*mW',
   'gGZWP': 'mW/(2*cw*sw)',

   'cw': '(mW/mZ)',

   'Nfrat': 'if(Nfgen,Nf/Nfgen,1)'
}
#---#] functions:
#---#[ types:
types = {
   'NC': 'R', 'gs': 'R',
   'me': 'R', 'mmu': 'R', 'mtau': 'R',
   'mU': 'R', 'mD': 'R', 'mS': 'R',
   'mC': 'R', 'mB': 'R', 'mT': 'R',
   'mH': 'R',
   'wB': 'R', 'wT': 'R', 'wtau': 'R',
   'wZ': 'R', 'wW': 'R', 'wH': 'R',
   'wghZ': 'R', 'wghWp': 'R', 'wghWm': 'R',
   'wchi': 'R', 'wphi': 'R',
   'cw': 'R',
   'mBMS': 'R',
   'Nf': 'R', 'Nfgen': 'R', 'NA': 'R',
   'Nfrat': 'R',
   'gUv': 'R', 'gUa': 'R', 'gDv': 'R', 'gDa': 'R',
   'gCv': 'R', 'gCa': 'R', 'gSv': 'R', 'gSa': 'R',
   'gTv': 'R', 'gTa': 'R', 'gBv': 'R', 'gBa': 'R',
   'gnev': 'R', 'gnea': 'R', 'gnmuv': 'R', 'gnmua': 'R',
   'gntauv': 'R', 'gntaua': 'R', 'gev': 'R', 'gea': 'R',
   'gmuv': 'R', 'gmua': 'R', 'gtauv': 'R', 'gtaua': 'R',
   'gUl': 'R', 'gUr': 'R', 'gDl': 'R', 'gDr': 'R',
   'gCl': 'R', 'gCr': 'R', 'gSl': 'R', 'gSr': 'R',
   'gTl': 'R', 'gTr': 'R', 'gBl': 'R', 'gBr': 'R',
   'gnel': 'R', 'gner': 'R', 'gnmul': 'R', 'gnmur': 'R',
   'gntaul': 'R', 'gntaur': 'R', 'gel': 'R', 'ger': 'R',
   'gmul': 'R', 'gmur': 'R', 'gtaul': 'R', 'gtaur': 'R',
   'gWWZZ': 'R', 'gWWAZ': 'R', 'gWWAA': 'R', 'gWWWW': 'R',
   'gWWZ': 'R',
   'gHHHH': 'R', 'gXXXX': 'R', 'gHHXX': 'R', 'gHHPP': 'R',
   'gXXPP': 'R', 'gPPPP': 'R', 'gHHH': 'R', 'gHXX': 'R', 'gHPP': 'R',
   'gZZHH': 'R', 'gZZXX': 'R', 'gWWHH': 'R', 'gWWXX': 'R', 'gWWPP': 'R',
   'gAAPP': 'R', 'gAZPP': 'R', 'gZZPP': 'R', 'gWAPH': 'R', 'gWZPH': 'R',
   'gWZPX': 'C', 'gWAPX': 'C',
   'gZXH': 'C', 'gAPP': 'R', 'gZPP': 'R', 'gWPH': 'R', 'gWPX': 'C',
   'gHZZ': 'R', 'gHWW': 'R', 'gPWA': 'R', 'gPWZ': 'R',
   'gHU': 'R', 'gHD': 'R', 'gHC': 'R', 'gHS': 'R', 'gHB': 'R',
   'gHT': 'R', 'gHe': 'R', 'gHmu': 'R', 'gHtau': 'R',
   'gXU': 'R', 'gXD': 'R', 'gXC': 'R', 'gXS': 'R', 'gXB': 'R',
   'gXT': 'R', 'gXe': 'R', 'gXmu': 'R', 'gXtau': 'R',
   'gPU': 'R', 'gPD': 'R', 'gPC': 'R', 'gPS': 'R', 'gPB': 'R',
   'gPT': 'R', 'gPe': 'R', 'gPmu': 'R', 'gPtau': 'R',
   'gGWX': 'C', 'gGWH': 'R', 'gGZH': 'R', 'gGWZP': 'R', 'gGZWP': 'R',

   'gZ': 'R', 'gW': 'R'
}
#---#] types:
#---#[ latex_names:
latex_names = {
   'U':       'u',
   'Ubar':    '\\bar{u}',
   'D':       'd',
   'Dbar':    '\\bar{d}',
   'S':       's',
   'Sbar':    '\\bar{s}',
   'C':       'c',
   'Cbar':    '\\bar{c}',
   'T':       't',
   'Tbar':    '\\bar{t}',
   'B':       'b',
   'Bbar':    '\\bar{b}',
   'gh':      'u_g',
   'ghbar':   '\\bar{u}_g',
   'g':       'g',
   'A':       '\\gamma',
   'Z':       'Z',
   'Wm':      'W^-',
   'Wp':      'W^+',

   'em':      'e^-',
   'ep':      'e^+',
   'ne':      '\\nu_e',
   'nebar':   '\\bar{\\nu}_e',

   'mum':     '\\mu^-',
   'mup':     '\\mu^+',
   'nmu':     '\\nu_\\mu',
   'nmubar':  '\\bar{\\nu}_\\mu',

   'taum':    '\\tau^-',
   'taup':    '\\tau^+',
   'ntau':    '\\nu_\\tau',
   'ntaubar': '\\bar{\\nu}_\\tau',

   'H':       'H',
   'phim':    '\\phi^-',
   'phip':    '\\phi^+',
   'chi':     '\\chi',

   'ghA':     'u_\\gamma',
   'ghAbar':  '\\bar{u}_\\gamma',
   'ghZ':     'u_Z',
   'ghZbar':  '\\bar{u}_Z',
   'ghWp':    'u_+',
   'ghWpbar': '\\bar{u}_+',
   'ghWm':    'u_-',
   'ghWmbar': '\\bar{u}_-'
}
#---#] latex_names:
#---#[ line_styles:
line_styles = {
   'U':       'fermion',
   'Ubar':    'fermion',
   'D':       'fermion',
   'Dbar':    'fermion',
   'S':       'fermion',
   'Sbar':    'fermion',
   'C':       'fermion',
   'Cbar':    'fermion',
   'T':       'fermion',
   'Tbar':    'fermion',
   'B':       'fermion',
   'Bbar':    'fermion',
   'gh':      'ghost',
   'ghbar':   'ghost',
   'g':       'gluon',
   'A':       'photon',
   'Z':       'photon',
   'Wm':      'photon',
   'Wp':      'photon',

   'em':      'fermion',
   'ep':      'fermion',
   'ne':      'fermion',
   'nebar':   'fermion',

   'mum':     'fermion',
   'mup':     'fermion',
   'nmu':     'fermion',
   'nmubar':  'fermion',

   'taum':    'fermion',
   'taup':    'fermion',
   'ntau':    'fermion',
   'ntaubar': 'fermion',

   'H':       'scalar',
   'phim':    'scalar',
   'phip':    'scalar',
   'chi':     'scalar',

   'ghA':     'ghost',
   'ghAbar':  'ghost',
   'ghZ':     'ghost',
   'ghZbar':  'ghost',
   'ghWp':    'ghost',
   'ghWpbar': 'ghost',
   'ghWm':    'ghost',
   'ghWmbar': 'ghost'
}
#---#] line_styles:
#---#[ slha_locations:
slha_locations = {
   'mD': ('MASS', [1]),
   'mU': ('MASS', [2]),
   'mS': ('MASS', [3]),
   'mC': ('MASS', [4]),
   'mB': ('MASS', [5]),
   'mT': ('MASS', [6]),
   'me': ('MASS', [11]),
   'mmu': ('MASS', [13]),
   'mtau': ('MASS', [15]),
   'mZ': ('MASS', [23]),
   'mW': ('MASS', [24]),
   'mH': ('MASS', [25]),
   'wB': ('DECAY', [5]),
   'wT': ('DECAY', [6]),
   'wtau': ('DECAY', [15]),
   'wZ': ('DECAY', [23]),
   'wW': ('DECAY', [24]),
   'wH': ('DECAY', [25]),
   'wchi': ('DECAY', [250]),
   'wphi': ('DECAY', [251]),
   'wghZ': ('DECAY', [9000003]),
   'wghWp': ('DECAY', [9000004]),
   'wghWm': ('DECAY', [9000005]),
}
#---#] slha_locations:

#---#[ def init_ew:
def init_ew(e_one=False,**options):
   """
   Produce entries in parameters and functions starting from the
   given initial values.

   Reference Formulae:

   GF / sqrt(2) = alpha * pi / 2 / mW^2 / sw^2
                = e^2 / 8 / mW^2 / sw^2
        sw^2 = 1 - mW^2 / mZ^2

   We have access to the "user_choice" from options
   and if any parameters were specified we determine
   gosam_choice from the input parameters

   Then we compare...

   """
   global parameters, functions, types
   keys = set(options.keys())
   for key in keys:
      parameters[key] = str(options[key])
      types[key] = "R"

   if keys == set(["GF", "mW", "mZ"]):
      # mW, mZ --> sw
      functions["sw"] = "sqrt(1-mW*mW/mZ/mZ)"
      types["sw"] = "R"
      # GF, mW, sw --> e
      functions["e"] = "mW*sw*sqrt(8*GF/sqrt(2))"
      types["e"] = "R"
   elif keys == set(["alpha", "mW", "mZ"]):
      # alpha --> e
      functions["e"] = "sqrt(4*pi*alpha))"
      types["e"] = "R"
      # mW, mZ --> sw
      functions["sw"] = "sqrt(1-mW*mW/mZ/mZ)"
      types["sw"] = "R"
   elif keys == set(["alpha", "sw", "mZ"]):
      # alpha --> e
      functions["e"] = "sqrt(4*pi*alpha))"
      types["e"] = "R"
      # sw, mZ --> mW
      functions["mW"] = "mZ*sqrt(1-sw*sw)"
      types["mW"] = "R"
   elif keys == set(["alpha", "sw", "GF"]):
      # alpha --> e
      functions["e"] = "sqrt(4*pi*alpha))"
      types["e"] = "R"
      # GF, sw, alpha --> mW
      functions["mW"] = "sqrt(alpha*pi/sqrt(2)/GF) / sw"
      types['mW'] = 'R'
      # mW, sw --> mZ
      functions["mZ"] = "mW / sqrt(1-sw*sw)"
      types["mZ"] = "R"
   elif keys == set(["alpha", "GF", "mZ"]):
      # alpha --> e
      functions["e"] = "sqrt(4*pi*alpha))"
      types["e"] = "R"
      # GF, mZ, alpha --> mW
      functions["mW"] = "sqrt(mZ*mZ/2+sqrt(mZ*mZ*mZ*mZ/4-pi*alpha*mZ*mZ/sqrt(2)/GF))"
      types["mW"] = "R"
      # mW, mZ --> sw
      functions["sw"] = "sqrt(1-mW*mW/mZ/mZ)"
      types["sw"] = "R"
   elif keys == set(["e", "mW", "mZ"]):
      # mW, mZ --> sw
      functions["sw"] = "sqrt(1-mW*mW/mZ/mZ)"
      types["sw"] = "R"
   elif keys == set(["e", "sw", "mZ"]):
      # mZ, sw --> mW
      functions["mW"] = "mZ*sqrt(1-sw*sw)"
      types["mW"] = "R"
   elif keys == set(["e", "sw", "GF"]):
      # e, sw, GF --> mW
      functions["mW"] = "e/2/sw/sqrt(sqrt(2)*GF)"
      types["mW"] = "R"
      # mW, sw --> mZ
      functions["mZ"] = "mW / sqrt(1-sw*sw)"
      types["mZ"] = "R"
   elif keys == set(["e", "sw", "GF", "mZ", "mW", "alpha"]):
      for dummy in ["e", "sw", "GF", "mZ", "mW", "alpha"]:
         #   parameters[dummy] = '0.0'
         functions['%sf' % dummy ] = dummy
         types[dummy] = "R"
         types['%sf' % dummy] = "R"
         #try:
         #   del slha_locations[dummy]
         #except:
         #   continue
   else:
      raise Exception("Invalid EW Scheme.")
   if e_one:
      if "e" in list(functions.keys()):
         functions["e"] = "1"
#---#] def init_ew:
#---#[ def ew_gosam_choice:

def ew_gosam_choice(keys, size_set):
   """
      Returns GoSam's prefered choice of electroweak scheme based on the
      input parameters in "keys"

      The values are 1-8, with the special results
       0 : no parameters specified
      -1 : less than 3 parameters specified (so a unique choice
           cannot be made)
      -2 : more than 3 parameters specified (so a unique choice
           cannot be made)
   """
   # is it one of these distince choices?
   if keys == set(["GF", "mW", "mZ"]):
      gosam_choice = 1
   elif keys == set(["alpha", "mW", "mZ"]):
      gosam_choice = 2
   elif keys == set(["alpha", "sw", "mZ"]):
      gosam_choice = 3
   elif keys == set(["alpha", "sw", "GF"]):
      gosam_choice = 4
   elif keys == set(["alpha", "GF", "mZ"]):
      gosam_choice = 5
   elif keys == set(["e", "mW", "mZ"]):
      gosam_choice = 6
   elif keys == set(["e", "sw", "mZ"]):
      gosam_choice = 7
   elif keys == set(["e", "sw", "GF"]):
      gosam_choice = 8
   elif size_set == 0:
      gosam_choice = 0
   elif size_set < 3 and size_set > 0:
      gosam_choice = -1
   elif size_set > 3:
      gosam_choice = -2
   else:
      raise Exception("Invalid EW Scheme input by user.")
   return gosam_choice
#---#] def ew_gosam_choice:
#---#] def init:

def init():
   """

   We choose which electroweak scheme to follow here. The decision is based
   on what is specified in the model.options line in the input cared
   (for models sm only). These parameters are:

   PARAMETERS:

   1. gosam_choice : the ew_scheme that gosam would choose based on the input
   parameters given in model.option (e.g. mZ=X,mW=Y,alpha=Z => gosam_choice=2)
   2. user_choice  : the ew_scheme the user chose i.e. ewchoose=n
   This is 0 if ewchoose is specified without a number
   3. ewchoose     : A boolean value, True means a choice
   of ew scheme as specified in the file config.f90

   """
   from golem.model.particle import simplify_model
   from golem.model import MODEL_OPTIONS, MODEL_ONES
   global particles, parameters, types, functions

   ew_input = {}

   masses = None
   widths = None

   DEFAULT={}
   DEFAULT['mZ'] = 91.1876
   DEFAULT['mW'] = 80.376
   DEFAULT['alpha'] = 1.0/137.035999679
   DEFAULT['GF'] = 1.16637E-05
   DEFAULT['sw'] = sqrt(0.23120)
   DEFAULT['e'] =  0.3028221202

   keys = MODEL_OPTIONS

   icount = 0
   for key, value in list(MODEL_OPTIONS.items()):
      if key in ["mZ", "mW", "alpha", "GF", "e", "sw"]:
         ew_input[key] = value
         icount += 1

   input_params = set(ew_input.keys())

   ones=golem.model.MODEL_ONES
   eone = False

   gosam_choice = int(ew_gosam_choice(input_params, icount))
   user_choice = int(keys["users_choice"])
   ewchoose = keys["ewchoose"]
   param=""

   logger.debug("GS: %r" % gosam_choice)
   logger.debug("user: %r" % user_choice)
   logger.debug("ewchoose: %r" % ewchoose)

   for item in list(DEFAULT.keys()):
      if item in ones:
         if item != "e":
            raise Exception("%s is set to one: GoSam cannot handle this EW Scheme" % item)
         else:
            eone = True

   if ewchoose:
      # Substitute parameters from user and fill gaps with defaults once
      for key in ["mZ", "mW", "alpha", "GF", "e", "sw"]:
         if key in list(MODEL_OPTIONS.keys()):
            ew_input[key] = MODEL_OPTIONS[key]
            param+= "%s = %s\n"  % (key, MODEL_OPTIONS[key])
         else:
            ew_input[key] = DEFAULT[key]
      if user_choice != 0:
         warn = "EW scheme was set to ewchoose = %s\n" % user_choice
         warn+= "You specified the following EW parameters:\n"
         if len(param)== 0:
            param = "None!\n"
         warn+= param
         warn+= "We trust you know what you are doing ;-).\n"
         logger.warning(warn)
   else:
      if gosam_choice == 0:
         for key in ["mZ","mW","alpha"]:
            ew_input[key] = DEFAULT[key]
      elif gosam_choice == -1:
         # Substitute parameters from user and fill gaps with defaults once
         for key in ["mZ", "mW", "alpha", "GF", "e", "sw"]:
            if key in list(MODEL_OPTIONS.keys()):
               ew_input[key] = MODEL_OPTIONS[key]
               param+= "%s = %s\n"  % (key, MODEL_OPTIONS[key])
            else:
               ew_input[key] = DEFAULT[key]
         keys["ewchoose"] = True
         keys["users_choice"] = '2'
         warn = "EW scheme under-specified.\n"
         warn+= "The number of EW parameters does not allow to select\n"
         warn+= "an EW-scheme. You specified:\n"
         warn+= param
         warn+= "EW parameters are computed from:\n"
         warn+= "mW, mZ, alpha.\n"
         warn+= "This can be changed editing ewchoice in common/config.f90.\n"
         logger.warning(warn)
      elif gosam_choice == -2:
         # Substitute parameters from user and fill gaps with defaults once
         for key in ["mZ", "mW", "alpha", "GF", "e", "sw"]:
            if key in list(MODEL_OPTIONS.keys()):
               ew_input[key] = MODEL_OPTIONS[key]
               param+= "%s = %s\n"  % (key, MODEL_OPTIONS[key])
            else:
               ew_input[key] = DEFAULT[key]
         keys["ewchoose"] = True
         keys["users_choice"] = '2'
         warn = "EW scheme over-specified.\n"
         warn+= "The number of EW parameters does not allow to select\n"
         warn+= "an EW-scheme. You specified:\n"
         warn+= param
         warn+= "EW parameters are computed from:\n"
         warn+= "mW, mZ, alpha.\n"
         warn+= "This can be changed editing ewchoice in common/config.f90.\n"
         logger.warning(warn)

   for key, value in list(MODEL_OPTIONS.items()):
      if key in parameters:
         try:
            sval = str(value)
            fval = float(sval)
            parameters[key] = sval
         except ValueError:
            logger.warning(
            "Model option %s=%r not in allowed range.\n" % (key, value) +
            "Option ignored")

      elif key.lower() == "masses":
         if value.strip().lower() == "none":
            masses = []
         else:
            masses = value.split()
      elif key.lower() == "widths":
         if value.strip().lower() == "none":
            widths = []
         else:
            widths = value.split()
   simplify_model(particles, parameters, types, functions, masses, widths)
   init_ew(e_one=eone,**ew_input)
#---#] def init:
init()
