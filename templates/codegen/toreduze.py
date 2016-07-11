# vim: ts=3:sw=3:expandtab

from yaml import load, dump
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--intfile", dest="intfile",
                    action="store", type=str, required=True,
                    help='integrals input file', metavar="INTFILE")

parser.add_argument("-s", "--secfile", dest="secfile",
                    action="store", type=str, required=True,
                    help='the Reduze output file "crss.yaml" produced by the Reduze job setup_sector_mappings_alt',
                    metavar="SECFILE")

parser.add_argument("-t", "--txtfile", dest="txtfile",
                    action="store", type=str, required=True,
                    help='txt output file', metavar="OUTFILE")

parser.add_argument("-y", "--yamlfile", dest="yamlfile",
                    action="store", type=str, required=True,
                    help='yaml output file', metavar="OUTFILE")

args = parser.parse_args()

# load input and close intfile immediately after reading
with open(args.intfile, 'r') as intfile:
   instring = intfile.read()

# remove whitespaces and newline characters
instring = instring.replace('\n','').replace(' ','')

# strip trailing "+"
if instring.startswith("+"):
   instring = instring[1:]

# split into individual integrals
integrals = instring.split("+")

# initialize max
tmax = 0
rmax = 0
smax = 0

# process the integrals
# directly write into the output file
with open(args.txtfile, 'w') as outfile:
   outfile.write("{\n")

   for idx, integral in enumerate(integrals):
      # expect integral to be of the form
      # "INT(<family name>,[],<t>,<ID>,<r>,<s>,[],<propagator powers>)"

      # Step 1: remove "INT(" and ")"
      tmp = integral[4:-1]

      # Step 2: split integral into name, tidrs, and powers
      name, tidrs, powers = tmp.split(",[],")

      # Step 3: write integral in the following format:
      #         'INT["<family name>",<t>,<ID>,<r>,<s>,{<propagator powers>}]'
      outfile.write('INT["%s",%s,{%s}]' % (name,tidrs,powers))

      # Step 4: add comma (if not the last) and newline
      if idx + 1 == len(integrals): # if is_last
         outfile.write("\n")
      else:
         outfile.write(",\n")

      # Step 5: determine the maxima of t, r, and s

      # split tidrs into t, ID, r, s and retype them to integer
      t, ID, r, s = map(int, tidrs.split(","))

      # reset maximum if current integral's value is larger
      tmax = max(t, tmax)
      rmax = max(r, rmax)
      smax = max(s, smax)

   outfile.write("}")

# pack tmax, rmax and smax into a dictionary (will be useful later)
maxvals = dict(tmax=tmax, rmax=rmax, smax=smax)

# write the file "codegen/reduze/#loop/reduze_reduce.yaml"
# example:
"""
jobs:
  - reduce_sectors:
      conditional: true
      sector_selection:
        select_recursively:
          - [ReduzeF5L2, 351]
          - <more lines like this>
        t_restriction: [-1, -1]
      identities:
        ibp:
          - { r: [t, 7], s: [0, 4] }
        lorentz:
          - { r: [t, 7], s: [4, 4] }
        sector_symmetries:
          - { r: [t, 7], s: [0, 4] }
"""

# read secfile file
# example:
"""
-
  -
    - sector_selection:
        select_all: false
        select:
          []
        select_recursively:
          - [ReduzeF2L1, 15]
          - [ReduzeF1L1, 15]
        deselect:
          []
        deselect_recursively:
          []
        deselect_independents:
          []
        deselect_graphless: false
        t_restriction: [-1, -1]
"""
with open(args.secfile, 'r') as infile:
   inyaml = load(infile)

# select identities to be generated and used by reduze
identities = {
    "ibp":
        [{"r": ["t", rmax], "s": [0, smax]}],
    "lorentz":
        [{"r": [rmax, rmax], "s": [smax, smax]}],
    "sector_symmetries":
        [{"r": ["t", rmax], "s": [0, smax]}]
}

# add identities key to sector selection, need to strip three - - -
inyaml[0][0][0]["identities"] = identities

# generate output yaml file with reduce_sectors job
outyaml = {
    "jobs":
        [
            {"reduce_sectors":
                 inyaml[0][0][0]
             }
        ]
}

# write yaml file
# large width aids human readibility by preventing lines from wrapping
with open(args.yamlfile, 'w') as outfile:
    outfile.write(dump(outyaml, width=10000))
