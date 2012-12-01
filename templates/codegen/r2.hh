[% ' vim:ts=3:sw=3:expandtab:syntax=golem
   '
   '
   '
   '
   '
   '
   '
   '
   ' %]* vim: ts=3:sw=3:expandtab:syntax=form

#define R2PREFACTOR "1"

#procedure ReduceDiagramR2(DIAG)
   #call shiftmomenta(`DIAG',0)
   Argument Spab, Spaa, Spbb, Spba;
      #Call shiftmomenta(`DIAG',0)
   EndArgument;
   Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(vDUMMY1?, iDUMMY2?, vDUMMY3?) = 
      fDUMMY1(vDUMMY1, iDUMMY2, vDUMMY3);
   ToTensor Functions, Q, ptens;
   If(count(ptens,1)==0) Multiply ptens;

   #switch `DIAG'[%
@for groups var=grp %]
*---#[ Diagram group [%grp%]:[%
   @for diagrams group=grp var=diag %]
   #case [%diag%][%
   @end @for diagrams %][%
   @for propagators group=grp %]
      #define r[%$_%] "[%momentum%]"
      #define m[%$_%]sq "([%mass%])^2-i_*([%width%]*[%mass%])"[%
   @end @for propagators %]
      #break
*---#] Diagram group [%grp%]:[%
@end @for groups %]
   #endswitch
   #switch `DIAG'[%
@for groups var=grp %]
*---#[ Diagram group [%grp%]:[%
   @for diagrams group=grp var=diag idxshift=1 %]
*------#[ Diagram [%diag%]:
   #case [%diag%][%
      @select loopsize diagram=diag
      @case 1 2 3 %]
      #call ReduceR2N[%loopsize diagram=diag%]([%
         @for elements indices %][%
            @if is_first %][% @else %],[%
            @end @if %]`r[%$_%]',`m[%$_%]sq'[%
         @end @for %])[%
      @case 4 %]
      #call ReduceR2N[%loopsize diagram=diag%]([%
         @for elements indices %][%
            @if is_first %][% @else %],[%
            @end @if %]`r[%$_%]'[%
         @end @for %])[%
      @case 5 %]
      #call ReduceR2N[%loopsize diagram=diag%][%
      @end @select %][%
      @if diagsum %][%
      @else %][%
      @select diagram_sign
      @case + %][%
         @if is_nf %]
      #redefine R2PREFACTOR "Nfrat"[%
         @end @if %][%
      @case - %]
      #redefine R2PREFACTOR "-[%
         @if is_nf %]Nfrat[%
         @else %]1[%
         @end @if %]"[%
      @end @select %][%
      @end @if %]
      #break
*------#] Diagram [%diag%]:[%
   @end @for diagrams %]
*---#] Diagram group [%grp%]:[%
@end @for groups %]
   #endswitch

   Id Qt2 = 0;
   Id eps = 0;

   Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(vDUMMY1?, 0, vDUMMY3?) = 0;
   #call SpContractMetrics
   #call SpContract
   #call SpOpen(`LIGHTLIKE')
#endprocedure
