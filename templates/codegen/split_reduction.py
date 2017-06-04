# vim: ts=3:sw=3:expandtab

import re
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-r", "--reduction", dest="reduction",
                    action="store", type=str, required=True,
                    help='reduction input file', metavar="REDUCTION")

parser.add_argument("-c", "--coeff", dest="coeff",
                    action="store", type=str, required=True,
                    help='prefix used for coefficient labels ',
                    metavar="COEFF")

parser.add_argument("-s", "--suffix", dest="suffix",
                    action="store", type=str, required=True,
                    help='suffix used for output files',
                    metavar="SUFFIX")

args = parser.parse_args()

#
# Takes a Reduction in Reduze FORM style
#  - Splits every coefficient into numerator and denominator and stores them in separate expressions
#  - Writes the reduction rule with the coefficients replaced by labels
#
# Example Input (produced by Reduze):
"""
id INT(F1x23,7,319,7,1,[],1,1,1,1,1,1,0,-1,1) =
  + INT(F1x23,6,317,7,2,[],1,0,1,1,1,1,-1,-1,2)
    * (es12*Den(mH^2-es23-es12)*Den(m)^2)
  + INT(F1x23,6,317,7,2,[],1,0,1,1,1,1,-2,0,2)
    * (-1/2*(mH^2-es23)*Den(mH^2-es23-es12)^2)
"""
# Example output:
# PREFIX_integrals.hh
"""
 id INT(F1x23,7,319,7,1,[],1,1,1,1,1,1,-1,0,1) =
  + INT(F1x23,6,317,7,2,[],1,0,1,1,1,1,-1,-1,2)
    * COEFF1
  + INT(F1x23,6,317,7,2,[],1,0,1,1,1,1,-2,0,2)
    * COEFF2;
"""
# PREFIX_coefficients.hh
"""
L NCOEFF1 = es12;
L DCOEFF1 = (mH^2-es23-es12)*(m)^2;

L NCOEFF2 = -1/2*(mH^2-es23);
L DCOEFF2 = (mH^2-es23-es12)^2;
"""

# Pattern to match Den(...), Den(...)^2 and return (...), (...)^2
den_pattern = 'Den(\([^\)]*\)(?:\^[0-9]*){0,1})'
den_regex = re.compile(den_pattern)

counter=0
with open('integrals' + args.suffix + '.hh', 'w') as integrals_file:
    with open('coefficients' + args.suffix + '.hh', 'w') as coefficients_file:
        with open(args.reduction, 'r') as reduction_file:

            for line in reduction_file:
                if line.startswith("    * ("):
                    # Line is a coefficient
                    counter += 1
                    integrals_file.write("    * " + args.coeff + str(counter))

                    # Search for appearance of Den function
                    den = den_regex.findall(line[6:])

                    # Numerator is built by replacing Den(...) = 1
                    num = den_regex.sub('1', line[6:])

                    coefficients_file.write("L N" + args.coeff + str(counter) + " = " + str(num.rstrip().rstrip(";")) + ";\n")
                    if not den:
                        coefficients_file.write("L D" + args.coeff + str(counter) + " = 1;\n")
                    else:
                        coefficients_file.write("L D" + args.coeff + str(counter) + " = " + '*'.join(den) + ";\n")

                    if line.rstrip().endswith(";"):
                        integrals_file.write(";\n\n")
                    else:
                        integrals_file.write("\n")

                else:
                    # Line is an integral
                    integrals_file.write(line)
