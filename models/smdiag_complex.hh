* vim: ts=3:sw=3
*---#[ Symbol Definitions :
Symbols [field.U], [field.Ubar], [field.D], [field.Dbar],
	[field.S], [field.Sbar], [field.C], [field.Cbar],
	[field.T], [field.Tbar], [field.B], [field.Bbar];
Symbols [field.em], [field.ep], [field.ne], [field.nebar],
	[field.mum], [field.mup], [field.nmu], [field.nmubar],
	[field.taum], [field.taup], [field.ntau], [field.ntaubar];
Symbols [field.gh], [field.ghbar], [field.g];
Symbols [field.A], [field.Wp], [field.Wm], [field.Z],
	[field.H], [field.chi], [field.phip], [field.phim],
	[field.ghA], [field.ghAbar], [field.ghZ], [field.ghZbar],
	[field.ghWm], [field.ghWmbar], [field.ghWp], [field.ghWpbar];

Symbols mU, mD, mC, mS, mB, mBMS, mT, mW, mZ, mH, me, mmu, mtau;
Symbols wB, wT, wtau, wZ, wW, wH, wghZ, wghWp, wghWm, wchi, wphi;
Symbols gs, e, cw, sw;
Symbols gWWZZ, gWWAZ, gWWAA, gWWWW, gWWZ;
Symbols gHHHH, gHHXX, gHHPP, gXXPP, gPPPP, gXXXX;
Symbols gHHH, gHXX, gHPP;
Symbols gZZHH, gZZXX, gWWHH, gWWXX, gWWPP, gAAPP, gAZPP, gZZPP;
Symbols gWAPH, gWZPH, gWZPX, gWAPX;
Symbols gZXH, gAPP, gZPP, gWPH, gWPX;
Symbols gHZZ, gHWW, gPWA, gPWZ;
Symbols gGWX, gGWH, gGZH, gGWZP, gGZWP;
Symbol gW, gH;

#Do f={U,D,C,S,T,B,e,mu,tau}
Symbols gH`f', gX`f', gP`f';
#EndDo

#Do f={U,D,C,S,T,B,ne,nmu,ntau,e,mu,tau}
Symbols g`f'v, g`f'a, g`f'l, g`f'r;
#EndDo
*---#] Symbol Definitions :
*---#[ Procedure VertexConstants :
#Procedure VertexConstants
* All equation numbers refer to Boehm, Denner, Joos: Gauge Theories
*
*---#[   flavour quantum numbers of the fermions :
*----#[   Leptons :
#define Qe    "(-1)"
#define Qmu   "(-1)"
#define Qtau  "(-1)"
#define Qne   "(0)"
#define Qnmu  "(0)"
#define Qntau "(0)"
#define I3e    "(-1/2)"
#define I3mu   "(-1/2)"
#define I3tau  "(-1/2)"
#define I3ne   "(+1/2)"
#define I3nmu  "(+1/2)"
#define I3ntau "(+1/2)"
*----#]   Leptons :
*----#[   Quarks :
#define QU    "(+2/3)"
#define QC    "(+2/3)"
#define QT    "(+2/3)"
#define QD    "(-1/3)"
#define QS    "(-1/3)"
#define QB    "(-1/3)"

#define I3U    "(+1/2)"
#define I3C    "(+1/2)"
#define I3T    "(+1/2)"
#define I3D    "(-1/2)"
#define I3S    "(-1/2)"
#define I3B    "(-1/2)"
*----#]   Quarks :
*---#]   EW quantum numbers of the fermions :
*---#[ VVVV (A.2.7) :
Id C([field.Wp], [field.Wm], [field.Z], [field.Z]) = PREFACTOR(e^2 * gWWZZ);
Id C([field.Wp], [field.Wm], [field.A], [field.Z]) = PREFACTOR(e^2 * gWWAZ);
Id C([field.Wp], [field.Wm], [field.A], [field.A]) = PREFACTOR(e^2 * gWWAA);
Id C([field.Wp], [field.Wm], [field.Wp], [field.Wm]) = PREFACTOR(e^2 * gWWWW);
*---#] VVVV (A.2.7) :
*---#[ VVVV (QCD) (2.4.32) :
Id C([field.g], [field.g], [field.g], [field.g]) = PREFACTOR(gs^2);
*---#] VVVV (QCD) (2.4.32) :
*---#[ VVV (A.2.9) :
Id C([field.A], [field.Wp], [field.Wm]) = PREFACTOR(e);
Id C([field.Z], [field.Wp], [field.Wm]) = PREFACTOR(e * gWWZ);
*---#] VVV (A.2.9) :
*---#[ VVV (QCD) (2.4.32) :
Id C([field.g], [field.g], [field.g]) = PREFACTOR(gs);
*---#] VVV (QCD) (2.4.32) :
*---#[ SSSS (A.2.11) :
Id C([field.H], [field.H], [field.H], [field.H]) =
   PREFACTOR(e^2 * gHHHH);
Id C([field.chi], [field.chi], [field.chi], [field.chi]) =
   PREFACTOR(e^2 * gXXXX);
Id C([field.H], [field.H], [field.chi], [field.chi]) =
   PREFACTOR(e^2 * gHHXX);
Id C([field.H], [field.H], [field.phip], [field.phim]) =
   PREFACTOR(e^2 * gHHPP);
Id C([field.chi], [field.chi], [field.phip], [field.phim]) =
   PREFACTOR(e^2 * gXXPP);
Id C([field.phip], [field.phim], [field.phip], [field.phim]) =
   PREFACTOR(e^2 * gPPPP);
*---#] SSSS (A.2.11) :
*---#[ SSS (A.2.13) :
Id C([field.H], [field.H], [field.H]) = PREFACTOR(e * gHHH);
Id C([field.H], [field.chi], [field.chi]) = PREFACTOR(e * gHXX);
Id C([field.H], [field.phip], [field.phim]) = PREFACTOR(e * gHPP);
*---#] SSS (A.2.13) :
*---#[ VVSS (A.2.14) :
Id C([field.Z], [field.Z], [field.H], [field.H]) = PREFACTOR(e^2 * gZZHH);
Id C([field.Z], [field.Z], [field.chi], [field.chi]) = PREFACTOR(e^2 * gZZXX);
Id C([field.Wp], [field.Wm], [field.H], [field.H]) = PREFACTOR(e^2 * gWWHH);
Id C([field.Wp], [field.Wm], [field.chi], [field.chi]) = PREFACTOR(e^2 * gWWXX);
Id C([field.Wp], [field.Wm], [field.phip], [field.phim]) =
   PREFACTOR(e^2 * gWWPP);
Id C([field.A], [field.A], [field.phip], [field.phim]) = PREFACTOR(e^2 * gAAPP);
Id C([field.Z], [field.A], [field.phip], [field.phim]) = PREFACTOR(e^2 * gAZPP);
Id C([field.Z], [field.Z], [field.phip], [field.phim]) =	PREFACTOR(e^2 * gZZPP);
Id C([field.Wp], [field.A], [field.phim], [field.H]) = PREFACTOR(e^2 * gWAPH);
Id C([field.Wm], [field.A], [field.phip], [field.H]) = PREFACTOR(e^2 * gWAPH);
Id C([field.Wp], [field.A], [field.phim], [field.chi]) = PREFACTOR(e^2 * gWAPX);
Id C([field.Wm], [field.A], [field.phip], [field.chi]) =
   PREFACTOR(-e^2 * gWAPX);
Id C([field.Wp], [field.Z], [field.phim], [field.H]) = PREFACTOR(e^2 * gWZPH);
Id C([field.Wm], [field.Z], [field.phip], [field.H]) = PREFACTOR(e^2 * gWZPH);
Id C([field.Wp], [field.Z], [field.phim], [field.chi]) = PREFACTOR(e^2 * gWZPX);
Id C([field.Wm], [field.Z], [field.phip], [field.chi]) =
   PREFACTOR(-e^2 * gWZPX);
*---#] VVSS (A.2.14) :
*---#[ VSS (A.2.17) :
Id C([field.Z], [field.chi], [field.H]) = PREFACTOR(e * gZXH);
Id C([field.A], [field.phim], [field.phip]) = PREFACTOR(e * gAPP);
Id C([field.Z], [field.phim], [field.phip]) = PREFACTOR(e * gZPP);
Id C([field.Wp], [field.phim], [field.H]) = PREFACTOR(e * gWPH);
Id C([field.Wm], [field.phip], [field.H]) = PREFACTOR(-e * gWPH);
Id C([field.Wp], [field.phim], [field.chi]) = PREFACTOR(e * gWPX);
Id C([field.Wm], [field.phip], [field.chi]) = PREFACTOR(e * gWPX);
*---#] VSS (A.2.17) :
*---#[ SVV (A.2.19) :
Id C([field.H], [field.Z], [field.Z]) = PREFACTOR(e * gHZZ);
Id C([field.H], [field.Wp], [field.Wm]) = PREFACTOR(e * gHWW);
Id C([field.phip], [field.Wm], [field.A]) = PREFACTOR(e * gPWA);
Id C([field.phim], [field.Wp], [field.A]) = PREFACTOR(e * gPWA);
Id C([field.phip], [field.Wm], [field.Z]) = PREFACTOR(e * gPWZ);
Id C([field.phim], [field.Wp], [field.Z]) = PREFACTOR(e * gPWZ);
*---#] SVV (A.2.19) :
*---#[ VFF (QCD) (2.4.32) :
#do f={U,D,S,C,B,T}
	Id C([field.`f'bar], [field.`f'], [field.g]) = PREFACTOR(gs);
#enddo
*---#] VFF (QCD) (2.4.32) :
*---#[ VFF (A.2.21) :
*---#[   WQQ :
Id CL([field.Ubar], [field.D], [field.Wp]) = PREFACTOR(e * gW);
Id CL([field.Dbar], [field.U], [field.Wm]) = PREFACTOR(e * gW);
Id CL([field.Cbar], [field.S], [field.Wp]) = PREFACTOR(e * gW);
Id CL([field.Sbar], [field.C], [field.Wm]) = PREFACTOR(e * gW);
Id CL([field.Tbar], [field.B], [field.Wp]) = PREFACTOR(e * gW);
Id CL([field.Bbar], [field.T], [field.Wm]) = PREFACTOR(e * gW);
Id CR([field.Ubar], [field.D], [field.Wp]) = 0;
Id CR([field.Dbar], [field.U], [field.Wm]) = 0;
Id CR([field.Cbar], [field.S], [field.Wp]) = 0;
Id CR([field.Sbar], [field.C], [field.Wm]) = 0;
Id CR([field.Tbar], [field.B], [field.Wp]) = 0;
Id CR([field.Bbar], [field.T], [field.Wm]) = 0;
*---#]   WQQ :
*---#[   Wll :
#do l={e,mu,tau}
	#do f={e,mu,tau}
		#if "`l'" == "`f'"
			Id CL([field.n`l'bar], [field.`f'm], [field.Wp]) =
				PREFACTOR(e * gW);
			Id CL([field.`l'p], [field.n`f'], [field.Wm]) =
				PREFACTOR(e * gW);
		#else
			Id CL([field.n`l'bar], [field.`f'm], [field.Wp]) = 0;
			Id CL([field.`l'p], [field.n`f'], [field.Wm]) = 0;
		#endif
		Id CR([field.n`l'bar], [field.`f'm], [field.Wp]) = 0;
		Id CR([field.`l'p], [field.n`f'], [field.Wm]) = 0;
	#enddo
#enddo
*---#]   Wll :
*---#[   AFF :
#Do f={U,D,C,S,T,B,ne,nmu,ntau}
   Id CL([field.`f'bar], [field.`f'], [field.A]) = PREFACTOR(- (`Q`f'') * e);
   Id CR([field.`f'bar], [field.`f'], [field.A]) = PREFACTOR(- (`Q`f'') * e);
#EndDo
#Do f={e,mu,tau}
	Id CL([field.`f'p], [field.`f'm], [field.A]) = PREFACTOR(- (`Q`f'') * e);
	Id CR([field.`f'p], [field.`f'm], [field.A]) = PREFACTOR(- (`Q`f'') * e);
#EndDo
*---#]   AFF :
*---#[   ZFF :
#Do f={U,D,C,S,T,B,ne,nmu,ntau}
	Id CL([field.`f'bar], [field.`f'], [field.Z]) =
		PREFACTOR(e) * (g`f'l);
	Id CR([field.`f'bar], [field.`f'], [field.Z]) =
		PREFACTOR(e) * (g`f'r);
#EndDo
#Do f={e,mu,tau}
	Id CL([field.`f'p], [field.`f'm], [field.Z]) =
		PREFACTOR(e) * (g`f'l);
	Id CR([field.`f'p], [field.`f'm], [field.Z]) =
		PREFACTOR(e) * (g`f'r);
#EndDo
*---#]   ZFF :
*---#] VFF (A.2.21) :
*---#[ SFF (A.2.25) :
*---#[   HFF :
#Do f={U,D,C,S,B,T}
	Id CL([field.`f'bar], [field.`f'], [field.H]) = PREFACTOR(e * gH`f');
	Id CR([field.`f'bar], [field.`f'], [field.H]) = PREFACTOR(e * gH`f');
#EndDo
#Do f={e,mu,tau}
	Id CL([field.`f'p], [field.`f'm], [field.H]) = PREFACTOR(e * gH`f');
	Id CR([field.`f'p], [field.`f'm], [field.H]) = PREFACTOR(e * gH`f');
#EndDo
#Do f={ne,nmu,ntau}
	Id CL([field.`f'bar], [field.`f'], [field.H]) = 0;
	Id CR([field.`f'bar], [field.`f'], [field.H]) = 0;
#EndDo
*---#]   HFF :
*---#[   chiFF :
#do f={U,C,T,D,S,B}
	Id CL([field.`f'bar], [field.`f'], [field.chi]) =
		+i_*PREFACTOR(e * gX`f');
	Id CR([field.`f'bar], [field.`f'], [field.chi]) =
		-i_*PREFACTOR(e * gX`f');
#enddo
#do f={e,mu,tau}
	Id CL([field.`f'p], [field.`f'm], [field.chi]) =
		+i_*PREFACTOR(e * gX`f');
	Id CR([field.`f'p], [field.`f'm], [field.chi]) =
		-i_*PREFACTOR(e * gX`f');
#enddo
#Do f={ne,nmu,ntau}
	Id CL([field.`f'bar], [field.`f'], [field.chi]) = 0;
	Id CR([field.`f'bar], [field.`f'], [field.chi]) = 0;
#EndDo
*---#]   chiFF :
*---#[   phiFF :
	Id CL([field.Ubar], [field.D], [field.phip]) = +PREFACTOR(e) * gPU;
	Id CR([field.Ubar], [field.D], [field.phip]) = -PREFACTOR(e) * gPD;
	Id CL([field.Dbar], [field.U], [field.phim]) = -PREFACTOR(e) * gPD;
	Id CR([field.Dbar], [field.U], [field.phim]) = +PREFACTOR(e) * gPU;

	Id CL([field.Cbar], [field.S], [field.phip]) = +PREFACTOR(e) * gPC;
	Id CR([field.Cbar], [field.S], [field.phip]) = -PREFACTOR(e) * gPS;
	Id CL([field.Sbar], [field.C], [field.phim]) = -PREFACTOR(e) * gPS;
	Id CR([field.Sbar], [field.C], [field.phim]) = +PREFACTOR(e) * gPC;

	Id CL([field.Tbar], [field.B], [field.phip]) = +PREFACTOR(e) * gPT;
	Id CR([field.Tbar], [field.B], [field.phip]) = -PREFACTOR(e) * gPB;
	Id CL([field.Bbar], [field.T], [field.phim]) = -PREFACTOR(e) * gPB;
	Id CR([field.Bbar], [field.T], [field.phim]) = +PREFACTOR(e) * gPT;

#do l={e,mu,tau}
	Id CL([field.n`l'bar], [field.`l'm], [field.phip]) = 0;
	Id CR([field.n`l'bar], [field.`l'm], [field.phip]) =
		PREFACTOR(-e * gP`l');
	Id CL([field.`l'p], [field.n`l'], [field.phim]) =
		PREFACTOR(-e * gP`l');
	Id CR([field.`l'p], [field.n`l'], [field.phim]) = 0;
#enddo
*---#]   phiFF :
*---#] SFF (A.2.25)
*---#[ VGG (QCD) (2.4.32) :
Id C([field.ghbar], [field.gh], [field.g]) = PREFACTOR(gs);
*---#] VGG (QCD) (2.4.32) :
*---#[ VGG (A.2.27) :
Id C([field.ghWpbar], [field.ghWp], [field.A]) = PREFACTOR(e);
Id C([field.ghWmbar], [field.ghWm], [field.A]) = PREFACTOR(-e);
Id C([field.ghAbar], [field.ghWm], [field.Wp]) = PREFACTOR(e);
Id C([field.ghAbar], [field.ghWp], [field.Wm]) = PREFACTOR(-e);
Id C([field.ghWmbar], [field.ghA], [field.Wm]) = PREFACTOR(e);
Id C([field.ghWpbar], [field.ghA], [field.Wp]) = PREFACTOR(-e);
Id C([field.ghWpbar], [field.ghWp], [field.Z]) = PREFACTOR(e * gWWZ);
Id C([field.ghWmbar], [field.ghWm], [field.Z]) = PREFACTOR(- e * gWWZ);
Id C([field.ghZbar], [field.ghWm], [field.Wp]) = PREFACTOR(e * gWWZ);
Id C([field.ghZbar], [field.ghWp], [field.Wm]) = PREFACTOR(- e * gWWZ);
Id C([field.ghWmbar], [field.ghZ], [field.Wm]) = PREFACTOR(e * gWWZ);
Id C([field.ghWpbar], [field.ghZ], [field.Wp]) = PREFACTOR(- e * gWWZ);
*---#] VGG (A.2.27) :
*---#[ SGG (A.2.27) :
Id C([field.ghZbar], [field.ghZ], [field.H]) = PREFACTOR(e * gGZH);
Id C([field.ghWpbar], [field.ghWp], [field.H]) = PREFACTOR(e * gGWH);
Id C([field.ghWmbar], [field.ghWm], [field.H]) = PREFACTOR(e * gGWH);
Id C([field.ghWpbar], [field.ghWp], [field.chi]) = PREFACTOR(e * gGWX);
Id C([field.ghWmbar], [field.ghWm], [field.chi]) = PREFACTOR(-e * gGWX);
Id C([field.ghWpbar], [field.ghA], [field.phip]) = PREFACTOR(- e * gPWA);
Id C([field.ghWmbar], [field.ghA], [field.phim]) = PREFACTOR(- e * gPWA);
Id C([field.ghWpbar], [field.ghZ], [field.phip]) =	PREFACTOR(e * gGWZP);
Id C([field.ghWmbar], [field.ghZ], [field.phim]) =	PREFACTOR(e * gGWZP);
Id C([field.ghZbar], [field.ghWm], [field.phip]) = PREFACTOR(e * gGZWP);
Id C([field.ghZbar], [field.ghWp], [field.phim]) = PREFACTOR(e * gGZWP);
*---#] SGG (A.2.27) :
*---#[ effective gg(g)(g)H:
Id C([field.g], [field.g], [field.H]) = PREFACTOR(e * gs^2 * gH);
Id C([field.g], [field.g], [field.g], [field.H]) = PREFACTOR(e * gs^3 * gH);
Id C([field.g], [field.g], [field.g], [field.g], [field.H]) =
	PREFACTOR(e * gs^4 * gH);
*---#] effective gg(g)(g)H:
#EndProcedure
*---#] Procedure VertexConstants :
