[%' vim: sw=3:syntax=golem

'%]module     [% process_name asprefix=\_ %]scalar_cache[%
@if extension samurai %]
   use precision, only: ki_sam => ki[%
   @if version_newer samurai.version 2.8 %]
   use constants[% @else %]
   use madds[% @end @if %][%
@end @if %]
   implicit none
   save

   private[%
@if extension samurai %][%
   @if version_newer samurai.version 2.0 %]
!---#[ scalar integral cache for samurai:[%
      @for groups var=grp %]
    logical, public  :: samurai_cache_flag_g[% grp %]
    complex(ki_sam), dimension(-2:0,cachedim[%
              loopsize group=grp %](1)), public :: samurai_cache_g[% grp %][%
         @for diagrams group=grp var=DIAG %]
    logical, public :: samurai_cache_flag_d[% DIAG %]
    complex(ki_sam), dimension(-2:0,cachedim[%
              loopsize diagram=DIAG %](1)), public :: samurai_cache_d[%
                        DIAG %][%
         @end @for %][%
      @end @for %]
!---#] scalar integral cache for samurai:[%
   @end @if version.samurai %][%
@end @if extension samurai %]

   public :: invalidate_cache
contains
   subroutine invalidate_cache()
      implicit none[%
@if extension samurai %][%
   @if version_newer samurai.version 2.0 %][%
      @for groups var=grp %]
      samurai_cache_flag_g[% grp %] = .false.[%
         @for diagrams group=grp var=DIAG %]
      samurai_cache_flag_d[% DIAG %] = .false.[%
         @end @for %][%
      @end @for %][%
   @end @if version.samurai %][%
@end @if extension samurai %]
   end subroutine invalidate_cache
end module [% process_name asprefix=\_ %]scalar_cache[%
