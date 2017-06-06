# vim: ts=4:sw=4:expandtab
"""
Create the input for SecDec to compute the master integrals

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

parser.add_argument("-r", "--run-card", dest="run_card_template_file",
                    action="store", type=str, required=True,
                    help="the template for the secdec run card",
                    metavar="INFILE")

parser.add_argument("-k", "--kinematics", dest="kinematics_template_file",
                    action="store", type=str, required=True,
                    help='the template for the file storing the kinematics',
                    metavar="INFILE")

parser.add_argument("-p", "--pysecdec", dest="pysecdec_template_file",
                    action="store", type=str, required=True,
                    help='the template file for pysecdec',
                    metavar="INFILE")

parser.add_argument("-a", "--amplitude", dest="amplitude_template_file",
                    action="store", type=str, required=True,
                    help='the template file for storing the amplitude',
                    metavar="INFILE")

parser.add_argument("-i", "--integral-prefix", dest="integral_prefix",
                    action="store", type=str, required=True,
                    help="the prefix of the files with the master integrals",
                    metavar="INFILE")

parser.add_argument("-s", "--integral-suffix", dest="integral_suffix",
                    action="store", type=str, required=True,
                    help="the suffix of the files with the master integrals",
                    metavar="INFILE")

parser.add_argument("-o", "--outpath", dest="outpath",
                    action="store", type=str, required=True,
                    help="the directory for the output",
                    metavar="OUTPATH")

args = parser.parse_args()


# load input

with open(args.run_card_template_file, 'r') as f:
   run_card_template = f.read()

with open(args.kinematics_template_file, 'r') as f:
   kinematics_template = f.read()

with open(args.pysecdec_template_file, 'r') as f:
   pysecdec_template = f.read()

with open(args.amplitude_template_file, 'r') as f:
   amplitude_template = f.read()

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

# create output directory if necessary
import os, errno
try:
    os.makedirs(args.outpath)
except OSError as error:
    if error.errno != errno.EEXIST:
      raise error

coefficient_include_list = []
integral_include_list = []
amplitude_term_list = []
code_form = []

# parse the individual integrals
for integral, epsord in integrals_epsorders.items():
    name, tidrs, powerlist, proplist = integral.split(',[],')

    # Remove "PropList(...)" and "PropVec" from the list of propagators.
    # These are just introduced to prevent form from expanding the
    # squares.
    proplist = proplist.replace("PropList(", '').replace("PropVec", '')
    assert proplist.endswith(')')
    proplist = proplist[:-1]
    proplist = "'" + proplist.replace("^", "**").replace("," , "','") + "'"

    graph = name + "pow" + powerlist.replace(',', '_')

    integral_t, integral_id, integral_r, integral_s, = tidrs.split(',')

    # check for integral in shifted dimensions
    dim=4
    dimRegex = re.findall('dim(inc|dec)(\d+)',name)
    if dimRegex:
        assert len(dimRegex)==1
        if dimRegex[0][0]=='inc':
           dim += int(dimRegex[0][1])
        else:
           dim -= int(dimRegex[0][1])

    # Generate name of integral for use in FORM, cpp code
    name_cpp = name + "pow" + powerlist.replace(',','_').replace('-','m')

    # generate coefficient include statement for amplitude
    coefficient_include_list.append('#include "coefficient_' + name_cpp + '.hpp"')

    # generate integral include statement for amplitude
    integral_include_list.append('#include "' + name_cpp + '.hpp"')

    # generate amplitude term declaration for amplitude
    amplitude_term_list.append('{ integral_coefficients::' + name_cpp + ', ' + name_cpp + '::prefactor' + ', ' + name_cpp + '::make_integrands }')

    # generate FORM code
    code_form.append("Id INT(" + name + ',' + tidrs + ',[],' + powerlist + ",[],sDUMMY1?) = factoutscale^( (" + str(dim) + "/2) * `LOOPS' - " + str(integral_r) + " + " + str(integral_s) + ") * INTDIMLESS(" + name_cpp +  ");")

    # write SecDec kinematics file and run card
    kinematics_outfile = os.path.join(args.outpath, graph + '.m')
    with open(kinematics_outfile, 'w') as f:
      f.write(kinematics_template % locals())

    rc_outfile = os.path.join(args.outpath, graph + '.input')
    with open(rc_outfile, 'w') as f:
      f.write(run_card_template % locals())

    pysecdec_outfile = os.path.join(args.outpath, graph + '.py')
    with open(pysecdec_outfile, 'w') as f:
      f.write(pysecdec_template % locals())


coefficient_includes = '\n'.join(coefficient_include_list)
integral_includes = '\n'.join(integral_include_list)
amplitude_terms = ',\n    '.join(amplitude_term_list)

# write a FORM file that replaces
# INT(<family name>,[],t,ID,r,s,[],<power list>,[],...) by INT(<family name>pow<power list where "-" -> m and "," -> _>)
form_outfilename = os.path.join(args.outpath, 'secdec_replace_integrals.hh')
with open(form_outfilename, 'w') as f:
    f.write('\n'.join(code_form))

amplitude_outfilename = args.amplitude_template_file
with open(amplitude_outfilename, 'w') as f:
    f.write(amplitude_template % locals())
