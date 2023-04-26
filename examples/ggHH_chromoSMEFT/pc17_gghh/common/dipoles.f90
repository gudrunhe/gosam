module     pc17_gghh_dipoles
   use pc17_gghh_config, only: ki
   use pc17_gghh_color, only: gammaF, gammaA, &
       & CF, CA, numcs, KF, KA, &
       & T1T2
   use pc17_gghh_kinematics, only: num_legs, dotproduct, &
       lambda
   implicit none

   private :: ki, gammaF, gammaA, CF, CA, numcs, KF, KA, &
       & T1T2
   private :: num_legs, dotproduct, lambda


   real(ki), parameter :: pi = &
   & 3.1415926535897932384626433832795028841971693993751_ki

   private :: V_SING, V_SING_QED, GAMMA_F, GAMMA_A
   private :: I_ff, I_if, I_ii, I_ii_qed, I_if_qed, I_ff_qed
contains
   function insertion_operator(mu_sq, vec, I, J)
      ! This function calculates the poles of the insertion operator
      ! for the specified process.
      ! See [Catani,Dittmaier,Seymour,Trocsanyi]
      ! The result does not include the factor of
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      integer, optional, intent(in) :: I, J
      complex(ki), dimension(numcs,numcs,2) :: insertion_operator

      if(present(I) .and. present(J)) then
              insertion_operator = &
                 &   I_ff(mu_sq, vec, I, J) &
                 & + I_if(mu_sq, vec, I, J) &
                 & + I_ii(mu_sq, vec, I, J)
      else
              insertion_operator = &
                 &   I_ff(mu_sq, vec) &
                 & + I_if(mu_sq, vec) &
                 & + I_ii(mu_sq, vec)
      end if
   end  function insertion_operator


   function insertion_operator_qed(mu_sq, vec, I, J)
      !This function calcualtions the poles for infrared QED singularities
      !See [Dittmaier '99] and [Gehrmann, Greiner '10] for details
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      integer, optional, intent(in) :: I, J
      complex(ki), dimension(numcs,numcs,2) :: insertion_operator_qed

      if(present(I) .and. present(J)) then
              insertion_operator_qed = &
                 &   I_ff_qed(mu_sq, vec, I, J) &
                 & + I_if_qed(mu_sq, vec, I, J) &
                 & + I_ii_qed(mu_sq, vec, I, J)
      else
              insertion_operator_qed = &
                 &   I_ff_qed(mu_sq, vec) &
                 & + I_if_qed(mu_sq, vec) &
                 & + I_ii_qed(mu_sq, vec)
      end if



   end  function insertion_operator_qed


   !=================================================================
   function I_ff(mu_sq, vec, I, J)
      ! This function calculates I_m as specified in (6.16) of
      ! [Catani,Dittmaier,Seymour,Trocsanyi]
      ! The result does not include the factor of
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      use pc17_gghh_model
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      integer, optional, intent(in) :: I, J
      complex(ki), dimension(numcs,numcs,2) :: I_ff
      real(ki), dimension(2) :: term
      complex(ki), dimension(numcs,numcs) :: matrix
      real(ki) :: log_s, s_jk
      real(ki) :: Q_jk, rho, v_jk
      real(ki) :: m1_2, m2_2, mu1_2, mu2_2
      logical :: flag

      I_ff(:,:,:) = 0.0_ki
      
   end  function I_ff

   !=================================================================
   function I_if(mu_sq, vec, I, J)
      ! Implements equation (6.52) from the above paper for
      ! each initial state particle. Again we omit the prefactor
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      use pc17_gghh_model
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      complex(ki), dimension(numcs,numcs,2) :: I_if
      real(ki), dimension(2) :: term
      complex(ki), dimension(numcs,numcs) :: matrix
      integer, optional, intent(in) :: I, J
      real(ki) :: log_s, s_ja
      logical :: flag

      I_if(:,:,:) = 0.0_ki
      
      
   end  function I_if

   !=================================================================
   function I_ii(mu_sq, vec, I, J)
      ! This function covers those terms from eq. (6.66)
      ! which are not part of the other two fuctions
      ! The result omits the factor
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      integer, optional, intent(in) :: I, J
      complex(ki), dimension(numcs,numcs,2) :: I_ii
      real(ki), dimension(2) :: term
      complex(ki), dimension(numcs,numcs) :: matrix
      real(ki) :: log_s, s_ab
      logical :: flag

      I_ii(:,:,:) = 0.0_ki
      
      s_ab = 2.0_ki * abs(dotproduct(vec(1,:), vec(2,:)))
      log_s = log(mu_sq / s_ab)
      !log_s = 0.0_ki

      ! T1.T2/T1^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 1) .and. (J .eq. 2)
      else
         flag = .true.
      end if

      if (flag) then
              matrix(:,:) = T1T2(:,:)/CA
              term(1) = gammaA
              term(2) = CA
              term(1) = term(1) + log_s * term(2)

              I_ii(:,:,1) = I_ii(:,:,1) + term(1) * matrix(:,:)
              I_ii(:,:,2) = I_ii(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T2.T1/T2^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 2) .and. (J .eq. 1)
      else
         flag = .true.
      end if

      if (flag) then
              matrix(:,:) = T1T2(:,:)/CA
              term(1) = gammaA
              term(2) = CA
              term(1) = term(1) + log_s * term(2)

              I_ii(:,:,1) = I_ii(:,:,1) + term(1) * matrix(:,:)
              I_ii(:,:,2) = I_ii(:,:,2) + term(2) * matrix(:,:)
      end if

   end  function I_ii


   !=================================================================
   function I_ff_qed(mu_sq, vec, I, J)
      ! The result does not include the factor of
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      use pc17_gghh_model
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      integer, optional, intent(in) :: I, J
      integer :: n
      complex(ki), dimension(numcs,numcs,2) :: I_ff_qed
      real(ki), dimension(2) :: term
      complex(ki), dimension(numcs,numcs) :: matrix
      real(ki) :: log_s, s_jk, ncs
      real(ki) :: Q_jk, rho, v_jk
      real(ki) :: m1_2, m2_2, mu1_2, mu2_2
      logical :: flag

      I_ff_qed(:,:,:) = 0.0_ki
      matrix(:,:)=0.0_ki
      do n=1,numcs
       matrix(n,n)=1.0_ki
      enddo
      
      s_jk = 2.0_ki * abs(dotproduct(vec(3,:), vec(4,:)))
      log_s = log(mu_sq / s_jk)
      !log_s = 0.0_ki

      m1_2  = (mdlMh)*(mdlMh)
      m2_2  = (mdlMh)*(mdlMh)
      Q_jk  = s_jk + m1_2 + m2_2
      mu1_2 = m1_2 / Q_jk
      mu2_2 = m2_2 / Q_jk
      v_jk  = sqrt(lambda(1.0_ki, mu1_2, mu2_2)) / (1.0_ki - mu1_2 - mu2_2)
      rho   = sqrt((1.0_ki - v_jk)/(1.0_ki + v_jk))

      ! T3.T4/T3^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 3) .and. (J .eq. 4)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki

              term = V_SING_QED(s_jk, real(mdlMh, ki), real(mdlMh, ki))
              term(1) = (term(1) + log_s * term(2) ) * ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              term(2) = term(2)* ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              I_ff_qed(:,:,1) = I_ff_qed(:,:,1) + term(1) * matrix(:,:)
              I_ff_qed(:,:,2) = I_ff_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T4.T3/T4^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 4) .and. (J .eq. 3)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki

              term = V_SING_QED(s_jk, real(mdlMh, ki), real(mdlMh, ki))
              term(1) = (term(1) + log_s * term(2) ) * ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              term(2) = term(2)* ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              I_ff_qed(:,:,1) = I_ff_qed(:,:,1) + term(1) * matrix(:,:)
              I_ff_qed(:,:,2) = I_ff_qed(:,:,2) + term(2) * matrix(:,:)
      end if

   end  function I_ff_qed

   !=================================================================
   function I_if_qed(mu_sq, vec, I, J)
      !  Again we omit the prefactor
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      use pc17_gghh_model
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      complex(ki), dimension(numcs,numcs,2) :: I_if_qed
      real(ki), dimension(2) :: term
      complex(ki), dimension(numcs,numcs) :: matrix
      integer, optional, intent(in) :: I, J
      integer :: n
      real(ki) :: log_s, s_ja, ncs
      logical :: flag

      I_if_qed(:,:,:) = 0.0_ki
      matrix(:,:)=0.0_ki
      do n=1,numcs
       matrix(n,n)=1.0_ki
      enddo
      

      s_ja = 2.0_ki * abs(dotproduct(vec(1,:), vec(3,:)))
      log_s = log(mu_sq / s_ja)
      !log_s = 0.0_ki

      ! T3.T1/T3^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 3) .and. (J .eq. 1)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T1.T3/T1^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 1) .and. (J .eq. 3)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      s_ja = 2.0_ki * abs(dotproduct(vec(1,:), vec(4,:)))
      log_s = log(mu_sq / s_ja)
      !log_s = 0.0_ki

      ! T4.T1/T4^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 4) .and. (J .eq. 1)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T1.T4/T1^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 1) .and. (J .eq. 4)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      s_ja = 2.0_ki * abs(dotproduct(vec(2,:), vec(3,:)))
      log_s = log(mu_sq / s_ja)
      !log_s = 0.0_ki

      ! T3.T2/T3^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 3) .and. (J .eq. 2)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T2.T3/T2^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 2) .and. (J .eq. 3)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      s_ja = 2.0_ki * abs(dotproduct(vec(2,:), vec(4,:)))
      log_s = log(mu_sq / s_ja)
      !log_s = 0.0_ki

      ! T4.T2/T4^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 4) .and. (J .eq. 2)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T2.T4/T2^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 2) .and. (J .eq. 4)
      else
         flag = .true.
      end if

      if (flag) then
              ncs=1.0_ki
              term = V_SING_QED(s_ja, mdlMh, 0.0_ki)
              term=term*ncs*(0.0_ki)*(0.0_ki/9.0_ki)
              term(1) = term(1) + log_s * term(2)

              I_if_qed(:,:,1) = I_if_qed(:,:,1) + term(1) * matrix(:,:)
              I_if_qed(:,:,2) = I_if_qed(:,:,2) + term(2) * matrix(:,:)
      end if
   end  function I_if_qed




   !=================================================================
   function I_ii_qed(mu_sq, vec, I, J)
      ! The result omits the factor
      ! $-\alpha_s/(2\pi)(4\pi)^\epsilon/\Gamma(1-\epsilon)$
      implicit none
      real(ki), intent(in) :: mu_sq
      real(ki), dimension(num_legs,4), intent(in) :: vec
      integer, optional, intent(in) :: I, J
      integer :: n
      complex(ki), dimension(numcs,numcs,2) :: I_ii_qed
      real(ki), dimension(2) :: term
      complex(ki), dimension(numcs,numcs) :: matrix
      real(ki) :: log_s, s_ab, ncs
      logical :: flag

      I_ii_qed(:,:,:) = 0.0_ki
      matrix(:,:)=0.0_ki
      do n=1,numcs
       matrix(n,n)=1.0_ki
      enddo
      
      s_ab = 2.0_ki * abs(dotproduct(vec(1,:), vec(2,:)))
      log_s = log(mu_sq / s_ab)
      !log_s = 0.0_ki

      ! T1.T2/T1^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 1) .and. (J .eq. 2)
      else
         flag = .true.
      end if

      if (flag) then

              ncs=1.0_ki

              term(1) = ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              term(2) = ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              term(1) = term(1)*(3.0_ki/2.0_ki + log_s )

              I_ii_qed(:,:,1) = I_ii_qed(:,:,1) + term(1) * matrix(:,:)
              I_ii_qed(:,:,2) = I_ii_qed(:,:,2) + term(2) * matrix(:,:)
      end if

      ! T2.T1/T2^2
      if(present(I) .and. present(J)) then
         flag = (I .eq. 2) .and. (J .eq. 1)
      else
         flag = .true.
      end if

      if (flag) then

              ncs=1.0_ki

              term(1) = ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              term(2) = ncs*(0.0_ki)*(0.0_ki)/9.0_ki
              term(1) = term(1)*(3.0_ki/2.0_ki + log_s )

              I_ii_qed(:,:,1) = I_ii_qed(:,:,1) + term(1) * matrix(:,:)
              I_ii_qed(:,:,2) = I_ii_qed(:,:,2) + term(2) * matrix(:,:)
      end if

   end  function I_ii_qed




   function V_SING(s_jk, m_j, m_k)
      implicit none
      real(ki), intent(in) :: s_jk, m_j, m_k
      real(ki), dimension(2) :: V_SING

      real(ki) :: Q_jk, v_jk, rho, mu1_2, mu2_2, m1_2, m2_2

      m1_2  = m_j*m_j
      m2_2  = m_k*m_k

      if (m_j .gt. 0.0_ki) then
              if(m_k .gt. 0.0_ki) then
                      Q_jk  = s_jk + m1_2 + m2_2
                      mu1_2 = m1_2 / Q_jk
                      mu2_2 = m2_2 / Q_jk
                      v_jk  = sqrt(lambda(1.0_ki, mu1_2, mu2_2)) &
                            &      / (1.0_ki - mu1_2 - mu2_2)
                      rho   = sqrt((1.0_ki - v_jk)/(1.0_ki + v_jk))
                      ! (6.20), case 1, both massive
                      V_SING(1) = log(rho)/v_jk
                      V_SING(2) = 0.0_ki
              else
                      ! (6.20), case 2, only m_j massive
                      V_SING(1) = 0.5_ki * log(m1_2/s_jk)
                      V_SING(2) = 0.5_ki
              end if
      else
              if(m_k .gt. 0.0_ki) then
                      ! (6.20), case 2, only m_k massive
                      V_SING(1) = 0.5_ki * log(m2_2/s_jk)
                      V_SING(2) = 0.5_ki
              else
                      ! (6.20), case 3, both massless
                      V_SING(1) = 0.0_ki
                      V_SING(2) = 1.0_ki
              end if
      end if
   end  function V_SING

   function V_SING_QED(s_jk, m_j, m_k)
      implicit none
      real(ki), intent(in) :: s_jk, m_j, m_k
      real(ki), dimension(2) :: V_SING_QED

      real(ki) :: Q_jk, v_jk, rho, mu1_2, mu2_2, m1_2, m2_2

      m1_2  = m_j*m_j
      m2_2  = m_k*m_k

      if (m_j .gt. 0.0_ki) then
               if(m_k .gt. 0.0_ki) then
                      Q_jk  = s_jk + m1_2 + m2_2
                      mu1_2 = m1_2 / Q_jk
                      mu2_2 = m2_2 / Q_jk
                      v_jk  = sqrt(lambda(1.0_ki, mu1_2, mu2_2)) &
                            &      / (1.0_ki - mu1_2 - mu2_2)
                      rho   = sqrt((1.0_ki - v_jk)/(1.0_ki + v_jk))
                      ! (6.20), case 1, both massive
                      V_SING_QED(1) = log(rho)/v_jk
                      V_SING_QED(2) = 0.0_ki
               else
                       V_SING_QED(1) = 0.5_ki * (5.0_ki/2.0_ki+log(m1_2/s_jk))
                       V_SING_QED(2) = 0.5_ki
               end if
      else
              if(m_k .gt. 0.0_ki) then
                      V_SING_QED(1) = 0.5_ki * (5.0_ki/2.0_ki +log(m2_2/s_jk))
                      V_SING_QED(2) = 0.5_ki
              else
                      V_SING_QED(1) = 3.0_ki/2.0_ki
                      V_SING_QED(2) = 1.0_ki
              end if
      end if
   end  function V_SING_QED


   function GAMMA_A()
      ! Equation (6.27)
      implicit none
      real(ki), dimension(2) :: GAMMA_A

      GAMMA_A(1) = gammaA
      GAMMA_A(2) = 0.0_ki
   end  function GAMMA_A

   function GAMMA_F(mq)
      implicit none
      real(ki), intent(in) :: mq
      real(ki), dimension(2) :: GAMMA_F

      if (mq .gt. 0.0_ki) then
              ! (6.29)
              GAMMA_F(1) = CF
              GAMMA_F(2) = 0.0_ki
      else
              ! (6.28)
              GAMMA_F(1) = gammaF
              GAMMA_F(2) = 0.0_ki
      end if
   end  function GAMMA_F
end module pc17_gghh_dipoles
