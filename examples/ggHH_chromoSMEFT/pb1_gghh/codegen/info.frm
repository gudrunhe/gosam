#-
#Create <`OUTPUT'>
#Write <`OUTPUT'> "module     pb1_gghh_version"
#Write <`OUTPUT'> "   implicit none"
#Write <`OUTPUT'> "   ! The version of Form used for code generation"
#Write <`OUTPUT'> "   integer, parameter, dimension(2) :: formversion %"
#Write <`OUTPUT'> "= (/`VERSION_', `SUBVERSION_'/)"
#Write <`OUTPUT'> "   ! The version of GoSam used for code generation"
#Write <`OUTPUT'> "   integer, parameter, dimension(2) :: gosamversion %"
#Write <`OUTPUT'> "= (/2, 1/)"
#Write <`OUTPUT'> "   ! The SVN revision of GoSam used for code generation"
#Write <`OUTPUT'> "   integer, parameter :: gosamrevision %"
#Write <`OUTPUT'> "= int(z\'39c7ae2\')"
#Write <`OUTPUT'> "end module pb1_gghh_version"
#Close <`OUTPUT'>
off statistics;
.end
