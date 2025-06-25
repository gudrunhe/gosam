module     olp_module
   use, intrinsic :: iso_c_binding;
   implicit none
   private
   public :: OLP_Start, OLP_EvalSubProcess, OLP_Finalize, OLP_Option
   public :: OLP_EvalSubProcess2, OLP_Polvec, OLP_SetParameter, OLP_Info
   public :: OLP_PrintParameter

contains

   subroutine     OLP_Start(contract_file_name,ierr[%
   @if internal OLP_BADPTSFILE_NUMBERING %],stage,rndseed[%
   @end @if %]) &
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_start[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_Start[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
      use, intrinsic :: iso_c_binding[%
      @for subprocesses %]
      use [%$_%]_matrix, only: [%$_%]_initgolem => initgolem[%
      @end @for %]
      use config, only: PSP_rescue => PSP_rescue, &
           & PSP_verbosity => PSP_verbosity, &[%
      @if generate_tree_diagrams %]
           & PSP_chk_th1 => PSP_chk_th1, &
           & PSP_chk_th2 => PSP_chk_th2, &
           & PSP_chk_th3 => PSP_chk_th3, &
           & PSP_chk_th4 => PSP_chk_th4, &
           & PSP_chk_th5 => PSP_chk_th5, &
           & PSP_chk_kfactor => PSP_chk_kfactor[%
      @else %]
           & PSP_chk_li1 => PSP_chk_li1, &
           & PSP_chk_li2 => PSP_chk_li2, &
           & PSP_chk_li3 => PSP_chk_li3, &
           & PSP_chk_li4 => PSP_chk_li4, &
           & PSP_chk_li5 => PSP_chk_li5, &
           & PSP_chk_kfactor => PSP_chk_kfactor[%
      @end @if %]
      implicit none
      character(kind=c_char,len=1), intent(in) :: contract_file_name
      integer(kind=c_int), intent(out) :: ierr[%
      @if internal OLP_BADPTSFILE_NUMBERING %]
      integer(kind=c_int), intent(in) :: stage, rndseed[%
      @end @if %]
      interface
         function strlen(s) bind(C,name='strlen')
            use, intrinsic :: iso_c_binding
            implicit none
            character(kind=c_char,len=1), intent(in) :: s
            integer(kind=c_int) :: strlen
         end function strlen
      end interface

      integer :: l, ferr
      character(len=128) :: line_buf
      character(len=9) :: kw

      ierr = 1
      l = strlen(contract_file_name)

      open(unit=21, file=contract_file_name(1:l), &
          & status='old', action='read', iostat=ferr)

      if (ferr .ne. 0) then
         write(7,*) "In OLP_Start: ", contract_file_name(1:l), " not found!"
         ierr = -1
      end if

      do while (ferr .eq. 0)
         read(unit=21,fmt='(A128)',iostat=ferr) line_buf
         if (ferr .ne. 0) exit
         line_buf = adjustl(line_buf)
         kw = line_buf(1:9)
         do
            l = scan(kw, "DEFILMO")
            if (l .eq. 0) exit
            kw(l:l) = achar(ichar(kw(l:l)) - ichar('A') + ichar('a'))
         end do
         if (kw .eq. "modelfile") then
            line_buf = adjustl(line_buf(10:128))
            l = scan(line_buf, "|") - 1
            if(l .lt. 1) l = len(line_buf)
            l = len_trim(line_buf(1:l))
            exit
         end if
      end do

      close(unit=21)

      if (ierr .eq. 1) then
         call read_slha_file(line_buf(1:l))
      end if

      ! Uncomment to change rescue system setting on all suprocesses
      ! PSP_rescue = .true.
      ! PSP_verbosity = .false.
      ! PSP_chk_th1 = [% PSP_chk_th1 default=8 %]
      ! PSP_chk_th2 = [% PSP_chk_th2 default=3 %]
      ! PSP_chk_th3 = [% PSP_chk_th3 default=5 %]
      ! PSP_chk_th4 = [% PSP_chk_th4 default=10 %]
      ! PSP_chk_th5 = [% PSP_chk_th5 default=7 %]
      ! PSP_chk_kfactor = [% PSP_chk_kfactor default=10000.0d0 %][%
      @if internal OLP_BADPTSFILE_NUMBERING %]
      if(stage.lt.0) then[%
         @for subprocesses %]
         call [%$_%]_initgolem([%
         @if is_first %].true.[% @else %].false.[%
         @end @if %])[%
         @end @for %]
      else[%
         @for subprocesses %]
         call [%$_%]_initgolem([%
         @if is_first %].true.[% @else %].false.[%
         @end @if %],stage,rndseed)[%
         @end @for %]
      end if[%
      @else %][%
      @for subprocesses %]
      call [%$_%]_initgolem([%
         @if is_first %].true.[% @else %].false.[%
         @end @if %])[%
      @end @for %][%
      @end @if %]

   end subroutine OLP_Start

   subroutine OLP_Info(olp_name, olp_version, message)&
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_info[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_Info[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
   use, intrinsic :: iso_c_binding, only: C_CHAR, C_NULL_CHAR
   use version, only: gosamversion, gosamrevision

   implicit none
   character(kind=c_char), intent(inout), dimension(20)  :: olp_name
   character(kind=c_char), intent(inout), dimension(20)  :: olp_version
   character(kind=c_char), intent(inout), dimension(255) :: message
   character(len=254) :: msg
   character(len=7)   :: rev
   character(len=1)   :: ver1, ver2

   interface
     subroutine strncpy(dest, src, n) bind(C)
       import
       character(kind=c_char),  intent(out) :: dest(*)
       character(kind=c_char),  intent(in)  :: src(*)
       integer(c_size_t), value, intent(in) :: n
     end subroutine strncpy
   end interface

   write(ver1,'(I1)') gosamversion(1)
   write(ver2,'(I1)') gosamversion(2)
   write(rev,'(Z7)')  gosamrevision

   msg = new_line('C')//'Please cite the following references when using this program:'//&
        &new_line('C')//'Peraro:2014cba, Mastrolia:2012bu, '//&
        &'Mastrolia:2010nb, Guillet:2013msa, Cullen:2011kv, Cullen:2014yla'

   call strncpy(olp_name, c_char_'GoSam-'//ver1//'.'//ver2//C_NULL_CHAR, &
        len(c_char_'GoSam-'//ver1//'.'//ver2//C_NULL_CHAR,kind=c_size_t))

   call strncpy(olp_version, c_char_'git rev-'//trim(adjustl(rev))//C_NULL_CHAR, &
        len(c_char_'git rev-'//trim(adjustl(rev))//C_NULL_CHAR,kind=c_size_t))

   call strncpy(message, c_char_'GoSam:'//trim(adjustl(msg))//C_NULL_CHAR, &
        len(c_char_'GoSam:'//trim(adjustl(msg))//C_NULL_CHAR,kind=c_size_t))

   end subroutine OLP_Info


   subroutine OLP_SetParameter(variable_name, real_part, imag_part, success)&
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_setparameter[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_SetParameter[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
      use, intrinsic :: iso_c_binding
      use model, only: set_parameter => set_parameter[%
      @if extension quadruple %]
      use model_qp, only: set_parameter_qp => set_parameter[%
      @end @if %]
      implicit none
      character(kind=c_char,len=1), intent(in) :: variable_name
      real(kind=c_double), intent(in) :: real_part, imag_part
      integer(kind=c_int), intent(out) :: success

      interface
         function strlen(s) bind(C,name='strlen')
            use, intrinsic :: iso_c_binding
            implicit none
            character(kind=c_char,len=1), intent(in) :: s
            integer(kind=c_int) :: strlen
         end function strlen
      end interface

      integer :: l;

      l = strlen(variable_name)
      call set_parameter(variable_name(1:l),real_part,imag_part,success)[%
      @if extension quadruple %]
      call set_parameter_qp(variable_name(1:l),real_part,imag_part,success)[%
      @end @if %]
      if(success==0) then ! return immediately on error
          return
      end if
   end subroutine


   ! BLHA1 interface
   subroutine     OLP_EvalSubProcess(label, momenta, mu,  parameters, res) &
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_evalsubprocess[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_EvalSubProcess[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
      use, intrinsic :: iso_c_binding
      implicit none
      integer(kind=c_int)[%
      @if internal OLP_CALL_BY_VALUE %], value[%
      @end @if %], intent(in) :: label
      real(kind=c_double)[%
      @if internal OLP_CALL_BY_VALUE %], value[%
      @end @if %], intent(in) :: mu
      real(kind=c_double), dimension(50), intent(in) :: momenta
      real(kind=c_double), dimension(10), intent(in) :: parameters
      real(kind=c_double), dimension(60), intent(out) :: res
      integer(kind=c_int) :: succ
      real(kind=c_double) :: alpha_s
      real(kind=c_double), parameter :: one_over_2pi = 0.15915494309189533577d0

      alpha_s = parameters(1)

      select case(label)[%
      @for subprocesses prefix=sp. %][%
         @for crossings include-self prefix=cr. %][%
            @select count elements cr.channels
            @case 1 %]
      case([% cr.channels %])
              call eval[% cr.id %](momenta(1:[% eval 5 * sp.num_legs
               %]), mu, parameters, res, blha1_mode=.true.)[%
            @else %][%
               @for elements cr.channels %]
      case([% $_ %])
              call eval[% cr.id %]([%index%], momenta(1:[% eval 5 * sp.num_legs
              %]), mu, parameters, res, blha1_mode=.true.)[%
               @end @for %][%
            @end @select %][%
         @if eval ( cr.amplitudetype .eq. "scTree" .or. cr.amplitudetype .eq. "scLoop" )
         %][% @elif eval ( cr.amplitudetype .eq. "ccTree" .or. cr.amplitudetype .eq. "ccLoop" )
         %][% @else %]
              res(1:3) = alpha_s * one_over_2pi * res(1:3)[%
         @end @if%][%
         @end @for %][%
      @end @for %]
      case default
         res(:) = 0.0d0
      end select

   end subroutine OLP_EvalSubProcess

   ! BLHA2 interface
   subroutine     OLP_EvalSubProcess2(label, momenta, mu, res, acc) &
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_evalsubprocess2[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_EvalSubProcess2[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
      use, intrinsic :: iso_c_binding
      implicit none
      integer(kind=c_int), intent(in) :: label
      real(kind=c_double), intent(in) :: mu
      real(kind=c_double), dimension(50), intent(in) :: momenta
      real(kind=c_double), dimension(60), intent(out) :: res
      real(kind=c_double), intent(out) :: acc

      real(kind=c_double), dimension(10) :: parameters

      real(kind=c_double), parameter :: one_over_2pi = 0.15915494309189533577d0

      select case(label)[%
      @for subprocesses prefix=sp. %][%
         @for crossings include-self prefix=cr. %][%
            @select count elements cr.channels
            @case 1 %]
      case([% cr.channels %])
              call eval[% cr.id %](momenta(1:[% eval 5 * sp.num_legs
               %]), mu, parameters, res, acc)[%
            @else %][%
               @for elements cr.channels %]
      case([% $_ %])
              call eval[% cr.id %]([%index%], momenta(1:[% eval 5 * sp.num_legs
              %]), mu, parameters, res, acc)[%
               @end @for %][%
            @end @select %][%
         @end @for %][%
      @end @for %]
      case default
         res(:) = 0.0d0
      end select
   end subroutine OLP_EvalSubProcess2

   subroutine     OLP_Finalize() &
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_finalize[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_Finalize[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
      use, intrinsic :: iso_c_binding[%
      @for subprocesses %]
      use [%$_%]_matrix, only: [%$_%]_exitgolem => exitgolem[%
      @end @for %]
      implicit none[%
      @for subprocesses %]
      call [%$_%]_exitgolem([%
      @if is_last %].true.[% @else %].false.[%
      @end @if %])[%
      @end @for %]
   end subroutine OLP_Finalize

   subroutine     OLP_Option(line,stat) &
   & bind(C,name="[%
   @if internal OLP_TO_LOWER %][%
      olp.process_name asprefix=\_ convert=lower %]olp_option[%
   @else %][%
      olp.process_name asprefix=\_ %]OLP_Option[%
   @end @if %][%
   @if internal OLP_TRAILING_UNDERSCORE %]_[%
   @end @if %]")
      use, intrinsic :: iso_c_binding
      use model, only: parseline => parseline[%
      @if extension quadruple %]
      use model_qp, only: parseline_qp => parseline[%
      @end @if %]
      implicit none
      character(kind=c_char,len=1), intent(in) :: line
      integer(kind=c_int), intent(out) :: stat
      integer :: l, ios

      interface
         function strlen(s) bind(C,name='strlen')
            use, intrinsic :: iso_c_binding
            implicit none
            character(kind=c_char,len=1), intent(in) :: s
            integer(kind=c_int) :: strlen
         end function strlen
      end interface

      l = strlen(line)
      call parseline(line(1:l),ios)[%
      @if extension quadruple %]
      call parseline_qp(line(1:l),ios)[%
      @end @if %]
      if (ios .ne. 0) then
         stat = 0
         return
      end if
      stat = 1
   end subroutine OLP_Option[%
      @select olp.parameters default=NONE
      @case NONE %]
   !---#[ init_event_parameters :
   subroutine     init_event_parameters(sp, parameters)
      use, intrinsic :: iso_c_binding
      implicit none
      integer, intent(in) :: sp
      real(kind=c_double), dimension(10), intent(in) :: parameters
      !
      ! User hook for propagating scale dependent parameters to the
      ! model parameters in the subprocesses.
      !
      ! sp specifies the subprocess
      !
   end subroutine init_event_parameters
   !---#] init_event_parameters :[%
      @end @select %]
[%
@for subprocesses prefix=sp. %][%
   @for crossings include-self prefix=cr. %]
   !---#[ subroutine eval[% cr.id %] :
   subroutine     eval[% cr.id %]([%
      @select count elements cr.channels
      @case 1 %][%
      @else %]h, [%
      @end @select %]momenta, mu, parameters, res, acc, blha1_mode)
      use, intrinsic :: iso_c_binding
      use config, only: ki, [% @if generate_tree_diagrams %]PSP_chk_th3[% @else %]PSP_chk_li3[% @end @if %], nlo_prefactors, PSP_check
      use model, only: parseline[%
            @if eval olp.mc.name ~ "amcatnlo" %], gs [% @end @if %]
      use [% sp.$_ %]_kinematics, only: boost_to_cms
      use [% cr.$_ %]_matrix, only: samplitude, OLP_spin_correlated_lo2, OLP_color_correlated, &
           & spin_correlated_lo2_whizard [%
      @if extension golem95 %]
      use [% sp.$_%]_groups, only: tear_down_golem95[%
      @end @if %][%
      @if extension ninja %]
      use [% sp.$_%]_groups, only: ninja_exit[%
      @if extension quadruple %], quadninja_exit[%
      @end @if %][%
      @end @if %]

      implicit none[%
      @select count elements cr.channels
      @case 1 %][%
      @else %]
      integer, intent(in) :: h[%
      @end @select %]
      real(kind=c_double), dimension([%
         eval 5 * sp.num_legs %]), intent(in) :: momenta
      real(kind=c_double), intent(in) :: mu
      real(kind=c_double), dimension(10), intent(in) :: parameters
      real(kind=c_double), dimension(60), intent(out) :: res

      real(kind=ki), dimension([% sp.num_legs %],4) :: vecs
      real(kind=ki), dimension([% @if eval ( cr.amplitudetype .eq. "scTree" .or. cr.amplitudetype .eq. "scLoop" )
      %][% eval 2 * sp.num_legs * sp.num_legs
      %][%@elif eval ( cr.amplitudetype .eq. "ccTree"  .or. cr.amplitudetype .eq. "ccLoop" )
      %][% eval ( sp.num_legs * ( sp.num_legs - 1 ) ) // 2
      %][%@elif eval ( cr.amplitudetype .eq. "scTree2" )
      %][% sp.num_legs %],4,4[%
      @else%]4[%@end @if
      %]) :: amp
      real(kind=c_double), optional :: acc
      logical, optional :: blha1_mode
      real(kind=ki) :: zero[%
      @if eval olp.mc.name ~ "amcatnlo" %]
      real(kind=ki), parameter :: pi = 3.14159265358979323846264&
           &3383279502884197169399375105820974944592307816406286209_ki[%
      @end @if %]
      integer :: i, prec, orig_nlo_prefactors[%
      @if eval ( cr.amplitudetype .eq. "scTree2" )
      %], iem[% @end @if
      %]
      logical :: ok[%
      @select olp.parameters default=NONE
      @case NONE %]

      call init_event_parameters([% cr.id %], parameters)[%
      @else %]
      character(len=255) :: buffer
      integer :: ierr

      !---#[ receive parameters from argument list:[%
         @for elements olp.parameters shift=1 %]
      write(buffer, '(A[% count $_ %],A1,E48.32)') "[% $_ %]", "=", parameters([% index %])
      call parseline(buffer, ierr)
      if(ierr.ne.0) then
         amp(1) = -1.0_c_double
         return
      end if[%
         @end @for %]
      !---#] receive parameters from argument list:[%
      @end @select %]

      if(present(blha1_mode)) then
         if(blha1_mode) then
            ! save nlo_prefactors and restore later
            orig_nlo_prefactors=nlo_prefactors
            nlo_prefactors=0[%
            @if eval olp.mc.name ~ "amcatnlo" %]
            ! compute g_s from alpha_s for aMC@NLO
            gs = 2.0_ki*sqrt(pi)*sqrt(parameters(1))[%
            @end @if %]
         end if
     end if

      vecs(:,1) = real(momenta(1::5),ki)
      vecs(:,2) = real(momenta(2::5),ki)
      vecs(:,3) = real(momenta(3::5),ki)
      vecs(:,4) = real(momenta(4::5),ki)

      [% @if eval ( sp.num_in .eq. 2 .and. cr.amplitudetype .ne. "scTree2" )
      %]call boost_to_cms(vecs)[%
      @else
      %]! For whizard we need the spin correlated tree in the lab frame,
      ! hence no boost to cms[%
      @end @if %]

      [% @if eval ( cr.amplitudetype .eq. "scTree" .or. cr.amplitudetype .eq. "scLoop" ) %]
      call OLP_spin_correlated_lo2(vecs,amp);
      ok=.true.[%
      @elif eval ( cr.amplitudetype .eq. "ccTree"  .or. cr.amplitudetype .eq. "ccLoop"  ) %]
      call OLP_color_correlated(vecs,amp);
      ok=.true.[%
      @elif eval ( cr.amplitudetype .eq. "scTree2"  ) %]
      call spin_correlated_lo2_whizard(vecs,amp);
      ok=.true.[%
      @else
      %]call samplitude(vecs, real(mu,ki)*real(mu,ki), amp, prec, ok[%
      @select count elements cr.channels
      @case 1 %][%
      @else %], h[%
      @end @select %])[%@end @if %][%
      @if extension golem95 %]
      call tear_down_golem95()[%
      @end @if %][%
      @if extension ninja %]
      call ninja_exit()[%
      @if extension quadruple %]
      call quadninja_exit()[%
      @end @if %][%
      @end @if %]
      if (ok) then
         !
      else
         !
      end if
      if(present(acc)) then
         acc=10.0_ki**(-prec) ! point accuracy
      else
         if(prec.lt.[% @if generate_tree_diagrams %]PSP_chk_th3[% @else %]PSP_chk_li3[% @end @if %] .and. PSP_check) then
            ! Give back a Nan so that point is discarded
            zero = log(1.0_ki)[%
            @if eval ( cr.amplitudetype .eq. "scTree2" )%]
            ! TODO: How to handle this case for scTree2?[%
            @else%]
            amp(2)= 1.0_ki/zero[%
            @if eval olp.mc.name ~ "amcatnlo" %]
            ! aMC@NLO cannot handle Nan's
            amp(2)= 0.0_ki[%
            @end @if %][%
            @end @if %]
        end if
        ! Cannot be assigned if present(acc)=F --> commented out!
        ! acc=1E5_ki ! dummy accuracy which is not used
      end if

      [% @if eval ( cr.amplitudetype .eq. "scTree" .or. cr.amplitudetype .eq. "scLoop" )%]
      do i=1, size(amp)
        res(i) = real(amp(i), c_double)
      end do
      [%@elif eval ( cr.amplitudetype .eq. "ccTree"  .or. cr.amplitudetype .eq. "ccLoop" )%]
      do i=1, size(amp)
        res(i) = real(amp(i), c_double)
      end do
      [%@elif eval ( cr.amplitudetype .eq. "scTree2" )%]
      ! TODO:
      ! How to deal with the different emitters?
      ! Is it necessary to pass a large array with mostly vanishing entries?
      do iem=1,[% sp.num_legs %]
         if (iem.gt.10) then
            print *, "WARNING: scTree2 supports only up to 10 emitters!"
            print *, "ToDo: Make this an proper exception..."
         end if
         ! Whizard convention
         res(6*(iem-1)+1) = real(amp(iem,2,2), c_double)
         res(6*(iem-1)+3) = real(amp(iem,3,3), c_double)
         res(6*(iem-1)+6) = real(amp(iem,4,4), c_double)
         if (iem.le.2) then
            res(6*(iem-1)+2) = -real(amp(iem,2,3), c_double)
            res(6*(iem-1)+4) = -real(amp(iem,2,4), c_double)
            res(6*(iem-1)+5) = -real(amp(iem,3,4), c_double)
         else
            res(6*(iem-1)+2) = real(amp(iem,2,3), c_double)
            res(6*(iem-1)+4) = real(amp(iem,2,4), c_double)
            res(6*(iem-1)+5) = real(amp(iem,3,4), c_double)
         end if
      end do
      [%@else%]
      res(1) = real(amp(4), c_double)
      res(2) = real(amp(3), c_double)
      res(3) = real(amp(2), c_double)
      res(4) = real(amp(1), c_double)[%
      @end @if %]

      if(present(blha1_mode)) then
         if(blha1_mode) then
            ! restore nlo_prefactors
            nlo_prefactors = orig_nlo_prefactors
         end if
     end if

   end subroutine eval[% cr.id %]
   !---#] subroutine eval[% cr.id %] :[%
   @end @for %][%
@end @for %]

   !---#[ OLP Polarization vector:
   subroutine OLP_Polvec(p,q,eps) &
       & bind(C,name="[%
       @if internal OLP_TO_LOWER %][%
          olp.process_name asprefix=\_ convert=lower %]olp_polvec[%
       @else %][%
          olp.process_name asprefix=\_ %]OLP_Polvec[%
       @end @if %][%
       @if internal OLP_TRAILING_UNDERSCORE %]_[%
       @end @if %]")
      use, intrinsic :: iso_c_binding
      use config , only:ki
      use model[%
      @for subprocesses %][%
       @if is_first %]
      use [%$_%]_kinematics, only: Spab3, Spaa [%
      @end @if %] [%
      @end @for %]
      implicit none
      real(kind=c_double), dimension(0:3), intent(in) :: p,q
      real(kind=c_double), dimension(0:7), intent(out) :: eps
      complex(kind=ki), dimension(4) :: eps_complex

      eps_complex(:)=Spab3(real(q,ki), real(p,ki))/Spaa(real(q,ki),real(p,ki))/sqrt2
      eps(0)=real(eps_complex(1),c_double)
      eps(1)=real(aimag(eps_complex(1)),c_double)
      eps(2)=real(eps_complex(2),c_double)
      eps(3)=real(aimag(eps_complex(2)),c_double)
      eps(4)=real(eps_complex(3),c_double)
      eps(5)=real(aimag(eps_complex(3)),c_double)
      eps(6)=real(eps_complex(4),c_double)
      eps(7)=real(aimag(eps_complex(4)),c_double)

   end subroutine OLP_Polvec
   !---#] OLP Polarization vector:

   !---#[ OLP_PrintParameter
   subroutine OLP_PrintParameter(filename) &
       & bind(C,name="[%
       @if internal OLP_TO_LOWER %][%
          olp.process_name asprefix=\_ convert=lower %]olp_printparameter[%
       @else %][%
          olp.process_name asprefix=\_ %]OLP_PrintParameter[%
       @end @if %][%
       @if internal OLP_TRAILING_UNDERSCORE %]_[%
       @end @if %]")

      use, intrinsic :: iso_c_binding
      use model, only: print_parameter => print_parameter
      implicit none
      character(kind=c_char,len=1), intent(in) :: filename
      integer :: ierr, l
      logical :: exists

      interface
         function strlen(s) bind(C,name='strlen')
            use, intrinsic :: iso_c_binding
            implicit none
            character(kind=c_char,len=1), intent(in) :: s
            integer(kind=c_int) :: strlen
         end function strlen
      end interface

      l = strlen(filename)

      inquire(file=filename(1:l), exist=exists)
      if (exists) then
         open(unit=27,file=filename(1:l),status="old", position="append", action="write",iostat=ierr)
      else
         open(unit=27,file=filename(1:l),status="new",iostat=ierr)
      end if
      if (ierr .ne. 0) then
         write(7,*) "OLP_PrintParameter: Could not open/create:", filename(1:l), "!"
         ierr = -1
      end if
      write (27, "(A)") "####### Setup of SubProcess #######"
      call print_parameter(.true.,27)
      write (27, *)

      close(27)

   end subroutine OLP_PrintParameter
   !---#] OLP_PrintParameter

   subroutine     read_slha_file(line)
      use model, only: read_slha => read_slha[%
      @if extension quadruple %]
      use model_qp, only: read_slha_qp => read_slha[%
      @end @if %]
      implicit none
      character(len=*), intent(in) :: line
      character(len=512) :: file_name
      integer :: ierr

      call unescape_file_name(line, file_name)
      open(unit=27,file=file_name,status='old',iostat=ierr)
      if(ierr.ne.0) then
         print*, "Could not find SLHA model file"
      else
         call read_slha(27)[%
         @if extension quadruple %]
         call read_slha_qp(27)[%
         @end @if %]
         close(27)
      end if
   end subroutine read_slha_file

   subroutine     unescape_file_name(source, dest)
      implicit none
      character(len=*), intent(in) :: source
      character(len=512), intent(out) :: dest
      integer :: is, id, l, hex, hexdigit, hexpos
      character(len=512) :: buf
      logical :: special

      is = scan(source, "|")

      if (is > 1) then
         buf = trim(source(1:is-1))
      else
         buf = trim(source)
      end if

      l = len(buf)
      id = 1
      special = .false.
      hexpos = 0
      if (buf(1:1) .eq. '"') then
         ! double quoted string
         do is = 2, l - 1
            if (special) then
               ! after a backslash or in \x.. escape
               if (hexpos == 1 .or. hexpos == 2) then
                  ! interpret hex digit
                  if ("0" .le. buf(is:is) .and. buf(is:is) .le. "9") then
                     hexdigit = ichar(buf(is:is)) - ichar("0")
                  elseif ("A" .le. buf(is:is) .and. buf(is:is) .le. "F") then
                     hexdigit = ichar(buf(is:is)) - ichar("A") + 10
                  elseif ("a" .le. buf(is:is) .and. buf(is:is) .le. "f") then
                     hexdigit = ichar(buf(is:is)) - ichar("a") + 10
                  else
                     print*, "Invalid hex escape sequence in file name"
                     stop
                  end if

                  if (hexpos == 1) then
                     hex = 16 * hexdigit
                     hexpos = 2
                  else
                     hex = hex + hexdigit
                     hexpos = 0
                     special = .false.
                     dest(id:id) = achar(hex)
                     id = id + 1
                  end if
               elseif (buf(is:is) .eq. "n") then
                  dest(id:id) = achar(10)
                  id = id + 1
                  special = .false.
               elseif (buf(is:is) .eq. "r") then
                  dest(id:id) = achar(13)
                  id = id + 1
                  special = .false.
               elseif (buf(is:is) .eq. "f") then
                  dest(id:id) = achar(12)
                  id = id + 1
                  special = .false.
               elseif (buf(is:is) .eq. "t") then
                  dest(id:id) = achar(9)
                  id = id + 1
                  special = .false.
               elseif (buf(is:is) .eq. "x") then
                  hexpos = 1
               else
                  dest(id:id) = buf(is:is)
                  id = id + 1
                  special = .false.
               end if
            else
               if(buf(is:is) .eq. "\") then
                  special = .true.
               else
                  dest(id:id) = source(is:is)
                  id = id + 1
               end if
            end if
         end do
      elseif (buf(1:1) .eq. '"') then
         ! single quoted string
         do is = 2, l - 1
            if (special) then
               dest(id:id) = buf(is:is)
               id = id + 1
               special = .false.
            elseif (buf(is:is) .eq. "'") then
               special = .true.
            else
               dest(id:id) = buf(is:is)
               id = id + 1
            end if
         end do
      else
         ! assume backslash escaped string
         do is = 1, l
            if (special) then
               dest(id:id) = buf(is:is)
               id = id + 1
               special = .false.
            elseif (buf(is:is) .eq. "\") then
               special = .true.
            else
               dest(id:id) = buf(is:is)
               id = id + 1
            end if
         end do
      end if
   end subroutine unescape_file_name
end module olp_module
