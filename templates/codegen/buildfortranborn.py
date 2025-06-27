#! /usr/bin/env python3
# vim: ts=3:sw=3:expandtab

import sys
import os
import re
from optparse import OptionParser
from t2f import translatefile, getdata, postformat
from pythonin import parameters, kinematics, symbols, lambdafunc, dotproducts
import tempfile, shutil

config={'parameters' : parameters,
        'kinematics' : kinematics,
        'symbols' : symbols,
        'lambdafunc' : lambdafunc,
        'dotproducts' : dotproducts}

parser = OptionParser()

parser.add_option("-i", "--input", dest="input",
                  action="store", type="string",
                  help="input file", metavar="INPUT")

parser.add_option("-H", "--HELICITY", dest="helicity",
                  action="store", type="int",
                  help="helicity number", metavar="HELICITY")

(options, args) = parser.parse_args()

if not options.input:
    sys.exit("Error: no input file was found! Please specify one with the -i options.")

file_name= options.input.split('.')[0]
heli=options.helicity

print('----------------------------------')
print('Input file is:      %s' % file_name+'.txt')
print('Diagram written in: %s' % 'diagramsl0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90')
print('----------------------------------')

txtfile = open(file_name+'.txt','r')
tmp_handle , tmpname = tempfile.mkstemp(suffix=".f90",prefix="gosam_tmp")
f90file = os.fdopen(tmp_handle,"w")
[% @if extension quadruple %]
tmp_handle_qp , tmpname_qp = tempfile.mkstemp(suffix="_qp.f90",prefix="gosam_tmp")
f90file_qp = os.fdopen(tmp_handle_qp,"w")
[% @end @if extension quadruple %]
datfilename = file_name + '.dat'

# import txt file
txt_lines=[]
abb_max=getdata(datfilename)['abbrev_terms']

[% @if enable_truncation_orders
%]outdict=translatefile(file_name+'.txt',config)[% @else
%]outdict=translatefile('born.txt',config)[% @end @if %]
f90file.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]\n')
f90file.write('   ! file: '+str(os.getcwd())+'diagramsl0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90 \n')
f90file.write('   ! generator: buildfortranborn[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].py \n')
f90file.write('   use [% process_name asprefix=\_ %]color, only: numcs\n')
f90file.write('   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private :: bornamplitude\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file.write('   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki\n')
f90file.write('   public :: amplitude, amplitude_Dym\n')
f90file.write('\n')
f90file.write('contains\n')
f90file.write('!---#[ function amplitude:\n')
f90file.write('   function amplitude()\n')
f90file.write('      implicit none\n')
f90file.write('      complex(ki), dimension(numcs) :: amplitude\n')
f90file.write('\n')
f90file.write('      amplitude = bornamplitude(.false., -1.0_ki, 0)\n')
f90file.write('\n')
f90file.write('   end function     amplitude\n')
f90file.write('!---#] function amplitude:\n')
f90file.write('!---#[ function amplitude_Dym:\n')
f90file.write('   function amplitude_Dym(scale2, eps)\n')
f90file.write('      implicit none\n')
f90file.write('      complex(ki), dimension(numcs) :: amplitude_Dym\n')
f90file.write('      real(ki) :: scale2\n')
f90file.write('      integer :: eps\n')
f90file.write('\n')
f90file.write('      amplitude_Dym = bornamplitude(.true., scale2, eps)\n')
f90file.write('\n')
f90file.write('   end function     amplitude_Dym\n')
f90file.write('!---#] function amplitude_Dym:\n')
f90file.write('!---#[ function bornamplitude:\n')
f90file.write('   function bornamplitude(renorm, scale2, eps) result(amplitude)\n')
f90file.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]color\n')
f90file.write('      use [% process_name asprefix=\_ %]counterterms\n')
f90file.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: renormalisation, renorm_logs, &\n')
f90file.write('        & renorm_mqse, renorm_yukawa, renorm_gamma5\n')
f90file.write('      use [% process_name asprefix=\_ %]util, only: inspect_lo_diagram\n')
f90file.write('      implicit none\n')
f90file.write('      complex(ki), dimension(numcs) :: amplitude\n')
f90file.write('      complex(ki), dimension('+str(abb_max)+') :: abb\n')
f90file.write('      integer :: i, eps\n')
f90file.write('      real(ki) :: CYUKAWA, CMASS, CFR5, XCT, scale2\n')
f90file.write('      logical :: renorm\n')
f90file.write('\n')
f90file.write('      amplitude(:) = 0.0_ki\n')
f90file.write('\n')
f90file.write('      if (renorm) then\n')
f90file.write('         XCT = 1.0_ki\n')
f90file.write('         select case (renormalisation)\n')
f90file.write('            case (0)\n')
f90file.write('               ! No renormalistion. This case is only here for completeness and never actually used.\n')
f90file.write('               return\n')
f90file.write('            case (1)\n')
f90file.write('               if (renorm_yukawa) then\n')
f90file.write('                  CYUKAWA = 1.0_ki\n')
f90file.write('               else\n')
f90file.write('                  CYUKAWA = 0.0_ki\n')
f90file.write('               end if\n')
f90file.write('               if (renorm_mqse) then\n')
f90file.write('                  CMASS = 1.0_ki\n')
f90file.write('               else\n')
f90file.write('                  CMASS = 0.0_ki\n')
f90file.write('               end if\n')
f90file.write('               if (renorm_gamma5) then\n')
f90file.write('                  CFR5 = 1.0_ki\n')
f90file.write('               else\n')
f90file.write('                  CFR5 = 0.0_ki\n')
f90file.write('               end if\n')
f90file.write('            case (2)\n')
f90file.write('               CYUKAWA = 0.0_ki\n')
f90file.write('               CMASS = 0.0_ki\n')
f90file.write('               CFR5 = 1.0_ki\n')
f90file.write('            case (3)\n')
f90file.write('               CYUKAWA = 0.0_ki\n')
f90file.write('               CMASS = 1.0_ki\n')
f90file.write('               CFR5 = 0.0_ki\n')
f90file.write('            case (4)\n')
f90file.write('               ! Quark mass renormalisation the old way. This case is only here for completeness and never actually used.\n')
f90file.write('               return\n')
f90file.write('            case default\n')
f90file.write('               print *, \"ERROR: In function bornamplitude: unkown case for renormalisation.\"\n')
f90file.write('               stop\n')
f90file.write('         end select\n')
f90file.write('      else\n')
f90file.write('         XCT = 0.0_ki\n')
f90file.write('         CYUKAWA = 0.0_ki\n')
f90file.write('         CMASS = 0.0_ki\n')
f90file.write('         CFR5 = 0.0_ki\n')
f90file.write('      end if\n')
f90file.write('\n')
f90file.write('\n')
newabbr = re.sub(r"DELTAYUKOS([a-zA-Z0-9]*)",r"counterterm_yukawa_OS(renorm,eps,scale2,\1)",outdict['Abbreviations'])
newabbr = re.sub(r"DELTAYUKMSbar([a-zA-Z0-9]*)",r"counterterm_yukawa_MSbar(renorm,eps)",newabbr)
newabbr = re.sub(r"DELTAMASSOS([a-zA-Z0-9]*)",r"counterterm_mass_OS(renorm,eps,scale2,\1)",newabbr)
newabbr = re.sub(r"deltaaxial",r"counterterm_fr5(renorm,eps)",newabbr)
f90file.write(newabbr)
f90file.write('\n')
f90file.write(outdict['Diagrams'])
f90file.write('\n')
f90file.write('   end function     bornamplitude\n')
f90file.write('!---#] function bornamplitude:\n')
f90file.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]\n')
f90file.close()
[% @if extension quadruple %]
f90file_qp.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp\n')
f90file_qp.write('   ! file: '+str(os.getcwd())+'diagramsl0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp.f90 \n')
f90file_qp.write('   ! generator: buildfortranborn[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].py \n')
f90file_qp.write('   use [% process_name asprefix=\_ %]color_qp, only: numcs\n')
f90file_qp.write('   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki => ki_qp\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file_qp.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file_qp.write('\n')
f90file_qp.write('   implicit none\n')
f90file_qp.write('   private :: bornamplitude\n')
f90file_qp.write('\n')
f90file_qp.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file_qp.write('   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki\n')
f90file_qp.write('   public :: amplitude, amplitude_Dym\n')
f90file_qp.write('\n')
f90file_qp.write('contains\n')
f90file_qp.write('!---#[ function amplitude:\n')
f90file_qp.write('   function amplitude()\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      complex(ki), dimension(numcs) :: amplitude\n')
f90file_qp.write('\n')
f90file_qp.write('      amplitude = bornamplitude(.false., -1.0_ki, 0)\n')
f90file_qp.write('\n')
f90file_qp.write('   end function     amplitude\n')
f90file_qp.write('!---#] function amplitude:\n')
f90file_qp.write('!---#[ function amplitude_Dym:\n')
f90file_qp.write('   function amplitude_Dym(scale2, eps)\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      complex(ki), dimension(numcs) :: amplitude_Dym\n')
f90file_qp.write('      real(ki) :: scale2\n')
f90file_qp.write('      integer :: eps, renorm_mode\n')
f90file_qp.write('\n')
f90file_qp.write('      amplitude_Dym = bornamplitude(.true., scale2, eps)\n')
f90file_qp.write('\n')
f90file_qp.write('   end function     amplitude_Dym\n')
f90file_qp.write('!---#] function amplitude_Dym:\n')
f90file_qp.write('!---#[ function bornamplitude:\n')
f90file_qp.write('   function bornamplitude(renorm, scale2, eps) result(amplitude)\n')
f90file_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]color_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]counterterms_qp\n')
f90file_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: renormalisation, renorm_logs, &\n')
f90file_qp.write('        & renorm_mqse, renorm_yukawa, renorm_gamma5\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]util_qp, only: inspect_lo_diagram\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      complex(ki), dimension(numcs) :: amplitude\n')
f90file_qp.write('      complex(ki), dimension('+str(abb_max)+') :: abb\n')
f90file_qp.write('!      complex(ki), dimension(2,numcs) :: diagrams\n')
f90file_qp.write('      integer :: i, eps\n')
f90file_qp.write('      real(ki) :: CYUKAWA, CMASS, CFR5, XCT, scale2\n')
f90file_qp.write('      logical :: renorm\n')
f90file_qp.write('\n')
f90file_qp.write('      amplitude(:) = 0.0_ki\n')
f90file_qp.write('\n')
f90file_qp.write('      if (renorm) then\n')
f90file_qp.write('         XCT = 1.0_ki\n')
f90file_qp.write('         select case (renormalisation)\n')
f90file_qp.write('            case (0)\n')
f90file_qp.write('               ! No renormalistion. This case is only here for completeness and never actually used.\n')
f90file_qp.write('               return\n')
f90file_qp.write('            case (1)\n')
f90file_qp.write('               if (renorm_yukawa) then\n')
f90file_qp.write('                  CYUKAWA = 1.0_ki\n')
f90file_qp.write('               else\n')
f90file_qp.write('                  CYUKAWA = 0.0_ki\n')
f90file_qp.write('               end if\n')
f90file_qp.write('               if (renorm_mqse) then\n')
f90file_qp.write('                  CMASS = 1.0_ki\n')
f90file_qp.write('               else\n')
f90file_qp.write('                  CMASS = 0.0_ki\n')
f90file_qp.write('               end if\n')
f90file_qp.write('               if (renorm_gamma5) then\n')
f90file_qp.write('                  CFR5= 1.0_ki\n')
f90file_qp.write('               else\n')
f90file_qp.write('                  CFR5 = 0.0_ki\n')
f90file_qp.write('               end if\n')
f90file_qp.write('            case (2)\n')
f90file_qp.write('               CYUKAWA = 0.0_ki\n')
f90file_qp.write('               CMASS = 0.0_ki\n')
f90file_qp.write('               CFR5 = 1.0_ki\n')
f90file_qp.write('            case (3)\n')
f90file_qp.write('               CYUKAWA = 0.0_ki\n')
f90file_qp.write('               CMASS = 1.0_ki\n')
f90file_qp.write('               CFR5 = 0.0_ki\n')
f90file_qp.write('            case (4)\n')
f90file_qp.write('               ! Quark mass renormalisation the old way. This case is only here for completeness and never actually used.\n')
f90file_qp.write('               return\n')
f90file_qp.write('            case default\n')
f90file_qp.write('               print *, \"ERROR: In function bornamplitude: unkown case for renormalisation.\"\n')
f90file_qp.write('               stop\n')
f90file_qp.write('         end select\n')
f90file_qp.write('      else\n')
f90file_qp.write('         XCT = 0.0_ki\n')
f90file_qp.write('         CYUKAWA = 0.0_ki\n')
f90file_qp.write('         CMASS = 0.0_ki\n')
f90file_qp.write('         CFR5 = 0.0_ki\n')
f90file_qp.write('      end if\n')
f90file_qp.write('\n')
f90file_qp.write('\n')
newabbr = re.sub(r"DELTAYUKOS([a-zA-Z0-9]*)",r"counterterm_yukawa_OS(renorm,eps,scale2,\1)",outdict['Abbreviations'])
newabbr = re.sub(r"DELTAYUKMSbar([a-zA-Z0-9]*)",r"counterterm_yukawa_MSbar(renorm,eps)",newabbr)
newabbr = re.sub(r"DELTAMASSOS([a-zA-Z0-9]*)",r"counterterm_mass_OS(renorm,eps,scale2,\1)",newabbr)
newabbr = re.sub(r"deltaaxial",r"counterterm_fr5(renorm,eps)",newabbr)
f90file_qp.write(newabbr)
f90file_qp.write('\n')
f90file_qp.write(outdict['Diagrams'])
f90file_qp.write('\n')
f90file_qp.write('   end function     bornamplitude\n')
f90file_qp.write('!---#] function bornamplitude:\n')
f90file_qp.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp\n')
f90file_qp.close()
[% @end @if extension quadruple %]
txtfile.close()

### additional formatting for output files

postformat(tmpname)
[% @if extension quadruple %]
postformat(tmpname_qp)
[% @end @if extension quadruple %]
shutil.move(tmpname,'diagramsl0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90')
[% @if extension quadruple %]
shutil.move(tmpname_qp,'diagramsl0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp.f90')
[% @end @if extension quadruple %]
