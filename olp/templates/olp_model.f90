%=$[$ ' vim:syntax=golem
$]module olp_model
   ! Model parameters for the model: [$ model $]
   use olp_config, only: ki[$
@if extension samurai $], &
   & samurai_scalar, samurai_verbosity, samurai_test, &
   & samurai_group_numerators, samurai_istop[$
@end @if $], &
   & renormalisation, reduction_interoperation, deltaOS, &
   & nlo_prefactors[$ 
@select model @case sm smdiag $][$ 
@select model.options @case ewchoose $], ewchoice[$
@end @select$][$@end @select$]
   implicit none

   private :: ki[$
@if extension samurai $]
   private :: samurai_scalar, samurai_verbosity, samurai_test
   private :: samurai_group_numerators, samurai_istop[$
@end @if $]
   private :: renormalisation, reduction_interoperation, deltaOS
   private :: nlo_prefactors

   real(ki), parameter :: sqrt2 = &
      &1.414213562373095048801688724209698078&
      &5696718753769480731766797379_ki
   real(ki), parameter :: sqrt3 = &
      &1.732050807568877293527446341505872366&
      &9428052538103806280558069795_ki
   [$
      @for parameters $]
   [$    @select type
         @case R $]real(ki) :: [$$_$] = [$
               real convert=float format=%24.15f_ki $][$
         @case C $]complex(ki) :: [$$_$] = ([$
               real convert=float format=%24.15f_ki $], [$
               imag convert=float format=%24.15f_ki $])[$
         @case RP $]real(ki), parameter :: [$$_$] = [$
               real convert=float format=%24.15f_ki $][$
         @case CP $]complex(ki), parameter :: [$$_
                          $] = ([$
               real convert=float format=%24.15f_ki $], [$
               imag convert=float format=%24.15f_ki $])[$
         @end @select type $][$
      @end @for parameters $][$
      @for functions $]
   [$    @select type
         @case R $]real(ki) :: [$$_$][$
         @case C $]complex(ki) :: [$$_$][$
         @end @select type $][$
      @end @for functions $]

   integer, parameter, private :: line_length = [$buffer_length$][$
   ' what is our longest extra name ?
   ' 0   0    1    1    2    2
   ' 1---5----0----5----0----5
   ' samurai_group_numerators
   ' reduction_interoperation
   ' samurai_verbatim
   ' renormalisation
   ' samurai_scalar
   ' samurai_test
   '
   ' ==> the longest is 24
   $]
   integer, parameter, private :: name_length = max([$name_length$],24)
   character(len=name_length), dimension([$ count R C $]) :: names = (/& [$
   @for parameters R C  $]
      & "[$ $_ $][$ alignment $]"[$
         @if is_last $]/)[$ @else $], &[$ @end @if $][$
   @end @for parse_names $]
   character(len=1), dimension([$ len_comment_chars $]) :: cc = (/[$
   @for comment_chars $]'[$$_$]'[$ @if is_last $]/)[$ @else $], [$
   @end @if $][$
   @end @for$]

   private :: digit, parsereal, names, cc

contains

   function     digit(ch, lnr) result(d)
      implicit none
      character(len=1), intent(in) :: ch
      integer, intent(in) :: lnr
      integer :: d
      d = -1
      select case(ch)[$
         @for repeat 10 $]
         case('[$$_$]')
            d = [$$_$][$
         @end @for $]
         case default
            write(*,'(A21,1x,I5)') 'invalid digit in line', lnr
         end select
   end function digit

   function     parsereal(str, ierr, lnr) result(num)
      implicit none
      character(len=*), intent(in) :: str
      integer, intent(out) :: ierr
      integer, intent(in) :: lnr
      integer, dimension(0:3,0:4), parameter :: DFA = &
      & reshape( (/1,  1,  2, -1,   & ! state = 0
      &            1, -1,  2,  3,   & ! state = 1
      &            2, -1, -1,  3,   & ! state = 2
      &            4,  4, -1, -1,   & ! state = 3
      &            4, -1, -1, -1/), (/4, 5/))
      real(ki) :: num
      integer :: i, expo, ofs, state, cclass, d, s1, s2
      num = 0.0_ki
      expo = 0
      state = 0
      ofs = 0
      s1 = 1
      s2 = 1
      d = -1
      cclass = -1
      do i=1,len(str)
         select case(str(i:i))
         case('_', '''', ' ')
            cycle
         case('+', '-')
            cclass = 1
         case('.')
            cclass = 2
         case('E', 'e')
            cclass = 3
         case default
            cclass = 0
            d = digit(str(i:i), lnr)
            if (d .eq. -1) then
               ierr = 1
               return
            end if
         end select
         if (cclass .eq. 0) then
            select case(state)
            case(0, 1)
               num = 10.0_ki * num + d
            case(2)
               num = 10.0_ki * num + d
               ofs = ofs - 1
            case(4)
               expo = 10 * expo + d
            end select
         elseif ((cclass .eq. 1) .and. (str(i:i) .eq. '-')) then
            if (state .eq. 0) then
               s1 = -1
            else
               s2 = -1
            endif
         end if
         ! Advance in the DFA
         state = DFA(cclass, state)
         if (state < 0) then
            write(*,'(A21,1x,A1,1x,A7,I5)') 'invalid position for', &
            & str(i:i), 'in line', lnr
            ierr = 1
            return
         end if
      end do
      num = s1 * num * 10.0_ki**(ofs + s2 * expo)
      ierr = 0
   end function parsereal

   subroutine     parseline(line,stat,line_number)
      implicit none
      character(len=*), intent(in) :: line
      integer, intent(out) :: stat
      integer, intent(in), optional :: line_number

      character(len=line_length) :: rvalue, ivalue, value
      character(len=name_length) :: name
      real(ki) :: re, im
      integer :: idx, icomma, idx1, idx2, lnr, nidx, ierr, pdg

      if(present(line_number)) then
         lnr = line_number
      else
         lnr = 0
      end if

      idx = scan(line, '=', .false.)
      if (idx .eq. 0) then
         if(present(line_number)) then
            write(*,'(A13,1x,I5)') 'error at line', line_number
         else
            write(*,'(A18)') 'error in parseline'
         end if
         stat = 1
         return
      end if
      name = adjustl(line(1:idx-1))
      value = adjustl(line(idx+1:len(line)))
      idx = scan(value, ',', .false.)
      
      if (name .eq. "renormalisation") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         renormalisation = int(re)
      elseif (name .eq. "nlo_prefactors") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         nlo_prefactors = int(re)
      elseif (name .eq. "deltaOS") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         deltaOS = int(re)
      elseif (name .eq. "reduction_interoperation") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         reduction_interoperation = int(re)[$
@if extension samurai $]
      elseif (name .eq. "samurai_scalar") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         samurai_scalar = int(re)
      elseif (name .eq. "samurai_verbosity") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         samurai_verbosity = int(re)
      elseif (name .eq. "samurai_test") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         samurai_test = int(re)
      elseif (name .eq. "samurai_istop") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         samurai_istop = int(re)
      elseif (name .eq. "samurai_group_numerators") then
         re = parsereal(value, ierr, lnr)
         if (ierr .ne. 0) then
            stat = 1
            return
         end if
         samurai_group_numerators = (int(re).ne.0)[$
@end @if $]
      elseif (any(names .eq. name)) then
         do nidx=1,size(names)
            if (names(nidx) .eq. name) exit
         end do
         if (idx .gt. 0) then
            rvalue = value(1:idx-1)
            ivalue = value(idx+1:len(value))
            re = parsereal(rvalue, ierr, lnr)
            if (ierr .ne. 0) then
               stat = 1
               return
            end if
            im = parsereal(ivalue, ierr, lnr)
            if (ierr .ne. 0) then
               stat = 1
               return
            end if
         else
            re = parsereal(value, ierr, lnr)
            if (ierr .ne. 0) then
               stat = 1
               return
            end if
            im = 0.0_ki
         end if
         select case (nidx)[$
         @for parameters R C $]
         case([$index$])
            [$ $_ $] = [$
         @select type
         @case C$]cmplx(re, im, ki)[$
         @else $]re[$
         @end @select $][$
         @end @for $]
         end select[$
@if has_slha_locations $][$
   @for slha_blocks lower dimension=1 $]
      elseif (name(1:[$ eval 1 + .len. $_ $]).eq."[$ $_ $](") then
         idx = scan(name, ')', .false.)
         if (idx.eq.0) then
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         endif
         read(name([$ eval 2 + .len. $_ $]:idx-1),*, iostat=ierr) pdg
         if (ierr.ne.0) then
            write(*,*) "Not an integer:", name([$
                    eval 2 + .len. $_ $]:idx-1)
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         end if
         select case(pdg)[$
      @for slha_entries $]
            case([$index$])
               [$ $_ $] = parsereal(value, ierr, lnr)[$
      @end @for $]
            case default
               write(*,'(A20,1x,I10)') "Cannot set [$ $_ $] for code:", pdg
               stat = 1
               return
         end select[$
   @end @for $][$
   @for slha_blocks lower dimension=2 $]
      elseif (name(1:[$ eval 1 + .len. $_ $]).eq."[$ $_ $](") then
         idx = scan(name, ')', .false.)
         if (idx.eq.0) then
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         endif
         icomma = scan(name(1:idx), ',', .false.)
         if (icomma.eq.0) then
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         endif
         read(name([$ eval 2 + .len. $_ $]:icomma-1),*, iostat=ierr) idx1
         if (ierr.ne.0) then
            write(*,*) "Not an integer:", name([$
                    eval 2 + .len. $_ $]:icomma-1)
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         end if
         read(name(icomma+1:idx-1),*, iostat=ierr) idx2
         if (ierr.ne.0) then
            write(*,*) "Not an integer:", name(icomma+1:idx-1)
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         end if[$
      @for slha_entries index=index1 $]
         [$
         @if is_first $][$ @else $]else[$
         @end @if$]if(idx1.eq.[$index1$]) then[$
         @for slha_entries index=index2 $]
            [$
            @if is_first $][$ @else $]else[$
            @end @if $]if(idx2.eq.[$index2$]) then
               [$ $_ $] = parsereal(value, ierr, lnr)[$
            @if is_last $]
            end if[$
            @end @if $][$
         @end @for $][$
         @if is_last $]
         end if[$
         @end @if $][$
      @end @for $][$
   @end @for $][$
@end @if $]
      elseif (name(1:2).eq."m(" .or. name(1:2).eq."w(") then
         idx = scan(name, ')', .false.)
         if (idx.eq.0) then
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         endif
         read(name(3:idx-1),*, iostat=ierr) pdg
         if (ierr.ne.0) then
            write(*,*) "pdg is not an integer:", name(3:idx-1)
            if(present(line_number)) then
               write(*,'(A13,1x,I5)') 'error at line', line_number
            else
               write(*,'(A18)') 'error in parseline'
            end if
            stat = 1
            return
         end if
         if (name(1:1).eq."m") then
            ! set mass according to PDG code
            select case(pdg)[$
@if has_slha_locations $][$
   @for slha_blocks lower $][$
      @select $_ @case masses $][$
         @for slha_entries $]
            case([$index$])
               [$ $_ $] = parsereal(value, ierr, lnr)[$
         @end @for $][$
      @end @select $][$
   @end @for $][$
@end @if $]
            case default
               write(*,'(A20,1x,I10)') "Cannot set mass for PDG code:", pdg
               stat = 1
               return
            end select
         else
            ! set width according to PDG code
            select case(pdg)[$
@if has_slha_locations $][$
   @for slha_blocks lower $][$
      @select $_ @case decay $][$
         @for slha_entries $]
            case([$index$])
               [$ $_ $] = parsereal(value, ierr, lnr)[$
         @end @for $][$
      @end @select $][$
   @end @for $][$
@end @if $]
            case default
               write(*,'(A20,1x,I10)') "Cannot set width for PDG code:", pdg
               stat = 1
               return
            end select
         endif
      else
         write(*,'(A20,1x,A20)') 'Unrecognized option:', name
         stat = 1
         return
      end if
      stat = 0
   end subroutine parseline

   subroutine     parse(aunit)
      implicit none
      integer, intent(in) :: aunit
      character(len=line_length) :: line
      integer :: ios, lnr
      lnr = 0
      loop1: do
         read(unit=aunit,fmt='(A[$buffer_length$])',iostat=ios) line
         if(ios .ne. 0) exit
         lnr = lnr + 1
         line = adjustl(line)
         if (line .eq. '') cycle loop1
         if (any(cc .eq. line(1:1))) cycle loop1

         call parseline(line,ios,lnr)
         if(ios .ne. 0) then
            write(*,'(A44,I2,A1)') &
            & 'Error while reading parameter file in parse(', aunit, ')'
         end if
      end do loop1
   end subroutine parse[$
@if has_slha_locations $]
!---#[ SLHA READER:
   subroutine     read_slha(ch, ierr)
      implicit none
      integer, intent(in) :: ch
      integer, intent(out), optional :: ierr
   
      integer :: lnr, i, l, ofs, ios
      character(len=255) :: line
   
      integer :: block
   
      ofs = iachar('A') - iachar('a')
   
      lnr = 0
      loop1: do
         read(unit=ch,fmt='(A[$buffer_length$])',iostat=ios) line
         if(ios .ne. 0) exit
         lnr = lnr + 1
   
         i = scan(line, '#', .false.)
         if (i .eq. 0) then
            l = len_trim(line)
         else
            l = i - 1
         end if
   
         if (l .eq. 0) cycle loop1
   
         ucase: do i = 1, l
            if (line(i:i) >= 'a' .and. line(i:i) <= 'z') then
               line(i:i) = achar(iachar(line(i:i))+ofs)
            end if
         end do ucase
   
         if (line(1:1) .eq. 'B') then
            if (line(1:5) .eq. 'BLOCK') then
               line = adjustl(line(6:l))
               do i=1,l
                 if (line(i:i) <= ' ') exit
               end do
               l = i[$
         @for slha_blocks upper $]
               [$
            @if is_first $][$ @else $]else[$
            @end @if
               $]if ("[$ $_ $]" .eq. line(1:l)) then
                  block = [$ index $][$
            @if is_last $]
               else
                  block = -1
               end if[$
            @end @if $][$
         @end @for $]
            else
               write(*,'(A37,I5)') "Illegal statement in SLHA file, line ", lnr
               if (present(ierr)) ierr = 1
               return
            end if[$
         @for slha_blocks lower $][$ 
            @select $_ @case decay $]
         elseif (line(1:1) .eq. 'D') then
            if (line(1:5) .eq. 'DECAY') then
               line = adjustl(line(6:l))
               call read_slha_line_decay(line, i)
               block = 2            
            else
               write(*,'(A37,I5)') "Illegal statement in SLHA file, line ", lnr
               if (present(ierr)) ierr = 1
               return
            end if[$
            @end @select $][$
         @end @for $]
         else
            ! read a parameter line
            select case(block)[$
         @for slha_blocks lower $]
            case([$ index $])
               call read_slha_block_[$ $_ $](line(1:l), i)
               if (i .ne. 0) then
                  if (present(ierr)) ierr = 1
                  write(*,'(A44,I5)') &
                  & "Unrecognized line format in SLHA file, line ", lnr
                  return
               end if[$
         @end @for $]
            case default
               cycle loop1
            end select
         end if
      end do loop1
      if (present(ierr)) ierr = 0
   end subroutine read_slha[$
   @for slha_blocks lower dimension=1 $][$ 
      @select $_ @case decay $]
   subroutine read_slha_block_[$ $_ $](line, ierr)
   !  This subroutine reads the 'branching ratios' of 
   !  the slha file: these are just thrown away
      implicit none
      character(len=*), intent(in) :: line
      integer, intent(out), optional :: ierr
      integer :: idx1,idx2,ioerr,nda
      real(ki) :: value
      read(line,*,iostat=ioerr) value, nda, idx1, idx2
      if (ioerr .ne. 0) then
         if (present(ierr)) ierr = 1
         return
      end if
      if (present(ierr)) ierr = 0
   end subroutine read_slha_block_[$ $_ $]
   subroutine read_slha_line_[$ $_ $](line, ierr)
      implicit none
      character(len=*), intent(in) :: line
      integer, intent(out), optional :: ierr[$
      @for slha_entries index=idx1$][$
         @if is_first $]
      integer :: idx1,ioerr
      real(ki) :: value

      read(line,*,iostat=ioerr) idx1, value
      if (ioerr .ne. 0) then
         if (present(ierr)) ierr = 1
         return
      end if
      select case(idx1)[$
         @end @if is_first $]
      case([$ idx1 $])
         [$ $_ $] = value[$
         @if is_last $]
      end select[$
         @end @if is_last $][$
      @end @for$]
      if (present(ierr)) ierr = 0
   end subroutine read_slha_line_[$ $_ $][$
   @else $]
   subroutine read_slha_block_[$ $_ $](line, ierr)
      implicit none
      character(len=*), intent(in) :: line
      integer, intent(out), optional :: ierr[$
      @for slha_entries index=idx1$][$
         @if is_first $]
      integer :: idx1,ioerr
      real(ki) :: value

      read(line,*,iostat=ioerr) idx1, value
      if (ioerr .ne. 0) then
         if (present(ierr)) ierr = 1
         return
      end if
      select case(idx1)[$
         @end @if is_first $]
      case([$ idx1 $])
         [$ $_ $] = value[$
         @if is_last $]
      end select[$
         @end @if is_last $][$
      @end @for$]
      if (present(ierr)) ierr = 0
   end subroutine read_slha_block_[$ $_ $][$ 
   @end @select $][$
   @end @for $][$
   @for slha_blocks lower dimension=2 $]
   subroutine read_slha_block_[$ $_ $](line, ierr)
      implicit none
      character(len=*), intent(in) :: line
      integer, intent(out), optional :: ierr[$
      @for slha_entries index=idx1$][$
         @if is_first $]
      integer :: idx1, idx2, ioerr
      real(ki) :: value

      read(line,*,iostat=ioerr) idx1, idx2, value
      if (ioerr .ne. 0) then
         if (present(ierr)) ierr = 1
         return
      end if

      select case(idx1)[$
         @end @if is_first $]
      case([$ idx1 $])
         select case(idx2)[$
         @for slha_entries index=idx2 $]
         case([$ idx2 $])
            [$ $_ $] = value[$
         @end @for $]
         end select[$
         @if is_last $]
      end select[$
         @end @if is_last $][$
      @end @for$]
      if (present(ierr)) ierr = 0
   end subroutine read_slha_block_[$ $_ $][$
   @end @for $]
!---#] SLHA READER:[$
@end @if has_slha_locations $]
!---#[ subroutine init_functions:
   subroutine     init_functions()
      implicit none
      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
      real(ki), parameter :: pi = 3.14159265358979323846264&
     &3383279502884197169399375105820974944592307816406286209_ki[$
@for floats $]
     real(ki), parameter :: [$ $_ $] = [$ value convert=float format=%24.15f_ki $][$
@end @for $][$
@for functions_resolved_fortran $]
     [$ $_ $] = [$ expression $][$
@end @for $][$ 
@select model @case sm smdiag $][$ 
@select model.options @case ewchoose $]
      call ewschemechoice(ewchoice)[$
@end @select $][$
@end @select $]
end subroutine init_functions
!---#] subroutine init_functions:
!---#[ utility functions for model initialization:
   pure function ifpos(x0, x1, x2)
      implicit none
      real(ki), intent(in) :: x0, x1, x2
      real(ki) :: ifpos

      if (x0 > 0.0_ki) then
         ifpos = x1
      else
         ifpos = x2
      endif
   end  function ifpos

   pure function sort4(m1, m2, m3, m4, n)
      implicit none
      real(ki), intent(in) :: m1, m2, m3, m4
      integer, intent(in) :: n
      real(ki) :: sort4

      real(ki), dimension(4) :: m
      logical :: f
      integer :: i
      real(ki) :: tmp

      m(1) = m1
      m(2) = m2
      m(3) = m3
      m(4) = m4

      ! Bubble Sort
      do
         f = .false.

         do i=1,3
            if (abs(m(i)) .gt. abs(m(i+1))) then
               tmp = m(i)
               m(i) = m(i+1)
               m(i+1) = tmp
               f = .true.
            end if
         end do

         if (.not. f) exit
      end do

      sort4 = m(n)
   end  function sort4
!---#] utility functions for model initialization:
[$ @select model @case sm smdiag $][$ 
@select model.options @case ewchoose $]
!---#[ EW scheme choice:
  subroutine ewschemechoice(ichoice)
  implicit none
  integer, intent(in) :: ichoice
  real(ki), parameter :: pi = 3.14159265358979323846264&
 &3383279502884197169399375105820974944592307816406286209_ki
  select case (ichoice)
        case (1)
      ! mW, mZ --> sw
        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)
      ! GF, mW, sw --> e
        e = mW*sw*sqrt(8.0_ki*GF/sqrt(2.0_ki))
        case (2)
      ! alpha --> e
        e = sqrt(4.0_ki*pi*alpha)
      ! mW, mZ --> sw
        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)
        case (3)
        e = sqrt(4.0_ki*pi*alpha)
      ! sw, mZ --> mW
        mW = mZ*sqrt(1.0_ki-sw*sw)
        case (4)
      ! alpha --> e
        e = sqrt(4.0_ki*pi*alpha)
      ! GF, sw, alpha --> mW
        mW = sqrt(alpha*pi/sqrt(2.0_ki)/GF) / sw
      ! mW, sw --> mZ
        mZ = mW / sqrt(1.0_ki-sw*sw)
        case (5)
      ! mW, mZ --> sw
        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)
        case (6)
      ! mZ, sw --> mW
        mW = mZ*sqrt(1-sw*sw)
        case(7)
      ! e, sw, GF --> mW
        mW = e/2.0_ki/sw/sqrt(sqrt(2.0_ki)*GF)
      ! mW, sw --> mZ
        mZ = mW / sqrt(1.0_ki-sw*sw)
        case(8)
      ! alpha --> e
        e = sqrt(4.0_ki*pi*alpha)
      ! GF, mZ, alpha --> mW
      mW = sqrt(mZ*mZ/2.0_ki+sqrt(mZ*mZ*mZ*mZ/4.0_ki-pi*alpha*mZ*mZ/&
     & sqrt(2.0_ki)/GF))
      ! mW, mZ --> sw
      sw = sqrt(1.0_ki-mW*mW/mZ/mZ)
!        case default
  end select
  end subroutine
!---#] EW scheme choice:[$
@end @select$][$
@end @select$]
[$ @select model @case sm_complex  $][$ 
@select model.options @case ewchoose $]
!---#[ EW scheme choice:
  subroutine ewschemechoice(ichoice)
  implicit none
  integer, intent(in) :: ichoice
  real(ki), parameter :: pi = 3.14159265358979323846264&
 &3383279502884197169399375105820974944592307816406286209_ki
  complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
  select case (ichoice)
        case (1)
      ! mW, mZ --> sw
        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))
      ! GF, mW, sw --> e
        e = sqrt(mW*mW-i_*mW*wW)*sw*sqrt(8.0_ki*GF/sqrt(2.0_ki))
        case (2)
      ! alpha --> e
        e = sqrt(4.0_ki*pi*alpha)
      ! mW, mZ --> sw
        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))
        case (3)
        e = sqrt(4.0_ki*pi*alpha)
      ! sw, mZ --> mW
        mW = sqrt(mZ*mZ-i_*mZ*wZ)*sqrt(1.0_ki-sw*sw)
        case (4)
      ! alpha --> e
        e = sqrt(4.0_ki*pi*alpha)
      ! GF, sw, alpha --> mW
        mW = sqrt(alpha*pi/sqrt(2.0_ki)/GF) / sw
      ! mW, sw --> mZ
        mZ = sqrt(mW*mW-i_*mW*wW) / sqrt(1.0_ki-sw*sw)
        case (5)
      ! mW, mZ --> sw
        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))
        case (6)
      ! mZ, sw --> mW
        mW = sqrt(mZ*mZ-i_*mZ*wZ)*sqrt(1.0_ki-sw*sw)
        case(7)
      ! e, sw, GF --> mW
        mW = e/2.0_ki/sw/sqrt(sqrt(2.0_ki)*GF)
      ! mW, sw --> mZ
        mZ = sqrt(mW*mW-i_*mW*wW) / sqrt(1.0_ki-sw*sw)
        case(8)
      ! alpha --> e
        e = sqrt(4.0_ki*pi*alpha)
      ! GF, mZ, alpha --> mW
      mW = sqrt((mZ*mZ-i_*mZ*wZ)/2.0_ki+sqrt((mZ*mZ-i_*mZ*wZ)**2/4.0_ki-pi*alpha*(mZ*mZ-i_*mZ*wZ)/&
     & sqrt(2.0_ki)/GF))
      ! mW, mZ --> sw
      sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))
!        case default
  end select
  end subroutine
!---#] EW scheme choice:[$
@end @select$][$
@end @select$]
end module olp_model

