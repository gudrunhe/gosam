# vim: ts=3:sw=3:expandtab

import os
import imp
import golem
import golem.util.tools
import golem.installation

class OLPSubprocess:
   def __init__(self, id,
         process_name,
         process_path,
         p_ini, p_fin,
         key):
      self.id = id
      self.process_name = process_name
      self.process_path = process_path
      self.p_ini = p_ini
      self.p_fin = p_fin
      self.crossings = {}
      self.ids = {id: process_name}
      self.channels = {}
      self.key = key

      self.num_legs = len(p_ini) + len(p_fin)
      self.num_helicities = -1
      self.generated_helicities = []

   def addCrossing(self, id, process_name, p_ini, p_fin):
      self.crossings[process_name] = "%s > %s" \
            % (" ".join(map(str,p_ini)), " ".join(map(str,p_fin)))
      self.ids[id] = process_name

   def assignChannels(self, id, channels):
      self.channels[id] = channels

   def assignNumberHelicities(self, nh, gh):
      self.num_helicities = nh
      self.generated_helicities = gh

   def getkey(self):
      return list(self.key)

   def getIDs(self):
      return list(self.ids.keys())

   def __str__(self):
      return self.process_name

   def __int__(self):
      return self.id

   def getPath(self, path=None):
      if path is None:
         return self.process_path
      else:
         return os.path.join(path, self.process_path)

   def getConf(self, conf, path, base=None):

      if base:
         subproc_conf = base.copy(True)
      else:
         subproc_conf = conf.copy(True)

      subproc_conf.cache["model"] = conf.cache["model"]
      subproc_conf[golem.properties.process_name] = self.process_name
      subproc_conf[golem.properties.process_path] = self.getPath(path)
      subproc_conf[golem.properties.qgraf_in] = map(str, self.p_ini)
      subproc_conf[golem.properties.qgraf_out] = map(str, self.p_fin)
      if len(self.crossings) > 0:
         subproc_conf[golem.properties.crossings] = [
            "%s: %s" % (name, process)
            for name, process in self.crossings.items()]

      return subproc_conf


def getSubprocess(olpname, id, inp, out, subprocesses, subprocesses_flav, model, use_crossings):

   def getparticle(name):
      return golem.util.tools.interpret_particle_name(name, model)

   p_ini = map(getparticle, inp)
   p_fin = map(getparticle, out)

   s_ini = map(str,p_ini)
   s_fin = map(str,p_fin)

   if len(olpname) > 0:
      process_name = "%s_p%d_%s_%s" \
            % (olpname, id, "".join(s_ini), "".join(s_fin))
   else:
      process_name = "p%d_%s_%s" \
            % (id, "".join(s_ini), "".join(s_fin))
   process_name = process_name.lower()
   originalkey = tuple(sorted(s_ini + s_fin))

   if use_crossings:
      key = tuple(sorted(s_ini + [p.getPartner() for p in p_fin]))

   else:
      key = tuple(s_ini + [p.getPartner() for p in p_fin])

   if key in subprocesses:
      sp = subprocesses[key]
      sp.addCrossing(id, process_name, p_ini, p_fin)
      is_new = False

   else:
      sp = OLPSubprocess(id, process_name, process_name, p_ini, p_fin, originalkey)
      subprocesses[key] = sp
      is_new = True

   return sp, is_new

def derive_output_name(input_name, pattern, dest_dir=None):
   path, file = os.path.split(input_name)
   if dest_dir is not None:
      path = dest_dir
   path = os.path.join(path, "")
   stem, ext = os.path.splitext(file)

   output_name = pattern
   output_name = output_name.replace("%f", input_name)
   output_name = output_name.replace("%F", file)
   output_name = output_name.replace("%p", path)
   output_name = output_name.replace("%s", stem)
   output_name = output_name.replace("%e", ext)

   return output_name

def derive_coupling_names(model_path, conf):
   """
   Return a triple (qcd_name, qed_name, all_couplings):

   qcd_name      -- the name to be used for the strong coupling constant
   qed_name      -- the name to be used for the weak coupling constant
   all_couplings -- all names that have to be set to one if couplings are 
                    stripped.

   It is recommended that the names QCD, QED, e, gs, gw, EE, EW, GG are used
   in model files, otherwise this routine has difficulties detecting them
   as couplings. These name can also be prefixed by the string 'mdl'
   """
   strong_coupling_names = ["QCD", "GS", "GG", "G"]
   weak_coupling_names   = ["QED", "GW", "E", "EE", "EW"]

   #---#[ Load model file as module:
   mod = golem.util.tools.getModel(conf, model_path)
   #---#] Load model file as module:

   strong_couplings_found = {}
   weak_couplings_found   = {}
   candidates = []

   for param in mod.types.iterkeys():
      if param.startswith('mdl'):
         canonical_name = param[3:].upper()
      else:
         canonical_name = param.upper()
      if canonical_name in strong_coupling_names:
         strong_couplings_found[canonical_name] = param
      elif canonical_name in weak_coupling_names:
         weak_couplings_found[canonical_name] = param
      else:
         candidates.append(canonical_name)

   if len(strong_couplings_found) == 0:
      golem.util.tools.error(
         "Invalid model file: cannot determine name of strong coupling.",
         "Candidates are:" + ",".join(candidates))
   else:
      for name in strong_coupling_names:
         if name in strong_couplings_found:
            qcd_name = strong_couplings_found[name]
            break

   if len(weak_couplings_found) == 0:
      golem.util.tools.error(
         "Invalid model file: cannot determine name of weak coupling.",
         "Candidates are:" + ",".join(candidates))
   else:
      for name in weak_coupling_names:
         if name in weak_couplings_found:
            qed_name = weak_couplings_found[name]
            break

   all_couplings = strong_couplings_found.values() \
         + weak_couplings_found.values()

   return qcd_name, qed_name, all_couplings

def get_qgraf_power(conf):
   """
   Returns two lists:
      list of length three: [coupling_name, born_power, virt_power]
   The list specifies the option 'order'.

   If the list is empty the process is not specified unambiguously.
   """
   alpha_power = conf.getProperty("olp.alphapower", default=None)
   alphas_power = conf.getProperty("olp.alphaspower", default=None)
   correction_type = conf.getProperty("olp.correctiontype", default=None)
   notreelevel = conf.getBooleanProperty("olp.no_tree_level", default=False)

   qcd_name = "QCD"
   qed_name = "QED"

   if alpha_power is None:
      if alphas_power is None:
         # No powers are specified, ambiguous:
         return []
      else:
         # Only alphas_power present:
         try:
            ipower = int(alphas_power)
         except ValueError:
            return []

         if notreelevel:
            treepower = "NONE"
         else:
            treepower = ipower

         if correction_type == "QCD":
            return [qcd_name, treepower, ipower + 2]
         elif correction_type == "EW":
            return [qcd_name, treepower, ipower]
   else:
      if alphas_power is None:
         # Only alpha_power present:
         try:
            ipower = int(alpha_power)
         except ValueError:
            return []

         if notreelevel:
            treepower = "NONE"
         else:
            treepower = ipower

         if correction_type == "QCD":
            return [qed_name, treepower, ipower]
         elif correction_type == "EW":
            return [qed_name, treepower, ipower + 2]
      else:
         try:
            iepower = int(alpha_power)
            icpower = int(alphas_power)
         except ValueError:
            return []

         if correction_type == "QCD":
            if notreelevel:
               treepower = "NONE"
            else:
               treepower = icpower
            return [qcd_name, treepower, icpower + 2]
         elif correction_type == "EW" or correction_type == "QED":
            if notreelevel:
               treepower = "NONE"
            else:
               treepower = iepower
            return [qed_name, treepower, iepower + 2]
   return []

def derive_zero_masses(model_path, slha_file, conf):
   mod_params = golem.util.olp_objects.SUSYLesHouchesFile(slha_file)
   #---#[ Load model file as module:
   mod = golem.util.tools.getModel(conf, model_path)
   #---#] Load model file as module:

   result = []
   for name, part in mod.particles.iteritems():
      mass = part.getMass().strip()
      if mass in mod.slha_locations:
         block, coords = mod.slha_locations[mass]
         params = mod_params[block]
         id = tuple(coords)
         if id in params:
            if params[id] == 0.0:
               result.append(mass)
         else:
            result.append(mass)
   return result

def process_order_file(order_file_name, f_contract, path, default_conf,
      templates = None,
      ignore_case = False,
      ignore_unknown = False,
      from_scratch = False,
      mc_name = "any",
      use_crossings = True,
      **opts
      ):

   def getquarktype(quark):
      # keep only first capital letter
      # trick to transform anti-quarks in quarks
      if list(quark)[0].isupper():
         return list(quark)[0]
      else:
         return quark   
      
   syntax_extensions = [
      "single_quotes",
      "double_quotes",
      "backslash_escape"
   ]

   extensions = {}
   for ex in syntax_extensions:
      if ex in opts:
         extensions[ex] = opts[ex]
      else:
         extensions[ex] = False
      
   golem.util.tools.debug("Processing order file at %r" % order_file_name)
   GOLEM_FULL = "GoSam %s" % ".".join(map(str,
      golem.installation.GOLEM_VERSION))
   result = 0

   conf = golem.util.config.Properties()
   conf += default_conf

   if "olp_process_name" in opts:
      olp_process_name = opts["olp_process_name"].strip().lower()
   else:
      olp_process_name = ""

   conf["olp.process_name"] = olp_process_name

   mc_name_parts = mc_name.split("/", 1)
   conf["olp.mc.name"] = mc_name_parts[0].lower()
   if len(mc_name_parts) > 1:
      conf["olp.mc.version"] = mc_name_parts[1].lower()

   # Set default options # TODO check if correct
   conf["olp.include_color_average"] = False
   conf["olp.include_helicity_average"] = False
   conf["olp.no_tree_level"] = False


   #---#[ Read order file:
   try:
      order_file = golem.util.olp_objects.OLPOrderFile(
            order_file_name, extensions)
   except IOError as err:
      raise golem.util.olp_objects.OLPError("while reading order file: %s"
            % err)

   mc_specials(conf, order_file)

   contract_file = golem.util.olp_objects.OLPContractFile(order_file)

   tmp_contract_file = golem.util.olp_objects.OLPContractFile(order_file)
   subprocesses_conf=[]

   conf.setProperty("setup-file", order_file_name)
   orig_conf=conf.copy()

   file_ok = golem.util.olp_options.process_olp_options(contract_file, conf,
         ignore_case, ignore_unknown)
   if not file_ok:
      golem.util.tools.warning(
            "Please, check configuration files for errors!")

   for lineo,_,_,_ in order_file.processes_ordered():
      subconf=orig_conf.copy()
      file_ok = golem.util.olp_options.process_olp_options(tmp_contract_file, subconf,
         ignore_case, ignore_unknown, lineo)
      subprocesses_conf.append(subconf)

   #---#] Read order file:
   if file_ok:
      if not os.path.exists(path):
         golem.util.tools.message("Creating directory %r" % path)
         os.mkdir(path)

      #---#[ Import model file once for all subprocesses:
      imodel_path = os.path.join(path, "model")
      if not os.path.exists(imodel_path):
         golem.util.tools.message("Creating directory %r" % imodel_path)
         os.mkdir(imodel_path)
      for lconf in [conf] + subprocesses_conf:
         golem.util.tools.prepare_model_files(lconf, imodel_path)

         lconf["modeltype"] = lconf["model"]

         lconf["model"] = os.path.join(imodel_path,
               golem.util.constants.MODEL_LOCAL)
      #---#] Import model file once for all subprocesses:
      #---#[ Constrain masses:
      model_file = conf["olp.modelfile"]
      if model_file is not None:
         zero_masses = derive_zero_masses(imodel_path, model_file, conf)
         zero = golem.util.tools.getZeroes(conf)
         for m in zero_masses:
            if m not in zero:
               zero.append(m)
               golem.util.tools.message("Identified %s==0 (from SLHA file)" % m)
         for lconf in [conf] + subprocesses_conf:
            lconf[golem.properties.zero] = ",".join(zero)
      #---#] Constrain masses:

      model = golem.util.tools.getModel(conf, imodel_path)

      #---#[ Setup excluded and massive particles :
      for lconf in [conf] + subprocesses_conf:
         list_exclude=[]
         for i in [int(p) for p in lconf["__excludeParticles__"].split()] if lconf["__excludeParticles__"] \
               else []:
            for n in model.particles:
               particle=model.particles[n]
               if particle.getPDGCode() == i:
                  list_exclude.append(str(particle))
         if list_exclude:
            if not lconf["qgraf.verbatim"]:
               lconf["qgraf.verbatim"]="true=iprop[%s,0,0];" % (",".join(list_exclude))
            else:
               lconf["qgraf.verbatim"]=lconf["qgraf.verbatim"] + \
                  "\ntrue=iprop[%s,0,0];" % (",".join(list_exclude))

         lconf["__excludeParticles__"]=None

         # TODO: check if massless list is complete
         possible_massless_particles = set( range(1,6) + [11,13])
         set_massiveParticles=set()
         for i in [int(p) for p in lconf["__massiveParticles__"].split()] if lconf["__massiveParticles__"] \
               else []:
            for n in model.particles:
               particle=model.particles[n]
               if particle.getPDGCode() == i:
                  set_massiveParticles.add(particle.getPDGCode())
                  set_massiveParticles.add(-particle.getPDGCode())

         list_zero_values=[];
         for n in model.particles:
               particle=model.particles[n]
               if not particle.getPDGCode() in set_massiveParticles \
                     and abs(particle.getPDGCode()) in possible_massless_particles:
                        mass=particle.getMass()
                        if mass !="0" and mass not in list_zero_values:
                           list_zero_values.append(mass)
                        width=particle.getMass()
                        if width !="0" and width not in list_zero_values:
                           list_zero_values.append(width)

         if list_zero_values:
            if lconf["zero"]:
               lconf["zero"]= lconf["zero"] + "," + ",".join(list_zero_values)
            else:
               lconf["zero"] = ",".join(list_zero_values)

         lconf["__massiveParticles__"]=None

      #---#] Setup excluded and massive particles :


      #---#[ Setup couplings :

      for lconf in [conf] + subprocesses_conf:
         qcd_name, qed_name, all_couplings = derive_coupling_names(imodel_path,
               lconf)
         qgraf_power = get_qgraf_power(lconf)

         if len(qgraf_power) == 0:
            contract_file.setPropertyResponse("CorrectionType",
                  ["Error:", "Wrong or missing entries in",
                     "CorrectionType, AlphaPower or AlphasPower"])
            file_ok = False
         else:
            lconf[golem.properties.qgraf_power] = ",".join(map(str,qgraf_power))

         if "olp.operationmode" in lconf:
            strip_couplings = "CouplingsStrippedOff" in \
                  lconf.getListProperty("olp.operationmode")
         else:
            strip_couplings = False

         if strip_couplings:
            ones = lconf.getListProperty(golem.properties.one)
            for coupling in all_couplings:
               if coupling not in ones:
                  ones.append(coupling)
            lconf[golem.properties.one] = ",".join(ones)
      #---#] Setup couplings :
      #---#[ Select regularisation scheme:
      for lconf in [conf] + subprocesses_conf:
         ir_scheme = lconf["olp.irregularisation"]
         ext = lconf.getListProperty(golem.properties.extensions)
         uext = map(lambda s: s.upper(), ext)
         if ir_scheme == "DRED":
            if "DRED" not in uext:
               ext.append("DRED")
               lconf[golem.properties.extensions] = ",".join(ext)
         if ir_scheme == "CDR":
            if "DRED" not in uext:
               ext.append("DRED")
               lconf[golem.properties.extensions] = ",".join(ext)
         else:
            if "DRED" in uext:
               i = uext.index("DRED")
               golem.util.tools.warning(
                     ("'%s' removed from extensions. " % ext[i]) +
                     "Inconsistent with order file")
               del ext[i]
               lconf[golem.properties.extensions] = ",".join(ext)
      #---#] Select regularisation scheme:
   if "olp.massiveparticlescheme" in conf:
      golem.util.tools.warning("UV-counterterms for massive particles are not "
            + "implemented yet.")

   #---#[ Iterate over subprocesses:
   subdivide = conf.getProperty("olp.subdivide", "no").lower() in ["yes", "true", "1"]
   channels  = {}
   chelis    = {}
   max_occupied_channel = -1
   subprocesses = {}
   subprocesses_flav = {}

   if file_ok:
      for lineno,id, inp, outp in contract_file.processes_ordered():
         subprocess, is_new = getSubprocess(
               olp_process_name, id, inp, outp, subprocesses, subprocesses_flav, model,
               use_crossings)
         if is_new:
            subdir = str(subprocess)
            process_path = os.path.join(path, subdir)
            if not os.path.exists(process_path):
               golem.util.tools.message("Creating directory %r" % process_path)
               try:
                  os.mkdir(process_path)
               except IOError as err:
                  golem.util.tools.error(str(err))

      # Now we run the loop again since all required crossings are added

      # store initial symmetries infos
      start_symmetries = conf["symmetries"]

      for subprocess in subprocesses.values():
         process_path = subprocess.getPath(path)
## -- gio start
         key = subprocess.getkey()
         for lconf in [conf] + subprocesses_conf:
            lconf["symmetries"] = start_symmetries
            if lconf["modeltype"] == 'sm' or lconf["modeltype"] == 'smdiag' or lconf["modeltype"] == 'smehc':
               # check D,Dbar
               if key.count('D')*10+key.count('Dbar') == 1 and 'mD' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %-1=+"
               elif key.count('D')*10+key.count('Dbar') == 10  and 'mD' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %1=-"
               # check U,Ubar
               if key.count('U')*10+key.count('Ubar') == 1  and 'mU' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %-2=+"
               elif key.count('U')*10+key.count('Ubar') == 10  and 'mU' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %2=-"
               # check S,Sbar
               if key.count('S')*10+key.count('Sbar') == 1 and 'mS' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %-3=+"
               elif key.count('S')*10+key.count('Sbar') == 10  and 'mS' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %3=-"
               # check C,Cbar
               if key.count('C')*10+key.count('Cbar') == 1  and 'mC' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %-4=+"
               elif key.count('C')*10+key.count('Cbar') == 10  and 'mC' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %4=-"
               # check B,Bbar
               if key.count('B')*10+key.count('Bbar') == 1 and 'mB' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %-5=+"
               elif key.count('B')*10+key.count('Bbar') == 10  and 'mB' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %5=-"
               # check T,Tbar
               if key.count('T')*10+key.count('Tbar') == 1  and 'mT' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %-6=+"
               elif key.count('T')*10+key.count('Tbar') == 10  and 'mT' in lconf[golem.properties.zero]:
                  lconf["symmetries"] += ", %6=-"
               # neutrinos:
               if key.count('ne') != 0:
                  lconf["symmetries"] += ", %12=-"
               if key.count('nmu') != 0:
                  lconf["symmetries"] += ", %14=-"
               if key.count('ntau') != 0:
                  lconf["symmetries"] += ", %16=-"
               if key.count('nebar') != 0:
                  lconf["symmetries"] += ", %-12=+"
               if key.count('nmubar') != 0:
                  lconf["symmetries"] += ", %-14=+"
               if key.count('ntaubar') != 0:
                  lconf["symmetries"] += ", %-16=+"
## -- gio end

         subprocess_conf = subprocess.getConf(subprocesses_conf[int(subprocess)], path)
         subprocess_conf["golem.name"] = "GoSam"
         subprocess_conf["golem.version"] = ".".join(map(str,
            golem.installation.GOLEM_VERSION))
         subprocess_conf["golem.full-name"] = GOLEM_FULL
         subprocess_conf["golem.revision"] = \
            golem.installation.GOLEM_REVISION

         golem.util.tools.POSTMORTEM_CFG = subprocess_conf

         try:
            golem.util.main_misc.workflow(subprocess_conf)
            golem.util.main_misc.generate_process_files(subprocess_conf,
                  from_scratch)

            helicities = list(
                  golem.util.tools.enumerate_and_reduce_helicities(
                     subprocess_conf))

            generated_helicities = map(lambda t: t[0],
                  filter(lambda t: t[1] is None, helicities))

            for id in subprocess.getIDs():
               chelis[id] = len(helicities)
               if subdivide:
                  num_channels = len(helicities)
                  min_channel = max_occupied_channel + 1
                  max_channel = min_channel + num_channels - 1
                  max_occupied_channel += num_channels
                  channels[id] = range(min_channel, max_channel + 1)
               else:
                  max_occupied_channel += 1
                  channel = max_occupied_channel
                  channels[id] = [ channel ]

               contract_file.setProcessResponse(id, channels[id])
               subprocess.assignChannels(id, channels[id])
               subprocess.assignNumberHelicities(len(helicities),
                     generated_helicities)

         except golem.util.config.GolemConfigError as err:
            result = 1
            for id in subprocess.getIDs():
               contract_file.setProcessError(id, "Error: %s" % err)
   #---#] Iterate over subprocesses:
   #---#[ Write output file:
   f_contract.write("# vim: syntax=olp\n")
   f_contract.write("#@OLP GOLEM %s\n" % ".".join(map(str,
      golem.installation.GOLEM_VERSION)))
   f_contract.write("#@IgnoreUnknown %s\n" % ignore_unknown)
   f_contract.write("#@IgnoreCase %s\n" % ignore_case)
   f_contract.write("#@SyntaxExtensions %s\n" % " ".join(
      filter(lambda i: extensions[i], extensions.keys())))
   try:
      contract_file.store(f_contract)
   except IOError as err:
      raise golem.util.olp_objects.OLPError(
            "while writing contract file: %s" % err)
   #---#] Write output file:
   #---#[ Process global templates:

   if templates is None:
      templates = ""

   if templates == "":
      templates = golem.util.tools.golem_path("olp", "templates")



   golem.properties.setInternals(conf)

   golem.templates.xmltemplates.transform_templates(templates, path, conf.copy(True),
         conf=conf,
         subprocesses=list(subprocesses.values()),
         contract=contract_file,
         user="olp")
   #---#] Process global templates:
   return result

def mc_specials(conf, order_file):
   for pi in order_file.processing_instructions():
      pi_parts = pi.strip().split(" ", 1)
      if len(pi_parts) == 2:
         conf.setProperty(pi_parts[0], pi_parts[1])
      else:
         conf.setProperty(pi_parts[0], True)

   mc_name = conf.getProperty("olp.mc.name").lower().strip()
   mc_version = []
   try:
      s = conf.getProperty("olp.mc.version", default="").strip()
      if len(s) > 0:
         mc_version = map(int, s.split("."))
   except ValueError as ex:
      pass

   required_extensions = []

   if mc_name.startswith("powheg"):
      required_extensions.extend(["f77"])
      required_extensions.extend(["olp_badpts"])
   elif mc_name.startswith("sherpa"):
      required_extensions.extend(["autotools"])
   elif mc_name.startswith("whizard"):
      required_extensions.extend(["autotools"])

   extensions = golem.properties.getExtensions(conf)
   add_extensions = []
   for ext in required_extensions:
      if ext not in extensions:
         add_extensions.append(ext)
   if len(add_extensions) > 0:
      conf.setProperty("%s-auto.extensions" % mc_name,
            ",".join(add_extensions))
