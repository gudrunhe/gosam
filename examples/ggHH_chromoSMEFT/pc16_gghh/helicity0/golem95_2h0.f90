module     pc16_gghh_golem95_2h0
   use precision_golem, only: ki_gol => ki
   use pc16_gghh_config, only: ki
   implicit none
   private
   interface reconstruct_group
      module procedure reconstruct_group0
      module procedure reconstruct_group1
      module procedure reconstruct_group2
   end interface

   public :: reconstruct_group
contains
!---#[ subroutine reconstruct_group0:
subroutine     reconstruct_group0(coeffs)
   use tens_rec
   use pc16_gghh_config
   use pc16_gghh_groups, only: tensrec_info_group0
   use pc16_gghh_d33_2h0l1, only: numerator_d33 => numerator_golem95
   use pc16_gghh_d33_2h0l1d, only: reconstruct_d33
   implicit none
   type(tensrec_info_group0), intent(out) :: coeffs
   !------#[ Diagram 33:
      if (tens_rec_by_derivatives) then
         call reconstruct_d33(coeffs)
      else
         call reconstruct6(numerator_d33, coeffs%coeffs_33)
      end if
   !------#] Diagram 33:
end subroutine reconstruct_group0
!---#] subroutine reconstruct_group0:
!---#[ subroutine reconstruct_group1:
subroutine     reconstruct_group1(coeffs)
   use tens_rec
   use pc16_gghh_config
   use pc16_gghh_groups, only: tensrec_info_group1
   use pc16_gghh_d5_2h0l1, only: numerator_d5 => numerator_golem95
   use pc16_gghh_d5_2h0l1d, only: reconstruct_d5
   use pc16_gghh_d12_2h0l1, only: numerator_d12 => numerator_golem95
   use pc16_gghh_d12_2h0l1d, only: reconstruct_d12
   use pc16_gghh_d14_2h0l1, only: numerator_d14 => numerator_golem95
   use pc16_gghh_d14_2h0l1d, only: reconstruct_d14
   use pc16_gghh_d31_2h0l1, only: numerator_d31 => numerator_golem95
   use pc16_gghh_d31_2h0l1d, only: reconstruct_d31
   implicit none
   type(tensrec_info_group1), intent(out) :: coeffs
   !------#[ Diagram 5:
      if (tens_rec_by_derivatives) then
         call reconstruct_d5(coeffs)
      else
         call reconstruct4(numerator_d5, coeffs%coeffs_5)
      end if
   !------#] Diagram 5:
   !------#[ Diagram 12:
      if (tens_rec_by_derivatives) then
         call reconstruct_d12(coeffs)
      else
         call reconstruct5(numerator_d12, coeffs%coeffs_12)
      end if
   !------#] Diagram 12:
   !------#[ Diagram 14:
      if (tens_rec_by_derivatives) then
         call reconstruct_d14(coeffs)
      else
         call reconstruct5(numerator_d14, coeffs%coeffs_14)
      end if
   !------#] Diagram 14:
   !------#[ Diagram 31:
      if (tens_rec_by_derivatives) then
         call reconstruct_d31(coeffs)
      else
         call reconstruct6(numerator_d31, coeffs%coeffs_31)
      end if
   !------#] Diagram 31:
end subroutine reconstruct_group1
!---#] subroutine reconstruct_group1:
!---#[ subroutine reconstruct_group2:
subroutine     reconstruct_group2(coeffs)
   use tens_rec
   use pc16_gghh_config
   use pc16_gghh_groups, only: tensrec_info_group2
   use pc16_gghh_d1_2h0l1, only: numerator_d1 => numerator_golem95
   use pc16_gghh_d1_2h0l1d, only: reconstruct_d1
   use pc16_gghh_d2_2h0l1, only: numerator_d2 => numerator_golem95
   use pc16_gghh_d2_2h0l1d, only: reconstruct_d2
   use pc16_gghh_d3_2h0l1, only: numerator_d3 => numerator_golem95
   use pc16_gghh_d3_2h0l1d, only: reconstruct_d3
   use pc16_gghh_d4_2h0l1, only: numerator_d4 => numerator_golem95
   use pc16_gghh_d4_2h0l1d, only: reconstruct_d4
   use pc16_gghh_d7_2h0l1, only: numerator_d7 => numerator_golem95
   use pc16_gghh_d7_2h0l1d, only: reconstruct_d7
   use pc16_gghh_d8_2h0l1, only: numerator_d8 => numerator_golem95
   use pc16_gghh_d8_2h0l1d, only: reconstruct_d8
   use pc16_gghh_d10_2h0l1, only: numerator_d10 => numerator_golem95
   use pc16_gghh_d10_2h0l1d, only: reconstruct_d10
   use pc16_gghh_d16_2h0l1, only: numerator_d16 => numerator_golem95
   use pc16_gghh_d16_2h0l1d, only: reconstruct_d16
   use pc16_gghh_d18_2h0l1, only: numerator_d18 => numerator_golem95
   use pc16_gghh_d18_2h0l1d, only: reconstruct_d18
   use pc16_gghh_d22_2h0l1, only: numerator_d22 => numerator_golem95
   use pc16_gghh_d22_2h0l1d, only: reconstruct_d22
   use pc16_gghh_d23_2h0l1, only: numerator_d23 => numerator_golem95
   use pc16_gghh_d23_2h0l1d, only: reconstruct_d23
   use pc16_gghh_d27_2h0l1, only: numerator_d27 => numerator_golem95
   use pc16_gghh_d27_2h0l1d, only: reconstruct_d27
   use pc16_gghh_d29_2h0l1, only: numerator_d29 => numerator_golem95
   use pc16_gghh_d29_2h0l1d, only: reconstruct_d29
   implicit none
   type(tensrec_info_group2), intent(out) :: coeffs
   !------#[ Diagram 1:
      if (tens_rec_by_derivatives) then
         call reconstruct_d1(coeffs)
      else
         call reconstruct2(numerator_d1, coeffs%coeffs_1)
      end if
   !------#] Diagram 1:
   !------#[ Diagram 2:
      if (tens_rec_by_derivatives) then
         call reconstruct_d2(coeffs)
      else
         call reconstruct2(numerator_d2, coeffs%coeffs_2)
      end if
   !------#] Diagram 2:
   !------#[ Diagram 3:
      if (tens_rec_by_derivatives) then
         call reconstruct_d3(coeffs)
      else
         call reconstruct2(numerator_d3, coeffs%coeffs_3)
      end if
   !------#] Diagram 3:
   !------#[ Diagram 4:
      if (tens_rec_by_derivatives) then
         call reconstruct_d4(coeffs)
      else
         call reconstruct4(numerator_d4, coeffs%coeffs_4)
      end if
   !------#] Diagram 4:
   !------#[ Diagram 7:
      if (tens_rec_by_derivatives) then
         call reconstruct_d7(coeffs)
      else
         call reconstruct2(numerator_d7, coeffs%coeffs_7)
      end if
   !------#] Diagram 7:
   !------#[ Diagram 8:
      if (tens_rec_by_derivatives) then
         call reconstruct_d8(coeffs)
      else
         call reconstruct5(numerator_d8, coeffs%coeffs_8)
      end if
   !------#] Diagram 8:
   !------#[ Diagram 10:
      if (tens_rec_by_derivatives) then
         call reconstruct_d10(coeffs)
      else
         call reconstruct5(numerator_d10, coeffs%coeffs_10)
      end if
   !------#] Diagram 10:
   !------#[ Diagram 16:
      if (tens_rec_by_derivatives) then
         call reconstruct_d16(coeffs)
      else
         call reconstruct5(numerator_d16, coeffs%coeffs_16)
      end if
   !------#] Diagram 16:
   !------#[ Diagram 18:
      if (tens_rec_by_derivatives) then
         call reconstruct_d18(coeffs)
      else
         call reconstruct3(numerator_d18, coeffs%coeffs_18)
      end if
   !------#] Diagram 18:
   !------#[ Diagram 22:
      if (tens_rec_by_derivatives) then
         call reconstruct_d22(coeffs)
      else
         call reconstruct4(numerator_d22, coeffs%coeffs_22)
      end if
   !------#] Diagram 22:
   !------#[ Diagram 23:
      if (tens_rec_by_derivatives) then
         call reconstruct_d23(coeffs)
      else
         call reconstruct4(numerator_d23, coeffs%coeffs_23)
      end if
   !------#] Diagram 23:
   !------#[ Diagram 27:
      if (tens_rec_by_derivatives) then
         call reconstruct_d27(coeffs)
      else
         call reconstruct5(numerator_d27, coeffs%coeffs_27)
      end if
   !------#] Diagram 27:
   !------#[ Diagram 29:
      if (tens_rec_by_derivatives) then
         call reconstruct_d29(coeffs)
      else
         call reconstruct6(numerator_d29, coeffs%coeffs_29)
      end if
   !------#] Diagram 29:
end subroutine reconstruct_group2
!---#] subroutine reconstruct_group2:
end module pc16_gghh_golem95_2h0
