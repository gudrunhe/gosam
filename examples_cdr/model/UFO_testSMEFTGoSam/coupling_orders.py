# This file was automatically created by FeynRules 2.3.47
# Mathematica version: 12.1.1 for Linux x86 (64-bit) (June 19, 2020)
# Date: Mon 20 Feb 2023 15:47:51


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

NP = CouplingOrder(name = 'NP',
                   expansion_order = 1,
                   hierarchy = 1)

QQ = CouplingOrder(name = 'QQ',
                   expansion_order = 99,
                   hierarchy = 1)

