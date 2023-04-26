Functions USpa, USpb, UbarSpa, UbarSpb;
Functions Gamma5, ProjPlus, ProjMinus, trL, trR;
NTensors Sm, Sm4, SmEps;
CTensors d(symmetric), d4(symmetric), dEps(symmetric);
CFunction NCContainer, SpERRORTOKEN;
Function SpFlip;
CFunctions Spaa, Spab, Spba, Spbb;
CFunctions Spa2(antisymmetric), Spb2(antisymmetric);
CFunction SpDenominator;
Vectors vDUMMY1, ..., vDUMMY4;
Indices iDUMMY1, ..., iDUMMY5;
Symbols sDUMMY1, ..., sDUMMY4;
CFunctions fDUMMY1, ..., fDUMMY3;
Function nDUMMY1, ..., nDUMMY3;
Set SpORIGSet : USpa, USpb, UbarSpa, UbarSpb;
Set SpIMAGSet : UbarSpa, UbarSpb, USpa, USpb;
Set SpObject : UbarSpa, UbarSpb, USpa, USpb, Sm, Sm4, SmEps,
               Gamma5, ProjPlus, ProjMinus, SpFlip;
#Procedure LightConeDecomposition(vec,lvec,vref,mass)
   #Do sign={-1,+1}
      Id UbarSpa(`vec', `sign') = UbarSpa(`lvec') 
         + (`sign') * `mass' *
           SpDenominator(Spb2(`vref', `lvec')) * UbarSpb(`vref');
      Id UbarSpb(`vec', `sign') = UbarSpb(`lvec') 
         + (`sign') * `mass' *
           SpDenominator(Spa2(`vref', `lvec')) * UbarSpa(`vref');
      Id USpa(`vec', `sign') = USpa(`lvec') 
         + (`sign') * USpb(`vref') * `mass' *
           SpDenominator(Spb2(`lvec', `vref'));
      Id USpb(`vec', `sign') = USpb(`lvec') 
         + (`sign') * USpa(`vref') * `mass' *
           SpDenominator(Spa2(`lvec', `vref'));
   #EndDo
   Id `vec' = `lvec'
      + (`mass') * SpDenominator(Spa2(`lvec', `vref')) *
        (`mass') * SpDenominator(Spb2(`vref', `lvec')) * `vref';
   Normalize SpDenominator;
#EndProcedure

#Procedure tHooftAlgebra()
   Id Sm(iDUMMY1?) = Sm4(iDUMMY1) + SmEps(iDUMMY1);
   Id Gamma5 = ProjPlus - ProjMinus;
   Repeat;
      Id SmEps(iDUMMY1?) * ProjPlus = ProjPlus * SmEps(iDUMMY1);
      Id SmEps(iDUMMY1?) * ProjMinus = ProjMinus * SmEps(iDUMMY1);
      Id Sm4(iDUMMY1?) * ProjPlus = ProjMinus * Sm4(iDUMMY1);
      Id Sm4(iDUMMY1?) * ProjMinus = ProjPlus * Sm4(iDUMMY1);
      Id ProjMinus * ProjMinus = ProjMinus;
      Id ProjPlus * ProjPlus = ProjPlus;
      Id ProjPlus * ProjMinus = 0;
      Id ProjMinus * ProjPlus = 0;
   EndRepeat;
   Id UbarSpa(vDUMMY1?) * ProjPlus = UbarSpa(vDUMMY1);
   Id UbarSpb(vDUMMY1?) * ProjMinus = UbarSpb(vDUMMY1);
   Id UbarSpa(vDUMMY1?) * ProjMinus = 0;
   Id UbarSpb(vDUMMY1?) * ProjPlus = 0;

   Repeat Id SmEps(iDUMMY1?) * Sm4(iDUMMY2?) =
      - Sm4(iDUMMY2) * SmEps(iDUMMY1);
   ChainIn SmEps;
   Id SmEps(?all) = fDUMMY1(?all);
   Repeat;
      Repeat;
         Id fDUMMY1(?head, iDUMMY1?, iDUMMY1?, ?tail) =
            dEps(iDUMMY1, iDUMMY1) * fDUMMY1(?head, ?tail);
         Id fDUMMY1(?head, iDUMMY1?, iDUMMY2?, iDUMMY1?, ?tail) =
            -(dEps(iDUMMY1, iDUMMY1) - 2) * fDUMMY1(?head, iDUMMY2, ?tail);
         Id fDUMMY1(?head, iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY1?, ?tail) =
            + 4 * dEps(iDUMMY2, iDUMMY3) * fDUMMY1(?head, ?tail)
            - (4 - dEps(iDUMMY1, iDUMMY1)) *
              fDUMMY1(?head, iDUMMY2, iDUMMY3, ?tail);
      EndRepeat;
      Id fDUMMY1(iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) =
         + dEps(iDUMMY1, iDUMMY2) * dEps(iDUMMY3, iDUMMY4)
         - dEps(iDUMMY1, iDUMMY3) * dEps(iDUMMY2, iDUMMY4)
         + dEps(iDUMMY1, iDUMMY4) * dEps(iDUMMY2, iDUMMY3);
      Id fDUMMY1(iDUMMY1?, iDUMMY2?, iDUMMY3?) = 0;
      Id fDUMMY1(iDUMMY1?, iDUMMY2?) = dEps(iDUMMY1, iDUMMY2);
      Id fDUMMY1(iDUMMY1?) = 0;
      Id fDUMMY1(iDUMMY1?, iDUMMY2?, ?tail) =
         fDUMMY1(iDUMMY1, 0, 0, iDUMMY2, ?tail);
      Repeat Id fDUMMY1(iDUMMY1?, 0, ?mid, 0, iDUMMY2?, ?tail) =
         + dEps(iDUMMY1, iDUMMY2) * fDUMMY1(?mid, ?tail)
         - fDUMMY1(iDUMMY1, 0, ?mid, iDUMMY2, 0, ?tail);
      Id fDUMMY1(iDUMMY1?, 0, ?mid, 0) = 0;
   EndRepeat;
   Id fDUMMY1 = 1;
   Id d(iDUMMY1?, iDUMMY2?) =
      d4(iDUMMY1, iDUMMY2) + dEps(iDUMMY1, iDUMMY2);
   #Call SpContractMetrics()
#EndProcedure

#Procedure SpClear()
   Id Spaa(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((mod_(nargs_(?GAMMA),2))) *
      Spaa(vDUMMY1, ?GAMMA, vDUMMY2);
   Id Spbb(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((mod_(nargs_(?GAMMA),2))) *
      Spbb(vDUMMY1, ?GAMMA, vDUMMY2);
   Id Spab(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((1-mod_(nargs_(?GAMMA),2))) *
      Spab(vDUMMY1, ?GAMMA, vDUMMY2);
   Id Spba(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((1-mod_(nargs_(?GAMMA),2))) *
      Spba(vDUMMY1, ?GAMMA, vDUMMY2);


#EndProcedure

#Procedure SpCheck()
   Id Spaa(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((mod_(nargs_(?GAMMA),2))) *
      Spaa(vDUMMY1, ?GAMMA, vDUMMY2)
   +   delta_((1-mod_(nargs_(?GAMMA),2))) *
      SpERRORTOKEN(Spaa(vDUMMY1, ?GAMMA, vDUMMY2));
   Id Spbb(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((mod_(nargs_(?GAMMA),2))) *
      Spbb(vDUMMY1, ?GAMMA, vDUMMY2);
   +   delta_((1-mod_(nargs_(?GAMMA),2))) *
      SpERRORTOKEN(Spbb(vDUMMY1, ?GAMMA, vDUMMY2));
   Id Spab(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((1-mod_(nargs_(?GAMMA),2))) *
      Spab(vDUMMY1, ?GAMMA, vDUMMY2)
   +   delta_((mod_(nargs_(?GAMMA),2))) *
      SpERRORTOKEN(Spab(vDUMMY1, ?GAMMA, vDUMMY2));
   Id Spba(vDUMMY1?, ?GAMMA, vDUMMY2?) =
      delta_((1-mod_(nargs_(?GAMMA),2))) *
      Spba(vDUMMY1, ?GAMMA, vDUMMY2)
   +   delta_((mod_(nargs_(?GAMMA),2))) *
      SpERRORTOKEN(Spba(vDUMMY1, ?GAMMA, vDUMMY2));
#EndProcedure

#Procedure SpCollect()
   ChainIn Sm4;
   Id UbarSpa(vDUMMY1?) * Sm4(?tail) = UbarSpa(vDUMMY1, ?tail);
   Id UbarSpb(vDUMMY1?) * Sm4(?tail) = UbarSpb(vDUMMY1, ?tail);

   Id UbarSpa(?all) * USpa(vDUMMY1?) = Spaa(?all, vDUMMY1);
   Id UbarSpb(?all) * USpa(vDUMMY1?) = Spba(?all, vDUMMY1);
   Id UbarSpa(?all) * USpb(vDUMMY1?) = Spab(?all, vDUMMY1);
   Id UbarSpb(?all) * USpb(vDUMMY1?) = Spbb(?all, vDUMMY1);
   ChainOut Sm4;
#EndProcedure

#Procedure SpContract()
   #Call SpClear()
   Repeat;
      Id fDUMMY1?{Spaa,Spab,Spba,Spbb}(
            ?head, iDUMMY1?, ?mid, iDUMMY1?, ?tail) =
         fDUMMY1(nargs_(?mid), ?head, dum_(?mid), ?tail);

      Id fDUMMY1?{Spaa,Spab,Spba,Spbb}(0, ?head, dum_, ?tail) =
         4 * fDUMMY1(?head, ?tail);
      Id fDUMMY1?{Spaa,Spab,Spba,Spbb}(
            sDUMMY1?odd_, ?head, dum_(?mid), ?tail) =
         -2 * fDUMMY1(?head, reverse_(?mid), ?tail);
      Id fDUMMY1?{Spaa,Spab,Spba,Spbb}(
            sDUMMY1?even_, ?head, dum_(?mid, iDUMMY1?), ?tail) =
         + 2 * fDUMMY1(?head, reverse_(?mid), iDUMMY1, ?tail)
         + 2 * fDUMMY1(?head, iDUMMY1, ?mid, ?tail);
      #Do x={a,b}
         #Do y={a,b}
            #If "`x'`y'" == "aa"
                  Id
            #Else
                  Also
            #EndIf
                  Spaa(vDUMMY1?, ?GA, iDUMMY1?, ?GB, vDUMMY2?) *
                        Sp`x'`y'(?head2, iDUMMY1?, ?tail2) =
                  + 2 * Sp`x'a(nargs_(?head2) + nargs_(?GB) - 1,
                          ?head2, ?GB, vDUMMY2) *
                        Spa`y'(nargs_(?GA) + nargs_(?tail2) - 1,
                          vDUMMY1, ?GA, ?tail2)
                  - 2 * Sp`x'a(nargs_(?head2) + nargs_(?GA) - 1,
                          ?head2, reverse_(?GA), vDUMMY1) *
                        Spa`y'(nargs_(?tail2) + nargs_(?GB) - 1,
                          vDUMMY2, reverse_(?GB), ?tail2);
            Also Spbb(vDUMMY1?, ?GA, iDUMMY1?, ?GB, vDUMMY2?) *
                        Sp`x'`y'(?head2, iDUMMY1?, ?tail2) =
                  + 2 * Sp`x'b(nargs_(?head2) + nargs_(?GB) - 1,
                          ?head2, ?GB, vDUMMY2) *
                        Spb`y'(nargs_(?tail2) + nargs_(?GA) - 1,
                          vDUMMY1, ?GA, ?tail2)
                  - 2 * Sp`x'b(nargs_(?head2) + nargs_(?GA) - 1,
                          ?head2, reverse_(?GA), vDUMMY1) *
                        Spb`y'(nargs_(?tail2) + nargs_(?GB) - 1,
                          vDUMMY2, reverse_(?GB), ?tail2);
            Also Spab(vDUMMY1?, ?GA, iDUMMY1?, ?GB, vDUMMY2?) *
                        Sp`x'`y'(?head2, iDUMMY1?, ?tail2) =
                  + 2 * Sp`x'b(nargs_(?head2) + nargs_(?GB) - 1,
                          ?head2, ?GB, vDUMMY2) *
                        Spa`y'(nargs_(?tail2) + nargs_(?GA) - 1,
                          vDUMMY1, ?GA, ?tail2)
                  + 2 * Sp`x'a(nargs_(?head2) + nargs_(?GA) - 1,
                          ?head2, reverse_(?GA), vDUMMY1) *
                        Spb`y'(nargs_(?tail2) + nargs_(?GB) - 1,
                          vDUMMY2, reverse_(?GB), ?tail2);
            Also Spba(vDUMMY1?, ?GA, iDUMMY1?, ?GB, vDUMMY2?) *
                        Sp`x'`y'(?head2, iDUMMY1?, ?tail2) =
                  + 2 * Sp`x'a(nargs_(?head2) + nargs_(?GB) - 1,
                          ?head2, ?GB, vDUMMY2) *
                        Spb`y'(nargs_(?tail2) + nargs_(?GA) - 1,
                          vDUMMY1, ?GA, ?tail2)
                  + 2 * Sp`x'b(nargs_(?head2) + nargs_(?GA) - 1,
                          ?head2, reverse_(?GA), vDUMMY1) *
                        Spa`y'(nargs_(?tail2) + nargs_(?GB) - 1,
                          vDUMMY2, reverse_(?GB), ?tail2);
         #EndDo
      #EndDo
      Id Spaa(sDUMMY1?even_, vDUMMY1?, ?GAMMA, vDUMMY2?) =
         Spaa(vDUMMY1, ?GAMMA, vDUMMY2);
      Id Spaa(sDUMMY1?odd_, vDUMMY1?, ?GAMMA, vDUMMY2?) = 0;
      Id Spbb(sDUMMY1?even_, vDUMMY1?, ?GAMMA, vDUMMY2?) =
         Spbb(vDUMMY1, ?GAMMA, vDUMMY2);
      Id Spbb(sDUMMY1?odd_, vDUMMY1?, ?GAMMA, vDUMMY2?) = 0;
      Id Spab(sDUMMY1?odd_, vDUMMY1?, ?GAMMA, vDUMMY2?) =
         Spab(vDUMMY1, ?GAMMA, vDUMMY2);
      Id Spab(sDUMMY1?even_, vDUMMY1?, ?GAMMA, vDUMMY2?) = 0;
      Id Spba(sDUMMY1?odd_, vDUMMY1?, ?GAMMA, vDUMMY2?) =
         Spba(vDUMMY1, ?GAMMA, vDUMMY2);
      Id Spba(sDUMMY1?even_, vDUMMY1?, ?GAMMA, vDUMMY2?) = 0;

      Id fDUMMY1?{Spaa,Spab,Spba,Spbb}
         (vDUMMY3?, ?head, vDUMMY1?, vDUMMY1?, ?tail, vDUMMY4?) = 
         d4(vDUMMY1, vDUMMY1) *
         fDUMMY1(vDUMMY3, ?head, ?tail, vDUMMY4);
   EndRepeat;
#EndProcedure

#Procedure SpContractMetrics()
   Id dEps(iDUMMY1?, iDUMMY2?) * d4(iDUMMY2?, iDUMMY3?) = 0;
   Repeat Id dEps(iDUMMY1?, iDUMMY2?) * dEps(iDUMMY2?, iDUMMY3?) =
      dEps(iDUMMY1, iDUMMY3);
   Repeat Id d4(iDUMMY1?, iDUMMY2?) * d4(iDUMMY2?, iDUMMY3?) =
      d4(iDUMMY1, iDUMMY3);
   Id d4(iDUMMY1?, iDUMMY1?) = 4;
   Repeat;
      Id d4(iDUMMY1?, iDUMMY2?) * SmEps(iDUMMY2?) = 0;
      Id dEps(iDUMMY1?, iDUMMY2?) * Sm4(iDUMMY2?) = 0;
      Id d4(iDUMMY1?, iDUMMY2?) * Sm4(iDUMMY2?) = Sm4(iDUMMY1);
      Id dEps(iDUMMY1?, iDUMMY2?) * SmEps(iDUMMY2?) = SmEps(iDUMMY1);
      Id dEps(iDUMMY1?, iDUMMY2?) *
         fDUMMY1?{Spaa,Spab,Spba,Spbb}(?head, iDUMMY1?, ?tail) = 0;
      Id d4(iDUMMY1?, iDUMMY2?) *
            fDUMMY1?{Spaa,Spab,Spba,Spbb}(?head, iDUMMY1?, ?tail) =
         fDUMMY1(?head, iDUMMY2, ?tail);
      Id dEps(iDUMMY1?, iDUMMY2?) * vDUMMY1?(iDUMMY1?) = 0;
      Id d4(iDUMMY1?, iDUMMY2?) * vDUMMY1?(iDUMMY1?) = vDUMMY1(iDUMMY2);
   EndRepeat;
#EndProcedure

#Procedure SpContractLeviCivita(?lightlike)
   Repeat Id e_(iDUMMY1?, ..., iDUMMY4?) *
         d4(iDUMMY4?, iDUMMY5?) =
      e_(iDUMMY1, ..., iDUMMY3, iDUMMY5);
   Id e_(iDUMMY1?, ..., iDUMMY4?) * dEps(iDUMMY4?, iDUMMY5?) = 0;
   Contract;
   Id e_(iDUMMY1?, ..., iDUMMY4?) =
      i_ * e_(iDUMMY1, ..., iDUMMY4);

   Repeat Id e_(iDUMMY1?, ..., iDUMMY4?) *
         fDUMMY1?{Spaa,Spab}(?head, iDUMMY4?, ?tail) =
      -i_/2 * (-1)^(nargs_(?head)-1) * (
         + fDUMMY1(?head, iDUMMY1, iDUMMY2, iDUMMY3, ?tail)
         - fDUMMY1(?head, iDUMMY3, iDUMMY2, iDUMMY1, ?tail)
      );
   Repeat Id e_(iDUMMY1?, ..., iDUMMY4?) *
         fDUMMY1?{Spba,Spbb}(?head, iDUMMY4?, ?tail) =
      +i_/2 * (-1)^(nargs_(?head)-1) * (
         + fDUMMY1(?head, iDUMMY1, iDUMMY2, iDUMMY3, ?tail)
         - fDUMMY1(?head, iDUMMY3, iDUMMY2, iDUMMY1, ?tail)
      );
   Id e_(vDUMMY1?{`?lightlike'}, iDUMMY2?, ..., iDUMMY4?) =
      - i_ / 4 * (
         + Spab(vDUMMY1, iDUMMY4, ..., iDUMMY2, vDUMMY1)
         - Spab(vDUMMY1, iDUMMY2, ..., iDUMMY4, vDUMMY1)
      );
   
#EndProcedure

#Procedure SpOpen(?vectors)
   #If "`?vectors'" == ""
      Repeat;
         Id Spaa(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
            Spa2(vDUMMY1, vDUMMY2) * Spba(vDUMMY2, ?tail, vDUMMY3);
         Id Spbb(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
            Spb2(vDUMMY1, vDUMMY2) * Spab(vDUMMY2, ?tail, vDUMMY3);
         Id Spab(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
            Spa2(vDUMMY1, vDUMMY2) * Spbb(vDUMMY2, ?tail, vDUMMY3);
         Id Spba(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
            Spb2(vDUMMY1, vDUMMY2) * Spaa(vDUMMY2, ?tail, vDUMMY3);
         Id Spaa(vDUMMY1?, vDUMMY3?) = Spa2(vDUMMY1, vDUMMY3);
         Id Spbb(vDUMMY1?, vDUMMY3?) = Spb2(vDUMMY1, vDUMMY3);
         Id Spab(vDUMMY1?, vDUMMY3?) = 0;
         Id Spba(vDUMMY1?, vDUMMY3?) = 0;
      EndRepeat;
      Argument SpDenominator;
         Repeat;
            Id Spaa(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
               Spa2(vDUMMY1, vDUMMY2) * Spba(vDUMMY2, ?tail, vDUMMY3);
            Id Spbb(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
               Spb2(vDUMMY1, vDUMMY2) * Spab(vDUMMY2, ?tail, vDUMMY3);
            Id Spab(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
               Spa2(vDUMMY1, vDUMMY2) * Spbb(vDUMMY2, ?tail, vDUMMY3);
            Id Spba(vDUMMY1?, vDUMMY2?, ?tail, vDUMMY3?) =
               Spb2(vDUMMY1, vDUMMY2) * Spaa(vDUMMY2, ?tail, vDUMMY3);
            Id Spaa(vDUMMY1?, vDUMMY3?) = Spa2(vDUMMY1, vDUMMY3);
            Id Spbb(vDUMMY1?, vDUMMY3?) = Spb2(vDUMMY1, vDUMMY3);
            Id Spab(vDUMMY1?, vDUMMY3?) = 0;
            Id Spba(vDUMMY1?, vDUMMY3?) = 0;
         EndRepeat;
      EndArgument;
   #Else
      Repeat;
         Id Spaa(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
            fDUMMY1(nargs_(?head),Spaa(vDUMMY1, ?head, vDUMMY3) * Spba(vDUMMY3, ?tail, vDUMMY2),Spab(vDUMMY1, ?head, vDUMMY3) * Spaa(vDUMMY3, ?tail, vDUMMY2));
         Id Spab(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
            fDUMMY1(nargs_(?head),Spaa(vDUMMY1, ?head, vDUMMY3) * Spbb(vDUMMY3, ?tail, vDUMMY2),Spab(vDUMMY1, ?head, vDUMMY3) * Spab(vDUMMY3, ?tail, vDUMMY2));
         Id Spba(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
            fDUMMY1(nargs_(?head),Spbb(vDUMMY1, ?head, vDUMMY3) * Spaa(vDUMMY3, ?tail, vDUMMY2),Spba(vDUMMY1, ?head, vDUMMY3) * Spba(vDUMMY3, ?tail, vDUMMY2));
         Id Spbb(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
            fDUMMY1(nargs_(?head),Spbb(vDUMMY1, ?head, vDUMMY3) * Spab(vDUMMY3, ?tail, vDUMMY2),Spba(vDUMMY1, ?head, vDUMMY3) * Spbb(vDUMMY3, ?tail, vDUMMY2));
         Id fDUMMY1(sDUMMY1?even_, sDUMMY2?, sDUMMY3?) = sDUMMY2;
         Id fDUMMY1(sDUMMY1?odd_, sDUMMY2?, sDUMMY3?) = sDUMMY3;
         Id Spaa(vDUMMY1?, vDUMMY2?) = Spa2(vDUMMY1, vDUMMY2);
         Id Spbb(vDUMMY1?, vDUMMY2?) = Spb2(vDUMMY1, vDUMMY2);
         Id Spab(vDUMMY1?, vDUMMY2?) = 0;
         Id Spba(vDUMMY1?, vDUMMY2?) = 0;
         
      EndRepeat;
      Argument SpDenominator;
         Repeat;
            Id Spaa(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
               fDUMMY1(nargs_(?head),Spaa(vDUMMY1, ?head, vDUMMY3) * Spba(vDUMMY3, ?tail, vDUMMY2),Spab(vDUMMY1, ?head, vDUMMY3) * Spaa(vDUMMY3, ?tail, vDUMMY2));
            Id Spab(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
               fDUMMY1(nargs_(?head),Spaa(vDUMMY1, ?head, vDUMMY3) * Spbb(vDUMMY3, ?tail, vDUMMY2),Spab(vDUMMY1, ?head, vDUMMY3) * Spab(vDUMMY3, ?tail, vDUMMY2));
            Id Spba(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
               fDUMMY1(nargs_(?head),Spbb(vDUMMY1, ?head, vDUMMY3) * Spaa(vDUMMY3, ?tail, vDUMMY2),Spba(vDUMMY1, ?head, vDUMMY3) * Spba(vDUMMY3, ?tail, vDUMMY2));
            Id Spbb(vDUMMY1?, ?head, vDUMMY3?{`?vectors',}, ?tail, vDUMMY2?) =
               fDUMMY1(nargs_(?head),Spbb(vDUMMY1, ?head, vDUMMY3) * Spab(vDUMMY3, ?tail, vDUMMY2),Spba(vDUMMY1, ?head, vDUMMY3) * Spbb(vDUMMY3, ?tail, vDUMMY2));
            Id fDUMMY1(sDUMMY1?even_, sDUMMY2?, sDUMMY3?) = sDUMMY2;
            Id fDUMMY1(sDUMMY1?odd_, sDUMMY2?, sDUMMY3?) = sDUMMY3;
            Id Spaa(vDUMMY1?, vDUMMY2?) = Spa2(vDUMMY1, vDUMMY2);
            Id Spbb(vDUMMY1?, vDUMMY2?) = Spb2(vDUMMY1, vDUMMY2);
            Id Spab(vDUMMY1?, vDUMMY2?) = 0;
            Id Spba(vDUMMY1?, vDUMMY2?) = 0;
            
         EndRepeat;
      EndArgument;
   #EndIf
   Normalize SpDenominator;
   #If `SPCANCEL'
      Repeat;
         Id Spa2(vDUMMY1?, k2?) * SpDenominator(Spa2(vDUMMY1?, k2?)) = 1;
         Id Spb2(vDUMMY1?, k2?) * SpDenominator(Spb2(vDUMMY1?, k2?)) = 1;
      EndRepeat;
   #EndIf
#EndProcedure

#Define SPCANCEL "1"

#Procedure SpClose(?vectors)
   #If "`?vectors'" == ""
      Id Spa2(vDUMMY1?, vDUMMY2?) * Spb2(vDUMMY2?, vDUMMY3?) =
         Spab(vDUMMY1, vDUMMY2, vDUMMY3);
      Repeat;
      #Do X={a,b}
         Id Sp`X'b(?head, vDUMMY1?) * Spa2(vDUMMY1?, vDUMMY2?) =
            Sp`X'a(?head, vDUMMY1, vDUMMY2);
         Id Sp`X'a(?head, vDUMMY1?) * Spb2(vDUMMY1?, vDUMMY2?) =
            Sp`X'b(?head, vDUMMY1, vDUMMY2);
         Id Spb`X'(vDUMMY1?, ?tail) * Spa2(vDUMMY2?, vDUMMY1?) =
            Spa`X'(vDUMMY2, vDUMMY1, ?tail);
         Id Spa`X'(vDUMMY1?, ?tail) * Spb2(vDUMMY2?, vDUMMY1?) =
            Spb`X'(vDUMMY2, vDUMMY1, ?tail);
      #EndDo
      EndRepeat;
      Repeat;
      #Do X={a,b}
         #Do Y={a,b}
            Id Sp`X'b(?head, vDUMMY1?) * Spa`Y'(vDUMMY1?, ?tail) =
               Sp`X'`Y'(?head, vDUMMY1, ?tail);
            Id Sp`X'a(?head, vDUMMY1?) * Spb`Y'(vDUMMY1?, ?tail) =
               Sp`X'`Y'(?head, vDUMMY1, ?tail);
         #EndDo
         Id Sp`X'b(?head1, vDUMMY1?) * Spaa(?head2, vDUMMY1?) =
            - Sp`X'a(?head1, vDUMMY1, reverse_(?head2));
         Id Sp`X'b(?head1, vDUMMY1?) * Spba(?head2, vDUMMY1?) =
            + Sp`X'b(?head1, vDUMMY1, reverse_(?head2));
         Id Sp`X'a(?head1, vDUMMY1?) * Spbb(?head2, vDUMMY1?) =
            - Sp`X'b(?head1, vDUMMY1, reverse_(?head2));
         Id Sp`X'a(?head1, vDUMMY1?) * Spab(?head2, vDUMMY1?) =
               + Sp`X'a(?head1, vDUMMY1, reverse_(?head2));
      #EndDo
      EndRepeat;
   #Else
      Id Spa2(vDUMMY1?, vDUMMY2?{`?vectors',}) *
             Spb2(vDUMMY2?{`?vectors',}, vDUMMY3?) =
         Spab(vDUMMY1, vDUMMY2, vDUMMY3);
      Repeat;
      #Do X={a,b}
         Id Sp`X'b(?head, vDUMMY1?{`?vectors',}) * Spa2(vDUMMY1?{`?vectors',}, vDUMMY2?) =
            Sp`X'a(?head, vDUMMY1, vDUMMY2);
         Id Sp`X'a(?head, vDUMMY1?{`?vectors',}) * Spb2(vDUMMY1?{`?vectors',}, vDUMMY2?) =
            Sp`X'b(?head, vDUMMY1, vDUMMY2);
         Id Spb`X'(vDUMMY1?{`?vectors',}, ?tail) * Spa2(vDUMMY2?, vDUMMY1?{`?vectors',}) =
            Spa`X'(vDUMMY2, vDUMMY1, ?tail);
         Id Spa`X'(vDUMMY1?{`?vectors',}, ?tail) * Spb2(vDUMMY2?, vDUMMY1?{`?vectors',}) =
            Spb`X'(vDUMMY2, vDUMMY1, ?tail);
      #EndDo
      EndRepeat;
      Repeat;
      #Do X={a,b}
         #Do Y={a,b}
            Id Sp`X'b(?head, vDUMMY1?{`?vectors',}) * Spa`Y'(vDUMMY1?{`?vectors',}, ?tail) =
               Sp`X'`Y'(?head, vDUMMY1, ?tail);
            Id Sp`X'a(?head, vDUMMY1?{`?vectors',}) * Spb`Y'(vDUMMY1?{`?vectors',}, ?tail) =
               Sp`X'`Y'(?head, vDUMMY1, ?tail);
         #EndDo
         Id Sp`X'b(?head1, vDUMMY1?{`?vectors',}) * Spaa(?head2, vDUMMY1?{`?vectors',}) =
            - Sp`X'a(?head1, vDUMMY1, reverse_(?head2));
         Id Sp`X'b(?head1, vDUMMY1?{`?vectors',}) * Spba(?head2, vDUMMY1?{`?vectors',}) =
            + Sp`X'b(?head1, vDUMMY1, reverse_(?head2));
         Id Sp`X'a(?head1, vDUMMY1?{`?vectors',}) * Spbb(?head2, vDUMMY1?{`?vectors',}) =
            - Sp`X'b(?head1, vDUMMY1, reverse_(?head2));
         Id Sp`X'a(?head1, vDUMMY1?{`?vectors',}) * Spab(?head2, vDUMMY1?{`?vectors',}) =
               + Sp`X'a(?head1, vDUMMY1, reverse_(?head2));
      #EndDo
      EndRepeat;
      Id Spaa(vDUMMY1?{`?vectors',}, ?s1, vDUMMY2?!{`?vectors',}, ?s2,
            vDUMMY1?{`?vectors',}) =
         fDUMMY1(Spaa, Spbb, nargs_(vDUMMY1, ?s1),
            vDUMMY2, ?s2, vDUMMY1, ?s1, vDUMMY2);
      Id Spbb(vDUMMY1?{`?vectors',}, ?s1, vDUMMY2?!{`?vectors',}, ?s2,
            vDUMMY1?{`?vectors',}) =
         fDUMMY1(Spbb, Spaa, nargs_(vDUMMY1, ?s1),
            vDUMMY2, ?s2, vDUMMY1, ?s1, vDUMMY2);
      Id Spab(vDUMMY1?{`?vectors',}, ?s1, vDUMMY2?!{`?vectors',}, ?s2,
            vDUMMY1?{`?vectors',}) =
         fDUMMY1(Spab, Spba, nargs_(vDUMMY1, ?s1),
            vDUMMY2, ?s2, vDUMMY1, ?s1, vDUMMY2);
      Id Spba(vDUMMY1?{`?vectors',}, ?s1, vDUMMY2?!{`?vectors',}, ?s2,
            vDUMMY1?{`?vectors',}) =
         fDUMMY1(Spba, Spab, nargs_(vDUMMY1, ?s1),
            vDUMMY2, ?s2, vDUMMY1, ?s1, vDUMMY2);
      Id fDUMMY1(fDUMMY2?, fDUMMY3?, sDUMMY1?even_, ?tail) =
         fDUMMY2(?tail);
      Also fDUMMY1(fDUMMY2?, fDUMMY3?, sDUMMY1?odd_, ?tail) =
         fDUMMY3(?tail);
   #EndIf
#EndProcedure
#Procedure SpTrace4(?lightlike)
   ChainIn Sm4;
   Id trL * Sm4(?args) * trR = 
      + trL * ProjPlus  * Sm4(?args) * trR
      + trL * ProjMinus * Sm4(?args) * trR;
   Id trL * ProjPlus * trR = 2;
   Id trL * ProjMinus * trR = 2;
   Id trL * trR = 4;
   #If "`?lightlike'" != ""
      Id trL * ProjPlus * Sm4(?head, vDUMMY1?{`?lightlike'}, ?tail) * trR =
         fDUMMY1(+1, nargs_(?head), nargs_(?tail),
            ?head, vDUMMY1, sDUMMY1, ?tail);
      Id trL * ProjMinus * Sm4(?head, vDUMMY1?{`?lightlike'}, ?tail) * trR =
         fDUMMY1(-1, nargs_(?head), nargs_(?tail),
            ?head, vDUMMY1, sDUMMY1, ?tail);
      Id fDUMMY1(sDUMMY4?, sDUMMY2?even_, sDUMMY3?even_, ?tail) = 0;
      Id fDUMMY1(sDUMMY4?, sDUMMY2?odd_, sDUMMY3?odd_, ?tail) = 0;
      Id fDUMMY1(+1, sDUMMY2?even_, sDUMMY3?odd_,
            ?head, vDUMMY1?, sDUMMY1, ?tail) =
         Spba(vDUMMY1, ?tail, ?head, vDUMMY1);
      Id fDUMMY1(-1, sDUMMY2?even_, sDUMMY3?odd_,
            ?head, vDUMMY1?, sDUMMY1, ?tail) =
         Spab(vDUMMY1, ?tail, ?head, vDUMMY1);
      Id fDUMMY1(+1, sDUMMY2?odd_, sDUMMY3?even_,
            ?head, vDUMMY1?, sDUMMY1, ?tail) =
         Spab(vDUMMY1, ?tail, ?head, vDUMMY1);
      Id fDUMMY1(-1, sDUMMY2?odd_, sDUMMY3?even_,
            ?head, vDUMMY1?, sDUMMY1, ?tail) =
         Spba(vDUMMY1, ?tail, ?head, vDUMMY1);
      
   #EndIf
   Repeat;
      Id once trL * ProjPlus * Sm4(?args) * trR =
         1/2 * g_(1, 6_, ?args);
      Trace4, 1;
   EndRepeat;
   Repeat;
      Id once trL * ProjMinus * Sm4(?args) * trR =
         1/2 * g_(1, 7_, ?args);
      Trace4, 1;
   EndRepeat;
   ChainOut Sm4;
#EndProcedure

#Procedure SpTracify(left,right,aux,?internal)
   #if "`?internal'" == ""
   Id Spaa(`left',?chain,`right') = SpDenominator(Spbb(`right',`left')) * trL * ProjMinus * Sm4(`left',?chain,`right') * trR;
   Id Spbb(`left',?chain,`right') = SpDenominator(Spaa(`right',`left')) * trL * ProjPlus * Sm4(`left',?chain,`right') * trR;
   Id Spab(`left',?chain,`right') = SpDenominator(Spab(`right',`aux',`left')) * trL * ProjMinus * Sm4(`left',?chain,`right',`aux') * trR;
   Id Spba(`left',?chain,`right') = SpDenominator(Spba(`right',`aux',`left')) * trL * ProjPlus * Sm4(`left',?chain,`right',`aux') * trR;
   #else
      #Do momentum={`?internal'}
         Id Spaa(`left',?head, `momentum', ?tail,`right') = SpDenominator(Spbb(`right',`left')) * trL * ProjMinus * Sm4(`left',?head,`momentum',?tail,`right') * trR;
         Id Spbb(`left',?head, `momentum', ?tail,`right') = SpDenominator(Spaa(`right',`left')) * trL * ProjPlus * Sm4(`left',?head,`momentum',?tail,`right') * trR;
         Id Spab(`left',?head, `momentum', ?tail,`right') = SpDenominator(Spab(`right',`aux',`left')) * trL * ProjMinus * Sm4(`left',?head,`momentum',?tail,`right',`aux') * trR;
         Id Spba(`left',?head, `momentum', ?tail,`right') = SpDenominator(Spba(`right',`aux',`left')) * trL * ProjPlus * Sm4(`left',?head,`momentum',?tail,`right',`aux') * trR;
      #enddo
   #endif
   ChainOut Sm4;
#EndProcedure

#Procedure SpOrder(?all)
   #Define flag "0"
   Repeat;
   #Do p={`?all'}
      #Redefine flag "0"
      #Do q={`?all'}
         #If "`p'" == "`q'"
            #Redefine flag "1"
            Id Sm(`p') * Sm(`p') = d(`p', `p');
            Id SmEps(`p') * SmEps(`p') = dEps(`p', `p');
            Id Sm4(`p') * Sm4(`p') = d4(`p', `p');
            Id Sm4(`p') * SmEps(`p') = 0;
            Id SmEps(`p') * Sm4(`p') = 0;
         #Else
            #If `flag'
               Id Sm(`q') * Sm(`p') = 2 * d(`p', `q') - Sm(`p') * Sm(`q');
               Id SmEps(`q') * SmEps(`p') = 2 * dEps(`p', `q') - SmEps(`p') * SmEps(`q');
               Id Sm4(`q') * Sm4(`p') = 2 * d4(`p', `q') - Sm4(`p') * Sm4(`q');
               Id Sm4(`q') * SmEps(`p') = - SmEps(`p') * Sm4(`q');
               Id SmEps(`q') * Sm4(`p') = - Sm4(`p') * SmEps(`q');
            #EndIf
         #EndIf
      #EndDo
   #EndDo
   EndRepeat;
#EndProcedure
#Procedure Schouten(arg1,?argv)
   #Call ASchouten(`arg1',`?argv')
   #Call BSchouten(`arg1',`?argv')
#EndProcedure

#Procedure ASchouten(arg1,?argv)
   #Define x "a"
   #Define argc "1"
   #If "`?argv'" != ""
      #Do arg={`?argv'}
         #ReDefine argc "{`argc'+1}"
         #Define arg`argc' "`arg'"
      #EndDo
   #EndIf
   
   #Switch `argc'
   #Case 1
      Repeat;
         
         #Do s1={+,-}
            #Do s2={+,-}
               Id Sp`x'2(`arg1', vDUMMY1?) *
                  SpDenominator(`s1'Sp`x'2(`arg1', vDUMMY2?!{vDUMMY3?})) *
                  SpDenominator(`s2'Sp`x'2(`arg1', vDUMMY3?!{vDUMMY2?})) =
             (`s1'1)*(`s2'1)*(
                     + Sp`x'2(vDUMMY2, vDUMMY1) *
                       SpDenominator(Sp`x'2(`arg1', vDUMMY2)) *
                       SpDenominator(Sp`x'2(vDUMMY2, vDUMMY3))
                     - Sp`x'2(vDUMMY3, vDUMMY1) *
                       SpDenominator(Sp`x'2(`arg1', vDUMMY3)) *
                       SpDenominator(Sp`x'2(vDUMMY2, vDUMMY3)));
            #EndDo
         #EndDo
         
      EndRepeat;
   #Break
   #Case 3
      Repeat;
         Id Sp`x'2(`arg1', `arg2') * Sp`x'2(`arg3', vDUMMY1?!{`arg1',`arg2'}) =
            + Sp`x'2(`arg1', vDUMMY1) * Sp`x'2(`arg3', `arg2')
            + Sp`x'2(`arg1', `arg3') * Sp`x'2(`arg2', vDUMMY1);
         
      EndRepeat;
   #Break
   #Case 4
      Repeat;
         Id Sp`x'2(`arg1', `arg2') * Sp`x'2(`arg3', `arg4') =
            + Sp`x'2(`arg1', `arg4') * Sp`x'2(`arg3', `arg2')
            + Sp`x'2(`arg1', `arg3') * Sp`x'2(`arg2', `arg4');
         
      EndRepeat;
   #Break
   #Default
      #Message Warning: [AB]Schouten called with `argc' arguments.
      #Message This procedure call has been ignored.
   #EndSwitch
   
#EndProcedure

#Procedure BSchouten(arg1,?argv)
   #Define x "b"
   #Define argc "1"
   #If "`?argv'" != ""
      #Do arg={`?argv'}
         #ReDefine argc "{`argc'+1}"
         #Define arg`argc' "`arg'"
      #EndDo
   #EndIf
   
   #Switch `argc'
   #Case 1
      Repeat;
         
         #Do s1={+,-}
            #Do s2={+,-}
               Id Sp`x'2(`arg1', vDUMMY1?) *
                  SpDenominator(`s1'Sp`x'2(`arg1', vDUMMY2?!{vDUMMY3?})) *
                  SpDenominator(`s2'Sp`x'2(`arg1', vDUMMY3?!{vDUMMY2?})) =
             (`s1'1)*(`s2'1)*(
                     + Sp`x'2(vDUMMY2, vDUMMY1) *
                       SpDenominator(Sp`x'2(`arg1', vDUMMY2)) *
                       SpDenominator(Sp`x'2(vDUMMY2, vDUMMY3))
                     - Sp`x'2(vDUMMY3, vDUMMY1) *
                       SpDenominator(Sp`x'2(`arg1', vDUMMY3)) *
                       SpDenominator(Sp`x'2(vDUMMY2, vDUMMY3)));
            #EndDo
         #EndDo
         
      EndRepeat;
   #Break
   #Case 3
      Repeat;
         Id Sp`x'2(`arg1', `arg2') * Sp`x'2(`arg3', vDUMMY1?!{`arg1',`arg2'}) =
            + Sp`x'2(`arg1', vDUMMY1) * Sp`x'2(`arg3', `arg2')
            + Sp`x'2(`arg1', `arg3') * Sp`x'2(`arg2', vDUMMY1);
         
      EndRepeat;
   #Break
   #Case 4
      Repeat;
         Id Sp`x'2(`arg1', `arg2') * Sp`x'2(`arg3', `arg4') =
            + Sp`x'2(`arg1', `arg4') * Sp`x'2(`arg3', `arg2')
            + Sp`x'2(`arg1', `arg3') * Sp`x'2(`arg2', `arg4');
         
      EndRepeat;
   #Break
   #Default
      #Message Warning: [AB]Schouten called with `argc' arguments.
      #Message This procedure call has been ignored.
   #EndSwitch
   
#EndProcedure

#Procedure RemoveNCContainer()
   SplitArg NCContainer;
   Repeat Id NCContainer(sDUMMY1?, sDUMMY2?, ?mid, iDUMMY1?, iDUMMY2?) =
      + NCContainer(sDUMMY1, iDUMMY1, iDUMMY2)
      + NCContainer(sDUMMY2, ?mid, iDUMMY1, iDUMMY2);
   Normalize NCContainer;
   Argument NCContainer;
      Repeat;
         Id nDUMMY1?(?args1) * nDUMMY2?(?args2) =
            NCOrder(nDUMMY1(?args1), nDUMMY2(?args2));
         Id nDUMMY1?(?args1) * Sm?(?args2) =
            NCOrder(nDUMMY1(?args1), Sm(?args2));
         Id Sm?(?args1) * nDUMMY2?(?args2) =
            NCOrder(Sm(?args1), nDUMMY2(?args2));
      EndRepeat;
      Repeat Id NCOrder(?head,NCOrder(?mid),?tail) =
         NCOrder(?head,?mid,?tail);
   EndArgument;
   Id NCContainer(?head,NCOrder(?mid),?tail) = NCContainer(?head,?mid,?tail);
   Repeat;
      Id NCContainer(?head, iDUMMY1?, iDUMMY2?) *
            NCContainer(?tail, iDUMMY2?, iDUMMY3?) =
         NCContainer(?head, ?tail, iDUMMY1, iDUMMY3);
      #IfNDef `NOSPFLIP'
         Id NCContainer(?head, iDUMMY1?, iDUMMY2?) *
               NCContainer(?tail, iDUMMY3?, iDUMMY2?) =

                  NCContainer(?head, iDUMMY1, iDUMMY2) *
                     SpFlip(?tail, iDUMMY2, iDUMMY3);
         Id NCContainer(?head, iDUMMY1?, iDUMMY2?) *
               NCContainer(?tail, iDUMMY1?, iDUMMY3?) =
                  SpFlip(?head, iDUMMY2, iDUMMY1) *
                     NCContainer(?tail, iDUMMY1, iDUMMY3);
         Id SpFlip(?args, iDUMMY1?, iDUMMY2?) = 
               nDUMMY1(reverse_(?args),iDUMMY1, iDUMMY2);
         Repeat;
            Id Once nDUMMY1(sDUMMY1?, sDUMMY2?, ?mid, iDUMMY1?, iDUMMY2?) =
               SpFlip(sDUMMY1, iDUMMY1, iDUMMY3) *
               nDUMMY1(sDUMMY2, ?mid, iDUMMY3, iDUMMY2);
            Sum iDUMMY3;
         EndRepeat;
         Id nDUMMY1(sDUMMY1?, iDUMMY1?, iDUMMY2?) =
            SpFlip(sDUMMY1, iDUMMY1, iDUMMY2);

         #Do Sm={Sm,Sm4,SmEps}
            Id SpFlip(`Sm'(iDUMMY1?), iDUMMY2?, iDUMMY3?) =
               - NCContainer(`Sm'(iDUMMY1), iDUMMY2, iDUMMY3);
         #EndDo
         Id SpFlip(nDUMMY1?{Gamma5,ProjPlus,ProjMinus}, iDUMMY2?, iDUMMY3?) =
            NCContainer(nDUMMY1, iDUMMY2, iDUMMY3);
         Id SpFlip(sDUMMY1?symbol_, iDUMMY2?, iDUMMY3?) =
               sDUMMY1 * NCContainer(1, iDUMMY2, iDUMMY3);
         Id SpFlip(sDUMMY1?number_, iDUMMY2?, iDUMMY3?) =
               sDUMMY1 * NCContainer(1, iDUMMY2, iDUMMY3);
         Id SpFlip(?all) = SpERRORTOKEN(?all);
      #EndIf
   EndRepeat;
   Id NCContainer(?string, iDUMMY1?, iDUMMY1?) =
      NCContainer(trL, ?string, trR);
   Id NCContainer(?string, iDUMMY1?, iDUMMY2?) *
               NCContainer(fDUMMY1?{UbarSpa,UbarSpb}(?spargs), iDUMMY1?) =
         NCContainer(fDUMMY1(?spargs), ?string, iDUMMY2);
   Id NCContainer(?string, iDUMMY1?, iDUMMY2?) *
               NCContainer(fDUMMY1?{USpa,USpb}(?spargs), iDUMMY1?) =
         NCContainer(SpFlip(fDUMMY1(?spargs)), ?string, iDUMMY2);
   Id NCContainer(?string, iDUMMY1?) *
               NCContainer(fDUMMY1?{UbarSpa,UbarSpb}(?spargs), iDUMMY1?) =
         NCContainer(?string, SpFlip(fDUMMY1(?spargs)));
   Id NCContainer(?string, iDUMMY1?) *
               NCContainer(fDUMMY1?{USpa,USpb}(?spargs), iDUMMY1?) =
         NCContainer(?string, fDUMMY1(?spargs));
   #IfNDef `NOSPFLIP'
      Argument NCContainer;
         Id SpFlip(nDUMMY1?SpORIGSet?SpIMAGSet(vDUMMY1?)) =
            nDUMMY1(vDUMMY1);
         Id SpFlip(nDUMMY1?SpORIGSet?SpIMAGSet(vDUMMY1?, sDUMMY1?)) =
            nDUMMY1(vDUMMY1, -sDUMMY1);
      EndArgument;
   #EndIf
   Repeat Id NCContainer(sDUMMY1?, sDUMMY2?, ?tail) =
      NCContainer(sDUMMY1 * sDUMMY2, ?tail);
   Id NCContainer(sDUMMY1?) = sDUMMY1;
#EndProcedure

