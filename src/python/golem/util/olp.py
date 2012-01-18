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
         p_ini, p_fin):
      self.id = id
      self.process_name = process_name
      self.process_path = process_path
      self.p_ini = p_ini
      self.p_fin = p_fin
      self.crossings = {}
      self.ids = {id: process_name}
      self.channels = {}

      self.num_legs = len(p_ini) + len(p_fin)
      self.num_helicities = -1

   def addCrossing(self, id, process_name, p_ini, p_fin):
      self.crossings[process_name] = "%s > %s" \
            % (" ".join(map(str,p_ini)), " ".join(map(str,p_fin)))
      self.ids[id] = process_name

   def assignChannels(self, id, channels):
      self.channels[id] = channels

   def assignNumberHelicities(self, nh):
      self.num_helicities = nh

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

   def getConf(self, conf, path):

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


def getSubprocess(olpname, id, inp, out, subprocesses, model, use_crossings):

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

   if use_crossings:
      key = tuple(sorted(s_ini + [p.getPartner() for p in p_fin]))
   else:
      key = tuple(s_ini + [p.getPartner() for p in p_fin])

   if key in subprocesses:
      sp = subprocesses[key]
      sp.addCrossing(id, process_name, p_ini, p_fin)
      is_new = False
   else:
      sp = OLPSubprocess(id, process_name, process_name, p_ini, p_fin)
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

   #---#[ Read order file:
   order_file = golem.util.olp_objects.OLPOrderFile(order_file_name, extensions)
   contract_file = golem.util.olp_objects.OLPContractFile(order_file)

   conf.setProperty("setup-file", order_file_name)
   
   file_ok = golem.util.olp_options.process_olp_options(contract_file, conf,
         ignore_case, ignore_unknown)
   if not file_ok:
      golem.util.tools.warning(
            "Please, check configuration files for errors!")
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
      golem.util.tools.prepare_model_files(conf, imodel_path)
      conf["model"] = os.path.join(imodel_path,
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
         conf[golem.properties.zero] = ",".join(zero)
      #---#] Constrain masses:

      model = golem.util.tools.getModel(conf, imodel_path)

      #---#[ Setup couplings :

      qcd_name, qed_name, all_couplings = derive_coupling_names(imodel_path,
            conf)
      qgraf_power = get_qgraf_power(conf)

      if len(qgraf_power) == 0:
         contract_file.setPropertyResponse("CorrectionType",
               ["Error:", "Wrong or missing entries in",
                  "CorrectionType, AlphaPower or AlphasPower"])
         file_ok = False
      else:
         conf[golem.properties.qgraf_power] = ",".join(map(str,qgraf_power))

      if "olp.operationmode" in conf:
         strip_couplings = "CouplingsStrippedOff" in \
               conf.getListProperty("olp.operationmode")
      else:
         strip_couplings = False

      if strip_couplings:
         ones = conf.getListProperty(golem.properties.one)
         for coupling in all_couplings:
            if coupling not in ones:
               ones.append(coupling)
         conf[golem.properties.one] = ",".join(ones)
      #---#] Setup couplings :
      #---#[ Select regularisation scheme:
      ir_scheme = conf["olp.irregularisation"]
      ext = conf.getListProperty(golem.properties.extensions)
      uext = map(lambda s: s.upper(), ext)
      if ir_scheme == "DRED":
         if "DRED" not in uext:
            ext.append("DRED")
            conf[golem.properties.extensions] = ",".join(ext)
      else:
         if "DRED" in uext:
            i = uext.index("DRED")
            golem.util.tools.warning(
                  ("'%s' removed from extensions. " % ext[i]) +
                  "Inconsistent with order file")
            del ext[i]
            conf[golem.properties.extensions] = ",".join(ext)
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

   if file_ok:
      for id, inp, outp in contract_file.processes():
         subprocess, is_new = getSubprocess(
               olp_process_name, id, inp, outp, subprocesses, model,
               use_crossings)
         if is_new:
            subdir = str(subprocess)
            process_path = os.path.join(path, subdir)
            if not os.path.exists(process_path):
               golem.util.tools.message("Creating directory %r" % process_path)
               try:
                  os.mkdir(process_path)
               except IOError as err:
                  error(str(err))

      # Now we run the loop again since all required crossings are added
      for subprocess in subprocesses.values():
         process_path = subprocess.getPath(path)
         subprocess_conf = subprocess.getConf(conf, path)
         subprocess_conf["golem.name"] = "GoSam"
         subprocess_conf["golem.version"] = ".".join(map(str,
            golem.installation.GOLEM_VERSION))
         subprocess_conf["golem.full-name"] = GOLEM_FULL

         #print(">"*80)
         #subprocess_conf.list()
         #print("<"*80)

         try:
            golem.util.main_misc.workflow(subprocess_conf)
            golem.util.main_misc.generate_process_files(subprocess_conf,
                  from_scratch)

            helicities = list(
                  golem.util.tools.enumerate_helicities(subprocess_conf))

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
               subprocess.assignNumberHelicities(len(helicities))

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
   contract_file.store(f_contract)
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
