%=$#-
#Create <`OUTPUT'>
#Write <`OUTPUT'> "module     [$ process_name asprefix=\_ $]version"
#Write <`OUTPUT'> "   implicit none"
#Write <`OUTPUT'> "   ! The version of Form used for code generation"
#Write <`OUTPUT'> "   integer, parameter, dimension(2) :: formversion %"
#Write <`OUTPUT'> "= (/`VERSION_', `SUBVERSION_'/)"[$
@if internal HAGGIES$]
#Write <`OUTPUT'> "   ! The version of haggies used for code generation"
#Write <`OUTPUT'> "   integer, parameter, dimension(2) :: haggiesversion %"
#Write <`OUTPUT'> "= (/[%%"
#Write <`OUTPUT'> "     program.version match=\"([0-9]*)\..*\" %"
#Write <`OUTPUT'> "format=\"%%s\" %%], [%%"
#Write <`OUTPUT'> "     program.version match=\"[0-9]*\.([0-9])\" %"
#Write <`OUTPUT'> "format=\"%%s\" %%]/)"
[$ @end @if $]
#Write <`OUTPUT'> "   ! The version of [$ golem.name
                         $] used for code generation"
#Write <`OUTPUT'> "   integer, parameter, dimension(2) :: gosamversion %"
#Write <`OUTPUT'> "= (/[$
@for elements golem.version delimiter=. $][$
   @select index
   @case 0 $][$ $_ $][$
   @case 1 $], [$ $_ $][$
   @end @select $][$
@end @for $]/)"
#Write <`OUTPUT'> "   ! The SVN revision of [$ golem.name
                         $] used for code generation"
#Write <`OUTPUT'> "   integer, parameter :: gosamrevision %"
#Write <`OUTPUT'> "= z\'[$ golem.revision $]\'"
#Write <`OUTPUT'> "end module [$ process_name asprefix=\_ $]version"
#Close <`OUTPUT'>
off statistics;
.end
