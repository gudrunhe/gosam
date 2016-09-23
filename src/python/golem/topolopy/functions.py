# vim: ts=3:sw=3:expandtab

import imp
import os.path
from yaml import load, load_all, dump
import sys

import golem.properties

from golem.topolopy.objects import Diagram, Propagator, Leg, LoopCache
import golem.topolopy.userlib
from golem.util.config import GolemConfigError
from golem.util.tools import error, warning, debug

def setup_list(prop, conf):
   result = []
   for r in conf.getListProperty(prop):
      if r=='':
         continue
      if ":" in r:
         boundaries = r.split(":")
         if len(boundaries) == 1:
            a = int(boundaries[0])
            b = a + 1
            c = 1
         elif len(boundaries) == 2:
            a = int(boundaries[0])
            b = int(boundaries[1])+1
            c = 1
         elif len(boundaries) == 3:
            a = int(boundaries[0])
            b = int(boundaries[1])+1
            c = int(boundaries[2])
         else:
            error("Invalid range: %r" % r)
         result.extend(range(a,b,c))
      else:
         result.append(int(r))
   return result

def setup_filter(prop, conf, model):
   generate_ct_internal = conf.getBooleanProperty("generate_ct_internal")
   locs = {}
   globs = globals().copy()

   globs.update(model.particles)
   globs["_"] = None

   quarks = []
   leptons = []
   fermions = []
   bosons = []
   
   #if generate_ct_internal and prop._name=='filter.nlo':
       #try:
            #if len(conf["filter.nlo"])==0:
                #conf["filter.nlo"]='lambda d: d.iprop(Cx)==0'
            #else:
                #conf["filter.nlo"]+='and d.iprop(Cx)==0'
       #except:
           ##conf["filter.nlo"]='lambda d: d.iprop(Cx)==0'
           #conf.setProperty("filter.nlo",'lambda d: d.iprop(Cx)==0')
           
           
   #golem.properties.filter_nlo_diagrams.setProperty('lambda d: d.iprop(g)==0')           
   #golem.properties.
   #prop._default='lambda d: d.iprop(Cx)==0'
   #print conf["filter.nlo"]


   for name, prtcl in model.particles.items():
      tsp = prtcl.getSpin()
      clr = prtcl.getColor()

      if tsp % 2 == 1:
         fermions.append(name)
      else:
         bosons.append(name)
      if abs(tsp) == 1 and abs(clr) == 3:
         quarks.append(name)
      if abs(tsp) == 1 and abs(clr) == 1:
         leptons.append(name)

   golem.topolopy.userlib.QUARKS = quarks
   golem.topolopy.userlib.LEPTONS = leptons
   golem.topolopy.userlib.FERMIONS = fermions
   golem.topolopy.userlib.BOSONS = bosons

   for name in dir(golem.topolopy.userlib):
      if name.startswith("_"):
         continue
      globs[name] = getattr(golem.topolopy.userlib, name)

   fltr_mod_file = conf.getProperty(golem.properties.filter_module).strip()
   if fltr_mod_file:
      try:
         fltr_mod_file=os.path.expanduser(os.path.expandvars(fltr_mod_file))
         execfile(fltr_mod_file, globs, globs)
      except IOError as ex:
         error("Problems reading filter module %r: %s" %
               (fltr_mod_file, str(ex)))
      except SyntaxError as ex:
         error("Syntax error while reading filter module %r [%d:%d]: %s" % 
               (ex.filename, ex.lineno, ex.offset, ex.msg),
               ex.text)

   fltr = conf.getProperty(prop)
   if len(fltr.strip()):
      try:
         return eval(fltr, globs)
      except SyntaxError as ex:
         error("Option %s is not a valid expression" % prop)
   else:
      return lambda d: True

def analyze_tree_diagrams(diagrams, model, conf, filter_flags = None):
   zero = golem.util.tools.getZeroes(conf)
   lst = setup_list(golem.properties.select_lo_diagrams, conf)
   fltr = setup_filter(golem.properties.filter_lo_diagrams, conf, model)
   keep = []
   lose = []
   signs = {}
   # flows = {}

   for idx, diagram in diagrams.items():

      if lst:
         if idx not in lst:
            lose.append(idx)
            continue

      if diagram.EHCfound():
         conf["ehc"]=True

      if analyze_diagram(diagram, zero, fltr):
         keep.append(idx)

         if filter_flags is not None:
            for flag in diagram.filter_flags:
               if flag not in filter_flags:
                  filter_flags[flag] = [idx]
               else:
                  filter_flags[flag].append(idx)
      else:
         lose.append(idx)


      signs[idx] = diagram.sign()
   #   flows[idx] = diagram.fermion_flow()
   #keep.remove(1)
   #lose.append(1)
   #keep.remove(3)
   #lose.append(3)

   debug("After analyzing tree diagrams: keeping %d, purging %d" % 
         (len(keep), len(lose)))
   return keep, signs #, flows

def analyze_loop_diagrams(diagrams, model, conf, onshell,
      quark_masses = None, complex_masses=None, filter_flags = None, massive_bubbles = {}):
   zero = golem.util.tools.getZeroes(conf)
   lst = setup_list(golem.properties.select_nlo_diagrams, conf)
   fltr = setup_filter(golem.properties.filter_nlo_diagrams, conf, model)
   keep = []
   keep_tot = []
   lose = []
   max_rank = 0

   loopcache     = LoopCache()
   loopcache_tot = LoopCache()
   


   for idx, diagram in diagrams.items():
      if lst:
         if idx not in lst:
            lose.append(idx)
            continue
      if analyze_diagram(diagram, zero, fltr):
         # check for massive quarks first. Even though the
         # diagram might fail the next test it contributes
         # to the renormalization of the gluon wave function.
         if quark_masses is not None:
            for qm in diagram.QuarkBubbleMasses():
               if qm not in quark_masses:
                  quark_masses.append(qm)
         if complex_masses is not None:
            for cqm in diagram.ComplexQuarkBubbleMasses():
               if cqm not in complex_masses:
                  complex_masses.append(cqm)
               if cqm=='0' and complex_masses[len(complex_masses)-1]!='0' and (len(complex_masses) % 2)==1:
                  complex_masses.append(cqm)
         
         cx=False
         for prop in diagram._propagators.items():
             if prop[1].field=='Cx':
                 cx=True
                 
         if not cx:
           if diagram.onshell() > 0:
              lose.append(idx)
           else:
              keep.append(idx)
              keep_tot.append(idx)
              loopcache_tot.add(diagram, idx)

              diagram.isMassiveBubble(idx, massive_bubbles)

              if filter_flags is not None:
                 for flag in diagram.filter_flags:
                    if flag not in filter_flags:
                       filter_flags[flag] = [idx]
                    else:
                       filter_flags[flag].append(idx)
              rk = diagram.rank()
              if rk > max_rank:
                 max_rank = rk
               
        
         #for prop in diagram._propagators.items():
             #if prop[1].field=='Cx':
                 #keep.remove(idx)
                 #keep_tot.remove(idx)
                 #lose.append(idx)
                 #break
        
      else:
         lose.append(idx)

   debug("After analyzing loop diagrams: keeping %d, purging %d" % 
            (len(keep_tot), len(lose)))

#--- new start

   props=[]
   eprops = {}
   for idx in keep:
	props.append([idx,str(diagrams[idx].getLoopIntegral())+','+str(diagrams[idx].rank())])

   if conf.getProperty(golem.properties.sum_diagrams):   
      for i,item in props:
         for j,jtem in props:
            if item == jtem and j>i:
               if j not in lose:
                  lose.append(j)
                  keep.remove(j)
                  if i not in eprops:
                     eprops[i]=[j]
                  else:
                     eprops[i].append(j)
   for idx in keep:
      loopcache.add(diagrams[idx], idx)
      if idx not in eprops.keys():
         eprops[idx]=[idx]
      else:
         eprops[idx].append(idx)
#--- new end

   debug("After analyzing loop diagrams and diagram sum: keeping %d, purging %d" % 
            (len(keep), len(lose)))

   conf["__max_rank__"] = max_rank
   


   return keep, keep_tot, eprops, loopcache, loopcache_tot



def analyze_higher_loop_diagrams(diagrams, model, conf, onshell, loop_order,
      quark_masses = None, complex_masses=None, filter_flags = None, massive_bubbles = {}):
  # TODO: Modify this subroutine according to the needs of nloop. Simply copy of NLO
  # at the moment
  # TODO: This is still the special case for two loop -> generalize to nloop
   zero = golem.util.tools.getZeroes(conf)
   lst = setup_list(golem.properties.select_nnlo_diagrams, conf)
   fltr = setup_filter(golem.properties.filter_nnlo_diagrams, conf, model)
   keep = []
   keep_tot = []
   lose = []
   max_rank = 0
   

   loopcache     = LoopCache()
   loopcache_tot = LoopCache()
   
   for idx, diagram in diagrams.items():
      if lst:
         if idx not in lst:
            lose.append(idx)
            continue
      #keep.append(idx)
      if analyze_higher_loop_diagram(diagram, zero, fltr):
         keep.append(idx)
         keep_tot.append(idx)
         # check for massive quarks first. Even though the
         # diagram might fail the next test it contributes
         # to the renormalization of the gluon wave function.
         #if quark_masses is not None:
            #for qm in diagram.QuarkBubbleMasses():
               #if qm not in quark_masses:
                  #quark_masses.append(qm)
         #if complex_masses is not None:
            #for cqm in diagram.ComplexQuarkBubbleMasses():
               #if cqm not in complex_masses:
                  #complex_masses.append(cqm)
               #if cqm=='0' and complex_masses[len(complex_masses)-1]!='0' and (len(complex_masses) % 2)==1:
                  #complex_masses.append(cqm)

         #if diagram.onshell() > 0:
            ##lose.append(idx)
            #keep.append(idx)
            #keep_tot.append(idx)
         #else:
            #keep.append(idx)
            #keep_tot.append(idx)
#            loopcache_tot.add(diagram, idx)

            ##diagram.isMassiveBubble(idx, massive_bubbles)

            #if filter_flags is not None:
               #for flag in diagram.filter_flags:
                  #if flag not in filter_flags:
                     #filter_flags[flag] = [idx]
                  #else:
                     #filter_flags[flag].append(idx)
            #rk = diagram.rank()
            #if rk > max_rank:
               #max_rank = rk
      else:
         lose.append(idx)
   #keep_tot = keep
   debug("After analyzing %sloop diagrams: keeping %s, purging %s" %
            (loop_order, len(keep_tot), len(lose)))

#--- new start

   props=[]
   eprops = {}
   #for idx in keep:
	#props.append([idx,str(diagrams[idx].getLoopIntegral())+','+str(diagrams[idx].rank())])

   #if conf.getProperty(golem.properties.sum_diagrams):   
      #for i,item in props:
         #for j,jtem in props:
            #if item == jtem and j>i:
               #if j not in lose:
                  #lose.append(j)
                  #keep.remove(j)
                  #if i not in eprops:
                     #eprops[i]=[j]
                  #else:
                     #eprops[i].append(j)
                  
   #for idx in keep:
      #loopcache.add(diagrams[idx], idx)
      #if idx not in eprops.keys():
         #eprops[idx]=[idx]
      #else:
         #eprops[idx].append(idx)
#--- new end

   debug("After analyzing 2loop diagrams and diagram sum: keeping %d, purging %d" % 
            (len(keep), len(lose)))

   #conf["__max_rank__"] = max_rank

   return keep, keep_tot



def analyze_yaml(path, conf, keep_loop, loop_yaml):
   zero = golem.util.tools.getZeroes(conf)
   loop_file = os.path.join(path, "%s.yaml" % loop_yaml)
   outfile_loop = os.path.join(path, loop_yaml+"_out.yaml")
   try:
     with open(outfile_loop,'w') as outfile:
       with open(loop_file,'r') as infile:
         for data in load_all(infile):
           try:
             diag_number = data["diagram"]["name"]
             if diag_number in keep_loop:
               replace_zeroes(data,zero)
               outfile.write(dump(data, width=10000, explicit_start=True))
           except:
             outfile.write(dump(data, width=10000, explicit_start=True))
   except:
      golem.util.tools.warning("Error processing %s file" % loop_file)
   
   outfile.close()   
   os.system('mv '+outfile_loop+' '+loop_file)
   


def analyze_ct_diagrams(diagrams, model, conf, filter_flags = None):
   zero = golem.util.tools.getZeroes(conf)
   lst = setup_list(golem.properties.select_lo_diagrams, conf)
   fltr = setup_filter(golem.properties.filter_lo_diagrams, conf, model)
   keep = []
   lose = []
   signs = {}
   # flows = {}

   for idx, diagram in diagrams.items():

      if lst:
         if idx not in lst:
            lose.append(idx)
            continue

      if diagram.EHCfound():
         conf["ehc"]=True

      if analyze_diagram(diagram, zero, fltr):
         keep.append(idx)

         if filter_flags is not None:
            for flag in diagram.filter_flags:
               if flag not in filter_flags:
                  filter_flags[flag] = [idx]
               else:
                  filter_flags[flag].append(idx)
      else:
         lose.append(idx)

      for prop in diagram._propagators.items():
          if str(prop[1]._mom).find('kx')>=0 and len(str(prop[1]._mom))<=6:
              try:
                keep.remove(idx)
                lose.append(idx)
              except:
                pass


      signs[idx] = diagram.sign()
      
   #keep.remove(1)
   #lose.append(1)
   #keep.remove(2)
   #lose.append(2)
   #keep.remove(3)
   #lose.append(3)
   #keep.remove(4)
   #lose.append(4)
   #keep.remove(5)
   #lose.append(5)
   #keep.remove(8)
   #lose.append(8)   
   #keep.remove(10)
   #lose.append(10)
   #   flows[idx] = diagram.fermion_flow()

   debug("After analyzing ct diagrams: keeping %d, purging %d" % 
         (len(keep), len(lose)))

   return keep, signs #, flows

def analyze_diagram(diagram, zero, fltr):
   if diagram.colorforbidden1loop():
      return False
   diagram.substituteZero(zero)

   if isinstance(fltr, list):
      result = False
      flags = []
      for key, predicate in enumerate(fltr):
         if predicate(diagram):
            flags.append(str(key))
            result = True
      diagram.filter_flags = flags
      return result
   elif isinstance(fltr, dict):
      flags = []
      result = False
      for key, predicate in fltr.items():
         if predicate(diagram):
            flags.append(key)
            result = True
      diagram.filter_flags = flags
      return result
   else:
      if fltr(diagram):
         diagram.filter_flags = [""]
         return True


def analyze_higher_loop_diagram(diagram, zero, fltr):
   diagram.substituteZero(zero)

   if isinstance(fltr, list):
      result = False
      flags = []
      for key, predicate in enumerate(fltr):
         if predicate(diagram):
            flags.append(str(key))
            result = True
      diagram.filter_flags = flags
      return result
   elif isinstance(fltr, dict):
      flags = []
      result = False
      for key, predicate in fltr.items():
         if predicate(diagram):
            flags.append(key)
            result = True
      diagram.filter_flags = flags
      return result
   else:
      if fltr(diagram):
         diagram.filter_flags = [""]
         return True


def replace_zeroes(objects, zeroes):
  
  if type(objects)==type(dict()):
    for key in objects.keys():
       if type(objects[key])==type(dict()) or type(objects[key])==type(list()):
         replace_zeroes(objects[key],zeroes)
       else:
         if objects[key] in zeroes:
	   objects[key]=0
  elif type(objects)==type(list()):
     for index, element in enumerate(objects):
       if type(element)==type(list()) or type(element)==type(dict()):
         replace_zeroes(element,zeroes)
       else:
         if objects[index] in zeroes:
	   objects[index]=0
