[% ' vim: ts=3:sw=3:expandtab:syntax=golem
   '%]#Procedure    shiftmomenta(DIAG)
* vim: ts=3:sw=3:expandtab:syntax=form
   #Switch `DIAG'[%
@for groups var=grp %]
*---#[ Diagram Group [%grp%]:[%
  @for diagrams group=grp %]
  #Case [% $_ %]
     Id p1 = [% sign %] Q - ([% shift %]);
     #Break[%
  @end @for diagrams %]
*---#] Diagram Group [%grp%]:[%
@end @for groups %]
   #Default
      #Message No Such Loop Diagram: `DIAG'
      #Terminate 1
   #EndSwitch
#EndProcedure
