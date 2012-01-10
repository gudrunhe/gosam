* vim: syntax=form:ts=3:sw=3
#-

*on shortstatistics;
off statistics;

#define LOOPS "0"
#include- spinney.hh
#redefine SPCANCEL "0"

#include- symbols.hh
#include- color.hh
#include- topology.hh


#include- `PROCESSPATH'/diagrams-ct.hh #global
*#include- `MODELFILE'
#include- model.hh
#include- `PROCESSPATH'/process.hh
#include- `PWD'/lightconedecomp.prc
#include- `PROCESSPATH'/diagrams-ct.hh #diagram`DIAG'

#call zeroes

#include- propagators.hh

#call rewritelegs
#include- legs.hh

* The rules of legs.hh do not restore all inp() and out()
* functions after we introduce the gauge check.
#if `GAUGEVAR'
	Id fDUMMY1?{inp,out}(sDUMMY1?, iDUMMY1?, vDUMMY1?, ?tail) =
		fDUMMY1(sDUMMY1, iDUMMY1, vDUMMY1);
#endif

* models that implement their own vertex replacements
* must define the preprocessor variable USEVERTEXPROC
* in the (Form-)model file and, in the same file,
* define the procedure ReplaceVertices

#ifndef `USEVERTEXPROC'
	#include- vertices.hh
#else
	Repeat;
		#call ReplaceVertices
	EndRepeat;
#endif

Id prop(sDUMMY1?, vDUMMY1?, iDUMMY1?, iDUMMY2?) = 1;
Id node(iDUMMY1?, iDUMMY2?, iDUMMY3?) = 1;
Id node(iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = 1;
Id inp(sDUMMY1?, iDUMMY1?, vDUMMY1?) = 1;
Id out(sDUMMY2?, iDUMMY1?, vDUMMY1?) = 1;

Brackets SplitLorentzIndex;
.sort:part 0.9.0;
Keep Brackets;

Repeat Id SplitLorentzIndex(iDUMMY1?, iDUMMY2?, ?tail1) *
          SplitLorentzIndex(iDUMMY3?, iDUMMY4?, ?tail2) =
	SplitLorentzIndex(iDUMMY1, ?tail1) *
	SplitLorentzIndex(iDUMMY3, ?tail2) * d_(iDUMMY2, iDUMMY4);
Id SplitLorentzIndex(iDUMMY1?) * SplitLorentzIndex(iDUMMY1?) = 1;

#call coloralgebra(0)
Id outcolor(sDUMMY1?, iDUMMY1?) = 1;

AntiBrackets c1, ..., c`NUMCS', TR, NC;
.sort:part 1;

Collect COLORFACTOR;

Id inv(k1?, m?) = inv(k1.k1 - m^2);
Id ZERO = 0;
Argument inv;
	Id ZERO = 0;
	#call kinematics
EndArgument;

* Counter term at external leg must be removed.
Id inv(0) = 0;

#call VertexConstants
#call ones
#call zeroes

Multiply replace_(Sqrt2, sqrt2);
Repeat Id d(iv1L?, iv2L?) * d(iv2L?, iv3L?) = d(iv1L, iv3L);

#call RemoveNCContainer

* Discrepancy between golem95 convention 1/(i\pi^(n/2))
* and 1/(2\pi)^n leaving out the pre-factors as described
* in the manual.
* Multiply PREFACTOR(i_ / 2);

Argument PREFACTOR;
Argument SpDenominator;
	#call spsymbols
EndArgument;
EndArgument;

Argument SpDenominator;
	Id ZERO = 0;
	#call spsymbols
EndArgument;

Id sqrt2 = PREFACTOR(sqrt2);
Id 1/sqrt2 = PREFACTOR(1/sqrt2);

AntiBrackets inv;
.sort
Collect PREFACTOR;
Normalize PREFACTOR;

Repeat Id PREFACTOR(sDUMMY1?) * PREFACTOR(sDUMMY2?) =
	PREFACTOR(sDUMMY1*sDUMMY2);

Id PREFACTOR(sDUMMY1?$thePrefactor) = 1;
.sort

Local prefactor`DIAG' = $thePrefactor;

#call lightconedecomp
Argument SpDenominator;
	#call spsymbols
EndArgument;

Argument formfactor;
	#call kinematics
	#call zeroes
	#call ones
EndArgument;

Id formfactor(sDUMMY1?, 0) = sDUMMY1;

* tHooftAlgebra will split all Dirac matrices Sm
* into Sm4 + SmEps. That would generate 2^n
* terms for n matrices, many of which become zero
* later on. To avoid this as far as possible we
* replace here all matrices contracted to external momenta.
Id Sm(vDUMMY1?{`EXTERNAL'}) = Sm4(vDUMMY1);
Id d(vDUMMY1?{`EXTERNAL'}, iDUMMY1?) = d4(vDUMMY1, iDUMMY1);

.sort:part 3.5;

#call tHooftAlgebra

Id dEps(iDUMMY1?, iDUMMY1?) = -2*eps;

#call SpCollect
Id fDUMMY1?{Spaa,Spab,Spba,Spbb}(?head, ZERO, ?tail) =  0;

#call SpClear()

#call SpContractMetrics
#call SpTrace4(`LIGHTLIKE')
.sort:part 4;

#call SpContractLeviCivita(`LIGHTLIKE')
#call SpContractMetrics

Id dEps(vDUMMY1?{`EXTERNAL'}, iv?) = 0;
Repeat Id d4(vDUMMY1?{`EXTERNAL'}, iv?) = vDUMMY1(iv);
Id dEps(iDUMMY1?, iDUMMY1?) = -2*eps;

Brackets Spaa, Spab, Spba, Spbb;
.sort:part 5;
Keep Brackets;
#call SpContract
#call SpOpen
.sort:part 5.1;

#ifdef `ABBREVIATE'
   #include- `PWD'/abbrev.hh
#endif

Repeat Id Spa2(vDUMMY1?{k1,...,k`LEGS'}, vDUMMY2?{k1,...,k`LEGS'}) *
	Spb2(vDUMMY2?, vDUMMY1?) = 2 * vDUMMY1.vDUMMY2;

Repeat Id
	SpDenominator(Spa2(vDUMMY1?{k1,...,k`LEGS'}, vDUMMY2?{k1,...,k`LEGS'})) *
	SpDenominator(Spb2(vDUMMY1?, vDUMMY2?)) = -1/2 * inv(vDUMMY1.vDUMMY2);

Id inv(sDUMMY1?symbol_) = 1/sDUMMY1;

#call kinematics
Id vDUMMY1?.vDUMMY2? = 1/2 * Spa2(vDUMMY1, vDUMMY2) * Spb2(vDUMMY2, vDUMMY1);
#call spsymbols

* just before doing the output: split into colour factors:
Normalize COLORFACTOR;

Id SpDenominator(sDUMMY1?) = 1/sDUMMY1;
Id inv(sDUMMY1?) = 1/sDUMMY1;

Brackets COLORFACTOR;
.sort:part.5.0.1;
Keep Brackets;

#$NUMCOL=0;
#Do cs=1,1
	Id IfMatch->succX`$NUMCOL'
		COLORFACTOR(sDUMMY1?$CS{`$NUMCOL'+1}) = COLORFACTOR(sDUMMY1);
	GoTo  failX`$NUMCOL';
	Label succX`$NUMCOL';
		ReDefine cs, "0";
	Label failX`$NUMCOL';
	.sort:part.5.0.2 COL=`$NUMCOL';
	Keep Brackets;
	#If `cs' == 0
		#$NUMCOL={`$NUMCOL'+1};
		Id COLORFACTOR(`$CS`$NUMCOL'') = COLORFACTOR(0,`$NUMCOL');
	#EndIf
#EndDo
Id COLORFACTOR(0, sDUMMY1?) = COLORFACTOR(sDUMMY1);

Brackets COLORFACTOR;
.sort:part.5.0.3;
#Do i=1,`$NUMCOL'
	Local diagram`DIAG'c`i' = diagram`DIAG'[COLORFACTOR(`i')];
#EndDo
Id COLORFACTOR(sDUMMY1?) = 0;

.sort:part 6;

#$terms=termsin_(diagram`DIAG');
#Do i=1,`$NUMCOL'
	#$terms`i'=termsin_(diagram`DIAG'c`i');
#EndDo

#Define TERMS "`$terms'"
#Do i=1,`$NUMCOL'
	#ReDefine TERMS "{`TERMS'+`$terms`i''}"
#EndDo
.sort:part 7;
#Create <`OUTFILE'.dat>
#Write <`OUTFILE'.dat> "terms=`TERMS'"
#Write <`OUTFILE'.dat> "NUMCOL=%$", $NUMCOL
#Write <`OUTFILE'.dat> "time=`time_'"
#Close <`OUTFILE'.dat>

#Create <`OUTFILE'.txt>
#If `TERMS' == 0
	#Write <`OUTFILE'.txt> "p`DIAG' = 0;"
#Else
	#Write <`OUTFILE'.txt> "p`DIAG' = %E;", prefactor`DIAG'
	#Do i=1,`$NUMCOL'
		#Write <`OUTFILE'.txt> "cf`i' = %$;", $CS`i'
		#Write <`OUTFILE'.txt> "vf`i' = %E;", diagram`DIAG'c`i'
	#EndDo
#EndIf
#Write <`OUTFILE'.txt> "d`DIAG' = %E;", diagram`DIAG'
#Close <`OUTFILE'.txt>
.end

