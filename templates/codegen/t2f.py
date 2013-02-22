# Last updated 12.02.2013 - To be tested

from cStringIO import StringIO
from tokenize import generate_tokens
import re
#from golem.templates.filter import Fortran90
from pythonin import parameters, kinematics, symbols, lambdafunc, dotproducts
from filter import Fortran90


dotproduct_global=[]

def getdata(infile_string):
	"""
	Give the string of the infile 
	(the file should look like 
	x=1
	y=2
	..
	and return { 'x' : 1, 'y' : 2, ...}
	"""
	exit_loop = False
	inf=open(infile_string,'r')
	outdict ={}
	while not exit_loop:
		st=inf.readline()
		# readline returns an empty string if it is the end of the file
		if st == '':
			exit_loop = True
		else:
			xy=st.strip('\n').split('=')
			outdict[xy[0]] = xy[1]
	return outdict	


def tokeniseline(inline):
	"""
	line : string
	example :    '  1/( - mW^2 + es34 + i_*mW*wW);	'
	returns a list of tokens 
	"""
	tokens = list(token[1] for token
		in generate_tokens(StringIO(inline).readline)
		if token[1])
	return tokens

def replace(function,args):
	# do we ever need more than 3 args?
	argl=args
	#.split(',')
	nargs = len(args)
	if nargs == 1:
		return [lambdafunc[function](argl[0]),nargs]
	elif nargs == 2:
		return [lambdafunc[function](argl[0],argl[1]),nargs]
	elif nargs == 3:
		return [lambdafunc[function](argl[0],argl[1],argl[2]),nargs]

def translate(tokens):
	"""
	Takes a list of tokens and translates and returns a newlist
	with the required 'translations'

	Can have objects like 'csqrt(5)'...
	"""
	newlist=[]
	ilist=0
	itoken=0
	bcount=0
	while itoken < len(tokens):
		token = tokens[itoken]
# special case for abbreviations
		abbpre = re.sub("\d+", " ", token).strip()
		if abbpre in parameters.keys() and  parameters[abbpre] == 'array':
			newtoken= token + '(%s)' % tokens[itoken+2]
			newlist.append(newtoken)
			itoken = itoken+4
		elif token in lambdafunc.keys():
			function=token
        	        l_rel = tokens[bcount:].index('(')
                	r_rel = tokens[bcount:].index(')')
	                l_abs = bcount + l_rel
        	        r_abs = bcount + r_rel
                	bcount = bcount + r_rel + 1
	               	bracklist = tokens[l_abs+1:r_abs]
			itoken = itoken + len(bracklist)
			tlist = translate(bracklist)
			args = glue(tlist).split(',')
	               	newlist.append('(')
			itoken = itoken +1
			newitem = replace(function,args)
			newlist.append(newitem[0])
			itoken = itoken + 1
	       	        newlist.append(')')
			itoken = itoken + 1
		elif token in dotproducts.keys():
			if token not in dotproduct_global:
				dotproduct_global.append(token)
			newlist.append(token)
			itoken=itoken+1
		elif token in symbols.keys():
			if token == '^':
				if tokens[itoken+1] == '-':
					newtoken = symbols[token] + '(-%s)' % tokens[itoken +2]
					itoken=itoken +3
				else:
					newtoken = symbols[token] + '%s' % tokens[itoken +1]
					itoken=itoken +2
				newlist.append(newtoken)
			else:
				newlist.append(symbols[token])
				itoken = itoken+1
		else:
			if token.isdigit():
				token = token + '.0_ki'
			newlist.append(token)
			itoken = itoken + 1
	return newlist

def glue(tokens):
	"""
	Takes a list and glues all the items together: returns a string
	"""
	str=''
	for token in tokens:
		str = str + token
	return str.rstrip(';')

def output(lhs,rhs):
	"""
	Take a string of the converted output and return nicely formatted
	output
	"""
	line = '      ' +  lhs.strip() + '=' + rhs.strip() + '\n'
	return line

def notblank(line):
	line=line.rstrip()
	if line:
		if not line[0] == '*':
			return line
	else:
		return 

def translatefile(infile_name):
	"""
	Opens infile_name, and parses the input
	then outputs to a string (outstring)

	The output is a list of dictionary of the format:

	{ 'Abbrevations' : outstring, 'R2' : outstring, 'Diagram' : outstring...}
	"""

	outstring=''
	blockname=''
	inf=open(infile_name,'r')

      	exit_loop = False
	outdict = {}
	while not exit_loop:
		st=inf.readline()
		# readline returns an empty string if it is the end of the file
		if st == '':
			exit_loop = True
		elif st[0] == '#':
			outdict[blockname] = outstring
			outstring = ''
			blockname = st.split('#####')[1].strip('\n')
		elif notblank(st):
			rl=st.strip(' \n').split('=')
			rhs=rl[1]
			lhs=rl[0]
			end = rhs[-1]
			while end != ';':
				rhs += inf.readline().strip(' \n')
				end = rhs[-1]
			tokens = tokeniseline(rhs)
			translated=translate(tokens)
			outstring=outstring + output(lhs,glue(translated))
		else:
			continue

	outdict[blockname] = outstring
	del outdict['']
	inf.close()
	outdict['dplist'] = dotproduct_global

	return outdict

def postformat(filename):
	"""
	Takes the input and puts it through a fortran90 filter
	to formate the width and comments correctly
	"""
	file= open( filename, 'r')
	fs = file.read()
	file.close()
	file= open( filename, 'w')
	newfilter= Fortran90(file,width='80')
	newfilter.write(fs)
	file.close()




