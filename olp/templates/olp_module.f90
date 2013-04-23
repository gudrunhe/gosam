module     olp_module
   implicit none
   private
   public :: OLP_Start, OLP_EvalSubProcess, OLP_Finalize, OLP_Option

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
           & [%$_%]_PSP_chk_threshold1 => PSP_chk_threshold1, &
           & [%$_%]_PSP_chk_threshold2 => PSP_chk_threshold2, &
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
      integer :: PSP_verbosity, PSP_chk_threshold1, PSP_chk_threshold2
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
      ! PSP_verbosity = [% PSP_verbosity default=2 %]
      ! PSP_chk_threshold1 = [% PSP_chk_threshold1 default=4 %]
      ! PSP_chk_threshold2 = [% PSP_chk_threshold2 default=3 %]
      ! PSP_chk_kfactor = [% PSP_chk_kfactor default=10000.0d0 %][%
      @for subprocesses %]
      ! [%$_%]_PSP_rescue = PSP_rescue
      ! [%$_%]_PSP_verbosity =  PSP_verbosity
      ! [%$_%]_PSP_chk_threshold1 = PSP_chk_threshold1
      ! [%$_%]_PSP_chk_threshold2 = PSP_chk_threshold2
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

   subroutine     OLP_EvalSubProcess(label, momenta, mu, parameters, res) &
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
      real(kind=c_double), dimension(4), intent(out) :: res
   
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

      res(1:3) = alpha_s * one_over_2pi * res(1:3)
   end subroutine OLP_EvalSubProcess

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
      @end @select %]momenta, mu, parameters, res)
      use, intrinsic :: iso_c_binding
      use [% sp.$_ %]_config, only: ki
      use [% sp.$_ %]_model, only: parseline
      use [% cr.$_ %]_matrix, only: samplitude[%
      @if extension golem95 %]
      use [% sp.$_%]_groups, only: tear_down_golem95[%
      @end @if %][%
      @if extension ninja %]
      use ninja_module, only: ninja_clear_cache[%
      @end @if %]
      implicit none[%
      @select count elements cr.channels
      @case 1 %][%
      @else %]
      integer, intent(in) :: h[%
      @end @select %]
      real(kind=c_double), dimension([%
         eval 5 * sp.num_legs %]), intent(in) :: momenta
      real(kind=c_double)[%
      @if internal OLP_CALL_BY_VALUE %], value[%
      @end @if %], intent(in) :: mu
      real(kind=c_double), dimension(10), intent(in) :: parameters
      real(kind=c_double), dimension(4), intent(out) :: res

      real(kind=ki), dimension([% sp.num_legs %],4) :: vecs
      real(kind=ki), dimension(4) :: amp
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

      call samplitude(vecs, mu*mu, amp, ok[%
      @select count elements cr.channels
      @case 1 %][%
      @else %], h[%
      @end @select %])[%
      @if extension golem95 %]
      call tear_down_golem95()[%
      @end @if %][%
      @if extension ninja %]
      call ninja_clear_cache()[%
      @end @if %]

      if (ok) then
         !
      else
         !
      end if

      res(1) = real(amp(4), c_double)
      res(2) = real(amp(3), c_double)
      res(3) = real(amp(2), c_double)
      res(4) = real(amp(1), c_double)
   end subroutine eval[% cr.id %]
   !---#] subroutine eval[% cr.id %] :[%
   @end @for %][%
@end @for %]

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
