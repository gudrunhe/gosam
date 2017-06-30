# vim: ts=4:sw=4:expandtab
"""
Create the coefficient header files

"""

import os
import re
from glob import iglob
try:
    from itertools import ifilterfalse as filterfalse
except ImportError:
    from itertools import filterfalse
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--integral-prefix", dest="integral_prefix",
                    action="store", type=str, required=True,
                    help="the prefix of the files with the master integrals",
                    metavar="INFILE")

parser.add_argument("-s", "--integral-suffix", dest="integral_suffix",
                    action="store", type=str, required=True,
                    help="the suffix of the files with the master integrals",
                    metavar="INFILE")

parser.add_argument("-p", "--projectors", dest="number_of_projectors",
                    action="store", type=int, required=True,
                    help="the number of projectors in the amplitude",
                    metavar="NUMPROJ")

parser.add_argument("-c", "--colors", dest="number_of_colors",
                    action="store", type=int, required=True,
                    help="the number of color projectors in the amplitude",
                    metavar="NUMCOL")

parser.add_argument("-o", "--outpath", dest="outpath",
                    action="store", type=str, required=True,
                    help="the directory for the output",
                    metavar="OUTPATH")

args = parser.parse_args()

# load input

integrals = []
for filename in iglob(args.integral_prefix + '*' + args.integral_suffix):
    with open(filename, 'r') as f:
        integrals.append( f.read() )

# convert form sum of integrals into python list

# strip trailing "+"
for i,integral in enumerate(integrals):
    if integral.startswith("+"):
        integral = integral[1:]

    # remove whitespaces and newline characters
    integrals[i] = integral.replace('\n','').replace(' ','')

integrals_out = []
for integral in filterfalse(lambda x: x == '0', integrals):
    # The string "integral" should now start with "INT(..."
    assert integral.startswith("INT(")
    integrals_out.append( integral[4:integral.rindex(')')] )
integrals = integrals_out
del integrals_out

# now the elements of integrals are expected to have the format:
"""
<family name>,[],t,ID,r,s,[],<power list>,[],<epsord>,[],
PropList(-<some mass>^2+PropVec(<some lorentz vector>)^2,<possibly more propagators>)
"""
# example:
"""
ReduzeT1L1,[],2,5,2,0,[],1,0,1,0,[],1,[],PropList(-mT^2+PropVec(p1)^2,\
-mT^2+PropVec(p1-k1)^2,-mT^2+PropVec(p1-k1-k2)^2,-mT^2+PropVec(p1-k1-k2-k3)^2)
"""

# keep only the highest "epsord"
integrals_epsorders = dict()
for integral in integrals:
    name, tidrs, powerlist, epsord, proplist = integral.split(',[],')
    id = ',[],'.join([name, tidrs, powerlist, proplist])
    try:
        integrals_epsorders[id] = max(integrals_epsorders[id], epsord)
    except KeyError:
        integrals_epsorders[id] = epsord

# parse the individual integrals
for integral, epsord in integrals_epsorders.items():
    name, tidrs, powerlist, proplist = integral.split(',[],')

    coefficient_name =  name + 'pow' + powerlist.replace(',','_').replace('-','m')

    # write coefficient header files
    coefficient_header_outfile = os.path.join(args.outpath, 'coefficient_' + coefficient_name + '.hpp')
    with open(coefficient_header_outfile, 'w') as f:
        f.write('#ifndef ' + 'coefficient_' + coefficient_name + '_hpp_included\n')
        f.write('#define ' + 'coefficient_' + coefficient_name + '_hpp_included\n')
        f.write('\n')
        f.write('#include "../../../typedef.hpp"\n')
        f.write('')
        for p in range(1, args.number_of_projectors + 1):
            for c in range(1, args.number_of_colors + 1):
                f.write('#include "coefficient_' + coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '.hpp"\n')
        f.write('\n')
        f.write('namespace integral_coefficients {\n')
        f.write('\t' + 'coeffs_func_series_t ' + coefficient_name + '\n')
        f.write('\t{\n')
        lines = []
        for p in range(1, args.number_of_projectors + 1):
            color_lines = []
            for c in range(1, args.number_of_colors + 1):
                color_lines.append(coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c))
            lines.append(','.join(color_lines))
        line = "},\n\t\t{".join(lines)
        f.write('\t\t{' + line + '}\n')
        f.write('\t};\n')
        f.write('};\n')
        f.write('\n')
        f.write("#endif\n")

    # write placeholder coefficient files (setting coefficients to 0, to be overwritten by form)
    for p in range(1, args.number_of_projectors + 1):
        for c in range(1, args.number_of_colors + 1):
            coefficient_outfile = os.path.join(args.outpath, 'coefficient_' + coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '.hpp')
            with open(coefficient_outfile, 'w') as f:
                f.write('#ifndef coefficient_' + coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '_hpp_included\n')
                f.write('#define coefficient_' + coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '_hpp_included\n')
                f.write('\n')
                f.write('#include "../../../typedef.hpp"\n')
                f.write('\n')
                f.write('namespace integral_coefficients {\n')
                f.write('\n')
                f.write('coeff_return_t ' + coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '_ord0(invariants_t invariants,parameters_t parameters)\n')
                f.write('{\n')
                f.write('\treturn {0.};\n')
                f.write('};\n')
                f.write('\n')
                f.write('coeff_func_series_t ' + coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '\n')
                f.write('{\n')
                f.write('/*\n')
                f.write(' * Set order in epsS to largest int in order to avoid truncation:\n')
                f.write(' * "((1/eps + O(eps^0)) * 0*eps^0 + O(eps) = O(eps^0)" but "((1/eps + O(eps^0)) * 0*eps + O(eps) = O(eps)"\n')
                f.write(' * Note: Setting the order to "std::numeric_limits<int>::max()" overflows "int" when multiplying Series together.\n')
                f.write(' */\n')
                f.write('100000, // Minimum epsS order\n')
                f.write('100000, // Maximum epsS order\n')
                f.write('{\n')
                f.write(coefficient_name + '_ProjLabel' + str(p) + '_c' + str(c) + '_ord0\n')
                f.write('},\n')
                f.write('false,\n')
                f.write('"eps"\n')
                f.write('};\n')
                f.write('\n')
                f.write('};\n')
                f.write('\n')
                f.write('#endif')
