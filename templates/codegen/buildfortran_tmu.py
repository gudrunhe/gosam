#! /usr/bin/env python


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

parser.add_option("-R", "--RANK", dest="rank",
                  action="store", type="int",
                  help="diagram rank", metavar="RANK")

parser.add_option("-L", "--LOOPSIZE", dest="loopsize",
                  action="store", type="string",
                  help="diagram loopsize", metavar="LOOPSIZE")

(options, args) = parser.parse_args()

if not options.input:
    sys.exit("Error: no input file was found! Please specify one with the -i options.")

diag_name= options.input.split('.')[0]
diag=str(options.diagram)
heli=str(options.helicity)
qsign=options.qsign
qshift=options.qshift
rank=options.rank
diagram=options.diagram
group=options.group
loopsize=options.loopsize
# print '----------------------------------'
# print 'Input file is:      %s' % diag_name+'.txt'
# print 'Diagram written in: %s' % diag_name+'.f90'
# print 'Abbrev. written in: %s' % 'abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'.f90'
# print 'Diagram information:'
# print 'diag:  %s' % options.diagram
# print 'group: %s' % options.group
# print 'heli:  %s' % options.helicity
# print 'qsign: %s' % options.qsign
# print 'qshif: %s' % options.qshift
# print '----------------------------------'

txtfile = open(diag_name+'.txt','r')
tmp_handle , tmpname = tempfile.mkstemp(suffix=".f90",prefix="gosam_tmp")
f90file = os.fdopen(tmp_handle,"w")
datfilename = diag_name[:-1] + '.dat'
# import txt file
txt_lines=[]
dotprod_spva=[]
dotprod_sp=[]
dotprod_kdotl=[]
dotprod_kdote=[]
dotprod_kdotspva=[]


outdict=translatefile(diag_name+'.txt',config)

acd_maxl = []

n_t_terms = 0
if (int(rank) >= int(loopsize) and int(loopsize) >= 4):
    n_t_terms = 1

for lidx in range(0,n_t_terms):
    acdmax=getdata(datfilename)['ninMu2diagram_terms']
    if acdmax == '0':
        acdmax = 1
    acd_maxl.append(acdmax)


# Write abbreviation file

f90file.write('module     [% process_name asprefix=\_%]'+diag_name[:-1]+'21\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name[:-1]+'21.f90 \n')
f90file.write('   ! generator: buildfortran_n3.py \n')
f90file.write('   use [% process_name asprefix=\_ %]config, only: ki \n')
f90file.write('   use [% process_name asprefix=\_ %]util, only: cond_t, d => metric_tensor \n')
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
if (int(rank)>=int(loopsize)+1):
    f90file.write('   integer, parameter :: ninjaidxt1 = 0\n')
    f90file.write('   integer, parameter :: ninjaidxt0 = 1\n')
else:
    f90file.write('   integer, parameter :: ninjaidxt0 = 0\n')
f90file.write('   public :: numerator_tmu\n')
f90file.write(' \n')
f90file.write('contains \n')

extra_arg = ''
if (int(rank)>=int(loopsize)+1):
    extra_arg = ' ninjaA1,'

for lidx in range(0,n_t_terms):
    f90file.write('!---#[ subroutine brack_%s: \n' % lidx)
    f90file.write('   pure subroutine brack_{0}(ninjaA0,'.format(lidx)
                  + extra_arg + ' brack)\n')
    f90file.write('      use [% process_name asprefix=\_ %]model \n')
    f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
    f90file.write('      use [% process_name asprefix=\_ %]color \n')
    f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
    f90file.write('      implicit none \n')
    f90file.write('      complex(ki), dimension(4), intent(in) :: ninjaA0\n')
    if (int(rank)>=int(loopsize)+1):
        f90file.write('      complex(ki), dimension(4), intent(in) :: ninjaA1\n')
    f90file.write('      complex(ki), dimension('+str(acd_maxl[lidx])+') :: acd'+diag+'\n')
    f90file.write('      complex(ki), dimension (0:*), intent(inout) :: brack\n')
    
    f90file.write(outdict['NinjaMu2'])
    f90file.write('   end subroutine brack_%s\n' % lidx)
    f90file.write('!---#] subroutine brack_%s: \n' % lidx)

if (extra_arg):
    extra_arg = ' vecA1,'

f90file.write('!---#[ subroutine numerator_tmu:\n')
f90file.write('   subroutine numerator_tmu(ncut, a, coeffs) &\n' )[%
@if helsum %]
f90file.write('   & bind(c, name="[% process_name asprefix=\_ %]d{0}_ninja_tmu")\n'.format(diag) )[%
@else %]
f90file.write('   & bind(c, name="[% process_name asprefix=\_ %]d{0}h{1}_ninja_tmu")\n'.format(diag,heli) )[%
@end @if %]
f90file.write('      use iso_c_binding, only: c_int\n')
f90file.write('      use ninjago_module, only: ki => ki_nin\n')
f90file.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow \n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
f90file.write('      implicit none \n')
f90file.write('      integer(c_int), intent(in) :: ncut\n')
f90file.write('      complex(ki), dimension(0:3,0:*), intent(in) :: a\n')
f90file.write('      complex(ki), dimension(0:*), intent(out) :: coeffs\n')
f90file.write('      integer :: t1 \n')
if qshift=='0':
    if (int(rank)>=int(loopsize)):
        f90file.write('      complex(ki), dimension(4) :: vecA0\n')
    if (int(rank)>=int(loopsize)+1):
        f90file.write('      complex(ki), dimension(4) :: vecA1\n')
    if (int(rank)>=int(loopsize)):
        f90file.write('	     vecA0(1:4) = ' + qsign + ' a(0:3,0)\n')
    if (int(rank)>=int(loopsize)+1):
        f90file.write('	     vecA1(1:4) = ' + qsign + ' a(0:3,1)\n')
else:
    if (int(rank)>=int(loopsize)):
        f90file.write('      complex(ki), dimension(4) :: qshift\n')
        f90file.write('      complex(ki), dimension(4) :: vecA0\n')
    if (int(rank)>=int(loopsize)+1):
        f90file.write('      complex(ki), dimension(4) :: vecA1\n')
    if (int(rank)>=int(loopsize)):
        f90file.write('      qshift = %s \n' % qshift)
        f90file.write('	     vecA0(1:4) = ' + qsign + ' a(0:3,0)\n')
    if (int(rank)>=int(loopsize)+1):
        f90file.write('	     vecA1(1:4) = ' + qsign + ' a(0:3,1) - qshift(1:4)\n')

f90file.write('      t1 = 0\n')

# avoids some warnings
if (n_t_terms==0):
    f90file.write('      coeffs(0) = 0.0_ki\n')

for lidx in range(0,n_t_terms):
    f90file.write('      call cond_t(epspow.eq.t1,brack_{0},vecA0,'.format(lidx)
                  + extra_arg + ' coeffs)\n')

f90file.write('   end subroutine numerator_tmu \n')
f90file.write('!---#] subroutine numerator_tmu: \n')


f90file.write('end module     [% process_name asprefix=\_%]'+diag_name[:-1]+'21\n')
f90file.close()   
### additional formatting for output files

postformat(tmpname)

shutil.move(tmpname,diag_name[:-1]+'21.f90')
