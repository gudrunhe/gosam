[% ' vim: ts=3:sw=3:expandtab:syntax=golem
%]module     [% process_name asprefix=\_ %]pjfry95pg
  ! Code by courtesy of Valery Yundin
  ! adapted to GoSam by T. Reiter 07/06/2011
  implicit none

  interface
    subroutine pginitgolem95(n)
      implicit none
      integer, intent(in) :: n
    end subroutine pginitgolem95
  end interface

  interface
    function pggetmusq()
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      real(ki_pjf) :: pggetmusq
    end function pggetmusq
  end interface

  interface
    subroutine pgsetmusq(musq)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      real(ki_pjf), intent(in) :: musq
    end subroutine pgsetmusq
  end interface

  interface
    subroutine pgsetmat(i, j, val)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j
      real(ki_pjf), intent(in) :: val
    end subroutine pgsetmat
  end interface

  interface
    function pggetmat(i, j)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j
      real(ki_pjf) :: pggetmat
    end function pggetmat
  end interface

  interface
    subroutine pgpreparesmatrix()
      implicit none
    end subroutine pgpreparesmatrix
  end interface

  interface
    function pga20(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pga20
    end function pga20
  end interface

  interface
    function pga21(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pga21
    end function pga21
  end interface

  interface
    function pga22(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pga22
    end function pga22
  end interface

  interface
    function pgb22(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pgb22
    end function pgb22
  end interface

  interface
    function pga30(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pga30
    end function pga30
  end interface

  interface
    function pga31(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pga31
    end function pga31
  end interface

  interface
    function pga32(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pga32
    end function pga32
  end interface

  interface
    function pgb32(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pgb32
    end function pgb32
  end interface

  interface
    function pga33(i, j, k, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, b_pin, ep
      complex(ki_pjf) :: pga33
    end function pga33
  end interface

  interface
    function pgb33(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pgb33
    end function pgb33
  end interface

  interface
    function pga40(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pga40
    end function pga40
  end interface

  interface
    function pga41(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pga41
    end function pga41
  end interface

  interface
    function pga42(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pga42
    end function pga42
  end interface

  interface
    function pgb42(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pgb42
    end function pgb42
  end interface

  interface
    function pga43(i, j, k, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, b_pin, ep
      complex(ki_pjf) :: pga43
    end function pga43
  end interface

  interface
    function pgb43(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pgb43
    end function pgb43
  end interface

  interface
    function pga44(i, j, k, l, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, l, b_pin, ep
      complex(ki_pjf) :: pga44
    end function pga44
  end interface

  interface
    function pgb44(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pgb44
    end function pgb44
  end interface

  interface
    function pgc44(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pgc44
    end function pgc44
  end interface

  interface
    function pga50(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pga50
    end function pga50
  end interface

  interface
    function pga51(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pga51
    end function pga51
  end interface

  interface
    function pga52(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pga52
    end function pga52
  end interface

  interface
    function pgb52(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pgb52
    end function pgb52
  end interface

  interface
    function pga53(i, j, k, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, b_pin, ep
      complex(ki_pjf) :: pga53
    end function pga53
  end interface

  interface
    function pgb53(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pgb53
    end function pgb53
  end interface

  interface
    function pga54(i, j, k, l, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, l, b_pin, ep
      complex(ki_pjf) :: pga54
    end function pga54
  end interface

  interface
    function pgb54(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pgb54
    end function pgb54
  end interface

  interface
    function pgc54(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pgc54
    end function pgc54
  end interface

  interface
    function pga55(i, j, k, l, m, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, l, m, b_pin, ep
      complex(ki_pjf) :: pga55
    end function pga55
  end interface

  interface
    function pgb55(i, j, k, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, b_pin, ep
      complex(ki_pjf) :: pgb55
    end function pgb55
  end interface

  interface
    function pgc55(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pgc55
    end function pgc55
  end interface

  interface
    function pga60(b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: b_pin, ep
      complex(ki_pjf) :: pga60
    end function pga60
  end interface

  interface
    function pga61(i, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, b_pin, ep
      complex(ki_pjf) :: pga61
    end function pga61
  end interface

  interface
    function pga62(i, j, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, b_pin, ep
      complex(ki_pjf) :: pga62
    end function pga62
  end interface

  interface
    function pga63(i, j, k, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, b_pin, ep
      complex(ki_pjf) :: pga63
    end function pga63
  end interface

  interface
    function pga64(i, j, k, l, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, l, b_pin, ep
      complex(ki_pjf) :: pga64
    end function pga64
  end interface

  interface
    function pga65(i, j, k, l, m, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, l, m, b_pin, ep
      complex(ki_pjf) :: pga65
    end function pga65
  end interface

  interface
    function pga66(i, j, k, l, m, n, b_pin, ep)
      use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
      implicit none
      integer, intent(in) :: i, j, k, l, m, n, b_pin, ep
      complex(ki_pjf) :: pga66
    end function pga66
  end interface

  contains

end module [% process_name asprefix=\_ %]pjfry95pg
  
