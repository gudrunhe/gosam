[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module [% process_name asprefix=\_ %]diagramscth[% helicity %]
   use [% process_name asprefix=\_ %]config, only: ki, &
   & debug_nlo_diagrams, logfile
   implicit none
   private

   public :: samplitudect

contains
!---#[ sum over counter term diagrams:
   function samplitudect(scale2)[%
@if generate_uv_counterterms %][%
      @for elements topolopy.keep.ct %]      
      use [% process_name asprefix=\_ %]d[% $_ %]h[% helicity 
     %]l1c, only: counterterm_[% $_ %] => counterterm[%
      @end @for elements %]
      implicit none
      real(ki), intent(in) :: scale2
      real(ki), dimension(3) :: samplitudect
      complex(ki), dimension(3) :: tot
      complex(ki), dimension(3) :: acc
      tot(:) = 0.0_ki
      samplitudect(:) = 0.0_ki[%
      @for elements topolopy.keep.ct %]
      acc(:) = counterterm_[% $_ %](scale2)
      tot(:) = acc(:) + tot(:)
      if (debug_nlo_diagrams) then 
         write(logfile,*) "<diagram index='[% $_ %]'>"
         write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
            & "<result kind='ct-finite' re='", real(acc(3), ki), &
            & "' im='", aimag(acc(3)), "'/>"
         write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
            & "<result kind='ct-single' re='", real(acc(2), ki), &
            & "' im='", aimag(acc(2)), "'/>"
         write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
            & "<result kind='ct-double' re='", real(acc(1), ki), &
            & "' im='", aimag(acc(1)), "'/>"
          write(logfile,*) "</diagram>"
      end if[%
      @end @for elements %]      
      samplitudect(:) = 2.0_ki*real(tot(:))[%
@end @if generate_uv_counterterms %]
   end function samplitudect
end module [% process_name asprefix=\_ %]diagramscth[% helicity %]
