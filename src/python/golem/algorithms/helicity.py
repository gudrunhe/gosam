# vim: ts=3:sw=3:expandtab
import golem.properties
import golem.algorithms.color
import itertools
import sys
from copy import deepcopy

import logging
logger = logging.getLogger(__name__)

symbol_to_heli = {'0': 0, '+': +1, '-': -1,
      'k': +2, 'm': -2, 'K': +3, 'M': -3}
heli_to_symbol = {0: '0', +1: '+', -1: '-',
      +2: 'k', -2: 'm', +3: 'K', -3: 'M'}

massless_states = [
      [0],          # spin 0
      [-1,1],       # spin 1/2
      [-1,1],       # spin 1
      [-2,2],       # spin 3/2
      [-2,2]        # spin 2
   ]

massive_states = [
      [0],          # spin 0
      [-1,1],       # spin 1/2
      [-1,0,1],     # spin 1
      [-2,-1,1,2],  # spin 3/2
      [-2,-1,0,1,2] # spin 2
   ]

def reference_vectors(conf, in_particles, out_particles, return_particle_ids=False):
   """
   For a given process and a given helicity choose, heuristicly,
   a good set of reference momenta.

   PARAMETER
      conf          -- the configuration.
      in_particles  -- list of incoming particles.
      out_particles -- list of outgoing particles.
      particle_ids  -- return reference vectors in terms of particle ids rather than momenta

   The algorithms tries to avoid the situation where
   ref(k1)=l2 and ref(k2)=l1. This is only used when no
   external light-like momenta are available.
   In this case the function light_cone_split (kinematics.f90)
   needs to be called.

   In all other cases the algorithm imposes an order on the
   momenta such that ref(k_i)=l_j only if l_j can be computed
   without knowing l_i; in general, it produces a cycle free
   dependency graph whenever possible.

   """
   zeroes = golem.util.tools.getZeroes(conf)
   suggstr = conf.getProperty(golem.properties.reference_vectors)
   if suggstr==[""]:
      suggstr=[]
   suggestions = dict([list(map(int, s.split(":"))) for s in suggstr])
   num_legs = len(in_particles) + len(out_particles)
   assert num_legs > 1, "Seriously, you need at least two particles!"

   external_massless = []
   reference_required = []
   gauge_vector_required = []
   references = {}
   not_favourable = set()
   ini_indices = set()

   by_index = {}

   def classify(particle, index, is_ini):
      mass = particle.getMass(zeroes)
      twospin = particle.getSpin()
      is_massive = particle.isMassive(zeroes)

      if is_massive:
         reference_required.insert(0, index)
         if abs(twospin) >= 2:
            not_favourable.update([index])

         if return_particle_ids:
            by_index[index] = index
         else:
            by_index[index] = "l%d" % (index + 1)

      else:
         if abs(twospin) >= 2:
            gauge_vector_required.append(index)

         if return_particle_ids:
            external_massless.append(index)
         else:
            external_massless.append("k%d" % (index + 1))

         if return_particle_ids:
            by_index[index] = index
         else:
            by_index[index] = "k%d" % (index + 1)
   #### END OF classify

   i = 0
   for ini in in_particles:
      classify(ini, i, True)
      ini_indices.update([i])
      i += 1

   for fin in out_particles:
      classify(fin, i, False)
      i += 1
   assert i == num_legs

   available_massless = external_massless[:]

   # Work through list of suggestions first
   for vec, ref in list(suggestions.items()):
      kref = by_index[ref-1]
      kvec = by_index[vec-1]
      if vec - 1 in reference_required:
         i = reference_required.index(vec - 1)
         del reference_required[i]
      elif vec - 1 in gauge_vector_required:
         i = gauge_vector_required.index(vec - 1)
         del gauge_vector_required[i]
      references[vec-1] = kref
      if kvec not in available_massless:
         available_massless.append(kvec)

   while(len(reference_required) > 0):
      if len(available_massless) == 0:
         # No vectors available, hence we must split a pair
         assert len(reference_required) > 0
         preferred = set(reference_required)
         # Avoid vector bosons since we haven't implemented
         # the polarisation vectors for the case of symmetric splitting.
         preferred.difference_update(not_favourable)

         # Avoid initial state vectors, which have typically
         # large momenta but small masses (numerically not favourable).
         if len(preferred - ini_indices) >= 2:
            preferred.difference_update(ini_indices)
         elif len(preferred) < 2:
            raise golem.util.parser.TemplateError(
               """Cannot produce correct code for your problem.\n\
            Please, see lorentz.pdf for more details.""")

         if len(preferred) > 0:
            particle = preferred.pop()
            reference_required.remove(particle)
         else:
            particle = reference_required.pop()

         if len(preferred) > 0:
            particle2 = preferred.pop()
            reference_required.remove(particle2)
         else:
            particle2 = reference_required.pop()

         if return_particle_ids:
            l1 = particle
            l2 = particle2
         else:
            l1 = "l%d" % (particle + 1)
            l2 = "l%d" % (particle2 + 1)

         references[particle] = l2
         references[particle2] = l1
         available_massless.append(l2)
      else:
         particle = reference_required.pop()

         if return_particle_ids:
            l1 = particle
         else:
            l1 = "l%d" % (particle + 1)

         # Preferably choose k1 or k2, because they are
         # more likely to be IR-safe from experimental cuts
         if len(external_massless) > 0:

            if return_particle_ids:
               if 1 in external_massless:
                  references[particle] = 1
               elif 0 in external_massless:
                  references[particle] = 0
               else:
                  references[particle] = external_massless[0]
            else:
               if "k2" in external_massless:
                  references[particle] = "k2"
               elif "k1" in external_massless:
                  references[particle] = "k1"
               else:
                  references[particle] = external_massless[0]

         else:
            references[particle] = available_massless[0]
      available_massless.append(l1)

   # Massive gauge bosons are already covered in the above case
   # hence gauge_vector_required only refers to massless particles.
   while len(gauge_vector_required) > 0:
      particle = gauge_vector_required.pop()

      if return_particle_ids:
         k1 = particle
      else:
         k1 = "k%d" % (particle + 1)

      if len(gauge_vector_required) > 0:
         particle2 = gauge_vector_required.pop()

         if return_particle_ids:
            k2 = particle2
         else:
            k2 = "k%d" % (particle2 + 1)

         references[particle] = k2
         references[particle2] = k1
      else:
         my_externals = [x for x in external_massless if x != k1]
         if len(my_externals) > 0:

            if return_particle_ids:
               if 1 in my_externals:
                  references[particle] = 1
               elif 0 in my_externals:
                  references[particle] = 0
               else:
                  references[particle] = my_externals[0]
            else:
               if "k2" in my_externals:
                  references[particle] = "k2"
               elif "k1" in my_externals:
                  references[particle] = "k1"
               else:
                  references[particle] = my_externals[0]
         else:
            my_available = [x for x in available_massless if x != k1]
            # If it's a proper process we will find another particle:
            assert len(my_available) > 0
            references[particle] = my_available[0]

   return references

def parse_helicity(string, symbols=symbol_to_heli):
   """
   Parse a string representation of a helicity combination
   into a dictionary of helicities.

   PARAMETER

   string  -- the string representation
   symbols -- a dictionary of symbols

   EXAMPLE
      >>> print(parse_helicity("+-0k"))
      {0: 1, 1: -1, 2: 0, 3: 2}
   """
   result = {}
   i = 0
   for c in string:
      if c in symbols:
         result[i] = symbols[c]
         i += 1
      else:
         raise golem.util.parser.TemplateError(
            "Illegal helicity: %r" % string)
   return result

def generate_symmetry_filter(conf, zeroes, in_particles, out_particles):
      symmetries = conf.getProperty(golem.properties.symmetries)
      lsymmetries = [s.lower().strip() for s in symmetries]
      family = "family" in lsymmetries
      flavour = "flavour" in lsymmetries
      lepton = "lepton" in lsymmetries
      generation = "generation" in lsymmetries

      quarks = {}
      anti_quarks = {}
      leptons = {}
      anti_leptons = {}

      fixed = {}
      pdg_fixed = {}
      for s in symmetries:
         if "=" in s:
            idx, hel = s.split("=", 1)
            if idx.strip().startswith("%"):
               #selection by pdg code
               pos = idx.index("%")
               pidx = idx[pos+1:]
               if pidx.startswith("+"):
                  signs = [1]
                  pidx = pidx[1:]
               elif pidx.startswith("-"):
                  signs = [-1]
                  pidx = pidx[1:]
               else:
                  signs = [1,-1]

               try:
                  pdg = int(pidx)
                  for sign in signs:
                     pdg_fixed[sign*pdg] = \
                           set(golem.algorithms.helicity.parse_helicity(
                                 hel.strip()).values())
               except ValueError:
                  logging.critical("In symmetries=%s ... : '%s' is not a PDG code."
                        % (s, pidx))
                  sys.exit("GoSam terminated due to an error")
            else:
               try:
                  idx = int(idx) - 1
               except ValueError:
                 logging.critical("In symmetries=%s ... : '%s' is not a particle number."
                        % (s, idx))
                 sys.exit("GoSam terminated due to an error")
               if idx < 0 or idx >= len(in_particles) + len(out_particles):
                  logging.critical("In symmetries=%s ... : '%d' is not in a good range."
                        % (s, idx+1))
                  sys.exit("GoSam terminated due to an error")

               fixed[idx] = set(golem.algorithms.helicity.parse_helicity(
                  hel.strip()).values())

      for idx, p in enumerate(in_particles):
         sp = p.getSpin()
         if abs(sp) % 2 != 1:
            continue

         m = p.isMassive(zeroes)
         pdg = p.getPDGCode()
         apdg = abs(pdg)

         if pdg in range(1,9):
            quarks[idx] = (apdg, m, ((apdg-1)//2) + 1)
         elif -pdg in range(1,9):
            anti_quarks[idx] = (apdg, m, ((apdg-1)//2) + 1)
         elif pdg in range(11,19):
            leptons[idx] = (apdg, m, ((apdg-11)//2) + 1)
         elif -pdg in range(11,19):
            anti_leptons[idx] = (apdg, m, ((apdg-11)//2) + 1)

      li = len(in_particles)
      for idx, p in enumerate(out_particles):
         sp = -p.getSpin()
         if abs(sp) % 2 != 1:
            continue

         m = p.isMassive(zeroes)
         pdg = -p.getPDGCode()
         apdg = abs(pdg)

         if pdg in range(1,9):
            quarks[li+idx] = (apdg, m, ((apdg-1)//2) + 1)
         elif -pdg in range(1,9):
            anti_quarks[li+idx] = (apdg, m, ((apdg-1)//2) + 1)
         elif pdg in range(11,19):
            leptons[li+idx] = (apdg, m, ((apdg-11)//2) + 1)
         elif -pdg in range(11,19):
            anti_leptons[li+idx] = (apdg, m, ((apdg-11)//2) + 1)

      quark_filters = []
      lepton_filters = []

      quark_assignments = 0
      lepton_assignments = 0

      if flavour or family:
         if len(quarks) != len(anti_quarks):
            logging.critical("Cannot apply 'flavour' or 'family' " +
               "symmetry to this external state.")
            sys.exit("GoSam terminated due to an error")

         qi = list(quarks.keys())
         ai = list(anti_quarks.keys())
         for p in itertools.permutations(ai):
            quark_assignments += 1
            valid = True
            lines = []
            for q, a in zip(qi, p):
               qpdg, qm, qg = quarks[q]
               apdg, am, ag = anti_quarks[a]
               if (flavour and qpdg != apdg) or (family and qg != ag):
                  valid = False
                  break
               if not (am or qm):
                  lines.append( (q, a) )
            if valid:
               quark_filters.append(lines)

      if lepton or generation:
         if len(leptons) != len(anti_leptons):
            logging.critical("Cannot apply 'lepton' or 'generation' " +
               "symmetry to this external state.")
            sys.exit("GoSam terminated due to an error")

         qi = list(leptons.keys())
         ai = list(anti_leptons.keys())
         for p in itertools.permutations(ai):
            lepton_assignments += 1
            valid = True
            lines = []
            for q, a in zip(qi, p):
               qpdg, qm, qg = leptons[q]
               apdg, am, ag = anti_leptons[a]
               if (lepton and qpdg != apdg) or (generation and qg != ag):
                  valid = False
                  break
               if not (am or qm):
                  lines.append( (q, a) )
            if valid:
               lepton_filters.append(lines)

      fermion_filters = []
      if lepton_assignments > 0:
         fermion_filters.append(lepton_filters)

      if quark_assignments > 0:
         fermion_filters.append(quark_filters)

      inp = in_particles[:]
      outp = out_particles[:]
      linp = len(inp)

      def filter_function(heli):
         for i, p in enumerate(inp):
            pdg = p.getPDGCode()
            if pdg in pdg_fixed:
               if heli[i] not in pdg_fixed[pdg]:
                  return False
         for i, p in enumerate(outp):
            pdg = p.getPDGCode()
            if pdg in pdg_fixed:
               if heli[linp+i] not in pdg_fixed[pdg]:
                  return False
         for k, h_set in list(fixed.items()):
            if heli[k] not in h_set:
               return False

         for branches in fermion_filters:
            this_filter = False
            for lines in branches:
               branch = True
               for fermion, anti_fermion in lines:
                  hf = heli[fermion]
                  ha = heli[anti_fermion]

                  if (float(linp - anti_fermion) - 0.5) * \
                        (float(linp - fermion) - 0.5) > 0:
                     fulfilled = (hf == - ha)
                  else:
                     fulfilled = (hf == ha)

                  if not fulfilled:
                     branch = False
                     break
               if branch:
                  this_filter = True
                  break
            if not this_filter:
               return False
         return True

      return filter_function

def parse_cycles(s):
   cycles = []
   current_cycle = None
   level = 0
   tokens = s.replace("(", " ( ").replace(")", " ) ").split()
   for token in tokens:
      if token == "(":
         if level == 0:
            level = 1
            current_cycle = []
         else:
            logger.critical("Bad place for %r in permutation %r" % (token, s))
            sys.exit("GoSam terminated due to an error")
      elif token == ")":
         if level == 1:
            level = 0
            if len(current_cycle) > 1:
               cycles.append(current_cycle)
         else:
            logger.critical("Bad place for %r in permutation %r" % (token, s))
            sys.exit("GoSam terminated due to an error")
      else:
         if level == 1:
            try:
               idx = int(token) - 1
               current_cycle.append(idx)
            except ValueError:
               logger.critical("Unrecognized token %r in permutation %r." % (token, s))
               sys.exit("GoSam terminated due to an error")
         else:
            logger.critical("Bad place for %r in permutation %r" % (token, s))
            sys.exit("GoSam terminated due to an error")

   return cycles

class Permutation:
   def __init__(self, a_map={}):
      self._map = {}
      for k, v in list(a_map.items()):
         if k == v:
            continue
         else:
            self._map[k] = v

   def __call__(self, arg):
      if isinstance(arg, Permutation):
         result = {}
         keys = set(self._map.keys()).union(list(arg._map.keys()))
         for k in keys:
            kk = arg(k)
            v = self(kk)
            if k == v:
               continue
            result[k] = v
         return Permutation(result)

      elif isinstance(arg, int):
         if arg in self._map:
            return self._map[arg]
         else:
            return arg
      else:
         return list(map(self, arg))

   def inverse(self):
      result = {}
      for k, v in list(self._map.items()):
         result[v] = k

      return Permutation(result)

   def cycles(self, arg):
      """
      Returns a string representing the permutation
      in cycle notation.

      Increments all elements of the permutation by 'arg'
      """
      # Get largest value mapped by permutation
      max_entry = 0
      for key, value in list(self._map.items()):
         if key > max_entry:
            max_entry = key
         if value > max_entry:
            max_entry = value
      max_entry += 1
      # Build cycles
      unchecked = [True] * max_entry
      cyclic_form = []
      for i in range(max_entry):
         if unchecked[i]:
            cycle = []
            cycle.append(str(i+arg))
            unchecked[i] = False
            j = i
            while unchecked[self(j)]:
               j = self(j)
               cycle.append(str(j+arg))
               unchecked[j] = False
            if len(cycle) > 1:
               cyclic_form.append(cycle)
      # Produce str representation
      result = ""
      for elem in cyclic_form:
         result += '(' + ''.join(elem) + ')'
      return result

   def __str__(self):
      args = []
      for k in sorted(self._map.keys()):
         v = self._map[k]
         if k == v:
            continue
         args.append("%d -> %d" % (k, v))
      return "Permutation(%s)" % ", ".join(args)

   def __repr__(self):
      return str(self)

   def __hash__(self):
      return hash(tuple(self._map.items()))

   def __eq__(self, other):
      if isinstance(other, Permutation):
         return len(self(other.inverse())._map) == 0
      else:
         return False


def permutation_from_cycles(cycles):
   result = Permutation()
   for cycle in cycles:
      l = len(cycle)
      for p in range(l-1):
         c0 = cycle[p]
         c1 = cycle[p+1]
         result = result(Permutation({c0: c1, c1: c0}))
   return result

def color_sort(tpl):
   lines, traces = tpl
   ntraces = []
   for trace in traces:
      l = len(trace)
      m = min(trace)
      r = list(reversed(trace))
      im = trace.index(m)
      ir = r.index(m)

      t = trace[im:] + trace[:im]
      tr = r[ir:] + r[:ir]
# gionata's modification to correct dipoles
#      if tr[1] < t[1]:
#         ntraces.append(tr)
#      else:
      ntraces.append(t)

   return (sorted(lines, key=lambda lst: lst[0]),
         sorted(ntraces, key=lambda lst: lst[0]))

def group_identical_particles(conf, in_particles, out_particles):
   """
   Produce a dictionary with particle names as key and a list of particle
   indices as value. Returns also a list of indices which should be
   considered relevant when permuting legs (during symmetry finding).
   """
   numpolvec = conf["__NUMPOLVEC__"].lower() == "true"
   zeroes = golem.util.tools.getZeroes(conf)

   relevant_indices = []
   groups = {}

   for i, p in enumerate(in_particles):
      name = str(p)
      if numpolvec:
         if abs(p.getSpin()) != 2 or (p.isMassive(zeroes) and p.getSpin() != 0):
            relevant_indices.append(i)
         else:
            continue
      else:
         relevant_indices.append(i)
      if name not in groups:
         groups[name] = []
      groups[name].append(i)

   ofs = len(in_particles)

   for i, p in enumerate(out_particles):
      name = p.getPartner()
      if numpolvec:
         if abs(p.getSpin()) != 2 or (p.isMassive(zeroes) and p.getSpin() != 0):
            relevant_indices.append(i + ofs)
         else:
            continue
      else:
         relevant_indices.append(i + ofs)
      if name not in groups:
         groups[name] = []
      groups[name].append(i + ofs)

   return groups, relevant_indices

def generate_all_permutations(conf, groups):
   """
   Generate a set of all permutations which exchange identical particles.

   PARAMETERS
      groups -- a dictionary with particle names as key and a list of particle
                indices as value

   See also: group_identical_particles
   """

   symmetries = conf.getProperty(golem.properties.symmetries)
   lsymmetries = [s.lower().strip() for s in symmetries]

   # Produce list of permutations explicitly requested by user
   user_permutations = [Permutation()]
   for p in lsymmetries:
      if not p.startswith("("):
         continue
      cycles = parse_cycles(p)
      user_permutations.append(permutation_from_cycles(cycles))

   permutation_group_factors = [ set(user_permutations) ]
   identical_particles = []
   for lst in list(groups.values()):
      if len(lst) > 1:
         identical_particles.append(lst)
         permutation_group_factors.append(set(
               [ Permutation(dict(list(zip(lst, p))))
                  for p in itertools.permutations(lst)]))

   while len(permutation_group_factors) > 1:
      f1 = permutation_group_factors.pop()
      f2 = permutation_group_factors.pop()
      f = set()
      for p1 in f1:
         for p2 in f2:
            f.add(p1(p2))
      permutation_group_factors.append(f)

   return permutation_group_factors.pop()

def find_symmetry_mapping(helicity, perm, relevant_indices, helicity_list, generated_helicities,
                          conf, in_particles, out_particles):
   """
   First apply a permutation to a helicity then try to find a symmetry transformation
   onto a generated helicity.

   A symmetry transformation is given as a tuple (h, lst, c, p) where h is
   an index in the original list, c is the permuted color basis, p is the
   permutation that led to this symmetry transformation.
   The element lst is a list of triples (k, m, p) where k is the index of a momentum,
   m is either +1 or -1 and p is either True or False. m == -1 means that -vec(k,:)
   has to be plugged in at this position and p == True means that parity has to be
   applied to this vector.

   The result is an individual symmetry transformation.

   PARAMETERS
      helicity             -- the input helicity
      perm                 -- the permutaiton to apply to the input helicity
      relevant_indices     -- the list of indicies that should be considered
                              when finding the symmetry transformation
      helicity_list        -- a list of all helicities
      generated_helicities -- a list of the indicies of helicities which
                              should be mapped to by the symmetry transformation

   See also: find_symmetry_group, find_gauge_invariant_symmetry_group
   """
   symmetries = conf.getProperty(golem.properties.symmetries)
   lsymmetries = [s.lower().strip() for s in symmetries]
   parity = "parity" in lsymmetries

   li = len(in_particles)
   lo = len(out_particles)
   in_indices = list(range(li))
   out_indices = list(range(li,li+lo))

   color_basis = list(map(color_sort, golem.algorithms.color.get_color_basis(in_particles, out_particles)))

   # compute permuted color basis:
   pcb = [color_sort(([perm(line) for line in lines],
                      [perm(trace) for trace in traces]))
          for lines, traces in color_basis]
   icb = [color_basis.index(c) for c in pcb]
   permuted_color_basis = icb

   # permute particle indices
   p_in_indices = perm(in_indices)
   p_out_indices = perm(out_indices)

   p_helicity = {}
   signs = []

   for i, j in zip(in_indices, p_in_indices):
      h = helicity[j]
      if j not in in_indices:
         p_helicity[i] = -h
         signs.append(-1)
      else:
         p_helicity[i] = h
         signs.append(+1)

   for i, j in zip(out_indices, p_out_indices):
      h = helicity[j]
      if j not in out_indices:
         p_helicity[i] = -h
         signs.append(-1)
      else:
         p_helicity[i] = h
         signs.append(+1)

   rp_helicity = [p_helicity[i] for i in relevant_indices]
   mrp_helicity = [-h for h in rp_helicity]

   mapping = None
   for gi in generated_helicities:

      gh = helicity_list[gi]
      r_gh = [gh[i] for i in relevant_indices]

      if (rp_helicity == r_gh):
         lst = [(perm(i), signs[i], False) for i in range(li + lo)]
         mapping = (gi, lst, permuted_color_basis, perm)
         break
      elif parity and (mrp_helicity == r_gh):
         lst = [(perm(i), signs[i], True) for i in range(li + lo)]
         mapping = (gi, lst, permuted_color_basis, perm)

   return mapping

def find_symmetry_group(helicity_list, conf, in_particles, out_particles):
   """
   Find a set of symmetry transformations which maps helicities of the
   given list onto each other.

   A symmetry transformation is given as a tuple (h, lst, c, p) where h is
   an index in the original list, c is the permuted color basis, p is the
   permutation that led to this symmetry transformation.
   The element lst is a list of triples (k, m, p) where k is the index of a momentum,
   m is either +1 or -1 and p is either True or False. m == -1 means that -vec(k,:)
   has to be plugged in at this position and p == True means that parity has to be
   applied to this vector.

   The result is a list of symmetry transformations. If result[i] == (i, lst, c, p)
   then lst should be None.

   See also: find_gauge_invariant_symmetry_group
   """
   noreduce = conf["__REDUCE_HELICITIES__"].lower() == "false"

   color_basis = list(map(color_sort, golem.algorithms.color.get_color_basis(in_particles, out_particles)))

   # If requested, do not attempt to reduce the number of helicities
   if noreduce:
      result = []
      for ih, helicity in enumerate(helicity_list):
         result.append( (ih, None, list(range(len(color_basis)))) )
      return result

   groups, relevant_indices = group_identical_particles(conf, in_particles, out_particles)
   permutation_group = generate_all_permutations(conf, groups)

   generated_helicities = []
   result = []

   for ih, helicity in enumerate(helicity_list):
      mapping = None
      for perm in permutation_group:
         mapping = find_symmetry_mapping(helicity, perm, relevant_indices,
                                         helicity_list, generated_helicities,
                                         conf, in_particles, out_particles)
         if mapping is not None:
            break

      if mapping is None:
         generated_helicities.append(ih)
         result.append( (ih, None, list(range(len(color_basis))), Permutation()) )
      else:
         result.append( mapping )

   # Append gauge invariant set to mappings (each helicity assumed to belong to different group)
   for ih,mapping in enumerate(result):
      result[ih] = mapping + (ih,)

   return result

def find_gauge_invariant_symmetry_group(helicity_list, conf, in_particles, out_particles):
   """
   Find a set of symmetry transformations which maps helicities of the
   given list onto each other. Only return symmetry transformations
   which respect gauge invariance.

   A symmetry transformation is given as a tuple (h, lst, c, p) where h is
   an index in the original list, c is the permuted color basis, p is the
   permutation that led to this symmetry transformation.
   The element lst is a list of triples (k, m, p) where k is the index of a momentum,
   m is either +1 or -1 and p is either True or False. m == -1 means that -vec(k,:)
   has to be plugged in at this position and p == True means that parity has to be
   applied to this vector.

   The result is a list of symmetry transformations. If result[i] == (i, lst, c, p)
   then lst should be None.

   See also: find_symmetry_group
   """
   zeroes = golem.util.tools.getZeroes(conf)
   noreduce = conf["__REDUCE_HELICITIES__"].lower() == "false"

   color_basis = list(map(color_sort, golem.algorithms.color.get_color_basis(in_particles, out_particles)))

   # If requested, do not attempt to reduce the number of helicities
   if noreduce:
      result = []
      for ih, helicity in enumerate(helicity_list):
         result.append( (ih, None, list(range(len(color_basis))), Permutation(), ih) )
      return result

   # Get list of massive/massless in_particles
   relevant_massive_particle_indices = []
   irrelevant_particle_indices = []
   for index, particle in enumerate(in_particles):
      if particle.isMassive(zeroes) and particle.getSpin() != 0:
         relevant_massive_particle_indices.append(index)
      else:
         irrelevant_particle_indices.append(index)
   for index, particle in enumerate(out_particles, start=len(in_particles)):
      if particle.isMassive(zeroes) and particle.getSpin() != 0:
         relevant_massive_particle_indices.append(index)
      else:
         irrelevant_particle_indices.append(index)

   # If only massless particles present, each helicity is a gauge invariant quantity => search all permutations
   if not relevant_massive_particle_indices:
      return find_symmetry_group(helicity_list, conf, in_particles, out_particles)

   #
   #  Step 1 - get list of gauge invariant sets of helicities and pick out only the part requested by the user
   #

   # Get list of helicities of massless particles, ignoring massive particle helicities
   massless_helicity_list = deepcopy(helicity_list)
   for helicity in massless_helicity_list:
      for index in relevant_massive_particle_indices:
         helicity.pop(index)

   # Remove duplicates
   massless_helicity_list = [dict(t) for t in sorted(set(tuple(sorted(d.items())) for d in massless_helicity_list))]

   # Look through helicity_list and group the parts of each gauge invariant set requested by the user
   gauge_invariant_sets = []
   for massless_helicity in massless_helicity_list:
      gauge_invariant_set = []
      for ih,helicity in enumerate(helicity_list):
         match = True
         for index in helicity:
               if index not in relevant_massive_particle_indices:
                  if massless_helicity[index] != helicity[index]:
                     match = False
                     break
         if match:
            gauge_invariant_set.append({"index": ih, "helicity" : helicity})
      gauge_invariant_sets.append(gauge_invariant_set)

   # List gauge set of each helicity
   helicity_gauge_set = [0] * len(helicity_list)
   for ig,gauge_invariant_set in enumerate(gauge_invariant_sets):
      for helicity in gauge_invariant_set:
         helicity_gauge_set[helicity["index"]] = ig

   #
   #  Step 2 - generate all permutations and sort them:
   #           * group permutations alter the reference vectors dictionary:
   #               they should be applied only to the entire gauge invariant set
   #           * individual permutations do not alter the reference vectors dictionary:
   #               they can be applied to an individual helicity
   #

   # Generate all permutations
   groups, relevant_indices = group_identical_particles(conf, in_particles, out_particles)
   all_permutations = generate_all_permutations(conf, groups)

   # Get dictionary of reference vectors
   ref_vectors = reference_vectors(conf, in_particles, out_particles, return_particle_ids=True)

   # Only the reference vectors of massive particles are relevant (each massless helicity is already a gauge set)
   relevant_ref_vectors = {}
   for key, value in list(ref_vectors.items()):
      if key in relevant_massive_particle_indices:
         relevant_ref_vectors[key] = value

   # Sort pemutations, allow trivial permutation for group or individual particles (always ok)
   group_permutations = set([Permutation()])
   individual_permutations = set([Permutation()])
   for perm in all_permutations:
      # Apply permutation to reference vectors dictionary
      p_relevant_ref_vectors = {}
      for key, value in list(ref_vectors.items()):
         p_relevant_ref_vectors[perm(key)] = perm(value)
      if p_relevant_ref_vectors != relevant_ref_vectors:
         # Permutation alters reference vectors dictionary, must be applied to gauge invariant group
         group_permutations.add(perm)
      else:
         # Permutation leaves reference vectors dictionary invariant, can be applied to individual permutations
         individual_permutations.add(perm)

   #
   # Step 3 - map helicities within a gauge invariant set onto each other
   #

   # Try to minimize helicities within gauge invariant set
   potentially_generated_helicities = []
   mappings = []
   for gauge_invariant_set in gauge_invariant_sets:
      gauge_set_generated_helicities = []
      for helicity in gauge_invariant_set:
         mapping = None
         for i_perm in individual_permutations:
            mapping = find_symmetry_mapping(helicity["helicity"], i_perm, relevant_indices, helicity_list,
                                            gauge_set_generated_helicities,
                                            conf, in_particles, out_particles
                                           )
            if mapping != None:
               mappings.append([helicity,mapping])
               break
         if mapping == None:
            gauge_set_generated_helicities.append(helicity["index"])
      potentially_generated_helicities.extend(gauge_set_generated_helicities)

   # Remove helicities that are already mapped (do not need to be generated) from gauge invariant sets
   gauge_invariant_sets[:] = [ [ helicity for helicity in gauge_invariant_set
                                 if helicity["index"] in potentially_generated_helicities ]
                               for gauge_invariant_set in gauge_invariant_sets ]

   #
   # Step 4 - map gauge invariant sets onto other gauge invariant sets
   #

   # Now try to map helicities between gauge invariant sets
   generated_helicities = []
   for gi,gauge_invariant_set in enumerate(gauge_invariant_sets):
      best_mappings = []
      best_count = 0
      best_helicities_to_generate = [helicity["index"] for helicity in gauge_invariant_set]

      for g_perm in group_permutations:
         potential_mappings = []
         count = 0
         helicities_to_generate = []
         for helicity in gauge_invariant_set:
            # Search for mapping
            mapping = None
            for i_perm in individual_permutations:
               composed_perm = i_perm(g_perm)
               mapping = find_symmetry_mapping(helicity["helicity"], composed_perm, relevant_indices, helicity_list,
                                               generated_helicities,
                                               conf, in_particles, out_particles
                                               )
               if mapping != None:
                  count += 1
                  potential_mappings.append([helicity,mapping])
                  break
            if mapping == None:
               helicities_to_generate.append(helicity["index"])
         if count > best_count:
            best_count = count
            best_mappings = potential_mappings
            best_helicities_to_generate = helicities_to_generate

      # Store mappings and helicities that must be generated
      generated_helicities.extend(best_helicities_to_generate)
      mappings.extend(best_mappings)

   # Begin generating result
   result = [(ih, None, list(range(len(color_basis))), Permutation()) for ih in range(0,len(helicity_list))]
   for mapping in mappings:
      result[mapping[0]["index"]] = mapping[1]

   # Helicities may have been mapped onto helicities within their gauge invariant set
   # which were subsequently mapped onto helicities in another gauge invariant set,
   # fix mappings which point to helicities that will not be generated
   for ih,mapping in enumerate(mappings):
      if mapping[1][0] not in generated_helicities:
         perm1 = mapping[1][3]
         perm2 = result[mapping[1][0]][3]
         composed_perm = perm1(perm2)
         new_mapping = find_symmetry_mapping(mapping[0]["helicity"], composed_perm, relevant_indices, helicity_list,
                                   generated_helicities,
                                   conf, in_particles, out_particles
                                   )
         result[mapping[0]["index"]] = new_mapping
         mappings[ih] = [mapping[0],new_mapping]

   for mapping in mappings:
      assert mapping[1][0] in generated_helicities, \
         "mapping points to a helicity that will not be generated %s" % mapping

   # Append to the result the gauge set to which the helicty belongs result
   for ih,gauge_set in enumerate(helicity_gauge_set):
      result[ih] = result[ih] + (gauge_set,)

   return result

def filter_helicities(conf, in_particles, out_particles):
   key = []
   for i in range(len(in_particles)):
      key.append(in_particles[i].getPDGCode())
   for i in range(len(out_particles)):
      key.append(out_particles[i].getPDGCode())

   smmodels = ['sm','smdiag','smehc']
   applyfilter = False
   # Check if model is some form of SM:
   if conf["modeltype"] is not None:
      if any(item.startswith(conf["modeltype"]) for item in smmodels):
         applyfilter = True
   if conf["model"] is not None:
      if any(item.startswith(conf["model"]) for item in smmodels):
         applyfilter = True

   if applyfilter == True:
      if conf["symmetries"] is None:
         conf["symmetries"] = " "
      # check D,Dbar
      if key.count(1)*10+key.count(-1) == 1 and 'mD' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %-1=+"
      elif key.count(1)*10+key.count(-1) == 10  and 'mD' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %+1=-"
      # check U,Ubar
      if key.count(2)*10+key.count(-2) == 1  and 'mU' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %-2=+"
      elif key.count(2)*10+key.count(-2) == 10  and 'mU' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %+2=-"
      # check S,Sbar
      if key.count(3)*10+key.count(-3) == 1 and 'mS' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %-3=+"
      elif key.count(3)*10+key.count(-3) == 10  and 'mS' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %+3=-"
      # check C,Cbar
      if key.count(4)*10+key.count(-4) == 1  and 'mC' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %-4=+"
      elif key.count(4)*10+key.count(-4) == 10  and 'mC' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %+4=-"
      # check B,Bbar
      if key.count(5)*10+key.count(-5) == 1 and 'mB' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %-5=+"
      elif key.count(5)*10+key.count(-5) == 10  and 'mB' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %+5=-"
      # check T,Tbar
      if key.count(6)*10+key.count(-6) == 1  and 'mT' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %-6=+"
      elif key.count(6)*10+key.count(-6) == 10  and 'mT' in conf[golem.properties.zero]:
         conf["symmetries"] += ", %+6=-"
      # neutrinos:
      if key.count(12) != 0:
         conf["symmetries"] += ", %+12=-"
      if key.count(14) != 0:
         conf["symmetries"] += ", %+14=-"
      if key.count(16) != 0:
         conf["symmetries"] += ", %+16=-"
      if key.count(-12) != 0:
         conf["symmetries"] += ", %-12=+"
      if key.count(-14) != 0:
         conf["symmetries"] += ", %-14=+"
      if key.count(-16) != 0:
         conf["symmetries"] += ", %-16=+"

   return conf
