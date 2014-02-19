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
      use [%$_%]_matrix, only: [%$_%]_initgolem => initgolem
      use [%$_%]_config, only: [%$_%]_PSP_rescue => PSP_rescue, &
           & [%$_%]_PSP_verbosity => PSP_verbosity, &
           & [%$_%]_PSP_chk_th1 => PSP_chk_th1, &
           & [%$_%]_PSP_chk_th2 => PSP_chk_th2, &
           & [%$_%]_PSP_chk_th3 => PSP_chk_th3, &
           & [%$_%]_PSP_chk_kfactor => PSP_chk_kfactor[%
      @end @for %]
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
      character(len=9) :: kw[%
      @if extension golem95 %]
      integer :: PSP_verbosity, PSP_chk_th1, PSP_chk_th2, PSP_chk_kfactor
      logical :: PSP_rescue[%
      @end @if %]

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
      ! PSP_chk_kfactor = [% PSP_chk_kfactor default=10000.0d0 %][%
      @for subprocesses %]
      ! [%$_%]_PSP_rescue = PSP_rescue
      ! [%$_%]_PSP_verbosity =  PSP_verbosity
      ! [%$_%]_PSP_chk_th1 = PSP_chk_th1
      ! [%$_%]_PSP_chk_th2 = PSP_chk_th2
      ! [%$_%]_PSP_chk_th3 = PSP_chk_th3
      ! [%$_%]_PSP_chk_kfactor = PSP_chk_kfactor[%
      @end @for %][%
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
   use, intrinsic :: iso_c_binding, only: C_CHAR, C_NULL_CHAR[%
   @for subprocesses %][%
       @if is_first %]
   use [%$_%]_version, only: gosamversion, gosamrevision[%
       @end @if %][%
   @end @for %]

   implicit none
   character(kind=c_char), intent(inout), dimension(15)  :: olp_name
   character(kind=c_char), intent(inout), dimension(15)  :: olp_version
   character(kind=c_char), intent(inout), dimension(255) :: message
   character(len=254) :: msg
   character(len=6)   :: rev
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
   write(rev,'(I6)')  gosamrevision

   msg = new_line('C')//'Please cite the following references when using this program:'//&
        &new_line('C')//'Mastrolia:2010nb, Binoth:2008uq, Cullen:2011kv, Cullen:2011ac'

   call strncpy(olp_name, c_char_'GoSam-'//ver1//'.'//ver2//C_NULL_CHAR, &
        len(c_char_'GoSam-'//ver1//'.'//ver2//C_NULL_CHAR,kind=c_size_t))

   call strncpy(olp_version, c_char_'svn rev-'//trim(adjustl(rev))//C_NULL_CHAR, &
        len(c_char_'svn rev-'//trim(adjustl(rev))//C_NULL_CHAR,kind=c_size_t))

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
      use, intrinsic :: iso_c_binding[%
   @for subprocesses %]
      use [%$_%]_model, only: [%$_%]_set_parameter => set_parameter[%
   @end @for %]
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

      l = strlen(variable_name)[%
   @for subprocesses %]
      call [%$_%]_set_parameter(variable_name(1:l),real_part,imag_part,success)
      if(success==0) then ! return immediately on error
          return
      end if[%
   @end @for %]
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

      call OLP_SetParameter("alphaS",parameters(1),0.0d0,succ)

      select case(label)[%
      @for subprocesses prefix=sp. %][%
         @for crossings include-self prefix=cr. %][%
            @select count elements cr.channels
            @case 1 %]
      case([% cr.channels %])
              call eval[% cr.id %](momenta(1:[% eval 5 * sp.num_legs
               %]), mu, parameters, res)[%
            @else %][%
               @for elements cr.channels %]
      case([% $_ %])
              call eval[% cr.id %]([%index%], momenta(1:[% eval 5 * sp.num_legs
              %]), mu, parameters, res)[%
               @end @for %][%
            @end @select %][%
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
      use, intrinsic :: iso_c_binding[%
      @for subprocesses %]
      use [%$_%]_model, only: [%$_%]_parseline => parseline[%
      @end @for %]
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

      l = strlen(line)[%
      @for subprocesses %]
      call [%$_%]_parseline(line(1:l),ios)
      if (ios .ne. 0) then
         stat = 0
         return
      end if[%
      @end @for %]
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
      @end @select %]momenta, mu, parameters, res, acc)
      use, intrinsic :: iso_c_binding
      use [% sp.$_ %]_config, only: ki, PSP_chk_th3
      use [% sp.$_ %]_model, only: parseline
      use [% sp.$_ %]_kinematics, only: boost_to_cms
      use [% cr.$_ %]_matrix, only: samplitude, OLP_spin_correlated_lo2, OLP_color_correlated[%
      @if extension golem95 %]
      use [% sp.$_%]_groups, only: tear_down_golem95[%
      @end @if %][%
      @if extension ninja %]
      use [% sp.$_%]_groups, only: ninja_exit[%
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
      real(kind=ki), dimension([% @if eval cr.amplitudetype ~ "scTree"
      %][% eval 2 * sp.num_legs * sp.num_legs
      %][%@elif eval cr.amplitudetype ~ "ccTree" %][%
                eval ( sp.num_legs * ( sp.num_legs - 1 ) ) // 2 %][%@else%]4[%@end @if
      %]) :: amp
      real(kind=c_double), optional :: acc
      real(kind=ki) :: zero
      integer :: i, prec
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


      vecs(:,1) = real(momenta(1::5),ki)
      vecs(:,2) = real(momenta(2::5),ki)
      vecs(:,3) = real(momenta(3::5),ki)
      vecs(:,4) = real(momenta(4::5),ki)

      call boost_to_cms(vecs)

      [% @if eval cr.amplitudetype ~ "scTree"
      %]call OLP_spin_correlated_lo2(vecs,amp);
      ok=.true.[%
      @else %][%
      @if eval cr.amplitudetype ~ "ccTree" %]
      call OLP_color_correlated(vecs,amp);
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
      @end @if %][%
      @if extension ninja %]
      call ninja_exit()[%
      @end @if %]
      if (ok) then
         !
      else
         !
      end if
      if(present(acc)) then
         acc=10.0_ki**(-prec) ! point accuracy
      else
         if(prec.lt.PSP_chk_th3) then
            ! Give back a Nan so that point is discarded
            zero = log(1.0_ki)
            amp(2)= 1.0_ki/zero
        end if
        acc=1E5_ki ! dummy accuracy which is not used
      end if

      [% @if eval cr.amplitudetype ~ "scTree"
      %]do i=1, size(amp)
        res(i) = real(amp(i), c_double)
      end do
      [%@elif eval cr.amplitudetype ~ "ccTree" %]
      do i=1, size(amp)
        res(i) = real(amp(i), c_double)
      end do[%
      @else%]
      res(1) = real(amp(4), c_double)
      res(2) = real(amp(3), c_double)
      res(3) = real(amp(2), c_double)
      res(4) = real(amp(1), c_double)[%
      @end @if %]

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
      use, intrinsic :: iso_c_binding[%
      @for subprocesses %][%
       @if is_first %]
      use [%$_%]_config , only:ki
      use [%$_%]_model
      use [%$_%]_kinematics, only: Spab3, Spaa [%
      @end @if %] [%
      @end @for %]
      implicit none
      real(kind=c_double), dimension(0:3), intent(in) :: p,q
      real(kind=c_double), dimension(0:7), intent(out) :: eps
      complex(kind=ki), dimension(4) :: eps_complex
      complex(kind=ki), dimension(0:3) :: Sp

      Sp=Spab3(real(q,ki), real(p,ki))

      eps_complex(:)=Sp(:)/Spaa(real(q,ki),real(p,ki))/sqrt2
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

      use, intrinsic :: iso_c_binding[%
      @for subprocesses %]
      use [%$_%]_model, only: [%$_%]_print_parameter => print_parameter[%
      @end @for %]
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
      end if[%
      @for subprocesses %]
      write (27, "(A)") "####### Setup of SubProcess [%$_%] #######"
      call [%$_%]_print_parameter(.true.,27)
      write (27, *)[%
      @end @for%]

      close(27)

   end subroutine OLP_PrintParameter
   !---#] OLP_PrintParameter

   subroutine     read_slha_file(line)[%
   @for subprocesses %]
      use [%$_%]_model, only: [%$_%]_read_slha => read_slha[%
   @end @for %]
      implicit none
      character(len=*), intent(in) :: line
      character(len=512) :: file_name
      integer :: ierr

      call unescape_file_name(line, file_name)
      open(unit=27,file=file_name,status='old',iostat=ierr)
      if(ierr.ne.0) then
         print*, "Could not find SLHA model file"
      else[%
      @for subprocesses %][%
         @if is_first %][%
         @else %]
         rewind(unit=27)[%
         @end @if %]
         call [%$_%]_read_slha(27)[%
      @end @for %]
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
