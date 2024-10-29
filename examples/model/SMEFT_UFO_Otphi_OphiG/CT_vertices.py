# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 13.0.1 for Linux x86 (64-bit) (January 29, 2022)
# Date: Mon 8 Jan 2024 12:54:06


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L

#### NP1 vertices from CphiG ####

CTV_25 = CTVertex(name = 'CTV_25',
 	type = 'UV',
        particles = [ P.g, P.g, P.G0, P.G0 ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVSS2 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_114})

CTV_27 = CTVertex(name = 'CTV_27',
 	type = 'UV',
        particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVSS2 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_114})

CTV_29 = CTVertex(name = 'CTV_29',
       	type = 'UV',
        particles = [ P.g, P.g, P.H ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVS2 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_178})

CTV_31 = CTVertex(name = 'CTV_31',
 	type = 'UV',
        particles = [ P.g, P.g, P.H, P.H ],
 	color = [ 'Identity(1,2)' ],
 	lorentz = [ L.VVSS2 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_114})

CTV_34 = CTVertex(name = 'CTV_34',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.G0, P.G0 ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVSS1 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_336})

CTV_36 = CTVertex(name = 'CTV_36',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.G__minus__, P.G__plus__ ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVSS1 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_336})

CTV_38 = CTVertex(name = 'CTV_38',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.H ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVS1 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_337})

CTV_40 = CTVertex(name = 'CTV_40',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.H, P.H ],
 	color = [ 'f(1,2,3)' ],
 	lorentz = [ L.VVVSS1 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_336})

CTV_43 = CTVertex(name = 'CTV_43',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.g, P.G0, P.G0 ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVSS1, L.VVVVSS2, L.VVVVSS3 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(1,1,0):C.UVGC_394, (0,0,0):C.UVGC_394, (2,2,0):C.UVGC_394})

CTV_45 = CTVertex(name = 'CTV_45',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.g, P.G__minus__, P.G__plus__ ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVSS1, L.VVVVSS2, L.VVVVSS3 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(1,1,0):C.UVGC_394, (0,0,0):C.UVGC_394, (2,2,0):C.UVGC_394})

CTV_47 = CTVertex(name = 'CTV_47',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.g, P.H ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVS1, L.VVVVS2, L.VVVVS3 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(1,1,0):C.UVGC_395, (0,0,0):C.UVGC_395, (2,2,0):C.UVGC_395})

CTV_49 = CTVertex(name = 'CTV_49',
 	type = 'UV',
        particles = [ P.g, P.g, P.g, P.g, P.H, P.H ],
 	color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
 	lorentz = [ L.VVVVSS1, L.VVVVSS2, L.VVVVSS3 ],
 	loop_particles = [ [ P.g ] ],
        couplings = {(1,1,0):C.UVGC_394, (0,0,0):C.UVGC_394, (2,2,0):C.UVGC_394})

#### NP1 vertices from Ctphi ####

CTV_60 = CTVertex(name = 'CTV_60',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G0, P.G0, P.G0 ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_668, (0,1,0):C.UVGC_168})

CTV_69 = CTVertex(name = 'CTV_69',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G0, P.G0 ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_674, (0,1,0):C.UVGC_212})

CTV_78 = CTVertex(name = 'CTV_78',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G0, P.G__minus__, P.G__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_669, (0,1,0):C.UVGC_167})

CTV_87 = CTVertex(name = 'CTV_87',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G__minus__, P.G__plus__ ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_674, (0,1,0):C.UVGC_212})

CTV_96 = CTVertex(name = 'CTV_96',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G0, P.G0, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_670, (0,1,0):C.UVGC_165})

CTV_114 = CTVertex(name = 'CTV_114',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFS3, L.FFS4 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_672, (0,1,0):C.UVGC_177})

CTV_123 = CTVertex(name = 'CTV_123',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G0, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_673, (0,1,0):C.UVGC_214})

CTV_132 = CTVertex(name = 'CTV_132',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G__minus__, P.G__plus__, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_670, (0,1,0):C.UVGC_165})

CTV_141 = CTVertex(name = 'CTV_141',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.G0, P.H, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_669, (0,1,0):C.UVGC_167})

CTV_150 = CTVertex(name = 'CTV_150',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.H, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSS1, L.FFSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_675, (0,1,0):C.UVGC_213})

CTV_159 = CTVertex(name = 'CTV_159',
	type = 'UV',
        particles = [ P.t__tilde__, P.t, P.H, P.H, P.H ],
	color = [ 'Identity(1,2)' ],
	lorentz = [ L.FFSSS1, L.FFSSS2 ],
	loop_particles = [ [ P.g ] ],
        couplings = {(0,0,0):C.UVGC_671, (0,1,0):C.UVGC_166})
