# vim: ts=3:sw=3:expandtab
import golem
import golem.algorithms.mandelstam
import golem.algorithms.color
import golem.util.tools

from golem.util.config import Properties
import golem.util.parser

from functools import reduce


class KinematicsTemplate(golem.util.parser.Template):
   """
   Implements a template that has knowledge about the
   kinematics of the process, especially, massive and
   light-like vectors and Mandelstam variables.
   """

   def init_kinematics(self, conf, in_particles, out_particles,
         tree_signs, heavy_quarks):
      self._mandel_stack = []
      zeroes = golem.util.tools.getZeroes(conf)
      self._zeroes = zeroes
      self._model = golem.util.tools.getModel(conf)

      props = Properties()
      props["order"] = conf[golem.properties.qgraf_power]

      num_in   = len(in_particles)
      num_out  = len(out_particles)
      num_legs = num_in + num_out

      self._num_in = num_in
      self._num_out = num_out
      self._num_legs = num_legs

      self._heavy_quarks = heavy_quarks

      self._references = golem.algorithms.helicity.reference_vectors(
            conf, in_particles, out_particles)

      self._masses = []
      self._lightlike = []
      self._twospin = []
      self._spin = []
      self._color = []
      self._helicities = []
      self._latex = []
      self._helicity_stack = []
      self._field_info = []
      self._tree_signs = tree_signs
      # self._tree_flows = tree_flows
      self._crossings = []

      for i, crossing in enumerate(
            conf.getProperty(golem.properties.crossings)):
         if ":" in crossing:
            pos = crossing.index(":")
            self._crossings.append(crossing[:pos].strip())

      def examine_particle(p, sign):
         mass    = p.getMass(zeroes)
         twospin = p.getSpin()
         color   = sign * p.getColor()
         latex   = p.getLaTeXName()

         self._masses.append(mass)
         self._latex.append(latex)

         self._lightlike.append(not p.isMassive(zeroes))

         self._twospin.append(twospin)
         if twospin % 2 == 0:
            self._spin.append(str(twospin/2))
         else:
            self._spin.append("%d/2" % twospin)

         self._color.append(color)
         self._helicities.append(p.getHelicityStates(zeroes))
         field_info = (str(p), p.getPartner(), sign)
         self._field_info.append(field_info)

      ################# end examine_particle(p)

      for ini in in_particles:
         examine_particle(ini, +1)

      identical_particles = {}
      for fin in out_particles:
         examine_particle(fin, -1)
         if str(fin) in identical_particles:
            identical_particles[str(fin)] += 1
         else:
            identical_particles[str(fin)] = 1
      symmetry_factor = 1
      for multi in identical_particles.values():
         fact = reduce(lambda x, y: x * y, range(1, multi + 1), 1)
         symmetry_factor *= fact

      props.setProperty("num_in", num_in)
      props.setProperty("num_out", num_out)
      props.setProperty("num_legs", num_legs)
      props.setProperty("num_helicities",
            reduce(lambda x, y: x*y, map(len,self._helicities), 1))
      props.setProperty("in_helicities",
            reduce(lambda x, y: x*y, map(len,self._helicities[:num_in]), 1))
      props.setProperty("symmetry_factor", symmetry_factor)

      # predict the number of colors:
      F = 0
      AF = 0
      G = 0
      for color in self._color:
         if color == -3:
            AF += 1
         elif color == 3:
            F += 1
         elif abs(color) == 8:
            G += 1
         elif abs(color) == 1:
            pass
         else:
            assert False, \
               "Color representation %d is not covered yet." % color
      if F != AF:
         props.setProperty("num_colors", 0)
      else:
         props.setProperty("num_colors",
            golem.algorithms.color.num_colors(F, G))

      self._properties = props
      self._mandel = \
            golem.algorithms.mandelstam.mandelstam_calc(num_in, num_out)
      self._mandel_parts = \
            golem.algorithms.mandelstam.mandelstam_calc(num_in, num_out,
                  prefix="", infix=" ", suffix="")

      helic = {}
      for i in range(num_legs):
         helic[i] = self._helicities[i]

      self._helicity_comb = [h for h in
            golem.util.tools.enumerate_helicities(conf)]

   def crossed_color(self, *args, **opts):
      cri = [prop.getIntegerProperty("$_") for prop in self.crossing()]
      crs = [int(prop.getProperty("sign") + "1") for prop in self.crossing()]

      ini_indices = range(self._num_in)
      fin_indices = range(self._num_in, self._num_in + self._num_out)

      use_indices = ini_indices + fin_indices
      sel_indices = []

      if "initial" in args:
         use_indices = sel_indices
         sel_indices.extend(ini_indices)
      if "final" in args:
         use_indices = sel_indices
         sel_indices.extend(fin_indices)

      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)
      index_name = self._setup_name("index", "index", opts)
      var_name = self._setup_name("var", "$_", opts)

      color = [self._color[i-1] for i in cri]

      last = len(use_indices) - 1
      props =  Properties()
      for count, idx in enumerate(use_indices):
         is_first = count == 0
         is_last = count == last

         props.setProperty(first_name, str(is_first))
         props.setProperty(last_name, str(is_last))
         props.setProperty(index_name, str(idx))
         props.setProperty(var_name, str(color[idx]))
         yield props
         
   def crossed_helicities(self, *args, **opts):
      cri = [prop.getIntegerProperty("$_") for prop in self.crossing()]
      crs = [int(prop.getProperty("sign") + "1") for prop in self.crossing()]

      ini_indices = range(self._num_in)
      fin_indices = range(self._num_in, self._num_in + self._num_out)

      use_indices = ini_indices + fin_indices
      sel_indices = []

      if "initial" in args:
         use_indices = sel_indices
         sel_indices.extend(ini_indices)
      if "final" in args:
         use_indices = sel_indices
         sel_indices.extend(fin_indices)

      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)
      index_name = self._setup_name("index", "index", opts)
      var_name = self._setup_name("var", "$_", opts)

      num_helis = [len(self._helicities[i-1]) for i in cri]

      last = len(use_indices) - 1
      props =  Properties()
      for count, idx in enumerate(use_indices):
         is_first = count == 0
         is_last = count == last

         props.setProperty(first_name, str(is_first))
         props.setProperty(last_name, str(is_last))
         props.setProperty(index_name, str(idx))
         props.setProperty(var_name, str(num_helis[idx]))
         yield props
         
   def crossed_symmetry_factor(self, *args, **opts):
      cri = [prop.getIntegerProperty("$_") for prop in self.crossing()]
      crs = [int(prop.getProperty("sign") + "1") for prop in self.crossing()]
      fields = self._field_info

      fin =  range(self._num_in, self._num_in + self._num_out)
      fin_indices = [cri[i] for i in fin]
      fin_signs = [crs[i] for i in fin]

      particles = {}
      for idx, sign in zip(fin_indices, fin_signs):
         field, anti, f_sign = fields[idx-1]
         if sign == -1:
            prtcl = anti
         else:
            prtcl = field

         if prtcl in particles:
            particles[prtcl] += 1
         else:
            particles[prtcl] = 1

      symmetry_factor = 1
      for multi in particles.values():
         fact = reduce(lambda x, y: x * y, range(1, multi + 1), 1)
         symmetry_factor *= fact

      return str(symmetry_factor)

   def __call__(self, *conf):
      for chunk in golem.util.parser.Template \
            .__call__(self, self._properties, *conf):
         yield chunk

   def quark_loop_masses(self, *args, **opts):
      quark_masses = self._heavy_quarks
      N = len(list(quark_masses))

      if "prefix" in opts:
         prefix = opts["prefix"]
      else:
         prefix = ""
      var_name = self._setup_name("var", prefix + "$_", opts)
      first_name = self._setup_name("first", prefix + "is_first", opts)
      last_name = self._setup_name("last", prefix + "is_last", opts)

      props = Properties()
      for i, mass in enumerate(quark_masses):
         props[var_name] = mass
         props[first_name] = i == 0
         props[last_name] = i == N - 1

         yield props

   def tree_sign(self, *args, **opts):
      if len(args) == 0:
         raise golem.util.parser.TemplateError(
               "[% tree_sign %] without diagram number.")

      diag = self._eval_int(args[0])

      if diag in self._tree_signs:
         return str(self._tree_signs[diag])
      else:
         raise golem.util.parser.TemplateError(
               "[% tree_sign %] with unknown diagram number.")

   def _OBSOLETE_tree_flow(self, *args, **opts):
      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)
      index_name = self._setup_name("index", "index", opts)
      var_name = self._setup_name("var", "$_", opts)
      props =  Properties()

      if len(args) == 0:
         raise golem.util.parser.TemplateError(
               "[% tree_flow %] without diagram number.")

      diag = self._eval_int(args[0])

      if diag not in self._tree_flows:
         raise golem.util.parser.TemplateError(
               "[% tree_sign %] with unknown diagram number.")

      flow = self._tree_flows[diag]
      N = len(flow)

      for i, l in enumerate(flow.keys()):
         is_first = i == 0
         is_last = i == N - 1
         value = flow[l]

         props.setProperty(first_name, str(is_first))
         props.setProperty(last_name, str(is_last))
         props.setProperty(index_name, str(l))
         props.setProperty(var_name, str(value))
         yield props

   def crossings(self, *args, **opts):
      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)
      index_name = self._setup_name("index", "index", opts)
      var_name = self._setup_name("var", "$_", opts)

      l = len(self._crossings)

      props = golem.util.config.Properties()
      for i, name in enumerate(self._crossings):
         props.setProperty(first_name, i == 0)
         props.setProperty(last_name, i >= l - 1)
         props.setProperty(index_name, i)
         props.setProperty(var_name, name)
         yield props

   def crossing(self, *args, **opts):
      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)
      index_name = self._setup_name("index", "index", opts)
      var_name = self._setup_name("var", "$_", opts)
      sign_name = self._setup_name("sign", "sign", opts)

      initial = map(
         lambda n:
            str(golem.util.tools.interpret_particle_name(n, self._model)),
            self.initial().split(","))
      final = map(
         lambda n:
            str(golem.util.tools.interpret_particle_name(n, self._model)),
            self.final().split(","))
      field_info = self._field_info

      avail = set(range(1, len(field_info)+1))
      mapping = {}

      for i, field in enumerate(initial):
         found = 0
         for j in avail:
            f, a, s = field_info[j-1]
            if s == 1 and field == f:
               found = j
               break
            elif s == -1 and field == a:
               found = -j
               break
         if found != 0:
            mapping[i+1] = found
            avail.remove(abs(found))
         else:
            raise golem.util.parser.TemplateError(
                  "No valid crossing found (%d)." % (i+1))

      l = len(initial)
      for k, field in enumerate(final):
         found = 0
         for j in avail:
            f, a, s = field_info[j-1]
            if s == -1 and field == f:
               found = j
               break
            elif s == 1 and field == a:
               found = -j
               break
         if found != 0:
            mapping[k+l+1] = found
            avail.remove(abs(found))
         else:
            raise golem.util.parser.TemplateError(
                  "No valid crossing found (%d)." % (k+i+1))

      props = golem.util.config.Properties()

      l = len(mapping)
      i = 0
      for new_vec, old_vec in mapping.items():
         props.setProperty(first_name, i == 0)
         props.setProperty(last_name, i >= l - 1)
         i += 1

         if old_vec < 0:
            sign = "-"
         else:
            sign = "+"

         props.setProperty(index_name, new_vec)
         props.setProperty(var_name, abs(old_vec))
         props.setProperty(sign_name, sign)
         yield props

   def loqcd(self, *args, **opts):
      """
      Deduct the number of QCD couplings at LO

      args -- optional list of names that refer to QCD couplings
      """
      if args:
         names = [s.lower() for s in args]
      else:
         names = ["qcd", "gg", "gs"]

      order = [s.strip().lower() for s in
            self._properties.getProperty("order").split(",")]
      if order[0] in names:
         # coupling is qcd
         if order[1] == "none":
            # we just assume the LO QCD order is NLO - 2
            return str(int(order[2]) - 2)
         else:
            return str(int(order[1]))
      else:
         # coupling is ew
         # over all number of tree level couplings (qcd+qed)
         lo_couplings = self._num_legs - 2
         if order[1] == "none":
            # we just assume the LO EW order is NLO - 2
            return str(lo_couplings - (int(order[2]) - 2))
         else:
            return str(lo_couplings - int(order[1]))

   def isqcd(self, *args, **opts):
      """
      Deduct the correction type 

      args -- optional list of names that refer to QCD couplings
      """
      if args:
         names = [s.lower() for s in args]
      else:
         names = ["qcd", "gg", "gs"]

      order = [s.strip().lower() for s in
            self._properties.getProperty("order").split(",")]
      if len(order) < 3:
         return False

      if order[0] in names:
         # coupling is qcd
         if order[1] == "none":
            return True
         else:
            return int(order[1]) < int(order[2])
      else:
         # coupling is ew
         if order[1] == "none":
            return False 
         else:
            return int(order[1]) >= int(order[2])

   def particles(self, *args, **opts):
      inout_filter = self._setup_filter(["initial", "final"], args)
      mass_filter  = self._setup_filter(["massive", "lightlike"], args)

      if "prefix" in opts:
         prefix = opts["prefix"]
      else:
         prefix = ""
      index_name = self._setup_name("index", prefix + "index", opts)
      out_index_name = self._setup_name("out_index", prefix + "out_index", opts)
      helicity_name = self._setup_name("hel", prefix + "hel", opts)
      mass_name = self._setup_name("mass", prefix + "mass", opts)
      spin_name = self._setup_name("spin", prefix + "spin", opts)
      twospin_name = self._setup_name("2spin", prefix + "2spin", opts)
      lightlike_name = self._setup_name("lightlike", prefix + "is_lightlike", 
            opts)
      massive_name = self._setup_name("massive", prefix + "is_massive", opts)
      ini_name = self._setup_name("initial", prefix + "is_inital", opts)
      fin_name = self._setup_name("final", prefix + "is_final", opts)
      color_name = self._setup_name("color", prefix + "color", opts)
      latex_name = self._setup_name("latex", prefix + "latex", opts)
      reference_name = self._setup_name("reference", prefix + "reference", opts)

      first_name = self._setup_name("first", prefix + "is_first", opts)

      is_first = True
      base = 1

      color_filter = []
      spin_filter = []

      if "white" in args:
         color_filter.extend([1, -1])
      if "colored" in args:
         color_filter.extend([3, -3, 8, -8])
      if "fundamental" in args:
            color_filter.extend([-3, 3])
      if "quarks" in args:
            color_filter.append(3)
      if "anti-quarks" in args:
            color_filter.append(-3)
      if ("adjoint" in args) or ("gluons" in args):
            color_filter.extend([-8, 8])

      if len(color_filter) == 0:
         color_filter = [1, -1, 3, -3, 8, -8]

      if "scalar" in args:
         spin_filter.append(0)
      if "spinor" in args:
         spin_filter.extend([-1, 1])
      if "vector" in args:
         spin_filter.extend([-2, 2])
      if "vectorspinor" in args:
         spin_filter.extend([-3, 3])
      if "tensor" in args:
         spin_filter.extend([-4, 4])

      if "boson" in args:
         spin_filter.extend([-4,-2,0,2,4])
      if "fermion" in args:
         spin_filter.extend([-3,-1,3,1])

      if len(spin_filter) == 0:
         spin_filter = [-4,-3,-2,-1,0,1,2,3,4]


      props = Properties()

      if "initial" in inout_filter:
         start_index = 0
      else:
         start_index = self._num_in

      if "final" in inout_filter:
         end_index = self._num_legs
      else:
         end_index = self._num_in

      for index in range(start_index, end_index):
         if self._lightlike[index]:
            if "lightlike" not in mass_filter:
               continue
         else:
            if "massive" not in mass_filter:
               continue

         color = self._color[index]
         if color not in color_filter:
            continue

         tspin = self._twospin[index]
         if tspin not in spin_filter:
            continue

         props.setProperty(first_name, is_first)
         is_first = False
         props.setProperty(index_name, index + base)
         props.setProperty(mass_name, self._masses[index])
         props.setProperty(spin_name, self._spin[index])
         props.setProperty(twospin_name, self._twospin[index])
         props.setProperty(latex_name, self._latex[index])
         props.setProperty(lightlike_name, self._lightlike[index])
         props.setProperty(massive_name, not self._lightlike[index])
         props.setProperty(ini_name, index < self._num_in)
         if index >= self._num_in:
            props.setProperty(out_index_name, index + base - self._num_in)
         else:
            props.setProperty(out_index_name,
               "[%% ' ERROR: initial state particle, %s not defined. ' %%]"
               % out_index_name)

         if len(self._helicity_stack) > 0:
            if index in self._helicity_stack[-1]:
               props.setProperty(helicity_name,
                     self._helicity_stack[-1][index])
            else:
               props.setProperty(helicity_name,
                  "[%% ' ERROR: %s not defined for this particle. ' %%]"
                  % helicity_name)

         if index in self._references:
            refk = self._references[index]
            if refk.startswith("k"):
               props.setProperty(reference_name, int(refk[1:]))
            else:
               assert refk.startswith("l")
               props.setProperty(reference_name, -int(refk[1:]))
         else:
            props.setProperty(reference_name, 0)

         props.setProperty(fin_name, index >= self._num_in)
         props.setProperty(color_name, color)
         yield props

   def pairs(self, *args, **opts):
      if "prefix" in opts:
         prefix = opts["prefix"]
      else:
         prefix = ""

      inout1_filter = self._setup_filter(["initial1", "final1"], args)
      inout2_filter = self._setup_filter(["initial2", "final2"], args)
      mass1_filter  = self._setup_filter(["massive1", "lightlike1"], args)
      mass2_filter  = self._setup_filter(["massive2", "lightlike2"], args)

      index1_name = self._setup_name("index1", prefix + "index1", opts)
      mass1_name = self._setup_name("mass1", prefix + "mass1", opts)
      spin1_name = self._setup_name("spin1", prefix + "spin1", opts)
      twospin1_name = self._setup_name("2spin1", prefix + "2spin1", opts)
      lightlike1_name = self._setup_name("lightlike1",
            prefix + "is_lightlike1", opts)
      massive1_name = self._setup_name("massive1", prefix + "is_massive1", opts)
      ini1_name = self._setup_name("initial1", prefix + "is_inital1", opts)
      fin1_name = self._setup_name("final1", prefix + "is_final1", opts)
      color1_name = self._setup_name("color1", prefix + "color1", opts)
      latex1_name = self._setup_name("latex1", prefix + "latex1", opts)

      index2_name = self._setup_name("index2", prefix + "index2", opts)
      mass2_name = self._setup_name("mass2", prefix + "mass2", opts)
      spin2_name = self._setup_name("spin2", prefix + "spin2", opts)
      twospin2_name = self._setup_name("2spin2", prefix + "2spin2", opts)
      lightlike2_name = self._setup_name("lightlike2",
            prefix + "is_lightlike2", opts)
      massive2_name = self._setup_name("massive2", prefix + "is_massive2", opts)
      ini2_name = self._setup_name("initial2", prefix + "is_inital2", opts)
      fin2_name = self._setup_name("final2", prefix + "is_final2", opts)
      color2_name = self._setup_name("color2", prefix + "color2", opts)
      out_index1_name = self._setup_name("out_index1",
            prefix + "out_index1", opts)
      out_index2_name = self._setup_name("out_index2",
            prefix + "out_index2", opts)
      helicity1_name = self._setup_name("hel1", prefix + "hel1", opts)
      helicity2_name = self._setup_name("hel2", prefix + "hel2", opts)
      reference1_name = self._setup_name("reference1",
            prefix + "reference1", opts)
      reference2_name = self._setup_name("reference2",
            prefix + "reference2", opts)
      latex2_name = self._setup_name("latex2",
            prefix + "latex2", opts)

      first_name = self._setup_name("first", prefix + "is_first", opts)
      is_first = True
      base = 1

      color1_filter = []
      if "white1" in args:
         color1_filter.extend([1, -1])
      if "colored1" in args:
         color1_filter.extend([3, -3, 8, -8])
      if "fundamental1" in args:
            color1_filter.extend([-3, 3])
      if "quarks1" in args:
            color1_filter.append(3)
      if "anti-quarks1" in args:
            color1_filter.append(-3)
      if ("adjoint1" in args) or ("gluons1" in args):
            color1_filter.extend([-8, 8])

      if len(color1_filter) == 0:
         color1_filter = [1, -1, 3, -3, 8, -8]

      color2_filter = []
      if "white2" in args:
         color2_filter.extend([1, -1])
      if "colored2" in args:
         color2_filter.extend([3, -3, 8, -8])
      if "fundamental2" in args:
            color2_filter.extend([-3, 3])
      if "quarks2" in args:
            color2_filter.append(3)
      if "anti-quarks2" in args:
            color2_filter.append(-3)
      if ("adjoint2" in args) or ("gluons2" in args):
            color2_filter.extend([-8, 8])

      if len(color2_filter) == 0:
         color2_filter = [1, -1, 3, -3, 8, -8]

      props = Properties()

      if "initial1" in inout1_filter:
         start1_index = 0
      else:
         start1_index = self._num_in

      if "final1" in inout1_filter:
         end1_index = self._num_legs
      else:
         end1_index = self._num_in

      if "initial2" in inout2_filter:
         start2_index = 0
      else:
         start2_index = self._num_in

      if "final2" in inout2_filter:
         end2_index = self._num_legs
      else:
         end2_index = self._num_in

      for index1 in range(start1_index, end1_index):
         if self._lightlike[index1]:
            if "lightlike1" not in mass1_filter:
               continue
         else:
            if "massive1" not in mass1_filter:
               continue

         color1 = self._color[index1]
         if color1 not in color1_filter:
            continue

         props.setProperty(index1_name, index1 + base)
         props.setProperty(mass1_name, self._masses[index1])
         props.setProperty(spin1_name, self._spin[index1])
         props.setProperty(twospin1_name, self._twospin[index1])
         props.setProperty(lightlike1_name, self._lightlike[index1])
         props.setProperty(massive1_name, not self._lightlike[index1])
         props.setProperty(ini1_name, index1 < self._num_in)
         props.setProperty(fin1_name, index1 >= self._num_in)
         props.setProperty(color1_name, color1)
         props.setProperty(latex1_name, self._latex[index1])
         if index1 >= self._num_in:
            props.setProperty(out_index1_name, index1 + base - self._num_in)
         else:
            props.setProperty(out_index1_name,
               "[%% ' ERROR: initial state particle, %s not defined. ' %%]"
               % out_index1_name)
         
         if len(self._helicity_stack) > 0:
            if index1 in self._helicity_stack[-1]:
               props.setProperty(helicity1_name,
                     self._helicity_stack[-1][index1])
            else:
               props.setProperty(helicity1_name,
                  "[%% ' ERROR: %s not defined for this particle. ' %%]"
                  % helicity1_name)

         if index1 in self._references:
            refk = self._references[index1]
            if refk.startswith("k"):
               props.setProperty(reference1_name, int(refk[1:]))
            else:
               assert refk.startswith("l")
               props.setProperty(reference1_name, -int(refk[1:]))
         else:
            props.setProperty(reference1_name, 0)
         start2 = start2_index
         if "ordered" in args:
            if start2 < index1:
               start2 = index1

         for index2 in range(start2, end2_index):
            if (index2 == index1) and ("distinct" in args):
               continue

            if self._lightlike[index2]:
               if "lightlike2" not in mass2_filter:
                  continue
            else:
               if "massive2" not in mass2_filter:
                  continue

            color2 = self._color[index2]
            if color2 not in color2_filter:
               continue

            if index2 >= self._num_in:
               props.setProperty(out_index2_name,
                  index2 + base - self._num_in)
            else:
               props.setProperty(out_index2_name,
                  "[%% ' ERROR: initial state particle, %s not defined. ' %%]"
                  % out_index2_name)
            if len(self._helicity_stack) > 0:
               if index2 in self._helicity_stack[-1]:
                  props.setProperty(helicity2_name,
                        self._helicity_stack[-1][index2])
               else:
                  props.setProperty(helicity2_name,
                     "[%% ' ERROR: %s not defined for this particle. ' %%]"
                     % helicity2_name)
            if index2 in self._references:
               refk = self._references[index2]
               if refk.startswith("k"):
                  props.setProperty(reference2_name, int(refk[1:]))
               else:
                  assert refk.startswith("l")
                  props.setProperty(reference2_name, -int(refk[1:]))
            else:
               props.setProperty(reference2_name, 0)

            props.setProperty(index2_name, index2 + base)
            props.setProperty(mass2_name, self._masses[index2])
            props.setProperty(spin2_name, self._spin[index2])
            props.setProperty(twospin2_name, self._twospin[index2])
            props.setProperty(lightlike2_name, self._lightlike[index2])
            props.setProperty(massive2_name, not self._lightlike[index2])
            props.setProperty(ini2_name, index2 < self._num_in)
            props.setProperty(fin2_name, index2 >= self._num_in)
            props.setProperty(color2_name, color2)
            props.setProperty(first_name, is_first)
            props.setProperty(latex2_name, self._latex[index2])
            is_first = False
            yield props

   def mandelstam(self, *args, **opts):
      zero_filter = self._setup_filter(["zero", "non-zero"], args)
      zero_name = self._setup_name("zero", "is_zero", opts)
      nzero_name = self._setup_name("non-zero", "is_non-zero", opts)
      symbol_name = \
         self._setup_name("symbol", "symbol", opts)
      first_name = self._setup_name("first", "is_first", opts)
      index_name = self._setup_name("index", "index", opts)
      gindex_name = self._setup_name("global_index", "global_index", opts)

      sym_prefix = self._setup_name("sym_prefix", "es", opts)
      sym_suffix = self._setup_name("sym_suffix", "", opts)
      sym_infix  = self._setup_name("sym_infix", "", opts)

      props = Properties()
      is_first = True

      idx = 0
      gidx = 0
      for parts, vecs in self._mandel_parts.items():
         gidx += 1
         default_name = "s" + "".join(parts.split())
         name = sym_prefix + sym_infix.join(parts.split()) + sym_suffix

         is_massive = True
         if len(vecs) == 1:
            mass = self._masses[vecs[0] - 1]
            is_massive = (mass != "0")

         if is_massive:
            if "non-zero" not in zero_filter:
               continue
         else:
            if "zero" not in zero_filter:
               continue

         idx += 1

         props.setProperty(symbol_name, name)
         props.setProperty(zero_name, not is_massive)
         props.setProperty(nzero_name, is_massive)
         props.setProperty(first_name, is_first)
         props.setProperty(index_name, idx)
         props.setProperty(gindex_name, gidx)

         is_first = False
         self._mandel_stack.append(default_name)
         yield props
         self._mandel_stack.pop()

   def mandelstam_expression(self, *args, **opts):
      index1_name = self._setup_name("index1", "index1", opts)
      mass1_name = self._setup_name("mass1", "mass1", opts)
      spin1_name = self._setup_name("spin1", "spin1", opts)
      twospin1_name = self._setup_name("2spin1", "2spin1", opts)
      lightlike1_name = self._setup_name("lightlike1", "is_lightlike1", opts)
      massive1_name = self._setup_name("massive1", "is_massive1", opts)
      ini1_name = self._setup_name("initial1", "is_inital1", opts)
      fin1_name = self._setup_name("final1", "is_final1", opts)
      color1_name = self._setup_name("color1", "color1", opts)

      index2_name = self._setup_name("index2", "index2", opts)
      mass2_name = self._setup_name("mass2", "mass2", opts)
      spin2_name = self._setup_name("spin2", "spin2", opts)
      twospin2_name = self._setup_name("2spin2", "2spin2", opts)
      lightlike2_name = self._setup_name("lightlike2", "is_lightlike2", opts)
      massive2_name = self._setup_name("massive2", "is_massive2", opts)
      ini2_name = self._setup_name("initial2", "is_inital2", opts)
      fin2_name = self._setup_name("final2", "is_final2", opts)
      color2_name = self._setup_name("color2", "color2", opts)

      symbol = self._mandel_stack[-1]
      vecs = self._mandel[symbol]
      
      is_first_term = True
      count_terms = (len(vecs) * (len(vecs) + 1)) / 2
      props = Properties()
      for i in range(len(vecs)):
         # i == j term
         vec1 = abs(vecs[i]) - 1
         mass1 = self._masses[vec1]
         color1 = self._color[vec1]
         count_terms -= 1
         props.setProperty(index1_name, vec1 + 1)
         props.setProperty(index2_name, vec1 + 1)
         props.setProperty(massive1_name, not self._lightlike[vec1])
         props.setProperty(massive2_name, not self._lightlike[vec1])
         props.setProperty(lightlike1_name, self._lightlike[vec1])
         props.setProperty(lightlike2_name, self._lightlike[vec1])
         props.setProperty(mass1_name, mass1)
         props.setProperty(mass2_name, mass1)
         props.setProperty(spin1_name, self._spin[vec1])
         props.setProperty(spin2_name, self._spin[vec1])
         props.setProperty(twospin1_name, self._twospin[vec1])
         props.setProperty(twospin2_name, self._twospin[vec1])
         props.setProperty(ini1_name, vec1 < self._num_in)
         props.setProperty(ini2_name, vec1 < self._num_in)
         props.setProperty(fin1_name, vec1 >= self._num_in)
         props.setProperty(fin2_name, vec1 >= self._num_in)
         props.setProperty(color1_name, color1)
         props.setProperty(color2_name, color1)

         if mass1 != "0":
            props.setProperty("term_mass", mass1)
            props.setProperty("term_coeff", "1")
            props.setProperty("term_is_mass", True)
            props.setProperty("is_first_term", is_first_term)
            props.setProperty("is_last_term", count_terms == 0)
            yield props
            is_first_term = False

         props.setProperty("term_is_mass", False)
         props.setProperty("term_mass",
               "[% ERROR: 'term_mass' not defined here. %]")
         props.setProperty("term_coeff", "2")

         for j in range(i+1, len(vecs)):
            count_terms -= 1
            vec2 = abs(vecs[j]) - 1
            mass2 = self._masses[vec2]
            color2 = self._color[vec2]

            props.setProperty(index2_name, vec2 + 1)
            props.setProperty(massive2_name, not self._lightlike[vec2])
            props.setProperty(lightlike2_name, self._lightlike[vec2])
            props.setProperty(mass2_name, mass2)
            props.setProperty(spin2_name, self._spin[vec2])
            props.setProperty(twospin2_name, self._twospin[vec2])
            props.setProperty(ini2_name, vec2 < self._num_in)
            props.setProperty(fin2_name, vec2 >= self._num_in)
            props.setProperty(color2_name, color2)
            props.setProperty("is_first_term", is_first_term)
            props.setProperty("is_last_term", count_terms == 0)
            yield props
            is_first_term = False

   def latex_color_base(self, *args, **opts):
      """
      Enumerates all color structures for this process in
      LaTeX format.
      """

      var_name = self._setup_name("var", "$_", opts)
      rhs_name = self._setup_name("expr", "expr", opts)

      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)

      # This is basically what has been golem.main_color.latex_color before.
      result = ""
      quarks = []
      aquarks = []
      gluons = []
      particles = []
      colored = []
      wf = []
      for i in range(len(self._color)):
         c = self._color[i]
         if c == 3:
            color_index = "i_%d" % (i+1)
            quarks.append(color_index)
            colored.append(i+1)
            wf.append("q^{(%d)}_{%s}" % (i+1, color_index))
         elif c == -3:
            color_index = "j_%d" % (i+1)
            aquarks.append(color_index)
            colored.append(i+1)
            wf.append("\\bar{q}^{(%d)}_{%s}" % (i+1, color_index))
         elif c == 8 or c == -8:
            color_index = "A_%d" % (i+1)
            gluons.append(color_index)
            colored.append(i+1)
            wf.append("g_{(%d)}^{%s}" % (i+1, color_index))
         else:
            continue
         particles.append(color_index)

      total_colors = int(self._properties["num_colors"])

      num_color = 0
      for lines, traces in golem.algorithms.color.colorbasis(
            quarks, aquarks, gluons):
         num_color += 1

         s_lines = wf[:]
         for line in lines:
            N = len(line)
            if N == 2:
               s_lines.append("\\delta_{%s%s}" % (line[0], line[1]))
            else:
               string = []
               for aidx in line[1:N-2]:
                  string.append("T^{%s}" % (aidx))
               string.append("T^{%s}" % (line[N-2]))
               s_lines.append("(%s)_{%s%s}" % (
                  "".join(string), line[0], line[N-1]))
            
         for tr in traces:
            N = len(tr)
            string = []
            for aidx in tr[1:N]:
               string.append("T^{%s}" % aidx)
            string.append("T^{%s}" % tr[0])
            s_lines.append("\\mathrm{tr}\\{%s\\}" % "".join(string))

         props = golem.util.config.Properties()
         props.setProperty(var_name, num_color)
         props.setProperty(rhs_name,
               "".join(s_lines) if len(s_lines) > 0 else "1")

         props.setProperty(first_name, num_color == 1)
         props.setProperty(last_name, num_color == total_colors)

         yield props

   def helicities(self, *args, **opts):
      """
      Enumerates all helicities possible with this
      kinematics.

      opts:
         symbol_plus=+    symbol used for helicity +1
         symbol_minus=-   symbol used for helicity -1
         symbol_zero=0    symbol used for helicity  0
         symbol_plus2=p   symbol used for helicity +2 (not yet in use)
         symbol_minus2=m  symbol used for helicity -2 (not yet in use)
         base=0           where to count from
         var=helicity     name for the index of the current helicity
         where=variable<op>value
                          variable is the name of a variable giving the
                          index of a particle. <op> is one of
                          .eq. .ne. .gt. .lt. .ge. .le.
                          value is one of the above symbols. example
                          where=index1.ge.0
                          where=index.ne.0
                          more than one value can be given separated by
                          commas, which then are combined via 'and'

      Depending on the spin of the particle the symbols have different
      meanings:

      spin massive  |  'm'  '-'  '0'   '+'   'p'
        0   YES/NO  | ---- ----    0  ----  ----
      1/2   YES/NO  | ---- -1/2 ----  +1/2  ----
        1     NO    | ----   -1 ----    +1  ----
        1    YES    | ----   -1    0    +1  ----
      3/2     NO    | -3/2 ---- ----  ----  +3/2
      3/2    YES    | -3/2 -1/2 ----  +1/2  +3/2
        2     NO    |   -2 ---- ----  ----    +2
        2    YES    |   -2   -1    0    +1    +2
      """
      sym = golem.algorithms.helicity.heli_to_symbol
      symbol_plus   = self._setup_name("symbol_plus",   sym[+1], opts)
      symbol_minus  = self._setup_name("symbol_minus",  sym[-1], opts)
      symbol_plus2  = self._setup_name("symbol_plus2",  sym[+2], opts)
      symbol_minus2 = self._setup_name("symbol_minus2", sym[-2], opts)
      symbol_zero   = self._setup_name("symbol_zero",   sym[ 0], opts)
      base = int(self._setup_name("base", "0", opts))
      prefix   = self._setup_name("prefix",   "", opts)
      var_name = self._setup_name("var", prefix + "helicity", opts)
      first_name = self._setup_name("first", prefix + "is_first", opts)
      last_name = self._setup_name("last", prefix + "is_last", opts)

      symbols = {
               -2: symbol_minus2,
               -1: symbol_minus,
                0: symbol_zero,
               +1: symbol_plus,
               +2: symbol_plus2
            }

      isymbols = {}
      for s,v in symbols.items():
         isymbols[v] = s

      isymbols.setdefault(100)

      pfilter = {}

      if "where" in opts:
         and_list = opts["where"].split(",")
         for s_expr in and_list:
            tokens = s_expr.split(".")

            where_name = tokens[0]
            where_index = self._eval_int(where_name)-1
            where_op = tokens[1]
            where_val = isymbols[tokens[2]]
            if where_op == "eq":
               pfilter[where_index] = [where_val]
            elif where_op == "ne":
               pfilter[where_index] = list(range(-100,where_val)) + \
                     list(range(where_val+1,100))
            elif where_op == "le":
               pfilter[where_index] = list(range(-100,where_val+1))
            elif where_op == "ge":
               pfilter[where_index] = list(range(where_val,100))
            elif where_op == "lt":
               pfilter[where_index] = list(range(-100,where_val))
            elif where_op == "gt":
               pfilter[where_index] = list(range(where_val+1,100))
            else:
               pfilter[where_index] = []

      props = Properties()
      i = base
      l = len(self._helicity_comb)
      for h in self._helicity_comb:
         h = golem.util.tools.encode_helicity(h, symbols)
         skip = False
         for idx, sym in h.items():
            if idx in pfilter:
               isym = isymbols[sym]
               if isym not in pfilter[idx]:
                  skip = True
                  break
         if not skip:
            props.setProperty(first_name, i == base)
            props.setProperty(last_name, i-base >= l-1)
            props.setProperty(var_name, i)
            self._helicity_stack.append(h)
            yield props
            self._helicity_stack.pop()
         i += 1
         
   def modified_helicity(self, *args, **opts):
      if (len(self._helicity_stack) > 0) and \
            ("modify" in opts) and ("to" in opts):
         sym = golem.algorithms.helicity.heli_to_symbol
         symbol_plus   = self._setup_name("symbol_plus",   sym[+1], opts)
         symbol_minus  = self._setup_name("symbol_minus",  sym[-1], opts)
         symbol_plus2  = self._setup_name("symbol_plus2",  sym[+2], opts)
         symbol_minus2 = self._setup_name("symbol_minus2", sym[-2], opts)
         symbol_zero   = self._setup_name("symbol_zero",   sym[ 0], opts)
         base = int(self._setup_name("base", "0", opts))
         prefix   = self._setup_name("prefix",   "", opts)
         var_name = self._setup_name("var", prefix + "helicity", opts)

         symbols = {
                  -2: symbol_minus2,
                  -1: symbol_minus,
                   0: symbol_zero,
                  +1: symbol_plus,
                  +2: symbol_plus2
               }

         key = opts["modify"]
         value = opts["to"]
         index = self._eval_int(key)-1
         helicity = self._helicity_stack[-1].copy()
         helicity[index] = value
      
         i = base
         for h in self._helicity_comb:
            h = golem.util.tools.encode_helicity(h, symbols)
            if h == helicity:
               props = Properties()
               props.setProperty(var_name, str(i))
               yield props
            i+=1

   def _compute_program(self):
      # Calculate dependencies between auxiliary vectors
      lst = sorted(self._references.keys())

      # Example: self._references = {0: 'l2', 1: 'l1', 2: 'l2', 3: 'l2'}
      #          self._masses = ['m', 'm', 'm', '0']
      dependencies = {}
      for i in lst:
         vector = self._references[i]
         mass = self._masses[i]
         if mass == "0":
            continue
         if vector.startswith("l"):
            idx = int(vector[1:]) - 1
            dependencies[i] = set([idx])
         else:
            dependencies[i] = set()
      # Now: dependencies = {
      #  0: set(['l2']),
      #  1: set(['l1']),
      #  2: set(['l2'])}

      for i in dependencies.keys():
         d = dependencies[i]
         new_d = set(d)
         flag = True
         while flag:
            d = frozenset(new_d)
            for j in d:
               new_d.update(dependencies[j])
               
            flag = (new_d != d)
         dependencies[i] = new_d
      # Now: dependencies = {
      #  1: set(['l1', 'l2']),
      #  2: set(['l1', 'l2']),
      #  3: set(['l1', 'l2'])}

      # Program: a list of instructions encoded as:
      #   [i]    == ligt_cone_decomposition(k_i, ref_i)
      #   [i, j] == symmetric splitting of k_i and k_j
      program = []
      available = set()
      while len(dependencies) > 0:
         success = False
         indep = list(filter(lambda i: len(dependencies[i]) == 0,
               dependencies.keys()))
         for i in indep:
            program.append([i])
            success = True

         if success:
            available.update(indep)
         else:
            # try splittings
            for i, depi in dependencies.items():
               li = "l%d" % (i+1)
               for j, depj in dependencies.items():
                  if j <= i:
                     continue
                  lj = "l%d" % (j+1)
                  if self._references[i] == lj and self._references[j] == li:
                     success = True
                     program.append([i, j])
                     available.update([i, j])
                     break
         if success:
            for i in available:
               if i in dependencies:
                  del dependencies[i]
            for i in dependencies.keys():
               dependencies[i].difference_update(available)
         else:
            raise golem.util.parser.TemplateError(
                  "Cannot create initialization for kinematics")

      return program

   def instructions(self, *args, **opts):
      """
      Enumerates a sequence of instructions to initialize
      the l-momenta.

      [% @for instructions opcode=<name>
         index1=<name> mass1=<name>
         index2=<name> mass2=<name>
      %]
         [%opcode%] -- either 1 or 2
         [%index%]  -- the number of the leg.
         [%mass%]  -- the mass of the corresponding external vector
      """
      opcode_name = self._setup_name("opcode", "opcode", opts)
      index1_name = self._setup_name("index1", "index1", opts)
      index2_name = self._setup_name("index2", "index2", opts)
      mass1_name = self._setup_name("mass1", "mass1", opts)
      mass2_name = self._setup_name("mass2", "mass2", opts)
      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)

      program = self._compute_program()
      references = self._references

      last = len(program) - 1

      for index, inst in enumerate(program):
         props = Properties()
         props.setProperty(first_name, index == 0)
         props.setProperty(last_name, index == last)
         props.setProperty(opcode_name, len(inst))

         props.setProperty(index1_name, inst[0] + 1)
         props.setProperty(mass1_name, self._masses[inst[0]])
         if len(inst) == 1:
            ref = self._references[inst[0]]
            j = int(ref[1:])
            mass = self._masses[j - 1]
            props.setProperty(index2_name, j)
            props.setProperty(mass2_name, mass)
         else:
            props.setProperty(index2_name, inst[1]+1)
            props.setProperty(mass2_name, self._masses[inst[1]])

         index += 1
         yield props
