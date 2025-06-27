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
# print('Diagram written in: %s' % diag_name+'.f90')[%
@if helsum %]
# print('Abbrev. written in: %s' % 'abbrevd'+diag+'.f90')[%
@else %]
# print('Abbrev. written in: %s' % 'abbrevd'+diag+'h'+heli+'.f90')[%
@end @if %]
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
[% @if extension quadruple %]
tmp_abb_handle_qp , abb_tmpname_qp = tempfile.mkstemp(suffix="_qp.f90",prefix="gosam_tmp")
abbfile_qp = os.fdopen(tmp_abb_handle_qp,"w")
f90_tmp_handle_qp , f90_tmpname_qp = tempfile.mkstemp(suffix="_qp.f90",prefix="gosam_tmp")
f90file_qp = os.fdopen(f90_tmp_handle_qp,"w")
[% @end @if extension quadruple %]
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
abbfile.write('module     [% process_name asprefix=\_
            %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
abbfile.write('   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki\n')
abbfile.write('   use [% process_name asprefix=\_ %]kinematics, only: epstensor\n')
abbfile.write('   use [% process_name asprefix=\_ %]globals'[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')[%
@if internal CUSTOM_SPIN2_PROP %]
abbfile.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
abbfile.write('   implicit none\n')
abbfile.write('   private\n')
abbfile.write('   complex(ki), dimension('+str(abb_max)+'), public :: abb'+diag+'\n')[%
@select r2
@case explicit %]
abbfile.write('   complex(ki), public :: R2d'+diag+'\n')[% 
@end @select %]
abbfile.write('\n')
abbfile.write('   public :: init_abbrev\n')
abbfile.write('\n')
abbfile.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
abbfile.write('\n')
abbfile.write('contains\n')
abbfile.write('   subroutine     init_abbrev()\n')
abbfile.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: deltaOS, &\n')
abbfile.write('     &    logfile, debug_nlo_diagrams\n')
abbfile.write('      use [% process_name asprefix=\_ %]kinematics\n')
abbfile.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model\n')
abbfile.write('      use [% process_name asprefix=\_ %]color, only: TR\n')
abbfile.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow\n')
abbfile.write('      implicit none\n')
abbfile.write('\n')[%
@if eval abbrev.limit > 0 %][% 'need to split into several subroutines' %]
abb_chunks = []
line_counter = 0
routine_counter = 0
for abb_line in outdict['Abbreviations'].split("\n"):
	abbfile.write(abb_line + "\n")
	line_counter += 1
	if line_counter >= [% abbrev.limit %]: # abbrev.limit = [% abbrev.limit %]
		routine_counter += 1
		line_counter = 0
		abbfile.write('      call init_abbrev_%i()\n' % routine_counter)
		abbfile.write('   end subroutine\n')
		abbfile.write('   subroutine init_abbrev_%i()\n' % routine_counter)
		abbfile.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: deltaOS, &\n')
		abbfile.write('     &    logfile, debug_nlo_diagrams\n')
		abbfile.write('      use [% process_name asprefix=\_ %]kinematics\n')
		abbfile.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model\n')
		abbfile.write('      use [% process_name asprefix=\_ %]color, only: TR\n')
		abbfile.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow\n')
		abbfile.write('      implicit none\n')
		abbfile.write('\n')[%
@else %]
abbfile.write(outdict['Abbreviations'])[%
@end @if %][%
@select r2
@case explicit %]
abbfile.write(outdict['R2'])
abbfile.write('\n')
abbfile.write('      rat2 = rat2 + R2d'+diag+'\n')
abbfile.write('\n')
abbfile.write('      if (debug_nlo_diagrams) then\n')
abbfile.write('          write (logfile,*) "<result name=\'r2\' index=\''+diag+'\' value=\'", &\n')
abbfile.write('          & R2d'+diag+', "\'/>"\n')
abbfile.write('      end if\n')[% 
@end @select %]
abbfile.write('   end subroutine\n')
abbfile.write('end module [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')

[% @if extension quadruple %]
abbfile_qp.write('module     [% process_name asprefix=\_
            %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'_qp\n')
abbfile_qp.write('   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki => ki_qp\n')
abbfile_qp.write('   use [% process_name asprefix=\_ %]kinematics_qp, only: epstensor\n')
abbfile_qp.write('   use [% process_name asprefix=\_ %]globals'[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'_qp\n')[%
@if internal CUSTOM_SPIN2_PROP %]
abbfile_qp.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
abbfile_qp.write('   implicit none\n')
abbfile_qp.write('   private\n')
abbfile_qp.write('   complex(ki), dimension('+str(abb_max)+'), public :: abb'+diag+'\n')[%
@select r2
@case explicit %]
abbfile_qp.write('   complex(ki), public :: R2d'+diag+'\n')[% 
@end @select %]
abbfile_qp.write('\n')
abbfile_qp.write('   public :: init_abbrev\n')
abbfile_qp.write('\n')
abbfile_qp.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
abbfile_qp.write('\n')
abbfile_qp.write('contains\n')
abbfile_qp.write('   subroutine     init_abbrev()\n')
abbfile_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: deltaOS, &\n')
abbfile_qp.write('     &    logfile, debug_nlo_diagrams\n')
abbfile_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
abbfile_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp\n')
abbfile_qp.write('      use [% process_name asprefix=\_ %]color_qp, only: TR\n')
abbfile_qp.write('      use [% process_name asprefix=\_ %]globalsl1_qp, only: epspow\n')
abbfile_qp.write('      implicit none\n')
abbfile_qp.write('\n')[%
@if eval abbrev.limit > 0 %][% 'need to split into several subroutines' %]
abb_chunks = []
line_counter = 0
routine_counter = 0
for abb_line in outdict['Abbreviations'].split("\n"):
	abbfile_qp.write(abb_line + "\n")
	line_counter += 1
	if line_counter >= [% abbrev.limit %]: # abbrev.limit = [% abbrev.limit %]
		routine_counter += 1
		line_counter = 0
		abbfile_qp.write('      call init_abbrev_%i()\n' % routine_counter)
		abbfile_qp.write('   end subroutine\n')
		abbfile_qp.write('   subroutine init_abbrev_%i()\n' % routine_counter)
		abbfile_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: deltaOS, &\n')
		abbfile_qp.write('     &    logfile, debug_nlo_diagrams\n')
		abbfile_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
		abbfile_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp\n')
		abbfile_qp.write('      use [% process_name asprefix=\_ %]color_qp, only: TR\n')
		abbfile_qp.write('      use [% process_name asprefix=\_ %]globalsl1_qp, only: epspow\n')
		abbfile_qp.write('      implicit none\n')
		abbfile_qp.write('\n')[%
@else %]
abbfile_qp.write(outdict['Abbreviations'])[%
@end @if %][%
@select r2
@case explicit %]
abbfile_qp.write(outdict['R2'])
abbfile_qp.write('\n')
abbfile_qp.write('      rat2 = rat2 + R2d'+diag+'\n')
abbfile_qp.write('\n')
abbfile_qp.write('      if (debug_nlo_diagrams) then\n')
abbfile_qp.write('          write (logfile,*) "<result name=\'r2\' index=\''+diag+'\' value=\'", &\n')
abbfile_qp.write('          & R2d'+diag+', "\'/>"\n')
abbfile_qp.write('      end if\n')[% 
@end @select %]
abbfile_qp.write('   end subroutine\n')
abbfile_qp.write('end module [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'_qp\n')
[% @end @if extension quadruple %]

f90file.write('module     [% process_name asprefix=\_ %]'+diag_name+'\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name+'.f90 \n')
f90file.write('   ! generator: buildfortran.py \n')
f90file.write('   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki\n')
f90file.write('   use [% process_name asprefix=\_ %]util, only: cond\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')[%
@if extension golem95 %]
f90file.write('   public :: numerator_golem95\n')[%
@end @if %][%
@if extension ninja %]
f90file.write('   public :: numerator_ninja\n')[%
@end @if %]
f90file.write('contains\n')
f90file.write('!---#[ function brack_1:\n')
f90file.write('   function brack_1(Q,mu2) result(brack)\n')
f90file.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]color\n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
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
f90file.write('!---#[ numerator interfaces:\n')[%
@if extension golem95 %]
f90file.write('   !------#[ function numerator_golem95:\n')
f90file.write('   function numerator_golem95(Q_ext, mu2_ext) result(numerator)\n')
f90file.write('      use precision_golem, only: ki_gol => ki\n')
f90file.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
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
    f90file.write('      Q(:)  =cmplx(real('+qsign+'Q_ext(:)  -qshift(:),  ki_gol), 0.0_ki_gol, ki)\n')[%
@select r2
@case implicit %]
f90file.write('      mu2  = cmplx(real(mu2_ext, ki), 0.0_ki, ki)\n')[%
@end @select %]
f90file.write('      d'+diag+' = 0.0_ki\n')
f90file.write('      d'+diag+' = (cond(epspow.eq.0,brack_1,Q,mu2))\n')
f90file.write('      numerator = cmplx(real(d'+diag+', ki), aimag(d'+diag+'), ki_gol)\n')
f90file.write('   end function numerator_golem95\n')
f90file.write('   !------#] function numerator_golem95:\n')[%
@end @if %]
[%
@if extension ninja %]
f90file.write('   !------#[ subroutine numerator_ninja:\n')
f90file.write('   subroutine numerator_ninja(ncut, Q_ext, mu2_ext, numerator) &\n')
f90file.write('   & bind(c, name="[% process_name asprefix=\_ %]'+diag_name+'_ninja")\n')
f90file.write('      use iso_c_binding, only: c_int\n')
f90file.write('      use ninjago_module, only: ki_nin\n')
f90file.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow\n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics\n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
f90file.write('      implicit none\n')
f90file.write('\n')
f90file.write('      integer(c_int), intent(in) :: ncut\n')
f90file.write('      complex(ki_nin), dimension(0:3), intent(in) :: Q_ext\n')
f90file.write('      complex(ki_nin), intent(in) :: mu2_ext\n')
f90file.write('      complex(ki_nin), intent(out) :: numerator\n')
f90file.write('      complex(ki) :: d'+diag+'\n')
f90file.write('\n')
f90file.write('      ! The Q that goes into the diagram\n')
f90file.write('      complex(ki), dimension(4) :: Q\n')
f90file.write('      complex(ki) :: mu2\n')
if qshift=='0':
    f90file.write('      Q(1:4)  =cmplx(real('+qsign+'Q_ext(0:3),  ki_nin), aimag('+qsign+'Q_ext(0:3)), ki)\n')
else:
    f90file.write('      real(ki), dimension(0:3) :: qshift\n')
    f90file.write('\n')
    f90file.write('      qshift = '+qshift+'\n')
    f90file.write('      Q(1:4)  =cmplx(real('+qsign+'Q_ext(0:3)  -qshift(:),  ki_nin), aimag('+qsign+'Q_ext(0:3)), ki)\n')[%
@select r2
@case implicit %]
f90file.write('      mu2  = cmplx(real(mu2_ext, ki), aimag(mu2_ext), ki)\n')[%
@end @select %]
f90file.write('      d'+diag+' = 0.0_ki\n')
f90file.write('      d'+diag+' = (cond(epspow.eq.0,brack_1,Q,mu2))\n')
f90file.write('      numerator = cmplx(real(d'+diag+', ki), aimag(d'+diag+'), ki_nin)\n')
f90file.write('   end subroutine numerator_ninja\n')
f90file.write('   !------#] subroutine numerator_ninja:\n')[%
@end @if %]
f90file.write('!---#] numerator interfaces:\n')
f90file.write('end module [% process_name asprefix=\_ %]'+diag_name+'\n')

[% @if extension quadruple %]
f90file_qp.write('module     [% process_name asprefix=\_ %]'+diag_name+'_qp\n')
f90file_qp.write('   ! file: '+str(os.getcwd())+diag_name+'_qp.f90 \n')
f90file_qp.write('   ! generator: buildfortran.py \n')
f90file_qp.write('   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki => ki_qp\n')
f90file_qp.write('   use [% process_name asprefix=\_ %]util_qp, only: cond\n')[%
@if internal CUSTOM_SPIN2_PROP %]
f90file_qp.write('   use [% process_name asprefix=\_ %]custompropagator\n')[%
@end @if %]
f90file_qp.write('\n')
f90file_qp.write('   implicit none\n')
f90file_qp.write('   private\n')
f90file_qp.write('\n')
f90file_qp.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')[%
@if extension golem95 %]
f90file_qp.write('   public :: numerator_golem95\n')[%
@end @if %][%
@if extension ninja %]
f90file_qp.write('   public :: numerator_ninja\n')[%
@end @if %]
f90file_qp.write('contains\n')
f90file_qp.write('!---#[ function brack_1:\n')
f90file_qp.write('   function brack_1(Q,mu2) result(brack)\n')
f90file_qp.write('      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]color_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'_qp\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('      complex(ki), dimension(4), intent(in) :: Q\n')
f90file_qp.write('      complex(ki), intent(in) :: mu2\n')
f90file_qp.write('      complex(ki) :: brack\n')
f90file_qp.write('      complex(ki) :: acc'+diag+'('+str(acc_max)+')'+'\n')

for Qitem in outdict['dplist']:
    f90file_qp.write('      complex(ki) :: '+ Qitem +'\n')

for Qitem in outdict['dplist']:
    f90file_qp.write('      %s = %s' % (Qitem, dotproducts[Qitem]) +'\n')
f90file_qp.write('\n')
f90file_qp.write(outdict['Diagram'])
f90file_qp.write('\n')
f90file_qp.write('   end  function brack_1\n')
f90file_qp.write('\n')
f90file_qp.write('!---#] function brack_1:\n')
f90file_qp.write('!---#[ numerator interfaces:\n')[%
@if extension golem95 %]
f90file_qp.write('   !------#[ function numerator_golem95:\n')
f90file_qp.write('   function numerator_golem95(Q_ext, mu2_ext) result(numerator)\n')
f90file_qp.write('      use precision_golem, only: ki_gol => ki\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]globalsl1_qp, only: epspow\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'_qp\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('\n')
f90file_qp.write('      real(ki_gol), dimension(0:3), intent(in) :: Q_ext\n')
f90file_qp.write('      real(ki_gol), intent(in) :: mu2_ext\n')
f90file_qp.write('      complex(ki_gol) :: numerator\n')
f90file_qp.write('      complex(ki) :: d'+diag+'\n')
f90file_qp.write('\n')
f90file_qp.write('      ! The Q that goes into the diagram\n')
f90file_qp.write('      complex(ki), dimension(4) :: Q\n')
f90file_qp.write('      complex(ki) :: mu2\n')
if qshift=='0':
    f90file_qp.write('      Q(:)  =cmplx(real('+qsign+'Q_ext(:),  ki_gol), 0.0_ki_gol, ki)\n')
else:
    f90file_qp.write('      real(ki), dimension(4) :: qshift\n')
    f90file_qp.write('\n')
    f90file_qp.write('      qshift = '+qshift+'\n')
    f90file_qp.write('      Q(:)  =cmplx(real('+qsign+'Q_ext(:)  -qshift(:),  ki_gol), 0.0_ki_gol, ki)\n')[%
@select r2
@case implicit %]
f90file_qp.write('      mu2  = cmplx(real(mu2_ext, ki), 0.0_ki, ki)\n')[%
@end @select %]
f90file_qp.write('      d'+diag+' = 0.0_ki\n')
f90file_qp.write('      d'+diag+' = (cond(epspow.eq.0,brack_1,Q,mu2))\n')
f90file_qp.write('      numerator = cmplx(real(d'+diag+', ki), aimag(d'+diag+'), ki_gol)\n')
f90file_qp.write('   end function numerator_golem95\n')
f90file_qp.write('   !------#] function numerator_golem95:\n')[%
@end @if %]
[%
@if extension ninja %]
f90file_qp.write('   !------#[ subroutine numerator_ninja:\n')
f90file_qp.write('   subroutine numerator_ninja(ncut, Q_ext, mu2_ext, numerator) &\n')
f90file_qp.write('   & bind(c, name="[% process_name asprefix=\_ %]'+diag_name+'_qp_ninja")\n')
f90file_qp.write('      use iso_c_binding, only: c_int\n')
f90file_qp.write('      use quadninjago_module, only: ki_nin\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]globalsl1_qp, only: epspow\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]kinematics_qp\n')
f90file_qp.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if enable_truncation_orders %]+'_[% trnco %]'[% @end @if %][% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'_qp\n')
f90file_qp.write('      implicit none\n')
f90file_qp.write('\n')
f90file_qp.write('      integer(c_int), intent(in) :: ncut\n')
f90file_qp.write('      complex(ki_nin), dimension(0:3), intent(in) :: Q_ext\n')
f90file_qp.write('      complex(ki_nin), intent(in) :: mu2_ext\n')
f90file_qp.write('      complex(ki_nin), intent(out) :: numerator\n')
f90file_qp.write('      complex(ki) :: d'+diag+'\n')
f90file_qp.write('\n')
f90file_qp.write('      ! The Q that goes into the diagram\n')
f90file_qp.write('      complex(ki), dimension(4) :: Q\n')
f90file_qp.write('      complex(ki) :: mu2\n')
if qshift=='0':
    f90file_qp.write('      Q(1:4)  =cmplx(real('+qsign+'Q_ext(0:3),  ki_nin), aimag('+qsign+'Q_ext(0:3)), ki)\n')
else:
    f90file_qp.write('      real(ki), dimension(0:3) :: qshift\n')
    f90file_qp.write('\n')
    f90file_qp.write('      qshift = '+qshift+'\n')
    f90file_qp.write('      Q(1:4)  =cmplx(real('+qsign+'Q_ext(0:3)  -qshift(:),  ki_nin), aimag('+qsign+'Q_ext(0:3)), ki)\n')[%
@select r2
@case implicit %]
f90file_qp.write('      mu2  = cmplx(real(mu2_ext, ki), aimag(mu2_ext), ki)\n')[%
@end @select %]
f90file_qp.write('      d'+diag+' = 0.0_ki\n')
f90file_qp.write('      d'+diag+' = (cond(epspow.eq.0,brack_1,Q,mu2))\n')
f90file_qp.write('      numerator = cmplx(real(d'+diag+', ki), aimag(d'+diag+'), ki_nin)\n')
f90file_qp.write('   end subroutine numerator_ninja\n')
f90file_qp.write('   !------#] subroutine numerator_ninja:\n')[%
@end @if %]
f90file_qp.write('!---#] numerator interfaces:\n')
f90file_qp.write('end module [% process_name asprefix=\_ %]'+diag_name+'_qp\n')
[% @end @if extension quadruple %]
txtfile.close()
abbfile.close()
[% @if extension quadruple %]
abbfile_qp.close()
[% @end @if extension quadruple %]
f90file.close()
[% @if extension quadruple %]
f90file_qp.close()
[% @end @if extension quadruple %]
### additional formatting for output files

postformat(abb_tmpname)
postformat(f90_tmpname)
[% @if extension quadruple %]
postformat(abb_tmpname_qp)
postformat(f90_tmpname_qp)
[% @end @if extension quadruple %]
if int(heli) == -1:
    shutil.move(abb_tmpname,'abbrevd'+diag+'[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].f90')
else:
    shutil.move(abb_tmpname,'abbrevd'+diag+'[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h'+heli+'.f90')
shutil.move(f90_tmpname,diag_name + '.f90')
[% @if extension quadruple %]
if int(heli) == -1:
    shutil.move(abb_tmpname_qp,'abbrevd'+diag+'[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp.f90')
else:
    shutil.move(abb_tmpname_qp,'abbrevd'+diag+'[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h'+heli+'_qp.f90')
shutil.move(f90_tmpname_qp,diag_name + '_qp.f90')
[% @end @if extension quadruple %]
