# vim: ts=3:sw=3:expandtab
"""
Create the input for SecDec to compute the master integrals

"""

import os
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

parser.add_argument("-i", "--integrals", dest="integrals_file",
                    action="store", type=str, required=True,
                    help="the file with the master integrals",
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

with open(args.integrals_file, 'r') as f:
   integrals = f.read()


# convert form sum of integrals into python list

# strip trailing "+"
if integrals.startswith("+"):
   integrals = integrals[1:]

# remove whitespaces and newline characters
integrals = integrals.replace('\n','').replace(' ','')

# The string "integrals" should now start with "INT(..."
assert integrals.startswith("INT(")
# remove the first "INT(" to avoid the first element
# to be the empty string when invoking "split"
integrals = integrals[4:]

# generate a list with the expressions inside of "INT(...)"
# strip the left parentheses
integrals = integrals.split("INT(")
# strip the right parentheses, the plusses between "INT(...)", and the trailing ";"
integrals = [i[:i.rindex(')')] for i in integrals]


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


# create output directory if necessary
import os, errno
try:
   os.makedirs(args.outpath)
except OSError as error:
   if error.errno != errno.EEXIST:
      raise error


# as part of the output, write a form file that replaces
#    INT(<family name>,[],t,ID,r,s,[],<power list>,[],...)
# by <family name>pow<power list where "-" -> m and "," -> _>
form_outfilename = os.path.join(args.outpath, 'secdec_replace_integrals.hh')
with open(form_outfilename, 'w') as form_outfile:

   # parse the individual integrals
   for integral in integrals:
      name, tidrs, powerlist, epsord, proplist = integral.split(',[],')

      # Remove "PropList(...)" and "PropVec" from the list of propagators.
      # These are just introduced to prevent form from expanding the
      # squares.
      proplist = proplist.replace("PropList(", '').replace("PropVec", '')
      assert proplist.endswith(')')
      proplist = proplist[:-1]

      graph = name + "pow" + powerlist.replace(',', '_')

      kinematics_outfile = os.path.join(args.outpath, graph + '.m')
      rc_outfile = os.path.join(args.outpath, graph + '.input')

      # write SecDec kinematics file and run card
      with open(kinematics_outfile, 'w') as f:
         f.write(kinematics_template % locals())

      with open(rc_outfile, 'w') as f:
         f.write(run_card_template % locals())

      form_outfile.write("Id INT(" + name + ',' + tidrs + ',[],' + powerlist + ") = " + name + "pow" + powerlist.replace(',','_').replace('-','m') +  ";\n")

