* try to make contractions work in dim dimensions
Symbols dimS,dimD;
Dimension dimS; * space-time dimension (normally d)
*UnitTrace dimD; * dirac algebra dimension (normally 4)


***** DO NOT PUBLISH *****
CFunction scalarProduct;
***** DO NOT PUBLISH *****


AutoDeclare Symbols ReduzeF; * topologies/integral families
AutoDeclare Symbols ReduzeN; * propagators
AutoDeclare Symbols ProjCoeff; * projector coefficients
AutoDeclare Symbols ProjLabel; * projector labels
CFunction prf; * for PolyRatFun
CFunction Sector;
CFunction Tag; * container for momentum/mass of ReduzeN
CFunction Shift; * container for momentum shifts
CFunction DiaMatch; * container for diagram number
CFunctions inversePropagator; * inverse propagator inversePropagator(p1,m^2) = p1.p1 - m^2
CFunctions INT; * Reduze integral function (stores the inverse powers of the propagators)
CFunction ProjDen; * function for storing projector denominators ProjDen(x)=1/x;
CFunction ProjNum; * function for storing projector numerators ProjNum(x)=x;
CFunction DenDim; * function for storing dimension denominators DenDim(dimS+n) = 1/(dimS+n);
CFunction Dim; * function for storing dimension numerators Dim(dimS) = dimS;
CFunction Den;
CFunctions Projector, ProjLabel; * functions for storing the projector and its label
Symbols sDUMMY5,[];

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

* map scalar products to (inverse) propagators
#Procedure SPToPropReduze()
   #include- reduzesptopl`LOOPS'.hh
   .Sort:SPToPropReduze;
***** DO NOT PUBLISH *****
   Id scalarProduct(vDUMMY1?,vDUMMY2?) = vDUMMY1.vDUMMY2;
   .sort:SPToPropReduze;
***** DO NOT PUBLISH *****
#EndProcedure
                     
#Procedure TagReduze()
   #include- reduzemapl`LOOPS'.hh
#EndProcedure
                   
* map propagators to Reduze ordered propagators
#Procedure MapReduze()
   #Call TagReduze
* try to map propagators with inv/inversePropagator(+...) and inv/inversePropagator(-...)
   #Do i = 0,1
* map propagators
   Repeat Id Tag(sDUMMY1?,vDUMMY1?,sDUMMY2?)*inv(vDUMMY1?,sDUMMY2?,?tail)=
      Tag(sDUMMY1,vDUMMY1,sDUMMY2)*sDUMMY1^(-1);
   Repeat Id Tag(sDUMMY1?,vDUMMY1?,sDUMMY2?)*inversePropagator(vDUMMY1?,sDUMMY2?^2,?tail)=
      Tag(sDUMMY1,vDUMMY1,sDUMMY2)*sDUMMY1;
* special case for massless inversePropagator
   Repeat Id Tag(sDUMMY1?,vDUMMY1?,0)*inversePropagator(vDUMMY1?,0,?tail)=
      Tag(sDUMMY1,vDUMMY1,0)*sDUMMY1;
* now flip sign of momentum in even functions inv/inversePropagator
   Id inv(vDUMMY1?,?tail)=inv(-vDUMMY1,?tail);
   Id inversePropagator(vDUMMY1?,?tail)=inversePropagator(-vDUMMY1,?tail);
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
   .Sort:red-toint2;
#EndProcedure
             
* tag each integral with its propagators
#Procedure TagIntReduze()
   Id INT(sDUMMY1?,?tail) = Sector(sDUMMY1)*INT(sDUMMY1,?tail);
   #Call TagReduze
   Id Sector(?tail)=1;
#EndProcedure

#Procedure FeedPolyRatFun(?exclude)

Repeat Id sDUMMY1?!{,`?exclude'}^sDUMMY2?pos_ = prf(sDUMMY1^sDUMMY2,1);
Repeat Id sDUMMY1?!{,`?exclude'}^sDUMMY2?neg_ = prf(1,sDUMMY1^(-sDUMMY2));
Repeat Id sDUMMY1?!{,`?exclude'} = prf(sDUMMY1,1);

Repeat Id Den(sDUMMY1?) = prf(1,sDUMMY1);

*Repeat Id Dim(sDUMMY1?) = prf(sDUMMY1,1);
*Repeat Id DenDim(sDUMMY1?) = prf(1,sDUMMY1);

Repeat Id ProjNum(sDUMMY1?) = prf(sDUMMY1,1);
Repeat Id ProjDen(sDUMMY1?) = prf(1,sDUMMY1);

.Sort:feed prf;

#EndProcedure
