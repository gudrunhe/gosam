%=$#! /usr/bin/env python
# vim: ts=3:sw=3:expandtab

import sys
import os
from optparse import OptionParser
from t2f import translatefile, postformat, getdata
from pythonin import parameters, kinematics, symbols, lambdafunc, dotproducts
config={'parameters' : parameters,
        'kinematics' : kinematics,
        'symbols' : symbols,
        'lambdafunc' : lambdafunc,
        'dotproducts' : dotproducts}


parser = OptionParser()

parser.add_option("-i", "--input", dest="input",                   
                  action="store", type="string",
                  help="input file", metavar="INPUT")


(options, args) = parser.parse_args()

if not options.input:
    sys.exit("Error: no input file was found! Please specify one with the -i options.")

# print '----------------------------------'

modelfile = open('model.f90', 'w')

abb_max=getdata('model.dat')['number_abbs']

#print "--------------------"

outdict=translatefile(options.input,config)
# Write model.f90 file
modelfile.write('module     [$ process_name asprefix=\_ $]model\n')
modelfile.write('   ! Model parameters for the model: [$ model $]\n')
modelfile.write('   use [$ process_name asprefix=\_ $]config, only: ki')[$
@if extension samurai $]
modelfile.write(', &\n')
modelfile.write('   & samurai_scalar, samurai_verbosity, samurai_test, &\n')
modelfile.write('   & samurai_group_numerators, samurai_istop')[$
@end @if $]
modelfile.write(', &\n')
modelfile.write('   & renormalisation, reduction_interoperation, deltaOS, &\n')
modelfile.write('   & nlo_prefactors\n')[$ 
@select model @case sm smdiag $][$ 
@select model.options @case ewchoose $]
modelfile.write(', ewchoice\n')[$
@end @select$][$@end @select$]
modelfile.write('   implicit none\n')
modelfile.write('\n')
modelfile.write('   private :: ki\n')[$
@if extension samurai $]
modelfile.write('   private :: samurai_scalar, samurai_verbosity, samurai_test\n')
modelfile.write('   private :: samurai_group_numerators, samurai_istop\n')[$
@end @if $]
modelfile.write('   private :: renormalisation, reduction_interoperation, deltaOS\n')
modelfile.write('   private :: nlo_prefactors\n')
modelfile.write('\n')
modelfile.write('   real(ki), parameter :: sqrt2 = &\n')
modelfile.write('      &1.414213562373095048801688724209698078&\n')
modelfile.write('      &5696718753769480731766797379_ki\n')
modelfile.write('   real(ki), parameter :: sqrt3 = &\n')
modelfile.write('      &1.732050807568877293527446341505872366&\n')
modelfile.write('      &9428052538103806280558069795_ki\n')[$
      @for parameters $][$
         @select type
            @case R $]
modelfile.write('   real(ki) :: [$$_$] = [$ real convert=float format=%24.15f_ki $]\n')[$
            @case C $]
modelfile.write('   complex(ki) :: [$$_$] = ([$ real convert=float format=%24.15f_ki $], [$ imag convert=float format=%24.15f_ki $])\n')[$
            @case RP $]
modelfile.write('   real(ki),parameter :: [$$_$] = [$ real convert=float format=%24.15f_ki $]\n')[$
            @case CP $]
modelfile.write('   complex(ki), parameter :: [$$_$] = ([$ real convert=float format=%24.15f_ki $], [$imag convert=float format=%24.15f_ki $])\n')[$
         @end @select type $][$
      @end @for parameters $][$
      @for functions $][$ 
         @select type
            @case R $]
modelfile.write('   real(ki) :: [$$_$]\n')[$
            @case C $]
modelfile.write('   complex(ki) :: [$$_$]\n')[$
         @end @select type $][$
      @end @for functions $]
modelfile.write('   integer, parameter, private :: line_length = [$buffer_length$]\n')
#      
#   ' what is our longest extra name ?
#   ' 0   0    1    1    2    2
#   ' 1---5----0----5----0----5
#   ' samurai_group_numerators
#   ' reduction_interoperation
#   ' samurai_verbatim
#   ' renormalisation
#   ' samurai_scalar
#   ' samurai_test
#   '
#   ' ==> the longest is 24
#   
modelfile.write('   integer, parameter, private :: name_length = max([$name_length$],24)\n')
modelfile.write('   character(len=name_length), dimension([$ count R C $]) :: names = (/&\n')[$
   @for parameters R C  $]
modelfile.write('      & "[$ $_ $][$ alignment $]"')[$
         @if is_last $]
modelfile.write('/)\n')
   [$ @else $]
modelfile.write(', &\n')
[$ @end @if $][$
   @end @for parse_names $]
modelfile.write('   character(len=1), dimension([$ len_comment_chars $]) :: cc = (/')[$
   @for comment_chars $]
modelfile.write(' \'[$$_$]\'')[$ @if is_last $]
modelfile.write('/)\n')[$ @else $]
modelfile.write(',')[$
   @end @if $][$
   @end @for$]
modelfile.write('\n')
modelfile.write("   private :: digit, parsereal, names, cc\n")
modelfile.write("\n")
modelfile.write("contains\n")
modelfile.write("\n")
modelfile.write("   function     digit(ch, lnr) result(d)\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=1), intent(in) :: ch\n")
modelfile.write("      integer, intent(in) :: lnr\n")
modelfile.write("      integer :: d\n")
modelfile.write("      d = -1\n")
modelfile.write("      select case(ch)\n")[$
         @for repeat 10 $]
modelfile.write("         case(\'[$$_$]\')\n")
modelfile.write("            d = [$$_$]\n")[$
         @end @for $]
modelfile.write("         case default\n")
modelfile.write("            write(*,'(A21,1x,I5)') 'invalid digit in line', lnr\n")
modelfile.write("         end select\n")
modelfile.write("   end function digit\n")
modelfile.write("\n")
modelfile.write("   function     parsereal(str, ierr, lnr) result(num)\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=*), intent(in) :: str\n")
modelfile.write("      integer, intent(out) :: ierr\n")
modelfile.write("      integer, intent(in) :: lnr\n")
modelfile.write("      integer, dimension(0:3,0:4), parameter :: DFA = &\n")
modelfile.write("      & reshape( (/1,  1,  2, -1,   & ! state = 0\n")
modelfile.write("      &            1, -1,  2,  3,   & ! state = 1\n")
modelfile.write("      &            2, -1, -1,  3,   & ! state = 2\n")
modelfile.write("      &            4,  4, -1, -1,   & ! state = 3\n")
modelfile.write("      &            4, -1, -1, -1/), (/4, 5/))\n")
modelfile.write("      real(ki) :: num\n")
modelfile.write("      integer :: i, expo, ofs, state, cclass, d, s1, s2\n")
modelfile.write("      num = 0.0_ki\n")
modelfile.write("      expo = 0\n")
modelfile.write("      state = 0\n")
modelfile.write("      ofs = 0\n")
modelfile.write("      s1 = 1\n")
modelfile.write("      s2 = 1\n")
modelfile.write("      d = -1\n")
modelfile.write("      cclass = -1\n")
modelfile.write("      do i=1,len(str)\n")
modelfile.write("         select case(str(i:i))\n")
modelfile.write("         case('_', '''', ' ')\n")
modelfile.write("            cycle\n")
modelfile.write("         case('+', '-')\n")
modelfile.write("            cclass = 1\n")
modelfile.write("         case('.')\n")
modelfile.write("            cclass = 2\n")
modelfile.write("         case('E', 'e')\n")
modelfile.write("            cclass = 3\n")
modelfile.write("         case default\n")
modelfile.write("            cclass = 0\n")
modelfile.write("            d = digit(str(i:i), lnr)\n")
modelfile.write("            if (d .eq. -1) then\n")
modelfile.write("               ierr = 1\n")
modelfile.write("               return\n")
modelfile.write("            end if\n")
modelfile.write("         end select\n")
modelfile.write("         if (cclass .eq. 0) then\n")
modelfile.write("            select case(state)\n")
modelfile.write("            case(0, 1)\n")
modelfile.write("               num = 10.0_ki * num + d\n")
modelfile.write("            case(2)\n")
modelfile.write("               num = 10.0_ki * num + d\n")
modelfile.write("               ofs = ofs - 1\n")
modelfile.write("            case(4)\n")
modelfile.write("               expo = 10 * expo + d\n")
modelfile.write("            end select\n")
modelfile.write("         elseif ((cclass .eq. 1) .and. (str(i:i) .eq. '-')) then\n")
modelfile.write("            if (state .eq. 0) then\n")
modelfile.write("               s1 = -1\n")
modelfile.write("            else\n")
modelfile.write("               s2 = -1\n")
modelfile.write("            endif\n")
modelfile.write("         end if\n")
modelfile.write("         ! Advance in the DFA\n")
modelfile.write("         state = DFA(cclass, state)\n")
modelfile.write("         if (state < 0) then\n")
modelfile.write("            write(*,'(A21,1x,A1,1x,A7,I5)') 'invalid position for', &\n")
modelfile.write("            & str(i:i), 'in line', lnr\n")
modelfile.write("            ierr = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("      end do\n")
modelfile.write("      num = s1 * num * 10.0_ki**(ofs + s2 * expo)\n")
modelfile.write("      ierr = 0\n")
modelfile.write("   end function parsereal\n")
modelfile.write("\n")
modelfile.write("   subroutine     parseline(line,stat,line_number)\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=*), intent(in) :: line\n")
modelfile.write("      integer, intent(out) :: stat\n")
modelfile.write("      integer, intent(in), optional :: line_number\n")
modelfile.write("\n")
modelfile.write("      character(len=line_length) :: rvalue, ivalue, value\n")
modelfile.write("      character(len=name_length) :: name\n")
modelfile.write("      real(ki) :: re, im\n")
modelfile.write("      integer :: idx, icomma, idx1, idx2, lnr, nidx, ierr, pdg\n")
modelfile.write("\n")
modelfile.write("      if(present(line_number)) then\n")
modelfile.write("         lnr = line_number\n")
modelfile.write("      else\n")
modelfile.write("         lnr = 0\n")
modelfile.write("      end if\n")
modelfile.write("\n")
modelfile.write("      idx = scan(line, '=', .false.)\n")
modelfile.write("      if (idx .eq. 0) then\n")
modelfile.write("         if(present(line_number)) then\n")
modelfile.write("            write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("         else\n")
modelfile.write("            write(*,'(A18)') 'error in parseline'\n")
modelfile.write("         end if\n")
modelfile.write("         stat = 1\n")
modelfile.write("         return\n")
modelfile.write("      end if\n")
modelfile.write("      name = adjustl(line(1:idx-1))\n")
modelfile.write("      value = adjustl(line(idx+1:len(line)))\n")
modelfile.write("      idx = scan(value, ',', .false.)\n")
modelfile.write("      \n")
modelfile.write("      if (name .eq. \"renormalisation\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         renormalisation = int(re)\n")
modelfile.write("      elseif (name .eq. \"nlo_prefactors\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         nlo_prefactors = int(re)\n")
modelfile.write("      elseif (name .eq. \"deltaOS\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         deltaOS = int(re)\n")
modelfile.write("      elseif (name .eq. \"reduction_interoperation\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         reduction_interoperation = int(re)\n")[$
@if extension samurai $]
modelfile.write("      elseif (name .eq. \"samurai_scalar\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         samurai_scalar = int(re)\n")
modelfile.write("      elseif (name .eq. \"samurai_verbosity\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         samurai_verbosity = int(re)\n")
modelfile.write("      elseif (name .eq. \"samurai_test\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         samurai_test = int(re)\n")
modelfile.write("      elseif (name .eq. \"samurai_istop\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         samurai_istop = int(re)\n")
modelfile.write("      elseif (name .eq. \"samurai_group_numerators\") then\n")
modelfile.write("         re = parsereal(value, ierr, lnr)\n")
modelfile.write("         if (ierr .ne. 0) then\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         samurai_group_numerators = (int(re).ne.0)\n")[$
@end @if $]
modelfile.write("      elseif (any(names .eq. name)) then\n")
modelfile.write("         do nidx=1,size(names)\n")
modelfile.write("            if (names(nidx) .eq. name) exit\n")
modelfile.write("         end do\n")
modelfile.write("         if (idx .gt. 0) then\n")
modelfile.write("            rvalue = value(1:idx-1)\n")
modelfile.write("            ivalue = value(idx+1:len(value))\n")
modelfile.write("            re = parsereal(rvalue, ierr, lnr)\n")
modelfile.write("            if (ierr .ne. 0) then\n")
modelfile.write("               stat = 1\n")
modelfile.write("               return\n")
modelfile.write("            end if\n")
modelfile.write("            im = parsereal(ivalue, ierr, lnr)\n")
modelfile.write("            if (ierr .ne. 0) then\n")
modelfile.write("               stat = 1\n")
modelfile.write("               return\n")
modelfile.write("            end if\n")
modelfile.write("         else\n")
modelfile.write("            re = parsereal(value, ierr, lnr)\n")
modelfile.write("            if (ierr .ne. 0) then\n")
modelfile.write("               stat = 1\n")
modelfile.write("               return\n")
modelfile.write("            end if\n")
modelfile.write("            im = 0.0_ki\n")
modelfile.write("         end if\n")
modelfile.write("         select case (nidx)\n")[$
         @for parameters R C $]
modelfile.write("         case([$index$])\n")
modelfile.write("            [$ $_ $] = ")[$
         @select type
         @case C$]
modelfile.write("cmplx(re, im, ki)\n")[$
         @else $]
modelfile.write("re\n")[$
         @end @select $][$
         @end @for $]
modelfile.write("         end select\n")[$
@if has_slha_locations $][$
   @for slha_blocks lower dimension=1 $]
modelfile.write('      elseif (name(1:[$ eval 1 + .len. $_ $]).eq."[$ $_ $](") then\n')
modelfile.write("         idx = scan(name, ')', .false.)\n")
modelfile.write("         if (idx.eq.0) then\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         endif\n")
modelfile.write("         read(name([$ eval 2 + .len. $_ $]:idx-1),*, iostat=ierr) pdg\n")
modelfile.write("         if (ierr.ne.0) then\n")
modelfile.write("            write(*,*) \"Not an integer:\", name([$ eval 2 + .len. $_ $]:idx-1)\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         select case(pdg)\n")[$
      @for slha_entries $]
modelfile.write("            case([$index$])\n")
modelfile.write("               [$ $_ $] = parsereal(value, ierr, lnr)\n")[$
      @end @for $]
modelfile.write("            case default\n")
modelfile.write("               write(*,'(A20,1x,I10)') \"Cannot set [$ $_ $] for code:\", pdg\n")
modelfile.write("               stat = 1\n")
modelfile.write("               return\n")
modelfile.write("         end select\n")[$
   @end @for $][$
   @for slha_blocks lower dimension=2 $]
modelfile.write("      elseif (name(1:[$ eval 1 + .len. $_ $]).eq.\"[$ $_ $](\") then\n")
modelfile.write("         idx = scan(name, ')', .false.)\n")
modelfile.write("         if (idx.eq.0) then\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         endif\n")
modelfile.write("         icomma = scan(name(1:idx), ',', .false.)\n")
modelfile.write("         if (icomma.eq.0) then\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         endif\n")
modelfile.write("         read(name([$ eval 2 + .len. $_ $]:icomma-1),*, iostat=ierr) idx1\n")
modelfile.write("         if (ierr.ne.0) then\n")
modelfile.write("            write(*,*) \"Not an integer:\", name([$ eval 2 + .len. $_ $]:icomma-1)\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         read(name(icomma+1:idx-1),*, iostat=ierr) idx2\n")
modelfile.write("         if (ierr.ne.0) then\n")
modelfile.write("            write(*,*) \"Not an integer:\", name(icomma+1:idx-1)\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")[$
      @for slha_entries index=index1 $]
         [$
         @if is_first $][$ @else $]
modelfile.write("         else\n")[$
         @end @if$]
modelfile.write("               if(idx1.eq.[$index1$]) then\n")[$
         @for slha_entries index=index2 $]
            [$
            @if is_first $][$ @else $]
modelfile.write("         else\n")[$
            @end @if $]
modelfile.write("if(idx2.eq.[$index2$]) then\n")
modelfile.write("               [$ $_ $] = parsereal(value, ierr, lnr)\n")[$
            @if is_last $]
modelfile.write("            end if\n")[$
            @end @if $][$
         @end @for $][$
         @if is_last $]
modelfile.write("         end if\n")[$
         @end @if $][$
      @end @for $][$
   @end @for $][$
@end @if $]
modelfile.write('      elseif (name(1:2).eq.\"m(\" .or. name(1:2).eq.\"w(\") then\n')
modelfile.write("         idx = scan(name, ')', .false.)\n")
modelfile.write("         if (idx.eq.0) then\n")
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         endif\n")
modelfile.write("         read(name(3:idx-1),*, iostat=ierr) pdg\n")
modelfile.write("         if (ierr.ne.0) then\n")
modelfile.write('            write(*,*) "pdg is not an integer:", name(3:idx-1)\n')
modelfile.write("            if(present(line_number)) then\n")
modelfile.write("               write(*,'(A13,1x,I5)') 'error at line', line_number\n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A18)') 'error in parseline'\n")
modelfile.write("            end if\n")
modelfile.write("            stat = 1\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         if (name(1:1).eq.\"m\") then\n")
modelfile.write("            ! set mass according to PDG code\n")
modelfile.write("            select case(pdg)\n")[$
@if has_slha_locations $][$
   @for slha_blocks lower $][$
      @select $_ @case masses $][$
         @for slha_entries $]
modelfile.write("            case([$index$])\n")
modelfile.write("               [$ $_ $] = parsereal(value, ierr, lnr)\n")[$
         @end @for $][$
      @end @select $][$
   @end @for $][$
@end @if $]
modelfile.write("            case default\n")
modelfile.write("               write(*,'(A20,1x,I10)') \"Cannot set mass for PDG code:\", pdg\n")
modelfile.write("               stat = 1\n")
modelfile.write("               return\n")
modelfile.write("            end select\n")
modelfile.write("         else\n")
modelfile.write("            ! set width according to PDG code\n")
modelfile.write("            select case(pdg)\n")[$
@if has_slha_locations $][$
   @for slha_blocks lower $][$
      @select $_ @case decay $][$
         @for slha_entries $]
modelfile.write("            case([$index$])\n")
modelfile.write("               [$ $_ $] = parsereal(value, ierr, lnr)\n")[$
         @end @for $][$
      @end @select $][$
   @end @for $][$
@end @if $]
modelfile.write("            case default\n")
modelfile.write("               write(*,'(A20,1x,I10)') \"Cannot set width for PDG code:\", pdg\n")
modelfile.write("               stat = 1\n")
modelfile.write("               return\n")
modelfile.write("            end select\n")
modelfile.write("         endif\n")
modelfile.write("      else\n")
modelfile.write("         write(*,'(A20,1x,A20)') 'Unrecognized option:', name\n")
modelfile.write("         stat = 1\n")
modelfile.write("         return\n")
modelfile.write("      end if\n")
modelfile.write("      stat = 0\n")
modelfile.write("   end subroutine parseline\n")
modelfile.write("\n")
modelfile.write("   subroutine     parse(aunit)\n")
modelfile.write("      implicit none\n")
modelfile.write("      integer, intent(in) :: aunit\n")
modelfile.write("      character(len=line_length) :: line\n")
modelfile.write("      integer :: ios, lnr\n")
modelfile.write("      lnr = 0\n")
modelfile.write("      loop1: do\n")
modelfile.write("         read(unit=aunit,fmt='(A[$buffer_length$])',iostat=ios) line\n")
modelfile.write("         if(ios .ne. 0) exit\n")
modelfile.write("         lnr = lnr + 1\n")
modelfile.write("         line = adjustl(line)\n")
modelfile.write("         if (line .eq. '') cycle loop1\n")
modelfile.write("         if (any(cc .eq. line(1:1))) cycle loop1\n")
modelfile.write("\n")
modelfile.write("         call parseline(line,ios,lnr)\n")
modelfile.write("         if(ios .ne. 0) then\n")
modelfile.write("            write(*,'(A44,I2,A1)') &\n")
modelfile.write("            & 'Error while reading parameter file in parse(', aunit, ')'\n")
modelfile.write("         end if\n")
modelfile.write("      end do loop1\n")
modelfile.write("   end subroutine parse\n")[$
@if has_slha_locations $]
modelfile.write("!---#[ SLHA READER:\n")
modelfile.write("   subroutine     read_slha(ch, ierr)\n")
modelfile.write("      implicit none\n")
modelfile.write("      integer, intent(in) :: ch\n")
modelfile.write("      integer, intent(out), optional :: ierr\n")
modelfile.write("   \n")
modelfile.write("      integer :: lnr, i, l, ofs, ios\n")
modelfile.write("      character(len=255) :: line\n")
modelfile.write("   \n")
modelfile.write("      integer :: block\n")
modelfile.write("   \n")
modelfile.write("      ofs = iachar('A') - iachar('a')\n")
modelfile.write("   \n")
modelfile.write("      lnr = 0\n")
modelfile.write("      loop1: do\n")
modelfile.write("         read(unit=ch,fmt='(A[$buffer_length$])',iostat=ios) line\n")
modelfile.write("         if(ios .ne. 0) exit\n")
modelfile.write("         lnr = lnr + 1\n")
modelfile.write("   \n")
modelfile.write("         i = scan(line, '#', .false.)\n")
modelfile.write("         if (i .eq. 0) then\n")
modelfile.write("            l = len_trim(line)\n")
modelfile.write("         else\n")
modelfile.write("            l = i - 1\n")
modelfile.write("         end if\n")
modelfile.write("   \n")
modelfile.write("         if (l .eq. 0) cycle loop1\n")
modelfile.write("   \n")
modelfile.write("         ucase: do i = 1, l\n")
modelfile.write("            if (line(i:i) >= 'a' .and. line(i:i) <= 'z') then\n")
modelfile.write("               line(i:i) = achar(iachar(line(i:i))+ofs)\n")
modelfile.write("            end if\n")
modelfile.write("         end do ucase\n")
modelfile.write("   \n")
modelfile.write("         if (line(1:1) .eq. 'B') then\n")
modelfile.write("            if (line(1:5) .eq. 'BLOCK') then\n")
modelfile.write("               line = adjustl(line(6:l))\n")
modelfile.write("               do i=1,l\n")
modelfile.write("                 if (line(i:i) <= ' ') exit\n")
modelfile.write("               end do\n")
modelfile.write("               l = i\n")[$
         @for slha_blocks upper $]
               [$
            @if is_first $][$ @else $]
modelfile.write("           else")[$
            @end @if
               $]
modelfile.write("           if (\"[$ $_ $]\" .eq. line(1:l)) then\n")
modelfile.write("                  block = [$ index $]\n")[$
            @if is_last $]
modelfile.write("               else\n")
modelfile.write("                  block = -1\n")
modelfile.write("               end if\n")[$
            @end @if $][$
         @end @for $]
modelfile.write("            else\n")
modelfile.write("               write(*,'(A37,I5)') \"Illegal statement in SLHA file, line \", lnr\n")
modelfile.write("               if (present(ierr)) ierr = 1\n")
modelfile.write("               return\n")
modelfile.write("            end if\n")[$
         @for slha_blocks lower $][$ 
            @select $_ @case decay $]
modelfile.write("         elseif (line(1:1) .eq. 'D') then\n")
modelfile.write("            if (line(1:5) .eq. 'DECAY') then\n")
modelfile.write("               line = adjustl(line(6:l))\n")
modelfile.write("               call read_slha_line_decay(line, i)\n")
modelfile.write("               block = 2            \n")
modelfile.write("            else\n")
modelfile.write("               write(*,'(A37,I5)') \"Illegal statement in SLHA file, line \", lnr\n")
modelfile.write("               if (present(ierr)) ierr = 1\n")
modelfile.write("               return\n")
modelfile.write("            end if\n")[$
            @end @select $][$
         @end @for $]
modelfile.write("         else\n")
modelfile.write("            ! read a parameter line\n")
modelfile.write("            select case(block)\n")[$
         @for slha_blocks lower $]
modelfile.write("            case([$ index $])\n")
modelfile.write("               call read_slha_block_[$ $_ $](line(1:l), i)\n")
modelfile.write("               if (i .ne. 0) then\n")
modelfile.write("                  if (present(ierr)) ierr = 1\n")
modelfile.write("                  write(*,'(A44,I5)') &\n")
modelfile.write("                  & \"Unrecognized line format in SLHA file, line \", lnr\n")
modelfile.write("                  return\n")
modelfile.write("               end if\n")[$
         @end @for $]
modelfile.write("            case default\n")
modelfile.write("               cycle loop1\n")
modelfile.write("            end select\n")
modelfile.write("         end if\n")
modelfile.write("      end do loop1\n")
modelfile.write("      if (present(ierr)) ierr = 0\n")
modelfile.write("   end subroutine read_slha\n")[$
   @for slha_blocks lower dimension=1 $][$ 
      @select $_ @case decay $]
modelfile.write("   subroutine read_slha_block_[$ $_ $](line, ierr)\n")
modelfile.write("   !  This subroutine reads the 'branching ratios' of \n")
modelfile.write("   !  the slha file: these are just thrown away\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=*), intent(in) :: line\n")
modelfile.write("      integer, intent(out), optional :: ierr\n")
modelfile.write("      integer :: idx1,idx2,ioerr,nda\n")
modelfile.write("      real(ki) :: value\n")
modelfile.write("      read(line,*,iostat=ioerr) value, nda, idx1, idx2\n")
modelfile.write("      if (ioerr .ne. 0) then\n")
modelfile.write("         if (present(ierr)) ierr = 1\n")
modelfile.write("         return\n")
modelfile.write("      end if\n")
modelfile.write("      if (present(ierr)) ierr = 0\n")
modelfile.write("   end subroutine read_slha_block_[$ $_ $]\n")
modelfile.write("   subroutine read_slha_line_[$ $_ $](line, ierr)\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=*), intent(in) :: line\n")
modelfile.write("      integer, intent(out), optional :: ierr\n")[$
      @for slha_entries index=idx1$][$
         @if is_first $]
modelfile.write("      integer :: idx1,ioerr\n")
modelfile.write("      real(ki) :: value\n")
modelfile.write("\n")
modelfile.write("      read(line,*,iostat=ioerr) idx1, value\n")
modelfile.write("      if (ioerr .ne. 0) then\n")
modelfile.write("         if (present(ierr)) ierr = 1\n")
modelfile.write("         return\n")
modelfile.write("      end if\n")
modelfile.write("      select case(idx1)\n")[$
         @end @if is_first $]
modelfile.write("      case([$ idx1 $])\n")
modelfile.write("         [$ $_ $] = value\n")[$
         @if is_last $]
modelfile.write("      end select\n")[$
         @end @if is_last $][$
      @end @for$]
modelfile.write("      if (present(ierr)) ierr = 0\n")
modelfile.write("   end subroutine read_slha_line_[$ $_ $]\n")[$
   @else $]
modelfile.write("   subroutine read_slha_block_[$ $_ $](line, ierr)\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=*), intent(in) :: line\n")
modelfile.write("      integer, intent(out), optional :: ierr\n")[$
      @for slha_entries index=idx1$][$
         @if is_first $]
modelfile.write("      integer :: idx1,ioerr\n")
modelfile.write("      real(ki) :: value\n")
modelfile.write("\n")
modelfile.write("      read(line,*,iostat=ioerr) idx1, value\n")
modelfile.write("      if (ioerr .ne. 0) then\n")
modelfile.write("         if (present(ierr)) ierr = 1\n")
modelfile.write("         return\n")
modelfile.write("      end if\n")
modelfile.write("      select case(idx1)\n")[$
         @end @if is_first $]
modelfile.write("      case([$ idx1 $])\n")
modelfile.write("         [$ $_ $] = value\n")[$
         @if is_last $]
modelfile.write("      end select\n")[$
         @end @if is_last $][$
      @end @for$]
modelfile.write("      if (present(ierr)) ierr = 0\n")
modelfile.write("   end subroutine read_slha_block_[$ $_ $]\n")[$ 
   @end @select $][$
   @end @for $][$
   @for slha_blocks lower dimension=2 $]
modelfile.write("   subroutine read_slha_block_[$ $_ $](line, ierr)\n")
modelfile.write("      implicit none\n")
modelfile.write("      character(len=*), intent(in) :: line\n")
modelfile.write("      integer, intent(out), optional :: ierr\n")[$
      @for slha_entries index=idx1$][$
         @if is_first $]
modelfile.write("      integer :: idx1, idx2, ioerr\n")
modelfile.write("      real(ki) :: value\n")
modelfile.write("\n")
modelfile.write("      read(line,*,iostat=ioerr) idx1, idx2, value\n")
modelfile.write("      if (ioerr .ne. 0) then\n")
modelfile.write("         if (present(ierr)) ierr = 1\n")
modelfile.write("         return\n")
modelfile.write("      end if\n")
modelfile.write("\n")
modelfile.write("      select case(idx1)\n")[$
         @end @if is_first $]
modelfile.write("      case([$ idx1 $])\n")
modelfile.write("         select case(idx2)\n")[$
         @for slha_entries index=idx2 $]
modelfile.write("         case([$ idx2 $])\n")
modelfile.write("            [$ $_ $] = value\n")[$
         @end @for $]
modelfile.write("         end select\n")[$
         @if is_last $]
modelfile.write("      end select\n")[$
         @end @if is_last $][$
      @end @for$]
modelfile.write("      if (present(ierr)) ierr = 0\n")
modelfile.write("   end subroutine read_slha_block_[$ $_ $]\n")[$
   @end @for $]
modelfile.write("!---#] SLHA READER:\n")[$
@end @if has_slha_locations $]
modelfile.write("!---#[ subroutine init_functions:\n")
modelfile.write("   subroutine     init_functions()\n")
modelfile.write("      implicit none\n")
modelfile.write("      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n")
modelfile.write("      real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write("     &3383279502884197169399375105820974944592307816406286209_ki\n")
if abb_max != '0':
   modelfile.write('      real(ki), dimension(%s) :: mabb\n' % abb_max)[$ 
@select model @case sm smdiag $][$ 
@select model.options @case ewchoose $]
modelfile.write("      call ewschemechoice(ewchoice)\n")[$
@end @select $][$
@end @select $]
modelfile.write("%s" % outdict['Functions'])
modelfile.write("end subroutine init_functions\n")
modelfile.write("!---#] subroutine init_functions:\n")
modelfile.write("!---#[ utility functions for model initialization:\n")
modelfile.write("   pure function ifpos(x0, x1, x2)\n")
modelfile.write("      implicit none\n")
modelfile.write("      real(ki), intent(in) :: x0, x1, x2\n")
modelfile.write("      real(ki) :: ifpos\n")
modelfile.write("\n")
modelfile.write("      if (x0 > 0.0_ki) then\n")
modelfile.write("         ifpos = x1\n")
modelfile.write("      else\n")
modelfile.write("         ifpos = x2\n")
modelfile.write("      endif\n")
modelfile.write("   end  function ifpos\n")
modelfile.write("\n")
modelfile.write("   pure function sort4(m1, m2, m3, m4, n)\n")
modelfile.write("      implicit none\n")
modelfile.write("      real(ki), intent(in) :: m1, m2, m3, m4\n")
modelfile.write("      integer, intent(in) :: n\n")
modelfile.write("      real(ki) :: sort4\n")
modelfile.write("\n")
modelfile.write("      real(ki), dimension(4) :: m\n")
modelfile.write("      logical :: f\n")
modelfile.write("      integer :: i\n")
modelfile.write("      real(ki) :: tmp\n")
modelfile.write("\n")
modelfile.write("      m(1) = m1\n")
modelfile.write("      m(2) = m2\n")
modelfile.write("      m(3) = m3\n")
modelfile.write("      m(4) = m4\n")
modelfile.write("\n")
modelfile.write("      ! Bubble Sort\n")
modelfile.write("      do\n")
modelfile.write("         f = .false.\n")
modelfile.write("\n")
modelfile.write("         do i=1,3\n")
modelfile.write("            if (abs(m(i)) .gt. abs(m(i+1))) then\n")
modelfile.write("               tmp = m(i)\n")
modelfile.write("               m(i) = m(i+1)\n")
modelfile.write("               m(i+1) = tmp\n")
modelfile.write("               f = .true.\n")
modelfile.write("            end if\n")
modelfile.write("         end do\n")
modelfile.write("\n")
modelfile.write("         if (.not. f) exit\n")
modelfile.write("      end do\n")
modelfile.write("\n")
modelfile.write("      sort4 = m(n)\n")
modelfile.write("   end  function sort4\n")
modelfile.write("!---#] utility functions for model initialization:\n")
[$ @select model @case sm smdiag $][$ 
@select model.options @case ewchoose $]
modelfile.write("!---#[ EW scheme choice:\n")
modelfile.write("  subroutine ewschemechoice(ichoice)\n")
modelfile.write("  implicit none\n")
modelfile.write("  integer, intent(in) :: ichoice\n")
modelfile.write("  real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write(" &3383279502884197169399375105820974944592307816406286209_ki\n")
modelfile.write("  select case (ichoice)\n")
modelfile.write("        case (1)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("      ! GF, mW, sw --> e\n")
modelfile.write("        e = mW*sw*sqrt(8.0_ki*GF/sqrt(2.0_ki))\n")
modelfile.write("        case (2)\n")
modelfile.write("      ! alpha --> e\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("        case (3)\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! sw, mZ --> mW\n")
modelfile.write("        mW = mZ*sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case (4)\n")
modelfile.write("      ! alpha --> e\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! GF, sw, alpha --> mW\n")
modelfile.write("        mW = sqrt(alpha*pi/sqrt(2.0_ki)/GF) / sw\n")
modelfile.write("      ! mW, sw --> mZ\n")
modelfile.write("        mZ = mW / sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case (5)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("        case (6)\n")
modelfile.write("      ! mZ, sw --> mW\n")
modelfile.write("        mW = mZ*sqrt(1-sw*sw)\n")
modelfile.write("        case(7)\n")
modelfile.write("      ! e, sw, GF --> mW\n")
modelfile.write("        mW = e/2.0_ki/sw/sqrt(sqrt(2.0_ki)*GF)\n")
modelfile.write("      ! mW, sw --> mZ\n")
modelfile.write("        mZ = mW / sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case(8)\n")
modelfile.write("      ! alpha --> e\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! GF, mZ, alpha --> mW\n")
modelfile.write("      mW = sqrt(mZ*mZ/2.0_ki+sqrt(mZ*mZ*mZ*mZ/4.0_ki-pi*alpha*mZ*mZ/&\n")
modelfile.write("     & sqrt(2.0_ki)/GF))\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("      sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("!        case default\n")
modelfile.write("  end select\n")
modelfile.write("  end subroutine\n")
modelfile.write("!---#] EW scheme choice:\n")[$
@end @select$][$
@end @select$]
modelfile.write("end module [$ process_name asprefix=\_ $]model\n")

modelfile.close()
### additional formatting for output files

postformat('model.f90')
