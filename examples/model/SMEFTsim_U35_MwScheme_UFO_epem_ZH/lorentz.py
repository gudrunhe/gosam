# This file was automatically created from UFO model SMEFTsim_U35_MwScheme_UFO
# by applying the 'modify_UFO.py' script. Only SM vertices and those containing
# one of the following coefficients have been kept:
# cHW  cHB  cHWB 


from object_library import all_lorentz, Lorentz

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot
try:
   import form_factors as ForFac
except ImportError:
   pass


VVV5 = Lorentz(name = 'VVV5',
	spins = [ 3, 3, 3 ],
	structure = 'P(3,1)*Metric(1,2) - P(3,2)*Metric(1,2) - P(2,1)*Metric(1,3) + P(2,3)*Metric(1,3) + P(1,2)*Metric(2,3) - P(1,3)*Metric(2,3)')

VVV6 = Lorentz(name = 'VVV6',
	spins = [ 3, 3, 3 ],
	structure = 'P(3,2)*Metric(1,2) - P(2,3)*Metric(1,3) - P(1,2)*Metric(2,3) + P(1,3)*Metric(2,3)')

VVV4 = Lorentz(name = 'VVV4',
	spins = [ 3, 3, 3 ],
	structure = 'P(3,1)*Metric(1,2) - P(3,2)*Metric(1,2) - P(2,1)*Metric(1,3) + P(1,2)*Metric(2,3)')

VVVV1 = Lorentz(name = 'VVVV1',
	spins = [ 3, 3, 3, 3 ],
	structure = 'Metric(1,4)*Metric(2,3) - Metric(1,3)*Metric(2,4)')

VVVV9 = Lorentz(name = 'VVVV9',
	spins = [ 3, 3, 3, 3 ],
	structure = 'Metric(1,4)*Metric(2,3) - Metric(1,2)*Metric(3,4)')

VVVV10 = Lorentz(name = 'VVVV10',
	spins = [ 3, 3, 3, 3 ],
	structure = 'Metric(1,3)*Metric(2,4) - Metric(1,2)*Metric(3,4)')

VVVV8 = Lorentz(name = 'VVVV8',
	spins = [ 3, 3, 3, 3 ],
	structure = 'Metric(1,4)*Metric(2,3) + Metric(1,3)*Metric(2,4) - 2*Metric(1,2)*Metric(3,4)')

VVVV11 = Lorentz(name = 'VVVV11',
	spins = [ 3, 3, 3, 3 ],
	structure = 'Metric(1,4)*Metric(2,3) - (Metric(1,3)*Metric(2,4))/2. - (Metric(1,2)*Metric(3,4))/2.')

VVSS4 = Lorentz(name = 'VVSS4',
	spins = [ 3, 3, 1, 1 ],
	structure = 'P(1,2)*P(2,1) - P(-1,1)*P(-1,2)*Metric(1,2)')

VVS4 = Lorentz(name = 'VVS4',
	spins = [ 3, 3, 1 ],
	structure = 'P(1,2)*P(2,1) - P(-1,1)*P(-1,2)*Metric(1,2)')

VVSS3 = Lorentz(name = 'VVSS3',
	spins = [ 3, 3, 1, 1 ],
	structure = 'Metric(1,2)')

VVS3 = Lorentz(name = 'VVS3',
	spins = [ 3, 3, 1 ],
	structure = 'Metric(1,2)')

VVVSS4 = Lorentz(name = 'VVVSS4',
	spins = [ 3, 3, 3, 1, 1 ],
	structure = 'P(3,1)*Metric(1,2) - P(2,1)*Metric(1,3)')

VVVSS6 = Lorentz(name = 'VVVSS6',
	spins = [ 3, 3, 3, 1, 1 ],
	structure = 'P(3,1)*Metric(1,2) - P(3,2)*Metric(1,2) - P(2,1)*Metric(1,3) + P(2,3)*Metric(1,3) + P(1,2)*Metric(2,3) - P(1,3)*Metric(2,3)')

VVVS4 = Lorentz(name = 'VVVS4',
	spins = [ 3, 3, 3, 1 ],
	structure = 'P(3,1)*Metric(1,2) - P(2,1)*Metric(1,3)')

VVVS6 = Lorentz(name = 'VVVS6',
	spins = [ 3, 3, 3, 1 ],
	structure = 'P(3,1)*Metric(1,2) - P(3,2)*Metric(1,2) - P(2,1)*Metric(1,3) + P(2,3)*Metric(1,3) + P(1,2)*Metric(2,3) - P(1,3)*Metric(2,3)')

VVVSS5 = Lorentz(name = 'VVVSS5',
	spins = [ 3, 3, 3, 1, 1 ],
	structure = 'P(2,3)*Metric(1,3) - P(1,3)*Metric(2,3)')

VVVS5 = Lorentz(name = 'VVVS5',
	spins = [ 3, 3, 3, 1 ],
	structure = 'P(2,3)*Metric(1,3) - P(1,3)*Metric(2,3)')

SSSS1 = Lorentz(name = 'SSSS1',
	spins = [ 1, 1, 1, 1 ],
	structure = '1')

SSS1 = Lorentz(name = 'SSS1',
	spins = [ 1, 1, 1 ],
	structure = '1')

VVVVSS2 = Lorentz(name = 'VVVVSS2',
	spins = [ 3, 3, 3, 3, 1, 1 ],
	structure = 'Metric(1,4)*Metric(2,3) + Metric(1,3)*Metric(2,4) - 2*Metric(1,2)*Metric(3,4)')

VVVVS6 = Lorentz(name = 'VVVVS6',
	spins = [ 3, 3, 3, 3, 1 ],
	structure = 'Metric(1,4)*Metric(2,3) + Metric(1,3)*Metric(2,4) - 2*Metric(1,2)*Metric(3,4)')

VVVVSS5 = Lorentz(name = 'VVVVSS5',
	spins = [ 3, 3, 3, 3, 1, 1 ],
	structure = 'Metric(1,4)*Metric(2,3) - (Metric(1,3)*Metric(2,4))/2. - (Metric(1,2)*Metric(3,4))/2.')

VVVVS9 = Lorentz(name = 'VVVVS9',
	spins = [ 3, 3, 3, 3, 1 ],
	structure = 'Metric(1,4)*Metric(2,3) - (Metric(1,3)*Metric(2,4))/2. - (Metric(1,2)*Metric(3,4))/2.')

FFV1 = Lorentz(name = 'FFV1',
	spins = [ 2, 2, 3 ],
	structure = 'Gamma(3,2,1)')

FFV3 = Lorentz(name = 'FFV3',
	spins = [ 2, 2, 3 ],
	structure = 'Gamma(3,2,-1)*ProjM(-1,1)')

FFS2 = Lorentz(name = 'FFS2',
	spins = [ 2, 2, 1 ],
	structure = 'Identity(2,1)')

