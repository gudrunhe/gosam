#! /usr/bin/env python3

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

parser.add_option("-D", "--DIAGRAM", dest="diagram",
                  action="store", type="int",
                  help="diagram name", metavar="DIAGRAM")

parser.add_option("-G", "--GROUP", dest="group",
                  action="store", type="int",
                  help="group number", metavar="GROUP")

parser.add_option("-H", "--HELICITY", dest="helicity",
                  action="store", type="int",
                  help="helicity number", metavar="HELICITY")

parser.add_option("-S", "--QSIGN", dest="qsign",
                  action="store", type="string",
                  help="q sign", metavar="QSIGN")

parser.add_option("-Q", "--QSHIFT", dest="qshift",
                  action="store", type="string",
                  help="q shift", metavar="QSHIFT")

(options, args) = parser.parse_args()

if not options.input:
    sys.exit("Error: no input file was found! Please specify one with the -i options.")

diag_name= options.input.split('.')[0]
diag=str(options.diagram)
heli=str(options.helicity)
qsign=options.qsign
qshift=options.qshift

# print('----------------------------------')
# print('Input file is:      %s' % diag_name+'.txt')
# print('Diagram written in: %s' % diag_name+'.f90')
# print('Abbrev. written in: %s' % 'abbrevd'+diag+'h'+heli+'.f90')
# print('Diagram information:')
# print('diag:  %s' % options.diagram)
# print('group: %s' % options.group)
# print('heli:  %s' % options.helicity)
# print('qsign: %s' % options.qsign)
# print('qshif: %s' % options.qshift)
# print('----------------------------------')

txtfile = open(diag_name+'.txt','r')
tmp_abb_handle , abb_tmpname = tempfile.mkstemp(suffix=".f90",prefix="gosam_tmp")
abbfile = os.fdopen(tmp_abb_handle,"w")
f90_tmp_handle , f90_tmpname = tempfile.mkstemp(suffix=".f90",prefix="gosam_tmp")
f90file = os.fdopen(f90_tmp_handle,"w")

datfilename = diag_name + '.dat'
# import txt file
txt_lines=[]
dotprod_spva=[]
dotprod_sp=[]
dotprod_kdotl=[]
dotprod_kdote=[]
dotprod_kdotspva=[]
abb_max=getdata(datfilename)['abbrev_terms']
acc_max=getdata(datfilename)['diagram_terms']

# catch the case that acc_max is zero
if acc_max == '0':
	acc_max = 1


#print("--------------------")

outdict=translatefile(diag_name+'.txt',config)

# Write abbreviation file
abbfile.write('module     pc17_gghh_abbrevd'+diag+'_0'+'h'+heli+'\n')
abbfile.write('   use pc17_gghh_config, only: ki\n')
abbfile.write('   use pc17_gghh_kinematics, only: epstensor\n')
abbfile.write('   use pc17_gghh_globals'+'h'+heli+'\n')
abbfile.write('   implicit none\n')
abbfile.write('   private\n')
abbfile.write('   complex(ki), dimension('+str(abb_max)+'), public :: abb'+diag+'\n')
abbfile.write('   complex(ki), public :: R2d'+diag+'\n')
abbfile.write('\n')
abbfile.write('   public :: init_abbrev\n')
abbfile.write('\n')
abbfile.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
abbfile.write('\n')
abbfile.write('contains\n')
abbfile.write('   subroutine     init_abbrev()\n')
abbfile.write('      use pc17_gghh_config, only: deltaOS, &\n')
abbfile.write('     &    logfile, debug_nlo_diagrams\n')
abbfile.write('      use pc17_gghh_kinematics\n')
abbfile.write('      use pc17_gghh_model\n')
abbfile.write('      use pc17_gghh_color, only: TR\n')
abbfile.write('      use pc17_gghh_globalsl1, only: epspow\n')
abbfile.write('      implicit none\n')
abbfile.write('\n')
abb_chunks = []
line_counter = 0
routine_counter = 0
for abb_line in outdict['Abbreviations'].split("\n"):
	abbfile.write(abb_line + "\n")
	line_counter += 1
	if line_counter >= 500: # abbrev.limit = 500
		routine_counter += 1
		line_counter = 0
		abbfile.write('      call init_abbrev_%i()\n' % routine_counter)
		abbfile.write('   end subroutine\n')
		abbfile.write('   subroutine init_abbrev_%i()\n' % routine_counter)
		abbfile.write('      use pc17_gghh_config, only: deltaOS, &\n')
		abbfile.write('     &    logfile, debug_nlo_diagrams\n')
		abbfile.write('      use pc17_gghh_kinematics\n')
		abbfile.write('      use pc17_gghh_model\n')
		abbfile.write('      use pc17_gghh_color, only: TR\n')
		abbfile.write('      use pc17_gghh_globalsl1, only: epspow\n')
		abbfile.write('      implicit none\n')
		abbfile.write('\n')
abbfile.write(outdict['R2'])
abbfile.write('\n')
abbfile.write('      rat2 = rat2 + R2d'+diag+'\n')
abbfile.write('\n')
abbfile.write('      if (debug_nlo_diagrams) then\n')
abbfile.write('          write (logfile,*) "<result name=\'r2\' index=\''+diag+'\' value=\'", &\n')
abbfile.write('          & R2d'+diag+', "\'/>"\n')
abbfile.write('      end if\n')
abbfile.write('   end subroutine\n')
abbfile.write('end module pc17_gghh_abbrevd'+diag+'_0'+'h'+heli+'\n')



f90file.write('module     pc17_gghh_'+diag_name+'\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name+'.f90 \n')
f90file.write('   ! generator: buildfortran.py \n')
f90file.write('   use pc17_gghh_config, only: ki\n')
f90file.write('   use pc17_gghh_util, only: cond\n')
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
f90file.write('   public :: numerator_golem95\n')
f90file.write('contains\n')
f90file.write('!---#[ function brack_1:\n')
f90file.write('   pure function brack_1(Q,mu2) result(brack)\n')
f90file.write('      use pc17_gghh_model\n')
f90file.write('      use pc17_gghh_kinematics\n')
f90file.write('      use pc17_gghh_color\n')
f90file.write('      use pc17_gghh_abbrevd'+diag+'_0'+'h'+heli+'\n')
f90file.write('      implicit none\n')
f90file.write('      complex(ki), dimension(4), intent(in) :: Q\n')
f90file.write('      complex(ki), intent(in) :: mu2\n')
f90file.write('      complex(ki) :: brack\n')
f90file.write('      complex(ki) :: acc'+diag+'('+str(acc_max)+')'+'\n')

for Qitem in outdict['dplist']:
    f90file.write('      complex(ki) :: '+ Qitem +'\n')

for Qitem in outdict['dplist']:
    f90file.write('      %s = %s' % (Qitem, dotproducts[Qitem]) +'\n')
f90file.write('\n')
f90file.write(outdict['Diagram'])
f90file.write('\n')
f90file.write('   end  function brack_1\n')
f90file.write('\n')
f90file.write('!---#] function brack_1:\n')
f90file.write('!---#[ numerator interfaces:\n')
f90file.write('   !------#[ function numerator_golem95:\n')
f90file.write('   function numerator_golem95(Q_ext, mu2_ext) result(numerator)\n')
f90file.write('      use precision_golem, only: ki_gol => ki\n')
f90file.write('      use pc17_gghh_globalsl1, only: epspow\n')
f90file.write('      use pc17_gghh_kinematics\n')
f90file.write('      use pc17_gghh_abbrevd'+diag+'_0'+'h'+heli+'\n')
f90file.write('      implicit none\n')
f90file.write('\n')
f90file.write('      real(ki_gol), dimension(0:3), intent(in) :: Q_ext\n')
f90file.write('      real(ki_gol), intent(in) :: mu2_ext\n')
f90file.write('      complex(ki_gol) :: numerator\n')
f90file.write('      complex(ki) :: d'+diag+'\n')
f90file.write('\n')
f90file.write('      ! The Q that goes into the diagram\n')
f90file.write('      complex(ki), dimension(4) :: Q\n')
f90file.write('      complex(ki) :: mu2\n')
if qshift=='0':
    f90file.write('      Q(:)  =cmplx(real('+qsign+'Q_ext(:),  ki_gol), 0.0_ki_gol, ki)\n')
else:
    f90file.write('      real(ki), dimension(4) :: qshift\n')
    f90file.write('\n')
    f90file.write('      qshift = '+qshift+'\n')
    f90file.write('      Q(:)  =cmplx(real('+qsign+'Q_ext(:)  -qshift(:),  ki_gol), 0.0_ki_gol, ki)\n')
f90file.write('      d'+diag+' = 0.0_ki\n')
f90file.write('      d'+diag+' = (cond(epspow.eq.0,brack_1,Q,mu2))\n')
f90file.write('      numerator = cmplx(real(d'+diag+', ki), aimag(d'+diag+'), ki_gol)\n')
f90file.write('   end function numerator_golem95\n')
f90file.write('   !------#] function numerator_golem95:\n')

f90file.write('!---#] numerator interfaces:\n')
f90file.write('end module pc17_gghh_'+diag_name+'\n')


txtfile.close()
abbfile.close()

f90file.close()

### additional formatting for output files

postformat(abb_tmpname)
postformat(f90_tmpname)

if int(heli) == -1:
    shutil.move(abb_tmpname,'abbrevd'+diag+'_0.f90')
else:
    shutil.move(abb_tmpname,'abbrevd'+diag+'_0h'+heli+'.f90')
shutil.move(f90_tmpname,diag_name + '.f90')

