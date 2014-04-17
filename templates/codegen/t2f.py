# Last updated 02.04.2013

from cStringIO import StringIO
from tokenize import generate_tokens
import re
from filter import Fortran90

dotproduct_global=[]

def initconfig(con):
        for p in ['parameters','kinematics','symbols','lambdafunc','dotproducts']:
                if p not in con.keys():
                        con[p] = {}
        return con

def bmatch(lin):
        """
        returns list of bracket matched indices in a list
        """
        lh = [idx for idx,val in enumerate(lin)  if val=='(']
        rh = [idx for idx,val in enumerate(lin)  if val==')']
        bmatch=[]
        bmatchd={}
        for li,le in enumerate(lh):
                bmatchd[rh[li]] = 'r'
                bmatchd[le] = 'l'
        sort=sorted(bmatchd.iteritems())
        idx = 0
	embed = False
	ib = 0
	while sort != []:
		item = sort[idx]
		next = sort[idx+1]
		if item[1] == 'l':
			if next[1] == 'r':
				if not embed:
					ib = len(bmatch)
				else:
					ib = 0
				bmatch.insert(ib,[ sort.pop(idx)[0], sort.pop(idx)[0]])
				if embed:
					idx -= 1
					if idx<0:
						idx=0
						embed=False
			else:
				idx += 1
				embed = True
	bmatchd={}
	for l,r in bmatch:
		bmatchd[l] = r
	return bmatchd


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

def replace(function,args,lambdafunc):
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

def translate(tokens,inconfig):
	"""
	Takes a list of tokens and translates and returns a newlist
	with the required 'translations'

	Can have objects like 'csqrt(5)'...
	"""
	config=initconfig(inconfig)
        parameters=config['parameters']
        kinematics=config['kinematics']
        symbols=config['symbols']
        lambdafunc=config['lambdafunc']
        dotproducts=config['dotproducts']

	newlist=[]
	ilist=0
	itoken=0
	
	bd = bmatch(tokens)
	while itoken < len(tokens):
		token = tokens[itoken]
# special case for abbreviations
		abbpre = re.sub("\d+", " ", token).strip()
		if abbpre in parameters.keys() and  parameters[abbpre] == 'array':
			newtoken= token + '(%s)' % tokens[itoken+2]
			newlist.append(newtoken)
			itoken = itoken+4
		elif abbpre in parameters.keys() and  parameters[abbpre] == 'matrix':
			newtoken= token + '(%s,%s)' % (tokens[itoken+2],tokens[itoken+4])
			newlist.append(newtoken)
			itoken = itoken+6
		elif token in lambdafunc.keys():
			# function(argument,...) 
			# token is 'function',
			# the next token is '('
			l,r = itoken+1, bd[itoken+1]
			function=token
			bracklist = tokens[l+1:r]
			itoken = itoken + len(bracklist)
			tlist = translate(bracklist,config)
			args = glue(tlist).split(',')
			itoken = itoken +1
			newitem = replace(token,args,lambdafunc)
			newlist.append(newitem[0])
			itoken = itoken + 2
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

def translatefile(infile_name,config,keepleft=False):
	"""
	Opens infile_name, and parses the input

	The output is a list of dictionary of the format:

	{ 'Abbrevations' : outstring, 'R2' : outstring, 'Diagram' : outstring...}

	If keepleft is set equal to True, then we also have an entry returned
	that gives a dictionary of all the variables on the left hand side
	of the expressions

	"""

	outstring=''
	blockname=''
	inf=open(infile_name,'r')
	leftlist=[]
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
			if keepleft==True and lhs not in leftlist:
				leftlist.append(lhs)
			end = rhs[-1]
			while end != ';':
				rhs += inf.readline().strip(' \n')
				end = rhs[-1]
			tokens = tokeniseline(rhs)
			translated=translate(tokens,config)
			outstring=outstring + output(lhs,glue(translated))
		else:
			continue

	outdict[blockname] = outstring
	del outdict['']
	inf.close()
	outdict['dplist'] = dotproduct_global
	if keepleft==True:
		outdict['lhs']=leftlist
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




