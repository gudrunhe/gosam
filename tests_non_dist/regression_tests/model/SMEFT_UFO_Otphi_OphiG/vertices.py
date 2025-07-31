
# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 13.0.1 for Linux x86 (64-bit) (January 29, 2022)
# Date: Mon 8 Jan 2024 12:54:06


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
	particles = [ P.G0, P.G0, P.G0, P.G0 ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_59})

V_2 = Vertex(name = 'V_2',
	particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_57})

V_3 = Vertex(name = 'V_3',
	particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_58})

V_4 = Vertex(name = 'V_4',
	particles = [ P.G0, P.G0, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSS1 ],
	couplings = {(0, 0):C.GC_55})

V_5 = Vertex(name = 'V_5',
	particles = [ P.G__minus__, P.G__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSS1 ],
	couplings = {(0, 0):C.GC_55})

V_6 = Vertex(name = 'V_6',
	particles = [ P.G0, P.G0, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_57})

V_7 = Vertex(name = 'V_7',
	particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_57})

V_8 = Vertex(name = 'V_8',
	particles = [ P.H, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSS1 ],
	couplings = {(0, 0):C.GC_56})

V_9 = Vertex(name = 'V_9',
	particles = [ P.H, P.H, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.SSSS1 ],
	couplings = {(0, 0):C.GC_59})

V_10 = Vertex(name = 'V_10',
	particles = [ P.ghWp, P.ghZ__tilde__, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_483_1})

V_11 = Vertex(name = 'V_11',
	particles = [ P.ghWm, P.ghZ__tilde__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_483_1})

V_12 = Vertex(name = 'V_12',
	particles = [ P.ghWm, P.ghWm__tilde__, P.G0 ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_461_1})

V_13 = Vertex(name = 'V_13',
	particles = [ P.ghWp, P.ghWp__tilde__, P.G0 ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_459_1})

V_14 = Vertex(name = 'V_14',
	particles = [ P.ghWm, P.ghWm__tilde__, P.H ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_460_1})

V_15 = Vertex(name = 'V_15',
	particles = [ P.ghWp, P.ghWp__tilde__, P.H ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_460_1})

V_16 = Vertex(name = 'V_16',
	particles = [ P.ghZ, P.ghWm__tilde__, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_469_1})

V_17 = Vertex(name = 'V_17',
	particles = [ P.ghZ, P.ghWp__tilde__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_469_1})

V_18 = Vertex(name = 'V_18',
	particles = [ P.ghZ, P.ghZ__tilde__, P.H ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_472_1})

V_19 = Vertex(name = 'V_19',
	particles = [ P.ghWp, P.ghA__tilde__, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_493_1})

V_20 = Vertex(name = 'V_20',
	particles = [ P.ghWm, P.ghA__tilde__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUS1 ],
	couplings = {(0, 0):C.GC_493_1})

V_21 = Vertex(name = 'V_21',
	particles = [ P.A, P.A, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_463})

V_22 = Vertex(name = 'V_22',
	particles = [ P.ghWm, P.ghWm__tilde__, P.A ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_487_1})

V_23 = Vertex(name = 'V_23',
	particles = [ P.ghWp, P.ghWp__tilde__, P.A ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_488_1})

V_24 = Vertex(name = 'V_24',
	particles = [ P.A, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_488})

V_33 = Vertex(name = 'V_33',
	particles = [ P.g, P.g, P.g ],
	color = [ 'f(1,2,3)' ],
	lorentz = [ L.VVV1 ],
	couplings = {(0, 0):C.GC_335})

V_42 = Vertex(name = 'V_42',
	particles = [ P.g, P.g, P.g, P.g ],
	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
	lorentz = [ L.VVVV1, L.VVVV3, L.VVVV4 ],
	couplings = {(1, 1):C.GC_393, (0, 0):C.GC_393, (2, 2):C.GC_393})

V_51 = Vertex(name = 'V_51',
	particles = [ P.ghG, P.ghG__tilde__, P.g ],
	color = [ 'f(1,2,3)' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_335_1})

V_113 = Vertex(name = 'V_113',
	particles = [ P.t__tilde__, P.t, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS3, L.FFS4 ],
	couplings = {(0, 0):C.GC_54, (0, 1):C.GC_54})

V_168 = Vertex(name = 'V_168',
	particles = [ P.b__tilde__, P.b, P.G0 ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS1 ],
	couplings = {(0, 0):C.GC_18})

V_177 = Vertex(name = 'V_177',
	particles = [ P.b__tilde__, P.b, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_17})

V_186 = Vertex(name = 'V_186',
	particles = [ P.t__tilde__, P.b, P.G__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS3, L.FFS4 ],
	couplings = {(0, 0):C.GC_68, (0, 1):C.GC_77})

V_195 = Vertex(name = 'V_195',
	particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
	color = [ '1' ],
	lorentz = [ L.FFS1 ],
	couplings = {(0, 0):C.GC_36})

V_204 = Vertex(name = 'V_204',
	particles = [ P.ta__plus__, P.ta__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.FFS2 ],
	couplings = {(0, 0):C.GC_35})

V_213 = Vertex(name = 'V_213',
	particles = [ P.t__tilde__, P.t, P.G0 ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS1 ],
	couplings = {(0, 0):C.GC_53})

V_258 = Vertex(name = 'V_258',
	particles = [ P.b__tilde__, P.t, P.G__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS3, L.FFS4 ],
	couplings = {(0, 0):C.GC_86, (0, 1):C.GC_95})

V_313 = Vertex(name = 'V_313',
	particles = [ P.A, P.W__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVS1 ],
	couplings = {(0, 0):C.GC_489})

V_314 = Vertex(name = 'V_314',
	particles = [ P.A, P.W__minus__, P.G0, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_490})

V_315 = Vertex(name = 'V_315',
	particles = [ P.A, P.W__minus__, P.G__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_491})

V_316 = Vertex(name = 'V_316',
	particles = [ P.W__minus__, P.G0, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_435})

V_317 = Vertex(name = 'V_317',
	particles = [ P.ghA, P.ghWm__tilde__, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_488_1})

V_318 = Vertex(name = 'V_318',
	particles = [ P.ghWp, P.ghZ__tilde__, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_465_1})

V_319 = Vertex(name = 'V_319',
	particles = [ P.ghWp, P.ghA__tilde__, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_487_1})

V_320 = Vertex(name = 'V_320',
	particles = [ P.ghZ, P.ghWm__tilde__, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_466_1})

V_321 = Vertex(name = 'V_321',
	particles = [ P.W__minus__, P.G__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_436})

V_322 = Vertex(name = 'V_322',
	particles = [ P.A, P.W__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVV1 ],
	couplings = {(0, 0):C.GC_487})

V_323 = Vertex(name = 'V_323',
	particles = [ P.A, P.W__plus__, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.VVS1 ],
	couplings = {(0, 0):C.GC_489})

V_324 = Vertex(name = 'V_324',
	particles = [ P.A, P.W__plus__, P.G0, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_492})

V_325 = Vertex(name = 'V_325',
	particles = [ P.A, P.W__plus__, P.G__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_491})

V_326 = Vertex(name = 'V_326',
	particles = [ P.W__plus__, P.G0, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_435})

V_327 = Vertex(name = 'V_327',
	particles = [ P.ghA, P.ghWp__tilde__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_487_1})

V_328 = Vertex(name = 'V_328',
	particles = [ P.ghWm, P.ghZ__tilde__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_466_1})

V_329 = Vertex(name = 'V_329',
	particles = [ P.ghWm, P.ghA__tilde__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_488_1})

V_330 = Vertex(name = 'V_330',
	particles = [ P.ghZ, P.ghWp__tilde__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_465_1})

V_331 = Vertex(name = 'V_331',
	particles = [ P.W__plus__, P.G__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_437})

V_332 = Vertex(name = 'V_332',
	particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_457})

V_333 = Vertex(name = 'V_333',
	particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_457})

V_334 = Vertex(name = 'V_334',
	particles = [ P.W__minus__, P.W__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS1 ],
	couplings = {(0, 0):C.GC_456})

V_335 = Vertex(name = 'V_335',
	particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_457})

V_336 = Vertex(name = 'V_336',
	particles = [ P.A, P.A, P.W__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVVV2 ],
	couplings = {(0, 0):C.GC_462})

V_337 = Vertex(name = 'V_337',
	particles = [ P.W__minus__, P.W__plus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVV1 ],
	couplings = {(0, 0):C.GC_465})

V_338 = Vertex(name = 'V_338',
	particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVVV2 ],
	couplings = {(0, 0):C.GC_458})

V_339 = Vertex(name = 'V_339',
	particles = [ P.A, P.Z, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_495})

V_340 = Vertex(name = 'V_340',
	particles = [ P.Z, P.G0, P.H ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_468})

V_341 = Vertex(name = 'V_341',
	particles = [ P.ghWm, P.ghWm__tilde__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_465_1})

V_342 = Vertex(name = 'V_342',
	particles = [ P.ghWp, P.ghWp__tilde__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.UUV1 ],
	couplings = {(0, 0):C.GC_466_1})

V_343 = Vertex(name = 'V_343',
	particles = [ P.Z, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VSS1 ],
	couplings = {(0, 0):C.GC_476})

V_344 = Vertex(name = 'V_344',
	particles = [ P.W__minus__, P.Z, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVS1 ],
	couplings = {(0, 0):C.GC_479})

V_345 = Vertex(name = 'V_345',
	particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_482})

V_346 = Vertex(name = 'V_346',
	particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_481})

V_347 = Vertex(name = 'V_347',
	particles = [ P.W__plus__, P.Z, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.VVS1 ],
	couplings = {(0, 0):C.GC_479})

V_348 = Vertex(name = 'V_348',
	particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_480})

V_349 = Vertex(name = 'V_349',
	particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_481})

V_350 = Vertex(name = 'V_350',
	particles = [ P.A, P.W__minus__, P.W__plus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVVV5 ],
	couplings = {(0, 0):C.GC_484})

V_351 = Vertex(name = 'V_351',
	particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_494})

V_352 = Vertex(name = 'V_352',
	particles = [ P.Z, P.Z, P.G0, P.G0 ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_471})

V_353 = Vertex(name = 'V_353',
	particles = [ P.Z, P.Z, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVS1 ],
	couplings = {(0, 0):C.GC_470})

V_354 = Vertex(name = 'V_354',
	particles = [ P.Z, P.Z, P.H, P.H ],
	color = [ '1' ],
	lorentz = [ L.VVSS1 ],
	couplings = {(0, 0):C.GC_471})

V_355 = Vertex(name = 'V_355',
	particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
	color = [ '1' ],
	lorentz = [ L.VVVV2 ],
	couplings = {(0, 0):C.GC_464})

V_356 = Vertex(name = 'V_356',
	particles = [ P.d__tilde__, P.d, P.A ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_485})

V_357 = Vertex(name = 'V_357',
	particles = [ P.s__tilde__, P.s, P.A ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_485})

V_358 = Vertex(name = 'V_358',
	particles = [ P.b__tilde__, P.b, P.A ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_485})

V_359 = Vertex(name = 'V_359',
	particles = [ P.e__plus__, P.e__minus__, P.A ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_488})

V_360 = Vertex(name = 'V_360',
	particles = [ P.mu__plus__, P.mu__minus__, P.A ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_488})

V_361 = Vertex(name = 'V_361',
	particles = [ P.ta__plus__, P.ta__minus__, P.A ],
	color = [ '1' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_488})

V_362 = Vertex(name = 'V_362',
	particles = [ P.u__tilde__, P.u, P.A ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_486})

V_363 = Vertex(name = 'V_363',
	particles = [ P.c__tilde__, P.c, P.A ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_486})

V_364 = Vertex(name = 'V_364',
	particles = [ P.t__tilde__, P.t, P.A ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_486})

V_365 = Vertex(name = 'V_365',
	particles = [ P.d__tilde__, P.d, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_334})

V_366 = Vertex(name = 'V_366',
	particles = [ P.s__tilde__, P.s, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_334})

V_367 = Vertex(name = 'V_367',
	particles = [ P.b__tilde__, P.b, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV1 ],
	couplings = {(0, 0):C.GC_334})

V_368_1 = Vertex(name = 'V_368_1',
	particles = [ P.u__tilde__, P.u, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV5 ],
	couplings = {(0, 0):C.GC_334})

V_376_1 = Vertex(name = 'V_376_1',
	particles = [ P.c__tilde__, P.c, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV5 ],
	couplings = {(0, 0):C.GC_334})

V_384_1 = Vertex(name = 'V_384_1',
	particles = [ P.t__tilde__, P.t, P.g ],
	color = [ 'T(3,2,1)' ],
	lorentz = [ L.FFV5 ],
	couplings = {(0, 0):C.GC_334})

V_386 = Vertex(name = 'V_386',
	particles = [ P.e__plus__, P.ve, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_685})

V_390 = Vertex(name = 'V_390',
	particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_689})

V_394 = Vertex(name = 'V_394',
	particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_693})

V_395 = Vertex(name = 'V_395',
	particles = [ P.d__tilde__, P.u, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_438})

V_399 = Vertex(name = 'V_399',
	particles = [ P.s__tilde__, P.c, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_442})

V_403 = Vertex(name = 'V_403',
	particles = [ P.b__tilde__, P.t, P.W__minus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_446})

V_404 = Vertex(name = 'V_404',
	particles = [ P.u__tilde__, P.d, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_676})

V_408 = Vertex(name = 'V_408',
	particles = [ P.c__tilde__, P.s, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_680})

V_412 = Vertex(name = 'V_412',
	particles = [ P.t__tilde__, P.b, P.W__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_684})

V_413 = Vertex(name = 'V_413',
	particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_447})

V_417 = Vertex(name = 'V_417',
	particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_451})

V_421 = Vertex(name = 'V_421',
	particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_455})

V_422 = Vertex(name = 'V_422',
	particles = [ P.d__tilde__, P.d, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_473, (0, 1):C.GC_475})

V_423 = Vertex(name = 'V_423',
	particles = [ P.s__tilde__, P.s, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_473, (0, 1):C.GC_475})

V_424 = Vertex(name = 'V_424',
	particles = [ P.b__tilde__, P.b, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_473, (0, 1):C.GC_475})

V_425 = Vertex(name = 'V_425',
	particles = [ P.e__plus__, P.e__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_476, (0, 1):C.GC_478})

V_426 = Vertex(name = 'V_426',
	particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_476, (0, 1):C.GC_478})

V_427 = Vertex(name = 'V_427',
	particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_476, (0, 1):C.GC_478})

V_428 = Vertex(name = 'V_428',
	particles = [ P.u__tilde__, P.u, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_474, (0, 1):C.GC_477})

V_429 = Vertex(name = 'V_429',
	particles = [ P.c__tilde__, P.c, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_474, (0, 1):C.GC_477})

V_430 = Vertex(name = 'V_430',
	particles = [ P.t__tilde__, P.t, P.Z ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFV2, L.FFV4 ],
	couplings = {(0, 0):C.GC_474, (0, 1):C.GC_477})

V_431 = Vertex(name = 'V_431',
	particles = [ P.ve__tilde__, P.ve, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_467})

V_432 = Vertex(name = 'V_432',
	particles = [ P.vm__tilde__, P.vm, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_467})

V_433 = Vertex(name = 'V_433',
	particles = [ P.vt__tilde__, P.vt, P.Z ],
	color = [ '1' ],
	lorentz = [ L.FFV2 ],
	couplings = {(0, 0):C.GC_467})

#### NP1 vertices from CphiG ####

V_25 = Vertex(name = 'V_25',
 	particles = [ P.g, P.g, P.G0, P.G0 ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVSS2 ],
 	couplings = {(0, 0):C.GC_114})

V_27 = Vertex(name = 'V_27',
 	particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVSS2 ],
 	couplings = {(0, 0):C.GC_114})

V_29 = Vertex(name = 'V_29',
 	particles = [ P.g, P.g, P.H ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVS2 ],
 	couplings = {(0, 0):C.GC_178})

V_31 = Vertex(name = 'V_31',
 	particles = [ P.g, P.g, P.H, P.H ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVSS2 ],
 	couplings = {(0, 0):C.GC_114})

V_34 = Vertex(name = 'V_34',
 	particles = [ P.g, P.g, P.g, P.G0, P.G0 ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVSS1 ],
 	couplings = {(0, 0):C.GC_336})

V_36 = Vertex(name = 'V_36',
 	particles = [ P.g, P.g, P.g, P.G__minus__, P.G__plus__ ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVSS1 ],
 	couplings = {(0, 0):C.GC_336})

V_38 = Vertex(name = 'V_38',
 	particles = [ P.g, P.g, P.g, P.H ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVS1 ],
 	couplings = {(0, 0):C.GC_337})

V_40 = Vertex(name = 'V_40',
 	particles = [ P.g, P.g, P.g, P.H, P.H ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVSS1 ],
 	couplings = {(0, 0):C.GC_336})

V_43 = Vertex(name = 'V_43',
 	particles = [ P.g, P.g, P.g, P.g, P.G0, P.G0 ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVSS1, L.VVVVSS2, L.VVVVSS3 ],
 	couplings = {(1, 1):C.GC_394, (0, 0):C.GC_394, (2, 2):C.GC_394})

V_45 = Vertex(name = 'V_45',
 	particles = [ P.g, P.g, P.g, P.g, P.G__minus__, P.G__plus__ ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVSS1, L.VVVVSS2, L.VVVVSS3 ],
 	couplings = {(1, 1):C.GC_394, (0, 0):C.GC_394, (2, 2):C.GC_394})

V_47 = Vertex(name = 'V_47',
 	particles = [ P.g, P.g, P.g, P.g, P.H ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVS1, L.VVVVS2, L.VVVVS3 ],
 	couplings = {(1, 1):C.GC_395, (0, 0):C.GC_395, (2, 2):C.GC_395})

V_49 = Vertex(name = 'V_49',
 	particles = [ P.g, P.g, P.g, P.g, P.H, P.H ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVSS1, L.VVVVSS2, L.VVVVSS3 ],
 	couplings = {(1, 1):C.GC_394, (0, 0):C.GC_394, (2, 2):C.GC_394})

#### NP1 vertices from Ctphi ####

V_60 = Vertex(name = 'V_60',
	particles = [ P.t__tilde__, P.t, P.G0, P.G0, P.G0 ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	couplings = {(0, 0):C.GC_668, (0, 1):C.GC_168})

V_69 = Vertex(name = 'V_69',
	particles = [ P.t__tilde__, P.t, P.G0, P.G0 ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	couplings = {(0, 0):C.GC_674, (0, 1):C.GC_212})

V_78 = Vertex(name = 'V_78',
	particles = [ P.t__tilde__, P.t, P.G0, P.G__minus__, P.G__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	couplings = {(0, 0):C.GC_669, (0, 1):C.GC_167})

V_87 = Vertex(name = 'V_87',
	particles = [ P.t__tilde__, P.t, P.G__minus__, P.G__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	couplings = {(0, 0):C.GC_674, (0, 1):C.GC_212})

V_96 = Vertex(name = 'V_96',
	particles = [ P.t__tilde__, P.t, P.G0, P.G0, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	couplings = {(0, 0):C.GC_670, (0, 1):C.GC_165})

V_114 = Vertex(name = 'V_114',
	particles = [ P.t__tilde__, P.t, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS3, L.FFS4 ],
	couplings = {(0, 0):C.GC_672, (0, 1):C.GC_177})

V_123 = Vertex(name = 'V_123',
	particles = [ P.t__tilde__, P.t, P.G0, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	couplings = {(0, 0):C.GC_673, (0, 1):C.GC_214})

V_132 = Vertex(name = 'V_132',
	particles = [ P.t__tilde__, P.t, P.G__minus__, P.G__plus__, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	couplings = {(0, 0):C.GC_670, (0, 1):C.GC_165})

V_141 = Vertex(name = 'V_141',
	particles = [ P.t__tilde__, P.t, P.G0, P.H, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	couplings = {(0, 0):C.GC_669, (0, 1):C.GC_167})

V_150 = Vertex(name = 'V_150',
	particles = [ P.t__tilde__, P.t, P.H, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	couplings = {(0, 0):C.GC_675, (0, 1):C.GC_213})

V_159 = Vertex(name = 'V_159',
	particles = [ P.t__tilde__, P.t, P.H, P.H, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	couplings = {(0, 0):C.GC_671, (0, 1):C.GC_166})
