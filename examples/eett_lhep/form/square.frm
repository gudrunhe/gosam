#-
Off statistics;
Vectors k1, ..., k4, Q, r1, r2, Qt;

Symbols mT, mZ, s, t, tau, rho;
CFunction gvq, gaq, gvl, gal, P, Pc;
Indices mu, nu, rh;
Symbols y, Z, sw, cw, NC, CF;
CTensor QTens;
Symbol PZ, PZc;
Symbols half;
Symbols gev, gea, gTv, gTa;

Symbols Qq, Ql, prefactor0, prefactor1, pinches;
CFunctions a30, a31, a32, b32;

#define PROPS "Z,y"
Local amp =
#Do X={`PROPS'}
#Do Y={`PROPS'}
	#Write "[amp](`X'-`Y')"
	+ 1/4 * CF * NC * (
		g_(1, k1) *
		(gvl(`X') * g_(1, mu) + gal(`X') * g_(1, mu, 5_)) *
		g_(1, k2) *
		(gvl(`Y') * g_(1, nu) + gal(`Y') * g_(1, nu, 5_))
	)*(
		(g_(2, k3) + mT) *

		g_(2, rh) *
		(g_(2, Q) + g_(2, k3) + mT) *

		(gvq(`X') * g_(2, mu) + gaq(`X') * g_(2, mu, 5_)) *

		(g_(2, Q) - g_(2, k4) + mT) *
		g_(2, rh) *

		(g_(2, k4) - mT) *
		(gvq(`Y') * g_(2, nu) + gaq(`Y') * g_(2, nu, 5_))
	) *
	P(`X') * Pc(`Y') / s^2
#EndDo
#EndDo
;

Local amp0 =
#Do X={`PROPS'}
#Do Y={`PROPS'}
	#Write "[amp0](`X'-`Y')"
	+ 1/4 * NC * (
		g_(1, k1) *
		(gvl(`X') * g_(1, mu) + gal(`X') * g_(1, mu, 5_)) *
		g_(1, k2) *
		(gvl(`Y') * g_(1, nu) + gal(`Y') * g_(1, nu, 5_))
	)*(
		(g_(2, k3) + mT) *
		(gvq(`X') * g_(2, mu) + gaq(`X') * g_(2, mu, 5_)) *
		(g_(2, k4) - mT) *
		(gvq(`Y') * g_(2, nu) + gaq(`Y') * g_(2, nu, 5_))
	) *
	P(`X') * Pc(`Y') / s^2
#EndDo
#EndDo
;

Id P(y) = 1;
Id Pc(y) = 1;
Id P(Z) = PZ;
Id Pc(Z) = PZc;

Id gvq(y) = -Qq;
Id gvl(y) = -Ql;
Id gaq(y) = 0;
Id gal(y) = 0;

Id gvq(Z) = gTv;
Id gvl(Z) = gev;
Id gaq(Z) = gTa;
Id gal(Z) = gea;

Id Qq = 2/3;
Id Ql = -1;

Id g_(2, Q, mu?, Q) = - Q.Q * g_(2, mu) + 2*g_(2, Q) * Q(mu);
Id g_(2, Q, mu?, 5_, Q) = Q.Q * g_(2, mu, 5_) - 2*g_(2, Q, 5_) * Q(mu);

Brackets Q;
.sort
Local ampr = amp[Q.Q];

Trace4, 1;
Trace4, 2;

.sort

Hide ampr, amp0;
*
*

ToTensor Q, QTens;
if(count(QTens,1) == 0) Multiply QTens;

Id QTens(mu?, nu?) =
	+ r1(mu) * r1(nu) * a32(1, 1, pinches)
	+ r1(mu) * r2(nu) * a32(1, 2, pinches)
	+ r2(mu) * r1(nu) * a32(1, 2, pinches)
	+ r2(mu) * r2(nu) * a32(2, 2, pinches)
	+ d_(mu, nu) * b32(pinches);

Id QTens(mu?) = 
	+ r1(mu) * a31(1, pinches)
	+ r2(mu) * a31(2, pinches);

Id QTens() = a30(pinches);

Id r1 = k3;
Id r2 = -k4;
*
*
*
.sort
Unhide ampr, amp0;

Id k4.k4 = mT^2;

Id k4 = k1 + k2 - k3;

Id k1.k3 = k3.k3 + k4.k3 - k2.k3;

Id k1.k1 = 0;
Id k2.k2 = 0;
Id k3.k3 = mT^2;
Id k1.k2 = s/2;
Id k3.k4 = 1/2 * (s - 2 * mT^2);

Id k2.k3 = -1/2 * (t - mT^2);

Id mT^2/s = rho;
Id t/s = tau;

#$prefactor0 = 1/36 * NC;
#$prefactor1 = 1/18 * CF * NC;

Id CF * NC = CF * NC * prefactor1 / $prefactor1;
Id NC = NC * prefactor0 / $prefactor0;

Brackets prefactor0, prefactor1;
.sort
Collect dum_, dum_;
MakeInteger dum_;
Brackets dum_, prefactor0, prefactor1;
.sort
Collect dum_, dum_;

Id dum_(1/2) = half;
Id dum_(-1/2) = -half;
Id dum_(1/4) = half^2;
Id dum_(-1/4) = -half^2;
Id dum_(t?) = t;

.sort

#write <analytic.txt> "prefactor0 = %$;", $prefactor0
#write <analytic.txt> "prefactor1 = %$;", $prefactor1
#write <analytic.txt> "amp = %e", amp
#write <analytic.txt> "ampr = %e", ampr
#write <analytic.txt> "amp0 = %e", amp0

.end
