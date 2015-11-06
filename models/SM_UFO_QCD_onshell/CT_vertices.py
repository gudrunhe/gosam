# This file was automatically created by FeynRules 2.3.9
# Mathematica version: 10.2.0 for Linux x86 (64-bit) (July 6, 2015)
# Date: Wed 23 Sep 2015 13:54:43


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'UV',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV10, L.VVV3, L.VVV4, L.VVV5, L.VVV6, L.VVV7, L.VVV8, L.VVV9 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
               couplings = {(0,1,0):C.UVGC_132_50,(0,1,1):C.UVGC_132_51,(0,1,2):C.UVGC_132_52,(0,1,3):C.UVGC_132_53,(0,1,4):C.UVGC_100_2,(0,1,5):C.UVGC_132_54,(0,2,0):C.UVGC_135_59,(0,2,1):C.UVGC_135_60,(0,2,2):C.UVGC_135_61,(0,2,3):C.UVGC_135_62,(0,2,4):C.UVGC_135_63,(0,2,5):C.UVGC_135_64,(0,4,0):C.UVGC_135_59,(0,4,1):C.UVGC_135_60,(0,4,2):C.UVGC_135_61,(0,4,3):C.UVGC_137_67,(0,4,4):C.UVGC_137_68,(0,4,5):C.UVGC_135_64,(0,6,0):C.UVGC_132_50,(0,6,1):C.UVGC_132_51,(0,6,2):C.UVGC_132_52,(0,6,3):C.UVGC_134_57,(0,6,4):C.UVGC_134_58,(0,6,5):C.UVGC_132_54,(0,7,0):C.UVGC_132_50,(0,7,1):C.UVGC_132_51,(0,7,2):C.UVGC_132_52,(0,7,3):C.UVGC_133_55,(0,7,4):C.UVGC_133_56,(0,7,5):C.UVGC_132_54,(0,0,0):C.UVGC_135_59,(0,0,1):C.UVGC_135_60,(0,0,2):C.UVGC_135_61,(0,0,3):C.UVGC_136_65,(0,0,4):C.UVGC_136_66,(0,0,5):C.UVGC_135_64,(0,3,3):C.UVGC_99_126,(0,3,4):C.UVGC_137_68,(0,5,3):C.UVGC_100_1,(0,5,4):C.UVGC_100_2})

V_2 = CTVertex(name = 'V_2',
               type = 'UV',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV11, L.VVVV12, L.VVVV13 ],
               loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
               couplings = {(7,0,0):C.UVGC_141_82,(7,0,2):C.UVGC_141_83,(7,0,3):C.UVGC_141_84,(7,0,4):C.UVGC_141_85,(7,0,5):C.UVGC_141_86,(7,0,6):C.UVGC_141_87,(6,0,0):C.UVGC_141_82,(6,0,2):C.UVGC_141_83,(6,0,3):C.UVGC_141_84,(6,0,4):C.UVGC_142_88,(6,0,5):C.UVGC_142_89,(6,0,6):C.UVGC_141_87,(0,0,4):C.UVGC_102_6,(0,0,5):C.UVGC_102_5,(2,0,4):C.UVGC_102_6,(2,0,5):C.UVGC_102_5,(5,0,4):C.UVGC_101_3,(5,0,5):C.UVGC_101_4,(1,0,4):C.UVGC_101_3,(1,0,5):C.UVGC_101_4,(4,0,4):C.UVGC_101_3,(4,0,5):C.UVGC_101_4,(3,0,4):C.UVGC_101_3,(3,0,5):C.UVGC_101_4,(8,0,4):C.UVGC_102_5,(8,0,5):C.UVGC_102_6,(11,0,4):C.UVGC_105_9,(11,0,5):C.UVGC_105_10,(10,0,4):C.UVGC_105_9,(10,0,5):C.UVGC_105_10,(9,0,4):C.UVGC_104_7,(9,0,5):C.UVGC_104_8,(6,1,0):C.UVGC_138_69,(6,1,2):C.UVGC_138_70,(6,1,4):C.UVGC_138_71,(6,1,5):C.UVGC_138_72,(6,1,6):C.UVGC_138_73,(7,1,1):C.UVGC_106_11,(7,1,4):C.UVGC_107_13,(7,1,5):C.UVGC_107_14,(8,1,0):C.UVGC_143_90,(8,1,2):C.UVGC_143_91,(8,1,3):C.UVGC_143_92,(8,1,4):C.UVGC_143_93,(8,1,5):C.UVGC_143_94,(8,1,6):C.UVGC_143_95,(0,1,4):C.UVGC_102_6,(0,1,5):C.UVGC_102_5,(2,1,4):C.UVGC_102_6,(2,1,5):C.UVGC_102_5,(5,1,4):C.UVGC_101_3,(5,1,5):C.UVGC_101_4,(1,1,4):C.UVGC_101_3,(1,1,5):C.UVGC_101_4,(4,1,4):C.UVGC_101_3,(4,1,5):C.UVGC_101_4,(3,1,4):C.UVGC_101_3,(3,1,5):C.UVGC_101_4,(11,1,4):C.UVGC_105_9,(11,1,5):C.UVGC_105_10,(10,1,4):C.UVGC_105_9,(10,1,5):C.UVGC_105_10,(9,1,4):C.UVGC_104_7,(9,1,5):C.UVGC_104_8,(6,2,1):C.UVGC_106_11,(6,2,4):C.UVGC_106_12,(6,2,5):C.UVGC_104_7,(7,2,0):C.UVGC_138_69,(7,2,2):C.UVGC_138_70,(7,2,4):C.UVGC_139_74,(7,2,5):C.UVGC_139_75,(7,2,6):C.UVGC_138_73,(8,2,0):C.UVGC_140_76,(8,2,2):C.UVGC_140_77,(8,2,3):C.UVGC_140_78,(8,2,4):C.UVGC_140_79,(8,2,5):C.UVGC_140_80,(8,2,6):C.UVGC_140_81,(0,2,4):C.UVGC_102_6,(0,2,5):C.UVGC_102_5,(2,2,4):C.UVGC_102_6,(2,2,5):C.UVGC_102_5,(5,2,4):C.UVGC_101_3,(5,2,5):C.UVGC_101_4,(1,2,4):C.UVGC_101_3,(1,2,5):C.UVGC_101_4,(4,2,4):C.UVGC_101_3,(4,2,5):C.UVGC_101_4,(3,2,4):C.UVGC_101_3,(3,2,5):C.UVGC_101_4,(11,2,4):C.UVGC_105_9,(11,2,5):C.UVGC_105_10,(10,2,4):C.UVGC_105_9,(10,2,5):C.UVGC_105_10,(9,2,4):C.UVGC_104_7,(9,2,5):C.UVGC_104_8})

V_3 = CTVertex(name = 'V_3',
               type = 'UV',
               particles = [ P.u__tilde__, P.u, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
               loop_particles = [ [ [P.g, P.u] ] ],
               couplings = {(0,2,0):C.UVGC_82_120,(0,0,0):C.UVGC_96_123,(0,1,0):C.UVGC_96_123})

V_4 = CTVertex(name = 'V_4',
               type = 'UV',
               particles = [ P.c__tilde__, P.c, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
               loop_particles = [ [ [P.c, P.g] ] ],
               couplings = {(0,2,0):C.UVGC_82_120,(0,0,0):C.UVGC_121_33,(0,1,0):C.UVGC_121_33})

V_5 = CTVertex(name = 'V_5',
               type = 'UV',
               particles = [ P.t__tilde__, P.t, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
               loop_particles = [ [ [P.g, P.t] ] ],
               couplings = {(0,2,0):C.UVGC_82_120,(0,0,0):C.UVGC_145_97,(0,1,0):C.UVGC_145_97})

V_6 = CTVertex(name = 'V_6',
               type = 'UV',
               particles = [ P.u__tilde__, P.u, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.u] ], [ [P.t] ] ],
               couplings = {(0,2,5):C.UVGC_81_119,(0,0,0):C.UVGC_108_15,(0,0,1):C.UVGC_108_16,(0,0,2):C.UVGC_108_17,(0,0,3):C.UVGC_108_18,(0,0,4):C.UVGC_108_19,(0,0,6):C.UVGC_108_20,(0,0,5):C.UVGC_108_21,(0,1,0):C.UVGC_108_15,(0,1,1):C.UVGC_108_16,(0,1,2):C.UVGC_108_17,(0,1,3):C.UVGC_108_18,(0,1,4):C.UVGC_108_19,(0,1,6):C.UVGC_108_20,(0,1,5):C.UVGC_108_21})

V_7 = CTVertex(name = 'V_7',
               type = 'UV',
               particles = [ P.c__tilde__, P.c, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
               couplings = {(0,2,2):C.UVGC_81_119,(0,0,0):C.UVGC_108_15,(0,0,1):C.UVGC_108_16,(0,0,3):C.UVGC_108_17,(0,0,4):C.UVGC_108_18,(0,0,5):C.UVGC_108_19,(0,0,6):C.UVGC_108_20,(0,0,2):C.UVGC_122_34,(0,1,0):C.UVGC_108_15,(0,1,1):C.UVGC_108_16,(0,1,3):C.UVGC_108_17,(0,1,4):C.UVGC_108_18,(0,1,5):C.UVGC_108_19,(0,1,6):C.UVGC_108_20,(0,1,2):C.UVGC_122_34})

V_8 = CTVertex(name = 'V_8',
               type = 'UV',
               particles = [ P.t__tilde__, P.t, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.t] ], [ [P.t] ] ],
               couplings = {(0,2,5):C.UVGC_81_119,(0,0,0):C.UVGC_108_15,(0,0,1):C.UVGC_108_16,(0,0,2):C.UVGC_108_17,(0,0,3):C.UVGC_108_18,(0,0,4):C.UVGC_108_19,(0,0,6):C.UVGC_108_20,(0,0,5):C.UVGC_146_98,(0,1,0):C.UVGC_108_15,(0,1,1):C.UVGC_108_16,(0,1,2):C.UVGC_108_17,(0,1,3):C.UVGC_108_18,(0,1,4):C.UVGC_108_19,(0,1,6):C.UVGC_108_20,(0,1,5):C.UVGC_146_98})

V_9 = CTVertex(name = 'V_9',
               type = 'UV',
               particles = [ P.d__tilde__, P.u, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV10 ],
               loop_particles = [ [ [P.d, P.g], [P.g, P.u] ], [ [P.d, P.g, P.u] ] ],
               couplings = {(0,0,0):C.UVGC_111_22,(0,0,1):C.UVGC_111_23})

V_10 = CTVertex(name = 'V_10',
                type = 'UV',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10 ],
                loop_particles = [ [ [P.c, P.g] ], [ [P.c, P.g, P.s] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_124_36,(0,0,2):C.UVGC_111_22,(0,0,1):C.UVGC_111_23})

V_11 = CTVertex(name = 'V_11',
                type = 'UV',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_148_100,(0,0,2):C.UVGC_148_101,(0,0,1):C.UVGC_111_23})

V_12 = CTVertex(name = 'V_12',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10, L.FFV11 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_125_37,(0,1,0):C.UVGC_126_38})

V_13 = CTVertex(name = 'V_13',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10, L.FFV11 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_149_102,(0,1,0):C.UVGC_150_103})

V_14 = CTVertex(name = 'V_14',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,2,0):C.UVGC_80_118,(0,0,0):C.UVGC_85_122,(0,1,0):C.UVGC_85_122})

V_15 = CTVertex(name = 'V_15',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,2,0):C.UVGC_80_118,(0,0,0):C.UVGC_85_122,(0,1,0):C.UVGC_85_122})

V_16 = CTVertex(name = 'V_16',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,2,0):C.UVGC_80_118,(0,0,0):C.UVGC_113_25,(0,1,0):C.UVGC_113_25})

V_17 = CTVertex(name = 'V_17',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d, P.g] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,2,2):C.UVGC_81_119,(0,0,0):C.UVGC_108_15,(0,0,1):C.UVGC_108_16,(0,0,3):C.UVGC_108_17,(0,0,4):C.UVGC_108_18,(0,0,5):C.UVGC_108_19,(0,0,6):C.UVGC_108_20,(0,0,2):C.UVGC_108_21,(0,1,0):C.UVGC_108_15,(0,1,1):C.UVGC_108_16,(0,1,3):C.UVGC_108_17,(0,1,4):C.UVGC_108_18,(0,1,5):C.UVGC_108_19,(0,1,6):C.UVGC_108_20,(0,1,2):C.UVGC_108_21})

V_18 = CTVertex(name = 'V_18',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.s] ], [ [P.t] ] ],
                couplings = {(0,2,5):C.UVGC_81_119,(0,0,0):C.UVGC_108_15,(0,0,1):C.UVGC_108_16,(0,0,2):C.UVGC_108_17,(0,0,3):C.UVGC_108_18,(0,0,4):C.UVGC_108_19,(0,0,6):C.UVGC_108_20,(0,0,5):C.UVGC_108_21,(0,1,0):C.UVGC_108_15,(0,1,1):C.UVGC_108_16,(0,1,2):C.UVGC_108_17,(0,1,3):C.UVGC_108_18,(0,1,4):C.UVGC_108_19,(0,1,6):C.UVGC_108_20,(0,1,5):C.UVGC_108_21})

V_19 = CTVertex(name = 'V_19',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV10, L.FFV11, L.FFV9 ],
                loop_particles = [ [ [P.b] ], [ [P.b, P.g] ], [ [P.c] ], [ [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,2,1):C.UVGC_81_119,(0,0,0):C.UVGC_108_15,(0,0,2):C.UVGC_108_16,(0,0,3):C.UVGC_108_17,(0,0,4):C.UVGC_108_18,(0,0,5):C.UVGC_108_19,(0,0,6):C.UVGC_108_20,(0,0,1):C.UVGC_114_26,(0,1,0):C.UVGC_108_15,(0,1,2):C.UVGC_108_16,(0,1,3):C.UVGC_108_17,(0,1,4):C.UVGC_108_18,(0,1,5):C.UVGC_108_19,(0,1,6):C.UVGC_108_20,(0,1,1):C.UVGC_114_26})

V_20 = CTVertex(name = 'V_20',
                type = 'UV',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10 ],
                loop_particles = [ [ [P.d, P.g], [P.g, P.u] ], [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_111_22,(0,0,1):C.UVGC_111_23})

V_21 = CTVertex(name = 'V_21',
                type = 'UV',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10 ],
                loop_particles = [ [ [P.c, P.g] ], [ [P.c, P.g, P.s] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_124_36,(0,0,2):C.UVGC_111_22,(0,0,1):C.UVGC_111_23})

V_22 = CTVertex(name = 'V_22',
                type = 'UV',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_148_100,(0,0,2):C.UVGC_148_101,(0,0,1):C.UVGC_111_23})

V_23 = CTVertex(name = 'V_23',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV10, L.FFV11 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_116_28,(0,1,0):C.UVGC_117_29})

V_24 = CTVertex(name = 'V_24',
                type = 'UV',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF3 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_84_121})

V_25 = CTVertex(name = 'V_25',
                type = 'UV',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1, L.FF2 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_123_35,(0,1,0):C.UVGC_120_32})

V_26 = CTVertex(name = 'V_26',
                type = 'UV',
                particles = [ P.t__tilde__, P.t ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1, L.FF2 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_147_99,(0,1,0):C.UVGC_144_96})

V_27 = CTVertex(name = 'V_27',
                type = 'UV',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF3 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_84_121})

V_28 = CTVertex(name = 'V_28',
                type = 'UV',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF3 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_84_121})

V_29 = CTVertex(name = 'V_29',
                type = 'UV',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1, L.FF2 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_115_27,(0,1,0):C.UVGC_112_24})

V_30 = CTVertex(name = 'V_30',
                type = 'UV',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV1, L.VV2 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,1,0):C.UVGC_131_47,(0,1,1):C.UVGC_131_48,(0,1,4):C.UVGC_131_49,(0,0,2):C.UVGC_98_124,(0,0,3):C.UVGC_98_125})

V_31 = CTVertex(name = 'V_31',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_128_40})

V_32 = CTVertex(name = 'V_32',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_154_111})

V_33 = CTVertex(name = 'V_33',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_118_30})

V_34 = CTVertex(name = 'V_34',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_127_39})

V_35 = CTVertex(name = 'V_35',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_153_110})

V_36 = CTVertex(name = 'V_36',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_119_31})

V_37 = CTVertex(name = 'V_37',
                type = 'UV',
                particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.c, P.g] ], [ [P.c, P.g, P.s] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_129_41,(0,0,2):C.UVGC_129_42,(0,0,1):C.UVGC_129_43})

V_38 = CTVertex(name = 'V_38',
                type = 'UV',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_152_107,(0,0,2):C.UVGC_152_108,(0,0,1):C.UVGC_152_109,(0,1,0):C.UVGC_155_112,(0,1,2):C.UVGC_155_113,(0,1,1):C.UVGC_155_114})

V_39 = CTVertex(name = 'V_39',
                type = 'UV',
                particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.c, P.g] ], [ [P.c, P.g, P.s] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_130_44,(0,0,2):C.UVGC_130_45,(0,0,1):C.UVGC_130_46})

V_40 = CTVertex(name = 'V_40',
                type = 'UV',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_156_115,(0,0,2):C.UVGC_156_116,(0,0,1):C.UVGC_156_117,(0,1,0):C.UVGC_151_104,(0,1,2):C.UVGC_151_105,(0,1,1):C.UVGC_151_106})

