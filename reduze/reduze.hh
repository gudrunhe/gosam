* try to make contractions work in dim dimensions
Symbols dimS,dimD;
Dimension dimS; * space-time dimension (normally d)
*UnitTrace dimD; * dirac algebra dimension (normally 4)

AutoDeclare Symbols ReduzeT; * topologies/integral families
AutoDeclare Symbols ReduzeN; * propagators
CFunction prf; * for PolyRatFun
CFunction Sector;
CFunction Tag; * container for momentum/mass of ReduzeN
CFunction Shift; * container for momentum shifts
CFunction DiaMatch; * container for diagram number
CFunction Crossing, CrossingShift, CrossingInvariants; * functions to store crossings
CFunctions num; * inverse propagator num=inv^(-1)
CFunctions ReduzeInt; * Reduze integral function (stores the inverse powers of the propagators)
CFunction ProjDen; * function for storing projector denominators ProjDen(x)=1/x;
Symbols [];

* disable spinor flipping rules in spinney.hh (RemoveNCContainer)
* does not implement arXiv:1008.0803v1 Eq(21), discussion at the end of section 3.5.2
#Define NOSPFLIP

* tag each diagram with DiaMatch(qgraf_digram_index)
#Procedure DiaMatchTagReduze()
Multiply DiaMatch(`DIAG'); * sj - probably want this when diasum is turned off
*Id DIAGRAM(sDUMMY1?) = DiaMatch(sDUMMY1); * sj - works for now
#EndProcedure

* screen inplorentz, outlorentz
#Procedure ScreenExternalReduze()
   Id fDUMMY1?{inplorentz,outlorentz}(?tail) =
      SCREEN(fDUMMY1(?tail));
#EndProcedure

* compute trace in d dimensions
* input: trL*Sm(a)*Sm(b)*...*Sm(c)*trR (= Tr[\gamma^a \gamma^b ... \gamma^c])
* WARNING - NOT SURE THIS HANDLES MULTIPLE CLOSED SPIN LINES CORRECTLY
*         - NOT SURE THIS HANDLES OPEN SPIN LINES CORRECTLY
#Procedure TraceReduze()
  ChainIn Sm;
* loop over closed spin lines computing traces
   #Do i = 1,1
      Id Once Sm(?tail) = g_(1,?tail);
      Tracen 1;
      if ( Count(Sm,1) > 0 ) Redefine i "0";
      .Sort:red-trace;
   #EndDo
   Id trL*trR=1;
#EndProcedure

* shift momenta to Reduze momenta
* WARNING - does shift always have (pair,[],pair,[],...,[])?
#Procedure ShiftReduze()
   #include- reduzeshifts-`LOOPS'.hh
   Repeat Id Shift(?head,[],?tail) = Shift(?head,?tail);
   Id Once Shift(?tail) = replace_(?tail);
   .Sort:red-shifting;
#EndProcedure
                  
#Procedure CrossReduze()
   #include- reduzecrossing-`LOOPS'.hh
#EndProcedure

* map crossed integral families to uncrossed
* WARNING - Not sure this is done consistently, do we need to eliminate k4 first? Have we done this correctly?
*         - this routine needs carefully checking
#Procedure CrossMomentaReduze()
   Repeat Id CrossingShift(?head,[],?tail) = CrossingShift(?head,?tail);
   Id Once CrossingShift(?tail) = replace_(?tail);
   .Sort:red-crossing;
#EndProcedure

* assumes that CrossingInvariants() already exists in the expression
#Procedure CrossInvariantsReduze()
   Repeat Id CrossingInvariants(?head,[],?tail) = CrossingInvariants(?head,?tail);
   Id Once CrossingInvariants(?tail) = CrossingInvariants(reverse_(?tail))*replace_(?tail);
   .Sort:red-crossinginvar;
#EndProcedure
                  
* map scalar products to (inverse) propagators
#Procedure SPToPropReduze()
   #include- reduzesptop-`LOOPS'.hh
   .Sort:SPToPropReduze;
#EndProcedure
                   
* map propagators to Reduze ordered propagators
#Procedure MapReduze()
   #include- reduzemap-`LOOPS'.hh
*   Bracket Tag,inv,num;
*   .Sort:red-btag;
*   Keep Brackets;
* try to map propagators with inv/num(+...) and inv/num(-...)
   #Do i = 0,1
* map propagators
   Repeat Id Tag(sDUMMY1?,vDUMMY1?,sDUMMY2?)*inv(vDUMMY1?,sDUMMY2?,?tail)=
      Tag(sDUMMY1,vDUMMY1,sDUMMY2)*sDUMMY1^(-1);
   Repeat Id Tag(sDUMMY1?,vDUMMY1?,sDUMMY2?)*num(vDUMMY1?,sDUMMY2?,?tail)=
      Tag(sDUMMY1,vDUMMY1,sDUMMY2)*sDUMMY1;
* now flip sign of momentum in even functions inv/num
   Id inv(vDUMMY1?,?tail)=inv(-vDUMMY1,?tail);
   Id num(vDUMMY1?,?tail)=num(-vDUMMY1,?tail);
   #EndDo
*   Id Tag(?tail) = 1;
*   .Sort:red-map;
#EndProcedure

* map Reduze ordered propagators to integral
* WARNING - LOOPS passed as FORM argument, LEGS set in symbols.hh
#Procedure ToIntReduze()
* store an ordered list of (inverse) powers of each propagator in ReduzeInt
   Multiply ReduzeInt();
*   Bracket ReduzeInt,
*   #Do i = 0, {`LOOPS'*(`LOOPS'+1)/2 +`LOOPS'*(`LEGS'-1) - 1}
*   ReduzeN`i'
*   #EndDo
*   ;
*   .Sort:red-breduzeint;
*   Keep Brackets;
* (maximal) number of independent scalar products is LOOPS*(LOOPS+1)/2 + LOOPS*(LEGS-1), provided momentum is conserved and LEGS-1<dimS
   #Do i = 0, {`LOOPS'*(`LOOPS'+1)/2 +`LOOPS'*(`LEGS'-1) - 1}
      Id ReduzeN`i'^sDUMMY1? * ReduzeInt(?head) = ReduzeInt(?head,-sDUMMY1);
   #EndDo
   .Sort:red-toint1;
   Id Sector(sDUMMY1?,?head)*ReduzeInt(?tail)=Sector(sDUMMY1,?head)*ReduzeInt(sDUMMY1,?tail);
   Id Crossing(sDUMMY1?)*ReduzeInt(sDUMMY2?,?tail)=ReduzeInt(sDUMMY1,?tail);
   .Sort:red-toint2;
#EndProcedure
