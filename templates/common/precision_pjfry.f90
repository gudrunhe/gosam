[% ' vim: ts=3:sw=3:expandtab:syntax=golem
%]module     [% process_name asprefix=\_ %]precision_pjfry
   implicit none
   private

   integer, parameter, public :: ki_pjf = kind(1.0d0)

end module [% process_name asprefix=\_ %]precision_pjfry
