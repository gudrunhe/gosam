
#procedure loopflow(DIAG)
   #switch `DIAG'[%

@for groups var=GRP %][%
   @for diagrams group=GRP var=DIAG %][%
      @for loop_flow DIAG %][%
         @if is_first %]
   #case [% DIAG %][%
         @end @if %]
      Id inplorentz(sDUMMY1?, iDUMMY1?, k[% index %], sDUMMY2?) = 
         inplorentz(-([% $_ %]), iDUMMY1, k[% index %], sDUMMY2);
      Id outlorentz(sDUMMY1?, iDUMMY1?, k[% index %], sDUMMY2?) = 
         outlorentz(+([% $_ %]), iDUMMY1, k[% index %], sDUMMY2);[%
         @if is_last %]
      #break[%
         @end @if %][%
      @end @for %][%
   @end @for %][%
@end @for %]
   #endswitch
#endprocedure

#procedure treeflow(DIAG)
   #switch `DIAG'[%

@for elements topolopy.keep.tree var=DIAG %][%
   @for tree_flow DIAG %][%
      @if is_first %]
   #case [% DIAG %][%
      @end @if %]
      Id inplorentz(sDUMMY1?, iDUMMY1?, k[% index %], sDUMMY2?) = 
         inplorentz(-([% $_ %]), iDUMMY1, k[% index %], sDUMMY2);
      Id outlorentz(sDUMMY1?, iDUMMY1?, k[% index %], sDUMMY2?) = 
         outlorentz(+([% $_ %]), iDUMMY1, k[% index %], sDUMMY2);[%
      @if is_last %]
      #break[%
      @end @if %][%
   @end @for %][%
@end @for %]
   #endswitch
#endprocedure
