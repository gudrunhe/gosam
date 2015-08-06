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
modelfile.write('   & renormalisation, reduction_interoperation, &\n')
modelfile.write('   & reduction_interoperation_rescue, deltaOS, &\n')
modelfile.write('   & nlo_prefactors, convert_to_cdr')[$
@select modeltype @case sm smdiag sm_complex smdiag_complex smehc $][$
@if ewchoose $]
modelfile.write(', ewchoice')[$
@end @if$][$
@end @select$]
modelfile.write('\n   implicit none\n')
modelfile.write('\n')
modelfile.write('   private :: ki\n')[$
@if extension samurai $]
modelfile.write('   private :: samurai_scalar, samurai_verbosity, samurai_test\n')
modelfile.write('   private :: samurai_group_numerators, samurai_istop\n')[$
@end @if $]
modelfile.write('   private :: renormalisation, reduction_interoperation\n')
modelfile.write('   private :: reduction_interoperation_rescue\n')
modelfile.write('   private :: deltaOS, nlo_prefactors\n')
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
[$ @if ewchoose $]
modelfile.write('   ! for automatic choosing the right EW scheme in set_parameters\n')
modelfile.write('   integer, private :: choosen_ew_parameters ! bit-set of EW parameters\n')
modelfile.write('   character(len=5), private, dimension(6) :: ew_parameters = &\n')
modelfile.write('          &(/\'mW   \',&\n')
modelfile.write('          &  \'mZ   \',&\n')
modelfile.write('          &  \'alpha\',&\n')
modelfile.write('          &  \'GF   \',&\n')
modelfile.write('          &  \'sw   \',&\n')
modelfile.write('          &  \'e    \'/)\n')
modelfile.write('   integer, private :: choosen_ew_parameters_count = 0 ! bitset of EW parameters\n')
modelfile.write('   integer, private :: orig_ewchoice = -1 ! saves the original ewchoice\n')
[$@end @if$]
modelfile.write("   private :: digit, parsereal, names, cc\n")
modelfile.write("\n")
modelfile.write("contains\n")
modelfile.write("\n")

modelfile.write("!---#[ print_parameter:\n")
modelfile.write("   ! Print current parameters / setup to stdout or output_unit\n")
modelfile.write("   subroutine   print_parameter(verbose,output_unit)\n")
modelfile.write("      implicit none\n")
modelfile.write("      logical, intent(in), optional :: verbose\n")
modelfile.write("      integer, intent(in), optional :: output_unit\n")
modelfile.write("      logical :: is_verbose\n")
modelfile.write("      integer :: unit\n")
modelfile.write("\n")
modelfile.write("      real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write("     &3383279502884197169399375105820974944592307816406286209_ki\n")
modelfile.write("      is_verbose = .false.\n")
modelfile.write("      if(present(verbose)) then\n")
modelfile.write("          is_verbose = verbose\n")
modelfile.write("      end if\n")
modelfile.write("\n")
modelfile.write("      unit = 6 ! stdout\n")
modelfile.write("      if(present(output_unit)) then\n")
modelfile.write("          unit = output_unit\n")
modelfile.write("      end if\n")
modelfile.write("\n")
modelfile.write("\n")
modelfile.write("   write(unit,'(A1,1x,A26)') \"#\", \"--------- SETUP ---------\"\n")
modelfile.write("   write(unit,'(A1,1x,A18,I2)') \"#\", \"renormalisation = \", renormalisation\n")
modelfile.write("   if(convert_to_cdr) then\n")
modelfile.write("      write(unit,'(A1,1x,A9,A3)') \"#\", \"scheme = \", \"CDR\"\n")
modelfile.write("   else\n")
modelfile.write("      write(unit,'(A1,1x,A9,A4)') \"#\", \"scheme = \", \"DRED\"\n")
modelfile.write("   end if\n")
modelfile.write("   if(reduction_interoperation.eq.0) then\n")
modelfile.write("      write(unit,'(A1,1x,A15,A7)') \"#\", \"reduction with \", \"SAMURAI\"\n")
modelfile.write("   else if(reduction_interoperation.eq.1) then\n")
modelfile.write("      write(unit,'(A1,1x,A15,A7)') \"#\", \"reduction with \", \"GOLEM95\"\n")
modelfile.write("   else if(reduction_interoperation.eq.2) then\n")
modelfile.write("      write(unit,'(A1,1x,A15,A15)') \"#\", \"reduction with \", \"NINJA\"\n")
modelfile.write("   else if(reduction_interoperation.eq.3) then\n")
modelfile.write("      write(unit,'(A1,1x,A15,A5)') \"#\", \"reduction with \", \"PJFRY\"\n")
modelfile.write("   end if\n")
modelfile.write("   if(reduction_interoperation_rescue.ne.reduction_interoperation) then\n")
modelfile.write("      if(reduction_interoperation_rescue.eq.0) then\n")
modelfile.write("         write(unit,'(A1,1x,A15,A7)') \"#\", \"    --> rescue \", \"SAMURAI\"\n")
modelfile.write("      else if(reduction_interoperation_rescue.eq.1) then\n")
modelfile.write("         write(unit,'(A1,1x,A15,A7)') \"#\", \"    --> rescue \", \"GOLEM95\"\n")
modelfile.write("      else if(reduction_interoperation_rescue.eq.2) then\n")
modelfile.write("         write(unit,'(A1,1x,A15,A15)') \"#\", \"    --> rescue \", \"NINJA\"\n")
modelfile.write("      else if(reduction_interoperation_rescue.eq.3) then\n")
modelfile.write("         write(unit,'(A1,1x,A15,A5)') \"#\", \"    --> rescue \", \"PJFRY\"\n")
modelfile.write("      end if\n")
modelfile.write("   end if\n")
[$ @if ewchoose $]
modelfile.write("    write(unit,'(A1,1x,A11,I2)') \"#\", \"ewchoice = \", ewchoice\n")[$
@end @if$][$
@select modeltype @case sm smdiag smehc sm_complex smdiag_complex smehc $]
modelfile.write("   write(unit,'(A1,1x,A27)') \"#\", \"--- PARAMETERS Overview ---\"\n")
modelfile.write("   write(unit,'(A1,1x,A22)') \"#\", \"Boson masses & widths:\"\n")
modelfile.write("   write(unit,'(A1,1x,A5,G23.16)') \"#\", \"mZ = \", mZ\n")
modelfile.write("   write(unit,'(A1,1x,A5,G23.16)') \"#\", \"mW = \", mW\n")
modelfile.write("   write(unit,'(A1,1x,A5,G23.16)') \"#\", \"mH = \", mH\n")
modelfile.write("   write(unit,'(A1,1x,A5,G23.16)') \"#\", \"wZ = \", wZ\n")
modelfile.write("   write(unit,'(A1,1x,A5,G23.16)') \"#\", \"wW = \", wW\n")
modelfile.write("   write(unit,'(A1,1x,A5,G23.16)') \"#\", \"wH = \", wH\n")
modelfile.write("   write(unit,'(A1,1x,A20)') \"#\", \"Active light quarks:\"\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"Nf    =\", Nf\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"Nfgen =\", Nfgen\n")
modelfile.write("   write(unit,'(A1,1x,A23)') \"#\", \"Fermion masses & width:\"\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mU   = \", mU\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mD   = \", mD\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mS   = \", mS\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mC   = \", mC\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mB   = \", mB\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mBMS = \", mBMS\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"wB   = \", wB\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mT   = \", mT\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"wT   = \", wT\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"me   = \", me\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mmu  = \", mmu\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"mtau = \", mtau\n")
modelfile.write("   write(unit,'(A1,1x,A7,G23.16)') \"#\", \"wtau = \", wtau\n")
modelfile.write("   write(unit,'(A1,1x,A14)') \"#\", \"Couplings etc.:\"\n")
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"alphaS = \", gs*gs/4._ki/pi\n")
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"gs     = \", gs\n")
[$@if ewchoose $]
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"alpha  = \", alpha\n")
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"e      = \", e\n")
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"GF     = \", GF\n")
[$@end @if $]
[$@select modeltype @case sm_complex smdiag_complex $]
modelfile.write("   write(unit,'(A1,1x,A9,\"(\",G23.16,G23.16,\")\")') \"#\", \"sw     = \", sw\n")
modelfile.write("   write(unit,'(A1,1x,A9,\"(\",G23.16,G23.16,\")\")') \"#\", \"sw2    = \", sw*sw\n")
[$@else $]
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"sw     = \", sw\n")
modelfile.write("   write(unit,'(A1,1x,A9,G23.16)') \"#\", \"sw2    = \", sw*sw\n")
[$ @end @select$]
modelfile.write("   if(is_verbose) then\n")
[$@end @select $]
modelfile.write("   write(unit,'(A1,1x,A21)') \"#\", \"--- ALL PARAMETERS ---\"\n")
[$@for parameters $][$
   @select type @case R $]
modelfile.write("   write(unit,'(A1,1x,A11,G23.16)') \"#\", \"[$$_ convert=str format=%-5s$]= \", [$$_$]\n")
[$@case C $]
modelfile.write("   write(unit,'(A1,1x,A11,\"(\",G23.16,G23.16,\")\")') \"#\", \"[$$_ convert=str format=%-5s$]= \", [$$_$]\n")
[$@case RP $]
modelfile.write("   write(unit,'(A1,1x,A11,G23.16,\"const.\")') \"#\", \"[$$_ convert=str format=%-5s$]= \", [$$_$]\n")
[$@case CP $]
modelfile.write("   write(unit,'(A1,1x,A11,\"(\",G23.16,G23.16,\")\",\"const.\")') \"#\", \"[$$_ convert=str format=%-5s$]= \", [$$_$]\n")
[$@end @select type $][$
@end @for parameters $]
modelfile.write("   if(is_verbose) then\n")
[$
@for functions $][$
   @select type @case R $]
modelfile.write("   write(unit,'(A1,1x,A11,G23.16,\"calc.\")') \"#\", \"[$$_ convert=str format=%-5s$]= \", [$$_$]\n")
[$@case C $]
modelfile.write("   write(unit,'(A1,1x,A11,\"(\",G23.16,G23.16,\")\",\" calc.\")') \"#\", \"[$$_ convert=str format=%-5s$]= \", [$$_$]\n")
[$@end @select type $][$
@end @for functions $]
modelfile.write("   end if\n")
[$@select modeltype @case sm smdiag smehc sm_complex smdiag_complex smehc $]
modelfile.write("   end if\n")
[$@end @select$]
modelfile.write("   write(unit,'(A1,1x,A25)') \"#\", \"-------------------------\"\n")
modelfile.write("   end subroutine\n")
modelfile.write("!---#] print_parameter:\n")

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
modelfile.write("\n")
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
      @select $_ @case mass $][$
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
modelfile.write("\n")
modelfile.write("      integer :: lnr, i, l, ofs, ios\n")
modelfile.write("      character(len=255) :: line\n")
modelfile.write("\n")
modelfile.write("      integer :: block\n")
modelfile.write("\n")
modelfile.write("      ofs = iachar('A') - iachar('a')\n")
modelfile.write("\n")
modelfile.write("      lnr = 0\n")
modelfile.write("      loop1: do\n")
modelfile.write("         read(unit=ch,fmt='(A[$buffer_length$])',iostat=ios) line\n")
modelfile.write("         if(ios .ne. 0) exit\n")
modelfile.write("         lnr = lnr + 1\n")
modelfile.write("\n")
modelfile.write("         i = scan(line, '#', .false.)\n")
modelfile.write("         if (i .eq. 0) then\n")
modelfile.write("            l = len_trim(line)\n")
modelfile.write("         else\n")
modelfile.write("            l = i - 1\n")
modelfile.write("         end if\n")
modelfile.write("\n")
modelfile.write("         if (l .eq. 0) cycle loop1\n")
modelfile.write("\n")
modelfile.write("         ucase: do i = 1, l\n")
modelfile.write("            if (line(i:i) >= 'a' .and. line(i:i) <= 'z') then\n")
modelfile.write("               line(i:i) = achar(iachar(line(i:i))+ofs)\n")
modelfile.write("            end if\n")
modelfile.write("         end do ucase\n")
modelfile.write("\n")
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
modelfile.write("               block = 2\n")
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
modelfile.write("   !  This subroutine reads the 'branching ratios' of\n")
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
modelfile.write("!---#[ subroutine set_parameter\n")
modelfile.write("   recursive subroutine set_parameter(name, re, im, ierr)\n")
modelfile.write("      implicit none\n")
modelfile.write("      real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write("     &3383279502884197169399375105820974944592307816406286209_ki\n")
modelfile.write("      character(len=*), intent(in) :: name\n")
modelfile.write("      real(ki), intent(in) :: re, im\n")
modelfile.write("      integer, intent(out) :: ierr\n")
modelfile.write("\n")
modelfile.write("      integer :: err, pdg, nidx, idx\n")
modelfile.write("      complex(ki) :: tmp\n")
modelfile.write("\n")
modelfile.write("      logical :: must_be_real\n")
modelfile.write("      must_be_real = .false.\n")
modelfile.write("      ierr = 1 ! OK\n")
modelfile.write("\n")[$
@select modeltype @case sm smdiag smehc sm_complex smdiag_complex $][$
@if gs_not_one $]
modelfile.write("      if (name.eq.\"aS\" .or. name.eq.\"alphaS\" .or. name.eq.\"alphas\") then\n")
modelfile.write("         gs = 2.0_ki*sqrt(pi)*sqrt(re)\n")
modelfile.write("         must_be_real = .true.\n")
modelfile.write("      else")[$
@else $]
modelfile.write("     ")[$
@end @if $][$
@if ewchoose $][$ @if alpha_not_one $]
modelfile.write("if (name.eq.\"alphaEW\" .or. name.eq.\"alpha\") then\n")
modelfile.write("         alpha = re\n")
modelfile.write("         must_be_real = .true.\n")
modelfile.write("      else")
[$ @end @if $][$ @end @if$][$
@select modeltype @case sm sm_complex smehc $]
modelfile.write("if (name.eq.\"VV12\") then\n")
modelfile.write("         call set_parameter(\"VUD\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV23\") then\n")
modelfile.write("         call set_parameter(\"VUS\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV25\") then\n")
modelfile.write("         call set_parameter(\"VUB\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV14\") then\n")
modelfile.write("         call set_parameter(\"VCB\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV34\") then\n")
modelfile.write("         call set_parameter(\"VCS\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV35\") then\n")
modelfile.write("         call set_parameter(\"VCS\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV16\") then\n")
modelfile.write("         call set_parameter(\"VTD\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV36\") then\n")
modelfile.write("         call set_parameter(\"VTS\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"VV56\") then\n")
modelfile.write("         call set_parameter(\"VTB\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      else")[$
@end @select $]
modelfile.write("if (name.eq.\"Gf\") then\n")
modelfile.write("         call set_parameter(\"GF\",re,im,ierr)\n")
modelfile.write("         return\n")
modelfile.write("      elseif (name.eq.\"sw2\") then\n")
modelfile.write("         tmp=sqrt(cmplx(re,im,ki))\n")
modelfile.write("         call set_parameter(\"sw\",real(tmp,ki),aimag(tmp),ierr)\n")
modelfile.write("         return\n")
modelfile.write("     else")[$
@end @select $]
modelfile.write("if (name(1:5).eq.\"mass(\" .and. len_trim(name)>=7) then\n")
modelfile.write("         idx = scan(name,\")\",.false.)\n")
modelfile.write("         if (idx.eq.0) then\n")
modelfile.write("            idx=len_trim(name)+1\n")
modelfile.write("         end if\n")
modelfile.write("         read(name(6:idx-1),*, iostat=err) pdg\n")
modelfile.write("         if (err.ne.0) then\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         must_be_real = .true.\n")
modelfile.write("         select case(pdg)\n")
[$@if has_slha_locations $][$
   @for slha_blocks lower $][$
      @select $_ @case mass $][$
         @for slha_entries $]
modelfile.write("            case([$index$])\n")
modelfile.write("               [$ $_ $] = re\n")[$
         @end @for $][$
      @end @select $][$
   @end @for $][$
@end @if $]
modelfile.write("            case default\n")
modelfile.write("               write(*,'(A20,1x,I10)') \"Cannot set mass for PDG code:\", pdg\n")
modelfile.write("               ierr = 0\n")
modelfile.write("               return\n")
modelfile.write("            end select\n")
modelfile.write("     elseif (len_trim(name)>=8 .and. name(1:6).eq.\"width(\") then\n")
modelfile.write("         idx = scan(name,\")\",.false.)\n")
modelfile.write("         if (idx.eq.0) then\n")
modelfile.write("            idx=len_trim(name)+1\n")
modelfile.write("         end if\n")
modelfile.write("         read(name(7:idx-1),*, iostat=err) pdg\n")
modelfile.write("         if (err.ne.0) then\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         must_be_real = .true.\n")
modelfile.write("         select case(pdg)\n")
[$@if has_slha_locations $][$
   @for slha_blocks lower $][$
      @select $_ @case decay $][$
         @for slha_entries $]
modelfile.write("            case([$index$])\n")
modelfile.write("               [$ $_ $] = re\n")[$
         @end @for $][$
      @end @select $][$
   @end @for $][$
@end @if $]
modelfile.write("            case default\n")
modelfile.write("               write(*,'(A20,1x,I10)') \"Cannot set width for PDG code:\", pdg\n")
modelfile.write("               ierr = 0 !FAIL\n")
modelfile.write("               return\n")
modelfile.write("            end select\n")[$
 @if has_slha_locations $][$
   @for slha_blocks upper dimension=1 name=blockname $][$
         @for slha_entries index=idx2 $]
modelfile.write("     elseif (name .eq. \"[$ blockname  $]&&[$ idx2 $]\") then\n")
modelfile.write("               must_be_real = .true.\n")
modelfile.write("               [$ $_ $] = re\n")[$
         @end @for $][$
   @end @for $][$
@end @if $]
modelfile.write("      elseif (name .eq. \"renormalisation\") then\n")
modelfile.write("          if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("             renormalisation = int(re)\n")
modelfile.write("          else\n")
modelfile.write("             ierr=0 !FAIL\n")
modelfile.write("          end if\n")
modelfile.write("      elseif (name .eq. \"nlo_prefactors\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            nlo_prefactors = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
modelfile.write("      elseif (name .eq. \"deltaOS\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            deltaOS = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
modelfile.write("      elseif (name .eq. \"reduction_interoperation\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            reduction_interoperation = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
[$@if extension samurai $]
modelfile.write("      elseif (name .eq. \"samurai_scalar\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            samurai_scalar = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
modelfile.write("      elseif (name .eq. \"samurai_verbosity\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            samurai_verbosity = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
modelfile.write("      elseif (name .eq. \"samurai_test\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            samurai_test = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
modelfile.write("      elseif (name .eq. \"samurai_istop\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            samurai_istop = int(re)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
modelfile.write("      elseif (name .eq. \"samurai_group_numerators\") then\n")
modelfile.write("         if ( real(int(re),ki) == re .and. im == 0.0_ki ) then\n")
modelfile.write("            samurai_group_numerators = (int(re).ne.0)\n")
modelfile.write("         else\n")
modelfile.write("            ierr=0 !FAIL\n")
modelfile.write("         end if\n")
[$@end @if $]
modelfile.write("     elseif (any(names .eq. name)) then\n")
modelfile.write("         do nidx=1,size(names)\n")
modelfile.write("            if (names(nidx) .eq. name) exit\n")
modelfile.write("         end do\n")
modelfile.write("         select case (nidx)\n")
[$ @for parameters R C $]
modelfile.write("         case([$index$])\n")
modelfile.write("            [$ $_ $] = ")
[$@select type @case C$]
modelfile.write("cmplx(re, im, ki)\n")
[$@else $]
modelfile.write("re\n")
[$@end @select $][$@select type @case R$]
modelfile.write("            must_be_real=.true.\n")
[$@end @select$]
[$@end @for$]
modelfile.write("         end select\n")[$
@for parameter_alias real=re $]
modelfile.write("      elseif (name .eq. \"[$ alias $]\") then\n")
modelfile.write("            [$ $_ $] = [$ expr $]\n")
modelfile.write("            must_be_real=.true.\n")[$
@end @for $]
modelfile.write("     else\n")
modelfile.write("         if (name(1:3) /= \"mdl\") then\n")
modelfile.write("            call set_parameter(\"mdl\" // name(4:),re,im,ierr)\n")
modelfile.write("            return\n")
modelfile.write("         end if\n")
modelfile.write("         ierr = 0 !FAIL / UNKNOWN\n")
modelfile.write("     end if\n")
modelfile.write("     if (must_be_real .and. im /= 0.0_ki .and. ierr.eq.1) then\n")
modelfile.write("        ierr = 0 ! FAIL\n")
modelfile.write("     end if\n")
modelfile.write("\n")
[$ @if ewchoose $]
modelfile.write("     if(any(ew_parameters .eq. name) .or. (name.eq.\"mass(23)\") .or. &\n")
modelfile.write("        (name.eq.\"mass(24)\"))  then\n")
modelfile.write("         do nidx=1,size(ew_parameters)\n")
modelfile.write("            if (ew_parameters(nidx) .eq. name) exit\n")
modelfile.write("         end do\n")
modelfile.write("         if(name.eq.\"mass(23)\") then\n")
modelfile.write("            nidx=2\n")
modelfile.write("         elseif(name.eq.\"mass(24)\") then\n")
modelfile.write("            nidx=1\n")
modelfile.write("         end if\n")
modelfile.write("         if (.not. btest(choosen_ew_parameters,nidx)) then\n")
modelfile.write("            choosen_ew_parameters_count = choosen_ew_parameters_count + 1\n")
modelfile.write("            choosen_ew_parameters = ibset(choosen_ew_parameters, nidx)\n")
[$ ' python program to calculate numbers below:\n")
 '   p=['mW','mZ','alpha','GF','sw','e']\n")
 '   print sum([2**(p.index(i.strip())+1) for i in \"GF,mW,mZ\".split(\",\")])\n")
 '   from itertools import combinations\n")
 '   ([sum([2**(p.index(i.strip())+1) for i in j]) for j in combinations(\"GF,mW,mZ\".split(\",\"),2)]) $]
modelfile.write("            if (choosen_ew_parameters_count == 1) then\n")
modelfile.write("               orig_ewchoice = ewchoice\n")
modelfile.write("               if(ewchoice > 0) then\n")
modelfile.write("                 select case(choosen_ew_parameters)\n")
modelfile.write("                      case(2) ! mW\n")
modelfile.write("                        if (ewchoice /= 1 .and. ewchoice /= 2 .and. &\n")
modelfile.write("                            &   ewchoice /= 6) then\n")
modelfile.write("                          ewchoice = 1\n")
modelfile.write("                        end if\n")
modelfile.write("                      case(4) ! mZ\n")
modelfile.write("                        if (ewchoice /= 1 .and. ewchoice /= 2 .and. &\n")
modelfile.write("                            &   ewchoice /= 6) then\n")
modelfile.write("                          ewchoice = 1\n")
modelfile.write("                        end if\n")
modelfile.write("                      case(8) ! alpha\n")
modelfile.write("                        if (ewchoice /= 2 .and. ewchoice /= 3 .and. &\n")
modelfile.write("                            &   ewchoice /= 4 .and. ewchoice /= 5) then\n")
modelfile.write("                          ewchoice = 2\n")
modelfile.write("                        end if\n")
modelfile.write("                      case(16) ! GF\n")
modelfile.write("                        if (ewchoice /= 1 .and. ewchoice /= 4 .and. &\n")
modelfile.write("                            &   ewchoice /= 8) then\n")
modelfile.write("                          ewchoice = 1\n")
modelfile.write("                        end if\n")
modelfile.write("                     case(32) ! sw\n")
modelfile.write("                        if (ewchoice /= 3 .and. ewchoice /= 4 .and. &\n")
modelfile.write("                             &   ewchoice /= 7 .and. ewchoice /= 8) then\n")
modelfile.write("                          ewchoice = 1\n")
modelfile.write("                        end if\n")
[$@if e_not_one$]
modelfile.write("                      case(64) ! e\n")
modelfile.write("                        if (ewchoice < 6) then\n")
modelfile.write("                           ewchoice = 6\n")
modelfile.write("                        end if\n")
[$@end @if$]
modelfile.write("                    end select\n")
modelfile.write("                end if\n")
modelfile.write("            elseif (choosen_ew_parameters_count == 2) then\n")
modelfile.write("                if (choosen_ew_parameters == 18 .or. choosen_ew_parameters == 20 &\n")
modelfile.write("                   & .or. choosen_ew_parameters == 6) then\n")
modelfile.write("                   ewchoice = 1\n")
modelfile.write("                elseif (choosen_ew_parameters == 10 .or. choosen_ew_parameters == 12) then\n")
modelfile.write("                   ewchoice = 2\n")
modelfile.write("                elseif (choosen_ew_parameters == 40 .or. choosen_ew_parameters == 36) then\n")
modelfile.write("                   ewchoice = 3\n")
modelfile.write("                elseif (choosen_ew_parameters == 24 .or. choosen_ew_parameters == 48) then\n")
modelfile.write("                   ewchoice = 4\n")
modelfile.write("                elseif (choosen_ew_parameters == 20) then\n")
modelfile.write("                   ewchoice = 5\n")
[$@if e_not_one$]
modelfile.write("                 elseif (choosen_ew_parameters == 66 .or. choosen_ew_parameters == 68) then\n")
modelfile.write("                   ewchoice = 6\n")
modelfile.write("                 elseif (choosen_ew_parameters == 96) then\n")
modelfile.write("                   ewchoice = 7\n")
modelfile.write("                 elseif (choosen_ew_parameters == 80) then\n")
modelfile.write("                   ewchoice = 8\n")
[$@end @if$]
modelfile.write("                 else\n")
modelfile.write("                 ewchoice = orig_ewchoice\n")
modelfile.write("                 write(*,'(A,1x,I2)') 'Unknown/Invalid EW scheme. Falling back to No.',&\n")
modelfile.write("                                     ewchoice\n")
modelfile.write("                 ierr = 0\n")
modelfile.write("                end if\n")
modelfile.write("            elseif (choosen_ew_parameters_count >= 4) then\n")
modelfile.write("                 write(*,'(A,A,A)') 'EW parameter \"', name, '\" is already determined.'\n")
modelfile.write("                 write(*,'(A)') 'New values are ignored.'\n")
modelfile.write("                 write(*,'(A17,1x,I3)') 'Current EW choice:', ewchoice\n")
modelfile.write("                 ierr = -1 ! IGNORE\n")
modelfile.write("            elseif(choosen_ew_parameters_count == 3) then\n")
modelfile.write("               select case(choosen_ew_parameters)\n")
modelfile.write("                case(22) ! GF,mW,mZ -> e,sw\n")
modelfile.write("                        ewchoice = 1\n")
modelfile.write("                case(14) ! alpha, mW, mZ  -> e,sw\n")
modelfile.write("                        ewchoice = 2\n")
modelfile.write("                case(44) ! alpha, sw, mZ -> e, mW\n")
modelfile.write("                        ewchoice = 3\n")
modelfile.write("                case(56) ! alpha, sw, GF ->  e, mW\n")
modelfile.write("                        ewchoice = 4\n")
modelfile.write("                case(28) ! alpha, GF, mZ ->  e, mW, sw\n")
modelfile.write("                        ewchoice = 5\n")
[$@if e_not_one$]
modelfile.write("                case(70) ! e, mW, mZ -> sw\n")
modelfile.write("                        ewchoice = 6\n")
modelfile.write("                case(100) ! e, sw, mZ -> mW\n")
modelfile.write("                        ewchoice = 7\n")
modelfile.write("                case(112) ! e, sw, GF -> mW, mZ\n")
modelfile.write("                        ewchoice = 8\n")
[$@end @if$]
modelfile.write("                case default\n")
modelfile.write("                 ewchoice = orig_ewchoice\n")
modelfile.write("                 write(*,'(A,1x,I2)') 'Unknown/Invalid EW scheme. Falling back to No.',&\n")
modelfile.write("                                     ewchoice\n")
modelfile.write("                 ierr = 0\n")
modelfile.write("               end select\n")
modelfile.write("            end if\n")
modelfile.write("         end if\n")
modelfile.write("     end if\n")
[$@end @if$]
modelfile.write("\n")
modelfile.write("\n")
modelfile.write("     call init_functions()\n")
modelfile.write("      ! TODO init_color\n")
modelfile.write("   end subroutine\n")
modelfile.write("!---#] subroutine set_parameter\n")




modelfile.write("!---#[ subroutine init_functions:\n")
modelfile.write("   subroutine     init_functions()\n")
modelfile.write("      implicit none\n")
modelfile.write("      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n")
modelfile.write("      real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write("     &3383279502884197169399375105820974944592307816406286209_ki\n")[$
@select modeltype @case sm smdiag sm_complex smdiag_complex smehc $][$
@if ewchoose $]
modelfile.write("      call ewschemechoice(ewchoice)\n")[$
@end @if $][$
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
[$ @select modeltype @case sm smdiag smehc $][$
@if ewchoose $]
modelfile.write("!---#[ EW scheme choice:\n")[$
@if e_not_one $]
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
@else $]
modelfile.write("  subroutine ewschemechoice(ichoice)\n")
modelfile.write("  implicit none\n")
modelfile.write("  integer, intent(in) :: ichoice\n")
modelfile.write("  real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write(" &3383279502884197169399375105820974944592307816406286209_ki\n")
modelfile.write("  ! e is algebraically set to one, do not calculate it here\n")
modelfile.write("  select case (ichoice)\n")
modelfile.write("        case (1)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("        case (2)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("        case (3)\n")
modelfile.write("      ! sw, mZ --> mW\n")
modelfile.write("        mW = mZ*sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case (4)\n")
modelfile.write("      ! GF, sw, alpha --> mW\n")
modelfile.write("        mW = sqrt(alpha*pi/sqrt(2.0_ki)/GF) / sw\n")
modelfile.write("      ! mW, sw --> mZ\n")
modelfile.write("        mZ = mW / sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case(5)\n")
modelfile.write("      ! GF, mZ, alpha --> mW\n")
modelfile.write("      mW = sqrt(mZ*mZ/2.0_ki+sqrt(mZ*mZ*mZ*mZ/4.0_ki-pi*alpha*mZ*mZ/&\n")
modelfile.write("     & sqrt(2.0_ki)/GF))\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("      sw = sqrt(1.0_ki-mW*mW/mZ/mZ)\n")
modelfile.write("  end select\n")
modelfile.write("  end subroutine\n")[$
@end @if$]
modelfile.write("!---#] EW scheme choice:\n")[$
@end @if$][$
@end @select$]
[$ @select modeltype @case sm_complex smdiag_complex  $][$
@if ewchoose $]
modelfile.write("!---#[ EW scheme choice:\n")[$
@if e_not_one $]
modelfile.write("  subroutine ewschemechoice(ichoice)\n")
modelfile.write("  implicit none\n")
modelfile.write("  integer, intent(in) :: ichoice\n")
modelfile.write("  real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write(" &3383279502884197169399375105820974944592307816406286209_ki\n")
modelfile.write("  complex(ki),parameter :: i_ = (0.0_ki, 1.0_ki)\n")
modelfile.write("  select case (ichoice)\n")
modelfile.write("        case (1)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("      ! GF, mW, sw --> e\n")
modelfile.write("        e = sqrt(mW*mW-i_*mW*wW)*sw*sqrt(8.0_ki*GF/sqrt(2.0_ki))\n")
modelfile.write("        case (2)\n")
modelfile.write("      ! alpha --> e\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("        case (3)\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! sw, mZ --> mW\n")
modelfile.write("        mW = sqrt(mZ*mZ-i_*mZ*wZ)*sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case (4)\n")
modelfile.write("      ! alpha --> e\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! GF, sw, alpha --> mW\n")
modelfile.write("        mW = sqrt(alpha*pi/sqrt(2.0_ki)/GF) / sw\n")
modelfile.write("      ! mW, sw --> mZ\n")
modelfile.write("        mZ = sqrt(mW*mW-i_*mW*wW) / sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case (5)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("        case (6)\n")
modelfile.write("      ! mZ, sw --> mW\n")
modelfile.write("        mW = sqrt(mZ*mZ-i_*mZ*wZ)*sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case(7)\n")
modelfile.write("      ! e, sw, GF --> mW\n")
modelfile.write("        mW = e/2.0_ki/sw/sqrt(sqrt(2.0_ki)*GF)\n")
modelfile.write("      ! mW, sw --> mZ\n")
modelfile.write("        mZ = sqrt(mW*mW-i_*mW*wW) / sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case(8)\n")
modelfile.write("      ! alpha --> e\n")
modelfile.write("        e = sqrt(4.0_ki*pi*alpha)\n")
modelfile.write("      ! GF, mZ, alpha --> mW\n")
modelfile.write("      mW = sqrt((mZ*mZ-i_*mZ*wZ)/2.0_ki+sqrt((mZ*mZ-i_*mZ*wZ)**2/4.0_ki-pi*alpha*(mZ*mZ-i_*mZ*wZ)/&\n")
modelfile.write("     & sqrt(2.0_ki)/GF))\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("      sw = sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("!        case default\n")
modelfile.write("  end select\n")
modelfile.write("  end subroutine\n")[$
@else $]
modelfile.write("  subroutine ewschemechoice(ichoice)\n")
modelfile.write("  implicit none\n")
modelfile.write("  integer, intent(in) :: ichoice\n")
modelfile.write("  real(ki), parameter :: pi = 3.14159265358979323846264&\n")
modelfile.write(" &3383279502884197169399375105820974944592307816406286209_ki\n")
modelfile.write("  complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n")
modelfile.write("  ! e is algebraically set to one, do not calculate it here\n")
modelfile.write("  select case (ichoice)\n")
modelfile.write("        case (1)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("        case (2)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("        case (3)\n")
modelfile.write("      ! sw, mZ --> mW\n")
modelfile.write("        mW = sqrt(mZ*mZ-i_*mZ*wZ)*sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case (4)\n")
modelfile.write("      ! GF, sw, alpha --> mW\n")
modelfile.write("        mW = sqrt(alpha*pi/sqrt(2.0_ki)/GF) / sw\n")
modelfile.write("      ! mW, sw --> mZ\n")
modelfile.write("        mZ = sqrt(mW*mW-i_*mW*wW) / sqrt(1.0_ki-sw*sw)\n")
modelfile.write("        case(5)\n")
modelfile.write("      ! GF, mZ, alpha --> mW\n")
modelfile.write("        mW = sqrt((mZ*mZ-i_*mZ*wZ)/2.0_ki+sqrt((mZ*mZ-i_*mZ*wZ)**2/4.0_ki-pi*alpha*(mZ*mZ-i_*mZ*wZ)/&\n")
modelfile.write("     & sqrt(2.0_ki)/GF))\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("        case(6)\n")
modelfile.write("      ! mW, mZ --> sw\n")
modelfile.write("        sw = sqrt(1.0_ki-(mW*mW-i_*mW*wW)/(mZ*mZ-i_*mZ*wZ))\n")
modelfile.write("        case(7)\n")
modelfile.write("      ! mZ, sw --> mW\n")
modelfile.write("        mW = sqrt(mZ*mZ-i_*mZ*wZ)*sqrt(1.0_ki-sw*sw)\n")
modelfile.write("  end select\n")\n")
modelfile.write("  end subroutine\n")[$
@end @if$]
modelfile.write("!---#] EW scheme choice:\n")[$
@end @if$][$
@end @select$]
modelfile.write("end module [$ process_name asprefix=\_ $]model\n")

modelfile.close()
### additional formatting for output files

postformat('model.f90')

