# vim: ts=3:sw=3:expandtab
# Input for python parser. It is here because Python needs it
# and you specified extensions=formopt

# we need types of parameters
# a list of all functions
# a list of all dotproducts
# a list of mathematical operators and their translations


parameters={[%
	include codegen/model-define.py class=Model %]
	'TR' : 'real',
	'pi' : 'real',
   'i_' : 'complex',
   'abb' : 'array',
   'ctabb' : 'array',   
   'acc' : 'array',
   'acd' : 'array',
   'abbWrap' : 'array',
   'mabb' : 'array'
   } 


[%
include codegen/kinematicsdef.py class=Kinematics
%]


symbols = {
            'sqrt2' : 'sqrt2',
            'Sqrt2' : 'sqrt2',
            'Qt2' : 'mu2',
            '/' : '/' ,
         	'(' : '(' ,
           	')' : ')' ,
         	'^' : '**',
         	'+' : '+',
         	'-' : '-',
         	'*' : '*',
            'ZERO' : '0.0_ki'
	}


lambdafunc = {  'madf'  :  lambda x,y,z: '%s + %s + %s' % (x,y,z),
                'log'   :  lambda x : 'log(%s)' % x,
                'csqrt' :  lambda x:  'sqrt(%s)' % x,
	             'sqrt'  :  lambda x:  'sqrt(%s)' % x,
  	             'sin'  :  lambda x:  'sin(%s)' % x,
	             'cos'  :  lambda x:  'cos(%s)' % x,
	             'tan'  :  lambda x:  'tan(%s)' % x,
	             'asin'  :  lambda x:  'asin(%s)' % x,
	             'acos'  :  lambda x:  'acos(%s)' % x,
	             'atan'  :  lambda x:  'atan(%s)' % x,
	             'exp'  :  lambda x:  'exp(%s)' % x,
                'pow'  :  lambda x,y : '(%s)**(%s)' % (x,y),
                'atan2' : lambda x,y : 'atan2(%s, %s)' % (x,y),
                'fabs' : lambda x : 'abs(%s)' % (x,y),
                'if' : lambda x,y,z : 'ifpos(%s,%s,%s)' % (x,y,z),
                'complexconjugate' : lambda x : 'conjg(%s)' % x,
  	             'SpSqrt' : lambda x : 'sqrt(%s)' % x,
                'dotproduct' : lambda x,y : 'dotproduct(%s,%s)' % (x,y),
                'SUBSCRIPT' : lambda f,x :  '%s(%s)' % (f,x),
                'Wrapper' : lambda f: '%s' % f,
                'd' : lambda x,y : 'd(%s,%s)' % (x,y)
            } 
