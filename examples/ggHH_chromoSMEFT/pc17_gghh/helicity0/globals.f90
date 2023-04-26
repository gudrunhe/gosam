module     pc17_gghh_globalsh0
   use pc17_gghh_config, only: ki
   use pc17_gghh_color, only:&
      & c1v => c1

   implicit none
   private
   complex(ki), public :: c1

   public :: init_lo

   complex(ki), public :: rat2
contains

subroutine     init_lo()
   use pc17_gghh_globalsl1, only: epspow, ccontract, amp0
   implicit none
   c1 = ccontract(c1v, amp0)
end subroutine init_lo

end module pc17_gghh_globalsh0
