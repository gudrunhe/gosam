#! /usr/bin/env python3
# vim: ts=3:sw=3:expandtab

import sys
import os
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
print('Diagram written in: %s' % 'diagramsl0.f90')
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

# outdict=translatefile('born.txt',config)
outdict=translatefile(file_name+'.txt',config)
f90file.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0_0\n')
f90file.write('   ! file: '+str(os.getcwd())+'diagramsl0_0.f90 \n')
f90file.write('   ! generator: buildfortranborn.py \n')
f90file.write('   use [% process_name asprefix=\_ %]color, only: numcs\n')
f90file.write('   use [% process_name asprefix=\_ %]config, only: ki\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file.write('   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki\n')
f90file.write('   public :: amplitude\n')
f90file.write('\n')
f90file.write('contains\n')
f90file.write('!---#[ function amplitude:\n')
f90file.write('   function amplitude()\n')
f90file.write('      use [% process_name asprefix=\_ %]model\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]color\n')
f90file.write('      use [% process_name asprefix=\_ %]config, only: debug_lo_diagrams, &\n')
f90file.write('        & use_sorted_sum\n')
f90file.write('      use [% process_name asprefix=\_ %]accu, only: sorted_sum\n')
f90file.write('      use [% process_name asprefix=\_ %]util, only: inspect_lo_diagram\n')
f90file.write('      implicit none\n')
f90file.write('      complex(ki), dimension(numcs) :: amplitude\n')
f90file.write('      complex(ki), dimension('+str(abb_max)+') :: abb\n')
f90file.write('!      complex(ki), dimension(2,numcs) :: diagrams\n')
f90file.write('      integer :: i\n')
f90file.write('\n')
f90file.write('      amplitude(:) = 0.0_ki\n')
f90file.write('\n')
f90file.write('\n')
f90file.write(outdict['Abbreviations'])
f90file.write('\n')
f90file.write(outdict['Diagrams'])
f90file.write('\n')
f90file.write('      if (debug_lo_diagrams) then\n')
f90file.write('         write(*,*) "Using Born optimization, debug_lo_diagrams not implemented."\n')
f90file.write('      end if\n')
f90file.write('\n')
f90file.write('!      if (use_sorted_sum) then\n')
f90file.write('!         do i=1,numcs\n')
f90file.write('!            amplitude(i) = sorted_sum(diagrams(i))\n')
f90file.write('!         end do\n')
f90file.write('!      else\n')
f90file.write('!         do i=1,numcs\n')
f90file.write('!            amplitude(i) = sum(diagrams(i))\n')
f90file.write('!         end do\n')
f90file.write('!      end if\n')
f90file.write('   end function     amplitude\n')
f90file.write('!---#] function amplitude:\n')
f90file.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0_0\n')
f90file.close()
[% @if extension quadruple %]
f90file_qp.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0_qp\n')
f90file_qp.write('   ! file: '+str(os.getcwd())+'diagramsl0_0_qp.f90 \n')
f90file_qp.write('   ! generator: buildfortranborn_0.py \n')
f90file_qp.write('   use [% process_name asprefix=\_ %]color_qp, only: numcs\n')
f90file_qp.write('   use [% process_name asprefix=\_ %]config, only: ki => ki_qp\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file_qp.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file_qp.write('\n')
f90file_qp.write('   implicit none\n')
f90file_qp.write('   private\n')
f90file_qp.write('\n')
f90file_qp.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file_qp.write('   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki\n')
f90file_qp.write('   public :: amplitude\n')
f90file_qp.write('\n')
f90file_qp.write('contains\n')
f90file_qp.write('!---#[ function amplitude:\n')
f90file_qp.write('   function amplitude()\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]model_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]color_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]config, only: debug_lo_diagrams, &\n')
f90file_qp.write('        & use_sorted_sum\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]accu_qp, only: sorted_sum\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]util_qp, only: inspect_lo_diagram\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      complex(ki), dimension(numcs) :: amplitude\n')
f90file_qp.write('      complex(ki), dimension('+str(abb_max)+') :: abb\n')
f90file_qp.write('!      complex(ki), dimension(2,numcs) :: diagrams\n')
f90file_qp.write('      integer :: i\n')
f90file_qp.write('\n')
f90file_qp.write('      amplitude(:) = 0.0_ki\n')
f90file_qp.write('\n')
f90file_qp.write('\n')
f90file_qp.write(outdict['Abbreviations'])
f90file_qp.write('\n')
f90file_qp.write(outdict['Diagrams'])
f90file_qp.write('\n')
f90file_qp.write('      if (debug_lo_diagrams) then\n')
f90file_qp.write('         write(*,*) "Using Born optimization, debug_lo_diagrams not implemented."\n')
f90file_qp.write('      end if\n')
f90file_qp.write('\n')
f90file_qp.write('!      if (use_sorted_sum) then\n')
f90file_qp.write('!         do i=1,numcs\n')
f90file_qp.write('!            amplitude(i) = sorted_sum(diagrams(i))\n')
f90file_qp.write('!         end do\n')
f90file_qp.write('!      else\n')
f90file_qp.write('!         do i=1,numcs\n')
f90file_qp.write('!            amplitude(i) = sum(diagrams(i))\n')
f90file_qp.write('!         end do\n')
f90file_qp.write('!      end if\n')
f90file_qp.write('   end function     amplitude\n')
f90file_qp.write('!---#] function amplitude:\n')
f90file_qp.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0_0_qp\n')
f90file_qp.close()
[% @end @if extension quadruple %]
txtfile.close()

### additional formatting for output files

postformat(tmpname)
[% @if extension quadruple %]
postformat(tmpname_qp)
[% @end @if extension quadruple %]
shutil.move(tmpname,'diagramsl0_0.f90')
[% @if extension quadruple %]
shutil.move(tmpname_qp,'diagramsl0_0_qp.f90')
[% @end @if extension quadruple %]
