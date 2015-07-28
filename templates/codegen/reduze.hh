* try to make contractions work in dim dimensions
Symbols dimS,dimD;
Dimension dimS; * space-time dimension (normally d)
*UnitTrace dimD; * dirac algebra dimension (normally 4)


***** DO NOT PUBLISH *****
AutoDeclare Symbols F1,F2,F3,F4,F5;
***** DO NOT PUBLISH *****


AutoDeclare Symbols ReduzeT; * topologies/integral families
AutoDeclare Symbols ReduzeN; * propagators
AutoDeclare Symbols Proj; * projector labels
CFunction prf; * for PolyRatFun
CFunction Sector;
CFunction Tag; * container for momentum/mass of ReduzeN
CFunction Shift; * container for momentum shifts
CFunction DiaMatch; * container for diagram number
CFunction Crossing, CrossingShift, CrossingInvariants; * functions to store crossings
CFunctions num; * inverse propagator num=inv^(-1)
CFunctions INT; * Reduze integral function (stores the inverse powers of the propagators)
CFunction ProjDen; * function for storing projector denominators ProjDen(x)=1/x;
CFunction DenDim; * function for storing dimension denominators DenDim(dimS+n) = 1/(dimS+n);
CFunction Dim; * function for storing dimension numerators Dim(dimS) = dimS;
CFunction Den;
CFunctions Projector, ProjLabel; * functions for storing the projector and its label
Symbols sDUMMY5,[];

* disable spinor flipping rules in spinney.hh (RemoveNCContainer)
* does not implement arXiv:1008.0803v1 Eq(21), discussion at the end of section 3.5.2
#Define NOSPFLIP

* tag each diagram with DiaMatch(qgraf_digram_index)
#Procedure DiaMatchTagReduze()
   Multiply DiaMatch(`DIAG');
#EndProcedure

* screen inplorentz, outlorentz
#Procedure ScreenExternalReduze()
   Id fDUMMY1?{inplorentz,outlorentz}(?tail) = SCREEN(fDUMMY1(?tail));
#EndProcedure

* compute trace in d dimensions
* input: trL*Sm(a)*Sm(b)*...*Sm(c)*trR (= Tr[\gamma^a \gamma^b ... \gamma^c])
* WARNING - NOT SURE THIS HANDLES OPEN SPIN LINES CORRECTLY
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
#Procedure ShiftReduze()
   #include- reduzeshiftsl`LOOPS'.hh
   Repeat Id Shift(?head,[],?tail) = Shift(?head,?tail);
   Id Once Shift(?tail) = replace_(?tail);
   .Sort:red-shifting;
#EndProcedure
                  
#Procedure CrossReduze()
   #include- reduzecrossingl`LOOPS'.hh
#EndProcedure

* map crossed integral families to uncrossed
#Procedure CrossMomentaReduze()
   Repeat Id CrossingShift(?head,[],?tail) = CrossingShift(?head,?tail);
   Id Once CrossingShift(?tail) = replace_(?tail);
   .Sort:red-crossing;
#EndProcedure

* assumes that CrossingInvariants() already exists in the expression
#Procedure CrossInvariantsReduze()
   Repeat Id CrossingInvariants(?head,[],?tail) = CrossingInvariants(?head,?tail);
   Id Once CrossingInvariants(?tail) = replace_(?tail);
   .Sort:red-crossinginvar;
#EndProcedure
                  
* map scalar products to (inverse) propagators
#Procedure SPToPropReduze()
   #include- reduzesptopl`LOOPS'.hh
   .Sort:SPToPropReduze;
#EndProcedure
                     
#Procedure TagReduze()
   #include- reduzemapl`LOOPS'.hh
#EndProcedure
                   
* map propagators to Reduze ordered propagators
#Procedure MapReduze()
   #Call TagReduze
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
   Id Tag(?tail) = 1;
*  .Sort:red-map;
#EndProcedure

* map Reduze ordered propagators to integral (LOOPS passed as FORM argument, LEGS set in symbols.hh)
#Procedure ToIntReduze()
* store an ordered list of (inverse) powers of each propagator in INT
   Multiply INT(0,0,0,0,[]); * Note: INT(t,ID,r,s,[],...indices...)
* (maximal) number of independent scalar products is LOOPS*(LOOPS+1)/2 + LOOPS*(LEGS-1), provided momentum is conserved and LEGS-1<dimS
   #Do i = 0, {`LOOPS'*(`LOOPS'+1)/2 +`LOOPS'*(`LEGS'-1) - 1}
      Id ReduzeN`i'^sDUMMY1?pos0_ * INT(sDUMMY2?,sDUMMY3?,sDUMMY4?,sDUMMY5?,[],?head) =
         INT(sDUMMY2,sDUMMY3,sDUMMY4,sDUMMY5+sDUMMY1,[],?head,-sDUMMY1); * numerator/zeros
      Id ReduzeN`i'^sDUMMY1?neg_ * INT(sDUMMY2?,sDUMMY3?,sDUMMY4?,sDUMMY5?,[],?head) =
         INT(sDUMMY2+1,sDUMMY3+2^`i',sDUMMY4-sDUMMY1,sDUMMY5,[],?head,-sDUMMY1); * denominator
   #EndDo
   .Sort:red-toint1;
   Id Sector(sDUMMY1?,?head)*INT(?tail)=INT(sDUMMY1,?tail);
   Id Crossing(sDUMMY1?)*INT(sDUMMY2?,?tail)=INT(sDUMMY1,?tail);
   .Sort:red-toint2;
#EndProcedure
             
* tag each integral with its propagators
#Procedure TagIntReduze()
   Id INT(sDUMMY1?,?tail) = Sector(sDUMMY1)*INT(sDUMMY1,?tail);
   #Call CrossReduze
   #Call TagReduze
   #Call CrossMomentaReduze
   Id Crossing(?tail)=1;
   Id CrossingInvariants(?tail) = 1;
   Id Sector(?tail)=1;
#EndProcedure

#Procedure UncrossIntReduze()
   Id INT(sDUMMY1?,?tail) = Sector(sDUMMY1)*INT(sDUMMY1,?tail);
   #Call CrossReduze
#EndProcedure
