[% ' vim: syntax=golem
%]* vim[%
   ' %]: syntax=form:expandtab:ts=3:sw=3
CFunctions out, outlorentz, outcolor;
CFunctions inp, inplorentz, inpcolor;
CFunctions proplorentz, propcolor;
CFunction vertex;
CFunction abbr;
CTensor SplitLorentzIndex;
CFunction SCREEN;
Function NCSIGN(antisymmetric);
CFunction csqrt;

* Used in the output to keep eps and form factors together
CFunction mulfirst;

CTensors f(antisymmetric), f4, T;

CFunctions C(symmetric), CL(symmetric), CR(symmetric);

CFunctions inv, PREFACTOR, COLORFACTOR, delta(symmetric);
CFunction customSpin2Prop;
CFunction QGRAFSIGN;
CTensor SUBSCRIPT;
NFunction NCOrder;

* formfactor(A, B) = A + B/eps
CFunction formfactor, log;

Symbols field1, ..., field5;
Symbols m, TR, NC, NA, eps(-2:2), sign1, ..., sign4;
Symbol sqrt2, Sqrt2, sqrt3, Sqrt3, scale2;
Symbol deltaaxial, deltaOS, deltaHV;

Vector ZERO, vDUMMYA;

#If `LOOPS' >= 1
   CFunction j;
   CTensor ptens;
   Vector Q
   #Do i = 1, `LOOPS'
        ,p`i'
   #EndDo
   ;
   Vector qshift;
   CFunction fshift;
#EndIf
[%
@if extension formopt %]
CF dotproduct;
[% @end @if %]
[%
@if genUV %]
#If `LOOPS' == ct
   Vector  p1;
   CFunction deltaM, deltaZ;
   Symbols epspole1, epsfin;
#EndIf[%
@end @if %]

*---#[ Process dependent symbol definitions:
#Define LEGS "[% num_legs %]"
* Flag: Rewrite gauge boson legs as eps(k) -> eps(k) + gaugeXz * k
#Define GAUGEVAR "[%
@if internal GAUGE_CHECK %]1[%
@else %]0[%
@end @if %]"
#Define EXTERNAL "[%
@for particles %][%
   @if is_first %][%
   @else %],[%
   @end @if %]k[%index%][%

   @if is_massive %],l[%index%][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],e[%index%][%
   @end @for %][%
@end @if %]"
#Define LIGHTLIKE "[%
@for particles %][%
   @if is_first %][%
   @else %],[%
   @end @if %][%

   @if is_massive %]l[%index%][%
   @else %]k[%index%][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],e[%index%][%
   @end @for %][%
@end @if %]"
#Define FERMIONS "[%
@for particles fermion %][%
   @if is_first %][%
   @else %],[%
   @end @if %][%index%][%
@end @for %]"
*------#[ symbols for color:
#Define NUMCS "[% num_colors %]"
#Define INCOLORS "[%
@for particles initial colored %][%
   @if is_first %][%
   @else %],[%
   @end @if %][%
   @select color
   @case -3 3 %]NC[%
   @case -8 8 %]NA[%
   @end @select %][%
@end @for %]"
#Define COLORED "[%
@for particles colored %][%
   @if is_first %][%
   @else %],[%
   @end @if %][% index %][%
@end @for %]"
#Define INIFUNDAMENTAL "[%
@for particles initial anti-quarks %][%
   @if is_first %][%
   @else %],[%
   @end @if %][% index %][%
@end @for %]"
#Define FINFUNDAMENTAL "[%
@for particles final anti-quarks %][%
   @if is_first %][%
   @else %],[%
   @end @if %][% out_index %][%
@end @for %]"[%
@if eval num_colors .gt. 0 %]
Symbols c1, ..., c[% num_colors %];[%
@end @if %]
*------#] symbols for color:
[%
@for mandelstam sym_prefix=es non-zero%]
Symbol [%symbol%];[%
@end @for mandelstam non-zero%][%
@for mandelstam sym_prefix=es zero%][%
   @if is_first %]
Symbol [%
   @else %], [%
   @end @if %][%symbol%][%
@end @for mandelstam zero%][%
@for mandelstam sym_prefix=es zero%][%
   @if is_first %];[%
   @end @if %][%
@end @for mandelstam zero%][%
@for pairs ordered distinct %]
Symbols spa[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
      %], spb[% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %][%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
@end @for pairs ordered distinct %][%
@for particles %][%
   @if is_first %]
Vectors [%
   @else %], [%
   @end @if %]k[%index%][%
   @if is_lightlike%][% @else %], l[%index%][%
   @end @if %][%
@end @for particles %][%
@for particles %][%
   @if is_first %];[%
   @end @if %][%
@end @for %][%
@for particles %][%
   @if is_first %]
#If `LOOPS' == 1
   Vectors [%
   @else %], [%
   @end @if %]r[%index%][%
@end @for particles %][%
@for particles %][%
   @if is_first %];
#EndIf[%
   @end @if %][%
@end @for %]
#If `GAUGEVAR'[%
@for particles %][%
   @select 2spin
   @case -2 2 %]
   Symbol gauge[% index %]z;[%
   @end @select %][%
@end @for particles %]
#EndIf[%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
Vector e[% index %];[%
   @end @for %][%
   @for pairs ordered %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
Symbols spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2
            %], spbe[% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
      @end @if %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) %]
Symbols spae[%index1%][%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %], spb[%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]e[%
            index1 %];[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
Symbols spae[% index1
            %]e[% index2 %], spbe[% index2 %]e[% index1 %];[%
      @end @if %][%
   @end @for %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
Vectors spva[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %], spvae[% index2 %][% 
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
Vectors spvae[% index1
            %]e[% index2 %], spvae[% index2 %]e[% index1 %];[%
      @end @if %][%
   @end @for %][%
@end @if %]
*---#] Process dependent symbol definitions:

AutoDeclare Indices idx, iv;
AutoDeclare CFunctions Lor;

*---#[ Process dependent procedures:
*------#[ procedure zeroes:
#Procedure zeroes[%
@for zeroes %]
   Multiply replace_([% $_ %], 0);[%
@end @for %]
#EndProcedure
*------#] procedure zeroes:
*------#[ procedure ones:
#Procedure ones[%
@for ones %]
   Multiply replace_([% $_ %], 1);[%
@end @for %]
#EndProcedure
*------#] procedure ones:
*------#[ procedure spsymbols:
#Procedure spsymbols[%
@for pairs ordered distinct %]
   Id Spa2([%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %], [% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]) = spa[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
      %];
   Id Spb2([% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %], [%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]) = spb[% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %][%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) %]
   Id Spa2(e[%index1%], [%
         @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]) = spae[%
      index1 %][%
         @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %];

   Id Spb2([%
         @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %], e[%
               index1 %]) = spb[%
         @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]e[%
               index1%];[%
      @end @if %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Spa2([%
         @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %], e[%
           index2%]) = spa[%
         @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]e[%
                index2%];

   Id Spb2(e[%index2%], [%
         @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]) = spbe[%
             index2 %][%
         @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
      @end @if %][%
   @end @for pairs ordered %][%
   @for pairs ordered distinct %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Spa2(e[% index1 %], e[% index2 %]) = spae[% index1 %]e[% index2 %];
   Id Spb2(e[% index2 %], e[% index1 %]) = spbe[% index2 %]e[% index1 %];[%
      @end @if %][%
   @end @for pairs ordered distinct %][%
@end @if %]
#EndProcedure
*------#] procedure spsymbols:
*------#[ procedure enforceconservation:
#Procedure enforceconservation
    Multiply replace_(k[% num_legs %],[%
@if eval num_legs .gt. num_in %][%
@for particles initial %][%
   @if eval index .lt. num_legs %] + k[%index%][%
   @end @if %][%
@end @for %][%
@for particles final %][%
   @if eval index .lt. num_legs %] - k[%index%][%
   @end @if %][%
@end @for %]);[%
@else %] -([%
@for particles initial %][%
   @if eval index .lt. num_legs %] + k[%index%][%
   @end @if %][%
@end @for %][%
@for particles final %][%
   @if eval index .lt. num_legs %] - k[%index%][%
   @end @if %][%
@end @for %]));[%
@end @if %]           
   .Sort
#EndProcedure
*------#] procedure enforceconservation:
*------#[ procedure conservation:
#Procedure conservation
   Id k[% num_legs %] =[%
@if eval num_legs .gt. num_in %][%
@for particles initial %][%
   @if eval index .lt. num_legs %] + k[%index%][%
   @end @if %][%
@end @for %][%
@for particles final %][%
   @if eval index .lt. num_legs %] - k[%index%][%
   @end @if %][%
@end @for %];[%
@else %] -([%
@for particles initial %][%
   @if eval index .lt. num_legs %] + k[%index%][%
   @end @if %][%
@end @for %][%
@for particles final %][%
   @if eval index .lt. num_legs %] - k[%index%][%
   @end @if %][%
@end @for %]);[%
@end @if %]
#EndProcedure
*------#] procedure conservation:
*------#[ procedure rewritelegs:
#Procedure rewritelegs[%
@for particles %][%
   @select 2spin
   @case -1 1 %]
   Id [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1?, k[%index%]) = [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1, k[%index%], `HEL[%
      @if is_initial %]i[%index%][%
      @else %]o[%out_index%][%
      @end @if %]');[%
   @case -2 2 %]
   Id [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1?, k[%index%]) = [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1, k[%index%], `HEL[%
      @if is_initial %]i[%index%][%
      @else %]o[%out_index%][%
      @end @if %]'[%
      @if is_massive %], l[%index%][%
      @else %][%
      @end @if %], `REFk[%index%]');
   #If `GAUGEVAR'
      Id [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %]lorentz([%2spin%], idx[%index%]L2?, k[%index%], [%mass%]) = [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %]lorentz([%2spin%], idx[%index%]L2, k[%index%], [%mass%])
         + gauge[%index%]z * k[%index%](idx[%index%]L2);
   #EndIf[%
   @case -3 3 %]
   Id [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1?, k[%index%]) = [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1, k[%index%], `HEL[%
      @if is_initial %]i[%index%][%
      @else %]o[%out_index%][%
      @end @if %]'[%
      @if is_massive %], l[%index%][%
      @else %][%
      @end @if %], `REFk[%index%]');[%
   @case -4 4 %]
   Id [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1?, k[%index%]) = [%
      @if is_initial %]inp[%
      @else %]out[%
      @end @if %](field1, k[%index%], `HEL[%
      @if is_initial %]i[%index%][%
      @else %]o[%out_index%][%
      @end @if %]'[%
      @if is_massive %], l[%index%][%
      @else %][%
      @end @if %], `REFk[%index%]');[%
   @end @select %][%
@end @for %]
#EndProcedure
*------#] procedure rewritelegs:
*------#[ procedure kinematics:
#Procedure kinematics[%
@for mandelstam_subs diagonal upper %]
   Id k[% index1 %].k[% index2 %] =[%
   @for mandelstam_subs_rhs %][%
      @select coeff
      @case -1 %] - 1/2 * [%
      @case 1 %][%
         @if is_first %][%
         @else %] +[%
         @end @if %] 1/2 * [%
      @case -2 %] - [%
      @case 2 %][%
         @if is_first %] [%
         @else %] + [%
         @end @if %][%
      @else %][%
         @if eval coeff .gt. 0 %][%
            @if is_first %] [%
            @else %] +[%
            @end @if %] [%coeff%] * [%
         @else %] - [%eval .abs. coeff%]/2 * [%
         @end @if %][%
      @end @select %][%$_%][%
      @if eval exponent .gt. 1 %]^[%exponent%][%
      @end @if %][%
   @end @for %];[%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
   Id k[%index%].e[%index%]=;[%
   @end @for %][%
   @for particles lightlike vector %][%
     @if is_massive %][%
     @else %]
   Id e[%index%].[%
       @if eval reference > 0 %]k[%reference %]=;[%
       @else %][% eval - reference %][%
       @end @if %][%
     @end @if %][% 
   @end @for %][%
@end @if %]
#EndProcedure
*------#] procedure kinematics:
*------#[ procedure colorbasis:
#Procedure colorbasis[%
@for color_basis index_shift=1 shift=1%]
   Id[%
   @for color_wf shift=1 %][%
      @if eval index .le. num_in %]
      inpcolor([%index%], idx[%io%][% lindex %]C[% rep %]?)[%
      @else %]
      outcolor([%eval index - num_in %], idx[%io%][% lindex %]C[% rep %]?)[%
      @end @if %][%
      @if is_last %][%
      @else %] *[%
      @end @if %][%
   @end @for %][%
   @for color_lines %][%
      @for color_line_elements %] *
      T(idx[%io%][%lindex%]C[%rep%]?, [%
         @if is_first %]idx[%first_io%][%first_lidx%]C[%first_rep%][%
         @else %]idx[%prev%]C3l[%
         @end @if %]?, [%
         @if is_last %]idx[%last_io%][%last_lidx%]C[%last_rep%][%
         @else %]idx[%index%]C3l[%
         @end @if %]?)[%
      @end @for %][%
   @end @for %][%
   @for color_traces %][%
      @for color_trace_elements %] *
      T(idx[%io%][%lindex%]C[%rep%]?, idx[%prev%]C3t?, idx[%index%]C3t?)[%
      @end @for %][%
   @end @for %] = c[% index %];[%
@end @for %]
#EndProcedure
*------#] procedure colorbasis:
*------#[ procedure invcolorbasis:
#Procedure invcolorbasis(suffix,num)[%
@for color_basis index_shift=1 shift=1%]
   #If `num' == 1
      Id c([%index%], m?) = c([%index%], m) * ([%
   @for color_wf shift=1 %][%
      @if eval index .le. num_in %]
         inpcolor([%index%], idx[%io%][% lindex %]C[% rep %]`suffix', `num')[%
      @else %]
         outcolor([%eval index - num_in %], idx[%io%][% lindex %]C[% rep 
            %]`suffix', `num')[%
      @end @if %][%
      @if is_last %][%
      @else %] *[%
      @end @if %][%
   @end @for %][%
   @for color_lines %][%
      @for color_line_elements %] *
         T(idx[%io%][%lindex%]C[%rep%]`suffix', [%
         @if is_first %]idx[%first_io%][%first_lidx%]C[%first_rep%][%
         @else %]idx[%prev%]C3l[%
         @end @if %]`suffix', [%
         @if is_last %]idx[%last_io%][%last_lidx%]C[%last_rep%][%
         @else %]idx[%index%]C3l[%
         @end @if %]`suffix')[%
      @end @for %][%
   @end @for %][%
   @for color_traces %][%
      @for color_trace_elements %] *
         T(idx[%io%][%lindex%]C[%rep%]`suffix', idx[%prev
               %]C3t`suffix', idx[%index%]C3t`suffix')[%
      @end @for %][%
   @end @for %]);
   #Else
      Id c(m?, [%index%]) = c(m, [%index%]) * ([%
   @for color_wf shift=1 %][%
      @if eval index .le. num_in %]
         inpcolor([%index%], idx[%io%][% lindex %]C[% rep %]`suffix', `num')[%
      @else %]
         outcolor([%eval index - num_in %], idx[%io%][% lindex %]C[% rep 
            %]`suffix', `num')[%
      @end @if %][%
      @if is_last %][%
      @else %] *[%
      @end @if %][%
   @end @for %][%
   @for color_lines %][%
      @for color_line_elements %] *
         T(idx[%io%][%lindex%]C[%rep%]`suffix', [%
         @if is_last %]idx[%last_io%][%last_lidx%]C[%last_rep%][%
         @else %]idx[%index%]C3l[%
         @end @if %]`suffix', [%
         @if is_first %]idx[%first_io%][%first_lidx%]C[%first_rep%][%
         @else %]idx[%prev%]C3l[%
         @end @if %]`suffix')[%
      @end @for %][%
   @end @for %][%
   @for color_traces %][%
      @for color_trace_elements %] *
         T(idx[%io%][%lindex%]C[%rep%]`suffix', idx[%index
              %]C3t`suffix', idx[%prev%]C3t`suffix')[%
      @end @for %][%
   @end @for %]);
   #EndIf[%
@end @for %]
#EndProcedure
*------#] procedure invcolorbasis:
*------#[ procedure colorinsertion:
#Procedure colorinsertion[%
@for particles initial %]
*---------#[ particle [%index%]:
   Id propcolor([%index%], [%index%]) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]a?, 1) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]b?, 2) =[%
   @select color
   @case -3 3 %]
      TR * (NC - 1/NC) * delta(idxi[%index%]C3a, idxi[%index%]C3b);[%
   @case -8 8 %]
      NC * d_(idxi[%index%]C8a, idxi[%index%]C8b);[%
   @else %]
      1;[%
   @end @select %]
   Id propcolor([%index%], m?) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]a?, 1) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]b?, 2) =[%
   @select color
   @case 3 %]
      T(idxIns, idxi[%index%]C3a, idxi[%index%]C3b) * propcolor([%
          index%], m);[%
   @case -3 %]
      - T(idxIns, idxi[%index%]C3b, idxi[%index%]C3a) * propcolor([%
          index%], m);[%
   @case -8 8 %]
      -i_ * f(idxIns, idxi[%index%]C8a, idxi[%index%]C8b) * propcolor([%
          index%], m);[%
   @else %]
      0;[%
   @end @select %]
   Id propcolor(m?, [%index%]) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]a?, 1) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]b?, 2) =[%
   @select color
   @case 3 %]
      T(idxIns, idxi[%index%]C3a, idxi[%index%]C3b) * propcolor(m, [%
           index%]);[%
   @case -3 %]
      - T(idxIns, idxi[%index%]C3b, idxi[%index%]C3a) * propcolor(m, [%
           index%]);[%
   @case -8 8 %]
      -i_ * f(idxIns, idxi[%index%]C8a, idxi[%index%]C8b) * propcolor(m, [%
           index%]);[%
   @else %]
      0;[%
   @end @select %]
   Id 
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]a?, 1) *
         inpcolor([%index%], idxi[%index%]C[%eval .abs. color%]b?, 2) =[%
   @select color
   @case -3 3 %]
      delta(idxi[%index%]C3a, idxi[%index%]C3b);[%
   @case -8 8 %]
      d_(idxi[%index%]C8a, idxi[%index%]C8b);[%
   @else %]
      1;[%
   @end @select %]
*---------#] particle [%index%]:[%
@end @for %][%
@for particles final %]
*---------#[ particle [%index%]:
   Id propcolor([%index%], [%index%]) *
         outcolor([%out_index%], idxo[%out_index%]C[%eval .abs. color%]a?, 1) *
         outcolor([%out_index%], idxo[%out_index%]C[%eval .abs. color%]b?, 2) =[%
   @select color
   @case -3 3 %]
      TR * (NC - 1/NC) * delta(idxo[%out_index%]C3a, idxo[%out_index%]C3b);[%
   @case -8 8 %]
      NC * d_(idxo[%out_index%]C8a, idxo[%out_index%]C8b);[%
   @else %]
      1;[%
   @end @select %]
   Id propcolor([%index%], m?) *
         outcolor([%out_index%], idxo[%out_index%]C[%
             eval .abs. color%]a?, 1) *
         outcolor([%out_index%], idxo[%out_index%]C[%
             eval .abs. color%]b?, 2) =[%
   @select color
   @case 3 %]
      T(idxIns, idxo[%out_index%]C3a, idxo[%out_index%]C3b) * propcolor([%
           index%], m);[%
   @case -3 %]
      - T(idxIns, idxo[%out_index%]C3b, idxo[%out_index%]C3a) * propcolor([%
           index%], m);[%
   @case -8 8 %]
      -i_ * f(idxIns, idxo[%out_index%]C8a, idxo[%out_index%]C8b) * propcolor([%
           index%], m);[%
   @else %]
      0;[%
   @end @select %]
   Id propcolor(m?, [%index%]) *
         outcolor([%out_index%], idxo[%out_index%]C[%
             eval .abs. color%]a?, 1) *
         outcolor([%out_index%], idxo[%out_index%]C[%
             eval .abs. color%]b?, 2) =[%
   @select color
   @case 3 %]
      T(idxIns, idxo[%out_index%]C3a, idxo[%out_index%]C3b) * propcolor(m, [%
           index%]);[%
   @case -3 %]
      - T(idxIns, idxo[%out_index%]C3b, idxo[%out_index%]C3a) * propcolor(m, [%
           index%]);[%
   @case -8 8 %]
      -i_ * f(idxIns, idxo[%out_index%]C8a, idxo[%
          out_index%]C8b) * propcolor(m, [% out_index%]);[%
   @else %]
      0;[%
   @end @select %]
   Id 
         outcolor([%out_index%], idxo[%out_index%]C[%
             eval .abs. color%]a?, 1) *
         outcolor([%out_index%], idxo[%out_index%]C[%
             eval .abs. color%]b?, 2) =[%
   @select color
   @case -3 3 %]
      delta(idxo[%out_index%]C3a, idxo[%out_index%]C3b);[%
   @case -8 8 %]
      d_(idxo[%out_index%]C8a, idxo[%out_index%]C8b);[%
   @else %]
      1;[%
   @end @select %]
*---------#] particle [%index%]:[%
@end @for %]
#EndProcedure
*------#] procedure colorinsertion:
*---#] Process dependent procedures:
