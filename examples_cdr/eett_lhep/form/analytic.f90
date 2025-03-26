module     analytic
   use precision_golem, only: ki_gol => ki
   use eett_config, only: ki
   use dilogarithme, only: zdilog
   implicit none
   private

   public :: reference_amp

   real(ki_gol), parameter :: Qq  =  2.0_ki/3.0_ki
   real(ki_gol), parameter :: T3q =  0.5_ki
   real(ki_gol), parameter :: Ql  = -1.0_ki
   real(ki_gol), parameter :: T3l = -0.5_ki
   real(ki_gol), parameter :: pi3 = &
    & 3.2898681336964528729448303332920503784378998024135968754711164580_ki

   logical, public :: include_Z = .true.

contains

function     reference_amp(vecs, scale2) result(xamp)
   use eett_model, only: mdlMtop, mdlMZ, mdlwZ, mdlSW, mdlCW, NC
   use form_factor_type, only: form_factor, operator(+), operator(*), &
       & operator(-), operator(/)
   use form_factor_3p, only: a30, a31, a32, b32
   use precision_golem, only: ki_gol => ki
   use matrice_s, only: allocation_s, deallocation_s, s_mat, set_ref, &
                      & s_mat_c, b_ref, preparesmatrix
   use parametre, only: rmass_or_cmass_par, cmass, mu2_scale_par
   use cache, only: allocate_cache, clear_cache, reset_cache
   use array, only: packb
   implicit none
   ! This routine implements equations (D.16)-(D.18) in
   ! Ref. [1] (see README).
   ! A factor of alpha_s/2/pi * (4 pi)^eps / Gamma(1-eps)
   ! has been factored out from the result

   integer, parameter :: pinches = 0
   real(ki_gol), parameter :: half = 0.5_ki_gol

   real(ki), parameter :: Qf  =  2.d0/3.d0
   real(ki), parameter :: Qe  = -1.d0
   real(ki), parameter :: I3f =  0.5d0
   real(ki), parameter :: I3e = -0.5d0

   real(ki), dimension(4,0:3), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   real(ki), dimension(0:3) :: xamp
   complex(ki_gol) :: ampr
   real(ki_gol) :: prefactor0, prefactor1, amp0
   type(form_factor) :: amp

   real(ki_gol) :: s, t, rho, tau, CF, x
   real(ki_gol) :: gZ, gTv, gTa, gev, gea
   complex(ki_gol) :: PZ, PZc
   real(ki) :: T1
   real(ki_gol) :: T2
   real(ki_gol) :: T3
   real(ki_gol) :: T4
   real(ki_gol) :: T5
   real(ki_gol) :: T6
   real(ki_gol) :: T7
   real(ki_gol) :: T8
   real(ki_gol) :: T9
   real(ki_gol) :: T10
   real(ki_gol) :: T11
   real(ki_gol) :: T12
   real(ki_gol) :: T13
   type(form_factor) :: T14
   type(form_factor) :: T15
   type(form_factor) :: T16
   type(form_factor) :: T17
   type(form_factor) :: T18
   type(form_factor) :: T19
   type(form_factor) :: T20
   type(form_factor) :: T21
   type(form_factor) :: T22
   type(form_factor) :: T23
   type(form_factor) :: T24
   type(form_factor) :: T25
   type(form_factor) :: T26
   type(form_factor) :: T27
   type(form_factor) :: T28
   type(form_factor) :: T29
   type(form_factor) :: T30
   type(form_factor) :: T31
   type(form_factor) :: T32
   type(form_factor) :: T33
   type(form_factor) :: T34
   type(form_factor) :: T35
   type(form_factor) :: T36
   type(form_factor) :: T37
   type(form_factor) :: T38
   type(form_factor) :: T39
   type(form_factor) :: T40
   type(form_factor) :: T41
   type(form_factor) :: T42
   type(form_factor) :: T43
   type(form_factor) :: T44
   type(form_factor) :: T45
   type(form_factor) :: T46
   type(form_factor) :: T47
   type(form_factor) :: T48
   type(form_factor) :: T49
   type(form_factor) :: T50

   gZ = 1.0_ki / mdlSW / mdlCW
   gTv =  (I3f - 2.d0 * Qf * mdlSW**2) * 0.5d0 * gZ
   gTa =  I3f * 0.5d0 * gZ
   gev =  (I3e - 2.d0 * Qe * mdlSW**2) * 0.5d0 * gZ
   gea =  I3e * 0.5d0 * gZ

   s = sp(vecs(1,:)+vecs(2,:), vecs(1,:)+vecs(2,:))
   t = sp(vecs(2,:)-vecs(3,:), vecs(2,:)-vecs(3,:))
   rho = mdlMtop*mdlMtop/s
   tau = t/s

   CF = 4._ki_gol / 3._ki_gol

   if (include_Z) then
      PZ = s / cmplx(s - mdlMZ*mdlMZ, mdlMZ*mdlwZ, ki)
      PZc = conjg(PZ)
   else
      PZ = 0._ki_gol
      PZc = 0._ki_gol
   end if

   rmass_or_cmass_par = cmass
   call allocation_s(3)
   set_ref = (/1, 2, 3/)
   b_ref = packb(set_ref)
   call allocate_cache(3)
   s_mat => s_mat_c

   x = s/mdlMtop/mdlMtop - 2._ki_gol

   s_mat(1,:) = (/ -2._ki_gol,          x, 0._ki_gol /)
   s_mat(2,:) = (/          x, -2._ki_gol, 0._ki_gol /)
   s_mat(3,:) = (/  0._ki_gol,  0._ki_gol, 0._ki_gol /)
   s_mat(:,:) = mdlMtop*mdlMtop * s_mat(:,:)
   call preparesmatrix()

   mu2_scale_par = scale2
   prefactor0 = (1._ki_gol/36._ki_gol*NC)
   prefactor1 = (1._ki_gol/18._ki_gol*CF*NC)
   T14 = b32(pinches)*prefactor1
   T15 = T14*tau
   T16 = a30(pinches)*prefactor1
   T17 = a31(1,pinches)*prefactor1
   T18 = a31(2,pinches)*prefactor1
   T19 = -(T18+T17+T16)
   T20 = a32(1,2,pinches)*prefactor1
   T21 = T19-T20
   T22 = T21*s
   T23 = (T14+(T14+T15)*2._ki_gol*tau)*2._ki_gol+T22
   T24 = T16+T17+T18
   T25 = T20+T24
   T26 = T15*2._ki_gol
   T27 = T25*s
   T28 = ((T25*t-(T26+T14))*2._ki_gol+T27)*48._ki_gol
   T29 = -(T18+T17)
   T30 = -(T20+T16)
   T31 = T30*192._ki_gol
   T32 = a32(1,1,pinches)*prefactor1
   T33 = a32(2,2,pinches)*prefactor1
   T34 = -(T33+T32)
   T35 = T34*48._ki_gol
   T1 = mdlMtop*mdlMtop
   T36 = T34*96._ki_gol
   T37 = T17+T18
   T38 = T16+T20
   T32 = T32+T33
   T33 = T32*96._ki_gol
   T39 = T14*192._ki_gol
   T15 = -(T15+T14)
   T40 = T14*rho
   T41 = T19+T20
   T42 = T33+T41*192._ki_gol
   T43 = T24-T20
   T19 = ((T27-(T14-T15*2._ki_gol*tau)*2._ki_gol)*48._ki_gol+((T26-T40)*192._ki_&
   &gol+(T25*96._ki_gol+T42*rho)*cmplx(T1, 0.0_ki_gol, ki_gol)+(T19*384._ki_gol+&
   &T33+(T34*192._ki_gol+T43*384._ki_gol)*rho+T42*tau)*t)*rho+(T29*192._ki_gol+T&
   &30*96._ki_gol+T35)*cmplx(T1, 0.0_ki_gol, ki_gol)+(T16+T17+T18+T20+T25*tau)*9&
   &6._ki_gol*t)*gTv*gev
   T27 = T34*64._ki_gol
   T42 = T27+T43*128._ki_gol
   T44 = T23*72._ki_gol
   T45 = T32*72._ki_gol
   T16 = (T21*tau-(T20+T18+T17+T16))*t
   T17 = T16*144._ki_gol
   T18 = T17+T44+(T25*432._ki_gol+T45)*cmplx(T1, 0.0_ki_gol, ki_gol)
   T2 = gea*gea
   T3 = gev*gev
   T15 = T15*576._ki_gol+T40*288._ki_gol
   T20 = T34*288._ki_gol
   T46 = T32*144._ki_gol
   T47 = T25*288._ki_gol+T46
   T48 = T20+T21*720._ki_gol+T47*rho
   T20 = T25*576._ki_gol+T46+(T20+T21*576._ki_gol)*rho+T47*tau
   T46 = T38*1152._ki_gol
   T47 = T32*288._ki_gol
   T17 = T17+T44+(T37*288._ki_gol+T38*144._ki_gol+T45)*cmplx(T1, 0.0_ki_gol, ki_&
   &gol)
   T44 = T14*T2
   T45 = T14*T3
   T49 = T34*144._ki_gol
   T43 = T43*288._ki_gol+T49
   T49 = T24*576._ki_gol+T49+(T41*576._ki_gol+T47)*rho+T43*tau
   T4 = gTv*gTv
   T50 = T21*192._ki_gol
   amp = (T16*64._ki_gol+T23*32._ki_gol+(T19+(T28+(T29*288._ki_gol+T31+T35)*cmpl&
   &x(T1, 0.0_ki_gol, ki_gol)+(T39+(T29*384._ki_gol+T31+T36)*t+(T33+T37*384._ki_&
   &gol+T38*192._ki_gol)*cmplx(T1, 0.0_ki_gol, ki_gol))*rho)*gTa*gea)*PZc+((T40-&
   &T26)*128._ki_gol+(T21*64._ki_gol+T42*rho)*cmplx(T1, 0.0_ki_gol, ki_gol)+(T24&
   &*256._ki_gol+T27+(T32*128._ki_gol+T41*256._ki_gol)*rho+T42*tau)*t)*rho+(T19+&
   &(((((T20*T2+T20*T3)*t+(T48*T2+T48*T3)*cmplx(T1, 0.0_ki_gol, ki_gol)+T15*T2+T&
   &15*T3)*rho+T18*T2+T18*T3)*gTa+(((T14+T26+T21*t)*2._ki_gol+T22)*288._ki_gol+(&
   &(T29*1728._ki_gol+T30*1152._ki_gol+T34*576._ki_gol)*cmplx(T1, 0.0_ki_gol, ki&
   &_gol)+(T32*576._ki_gol+T37*1728._ki_gol+T46)*t-T14*1152._ki_gol)*rho+(T37*14&
   &40._ki_gol+T46+T47)*cmplx(T1, 0.0_ki_gol, ki_gol))*gTv*gea*gev)*gTa+((((-(T4&
   &5+T44))*2._ki_gol*tau+(T44+T45)*rho)*288._ki_gol+((T21*T2+T21*T3)*144._ki_go&
   &l+(T43*T2+T43*T3)*rho)*cmplx(T1, 0.0_ki_gol, ki_gol)+(T49*T2+T49*T3)*t)*rho+&
   &T17*T2+T17*T3)*T4)*PZc+(T28+(T35+T50)*cmplx(T1, 0.0_ki_gol, ki_gol)+(T39+(T2&
   &5*192._ki_gol+T33)*cmplx(T1, 0.0_ki_gol, ki_gol)+(T36+T50)*t)*rho)*gTa*gea)*&
   &PZ+(T32*32._ki_gol+T37*128._ki_gol+T38*64._ki_gol)*cmplx(T1, 0.0_ki_gol, ki_&
   &gol))
   T5 = prefactor1*rho
   T6 = 2._ki_gol*T5
   T7 = prefactor1*tau
   T8 = T7+prefactor1-T6
   T9 = rho*rho
   T10 = 2._ki_gol*T9*prefactor1
   T11 = (96._ki_gol*(T5-T7)-48._ki_gol*prefactor1)*gTa*gea
   T6 = 48._ki_gol*(2._ki_gol*(T6-(prefactor1+T7))*tau-(prefactor1+T10))*gTv*gev
   T12 = 72._ki_gol*(prefactor1+2._ki_gol*(T7+prefactor1)*tau)+(288._ki_gol*(-(p&
   &refactor1+T7))+144._ki_gol*T5)*rho
   T13 = T10+prefactor1
   ampr = (32._ki_gol*(T10+prefactor1+2._ki_gol*T8*tau)+(T11+T6)*PZc+(T11+T6+(((&
   &T12*T2+T12*T3)*gTa+(576._ki_gol*(T7-T5)+288._ki_gol*prefactor1)*gTv*gea*gev)&
   &*gTa+72._ki_gol*(2._ki_gol*(T2*T8+T3*T8)*tau+T13*T2+T13*T3)*T4)*PZc)*PZ)
   T5 = prefactor0*rho
   T6 = 2._ki_gol*T5
   T7 = prefactor0*tau
   T8 = T7+prefactor0-T6
   T9 = 2._ki_gol*T9*prefactor0
   T10 = (96._ki_gol*(T5-T7)-48._ki_gol*prefactor0)*gTa*gea
   T6 = 48._ki_gol*(2._ki_gol*(T6-(prefactor0+T7))*tau-(prefactor0+T9))*gTv*gev
   T11 = 72._ki_gol*(prefactor0+2._ki_gol*(T7+prefactor0)*tau)+(288._ki_gol*(-(p&
   &refactor0+T7))+144._ki_gol*T5)*rho
   T12 = T9+prefactor0
   amp0 = (32._ki_gol*(T9+prefactor0+2._ki_gol*T8*tau)+(T10+T6)*PZc+(T10+T6+(((T&
   &11*T2+T11*T3)*gTa+(576._ki_gol*(T7-T5)+288._ki_gol*prefactor0)*gTv*gea*gev)*&
   &gTa+72._ki_gol*(2._ki_gol*(T2*T8+T3*T8)*tau+T12*T2+T12*T3)*T4)*PZc)*PZ)
   rmass_or_cmass_par = cmass
   nullify(s_mat)
   call deallocation_s()
   call clear_cache()
   xamp(0) = amp0
   ! The factor -1/2 in front of ampr
   ! is the value of the higher dim. triangle
   xamp(1) = 2.0_ki * real(amp%C - 0.5_ki * ampr, ki)
   xamp(2) = 2.0_ki * real(amp%B, ki)
   xamp(3) = 2.0_ki * real(amp%A, ki)
   ! Factor 1/2 from mismatch between integral measure and prefactor
   ! alpha_s/2pi
   xamp(1:3) = 0.5_ki * xamp(1:3)
end function reference_amp

pure function sp(vec1, vec2)
   implicit none
   real(ki), dimension(0:3), intent(in) :: vec1, vec2
   real(ki) :: sp

   sp = vec1(0)*vec2(0) - vec1(3)*vec2(3) &
      - vec1(1)*vec2(1) - vec1(2)*vec2(2)
end  function sp

end module analytic
