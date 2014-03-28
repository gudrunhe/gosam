* The reference result in [1] is given in terms of primitive
* amplitudes. We use this script to assemble the full amplitude.
*
*
* [1] T. Melia, K. Melnikov, R. Rontsch et al.,
*     ``Next-to-leading order QCD predictions for $W^+W^+jj$ production
*       at the LHC,'' JHEP {\bf 1012 } (2010)  053.
*       [arXiv:1007.5313 [hep-ph]].

#-
Off Statistics;

CFunctions ra, rb, rc, rd;
CFunctions A0, A1, A2, Aa, Ab, Ac, Ad;
Symbols PREFACTORS, gs, NC, nf, NA;
Symbols s, u, d, c;
Symbols X0, X0c;

Indices js=NC, ju=NC, jd=NC, jc=NC;

.global

Global ATree = gs^2 * PREFACTORS * (
		d_(jd,jc) * d_(js,ju) - 1/NC * d_(jd,ju) * d_(js,jc)
	) * A0(u,d,c,s);


Global AVirt = gs^4 * PREFACTORS * (
		+ d_(jd,jc) * d_(js,ju) * A1
		+ d_(jd,ju) * d_(js,jc) * A2
	);

Id A1 = (NC - 2/NC) * Aa(u,d,c,s) - 2/NC * Aa(u,d,s,c)
	- 1/NC * Ab(u,s,c,d) - 1/NC * Ac(u,s,c,d) + nf * Ad(u,d,c,s);
Id A2 = 1/NC^2 * Aa(u,d,c,s) + (1 + 1/NC^2) * Aa(u,d,s,c)
	+ 1/NC^2 * Ab(u,s,c,d) + 1/NC^2 * Ac(u,s,c,d) - nf/NC * Ad(u,d,c,s);

#Do x={a,b,c,d}
   Id A`x'(?all) = r`x'(?all) * A0(u,d,c,s);
#EndDo

.store

*Dimension NC;

Global M20 = ATree * ATree;
Global M21 = ATree * AVirt;

Id A0(u,d,c,s)^2 = X0*X0c;

Brackets PREFACTORS, gs, X0, X0c;
.sort
Collect dum_;
Id dum_(NC^2-1) = NA;
Id dum_(1-NC^2) = -NA;

Id dum_(X0?) = X0;
.store

Local rat = M21 / M20 / gs^2;

* Check the double pole analytically:
*Id ra(u,d,s,c) = -2;
*Id ra(u,d,c,s) = -2;
*Id rb(u,s,c,d) = -1;
*Id rc(u,s,c,d) = -1;
*Id rd(u,d,c,s) =  0;
*multiply replace_(NC,3,NA,8);
Print;
.end
