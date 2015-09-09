[% ' vim: ts=3:sw=3:expandtab:syntax=golem
   '%]#Procedure    shiftmomenta(DIAG,WRAP)
* vim: ts=3:sw=3:expandtab:syntax=form
   #Switch `DIAG'[%
@for groups var=grp %]
*---#[ Diagram Group [%grp%]:[%
  @for diagrams group=grp %]
  #Case [% $_ %]
     #If `WRAP'
        Multiply replace_( p1 , [% sign %] Q - qshift * fshift([% shift %]) );
     #Else
        Multiply replace_( p1 , [% sign %] Q - ([% shift %]) );
     #EndIf
     #Break[%
  @end @for diagrams %]
*---#] Diagram Group [%grp%]:[%
@end @for groups %]
   #Default
      #Message No Such Loop Diagram: `DIAG'
      #Terminate 1
   #EndSwitch
#EndProcedure
