[% ' # vim: ts=3:sw=3:syntax=golem
%]* vim[% ' %]: syntax=form
#procedure subscriptreplace(INRANK)
AutoDeclare S Vec;
AutoDeclare S dtensor;
[% @if extension formopt %]
#do irank=0,`INRANK'[%
@for pairs distinct %]
   Id SUBSCRIPT(spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %],iv`irank') = Vecspva[% 
					@if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]iv`irank';[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id SUBSCRIPT(spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %],iv`irank') = Vecspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %]iv`irank';
   Id SUBSCRIPT(spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %],iv`irank')= Vecspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]iv`irank';[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id SUBSCRIPT(spvae[%index1%]e[%index2%],iv`irank') =Vecspvae[%index1%]e[%index2%]iv`irank';
   Id SUBSCRIPT(spvae[%index2%]e[%index1%],iv`irank') =Vecspvae[%index2%]e[%index1%]iv`irank';[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]
[%
@for particles %]
	Id SUBSCRIPT(k[%index%],iv`irank') = Veck[%index%]iv`irank';[%
   @if is_massive %]
	Id SUBSCRIPT(l[%index%],iv`irank') = Vecl[%index%]iv`irank';[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	Id SUBSCRIPT(e[%index%],iv`irank') = Vece[%index%]iv`irank';[%
   @end @for %][%
@end @if %]
	Id SUBSCRIPT(qshift,iv`irank') = Vecqshiftiv`irank';
#Do jrank=0,`RANK'
	Id d(iv`irank',iv`jrank') = dtensoriv`irank'iv`jrank';
#EndDo
#EndDo
#EndProcedure
#Procedure bracketninja
* The following code is contained in brackets
#Do vec={vecA,vecB,vecC}
[%
@for particles %],dpspk[% index %]`vec'[%
   @if is_massive %],dpspl[% index %]`vec'[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],dpspe[%index%]`vec'[%
   @end @for %][%
@end @if %][%
@for pairs distinct %],dpspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]`vec'[%
@end @for %][%
@if internal NUMPOLVEC %][%
@for pairs %][%
   @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],dpspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %]`vec',dpspvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%@end @if %]`vec'[%
   @end @for %][%
@for pairs distinct ordered %][%
   @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
            is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],dpspvae[%index1%]e[%index2%]`vec',spvae[%index2%]e[%index1%]`vec'[%
      @end @if %][%
   @end @for %][%
@end @if %],[%
@for particles %]
	dpk[%index%]`vec',[%
   @if is_massive %]
	dpl[%index%]`vec',[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	dpe[%index%]`vec',[%
   @end @for %][%
@end @if %]
	dp`vec'`vec',
   dpvecAvecB,
   dpvecAvecC,
   dpvecBvecC,
#EndDo
#EndProcedure
#procedure subscriptreplaceinvert(INRANK)
[% @if extension formopt %]
#do irank=0,`INRANK'[%
@for pairs distinct %]
	Id Vecspva[% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]iv`irank' = SUBSCRIPT(spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %],iv`irank');[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Vecspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %]iv`irank' = spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %];
   Id Vecspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]iv`irank'[%
      @end @if %] = SUBSCRIPT(spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %],iv`irank');[%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Vecspvae[%index1%]e[%index2%]iv`irank' = SUBSCRIPT(spvae[%index1%]e[%index2%],iv`irank'); 
   Id Vecspvae[%index2%]e[%index1%]iv`irank' = SUBSCRIPT(spvae[%index2%]e[%index1%],iv`irank');[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]
[%
@for particles %]
	Id Veck[%index%]iv`irank' = SUBSCRIPT(k[%index%],iv`irank');[%
   @if is_massive %]
	Id Vecl[%index%]iv`irank' = SUBSCRIPT(l[%index%],iv`irank');[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	Id Vece[%index%]iv`irank' = SUBSCRIPT(e[%index%],iv`irank');[%
   @end @for %][%
@end @if %]
	Id Vecqshiftiv`irank' = SUBSCRIPT(qshift,iv`irank');
#Do jrank=0,`RANK'
	Id dtensoriv`irank'iv`jrank' = d(iv`irank',iv`jrank');
#EndDo
#EndDo
#EndProcedure
#procedure qshiftdotreplace
[% @if extension formopt %]
AutoDeclare S dp;[%
@for pairs distinct %]
   Id dotproduct(spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %],qshift) = dpspva[% 
					@if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]qshift;[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dotproduct(spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %],qshift) = dpspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %]qshift;
   Id dotproduct(spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %],qshift)= dpspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]qshift;[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dotproduct(spvae[%index1%]e[%index2%],qshift) =dpspvae[%index1%]e[%index2%]qshift;
   Id dotproduct(spvae[%index2%]e[%index1%],qshift) =dpspvae[%index2%]e[%index1%]qshift;[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]
[%
@for particles %]
	Id dotproduct(k[%index%],qshift) = dpk[%index%]qshift;[%
   @if is_massive %]
	Id dotproduct(l[%index%],qshift) = dpl[%index%]qshift;[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	Id dotproduct(e[%index%],qshift) = dpe[%index%]qshift;[%
   @end @for %][%
@end @if %]
   Id dotproduct(qshift,qshift) = dpqshiftqshift;
#EndProcedure
#procedure qshiftdotreplaceinvert
[% @if extension formopt %][%
@for pairs distinct %]
   Id dpspva[% 
					@if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]qshift = dotproduct(spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %],qshift);[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dpspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %]qshift = dotproduct(spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %],qshift);
   Id dpspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]qshift = dotproduct(spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %],qshift);[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dpspvae[%index1%]e[%index2%]qshift = dotproduct(spvae[%index1%]e[%index2%],qshift);
   Id dpspvae[%index2%]e[%index1%]qshift = dotproduct(spvae[%index2%]e[%index1%],qshift);[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]
[%
@for particles %]
	Id dpk[%index%]qshift = dotproduct(k[%index%],qshift);[%
   @if is_massive %]
	Id dpl[%index%]qshift = dotproduct(l[%index%],qshift);[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	Id dpe[%index%]qshift = dotproduct(e[%index%],qshift);[%
   @end @for %][%
@end @if %]
   Id  dpqshiftqshift= dotproduct(qshift,qshift);

#EndProcedure
#procedure vecdotreplace
[% @if extension formopt %]
AutoDeclare S dp;
#Do vec={vecA,vecB,vecC}
[%
@for pairs distinct %]
   Id dotproduct(spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %],`vec') = dpspva[% 
					@if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]`vec';[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dotproduct(spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %],`vec') = dpspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %]`vec';
   Id dotproduct(spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %],`vec')= dpspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]`vec';[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dotproduct(spvae[%index1%]e[%index2%],`vec') =dpspvae[%index1%]e[%index2%]`vec';
   Id dotproduct(spvae[%index2%]e[%index1%],`vec') =dpspvae[%index2%]e[%index1%]`vec';[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]
[%
@for particles %]
	Id dotproduct(k[%index%],`vec') = dpk[%index%]`vec';[%
   @if is_massive %]
	Id dotproduct(l[%index%],`vec') = dpl[%index%]`vec';[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	Id dotproduct(e[%index%],`vec') = dpe[%index%]`vec';[%
   @end @for %][%
@end @if %]
#EndDo

#Do vec={vecA,vecB,vecC}
Id dotproduct(`vec',`vec') = dp`vec'`vec';
#EndDo
Id dotproduct(vecA,vecB) = dpvecAvecB;
Id dotproduct(vecA,vecC) = dpvecAvecC;
Id dotproduct(vecB,vecC) = dpvecBvecC;


#EndProcedure
#procedure vecdotreplaceinvert
[% @if extension formopt %]
#Do vec={vecA,vecB,vecC}[%
@for pairs distinct %]
   Id dpspva[% 
					@if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]`vec' = dotproduct(spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %],`vec');[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dpspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %]`vec' = dotproduct(spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %],`vec');
   Id dpspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]`vec' = dotproduct(spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %],`vec');[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id dpspvae[%index1%]e[%index2%]`vec' = dotproduct(spvae[%index1%]e[%index2%],`vec');
   Id dpspvae[%index2%]e[%index1%]`vec' = dotproduct(spvae[%index2%]e[%index1%],`vec');[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]
[%
@for particles %]
	Id dpk[%index%]`vec' = dotproduct(k[%index%],`vec');[%
   @if is_massive %]
	Id dpl[%index%]`vec' = dotproduct(l[%index%],`vec');[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	Id dpe[%index%]`vec' = dotproduct(e[%index%],`vec');[%
   @end @for %][%
@end @if %]
#EndDo

#Do vec={vecA,vecB,vecC}
Id dp`vec'`vec' = dotproduct(`vec',`vec');
#EndDo
Id dpvecAvecB = dotproduct(vecA,vecB);
Id dpvecAvecC = dotproduct(vecA,vecC);
Id dpvecBvecC = dotproduct(vecB,vecC);

#EndProcedure

