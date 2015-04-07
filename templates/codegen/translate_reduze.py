#!/usr/bin/python

import sys

class crossing:
  def __init__(self):
    self.name=None
    self.permutation=[]
    self.rules_momenta=[]
    self.rules_invariants=[]
    self.equiv={}

class Topology:
  def __init__(self):
    self.name=''
    self.loop=[]
    self.propagators=[]
    self.sp=[]
    self.crossing=[]

  
def get_permutation(line):
  permutation=[]
  line=line[1:-1]
  parts=line.split('],')
  for i in range(0,len(parts)-1):
    permutation.append(parts[i]+']')
  permutation.append(parts[len(parts)-1])
  return permutation		     
  

def gettopologies(infile):
  topologies=[]
  while True:
    line=infile.readline()
    if len(line)==0:
      break
    if line.find('Found valid sector mappings for')>=0:
	topology_complete=False
	newtopology=Topology()
	name=line.split('\n')[0].split('Found valid sector mappings for')[1]
	newtopology.name=name
	crossing_found=False
	name_found=False
	loop_found=False
	prop_found=False 
	sp_found=False	
	while not topology_complete:  
	  while not crossing_found:
	    line2=infile.readline()
	    if line2.find('permutation:')>=0:
	      cross=crossing()
	      part=line2.split('permutation: ')[1].strip('\n')
	      cross.permutation=get_permutation(part)
	    if line2.find('name:')>=0:
	      cross.name=line2.split('name: ')[1].strip('\n')
	    if line2.find('rules_momenta:')>=0:
	      part=line2.split('rules_momenta: ')[1].strip('\n')
	      cross.rules_momenta=get_permutation(part)
	    if line2.find('rules_invariants:')>=0:
	      part=line2.split('rules_invariants: ')[1].strip('\n')
	      cross.rules_invariants=get_permutation(part)
	    if line2.find('is equivalent to')>=0:
	      equiv=line2.split('is equivalent to ')[1].strip('\'\n')
	      cross.equiv[cross.name]=equiv
	      newtopology.crossing.append(cross)
	    if line2.find('---')>=0:
              position=infile.tell()
              line3=infile.readline()
              if line3.find('name')>=0:
	        crossing_found=True
	      else:
		infile.seek(position)
	        
	      

	  line1=infile.readline()
	  if line1.find('propagators')<0 and line1.find('-')>=0 and line1.find('---')<0 and not loop_found:
	    line1=line1.strip('\n')
	    newtopology.loop.append(line1.split('-')[1].split()[0])
	  if line1.find('propagators')>=0 and not loop_found:
	    loop_found=True
	  if loop_found and not prop_found and line1.find('standard')>=0:
	    line1=line1.strip('}\n')
	    newtopology.propagators.append(line1.split('standard: ')[1])
	  if line1.find('permutation')>=0 and not prop_found:
	    prop_found=True
	  if prop_found and not sp_found and line1.find('Rules scalar products to propagators')>=0:	    
	    spline=infile.readline()
	    spline=spline.strip('}{\n')
	    parts=spline.split('==')
	    for i in range(0,len(parts)):
	      if parts[i].startswith('SP'):
		newtopology.sp.append(parts[i])
	      else:
		parts1=parts[i].split(',SP')
		newtopology.sp.append(parts1[0])
		try:
		  newtopology.sp.append('SP'+parts1[1])
		except IndexError:
		  pass
	    sp_found=True	    
	    topology_complete=True
       
       
        topologies.append(newtopology)
    
  return topologies

def get_sp_momenta(sp):
  sp=sp.strip('SP()')
  parts=sp.split(',')
  sp=parts[0]+'.'+parts[1]
  return sp

def replace_squares(exp):
  return exp

def get_sp_exp(sp):
  sp1=sp.replace('Prop','num')
  sp2=sp1.replace('^(-1)','')
  sp3=sp2.replace('^2)',')')
  return sp3

def write_reduze_sp(top,spfile):
  spfile.write('If ( Match(Sector('+top.name+',?tail)) );\n')
  for i in range(0,len(top.sp),2):
    sp=get_sp_momenta(top.sp[i])
    exp=get_sp_exp(top.sp[i+1])
    spfile.write('id '+sp+' = ( '+exp+' );\n')
  spfile.write('EndIf;\n')

def replace_prop_tag(prop,i):
  prop=prop.strip('[]')
  prop=prop.replace('^2','')
  newprop='Tag(ReduzeN'+str(i)+','+prop+')'
  return newprop

def write_reduze_map_tag(top,mapfile):
  for i in range(0,len(top.propagators)):
    newprop=replace_prop_tag(top.propagators[i],i)
    mapfile.write('id Sector('+top.name+',?tail) = Sector('+top.name+',?tail)*'+newprop+';\n')
  mapfile.write('\n')  

def replace_prop_inv(prop,i):
  prop=prop.strip('[]')
  prop=prop.replace('^2','')
  newprop=[]
  parts=prop.split(',')
  newprop.append(prop)
  return newprop
    
def write_reduze_map_inv(top,mapfile):
  mapfile.write('If ( Match(Sector('+top.name+',?tail)) );\n')
  for i in range(0,len(top.propagators)):
    newprop=replace_prop_inv(top.propagators[i],i)
    mapfile.write('Multiply Tag(ReduzeN'+str(i)+','+newprop[0]+');\n')
  mapfile.write('EndIf;\n')
  mapfile.write('\n')  
  
def get_args_rules_momenta(momenta):
  momenta=momenta.strip(' []')
  parts=momenta.split(',')
  return parts[0], parts[1]
  
def write_reduze_crossing(top,crossfile):
  for i in range(0,len(top.crossing)):
    crossfile.write('Id Sector('+top.name+top.crossing[i].name+',?tail) = Crossing('+ \
      top.name+top.crossing[i].name+')*Sector('+top.name+',?tail);\n')
    crossfile.write('If ( Match(Crossing('+top.name+top.crossing[i].name+')) );\n')
    crossfile.write(' Multiply CrossingShift(')
    for j in range(0,len(top.crossing[i].rules_momenta)-1):
      arg1,arg2=get_args_rules_momenta(top.crossing[i].rules_momenta[j])
      crossfile.write(arg1+','+arg2+',[],')
    arg1,arg2=get_args_rules_momenta(top.crossing[i].rules_momenta[len(top.crossing[i].rules_momenta)-1])  
    crossfile.write(arg1+','+arg2+',[]')
    crossfile.write(');\n')
    crossfile.write(' Multiply CrossingInvariants(')
    for j in range(0,len(top.crossing[i].rules_invariants)-1):
      arg1,arg2=get_args_rules_momenta(top.crossing[i].rules_invariants[j])
      crossfile.write(arg1+','+arg2+',[],')
    try:  
      arg1,arg2=get_args_rules_momenta(top.crossing[i].rules_invariants[len(top.crossing[i].rules_invariants)-1])  
      crossfile.write(arg1+','+arg2+',[]')
    except:
      crossfile.write('[]')
    crossfile.write(');\n')
    crossfile.write('EndIf;\n')
    crossfile.write('\n')
    
    


if __name__=='__main__':
  path = sys.argv[1]
  infile=file(path+'setup_sector_mappings.log')
  spfile=open(path+'reduzesptop.hh','w')
  mapfile=open(path+'reduzemap.hh','w')
  crossfile=open(path+'reduzecrossing.hh','w')

  topologies=gettopologies(infile)
  
  for i in range(0, len(topologies)):
    write_reduze_sp(topologies[i],spfile)
    write_reduze_map_inv(topologies[i],mapfile)
    write_reduze_crossing(topologies[i],crossfile)
    
    
  
  mapfile.close()
  spfile.close()
  infile.close()