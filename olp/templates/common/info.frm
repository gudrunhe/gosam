%=$#-
#Create <`OUTPUT'>
#Write <`OUTPUT'> "module     version"
#Write <`OUTPUT'> "   implicit none"
#Write <`OUTPUT'> "   ! The version of Form used for code generation"
#Write <`OUTPUT'> "   integer, parameter, dimension(2) :: formversion %"
#Write <`OUTPUT'> "= (/`VERSION_', `SUBVERSION_'/)"
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
#Write <`OUTPUT'> "= int(z\'[$ golem.revision $]\')"
#Write <`OUTPUT'> "end module version"
#Close <`OUTPUT'>
off statistics;
.end
