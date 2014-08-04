# This file was automatically created by FeynRules 2.0.23
# Mathematica version: 9.0 for Linux x86 (64-bit) (February 7, 2013)
# Date: Mon 14 Apr 2014 18:20:07


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.H, P.H, P.H, P.H ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_20})

V_2 = Vertex(name = 'V_2',
             particles = [ P.H, P.H, P.H ],
             color = [ '1' ],
             lorentz = [ L.SSS1 ],
             couplings = {(0,0):C.GC_65})

V_3 = Vertex(name = 'V_3',
             particles = [ P.ghG, P.ghG__tilde__, P.G ],
             color = [ 'f(1,2,3)' ],
             lorentz = [ L.UUV1 ],
             couplings = {(0,0):C.GC_4})

V_4 = Vertex(name = 'V_4',
             particles = [ P.G, P.G, P.G ],
             color = [ 'f(1,2,3)' ],
             lorentz = [ L.VVV1 ],
             couplings = {(0,0):C.GC_4})

V_5 = Vertex(name = 'V_5',
             particles = [ P.G, P.G, P.G, P.G ],
             color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
             lorentz = [ L.VVVV1, L.VVVV3, L.VVVV4 ],
             couplings = {(1,1):C.GC_6,(0,0):C.GC_6,(2,2):C.GC_6})

V_6 = Vertex(name = 'V_6',
             particles = [ P.H, P.H, P.Gr ],
             color = [ '1' ],
             lorentz = [ L.SST1, L.SST2 ],
             couplings = {(0,0):C.GC_12,(0,1):C.GC_72})

V_7 = Vertex(name = 'V_7',
             particles = [ P.H, P.H, P.H, P.H, P.Gr ],
             color = [ '1' ],
             lorentz = [ L.SSSST1 ],
             couplings = {(0,0):C.GC_21})

V_8 = Vertex(name = 'V_8',
             particles = [ P.H, P.H, P.H, P.Gr ],
             color = [ '1' ],
             lorentz = [ L.SSST1 ],
             couplings = {(0,0):C.GC_66})

V_9 = Vertex(name = 'V_9',
             particles = [ P.A, P.A, P.Gr ],
             color = [ '1' ],
             lorentz = [ L.VVT2 ],
             couplings = {(0,0):C.GC_63})

V_10 = Vertex(name = 'V_10',
              particles = [ P.G, P.G, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.VVT2 ],
              couplings = {(0,0):C.GC_11})

V_11 = Vertex(name = 'V_11',
              particles = [ P.W__minus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVT1, L.VVT2 ],
              couplings = {(0,1):C.GC_11,(0,0):C.GC_69})

V_12 = Vertex(name = 'V_12',
              particles = [ P.Z, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVT1, L.VVT2 ],
              couplings = {(0,1):C.GC_63,(0,0):C.GC_73})

V_13 = Vertex(name = 'V_13',
              particles = [ P.G, P.G, P.G, P.Gr ],
              color = [ 'f(1,2,3)' ],
              lorentz = [ L.VVVT1 ],
              couplings = {(0,0):C.GC_18})

V_14 = Vertex(name = 'V_14',
              particles = [ P.G, P.G, P.G, P.G, P.Gr ],
              color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
              lorentz = [ L.VVVVT1, L.VVVVT2, L.VVVVT5 ],
              couplings = {(2,2):C.GC_19,(1,1):C.GC_19,(0,0):C.GC_19})

V_15 = Vertex(name = 'V_15',
              particles = [ P.ve__tilde__, P.ve, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFT1 ],
              couplings = {(0,0):C.GC_10})

V_16 = Vertex(name = 'V_16',
              particles = [ P.vm__tilde__, P.vm, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFT1 ],
              couplings = {(0,0):C.GC_10})

V_17 = Vertex(name = 'V_17',
              particles = [ P.vt__tilde__, P.vt, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFT1 ],
              couplings = {(0,0):C.GC_10})

V_18 = Vertex(name = 'V_18',
              particles = [ P.u__tilde__, P.u, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_100})

V_19 = Vertex(name = 'V_19',
              particles = [ P.c__tilde__, P.c, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_79})

V_20 = Vertex(name = 'V_20',
              particles = [ P.t__tilde__, P.t, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_94})

V_21 = Vertex(name = 'V_21',
              particles = [ P.e__plus__, P.e__minus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_85})

V_22 = Vertex(name = 'V_22',
              particles = [ P.m__plus__, P.m__minus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_88})

V_23 = Vertex(name = 'V_23',
              particles = [ P.tt__plus__, P.tt__minus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_97})

V_24 = Vertex(name = 'V_24',
              particles = [ P.d__tilde__, P.d, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_82})

V_25 = Vertex(name = 'V_25',
              particles = [ P.s__tilde__, P.s, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_91})

V_26 = Vertex(name = 'V_26',
              particles = [ P.b__tilde__, P.b, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFT1, L.FFT2 ],
              couplings = {(0,0):C.GC_10,(0,1):C.GC_76})

V_27 = Vertex(name = 'V_27',
              particles = [ P.u__tilde__, P.u, P.G ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_28 = Vertex(name = 'V_28',
              particles = [ P.c__tilde__, P.c, P.G ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_29 = Vertex(name = 'V_29',
              particles = [ P.t__tilde__, P.t, P.G ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_30 = Vertex(name = 'V_30',
              particles = [ P.d__tilde__, P.d, P.G ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_31 = Vertex(name = 'V_31',
              particles = [ P.s__tilde__, P.s, P.G ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_32 = Vertex(name = 'V_32',
              particles = [ P.b__tilde__, P.b, P.G ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_33 = Vertex(name = 'V_33',
              particles = [ P.u__tilde__, P.u, P.G, P.Gr ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFVT1 ],
              couplings = {(0,0):C.GC_17})

V_34 = Vertex(name = 'V_34',
              particles = [ P.c__tilde__, P.c, P.G, P.Gr ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFVT1 ],
              couplings = {(0,0):C.GC_17})

V_35 = Vertex(name = 'V_35',
              particles = [ P.t__tilde__, P.t, P.G, P.Gr ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFVT1 ],
              couplings = {(0,0):C.GC_17})

V_36 = Vertex(name = 'V_36',
              particles = [ P.d__tilde__, P.d, P.G, P.Gr ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFVT1 ],
              couplings = {(0,0):C.GC_17})

V_37 = Vertex(name = 'V_37',
              particles = [ P.s__tilde__, P.s, P.G, P.Gr ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFVT1 ],
              couplings = {(0,0):C.GC_17})

V_38 = Vertex(name = 'V_38',
              particles = [ P.b__tilde__, P.b, P.G, P.Gr ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFVT1 ],
              couplings = {(0,0):C.GC_17})

V_39 = Vertex(name = 'V_39',
              particles = [ P.A, P.W__minus__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.VVV1 ],
              couplings = {(0,0):C.GC_55})

V_40 = Vertex(name = 'V_40',
              particles = [ P.A, P.W__minus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVVT1 ],
              couplings = {(0,0):C.GC_15})

V_41 = Vertex(name = 'V_41',
              particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
              color = [ '1' ],
              lorentz = [ L.VVSS1 ],
              couplings = {(0,0):C.GC_22})

V_42 = Vertex(name = 'V_42',
              particles = [ P.W__minus__, P.W__plus__, P.H ],
              color = [ '1' ],
              lorentz = [ L.VVS1 ],
              couplings = {(0,0):C.GC_67})

V_43 = Vertex(name = 'V_43',
              particles = [ P.A, P.A, P.W__minus__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.VVVV2 ],
              couplings = {(0,0):C.GC_59})

V_44 = Vertex(name = 'V_44',
              particles = [ P.W__minus__, P.W__plus__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.VVV1 ],
              couplings = {(0,0):C.GC_7})

V_45 = Vertex(name = 'V_45',
              particles = [ P.W__minus__, P.W__plus__, P.H, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVSST1 ],
              couplings = {(0,0):C.GC_23})

V_46 = Vertex(name = 'V_46',
              particles = [ P.W__minus__, P.W__plus__, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVST1 ],
              couplings = {(0,0):C.GC_68})

V_47 = Vertex(name = 'V_47',
              particles = [ P.A, P.A, P.W__minus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVVVT4 ],
              couplings = {(0,0):C.GC_16})

V_48 = Vertex(name = 'V_48',
              particles = [ P.W__minus__, P.W__plus__, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVVT1 ],
              couplings = {(0,0):C.GC_51})

V_49 = Vertex(name = 'V_49',
              particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.VVVV2 ],
              couplings = {(0,0):C.GC_8})

V_50 = Vertex(name = 'V_50',
              particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVVVT4 ],
              couplings = {(0,0):C.GC_24})

V_51 = Vertex(name = 'V_51',
              particles = [ P.d__tilde__, P.d, P.H ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_80})

V_52 = Vertex(name = 'V_52',
              particles = [ P.s__tilde__, P.s, P.H ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_89})

V_53 = Vertex(name = 'V_53',
              particles = [ P.b__tilde__, P.b, P.H ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_74})

V_54 = Vertex(name = 'V_54',
              particles = [ P.d__tilde__, P.d, P.H, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_81})

V_55 = Vertex(name = 'V_55',
              particles = [ P.s__tilde__, P.s, P.H, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_90})

V_56 = Vertex(name = 'V_56',
              particles = [ P.b__tilde__, P.b, P.H, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_75})

V_57 = Vertex(name = 'V_57',
              particles = [ P.e__plus__, P.e__minus__, P.H ],
              color = [ '1' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_83})

V_58 = Vertex(name = 'V_58',
              particles = [ P.m__plus__, P.m__minus__, P.H ],
              color = [ '1' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_86})

V_59 = Vertex(name = 'V_59',
              particles = [ P.tt__plus__, P.tt__minus__, P.H ],
              color = [ '1' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_95})

V_60 = Vertex(name = 'V_60',
              particles = [ P.e__plus__, P.e__minus__, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_84})

V_61 = Vertex(name = 'V_61',
              particles = [ P.m__plus__, P.m__minus__, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_87})

V_62 = Vertex(name = 'V_62',
              particles = [ P.tt__plus__, P.tt__minus__, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_96})

V_63 = Vertex(name = 'V_63',
              particles = [ P.u__tilde__, P.u, P.H ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_98})

V_64 = Vertex(name = 'V_64',
              particles = [ P.c__tilde__, P.c, P.H ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_77})

V_65 = Vertex(name = 'V_65',
              particles = [ P.t__tilde__, P.t, P.H ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS1 ],
              couplings = {(0,0):C.GC_92})

V_66 = Vertex(name = 'V_66',
              particles = [ P.u__tilde__, P.u, P.H, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_99})

V_67 = Vertex(name = 'V_67',
              particles = [ P.c__tilde__, P.c, P.H, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_78})

V_68 = Vertex(name = 'V_68',
              particles = [ P.t__tilde__, P.t, P.H, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFST1 ],
              couplings = {(0,0):C.GC_93})

V_69 = Vertex(name = 'V_69',
              particles = [ P.A, P.W__minus__, P.W__plus__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.VVVV5 ],
              couplings = {(0,0):C.GC_56})

V_70 = Vertex(name = 'V_70',
              particles = [ P.A, P.W__minus__, P.W__plus__, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVVVT3 ],
              couplings = {(0,0):C.GC_52})

V_71 = Vertex(name = 'V_71',
              particles = [ P.Z, P.Z, P.H, P.H ],
              color = [ '1' ],
              lorentz = [ L.VVSS1 ],
              couplings = {(0,0):C.GC_62})

V_72 = Vertex(name = 'V_72',
              particles = [ P.Z, P.Z, P.H ],
              color = [ '1' ],
              lorentz = [ L.VVS1 ],
              couplings = {(0,0):C.GC_70})

V_73 = Vertex(name = 'V_73',
              particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
              color = [ '1' ],
              lorentz = [ L.VVVV2 ],
              couplings = {(0,0):C.GC_9})

V_74 = Vertex(name = 'V_74',
              particles = [ P.Z, P.Z, P.H, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVSST1 ],
              couplings = {(0,0):C.GC_64})

V_75 = Vertex(name = 'V_75',
              particles = [ P.Z, P.Z, P.H, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVST1 ],
              couplings = {(0,0):C.GC_71})

V_76 = Vertex(name = 'V_76',
              particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.VVVVT4 ],
              couplings = {(0,0):C.GC_25})

V_77 = Vertex(name = 'V_77',
              particles = [ P.e__plus__, P.e__minus__, P.A ],
              color = [ '1' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_3})

V_78 = Vertex(name = 'V_78',
              particles = [ P.m__plus__, P.m__minus__, P.A ],
              color = [ '1' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_3})

V_79 = Vertex(name = 'V_79',
              particles = [ P.tt__plus__, P.tt__minus__, P.A ],
              color = [ '1' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_3})

V_80 = Vertex(name = 'V_80',
              particles = [ P.e__plus__, P.e__minus__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.FFV2, L.FFV4 ],
              couplings = {(0,0):C.GC_36,(0,1):C.GC_54})

V_81 = Vertex(name = 'V_81',
              particles = [ P.m__plus__, P.m__minus__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.FFV2, L.FFV4 ],
              couplings = {(0,0):C.GC_36,(0,1):C.GC_54})

V_82 = Vertex(name = 'V_82',
              particles = [ P.tt__plus__, P.tt__minus__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.FFV2, L.FFV4 ],
              couplings = {(0,1):C.GC_54,(0,0):C.GC_36})

V_83 = Vertex(name = 'V_83',
              particles = [ P.ve__tilde__, P.ve, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFVT6 ],
              couplings = {(0,0):C.GC_61})

V_84 = Vertex(name = 'V_84',
              particles = [ P.vm__tilde__, P.vm, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFVT6 ],
              couplings = {(0,0):C.GC_61})

V_85 = Vertex(name = 'V_85',
              particles = [ P.vt__tilde__, P.vt, P.Z, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFVT6 ],
              couplings = {(0,0):C.GC_61})

V_86 = Vertex(name = 'V_86',
              particles = [ P.u__tilde__, P.u, P.A, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFVT7 ],
              couplings = {(0,0):C.GC_13})

V_87 = Vertex(name = 'V_87',
              particles = [ P.c__tilde__, P.c, P.A, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFVT10 ],
              couplings = {(0,0):C.GC_14})

V_88 = Vertex(name = 'V_88',
              particles = [ P.t__tilde__, P.t, P.A, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFVT10 ],
              couplings = {(0,0):C.GC_14})

V_89 = Vertex(name = 'V_89',
              particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFVT5 ],
              couplings = {(0,0):C.GC_38})

V_90 = Vertex(name = 'V_90',
              particles = [ P.vm__tilde__, P.m__minus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFVT5 ],
              couplings = {(0,0):C.GC_38})

V_91 = Vertex(name = 'V_91',
              particles = [ P.vt__tilde__, P.tt__minus__, P.W__plus__, P.Gr ],
              color = [ '1' ],
              lorentz = [ L.FFVT5 ],
              couplings = {(0,0):C.GC_38})

V_92 = Vertex(name = 'V_92',
              particles = [ P.u__tilde__, P.u, P.Z, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFVT11, L.FFVT6 ],
              couplings = {(0,1):C.GC_50,(0,0):C.GC_57})

V_93 = Vertex(name = 'V_93',
              particles = [ P.c__tilde__, P.c, P.Z, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFVT11, L.FFVT6 ],
              couplings = {(0,1):C.GC_50,(0,0):C.GC_57})

V_94 = Vertex(name = 'V_94',
              particles = [ P.t__tilde__, P.t, P.Z, P.Gr ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFVT11, L.FFVT6 ],
              couplings = {(0,1):C.GC_50,(0,0):C.GC_57})

V_95 = Vertex(name = 'V_95',
              particles = [ P.u__tilde__, P.u, P.A ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_2})

V_96 = Vertex(name = 'V_96',
              particles = [ P.c__tilde__, P.c, P.A ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_2})

V_97 = Vertex(name = 'V_97',
              particles = [ P.t__tilde__, P.t, P.A ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_2})

V_98 = Vertex(name = 'V_98',
              particles = [ P.d__tilde__, P.u, P.W__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV2 ],
              couplings = {(0,0):C.GC_27})

V_99 = Vertex(name = 'V_99',
              particles = [ P.s__tilde__, P.u, P.W__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV2 ],
              couplings = {(0,0):C.GC_28})

V_100 = Vertex(name = 'V_100',
               particles = [ P.b__tilde__, P.u, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_29})

V_101 = Vertex(name = 'V_101',
               particles = [ P.d__tilde__, P.c, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_30})

V_102 = Vertex(name = 'V_102',
               particles = [ P.s__tilde__, P.c, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_31})

V_103 = Vertex(name = 'V_103',
               particles = [ P.b__tilde__, P.c, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_32})

V_104 = Vertex(name = 'V_104',
               particles = [ P.d__tilde__, P.t, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_33})

V_105 = Vertex(name = 'V_105',
               particles = [ P.s__tilde__, P.t, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_34})

V_106 = Vertex(name = 'V_106',
               particles = [ P.b__tilde__, P.t, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_35})

V_107 = Vertex(name = 'V_107',
               particles = [ P.u__tilde__, P.u, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV5 ],
               couplings = {(0,0):C.GC_37,(0,1):C.GC_53})

V_108 = Vertex(name = 'V_108',
               particles = [ P.c__tilde__, P.c, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV5 ],
               couplings = {(0,0):C.GC_37,(0,1):C.GC_53})

V_109 = Vertex(name = 'V_109',
               particles = [ P.t__tilde__, P.t, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV5 ],
               couplings = {(0,0):C.GC_37,(0,1):C.GC_53})

V_110 = Vertex(name = 'V_110',
               particles = [ P.u__tilde__, P.d, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_101})

V_111 = Vertex(name = 'V_111',
               particles = [ P.c__tilde__, P.d, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_107})

V_112 = Vertex(name = 'V_112',
               particles = [ P.t__tilde__, P.d, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_113})

V_113 = Vertex(name = 'V_113',
               particles = [ P.u__tilde__, P.s, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_103})

V_114 = Vertex(name = 'V_114',
               particles = [ P.c__tilde__, P.s, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_109})

V_115 = Vertex(name = 'V_115',
               particles = [ P.t__tilde__, P.s, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_115})

V_116 = Vertex(name = 'V_116',
               particles = [ P.u__tilde__, P.b, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_105})

V_117 = Vertex(name = 'V_117',
               particles = [ P.c__tilde__, P.b, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_111})

V_118 = Vertex(name = 'V_118',
               particles = [ P.t__tilde__, P.b, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_117})

V_119 = Vertex(name = 'V_119',
               particles = [ P.e__plus__, P.e__minus__, P.A, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT9 ],
               couplings = {(0,0):C.GC_15})

V_120 = Vertex(name = 'V_120',
               particles = [ P.m__plus__, P.m__minus__, P.A, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT9 ],
               couplings = {(0,0):C.GC_15})

V_121 = Vertex(name = 'V_121',
               particles = [ P.tt__plus__, P.tt__minus__, P.A, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT9 ],
               couplings = {(0,0):C.GC_15})

V_122 = Vertex(name = 'V_122',
               particles = [ P.e__plus__, P.e__minus__, P.Z, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT6, L.FFVT8 ],
               couplings = {(0,0):C.GC_49,(0,1):C.GC_58})

V_123 = Vertex(name = 'V_123',
               particles = [ P.m__plus__, P.m__minus__, P.Z, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT6, L.FFVT8 ],
               couplings = {(0,0):C.GC_49,(0,1):C.GC_58})

V_124 = Vertex(name = 'V_124',
               particles = [ P.tt__plus__, P.tt__minus__, P.Z, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT6, L.FFVT8 ],
               couplings = {(0,0):C.GC_49,(0,1):C.GC_58})

V_125 = Vertex(name = 'V_125',
               particles = [ P.e__plus__, P.ve, P.W__minus__, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_38})

V_126 = Vertex(name = 'V_126',
               particles = [ P.m__plus__, P.vm, P.W__minus__, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_38})

V_127 = Vertex(name = 'V_127',
               particles = [ P.tt__plus__, P.vt, P.W__minus__, P.Gr ],
               color = [ '1' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_38})

V_128 = Vertex(name = 'V_128',
               particles = [ P.d__tilde__, P.d, P.A ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_1})

V_129 = Vertex(name = 'V_129',
               particles = [ P.s__tilde__, P.s, P.A ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_1})

V_130 = Vertex(name = 'V_130',
               particles = [ P.b__tilde__, P.b, P.A ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_1})

V_131 = Vertex(name = 'V_131',
               particles = [ P.d__tilde__, P.d, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV3 ],
               couplings = {(0,0):C.GC_36,(0,1):C.GC_53})

V_132 = Vertex(name = 'V_132',
               particles = [ P.s__tilde__, P.s, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV3 ],
               couplings = {(0,1):C.GC_53,(0,0):C.GC_36})

V_133 = Vertex(name = 'V_133',
               particles = [ P.b__tilde__, P.b, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV3 ],
               couplings = {(0,0):C.GC_36,(0,1):C.GC_53})

V_134 = Vertex(name = 'V_134',
               particles = [ P.ve__tilde__, P.ve, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_60})

V_135 = Vertex(name = 'V_135',
               particles = [ P.vm__tilde__, P.vm, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_60})

V_136 = Vertex(name = 'V_136',
               particles = [ P.vt__tilde__, P.vt, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_60})

V_137 = Vertex(name = 'V_137',
               particles = [ P.d__tilde__, P.u, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_102,(0,1):C.GC_39})

V_138 = Vertex(name = 'V_138',
               particles = [ P.s__tilde__, P.u, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_108,(0,1):C.GC_40})

V_139 = Vertex(name = 'V_139',
               particles = [ P.b__tilde__, P.u, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_114,(0,1):C.GC_41})

V_140 = Vertex(name = 'V_140',
               particles = [ P.d__tilde__, P.c, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_104,(0,1):C.GC_42})

V_141 = Vertex(name = 'V_141',
               particles = [ P.s__tilde__, P.c, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_110,(0,1):C.GC_43})

V_142 = Vertex(name = 'V_142',
               particles = [ P.b__tilde__, P.c, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_116,(0,1):C.GC_44})

V_143 = Vertex(name = 'V_143',
               particles = [ P.d__tilde__, P.t, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_106,(0,1):C.GC_45})

V_144 = Vertex(name = 'V_144',
               particles = [ P.s__tilde__, P.t, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_112,(0,1):C.GC_46})

V_145 = Vertex(name = 'V_145',
               particles = [ P.b__tilde__, P.t, P.W__minus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT2, L.FFVT3 ],
               couplings = {(0,0):C.GC_118,(0,1):C.GC_47})

V_146 = Vertex(name = 'V_146',
               particles = [ P.d__tilde__, P.d, P.A, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT10 ],
               couplings = {(0,0):C.GC_13})

V_147 = Vertex(name = 'V_147',
               particles = [ P.s__tilde__, P.s, P.A, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT10 ],
               couplings = {(0,0):C.GC_13})

V_148 = Vertex(name = 'V_148',
               particles = [ P.b__tilde__, P.b, P.A, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT10 ],
               couplings = {(0,0):C.GC_13})

V_149 = Vertex(name = 'V_149',
               particles = [ P.d__tilde__, P.d, P.Z, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT4, L.FFVT8 ],
               couplings = {(0,1):C.GC_57,(0,0):C.GC_48})

V_150 = Vertex(name = 'V_150',
               particles = [ P.s__tilde__, P.s, P.Z, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT6, L.FFVT8 ],
               couplings = {(0,0):C.GC_49,(0,1):C.GC_57})

V_151 = Vertex(name = 'V_151',
               particles = [ P.b__tilde__, P.b, P.Z, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT6, L.FFVT8 ],
               couplings = {(0,0):C.GC_49,(0,1):C.GC_57})

V_152 = Vertex(name = 'V_152',
               particles = [ P.e__plus__, P.ve, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_26})

V_153 = Vertex(name = 'V_153',
               particles = [ P.m__plus__, P.vm, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_26})

V_154 = Vertex(name = 'V_154',
               particles = [ P.tt__plus__, P.vt, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_26})

V_155 = Vertex(name = 'V_155',
               particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_26})

V_156 = Vertex(name = 'V_156',
               particles = [ P.vm__tilde__, P.m__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_26})

V_157 = Vertex(name = 'V_157',
               particles = [ P.vt__tilde__, P.tt__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_26})

V_158 = Vertex(name = 'V_158',
               particles = [ P.u__tilde__, P.d, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_102})

V_159 = Vertex(name = 'V_159',
               particles = [ P.c__tilde__, P.d, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_108})

V_160 = Vertex(name = 'V_160',
               particles = [ P.t__tilde__, P.d, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_114})

V_161 = Vertex(name = 'V_161',
               particles = [ P.u__tilde__, P.s, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_104})

V_162 = Vertex(name = 'V_162',
               particles = [ P.c__tilde__, P.s, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_110})

V_163 = Vertex(name = 'V_163',
               particles = [ P.t__tilde__, P.s, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_116})

V_164 = Vertex(name = 'V_164',
               particles = [ P.u__tilde__, P.b, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_106})

V_165 = Vertex(name = 'V_165',
               particles = [ P.c__tilde__, P.b, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_112})

V_166 = Vertex(name = 'V_166',
               particles = [ P.t__tilde__, P.b, P.W__plus__, P.Gr ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFVT5 ],
               couplings = {(0,0):C.GC_118})

