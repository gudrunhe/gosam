# This file was automatically created from UFO model SMEFTsim_U35_MwScheme_UFO
# by applying the 'modify_UFO.py' script. Only SM vertices and those containing
# one of the following coefficients have been kept:
# cHW  cHB  cHWB 


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
	particles = [ P.a, P.W__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVV5, L.VVV6 ],
	couplings = {(0, 0):C.GC_3, (0, 1):C.GC_417})

V_5 = Vertex(name = 'V_5',
	particles = [ P.W__minus__, P.W__plus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVV4, L.VVV5 ],
	couplings = {(0, 0):C.GC_337, (0, 1):C.GC_137})

V_9 = Vertex(name = 'V_9',
	particles = [ P.g, P.g, P.g ],
	color = [ 'f(1,2,3)' ],
	lorentz = [ L.VVV5 ],
	couplings = {(0, 0):C.GC_7})

V_10 = Vertex(name = 'V_10',
	particles = [ P.g, P.g, P.g, P.g ],
	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
	lorentz = [ L.VVVV1, L.VVVV9, L.VVVV10 ],
	couplings = {(0, 0):C.GC_8, (1, 1):C.GC_8, (2, 2):C.GC_8})

V_13 = Vertex(name = 'V_13',
	particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVVV8 ],
	couplings = {(0, 0):C.GC_5})

V_17 = Vertex(name = 'V_17',
	particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVVV8 ],
	couplings = {(0, 0):C.GC_422})

V_18 = Vertex(name = 'V_18',
	particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVVV11 ],
	couplings = {(0, 0):C.GC_138})

V_19 = Vertex(name = 'V_19',
	particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVVV11 ],
	couplings = {(0, 0):C.GC_449})

V_24 = Vertex(name = 'V_24',
	particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVVV8 ],
	couplings = {(0, 0):C.GC_98})

V_30 = Vertex(name = 'V_30',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVVV8 ],
	couplings = {(0, 0):C.GC_100})

V_34 = Vertex(name = 'V_34',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVVV8 ],
	couplings = {(0, 0):C.GC_423})

V_40 = Vertex(name = 'V_40',
	particles = [ P.a, P.a, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_52})

V_41 = Vertex(name = 'V_41',
	particles = [ P.a, P.a, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_201})

V_42 = Vertex(name = 'V_42',
	particles = [ P.a, P.a, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_219})

V_44 = Vertex(name = 'V_44',
	particles = [ P.a, P.a, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_268})

V_45 = Vertex(name = 'V_45',
	particles = [ P.a, P.a, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_321})

V_46 = Vertex(name = 'V_46',
	particles = [ P.a, P.a, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_328})

V_50 = Vertex(name = 'V_50',
	particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS3, L.VVSS4 ],
	couplings = {(0, 0):C.GC_97, (0, 1):C.GC_22})

V_55 = Vertex(name = 'V_55',
	particles = [ P.W__minus__, P.W__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS3, L.VVS4 ],
	couplings = {(0, 0):C.GC_283, (0, 1):C.GC_266})

V_60 = Vertex(name = 'V_60',
	particles = [ P.a, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_221})

V_61 = Vertex(name = 'V_61',
	particles = [ P.a, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_198})

V_62 = Vertex(name = 'V_62',
	particles = [ P.a, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_200})

V_64 = Vertex(name = 'V_64',
	particles = [ P.a, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_447})

V_65 = Vertex(name = 'V_65',
	particles = [ P.a, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_318})

V_66 = Vertex(name = 'V_66',
	particles = [ P.a, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_320})

V_67 = Vertex(name = 'V_67',
	particles = [ P.Z, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS3, L.VVSS4 ],
	couplings = {(0, 0):C.GC_99, (0, 1):C.GC_54})

V_68 = Vertex(name = 'V_68',
	particles = [ P.Z, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_202})

V_69 = Vertex(name = 'V_69',
	particles = [ P.Z, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS4 ],
	couplings = {(0, 0):C.GC_217})

V_72 = Vertex(name = 'V_72',
	particles = [ P.Z, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS3, L.VVS4 ],
	couplings = {(0, 0):C.GC_284, (0, 1):C.GC_270})

V_73 = Vertex(name = 'V_73',
	particles = [ P.Z, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_322})

V_74 = Vertex(name = 'V_74',
	particles = [ P.Z, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS4 ],
	couplings = {(0, 0):C.GC_326})

V_80 = Vertex(name = 'V_80',
	particles = [ P.a, P.W__minus__, P.W__plus__, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVSS4, L.VVVSS6 ],
	couplings = {(0, 0):C.GC_159, (0, 1):C.GC_62})

V_81 = Vertex(name = 'V_81',
	particles = [ P.a, P.W__minus__, P.W__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVS4, L.VVVS6 ],
	couplings = {(0, 0):C.GC_314, (0, 1):C.GC_272})

V_82 = Vertex(name = 'V_82',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVSS5, L.VVVSS6 ],
	couplings = {(0, 0):C.GC_63, (0, 1):C.GC_158})

V_83 = Vertex(name = 'V_83',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVS5, L.VVVS6 ],
	couplings = {(0, 0):C.GC_273, (0, 1):C.GC_313})

V_84 = Vertex(name = 'V_84',
	particles = [ P.H, P.H, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_9})

V_91 = Vertex(name = 'V_91',
	particles = [ P.H, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSS1 ],
	couplings = {(0, 0):C.GC_260})

V_101 = Vertex(name = 'V_101',
	particles = [ P.a, P.a, P.W__minus__, P.W__plus__, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVSS2 ],
	couplings = {(0, 0):C.GC_68})

V_102 = Vertex(name = 'V_102',
	particles = [ P.a, P.a, P.W__minus__, P.W__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVS6 ],
	couplings = {(0, 0):C.GC_276})

V_103 = Vertex(name = 'V_103',
	particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVSS2 ],
	couplings = {(0, 0):C.GC_101})

V_104 = Vertex(name = 'V_104',
	particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVS6 ],
	couplings = {(0, 0):C.GC_285})

V_105 = Vertex(name = 'V_105',
	particles = [ P.a, P.W__minus__, P.W__plus__, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVSS5 ],
	couplings = {(0, 0):C.GC_166})

V_106 = Vertex(name = 'V_106',
	particles = [ P.a, P.W__minus__, P.W__plus__, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVS9 ],
	couplings = {(0, 0):C.GC_317})

V_109 = Vertex(name = 'V_109',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVSS2 ],
	couplings = {(0, 0):C.GC_103})

V_110 = Vertex(name = 'V_110',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVVVS6 ],
	couplings = {(0, 0):C.GC_287})

V_188 = Vertex(name = 'V_188',
	particles = [ P.e__plus__, P.e__minus__, P.a ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_4})

V_192 = Vertex(name = 'V_192',
	particles = [ P.e__plus__, P.e__minus__, P.a ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_417})

V_193 = Vertex(name = 'V_193',
	particles = [ P.mu__plus__, P.mu__minus__, P.a ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_4})

V_197 = Vertex(name = 'V_197',
	particles = [ P.mu__plus__, P.mu__minus__, P.a ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_417})

V_198 = Vertex(name = 'V_198',
	particles = [ P.ta__plus__, P.ta__minus__, P.a ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_4})

V_202 = Vertex(name = 'V_202',
	particles = [ P.ta__plus__, P.ta__minus__, P.a ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_417})

V_203 = Vertex(name = 'V_203',
	particles = [ P.e__plus__, P.e__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_197, (0, 1):C.GC_136})

V_204 = Vertex(name = 'V_204',
	particles = [ P.e__plus__, P.e__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_338})

V_208 = Vertex(name = 'V_208',
	particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_197, (0, 1):C.GC_136})

V_209 = Vertex(name = 'V_209',
	particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_338})

V_213 = Vertex(name = 'V_213',
	particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_197, (0, 1):C.GC_136})

V_214 = Vertex(name = 'V_214',
	particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_338})

V_218 = Vertex(name = 'V_218',
	particles = [ P.d__tilde__, P.d, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_1})

V_222 = Vertex(name = 'V_222',
	particles = [ P.d__tilde__, P.d, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_415})

V_223 = Vertex(name = 'V_223',
	particles = [ P.s__tilde__, P.s, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_1})

V_227 = Vertex(name = 'V_227',
	particles = [ P.s__tilde__, P.s, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_415})

V_228 = Vertex(name = 'V_228',
	particles = [ P.b__tilde__, P.b, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_1})

V_232 = Vertex(name = 'V_232',
	particles = [ P.b__tilde__, P.b, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_415})

V_233 = Vertex(name = 'V_233',
	particles = [ P.u__tilde__, P.u, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_2})

V_237 = Vertex(name = 'V_237',
	particles = [ P.u__tilde__, P.u, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_416})

V_238 = Vertex(name = 'V_238',
	particles = [ P.c__tilde__, P.c, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_2})

V_242 = Vertex(name = 'V_242',
	particles = [ P.c__tilde__, P.c, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_416})

V_243 = Vertex(name = 'V_243',
	particles = [ P.t__tilde__, P.t, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_2})

V_247 = Vertex(name = 'V_247',
	particles = [ P.t__tilde__, P.t, P.a ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_416})

V_248 = Vertex(name = 'V_248',
	particles = [ P.d__tilde__, P.d, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_6})

V_249 = Vertex(name = 'V_249',
	particles = [ P.s__tilde__, P.s, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_6})

V_250 = Vertex(name = 'V_250',
	particles = [ P.b__tilde__, P.b, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_6})

V_251 = Vertex(name = 'V_251',
	particles = [ P.u__tilde__, P.u, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_6})

V_252 = Vertex(name = 'V_252',
	particles = [ P.c__tilde__, P.c, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_6})

V_253 = Vertex(name = 'V_253',
	particles = [ P.t__tilde__, P.t, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_6})

V_254 = Vertex(name = 'V_254',
	particles = [ P.d__tilde__, P.u, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_126})

V_258 = Vertex(name = 'V_258',
	particles = [ P.s__tilde__, P.u, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_127})

V_262 = Vertex(name = 'V_262',
	particles = [ P.b__tilde__, P.u, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_128})

V_266 = Vertex(name = 'V_266',
	particles = [ P.d__tilde__, P.c, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_129})

V_270 = Vertex(name = 'V_270',
	particles = [ P.s__tilde__, P.c, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_130})

V_274 = Vertex(name = 'V_274',
	particles = [ P.b__tilde__, P.c, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_131})

V_278 = Vertex(name = 'V_278',
	particles = [ P.d__tilde__, P.t, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_132})

V_282 = Vertex(name = 'V_282',
	particles = [ P.s__tilde__, P.t, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_133})

V_286 = Vertex(name = 'V_286',
	particles = [ P.b__tilde__, P.t, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_134})

V_326 = Vertex(name = 'V_326',
	particles = [ P.e__plus__, P.ve, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_125})

V_328 = Vertex(name = 'V_328',
	particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_125})

V_330 = Vertex(name = 'V_330',
	particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_125})

V_340 = Vertex(name = 'V_340',
	particles = [ P.u__tilde__, P.d, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_1465})

V_344 = Vertex(name = 'V_344',
	particles = [ P.c__tilde__, P.d, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_2080})

V_348 = Vertex(name = 'V_348',
	particles = [ P.t__tilde__, P.d, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_2695})

V_352 = Vertex(name = 'V_352',
	particles = [ P.u__tilde__, P.s, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_1670})

V_356 = Vertex(name = 'V_356',
	particles = [ P.c__tilde__, P.s, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_2285})

V_360 = Vertex(name = 'V_360',
	particles = [ P.t__tilde__, P.s, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_2901})

V_364 = Vertex(name = 'V_364',
	particles = [ P.u__tilde__, P.b, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_1875})

V_368 = Vertex(name = 'V_368',
	particles = [ P.c__tilde__, P.b, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_2490})

V_372 = Vertex(name = 'V_372',
	particles = [ P.t__tilde__, P.b, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_3107})

V_412 = Vertex(name = 'V_412',
	particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_125})

V_414 = Vertex(name = 'V_414',
	particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_125})

V_416 = Vertex(name = 'V_416',
	particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_125})

V_439 = Vertex(name = 'V_439',
	particles = [ P.d__tilde__, P.d, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_195, (0, 1):C.GC_136})

V_440 = Vertex(name = 'V_440',
	particles = [ P.d__tilde__, P.d, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_335})

V_444 = Vertex(name = 'V_444',
	particles = [ P.s__tilde__, P.s, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_195, (0, 1):C.GC_136})

V_445 = Vertex(name = 'V_445',
	particles = [ P.s__tilde__, P.s, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_335})

V_449 = Vertex(name = 'V_449',
	particles = [ P.b__tilde__, P.b, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_195, (0, 1):C.GC_136})

V_450 = Vertex(name = 'V_450',
	particles = [ P.b__tilde__, P.b, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_335})

V_466 = Vertex(name = 'V_466',
	particles = [ P.u__tilde__, P.u, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_196, (0, 1):C.GC_135})

V_467 = Vertex(name = 'V_467',
	particles = [ P.u__tilde__, P.u, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_336})

V_471 = Vertex(name = 'V_471',
	particles = [ P.c__tilde__, P.c, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_196, (0, 1):C.GC_135})

V_472 = Vertex(name = 'V_472',
	particles = [ P.c__tilde__, P.c, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_336})

V_476 = Vertex(name = 'V_476',
	particles = [ P.t__tilde__, P.t, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1, L.FFV3 ],
	couplings = {(0, 0):C.GC_196, (0, 1):C.GC_135})

V_477 = Vertex(name = 'V_477',
	particles = [ P.t__tilde__, P.t, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_336})

V_493 = Vertex(name = 'V_493',
	particles = [ P.ve__tilde__, P.ve, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_135})

V_497 = Vertex(name = 'V_497',
	particles = [ P.vm__tilde__, P.vm, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_135})

V_501 = Vertex(name = 'V_501',
	particles = [ P.vt__tilde__, P.vt, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV3 ],
	couplings = {(0, 0):C.GC_135})

V_577 = Vertex(name = 'V_577',
	particles = [ P.d__tilde__, P.d, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_585})

V_583 = Vertex(name = 'V_583',
	particles = [ P.s__tilde__, P.s, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_851})

V_589 = Vertex(name = 'V_589',
	particles = [ P.b__tilde__, P.b, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_451})

V_595 = Vertex(name = 'V_595',
	particles = [ P.e__plus__, P.e__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_661})

V_601 = Vertex(name = 'V_601',
	particles = [ P.mu__plus__, P.mu__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_756})

V_607 = Vertex(name = 'V_607',
	particles = [ P.ta__plus__, P.ta__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_1113})

V_613 = Vertex(name = 'V_613',
	particles = [ P.u__tilde__, P.u, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_1244})

V_619 = Vertex(name = 'V_619',
	particles = [ P.c__tilde__, P.c, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_509})

V_625 = Vertex(name = 'V_625',
	particles = [ P.t__tilde__, P.t, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_945})

