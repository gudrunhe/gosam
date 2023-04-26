
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
tmp_handle , tmpname = tempfile.mkstemp(suffix=".f90",prefix="gosam_tmp")
f90file = os.fdopen(tmp_handle,"w")

datfilename = diag_name.rstrip('d') + '.dat'
# import txt file
txt_lines=[]
dotprod_spva=[]
dotprod_sp=[]
dotprod_kdotl=[]
dotprod_kdote=[]
dotprod_kdotspva=[]


outdict=translatefile(diag_name+'.txt',config)

acd_maxl = []
for irank in range(0,rank+1):
	acdmax=getdata(datfilename)['d%sdiagram_terms' % str(irank)]
	if acdmax == '0':
		acdmax = 1
	acd_maxl.append(acdmax)


# Write abbreviation file

f90file.write('module     pb0_gghh_'+diag_name+'\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name+'.f90 \n')
f90file.write('   ! generator: buildfortran_d.py \n')
f90file.write('   use pb0_gghh_config, only: ki \n')
f90file.write('   use pb0_gghh_util, only: cond, d => metric_tensor \n')
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
# ADD MORE
for irank in range(0,rank+1):
    f90file.write('   integer, private :: iv' + str(irank) +'\n')

f90file.write('   real(ki), dimension(4), private :: qshift \n')

f90file.write('   public :: derivative \n')
f90file.write(' \n')
f90file.write('contains \n')
for irank in range(1,rank+2):
	f90file.write('!---#[ function brack_%s: \n' % irank)
	f90file.write('   pure function brack_%s(Q' % irank+ ', mu2'+') result(brack)\n')
	f90file.write('      use pb0_gghh_model \n')
	f90file.write('      use pb0_gghh_kinematics \n')
	f90file.write('      use pb0_gghh_color \n')
	f90file.write('      use pb0_gghh_abbrevd'+diag+'_2'+'h'+heli+'\n')
	f90file.write('      implicit none \n')
	f90file.write('      complex(ki), dimension(4), intent(in) :: Q\n')
	f90file.write('      complex(ki), intent(in) :: mu2\n')
	f90file.write('      complex(ki), dimension('+str(acd_maxl[irank-1])+') :: acd'+diag+'\n')
	f90file.write('      complex(ki) :: brack\n')

	f90file.write(outdict['Derive%s' % str(irank-1)])
	f90file.write('   end function brack_%s\n' % irank)
	f90file.write('!---#] function brack_%s: \n' % irank)

f90file.write('!---#[ function derivative: \n')
dstring='   function derivative(' + 'mu2,'
indices=[]
for irank in range(0,rank):
	dstring += 'i' + str(irank+1) +','
	indices.append(str(irank+1))

dstring=dstring.rstrip(',') + ')' + ' result(numerator)\n'
f90file.write(dstring)
f90file.write('      use pb0_gghh_globalsl1, only: epspow \n')
f90file.write('      use pb0_gghh_kinematics \n')
f90file.write('      use pb0_gghh_abbrevd'+diag+'_2'+'h'+heli+'\n')
f90file.write('      implicit none \n')
f90file.write('      complex(ki), intent(in) :: mu2 \n')
for item in indices:
	f90file.write('      integer, intent(in), optional :: i%s \n' %item)

f90file.write('      complex(ki) :: numerator \n')
f90file.write('      complex(ki) :: loc \n')
# ???
f90file.write('      integer :: t1 \n')
# ???
f90file.write('      integer :: deg \n')

f90file.write('      complex(ki), dimension(4), parameter :: Q = (/ (0.0_ki,0.0_ki),(0.0_ki,0.0_ki),(0.0_ki,0.0_ki),(0.0_ki,0.0_ki)/)\n')
if qshift==0:
	f90file.write('	     qshift(:) = 0.0_ki \n')
else:
	f90file.write('      qshift = %s \n' % qshift)
f90file.write('      numerator = 0.0_ki \n')
f90file.write('      deg = 0 \n')
for item in indices:
	f90file.write('      if(present(i%s)) then\n' % item)
	f90file.write('          iv%s=i%s\n' % (item,item))
	f90file.write('          deg=%s\n' % item)
	f90file.write('      else\n')
	f90file.write('          iv%s=1\n' % item)
	f90file.write('      end if\n')
f90file.write('      t1 = 0\n')
for irank in range(1,rank+2):
	jtem = str(irank - 1)
	f90file.write('      if(deg.eq.%s) then\n' % jtem )
	
	brackstr = 'brack_%s' % str(irank)
	
	wstr = '         numerator = cond(epspow.eq.t1,%s,Q,mu2)\n' % brackstr
	f90file.write(wstr)
	f90file.write('         return\n')
	f90file.write('      end if\n')

f90file.write('   end function derivative \n')
f90file.write('!---#] function derivative: \n')




f90file.write('end module     pb0_gghh_'+diag_name+'\n')
f90file.close()



### additional formatting for output files

postformat(tmpname)

shutil.move(tmpname,diag_name+'.f90')


