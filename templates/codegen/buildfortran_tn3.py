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


outdict = translatefile(diag_name+'.txt',config)

acd_maxl = dict()
nl = int(loopsize)
rk = int(rank)
#n_t_terms = max( int(rank) - int(loopsize) + 4 - max(3-int(loopsize),0) , 0)

expids = ['31']
if (int(loopsize)>=3):
    expids.append('32')

for lidx in expids:
    acdmax=getdata(datfilename)['nin{0}diagram_terms'.format(lidx)]
    if acdmax == '0':
        acdmax = 1
    acd_maxl[lidx] = acdmax


# Write abbreviation file

f90file.write('module     [% process_name asprefix=\_%]'+diag_name[:-1]+'31\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name[:-1]+'31.f90 \n')
f90file.write('   ! generator: buildfortran_tn3.py \n')
f90file.write('   use [% process_name asprefix=\_ %]config, only: ki \n')
f90file.write('   use [% process_name asprefix=\_ %]util, only: cond_t, d => metric_tensor \n')
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
idxcount = 0
for tpow in range(rk-nl+3,-1,-1):
    for mupow in range(0,rk-nl+3+1-tpow,2):
        f90file.write('   integer, parameter :: ninjaidxt{0}mu{1} = {2}\n'.format(tpow,mupow,idxcount))
        idxcount = idxcount +1
f90file.write('   public :: numerator_t3\n')
f90file.write(' \n')
f90file.write('contains \n')
for lidx in expids:
	f90file.write('!---#[ subroutine brack_%s: \n' % lidx)
        # T.P. removed the explicit-implicit mu^2 stuff
	f90file.write('   pure subroutine brack_%s(ninjaA, ninjaE3, ninjaE4, ninjaP, brack)\n' % lidx)
	f90file.write('      use [% process_name asprefix=\_ %]model \n')
	f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
	f90file.write('      use [% process_name asprefix=\_ %]color \n')
	f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
	f90file.write('      implicit none \n')
	f90file.write('      complex(ki), dimension(4), intent(in) :: ninjaA, ninjaE3, ninjaE4\n')
#	f90file.write('      complex(ki), dimension(4), intent(in) :: Q\n')
	f90file.write('      complex(ki), intent(in) :: ninjaP\n')
	f90file.write('      complex(ki), dimension('+str(acd_maxl[lidx])+') :: acd'+diag+'\n')
	f90file.write('      complex(ki), dimension (0:*), intent(inout) :: brack\n')
	f90file.write(outdict['Ninja%s' % str(lidx)])
	f90file.write('   end subroutine brack_%s\n' % lidx)
	f90file.write('!---#] subroutine brack_%s: \n' % lidx)

f90file.write('!---#[ subroutine numerator_t3:\n')
f90file.write('   subroutine numerator_t3(ncut, a, b, c, param, deg, coeffs) &\n' )[%
@if helsum %]
f90file.write('   & bind(c, name="[% process_name asprefix=\_ %]d{0}_ninja_t3")\n'.format(diag) )[%
@else %]
f90file.write('   & bind(c, name="[% process_name asprefix=\_ %]d{0}h{1}_ninja_t3")\n'.format(diag,heli) )[%
@end @if %]
f90file.write('      use iso_c_binding, only: c_int\n')
f90file.write('      use ninjago_module, only: ki => ki_nin\n')
f90file.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow \n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
f90file.write('      implicit none \n')
f90file.write('      integer(c_int), intent(in) :: ncut, deg\n')
f90file.write('      complex(ki), dimension(0:3), intent(in) :: a, b, c\n')
f90file.write('      complex(ki), intent(in) :: param \n')
f90file.write('      complex(ki), dimension(4) :: vecA, vecB, vecC\n')
f90file.write('      complex(ki), dimension(0:*), intent(out) :: coeffs\n')
# ???
f90file.write('      integer :: t1 \n')
# ???
#f90file.write('      ! The Q that goes into the diagram \n')  # T.P.: This would be useless if it weren't for the form of brack_*(Q,mu^2).  We should use a brack_*(a,b,c,mu^2) instead
#f90file.write('      complex(ki), dimension(4), parameter :: Q = (/ (0.0_ki,0.0_ki),(0.0_ki,0.0_ki),(0.0_ki,0.0_ki),(0.0_ki,0.0_ki)/)\n')
if qshift=='0':
	f90file.write('	     vecA(1:4) = ' + qsign + ' a(0:3)\n')
	f90file.write('	     vecB(1:4) = ' + qsign + ' b(0:3)\n')
	f90file.write('	     vecC(1:4) = ' + qsign + ' c(0:3)\n')
else:
    f90file.write('      complex(ki), dimension(4) :: qshift\n')
    f90file.write('      qshift = %s \n' % qshift)
    f90file.write('	     vecA(1:4) = ' + qsign + ' a(0:3) - qshift(1:4)\n')
    f90file.write('	     vecB(1:4) = ' + qsign + ' b(0:3)\n')
    f90file.write('	     vecC(1:4) = ' + qsign + ' c(0:3)\n')

#f90file.write('      vecA = a\n')
#f90file.write('      vecB = b\n')
#f90file.write('      vecC = c\n')

f90file.write('      if (deg.lt.0) return\n')
f90file.write('      t1 = 0\n')

f90file.write('      call cond_t(epspow.eq.t1,brack_31,vecA,vecB,vecC,param,coeffs)\n')

if (len(expids)>=2):
    f90file.write('      if (deg.le.(1+({0}))) return\n'.format(rk-nl))
    f90file.write('      call cond_t(epspow.eq.t1,brack_32,vecA,vecB,vecC,param,coeffs)\n')

f90file.write('   end subroutine numerator_t3 \n')
f90file.write('!---#] subroutine numerator_t3: \n')


f90file.write('end module     [% process_name asprefix=\_%]'+diag_name[:-1]+'31\n')
f90file.close()   
### additional formatting for output files

postformat(tmpname)

shutil.move(tmpname,diag_name[:-1]+'31.f90')
