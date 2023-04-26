#! /usr/bin/env python3
# vim: ts=3:sw=3:expandtab

import sys
import os
from optparse import OptionParser
from t2f import translatefile, getdata
from colorin import parameters, symbols

config={ 'parameters':parameters,
        'symbols' : symbols}

parser = OptionParser()

parser.add_option("-i", "--input", dest="input",
                  action="store", type="string",
                  help="input file", metavar="INPUT")


(options, args) = parser.parse_args()

if not options.input:
    sys.exit("Error: no input file was found! Please specify one with the -i options.")

outdict=translatefile(options.input,config,True)

# 'global' color variables

gc=[]
for item in outdict['lhs']:
   idx_s = '(1,1)'
   if idx_s in item:
      gc.append(item[:len(item) - 6 ])

abb_max=getdata('color.dat')['number_abbs']


# Write color.f90 file
colorfile = open('color.f90', 'w')

colorfile.write('module     pc16_gghh_color\n')
colorfile.write('   ! file: '+str(os.getcwd())+'/color.f90 \n')
colorfile.write('   ! generator: buildcolor.py\n')
colorfile.write('   use pc16_gghh_config, only: ki\n')
colorfile.write('   use pc16_gghh_model, only: NC, Nf\n')
colorfile.write('   implicit none\n')
colorfile.write('   private\n')
colorfile.write('   save\n')
colorfile.write('\n')
colorfile.write('   public :: init_color\n')
colorfile.write('\n')
colorfile.write('   real(ki), parameter, public :: TR = 0.5_ki\n')
colorfile.write('\n')
colorfile.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
colorfile.write('   real(ki), parameter :: pi = &\n')
colorfile.write('   & 3.1415926535897932384626433832795028841971693993751058209749445920_ki\n')
colorfile.write('   real(ki), parameter :: pi6 = pi*pi/6.0_ki\n')
colorfile.write('\n')
colorfile.write('   integer, parameter, public :: numcs = 1\n')
for item in gc:
   colorfile.write('   complex(ki), dimension(numcs,numcs), public :: %s\n' % item)
colorfile.write('   real(ki), public :: incolors\n')
colorfile.write('\n')
colorfile.write('   real(ki), public :: CA, CF, KA, KF, gammaA, gammaF\n')
colorfile.write('\n')
colorfile.write('   real(ki) :: NA\n')
colorfile.write('   real(ki), dimension(%s) :: cabb\n' % abb_max)
colorfile.write('\n')
colorfile.write('   ! Basis vectors\n')
colorfile.write('   real(ki), dimension(numcs), parameter, public :: c1 = &\n')
colorfile.write('      & (/')
colorfile.write('         1.0_ki')
colorfile.write('/)\n')
colorfile.write('contains\n')
colorfile.write('   subroutine     init_color()\n')
colorfile.write('      implicit none\n')
abb_chunks = []
line_counter = 0
routine_counter = 0
for abb_line in outdict['Color'].split("\n"):
	colorfile.write(abb_line + "\n")
	line_counter += 1
	if line_counter >= 500: # abbrev.limit = 500
		routine_counter += 1
		line_counter = 0
		colorfile.write('      call init_color_%i()\n' % routine_counter)
		colorfile.write('   end subroutine\n')
		colorfile.write('   subroutine init_color_%i()\n' % routine_counter)
		colorfile.write('      implicit none\n')
colorfile.write('      CA = NC\n')
colorfile.write('      CF = TR * NA / NC\n')
colorfile.write('      ! KA = Kg in (C.11) [Catani,Seymour]\n')
colorfile.write('      KA = (67.0_ki/18.0_ki - pi6) * CA &\n')
colorfile.write('         & - 10.0_ki/9.0_ki * TR * Nf\n')
colorfile.write('      ! KF = Kq in (C.11) [Catani,Seymour]\n')
colorfile.write('      KF = (3.5_ki - pi6) * CF\n')
colorfile.write('      ! gammaA = \gamma_g in (C.11) [Catani,Seymour]\n')
colorfile.write('      gammaA = 11.0_ki/6.0_ki * CA - 2.0_ki/3.0_ki * TR * Nf\n')
colorfile.write('      ! gammaF = \gamma_q in (C.11) [Catani,Seymour]\n')
colorfile.write('      gammaF = 1.5_ki * CF\n')
colorfile.write('   end subroutine ! end of "init_color"\n')
colorfile.write('   subroutine     inspect_color(unit)\n')
colorfile.write('      implicit none\n')
colorfile.write('      integer, intent(in) :: unit\n')
colorfile.write('      integer :: i, j\n')
colorfile.write('      character :: ch1, ch2, ch3\n')
colorfile.write('\n')
colorfile.write('      ch3 = ","\n')
colorfile.write('      write (unit,\'(A13)\') "gosam_color=["\n')
colorfile.write('      do i=1,numcs\n')
colorfile.write('         do j=1,numcs\n')
colorfile.write('            if (j==1) then\n')
colorfile.write('               ch1 = "["\n')
colorfile.write('            else\n')
colorfile.write('               ch1 = " "\n')
colorfile.write('            endif\n')
colorfile.write('\n')
colorfile.write('            if (j == numcs) then\n')
colorfile.write('               ch2 = "]"\n')
colorfile.write('               if (i == numcs) then\n')
colorfile.write('                  ch3 = "]"\n')
colorfile.write('               end if\n')
colorfile.write('            else\n')
colorfile.write('               ch2 = ","\n')
colorfile.write('            end if\n')
colorfile.write('\n')
colorfile.write('            if (j == numcs) then\n')
colorfile.write('               write (unit,\'(3x,A1,A8,G23.16,A1,G23.16,A1,A1,A1)\') &\n')
colorfile.write('               & ch1, "complex(", real(CC(i,j)), ",", aimag(CC(i,j)), ")", &\n')
colorfile.write('               & ch2, ch3\n')
colorfile.write('            else\n')
colorfile.write('               write (unit,\'(3x,A1,A8,G23.16,A1,G23.16,A1,A1)\') &\n')
colorfile.write('               & ch1, "complex(", real(CC(i,j)), ",", aimag(CC(i,j)), ")", &\n')
colorfile.write('               & ch2\n')
colorfile.write('            end if\n')
colorfile.write('         enddo\n')
colorfile.write('      enddo\n')
colorfile.write('   end subroutine inspect_color\n')
colorfile.write('end module pc16_gghh_color\n')

colorfile.close()



