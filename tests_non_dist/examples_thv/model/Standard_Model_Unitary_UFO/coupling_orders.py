from __future__ import absolute_import
# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 13.3.0 for Microsoft Windows (64-bit) (June 3, 2023)
# Date: Wed 10 Jul 2024 18:13:52


from .object_library import all_orders, CouplingOrder


QCD = CouplingOrder(name = 'QCD',
                    expansion_order = 99,
                    hierarchy = 1)

QED = CouplingOrder(name = 'QED',
                    expansion_order = 99,
                    hierarchy = 2)

