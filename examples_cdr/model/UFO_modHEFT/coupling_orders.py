# This file was automatically created by FeynRules 2.3.32
# Mathematica version: 8.0 for Linux x86 (64-bit) (October 10, 2011)
# Date: Wed 7 Jul 2021 13:14:47


from .object_library import all_orders, CouplingOrder


QCD = CouplingOrder(name = 'QCD',
                    expansion_order = 99,
                    hierarchy = 1)

QED = CouplingOrder(name = 'QED',
                    expansion_order = 99,
                    hierarchy = 2)

QL = CouplingOrder(name = 'QL',
                   expansion_order = 1,
                   hierarchy = 2)

QQ = CouplingOrder(name = 'QQ',
                   expansion_order = 99,
                   hierarchy = 1)
