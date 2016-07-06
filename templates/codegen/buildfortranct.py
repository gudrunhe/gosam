#! /usr/bin/env python
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

def corr_dim_abbrev(abbrev):
  match=re.findall(r'ctabb\(\d+\)',abbrev)
  new_abbrev=[]
  for element in match:
    new_abbrev.append(element.replace(')',',:)'))
  for (i,j) in zip(match,new_abbrev):
    abbrev=abbrev.replace(i,j)

  match=re.findall(r'UV\w+\d+',abbrev) or re.findall(r'gct\w+',abbrev)[%
@if generate_ct_internal %]
  new_abbrev=[]
  for element in match:
      if not (element+'(:)' in new_abbrev):
        element=element.replace('gct','g1ct')
	new_abbrev.append(element.replace(element,element+'(:)'))  
  match.sort()
  match.reverse()
  new_abbrev.sort()
  new_abbrev.reverse()
  
  for element in new_abbrev:
    try:
      i= new_abbrev.index(element)
      abbrev=abbrev.replace(match[i],new_abbrev[i])
    except ValueError:
      pass
  abbrev=abbrev.replace('g1ct','gct')[%
@else %]  
  new_abbrev=[]
  for element in match:
      if not (element+'(:)' in new_abbrev):
	new_abbrev.append(element.replace(element,element+'(:)'))

  for element in match:
    try:
      i= new_abbrev.index(element+'(:)')
      abbrev=abbrev.replace(element,new_abbrev[i])
      del new_abbrev[i]
    except ValueError:
      pass[%
@end @if %]           
    
  return abbrev
    
def corr_dim_diag(diag,i):
  diag=diag.replace('ctamplitude','  ctamplitude(:,'+i+')')
  match=re.findall(r'ctabb\(\d+\)',diag)
  new_diag=[]
  for element in match:
    new_diag.append(element.replace(')',','+i+')'))
  for (i,j) in zip(match,new_diag):
    diag=diag.replace(i,j)  
  
  return diag
  
file_name= options.input.split('.')[0]
heli=options.helicity

print '----------------------------------'
print 'Input file is:      %s' % file_name+'.txt'
print 'Diagram written in: %s' % 'diagramsct.f90'
print '----------------------------------'

txtfile = open(file_name+'.txt','r')
tmp_handle , tmpname = tempfile.mkstemp(suffix=".f90",prefix="gosam_tmp")
f90file = os.fdopen(tmp_handle,"w")
datfilename = file_name + '.dat'

# import txt file
txt_lines=[]
abb_max=getdata(datfilename)['ctabbrev_terms']

outdict=translatefile('ct.txt',config)
f90file.write('module     [% process_name asprefix=\_ %]ctdiagramsh'+str(heli)+'l0\n')
f90file.write('   ! file: '+str(os.getcwd())+'/diagramsct.f90 \n')
f90file.write('   ! generator: buildfortranct.py \n')
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
f90file.write('   public :: ctamplitude\n')
f90file.write('\n')
f90file.write('contains\n')
f90file.write('!---#[ function ctamplitude:\n')
f90file.write('   function ctamplitude()\n')
f90file.write('      use [% process_name asprefix=\_ %]model\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]color\n')
f90file.write('      use [% process_name asprefix=\_ %]config, only: debug_lo_diagrams, &\n')
f90file.write('        & use_sorted_sum\n')
f90file.write('      use [% process_name asprefix=\_ %]accu, only: sorted_sum\n')
f90file.write('      use [% process_name asprefix=\_ %]util, only: inspect_lo_diagram\n')[%
@if generate_ct_internal %]
f90file.write('      use [% process_name asprefix=\_ %]ew_ct\n')[%
@end @if %]  
f90file.write('      implicit none\n')[%
@if generate_ct_internal %]
f90file.write('      include "../common/dzdecl.h"\n')      
f90file.write('      include "../common/declscalars.h"\n')
f90file.write('      include "../common/realparam.h"\n')[%
@end @if %]  
f90file.write('      complex(ki), dimension(numcs,0:1) :: ctamplitude\n')
f90file.write('      complex(ki), dimension('+str(abb_max)+',0:1) :: ctabb\n')
f90file.write('!      complex(ki), dimension(2,numcs) :: diagrams\n')
f90file.write('      integer :: i\n')
f90file.write('\n')
f90file.write('      ctamplitude(:,:) = 0.0_ki\n')
f90file.write('\n')
f90file.write('\n')
abbrev = corr_dim_abbrev(outdict['Abbreviations'])
f90file.write(abbrev)
f90file.write('\n')
diag = corr_dim_diag(outdict['Diagrams'],'0')
f90file.write(diag)
diag = corr_dim_diag(outdict['Diagrams'],'1')
f90file.write(diag)
f90file.write('\n')
f90file.write('      if (debug_lo_diagrams) then\n')
f90file.write('         write(*,*) "Using Born optimization, debug_lo_diagrams not implemented."\n')
f90file.write('      end if\n')
f90file.write('\n')
f90file.write('!      if (use_sorted_sum) then\n')
f90file.write('!         do i=1,numcs\n')
f90file.write('!            ctamplitude(i) = sorted_sum(diagrams(i))\n')
f90file.write('!         end do\n')
f90file.write('!      else\n')
f90file.write('!         do i=1,numcs\n')
f90file.write('!            ctamplitude(i) = sum(diagrams(i))\n')
f90file.write('!         end do\n')
f90file.write('!      end if\n')
f90file.write('   end function     ctamplitude\n')
f90file.write('!---#] function ctamplitude:\n')
f90file.write('end module [% process_name asprefix=\_ %]ctdiagramsh'+str(heli)+'l0\n')
txtfile.close()
f90file.close()
### additional formatting for output files

postformat(tmpname)

shutil.move(tmpname,'diagramsct.f90')
