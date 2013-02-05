#! /usr/bin/env python

import sys
import os
from optparse import OptionParser

def parse_string(string,line,list,left=0,right=0):
    occ = line.count(string)
    if occ > 0:
        tmpl=line
        for i in range(0,occ):
            s=tmpl.find(string)-left
            e=tmpl.find(string,s)+len(string)+right
            if tmpl[s:e] not in list:
                list.append(tmpl[s:e])
            tmpl=tmpl[:s]+tmpl[e:]
    return

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

print '----------------------------------'
print 'Input file is:      %s' % file_name+'.txt'
print 'Diagram written in: %s' % 'diagramsl0.f90'
print '----------------------------------'

txtfile = open(file_name+'.txt','r')
f90file = open('diagramsl0.f90', 'w')

# import txt file
txt_lines=[]
abb_max=0
dotprod_kdotl=[]
dotprod_kdote=[]
dotprod_kdotspva=[]

while True:
    line=txtfile.readline()
    if len(line)==0:
        break
    txt_lines.append(line.replace('&','').replace('D0','0_ki').strip())
    if line.startswith('#####Abbreviations'):
        abb_low=len(txt_lines)-1
    if line.startswith('#####Diagrams'):
        abb_up=len(txt_lines)-1
line_num=len(txt_lines)

# find maximal number of abbreviations:
for idx,line in enumerate(txt_lines):
    if line.startswith('#####Diagrams'):
        break
    tmp_lline=line.partition('=')[0].strip()
    tmp_cline=line.partition('=')[1].strip()
    tmp_rline=line.partition('=')[2].strip()
    if tmp_lline.startswith('abb'):
        abb_max=max(abb_max,int(tmp_lline.split('(')[1].split(')')[0]))
    parse_string('_e',txt_lines[idx],dotprod_kdote,2,1)
    parse_string('_l',txt_lines[idx],dotprod_kdotl,2,1)
    parse_string('_spva',txt_lines[idx],dotprod_kdotspva,2,4)
    if txt_lines[idx].endswith('.D'):
        txt_lines[idx]=txt_lines[idx].replace('D','0_ki')
        txt_lines[idx+1]=txt_lines[idx+1][1:len(txt_lines[idx+1])+1]
    if txt_lines[idx].endswith('.') and txt_lines[idx+1].startswith('0_ki'):
        txt_lines[idx]=txt_lines[idx][0:len(txt_lines[idx])+1]+'0_ki'
        txt_lines[idx+1]=txt_lines[idx+1][4:len(txt_lines[idx+1])+1]
    ## replacement of SQRT. VALID ONLY FOR SM --> TO BE GENERALIZED!!!
    txt_lines[idx]=txt_lines[idx].replace('csqrt(mT**2)','mT')

#print "--------------------"

  
f90file.write('module     [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0\n')
f90file.write('   ! file: '+str(os.getcwd())+'diagramsl0.f90 \n')
f90file.write('   ! generator: buildfortranborn.py \n')
f90file.write('   use [% process_name asprefix=\_ %]color, only: numcs\n')
f90file.write('   use [% process_name asprefix=\_ %]config, only: ki\n')
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
for sp in dotprod_kdote:
    f90file.write('      complex(ki) :: '+sp+'\n')
for sp in dotprod_kdotl:
    f90file.write('      complex(ki) :: '+sp+'\n')
for sp in dotprod_kdotspva:
    f90file.write('      complex(ki) :: '+sp+'\n')
f90file.write('      integer :: i\n')
f90file.write('\n')
f90file.write('      amplitude(:) = 0.0_ki\n')
f90file.write('\n')
for sp in dotprod_kdote:
    f90file.write('      '+sp+ '=dotproduct('+sp.partition('_')[0]+','+sp.partition('_')[2]+')\n')
for sp in dotprod_kdotl:
    f90file.write('      '+sp+ '=dotproduct('+sp.partition('_')[0]+','+sp.partition('_')[2]+')\n')
for sp in dotprod_kdotspva:
    f90file.write('      '+sp+ '=dotproduct('+sp.partition('_')[0]+','+sp.partition('_')[2]+')\n')
f90file.write('\n')
for i in range(abb_low+1,abb_up-1):
    if txt_lines[i+1].count('=') == 1 or len(txt_lines[i+1]) == 0:
        f90file.write('      '+txt_lines[i]+'\n')
    else:
        f90file.write('      '+txt_lines[i]+'&\n')
f90file.write('\n')
for i in range(abb_up+2,line_num):
    if len(txt_lines[i]) == 0:
        f90file.write('      '+txt_lines[i-1].replace('diagrams','amplitude')+'\n')
    else:
        f90file.write('      '+txt_lines[i-1].replace('diagrams','amplitude')+'&\n')
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
f90file.write('end module [% process_name asprefix=\_ %]diagramsh'+str(heli)+'l0\n')
