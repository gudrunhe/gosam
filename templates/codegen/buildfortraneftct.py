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
print('Diagram written in: %s' % 'diagramsct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90')
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
%]outdict=translatefile('eft_ct.txt',config)[% @end @if %]
f90file.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'ct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]\n')
f90file.write('   ! file: '+str(os.getcwd())+'diagramsct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90 \n')
f90file.write('   ! generator: buildfortraneftct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].py \n')
f90file.write('   use [% process_name asprefix=\_ %]color, only: numcs\n')
f90file.write('   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private :: reglog\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file.write('   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki\n')
f90file.write('   public :: amplitude\n')
f90file.write('\n')
f90file.write('contains\n')
f90file.write('!---#[ function amplitude:\n')
f90file.write('   function amplitude(logs,scale2)\n')
f90file.write('      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]color\n')
f90file.write('      use [% process_name asprefix=\_ %]util, only: inspect_lo_diagram\n')
f90file.write('      implicit none\n')
f90file.write('      complex(ki), dimension(-1:0,numcs) :: amplitude\n')
f90file.write('      complex(ki), dimension(-1:0,'+str(abb_max)+') :: abb\n')
f90file.write('!      complex(ki), dimension(2,numcs) :: diagrams\n')
f90file.write('      integer :: i, ii, jj\n')
f90file.write('      real(ki) :: eftlog, scale2\n')
f90file.write('      logical :: logs\n')
f90file.write('\n')
f90file.write('      if (logs) then\n')
f90file.write('         eftlog = reglog(scale2/mdlmueft/mdlmueft)\n')
f90file.write('      else\n')
f90file.write('         eftlog = 0.0_ki\n')
f90file.write('      end if\n')
f90file.write('\n')
f90file.write('      amplitude(:,:) = 0.0_ki\n')
f90file.write('      abb(:,:) = 0.0_ki\n')
f90file.write('\n')
f90file.write('\n')
newabbr = re.sub(r"abb\(([0-9]*)\)",r"abb(-1,\1)",outdict['Abbreviations'])
newabbr = re.sub(r"mdl([a-zA-Z0-9]*)eftctcpl",r"(mdl\1(-1))",newabbr)
f90file.write(newabbr)
newabbr = re.sub(r"abb\(([0-9]*)\)",r"abb(0,\1)",outdict['Abbreviations'])
newabbr = re.sub(r"mdl([a-zA-Z0-9]*)eftctcpl",r"(mdl\1(0)+eftlog*mdl\1(-1))",newabbr)
f90file.write(newabbr)
f90file.write('\n')
f90file.write('      do ii=-1,0\n')
f90file.write('         do jj=1,numcs\n')
newdiags = re.sub(r"amplitude",r"            amplitude(ii,jj)",outdict['Diagrams'])
newdiags = re.sub(r"abb\(([0-9]*)\)",r"abb(ii,\1)",newdiags)
newdiags = re.sub(r"([ \t\-+*=])c([0-9]*)\*",r"\1c\2(jj)*",newdiags)
f90file.write(newdiags)
f90file.write('         end do\n')
f90file.write('      end do\n')
f90file.write('\n')
f90file.write('   end function amplitude\n')
f90file.write('!---#] function amplitude:\n')
f90file.write('!---#[ function reglog:\n')
f90file.write('   function reglog(r)\n')
f90file.write('      implicit none\n')
f90file.write('      real(ki) :: reglog, r\n')
f90file.write('\n')
f90file.write('      if (r.le.0.0_ki) then\n')
f90file.write('         reglog = 0.0_ki\n')
f90file.write('      else\n')
f90file.write('         reglog = log(r)\n')
f90file.write('      end if\n')
f90file.write('\n')
f90file.write('   end function reglog\n')
f90file.write('!---#] function reglog:\n')
f90file.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'ct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]\n')
f90file.close()
[% @if extension quadruple %]
f90file_qp.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'ct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp\n')
f90file_qp.write('   ! file: '+str(os.getcwd())+'diagramsct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp.f90 \n')
f90file_qp.write('   ! generator: buildfortraneftct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].py \n')
f90file_qp.write('   use [% process_name asprefix=\_ %]color_qp, only: numcs\n')
f90file_qp.write('   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file_qp.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file_qp.write('\n')
f90file_qp.write('   implicit none\n')
f90file_qp.write('   private :: reglog\n')
f90file_qp.write('\n')
f90file_qp.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file_qp.write('   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki\n')
f90file_qp.write('   public :: amplitude\n')
f90file_qp.write('\n')
f90file_qp.write('contains\n')
f90file_qp.write('!---#[ function amplitude:\n')
f90file_qp.write('   function amplitude(logs,scale2)\n')
f90file_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]color_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]util_qp, only: inspect_lo_diagram\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      complex(ki), dimension(-1:0,numcs) :: amplitude\n')
f90file_qp.write('      complex(ki), dimension(-1:0,'+str(abb_max)+') :: abb\n')
f90file_qp.write('!      complex(ki), dimension(2,numcs) :: diagrams\n')
f90file_qp.write('      integer :: i, ii, jj\n')
f90file_qp.write('      real(ki) :: eftlog, scale2\n')
f90file_qp.write('      logical :: logs\n')
f90file_qp.write('\n')
f90file_qp.write('      if (logs) then\n')
f90file_qp.write('         eftlog = reglog(scale2/mdlmueft/mdlmueft)\n')
f90file_qp.write('      else\n')
f90file_qp.write('         eftlog = 0.0_ki\n')
f90file_qp.write('      end if\n')
f90file_qp.write('\n')
f90file_qp.write('      amplitude(:,:) = 0.0_ki\n')
f90file_qp.write('      abb(:,:) = 0.0_ki\n')
f90file_qp.write('\n')
f90file_qp.write('\n')
newabbr = re.sub(r"abb\(([0-9]*)\)",r"abb(-1,\1)",outdict['Abbreviations'])
newabbr = re.sub(r"mdl([a-zA-Z0-9]*)eftctcpl",r"(mdl\1(-1))",newabbr)
f90file_qp.write(newabbr)
newabbr = re.sub(r"abb\(([0-9]*)\)",r"abb(0,\1)",outdict['Abbreviations'])
newabbr = re.sub(r"mdl([a-zA-Z0-9]*)eftctcpl",r"(mdl\1(0)+eftlog*mdl\1(-1))",newabbr)
f90file_qp.write(newabbr)
f90file_qp.write('\n')
f90file_qp.write('      do ii=-1,0\n')
f90file_qp.write('         do jj=1,numcs\n')
newdiags = re.sub(r"amplitude",r"            amplitude(ii,jj)",outdict['Diagrams'])
newdiags = re.sub(r"abb\(([0-9]*)\)",r"abb(ii,\1)",newdiags)
newdiags = re.sub(r"([ \t\-+*=])c([0-9]*)\*",r"\1c\2(jj)*",newdiags)
f90file_qp.write(newdiags)
f90file_qp.write('         end do\n')
f90file_qp.write('      end do\n')
f90file_qp.write('\n')
f90file_qp.write('   end function     amplitude\n')
f90file_qp.write('!---#] function amplitude:\n')
f90file_qp.write('!---#[ function reglog:\n')
f90file_qp.write('   function reglog(r)\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      real(ki) :: reglog, r\n')
f90file_qp.write('\n')
f90file_qp.write('      if (r.le.0.0_ki) then\n')
f90file_qp.write('         reglog = 0.0_ki\n')
f90file_qp.write('      else\n')
f90file_qp.write('         reglog = log(r)\n')
f90file_qp.write('      end if\n')
f90file_qp.write('\n')
f90file_qp.write('   end function reglog\n')
f90file_qp.write('!---#] function reglog:\n')
f90file_qp.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'ct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp\n')
f90file_qp.close()
[% @end @if extension quadruple %]
txtfile.close()

### additional formatting for output files

postformat(tmpname)
[% @if extension quadruple %]
postformat(tmpname_qp)
[% @end @if extension quadruple %]
shutil.move(tmpname,'diagramsct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90')
[% @if extension quadruple %]
shutil.move(tmpname_qp,'diagramsct[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp.f90')
[% @end @if extension quadruple %]
