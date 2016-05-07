# vim: ts=3:sw=3:expandtab

#################################################################################
#                                                                               #
# TODO: CRITICAL when outputting FORM code print scalarProduct(p1,p2) as p1.p2 #
#                                                                               #
#################################################################################

from yaml import load, dump
from argparse import ArgumentParser
import sympy as sp

parser = ArgumentParser()

parser.add_argument("-i", "--intfile", dest="intfile",
                    action="store", type=str, required=True,
                    help='the Reduze input file "integralfamilies.yaml"',
                    metavar="INTFILE")

parser.add_argument("-k", "--kinfile", dest="kinfile",
                    action="store", type=str, required=True,
                    help='the Reduze input file "kinematics.yaml"',
                    metavar="KINFILE")

parser.add_argument("-c", "--crossfile", dest="crossfile",
                    action="store", type=str, required=True,
                    help='the Reduze output file "crossings.yaml" produced by the Reduze job setup_sector_mappings',
                    metavar="CROSSFILE")

parser.add_argument("-o", "--outputfile", dest="outputfile",
                    action="store", type=str, required=True,
                    help='YAML file in which to store the generated (crossed) integral families and scalar product rules',
                    metavar="OUTPUTFILE")

parser.add_argument("-m", "--mappingfile", dest="mappingfile",
                    action="store", type=str, required=True,
                    help='FORM file which maps Reduze families to propagators',
                    metavar="MAPPINGFILE")

parser.add_argument("-s", "--scalarproductfile", dest="scalarproductfile",
                    action="store", type=str, required=True,
                    help='FORM file which replaces scalar products with inverse propagators depending on the Reduze family',
                    metavar="SCALARPRODUCTFILE")

args = parser.parse_args()

# load input and close intfile immediately after reading
with open(args.intfile, 'r') as intfile:
   inyaml = load(intfile)

# load input and close kinfile immediately after reading
with open(args.kinfile, 'r') as kinfile:
   kinyaml = load(kinfile)

# load input and close crossfile immediately after reading
with open(args.crossfile, 'r') as crossfile:
   crossyaml = load(crossfile)

# Step 1: parse kinfile and declare all momenta, invariants and masses as sympy symbols

# incoming momenta are stored in a list ['k1', 'k2', 'k3', 'k4'] where each element is an incoming momentum
# generate a list of sympy symbols [k1, k2, k3, k4]
incoming_momenta = [sp.symbols(str(incoming_momentum)) for incoming_momentum in kinyaml["kinematics"]["incoming_momenta"]]

# outgoing momenta are stored in a list ['k5', 'k6', 'k7', 'k8'] where each element is an outgoing momentum
# generate a list of sympy symbols [k5, k6, k7, k8]
outgoing_momenta = [sp.symbols(str(outgoing_momentum)) for outgoing_momentum in kinyaml["kinematics"]["outgoing_momenta"]]

# momentum conservation rule stored in a two element list ['k4', '-k1 - k2 - k3'] where the 0th element is a single momentum
# and the 1st element is an expression (usually involving other external momenta) which it is equal to
momentum_conservation = kinyaml["kinematics"]["momentum_conservation"]

# remember momentum that should be eliminated by momentum conservation
if momentum_conservation:
    excluded_momentum = str(momentum_conservation[0])
else:
    excluded_momentum = ""

# kinematic invariants are stored as a list of lists [ ['a', 1], ['b', 2] ] where the 0th element is the name
# of the kinematic invariant and the 1st element is the mass dimension
# generate a list of sympy symbols [a , b]
kinematic_invariants = [sp.symbols(str(kinematic_invariant[0])) for kinematic_invariant in kinyaml["kinematics"]["kinematic_invariants"]]

# Step 2: apply each crossing to each integral family computing the new propagators by using the rules_momenta replacements
# append each crossed family to the dictionary of all families
# assume crossings.yaml has a single unnamed map of ordered_crossings, e.g...
'''
crossings:
  - name: ""
    ordered_crossings:
      - permutation: [[1, 2]]
        name: x12
        rules_momenta: [[k2, k1], [k1, k2]]
        rules_invariants: [[t, h^2-t-s]]
      - permutation: [[1, 2, 3]]
        name: x123
        rules_momenta: [[k2, k3], [k1, k2], [k3, k1]]
        rules_invariants: [[t, h^2-t-s], [s, t]]
'''

# Set up empty dictionary to hold all families & Create dictionary entry for key "integralfamilies" with empty list of families
all_families = {}
all_families["integralfamilies"] = []

for crossing in crossyaml["crossings"][0]["ordered_crossings"]:

    print "----- Parsing Crossing: " + str(crossing["name"]) + ", " + str(crossing["rules_momenta"])

    for family in inyaml["integralfamilies"]:

        # loop momenta are stored as a list ['p1', 'p2'] where each element is a loop momentum
        # generate a list of sympy symbols [p1, p2]
        loop_momenta = [sp.symbols(str(loop_momentum)) for loop_momentum in family["loop_momenta"]]

        # Set up empty dictionary to hold current crossed family & Construct name for crossed family
        crossed_family = {}
        crossed_family["name"] = str(family["name"]) + str(crossing["name"])

        # loop momenta are stored as a list ['p1', 'p2'] where each element is a loop momentum
        # store list in crossed_family, list() used to explicitly copy list
        crossed_family["loop_momenta"] = list(family["loop_momenta"])

        # Set up an empty list to hold propagators of crossed family
        crossed_family["propagators"] = []

        # Apply the crossing to the momentum of each propagator
        # propagators are two element lists ['p1-k2-k3', 'm^2'] where the 0th element contains the momentum
        # and the 1st element contains the mass
        for propagator in family["propagators"]:

            # Convert momentum of propgator to a sympy expression
            propagator_expr = sp.sympify(propagator[0])

            # Simultaneously replace momenta, must do this simultaneously as we may wish to swap two momenta k1 <-> k2
            propagator_expr = propagator_expr.subs(crossing["rules_momenta"], simultaneous=True)

            # Convert sympy expression to a two element list ['p1-k2-k3', 'm^2'] where the 0th element contains the momentum
            # and the 1st element contains the mass
            crossed_propagator = [str(propagator_expr), str(propagator[1])]

            # Append propagator to propagators of current crossed family
            crossed_family["propagators"].append(crossed_propagator)

        # Append to list of all families
        all_families["integralfamilies"].append(crossed_family)

        print "Generated Family: " + str(crossed_family["name"])

# Add list of (uncrossed) integralfamilies from inyaml to list of (crossed) integralfamilies already in all families
all_families["integralfamilies"] = all_families["integralfamilies"] + inyaml["integralfamilies"]

# Step 3: for each integralfamily compute relation between each scalar product involving the loop momenta and the propagators
# append each relation to the dictionary of all families

# The relations form a linear system
# n = m s + c
# n is a vector of propagators which we call inverse_propagators_matrix
# s is a vector of scalar products which we call scalar_products_matrix
# m is a matrix containing the coefficient of each scalar product appearing in a given propagator
# which we call propagators_to_scalar_products_matrix
# c is a vector containing masses or scalar products which do not involve the loop momenta which we call constants_matrix

# We proceed by:
# 1) computing m
# 2) computing c from c = n - m * s
# 3) computing s from s = m^(-1) * ( n - c )

print "----- Computing scalar product rules"

class scalarProduct(sp.Function):
    '''
    SymPy scalar product function scalarProduct('k1','k2') = k1.k2 = k2.k1
    '''
    nargs = 2
    is_commutative = True

def strip_pow_two(expr):
    """
    Convert powers of two in an expression to scalarProducts, like a**2 => scalarProduct(a,a)
    adapted from: http://stackoverflow.com/questions/14264431/expanding-algebraic-powers-in-python-sympy
    """
    wild_symbol_1 = sp.Wild('wild_symbol_1', exclude=[sp.Number])

    return expr.replace(sp.Pow(wild_symbol_1,sp.Integer(2)),wild_symbol_1, exact=True)

def square_to_scalarProduct(expr):
    """
    Convert powers of two in an expression to scalarProducts, like a**2 => scalarProduct(a,a)
    adapted from: http://stackoverflow.com/questions/14264431/expanding-algebraic-powers-in-python-sympy
    """

    # Get list of all powers appearing
    pows = list(expr.atoms(sp.Pow))

    # Check all powers have exponent 2
    if any(not sp.Integer(2) for b, e in (i.as_base_exp() for i in pows)):
        raise ValueError("A power contains an exponent other than 2")

    # Create list of tuples of replacements
    repl = zip(pows, (scalarProduct(*[b]*e) for b,e in (i.as_base_exp() for i in pows)))

    return expr.subs(repl)

def mul_to_scalarProduct(expr):
    """
    Convert products of symbols in an expression to scalarProducts, like -2*a*b => -2*scalarProduct(a,b)
    """

    # Get list of all mul appearing
    muls = list(expr.atoms(sp.Mul))

    # TODO: check this works
    # Check all mul contain at most two symbols
    if any(len(filter(lambda x: not x.is_Number, i.as_ordered_factors())) > 2 for i in muls):
        raise ValueError("Expression contains a product of more than 2 symbols")

    # Declare wild cards
    wild_complex_1 = sp.Wild('wild_complex_1', exclude=[not sp.Number])
    wild_symbol_1 = sp.Wild('wild_symbol_1', exclude=[sp.Number])
    wild_symbol_2 = sp.Wild('wild_symbol_2', exclude=[sp.Number])

    # Try matching just two symbols a*a
    expr = expr.replace(sp.Mul(wild_symbol_1, wild_symbol_2),
                        scalarProduct(wild_symbol_1, wild_symbol_2), exact=True)

    # Try matching two symbols and a number 2*a*a (seems to match also two symbols and more than one number)
    expr = expr.replace(sp.Mul(wild_complex_1, wild_symbol_1, wild_symbol_2),
                        sp.Mul(wild_complex_1, scalarProduct(wild_symbol_1, wild_symbol_2)), exact=True)

    return expr

def inversePropagator(x,y):
    '''
    SymPy inverse propagator function inversePropagator('k1','m^2') = SP(k1,k1) - m^2
    '''
    return sp.Function('inversePropagator', nargs=2)(x,y)


for family in all_families["integralfamilies"]:

    print "Generating scalar product rules for family: " + str(family["name"])

    # loop momenta are stored as a list ['p1', 'p2'] where each element is a loop momentum
    # generate a list of sympy symbols [p1, p2]
    loop_momenta = [sp.symbols(str(loop_momentum)) for loop_momentum in family["loop_momenta"]]

    # Step 3.1.1: Generate list of all scalar products

    # Set up an empty list to hold scalar products as SymPy functions [ scalarProduct(p1,p1), scalarProduct(p1,p2) ]
    scalar_products = []

    # Set up an empty list to hold lists of scalar products as lists [ [p1,p1], [p1,p2] ]
    scalar_products_list = []

    # TODO: remove crazy hack mul_to_scalarProduct(square_to_scalarProduct(sp.Mul(a,b))) to get scalarProduct(a,b) in 'canonical' form
    # Generate list involving all scalar products of loop momenta with loop momenta
    for i in range(len(loop_momenta)):
        for j in range(len(loop_momenta)):
            if(i>=j):
                scalar_products.append(mul_to_scalarProduct(square_to_scalarProduct(sp.Mul(loop_momenta[i],loop_momenta[j]))))
                scalar_products_list.append([str(loop_momenta[i]),str(loop_momenta[j])])

    # TODO: remove crazy hack mul_to_scalarProduct(square_to_scalarProduct(sp.Mul(a,b))) to get scalarProduct(a,b) in 'canonical' form
    # Append to list all scalar products of loop momenta with incoming momenta
    for loop_momentum in loop_momenta:
        for incoming_momentum in incoming_momenta:
            if str(incoming_momentum) != str(excluded_momentum):
                scalar_products.append(mul_to_scalarProduct(square_to_scalarProduct(sp.Mul(loop_momentum,incoming_momentum))))
                scalar_products_list.append([str(loop_momentum),str(incoming_momentum)])


    # TODO: remove crazy hack mul_to_scalarProduct(square_to_scalarProduct(sp.Mul(a,b))) to get scalarProduct(a,b) in 'canonical' form
    # Append to list all scalar products of loop momenta with outgoing momenta
    for loop_momentum in loop_momenta:
        for outgoing_momentum in outgoing_momenta:
            if str(outgoing_momentum) != str(excluded_momentum):
                scalar_products.append(mul_to_scalarProduct(square_to_scalarProduct(sp.Mul(loop_momentum,outgoing_momentum))))
                scalar_products_list.append([str(loop_momentum),str(outgoing_momentum)])


    # Create SymPy matrix (vector) from list of scalar products
    scalar_products_matrix = sp.Matrix(scalar_products)

    # Now check that we have exactly as many scalar products as propagators
    assert len(scalar_products) == len(family["propagators"])

    # Step 3.1.2: Generate list of all inverse propagators

    # Set up an empty list to hold inverse propagators
    inverse_propagators = []

    # Set up an empty list to hold expanded inverse propagators
    inverse_propagators_expanded = []

    for propagator in family["propagators"]:
        # propagators are two element lists ['p1-k2-k3', 'm^2'] where the 0th element contains the momentum
        # and the 1st element contains the mass
        inverse_propagators.append(inversePropagator(sp.sympify(propagator[0]),sp.sympify(propagator[1])))

        # TODO: improve this code
        # Dirty hack to expand propagators
        inverse_propagators_expanded.append(
            [
                mul_to_scalarProduct(
                    square_to_scalarProduct(
                        sp.expand(
                            sp.Mul(
                                sp.sympify(propagator[0]),
                                sp.sympify(propagator[0])
                            )
                        )
                    )
                )-sp.sympify(propagator[1])
            ]
        )

    # Create SymPy matrix (vector) from list of inverse propagators
    inverse_propagators_matrix = sp.Matrix(inverse_propagators)

    # Create SymPy matrix (vector) from list of expanded inverse propagators
    inverse_propagators_expanded_matrix = sp.Matrix(inverse_propagators_expanded)

    # Step 3.1.3: Generate matrix m which expresses propagators in terms of scalar products

    # Set up an empty list to hold for each propagator the coefficient of each scalar product
    propagators_to_scalar_products = []

    for propagator in inverse_propagators_expanded_matrix:
        # Store the coefficient of each scalar product appearing in the propagator in a list
        propagators_to_scalar_products_row = []
        for scalar in scalar_products_matrix:
            propagators_to_scalar_products_row.append(propagator.coeff(scalar))
        # Append coefficient lists to a list
        propagators_to_scalar_products.append(propagators_to_scalar_products_row)

    # Create SymPy matrix from the coefficient list
    propagators_to_scalar_products_matrix = sp.Matrix(propagators_to_scalar_products)

    # Step 3.2: Compute matrix c which contains all factors appearing in the expanded propagators which are independent of the loop momenta
    constants_matrix = inverse_propagators_expanded_matrix - (propagators_to_scalar_products_matrix * scalar_products_matrix)

    # TODO: check that constants_matrix is free of loop momenta

    # Step 3.3: Solve system for s

    inverse_propagators_scalar_products_matrix = propagators_to_scalar_products_matrix.inv()

    # Now check that s = m^(-1) * ( n - c )
    assert(
        sp.sympify(
            inverse_propagators_scalar_products_matrix *  ( inverse_propagators_expanded_matrix - constants_matrix)
        ) == sp.sympify(scalar_products_matrix)
    )

    # Add relation between scalar propagators and inverse propagators to family
    family["scalar_products_to_inverse_propagators"] = \
        [list(i) for i in zip( scalar_products_list,
             [str(x[0]).replace('**','^') for x in (inverse_propagators_scalar_products_matrix * ( inverse_propagators_matrix - constants_matrix)).tolist()] )]

print "----- Saving all families to YAML file"
# large width aids human readibility by preventing lines from wrapping
with open(args.outputfile, 'w') as outfile:
    outfile.write(dump(all_families, width=10000))
print "created " + str(args.outputfile)

print "----- Saving Reduze family mapping to FORM file"
'''
Example output:

If( Match( Sector( N1x132, ?tail) ) );
    Multiply Tag( ReduzeN0, p1, 0);
    Multiply Tag( ReduzeN1, p2, 0);
    Multiply Tag( ReduzeN2, p1 - p2, m);
    Multiply Tag( ReduzeN3, k3 + p1, 0);
    Multiply Tag( ReduzeN4, k3 + p2, m);
    Multiply Tag( ReduzeN5, -k1 + p1, 0);
    Multiply Tag( ReduzeN6, -k1 + p2, 0);
    Multiply Tag( ReduzeN7, k2 + p1 - p2, m);
    Multiply Tag( ReduzeN8, -k1 - k2 + p2, m);
EndIf;

'''
with open(args.mappingfile, 'w') as outfile:
    for family in all_families["integralfamilies"]:
        outfile.write("If( Match( Sector( " + str(family["name"]) + ", ?tail) ) );")
        outfile.write('\n')
        for counter, propagator in enumerate(family["propagators"]):
            # Note: must write only mass and not mass^2 in Tag hence we call strip_pow_two
            outfile.write("    Multiply Tag( ReduzeN" + str(counter) + ", " + str(propagator[0]) + ", " + str(strip_pow_two(sp.sympify(propagator[1]))) + ");")
            outfile.write('\n')
        outfile.write("EndIf;")
        outfile.write('\n')
        outfile.write('\n')
print "created " + str(args.mappingfile)

print "----- Saving Reduze scalar product to propagator rules to FORM file"
'''
Example output:

If( Match( Sector( F1x12, ?tail) ) );
    Identify p1.p1 = m^2 + inversePropagator(p1, m^2);
    Identify p2.p1 = m^2 + inversePropagator(p1, m^2)/2 + inversePropagator(p2, m^2)/2 - inversePropagator(p1 - p2, 0)/2;
    Identify p2.p2 = m^2 + inversePropagator(p2, m^2);
    Identify p1.k1 = inversePropagator(p1, m^2)/2 - inversePropagator(-k1 + p1, m^2)/2 + scalarProduct(k1, k1)/2;
    Identify p1.k2 = -inversePropagator(p1, m^2)/2 + inversePropagator(k2 + p1, m^2)/2 - scalarProduct(k2, k2)/2;
    Identify p1.k3 = inversePropagator(-k1 + p1, m^2)/2 - inversePropagator(-k1 - k3 + p1, m^2)/2 + scalarProduct(k1, k3) + scalarProduct(k3, k3)/2;
    Identify p2.k1 = inversePropagator(p2, m^2)/2 - inversePropagator(-k1 + p2, m^2)/2 + scalarProduct(k1, k1)/2;
    Identify p2.k2 = -inversePropagator(p2, m^2)/2 + inversePropagator(k2 + p2, m^2)/2 - scalarProduct(k2, k2)/2;
    Identify p2.k3 = inversePropagator(-k1 + p2, m^2)/2 - inversePropagator(-k1 - k3 + p2, m^2)/2 + scalarProduct(k1, k3) + scalarProduct(k3, k3)/2;
EndIf;
'''
with open(args.scalarproductfile, 'w') as outfile:
    for family in all_families["integralfamilies"]:
        outfile.write("If( Match( Sector( " + str(family["name"]) + ", ?tail) ) );")
        outfile.write('\n')
        for scalar_product_rule in family["scalar_products_to_inverse_propagators"]:
            outfile.write("    Identify " + str(scalar_product_rule[0][0]) + "." + str(scalar_product_rule[0][1]) + \
              " = " + str(scalar_product_rule[1]) + ";")
            outfile.write('\n')
        outfile.write("EndIf;")
        outfile.write('\n')
        outfile.write('\n')
print "created " + str(args.scalarproductfile)
