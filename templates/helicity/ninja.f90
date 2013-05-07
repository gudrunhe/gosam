[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]ninjah[% helicity %]
   ! This file has been generated for ninja 
   use ninja_module, only: ki_nin
   use [% process_name asprefix=\_ %]config
   implicit none
   private[%

   @for groups var=grp %]
   public :: ninja_reduce_group[% grp %][%
   @end @for %]
contains
 !---#[ grouped numerators for ninja:[%
   @for groups var=grp %][%
      @with eval loopsize group=grp result=ls %]
!-----#[ subroutine numeval_group[% grp %]:
subroutine     numeval_group[% grp %](icut, Q, mu2, num) &
   & bind(c, name="gggg_g[% grp %]h[% helicity %]l1_ninja")
  use iso_c_binding, only: c_int
  use ninja_module, only: ki_nin[%
         @for repeat num_legs shift=1 %][%
            @if is_first %]
   use [% process_name asprefix=\_ %]kinematics, only:[%
            @else %],[%
            @end @if %] k[% $_ %][%
         @end @for %]
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l1, only: numerator_d[% DIAG %] => numerator_ninja[%
         @end @for %][%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]
   implicit none
   integer(c_int), intent(in) :: icut
   complex(ki_nin), dimension(0:3), intent(in) :: Q
   complex(ki_nin), intent(in) :: mu2
   complex(ki_nin), intent(out) :: num
   complex(ki_nin) :: temp

   logical, dimension(0:[% count diagrams group=grp %]-1) :: nonzero
   real(ki_nin), dimension(0:3) :: R
   complex(ki_nin) :: Q2[%
         @for propagators group=grp %][%
            @if is_first %]
   complex(ki_nin) ::[%
            @else %],[%
            @end @if %]denom[% $_ %][%
         @end @for %]

   nonzero(:) = .true.
   Q2 = Q(0)*Q(0) - Q(1)*Q(1) - Q(2)*Q(2) - Q(3)*Q(3) - mu2

   select case(icut)[%
         @for cuts ls %][%
            @for diagrams group=grp global_index=DIAGIDX var=DIAG
                 unpinched=$_ invert=true %][%
               @if is_first %]
   case([% $_ %])[%
               @end @if %]
      nonzero([% DIAGIDX %]) = .false.[%
               @if is_last %][%
                  @for propagators group=grp prefix=k index=propidx %][%
                     @if eval $_ ~ ( propidx - 1 ) %]
      denom[% propidx %] = 0.0_ki[%
                     @else %][%
                        @if eval momentum .eq. 0 %]
      denom[% propidx %] = Q2[%
                           @if eval mass .eq. 0 %][%
                           @else %] - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %][%
                        @else %]
      R = real([% momentum %], ki_nin)
      denom[% propidx %] = (Q(0) + Q(0) + R(0))*R(0) &
                 &    - (Q(1) + Q(1) + R(1))*R(1) &
                 &    - (Q(2) + Q(2) + R(2))*R(2) &
                 &    - (Q(3) + Q(3) + R(3))*R(3)[%
                           @if eval mass .eq. 0 %][%
                           @else %]&
                 &    - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %][%
                        @end @if %][%
                     @end @if %][%
                  @end @for propagators %][%
               @end @if %][%
            @end @for diagrams %][%
         @end @for cuts %]
   case default[%
         @for propagators group=grp prefix=k %][%
            @if eval momentum .eq. 0 %]
      denom[% $_ %] = Q2[%
               @if eval mass .eq. 0 %][%
               @else %] - [%mass%]*[%mass%][%
                  @if eval width .eq. 0 %][%
                  @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                  @end @if %][%
               @end @if %][%
            @else %]
      R = real([% momentum %], ki_nin)
      denom[% $_ %] = Q2 + (Q(0) + Q(0) + R(0))*R(0) &
                 &    - (Q(1) + Q(1) + R(1))*R(1) &
                 &    - (Q(2) + Q(2) + R(2))*R(2) &
                 &    - (Q(3) + Q(3) + R(3))*R(3)[%
               @if eval mass .eq. 0 %][%
               @else %]&
                 &    - [%mass%]*[%mass%][%
                  @if eval width .eq. 0 %][%
                  @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                  @end @if width .eq. 0 %][%
               @end @if mass .eq. 0 %][%
            @end @if momentum .eq. 0 %][%
         @end @for propagators %]
   end select
   
   num = (0.0_ki_nin, 0.0_ki_nin)[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   !-------#[ Diagram [% DIAG %]:
   if(nonzero([% index %])[%
            @if use_flags_1 %].and.evaluate_virt_diagram([% DIAG %])[%
            @end @if %]) then
	  call numerator_d[% DIAG %](icut, Q, mu2, temp)
      num = num [%
      @if diagsum %]+ temp[%
            @for elements pinches %] * denom[% $_ %][%
            @end @for %][%
            @else %][% diagram_sign %] [%
            @if is_nf %]Nfrat * [%
            @end @if %]temp[%
            @for elements pinches %] * denom[% $_ %][%
            @end @for %][% @end @if %]
   end if
   !-------#] Diagram [% DIAG %]:[%
         @end @for diagrams %]
end subroutine numeval_group[% grp %]
!-----#] subroutine numeval_group[% grp %]:
!-----#[ subroutine numeval_group[% grp %]_d:
subroutine     numeval_group[% grp %]_d(icut, beta, vperp, v0, coeff) &
   & bind(c, name="gggg_g[% grp %]h[% helicity %]l12_ninja")
  use iso_c_binding, only: c_int
  use ninja_module, only: ki_nin[%
         @for repeat num_legs shift=1 %][%
            @if is_first %]
   use [% process_name asprefix=\_ %]kinematics, only:[%
            @else %],[%
            @end @if %] k[% $_ %][%
         @end @for %]
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l12, only: numerator_d[% DIAG %] => numerator_d[%
         @end @for %][%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]
   implicit none
   integer(c_int), intent(in) :: icut
   complex(ki_nin), intent(in) :: beta
   complex(ki_nin), dimension(0:3), intent(in) :: vperp
   complex(ki_nin), dimension(0:3), intent(in) :: v0
   complex(ki_nin), dimension(0:*), intent(out) :: coeff
   complex(ki_nin), dimension(0:0) :: temp

   logical, dimension(0:[% count diagrams group=grp %]-1) :: nonzero
   real(ki_nin), dimension(0:3) :: R[%
         @for propagators group=grp %][%
            @if is_first %]
   complex(ki_nin) ::[%
            @else %],[%
            @end @if %]denom[% $_ %][%
         @end @for %]

   nonzero(:) = .true.

   select case(icut)[%
         @for cuts ls %][%
            @for diagrams group=grp global_index=DIAGIDX var=DIAG
                 unpinched=$_ invert=true %][%
               @if is_first %]
   case([% $_ %])[%
               @end @if %]
      nonzero([% DIAGIDX %]) = .false.[%
               @if is_last %][%
                  @for propagators group=grp prefix=k index=propidx %][%
                     @if eval $_ ~ ( propidx - 1 ) %]
      denom[% propidx %] = 0.0_ki[%
                     @else %][%
                        @if eval momentum .eq. 0 %]
      denom[% propidx %] = - 2.0_ki_nin*(  vperp(0) * v0(0) &
                 &    - vperp(1) * v0(1) &
                 &    - vperp(2) * v0(2) &
                 &    - vperp(3) * v0(3) )[%
                        @else %]
      R = real([% momentum %], ki_nin)
      denom[% propidx %] = 2.0_ki_nin*(  vperp(0)*( R(0) - v0(0) ) &
                 &    - vperp(1)*( R(1) - v0(1) ) &
                 &    - vperp(2)*( R(2) - v0(2) ) &
                 &    - vperp(3)*( R(3) - v0(3) ) )[%
                        @end @if %][%
                     @end @if %][%
                  @end @for propagators %][%
               @end @if %][%
            @end @for diagrams %][%
         @end @for cuts %]
   case default[%
                  @for propagators group=grp prefix=k %][%
                        @if eval momentum .eq. 0 %]
      denom[% $_ %] = - 2.0_ki_nin*(  vperp(0) * v0(0) &
                 &    - vperp(1) * v0(1) &
                 &    - vperp(2) * v0(2) &
                 &    - vperp(3) * v0(3) )[%
                        @else %]
      R = real([% momentum %], ki_nin)
      denom[% $_ %] = 2.0_ki_nin*(  vperp(0)*( R(0) - v0(0) ) &
                 &    - vperp(1)*( R(1) - v0(1) ) &
                 &    - vperp(2)*( R(2) - v0(2) ) &
                 &    - vperp(3)*( R(3) - v0(3) ) )[%
                        @end @if %][%
                  @end @for propagators %]
   end select
   
   coeff(0) = (0.0_ki_nin, 0.0_ki_nin)[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   !-------#[ Diagram [% DIAG %]:
   if(nonzero([% index %])[%
            @if use_flags_1 %].and.evaluate_virt_diagram([% DIAG %])[%
            @end @if %]) then
      if( [% rank diagram=DIAG %] .eq. [% loopsize diagram=DIAG %] ) then
	     call numerator_d[% DIAG %](icut, beta, vperp, temp)
         coeff(0) = coeff(0) [%
         @if diagsum %]+ temp(0)[%
               @for elements pinches %] * denom[% $_ %][%
               @end @for %][%
               @else %][% diagram_sign %] [%
               @if is_nf %]Nfrat * [%
               @end @if %]temp(0)[%
               @for elements pinches %] * denom[% $_ %][%
               @end @for %][% @end @if %]
      end if
   end if
   !-------#] Diagram [% DIAG %]:[%
         @end @for diagrams %]
end subroutine numeval_group[% grp %]_d
!-----#] subroutine numeval_group[% grp %]_d:
!-----#[ subroutine numeval_group[% grp %]_t:
subroutine     numeval_group[% grp %]_t(icut, mu2, a, b, c, gdeg,&
			                           & vcut, msqcut, coeff) &
   & bind(c, name="gggg_g[% grp %]h[% helicity %]l13_ninja")
  use iso_c_binding, only: c_int
  use ninja_module, only: ki_nin, ninja_poly_multiply[%
         @for repeat num_legs shift=1 %][%
            @if is_first %]
   use [% process_name asprefix=\_ %]kinematics, only:[%
            @else %],[%
            @end @if %] k[% $_ %][%
         @end @for %]
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l13, only: numerator_t[% DIAG %] => numerator_t[%
         @end @for %][%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]
   implicit none
   integer(c_int), intent(in) :: icut, gdeg
   complex(ki_nin), dimension(0:3), intent(in) :: a, b, c
   real(ki_nin), dimension(0:3), intent(in) :: vcut
   complex(ki_nin), intent(in) :: mu2, msqcut
   complex(ki_nin), dimension(0:*), intent(out) :: coeff
   complex(ki_nin), dimension(0:4) :: temp
   integer(c_int) :: gdegshift, deg, rankshift
   integer, parameter :: grank = [% rank %]
   integer, parameter :: gloopsize = [% loopsize group=grp %]
   integer, parameter :: grankshift = [% loopsize group=grp %] - [% rank %]
   integer :: ii

   logical, dimension(0:[% count diagrams group=grp %]-1) :: nonzero
   real(ki_nin), dimension(0:3) :: R
   complex(ki_nin) :: d0add, d1add, d2add[%
         @for propagators group=grp %][%
            @if is_first %]
   complex(ki_nin), dimension(0:2) ::[%
            @else %],[%
            @end @if %]denom[% $_ %][%
         @end @for %]

   gdegshift = grankshift + gdeg

   nonzero(:) = .true.
   d1add = - ( (a(0) + a(0) + vcut(0))*vcut(0) &
             &  - (a(1) + a(1) + vcut(1))*vcut(1) &
             &  - (a(2) + a(2) + vcut(2))*vcut(2) &
             &  - (a(3) + a(3) + vcut(3))*vcut(3) ) &
		 & + msqcut
   d0add = - 2.0_ki_nin *( b(0)*vcut(0) &
                        &  - b(1)*vcut(1) - b(2)*vcut(2) - b(3)*vcut(3) )
   d2add = - 2.0_ki_nin *( c(0)*vcut(0) &
                        &  - c(1)*vcut(1) - c(2)*vcut(2) - c(3)*vcut(3) )

   select case(icut)[%
         @for cuts ls %][%
            @for diagrams group=grp global_index=DIAGIDX var=DIAG
                 unpinched=$_ invert=true %][%
               @if is_first %]
   case([% $_ %])[%
               @end @if %]
      nonzero([% DIAGIDX %]) = .false.[%
               @if is_last %][%
                  @for propagators group=grp prefix=k index=propidx %][%
                     @if eval $_ ~ ( propidx - 1 ) %]
      denom[% propidx %](:) = (0.0_ki_nin,0.0_ki_nin)[%
                     @else %][%
                        @if eval momentum .eq. 0 %]
      denom[% propidx %](1) = d1add[%
                           @if eval mass .eq. 0 %][%
                           @else %] - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %]
      denom[% propidx %](0) = d0add
	  denom[% propidx %](2) = d2add[%
                        @else %]
      R = real([% momentum %], ki_nin)
      denom[% propidx %](1) = d1add + (a(0) + a(0) + R(0))*R(0) &
                 &    - (a(1) + a(1) + R(1))*R(1) &
                 &    - (a(2) + a(2) + R(2))*R(2) &
                 &    - (a(3) + a(3) + R(3))*R(3)[%
                           @if eval mass .eq. 0 %][%
                           @else %]&
                 &    - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %]
      denom[% propidx %](0) = d0add + 2.0_ki_nin *( b(0)*R(0) &
                        &  - b(1)*R(1) - b(2)*R(2) - b(3)*R(3) )
	  denom[% propidx %](2) = d2add + 2.0_ki_nin *( c(0)*R(0) &
                        &  - c(1)*R(1) - c(2)*R(2) - c(3)*R(3) )[%
                        @end @if %][%
                     @end @if %][%
                  @end @for propagators %][%
               @end @if %][%
            @end @for diagrams %][%
         @end @for cuts %]
   case default[%
                  @for propagators group=grp prefix=k %][%
                        @if eval momentum .eq. 0 %]
      denom[% $_ %](1) = d1add[%
                           @if eval mass .eq. 0 %][%
                           @else %] - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %]
      denom[% $_ %](0) = d0add
	  denom[% $_ %](2) = d2add[%
                        @else %]
      R = real([% momentum %], ki_nin)
      denom[% $_ %](1) = d1add + (a(0) + a(0) + R(0))*R(0) &
                 &    - (a(1) + a(1) + R(1))*R(1) &
                 &    - (a(2) + a(2) + R(2))*R(2) &
                 &    - (a(3) + a(3) + R(3))*R(3)[%
                           @if eval mass .eq. 0 %][%
                           @else %]&
                 &    - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_nin, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %]
      denom[% $_ %](0) = d0add + 2.0_ki_nin *( b(0)*R(0) &
                        &  - b(1)*R(1) - b(2)*R(2) - b(3)*R(3) )
	  denom[% $_ %](2) = d2add + 2.0_ki_nin *( c(0)*R(0) &
                        &  - c(1)*R(1) - c(2)*R(2) - c(3)*R(3) )[%
                        @end @if %][%
                  @end @for propagators %]
   end select
   
   do ii=0,gdeg
      coeff(ii) = (0.0_ki_nin, 0.0_ki_nin)
   enddo
[%
         @for diagrams group=grp var=DIAG idxshift=1 %]
   !-------#[ Diagram [% DIAG %]:
   if(nonzero([% index %])[%
            @if use_flags_1 %].and.evaluate_virt_diagram([% DIAG %])[%
            @end @if %]) then
	  deg = gdegshift + [%rank diagram=DIAG%] - [%loopsize diagram=DIAG%]
      if(deg .ge. 0) then 
	     rankshift = [%loopsize diagram=DIAG%] - [%rank diagram=DIAG%] - grankshift
	     call numerator_t[% DIAG %](icut, mu2, a, b, c, deg, temp)[%
	      @if diagsum %][% @for elements pinches %]
         call ninja_poly_multiply(temp, denom[% $_ %], deg)[%
               @end @for %]
	     do ii=0,deg
           coeff(rankshift+ii) =  coeff(ii+rankshift) + temp(ii)
	     enddo[%
               @else %][%
               @for elements pinches %]
         call ninja_poly_multiply(temp, denom[% $_ %], deg)[%
               @end @for %]
	       do ii=0,deg
            coeff(ii+rankshift) = coeff(ii+rankshift) [%
	     		diagram_sign %] [%
               @if is_nf %]Nfrat *[% @end @if %] temp(ii)
         enddo[%
               @end @if %]
      endif
   end if
   !-------#] Diagram [% DIAG %]:[%
         @end @for diagrams %]
end subroutine numeval_group[% grp %]_t
!-----#] subroutine numeval_group[% grp %]_t:[%
      @end @with %][%
   @end @for groups %]
!---#] grouped numerators for ninja:
!---#[ reduce groups with ninja:[%
   @for groups var=grp %]
!-----#[ subroutine ninja_reduce_group[% grp %]:
subroutine     ninja_reduce_group[% grp %](scale2,tot,totr,ok)
   use iso_c_binding, only: c_ptr, c_loc
   use ninja_module
   use [% process_name asprefix=\_ %]kinematics
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l1, only: numerator_diagram[% DIAG %] => numerator_ninja
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l12, only: numerator_d_diagram[% DIAG %] => numerator_d
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l13, only: numerator_t_diagram[% DIAG %] => numerator_t[%
         @end @for %]
   use [% process_name asprefix=\_ %]globalsl1, only: epspow[%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]

   implicit none
   real(ki_nin), intent(in) :: scale2
   complex(ki_nin), dimension(-2:0), intent(out) :: tot
   complex(ki_nin), intent(out) :: totr
   logical, intent(out) :: ok

   complex(ki_nin), dimension(-2:0) :: acc
   complex(ki_nin) :: accr
   logical :: acc_ok

   integer :: istopm, istop0

   integer, parameter :: effective_group_rank = [% rank %]

   !-----------#[ invariants for ninja:
   real(ki_nin), dimension([% loopsize group=grp %]**2), target :: s_mat
   !-----------#] initialize invariants:
   [%
   @if complex_mass_needed group=grp %]complex(ki_nin)[%
   @else %]real(ki_nin)[%
   @end @if %], dimension([% loopsize group=grp %]) :: msq
   real(ki_nin), dimension([% loopsize group=grp %]*4) :: Vi
   
   if(ninja_test.eq.1) then
      istopm = 1
      istop0 = 1
   else
      istopm = ninja_istop
      istop0 = max(2,ninja_istop)
   end if[%
   @for propagators group=grp %]
   msq([% $_ %]) = [% 
      @if eval mass .eq. 0 %]0.0_ki_nin[%
      @else %][%
         @if eval width .eq. 0 %]real([% mass %]*[% mass %], ki_nin)[%
         @else %]real([%mass%],ki_nin)*cmplx([%mass%],-[%width%],ki_nin)[%
         @end @if %][%
      @end @if %]
   !Vi(([% $_ %]-1)*[% loopsize group=grp %]+1:([% $_ %]-1)*[% loopsize group=grp %]+4) = real([% momentum %], ki_nin)
   Vi(([% $_ %]-1)*4+1:([% $_ %]-1)*4+4) = real([% momentum %], ki_nin)[%
   @end @for %]
   !-----------#[ initialize invariants:[%
      @for smat upper diagonal
           group=grp powfmt=%s**%d prodfmt=%s*%s prefix=es %]
   s_mat([% loopsize group=grp %]*([%rowindex%]-1)+[%colindex%]) = real([%
            @if re.is_zero %]0.0_ki[% 
            @else %][%
               @for elements re delimiter=; var=term first=first_term %][%
                  @for elements term delimiter=: %][%
                     @if is_first %][%
                        @if eval $_ .ge. 0 %][%
                           @if first_term %][%
                           @else %]+[%
                           @end @if %][%
                        @else %]-[%
                        @end @if %][%
   
                        @select $_
                        @case 2 -2 %][%
                        @case 4 -4%]2.0_ki*[%
                        @else %][%
                           @with eval .abs. $_ / 2 result=num %][%
                           num convert=float format=%0.1f_ki%][%
                           @end @with %]*[%
                        @end @select %][%
                     @else %][% $_ %][%
                     @end @if %][%
                  @end @for %][%
               @end @for %][%
            @end @if %][%
      
            @for elements im delimiter=; var=term first=first_term %][%
               @for elements term delimiter=: %][%
                  @if is_first %][%
                     @if eval $_ .ge. 0 %]+[%
                     @else %]-[%
                     @end @if %][%
      
                     @select $_
                     @case 2 -2 %][%
                     @case 4 -4%]2.0_ki*[%
                     @else %][%
                        @with eval .abs. $_ / 2 result=num %][%
                           num convert=float format=%0.1f_ki %][%
                        @end @with %]*[%
                     @end @select %][%
                  @else %][% $_ %][%
                  @end @if %][%
               @end @for %][%
            @end @for %], ki_nin)[%
      
            @if eval rowindex .ne. colindex %]
   s_mat([% loopsize group=grp %]*([% colindex %]-1)+[% rowindex %]) = s_mat([% loopsize group=grp %]*([% 
                                        rowindex %]-1)+[% colindex %])[%
            @end @if %][%
         @end @for %]
   !-----------#] initialize invariants

   
   if(ninja_group_numerators) then
      !------#[ reduce numerator numeval_group[% grp %]:
    call ninja_group(numeval_group[%grp%], numeval_group[%grp%]_t,&
	               & numeval_group[%grp%]_d, &
                   & tot, totr, [% loopsize group=grp %], &
                   & Vi, msq, c_loc( s_mat(1) ), [% rank group=grp %], [%
                     @if iterator_empty propagators group=grp massive
                     %]istop0[%
                     @else %]istopm[%
                     @end @if %], scale2 )

      !------#] reduce numerator numeval_group[% grp %]:
   else
      !------#[ sum over reduction of single diagrams:[%
   @for diagrams group=grp var=DIAG index=DIAGIDX idxshift=1 %][%
      @if use_flags_1 %]
      if(evaluate_virt_diagram([% DIAG %])) then[%
      @end @if %]
         if(debug_nlo_diagrams) then
            write(logfile,*) "<diagram index='[% DIAG %]'>"
         end if
         call ninja_diagram(numerator_diagram[% DIAG %], numerator_t_diagram[% DIAG %], &
          &  numerator_d_diagram[% DIAG %],  acc, accr, [% loopsize group=grp %], [% loopsize diagram=DIAG %], &
          & Vi, msq, c_loc( s_mat(1) ), [% rank %], [%
            @if iterator_empty propagators group=grp
            select=indices massive %]istop0[%
            @else %]istopm[%
            @end @if %], scale2, &
          & (/[% indices %]/))
         if(debug_nlo_diagrams) then
            write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-finite' re='", [%
                  diagram_sign %]real(acc(0), ki), &
               & "' im='", aimag(acc(0)), "'/>"
            write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-single' re='", [%
                  diagram_sign %]real(acc(-1), ki), &
               & "' im='", aimag(acc(-1)), "'/>"
            write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-double' re='", [%
                  diagram_sign %]real(acc(-2), ki), &
               & "' im='", aimag(acc(-2)), "'/>"
            write(logfile,'(A32,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-rational' re='", [%
                  diagram_sign %]real(accr, ki), &
               & "' im='", aimag(accr), "'/>"
            if(ok) then
               write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
            else
               write(logfile,'(A29)') "<flag name='ok' status='no'/>"
            end if
            write(logfile,*) "</diagram>"
         end if
         tot = [%
      @if is_first %][% @if diagsum %] + [%
      @else %][% diagram_sign %][% @end @if %][%
      @else %]tot [% @if diagsum %] + [% @else %] [% diagram_sign %] [%
      @end @if %][%
      @end @if %][%
      @if is_nf %][% @if diagsum %] [% @else %] Nfrat * [%
      @end @if %][%
      @end @if %]acc
         totr = [%
      @if is_first %][% @if diagsum %] + [%
      @else %][% diagram_sign %][% @end @if %][%
      @else %]totr [% @if diagsum %] + [% @else %] [% diagram_sign %] [%
      @end @if %][%
      @end @if %][%
      @if is_nf %][% @if diagsum %] [% @else %] Nfrat * [%
      @end @if %][%
      @end @if %]accr[%
      @if is_first %][%
      @else %]
         ok = ok .and. acc_ok[%
      @end @if %][%
      @if use_flags_1 %]
      end if[%
      @end @if %][%
   @end @for %]
      !------#] sum over reduction of single diagrams:
	  endif

end subroutine ninja_reduce_group[% grp %]
!-----#] subroutine ninja_reduce_group[% grp %]:[%
   @end @for %]
!---#] reduce groups with ninja:
end module [% process_name asprefix=\_ %]ninjah[% helicity %]
