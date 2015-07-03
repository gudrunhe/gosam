[%
 ' vim: ts=3:sw=3:syntax=golem
%]
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

f90file.write('module     [% process_name asprefix=\_%]'+diag_name+'\n')
f90file.write('   ! file: '+str(os.getcwd())+diag_name+'.f90 \n')
f90file.write('   ! generator: buildfortran_d.py \n')
f90file.write('   use [% process_name asprefix=\_ %]config, only: ki \n')
f90file.write('   use [% process_name asprefix=\_ %]util, only: cond, d => metric_tensor \n')
f90file.write('\n')
f90file.write('   implicit none\n')
f90file.write('   private\n')
f90file.write('\n')
f90file.write('   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)\n')
# ADD MORE
for irank in range(0,rank+1):
    f90file.write('   integer, private :: iv' + str(irank) +'\n')
[%@if extension qshift %][% @else %]
f90file.write('   real(ki), dimension(4), private :: qshift \n')
[%@end @if %]
f90file.write('   public :: derivative [%
   @if extension golem95 %], reconstruct_d' + str(diagram) + '[%
   @end @if %]\n')
f90file.write(' \n')
f90file.write('contains \n')
for irank in range(1,rank+2):
	f90file.write('!---#[ function brack_%s: \n' % irank)
	f90file.write('   pure function brack_%s(Q' % irank[%
      @select r2
      @case implicit explicit %]+ ', mu2'[%
      @end @select %]+') result(brack)\n')
	f90file.write('      use [% process_name asprefix=\_ %]model \n')
	f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
	f90file.write('      use [% process_name asprefix=\_ %]color \n')
	f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
	f90file.write('      implicit none \n')
	f90file.write('      complex(ki), dimension(4), intent(in) :: Q\n')[%
      @select r2
      @case implicit explicit %]
	f90file.write('      complex(ki), intent(in) :: mu2\n')[%
      @end @select %]
	f90file.write('      complex(ki), dimension('+str(acd_maxl[irank-1])+') :: acd'+diag+'\n')
	f90file.write('      complex(ki) :: brack\n')

	f90file.write(outdict['Derive%s' % str(irank-1)])
	f90file.write('   end function brack_%s\n' % irank)
	f90file.write('!---#] function brack_%s: \n' % irank)

f90file.write('!---#[ function derivative: \n')
dstring='   function derivative(' + [%
   @if internal DERIVATIVES_AT_ZERO %][%
   @else %]'Q_ext,' + [%
   @end @if %]'mu2,' 
indices=[]
for irank in range(0,rank):
	dstring += 'i' + str(irank+1) +','
	indices.append(str(irank+1))

dstring=dstring.rstrip(',') + ')' + ' result(numerator)\n'
f90file.write(dstring)
f90file.write('      use [% process_name asprefix=\_ %]globalsl1, only: epspow \n')
f90file.write('      use [% process_name asprefix=\_ %]kinematics \n')
f90file.write('      use [% process_name asprefix=\_ %]abbrevd'+diag[% @if helsum %][% @else %]+'h'+heli[% @end @if %]+'\n')
f90file.write('      implicit none \n')[%
      @if internal DERIVATIVES_AT_ZERO %][%
      @else %]
f90file.write('      complex(ki), dimension(4), intent(in) :: Q_ext\n')[%
      @end @if %]
f90file.write('      complex(ki), intent(in) :: mu2 \n')
for item in indices:
	f90file.write('      integer, intent(in), optional :: i%s \n' %item)

f90file.write('      complex(ki) :: numerator \n')
f90file.write('      complex(ki) :: loc \n')
# ???
f90file.write('      integer :: t1 \n')
# ???
f90file.write('      integer :: deg \n')
[%
      @if internal DERIVATIVES_AT_ZERO %]
f90file.write('      complex(ki), dimension(4), parameter :: Q = (/ (0.0_ki,0.0_ki),(0.0_ki,0.0_ki),(0.0_ki,0.0_ki),(0.0_ki,0.0_ki)/)\n')[%
      @else %]
f90file.write('      ! The Q that goes into the diagram \n')
f90file.write('      complex(ki), dimension(4) :: Q\n')[%
      @end @if %][%
      @if extension qshift %][%
      @else %]
if qshift==0:
	f90file.write('	     qshift(:) = 0.0_ki \n')
else:
	f90file.write('      qshift = %s \n' % qshift)[%
      @end @if %][%
      @if internal DERIVATIVES_AT_ZERO %][%
      @else %][%
      @if extension qshift %]
f90file.write('      Q(:) = Q_ext(:)\n')[%
      @else %]
if qshift == 0:      
	f90file.write('      Q(:) = %s Q_ext(:)\n' % qsign)
else:
	f90file.write('      Q(:) = %s Q_ext(:) - qshift(:)\n' % qsign)[%
      @end @if %][%
@end @if %]
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
	[%@select r2 @case explicit implicit %]
	brackstr = 'brack_%s' % str(irank) 
	[%@end @select %]
	wstr = '         numerator = cond(epspow.eq.t1,%s,Q,mu2)\n' % brackstr
	f90file.write(wstr)
	f90file.write('         return\n')
	f90file.write('      end if\n')   

f90file.write('   end function derivative \n') 
f90file.write('!---#] function derivative: \n')[%
@if extension golem95 %]
f90file.write('!---#[ subroutine reconstruct_d%s: \n' % str(diagram))
f90file.write('   subroutine     reconstruct_d%s(coeffs) \n' % str(diagram))
f90file.write('      use [% process_name asprefix=\_ %]groups, only: tensrec_info_group%s\n' % group)
f90file.write('      implicit none \n')
f90file.write('      complex(ki), parameter :: czip = (0.0_ki, 0.0_ki) \n')
f90file.write('      complex(ki), parameter :: cone = (1.0_ki, 0.0_ki) \n')
f90file.write('      complex(ki), parameter :: ctwo = (2.0_ki, 0.0_ki) \n')
f90file.write('      type(tensrec_info_group%s), intent(out) :: coeffs \n' % group)[%
	@select r2 @case implicit %]
if int(loopsize) in [0,1,2,3,4,5]:
	if int(rank) not in [0,1,2,3] and int(loopsize)<5:
		f90file.write('      complex(ki) :: x1,x2\n')
	if int(loopsize)==5 and int(rank)>=6:
		f90file.write('      complex(ki) :: x1,x2,x3\n')[%
	@end @select %][%
	@if internal DERIVATIVES_AT_ZERO %][%
	@else %]
f90file.write('      complex(ki), dimension(4), parameter :: Q = (/czip,czip,czip,czip/)\n')[%
	@end @if %][%
   @for repeat max_rank inclusive=true var=rk %][%
		@if is_first%]
if int(rank) == [% rk %]:[%
		@else %]
elif int(rank) == [% rk %]:[%
		@end @if %]
	f90file.write('      ! rank %s case :\n' % rank)
	f90file.write('      !---[# reconstruct coeffs%%coeffs_%s:\n' % diagram)[%
      @for tens_rec_info rk shift_args=1 %]
	f90file.write('      coeffs%%coeffs_%s' % diagram)[%
         @if eval rk .gt. 0 %]
	f90file.write('%c[% coeff %]')[%
            @select coeff @case 0 %][%
            @else %]
	f90file.write('([%k%],[%i%])')[%
            @end @select %][%
         @end @if %]
	f90file.write(' = ')[%
         @select sign @case -1 %]
	f90file.write('-')[%
         @end @select %]
	f90file.write('derivative(')[%
         @if internal DERIVATIVES_AT_ZERO %][%
         @else %]
	f90file.write('Q,')[%
         @end @if %]
	f90file.write('czip')[%
         @for elements args delim=, %]
	f90file.write(',[% $_ %]')[%
         @end @for %]
	f90file.write(')')[%
         @if eval symmetry .gt. 1 %] 
	f90file.write('/[% symmetry %].0_ki')[%
         @end @if %]
	f90file.write('\n')[%
      @end @for tens_rec_info rk %]
	f90file.write('      !---#] reconstruct coeffs%%coeffs_%s:\n' % diagram)[%
      @select r2 @case implicit %]
	if int(loopsize) in [0,1,2,3,4,5]:
		if int(rank) in [2,3] and int(loopsize)<5:
			f90file.write('      !---#[ reconstruct coeffs%%coeffs_%ss1:\n' % diagram)[%
            @with eval rk - 2 result=rkk %][%
               @for tens_rec_info rkk shift_args=1 %]
			f90file.write('      coeffs%%coeffs_%ss1' %diagram)[%
                  @if eval rkk .gt. 0 %]
			f90file.write('%c[% coeff %]')[%
                     @select coeff @case 0 %][%
                     @else %]
			f90file.write('([%k%],[%i%])')[%
                     @end @select %][%
                  @end @if %] 
			f90file.write('=')[%
                  @select sign @case -1 %]
			f90file.write('-')[%
                  @end @select %]
			f90file.write('derivative(')[%
                  @if internal DERIVATIVES_AT_ZERO %][%
                  @else %]
			f90file.write('Q,')[%
                  @end @if %]
			f90file.write('cone')[%
                  @for elements args delim=, %]
			f90file.write(',[% $_ %]')[%
                  @end @for %]
			f90file.write(')')[%
                  @if eval symmetry .gt. 1 %] 
			f90file.write('/ [% symmetry %].0_ki')[%
                  @end @if %]
			f90file.write('- coeffs%%coeffs_%s%%c[% coeff %]' % diagram)[%
                  @select coeff @case 0 %][%
                  @else %]
			f90file.write('([%kmap%],[%imap%])')[%
                  @end @select %]
			f90file.write('\n')[%
               @end @for tens_rec_info rkk %][%
            @end @with eval rkk %]
			f90file.write('      !---#] reconstruct coeffs%%coeffs_%ss1:\n' % diagram )
		elif int(rank) not in [0,1] and int(loopsize)<5:
			f90file.write('      !---#[ reconstruct coeffs%%coeffs_%ss1 and s2:\n' % diagram)[%
            @with eval rk - 2 result=rkk %][%
               @for tens_rec_info rkk shift_args=1 %]
			f90file.write('      x1 = ')[%
                  @select sign @case -1 %]
			f90file.write('-')[%
                  @end @select %]
			f90file.write('derivative(')[%
                  @if internal DERIVATIVES_AT_ZERO %][%
                  @else %]
			f90file.write('Q,')[%
                  @end @if %]
			f90file.write('cone')[%
                  @for elements args delim=, %]
			f90file.write(',[% $_ %]')[%
                  @end @for %]
			f90file.write(')')[%
                  @if eval symmetry .gt. 1 %]
			f90file.write('/[% symmetry %].0_ki')[%
                  @end @if %]
			f90file.write('- coeffs%%coeffs_%s%%c[% coeff %]' % diagram)[%
                  @select coeff @case 0 %][%
                  @else %]
			f90file.write('([%kmap%],[%imap%])')[%
                  @end @select %]
			f90file.write('\n')
			f90file.write('      x2 = ')[%
                  @select sign @case -1 %]
			f90file.write('-')[%
                  @end @select %]
			f90file.write('derivative(')[%
                  @if internal DERIVATIVES_AT_ZERO %][%
                  @else %]
			f90file.write('Q,')[%
                  @end @if %]
			f90file.write('-cone')[%
                  @for elements args delim=, %]
			f90file.write(',[% $_ %]')[%
                  @end @for %]
			f90file.write(')')[%
                  @if eval symmetry .gt. 1 %]
			f90file.write('/ [% symmetry %].0_ki')[%
                  @end @if %] 
			f90file.write(' - coeffs%%coeffs_%s%%c[% coeff %]' % diagram)[%
                  @select coeff @case 0 %][%
                  @else %]
			f90file.write('([%kmap%],[%imap%])')[%
                  @end @select %]
			f90file.write('\n')
			f90file.write('      coeffs%%coeffs_%ss1' % diagram)[%
                  @if eval rkk .gt. 0 %]
			f90file.write('%c[% coeff %]')[%
                     @select coeff @case 0 %][%
                     @else %]
			f90file.write('([%k%],[%i%])')[%
                     @end @select %][%
                  @end @if %]
			f90file.write('= 0.5_ki * (x1 - x2)')
			f90file.write('\n')
			f90file.write('      coeffs%%coeffs_%ss2' % diagram)[%
                  @if eval rkk .gt. 0 %]
			f90file.write('%c[% coeff %]')[%
                     @select coeff @case 0 %][%
                     @else %]
			f90file.write('([%k%],[%i%])')[%
                     @end @select %][%
                  @end @if %]
			f90file.write('= 0.5_ki * (x1 + x2)')
			f90file.write('\n')[%
               @end @for tens_rec_info %][%
            @end @with eval rkk %]
			f90file.write('      !---#] reconstruct coeffs%%coeffs_%ss1 and s2:\n' % diagram)
		elif int(loopsize)==5 and int(rank)>=6:
			f90file.write('      !---#[ reconstruct coeffs%%coeffs_%ss1, s2 and s3:\n' % diagram)[%
            @with eval rk - 2 result=rkk %][%
               @for tens_rec_info rkk shift_args=1 %]
			f90file.write('      x1 =')[%
                  @select sign @case -1 %]
			f90file.write('-')[%
                  @end @select %]
			f90file.write('derivative(')[%
                  @if internal DERIVATIVES_AT_ZERO %][%
                  @else %]
			f90file.write('Q,')[%
                  @end @if %]
			f90file.write('cone')[%
                  @for elements args delim=, %]
			f90file.write(',[% $_ %]')[%
                  @end @for %]
			f90file.write(')')[%
                  @if eval symmetry .gt. 1 %]
			f90file.write('/[% symmetry %].0_ki')[%
                  @end @if %]
			f90file.write(' - coeffs%%coeffs_%s%%c[% coeff %]' % diagram)[%
                  @select coeff @case 0 %][%
                  @else %]
			f90file.write('([%kmap%],[%imap%])')[%
                  @end @select %]
			f90file.write('\n')
			f90file.write('      x2 = ')[%
                  @select sign @case -1 %]
			f90file.write('-')[%
                  @end @select %]
			f90file.write('derivative(')[%
                  @if internal DERIVATIVES_AT_ZERO %][%
                  @else %]
			f90file.write('Q,')[%
                  @end @if %]
			f90file.write('-cone')[%
                  @for elements args delim=, %]
			f90file.write(',[% $_ %]')[%
                  @end @for %]
			f90file.write(')')[%
                  @if eval symmetry .gt. 1 %]
			f90file.write('/[% symmetry %].0_ki')[%
                  @end @if %]
			f90file.write(' - coeffs%%coeffs_%s%%c[% coeff %]' % diagram)[%
                  @select coeff @case 0 %][%
                  @else %]
			f90file.write('([%kmap%],[%imap%])')[%
                  @end @select %]
			f90file.write('\n')
			f90file.write('      x3 = ')[%
                  @select sign @case -1 %]
			f90file.write('-')[%
                  @end @select %]
			f90file.write('derivative(')[%
                  @if internal DERIVATIVES_AT_ZERO %][%
                  @else %]
			f90file.write('Q,')[%
                  @end @if %]
			f90file.write('ctwo')[%
                  @for elements args delim=, %]
			f90file.write(',[% $_ %]')[%
                  @end @for %]
			f90file.write(')')[%
                  @if eval symmetry .gt. 1 %]
			f90file.write('/[% symmetry %].0_ki')[%
                  @end @if %]
			f90file.write('- coeffs%%coeffs_%s%%c[% coeff %]' % diagram)[%
                  @select coeff @case 0 %][%
                  @else %]
			f90file.write('([%kmap%],[%imap%])')[%
                  @end @select %]
			f90file.write('\n')

			f90file.write('      coeffs%%coeffs_%ss1' % diagram)[%
                  @if eval rkk .gt. 0 %]
			f90file.write('%c[% coeff %]')[%
                     @select coeff @case 0 %][%
                     @else %]
			f90file.write('([%k%],[%i%])')[%
                     @end @select %][%
                  @end @if %]
			f90file.write('= x1 - x2/3._ki - x3/6._ki')
			f90file.write('\n')
			f90file.write('      coeffs%%coeffs_%ss2' % diagram)[%
                  @if eval rkk .gt. 0 %]
			f90file.write('%c[% coeff %]')[%
                     @select coeff @case 0 %][%
                     @else %]
			f90file.write('([%k%],[%i%])')[%
                     @end @select %][%
                  @end @if %]
			f90file.write('= 0.5_ki * (x1 + x2)')
			f90file.write('\n')
			f90file.write('      coeffs%%coeffs_%ss3' % diagram)[%
                  @if eval rkk .gt. 0 %]
			f90file.write('%c[% coeff %]')[%
                     @select coeff @case 0 %][%
                     @else %]
			f90file.write('([%k%],[%i%])')[%
                     @end @select %][%
                  @end @if %]
			f90file.write('= (x3 - x2)/6._ki - 0.5_ki * x1')
			f90file.write('\n')[%
               @end @for tens_rec_info %][%
            @end @with eval rkk %]
			f90file.write('      !---#] reconstruct coeffs%%coeffs_%ss1, s2 and s3:\n' % diagram)[%
      @end @select r2 %][%
   @end @for repeat max_rank %]



f90file.write('   end subroutine reconstruct_d%s\n' % str(diagram))
f90file.write('!---#] subroutine reconstruct_d%s:\n' % str(diagram))[%
@end @if %]




f90file.write('end module     [% process_name asprefix=\_%]'+diag_name+'\n')
f90file.close()   
### additional formatting for output files

postformat(tmpname)

shutil.move(tmpname,diag_name+'.f90')
