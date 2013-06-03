[%
 ' vim: ts=3:sw=3:syntax=golem
%]#! /usr/bin/env python


import sys
import os
from optparse import OptionParser
from t2f import translatefile, getdata, postformat
from pythonin import parameters, kinematics, symbols, lambdafunc, dotproducts

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
diag=diag_name.split('d')[1].split('h')[0]
heli=diag_name.split('h')[1].split('l')[0]
qsign=options.qsign
qshift=options.qshift
rank=options.rank
diagram=options.diagram
group=options.group
loopsize=options.loopsize
# print '----------------------------------'
# print 'Input file is:      %s' % diag_name+'.txt'
# print 'Diagram written in: %s' % diag_name+'.f90'
# print 'Abbrev. written in: %s' % 'abbrevd'+diag+'h'+heli+'.f90'
# print 'Diagram information:'
# print 'diag:  %s' % options.diagram
# print 'group: %s' % options.group
# print 'heli:  %s' % options.helicity
# print 'qsign: %s' % options.qsign
# print 'qshif: %s' % options.qshift
# print '----------------------------------'

txtfile = open(diag_name+'.txt','r')
f90file = open(diag_name+'.f90', 'w')
datfilename = diag_name.rstrip('2') + '.dat'
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
if ( int(rank)==int(loopsize) and int(loopsize) >= 4 ):
    n_t_terms = 1

for lidx in range(0,n_t_terms):
    acdmax=getdata(datfilename)['nind{0}diagram_terms'.format(lidx)]
    if acdmax == '0':
        acdmax = 1
    acd_maxl.append(acdmax)


# Write abbreviation file

f90file.write('module     [% process_name asprefix=\_%]'+diag_name+'\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name+'.f90 \n')
f90file.write('   ! generator: buildfortran_n3.py \n')
f90file.write('   use [% process_name asprefix=\_ %]config, only: ki \n')
f90file.write('   use [% process_name asprefix=\_ %]util, only: cond, d => metric_tensor \n')
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
#f90file.write('   complex(ki), dimension(4), private :: vecA\n')
#f90file.write('   complex(ki), private :: beta\n')
[%@if extension qshift %][% @else %]
#f90file.write('   real(ki), dimension(4), private :: qshift \n')
[%@end @if %]
f90file.write('   public :: numerator_d\n')
f90file.write(' \n')
f90file.write('contains \n')
for lidx in range(0,n_t_terms):
	f90file.write('!---#[ function brack_%s: \n' % lidx)
        # T.P. removed the explicit-implicit mu^2 stuff
	f90file.write('   pure function brack_%s(vecA,beta) result(brack)\n' % lidx)
	f90file.write('      use [% process_name asprefix=\_ %]model \n')
	f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
	f90file.write('      use [% process_name asprefix=\_ %]color \n')
	f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag+'h'+heli+'\n')
	f90file.write('      implicit none \n')
        f90file.write('   complex(ki), dimension(4), intent(in) :: vecA\n')
        f90file.write('   complex(ki), intent(in) :: beta\n')
	#f90file.write('      complex(ki), dimension(4), intent(in) :: Q\n')
	#f90file.write('      complex(ki), intent(in) :: mu2\n')
	f90file.write('      complex(ki), dimension('+str(acd_maxl[lidx])+') :: acd'+diag+'\n')
	f90file.write('      complex(ki) :: brack\n')

	f90file.write(outdict['NinjaDouble%s' % str(lidx)])
	f90file.write('   end function brack_%s\n' % lidx)
	f90file.write('!---#] function brack_%s: \n' % lidx)

f90file.write('!---#[ subroutine numerator_d:\n')
f90file.write('   subroutine numerator_d(ncut, loc_beta, a, coeffs) &\n' )
f90file.write('   & bind(c, name="[% process_name asprefix=\_ %]d{0}h{1}_ninja_d")\n'.format(diag,heli) )
f90file.write('      use iso_c_binding, only: c_int\n')
f90file.write('      use ninja_module, only: ki => ki_nin\n')
f90file.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow \n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag+'h'+heli+'\n')
f90file.write('      implicit none \n')
f90file.write('      integer(c_int), intent(in) :: ncut\n')
f90file.write('      complex(ki), intent(in) :: loc_beta \n')
f90file.write('      complex(ki), dimension(0:3), intent(in) :: a\n')
f90file.write('      complex(ki), dimension(0:*), intent(out) :: coeffs\n')
# ???
f90file.write('      integer :: t1 \n')
# ???
f90file.write('      integer, parameter :: deg = 0 \n')
f90file.write('      complex(ki) :: mu2\n')
f90file.write('      complex(ki), dimension(4) :: vecA\n')[%
      @if extension qshift %][%
      @else %]
#if qshift==0:
f90file.write('	     vecA(1:4) = ' + qsign + ' a(0:3)\n')
#	f90file.write('	     qshift(:) = 0.0_ki \n')
#else:
#	f90file.write('      qshift = %s \n' % qshift)[%
      @end @if %]

#f90file.write('      beta = loc_beta\n')
#f90file.write('      vecA = a\n')

f90file.write('      if (deg.lt.0) return\n')
f90file.write('      t1 = 0\n')

for lidx in range(0,n_t_terms):
    f90file.write('      coeffs({0}) = (cond(epspow.eq.t1,brack_{0},vecA,loc_beta))\n'.format(lidx))
    f90file.write('      if (deg.eq.{0}) return\n'.format(lidx))

f90file.write('   end subroutine numerator_d \n')
f90file.write('!---#] subroutine numerator_d: \n')


f90file.write('end module     [% process_name asprefix=\_%]'+diag_name+'\n')
f90file.close()   
### additional formatting for output files

postformat(diag_name + '.f90')

