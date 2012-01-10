# vim: ts=3:sw=3:expandtab
import golem.properties
import itertools

symbol_to_heli = {'0': 0, '+': +1, '-': -1,
      'p': +2, 'm': -2, 'P': +3, 'M': -3}
heli_to_symbol = {0: '0', +1: '+', -1: '-',
      +2: 'p', -2: 'm', +3: 'P', -3: 'M'}

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

def reference_vectors(conf, in_particles, out_particles):
   """
   For a given process and a given helicity choose, heuristicly,
   a good set of reference momenta.

   PARAMETER
      conf          -- the configuration.
      in_particles  -- list of incoming particles.
      out_particles -- list of outgoing particles.

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
   suggestions = dict(map(lambda s: map(int, s.split(":")), suggstr))
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

         by_index[index] = "l%d" % (index + 1)
      else:
         if abs(twospin) >= 2:
            gauge_vector_required.append(index)
         external_massless.append("k%d" % (index + 1))

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
   for vec, ref in suggestions.items():
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
         l1 = "l%d" % (particle + 1)
         l2 = "l%d" % (particle2 + 1)
         references[particle] = l2
         references[particle2] = l1
         available_massless.append(l2)
      else:
         particle = reference_required.pop()
         l1 = "l%d" % (particle + 1)
         # Preferably choose k1 or k2, because they are
         # more likely to be IR-safe from experimental cuts
         if len(external_massless) > 0:
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
      k1 = "k%d" % (particle + 1)
      if len(gauge_vector_required) > 0:
         particle2 = gauge_vector_required.pop()
         k2 = "k%d" % (particle2 + 1)
         references[particle] = k2
         references[particle2] = k1
      else:
         my_externals = filter(lambda x: x != k1, external_massless)
         if len(my_externals) > 0:
            if "k2" in my_externals:
               references[particle] = "k2"
            elif "k1" in my_externals:
               references[particle] = "k1"
            else:
               references[particle] = my_externals[0]
         else:
            my_available = filter(lambda x: x != k1, available_massless)
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
      >>> print parse_helicity("+-0p")
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
      # parity = "parity" in lsymmetries

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
                  error("In symmetries=%s ... : '%s' is not a PDG code."
                        % (s, pidx))
            else:
               try:
                  idx = int(idx) - 1
               except ValueError:
                  error("In symmetries=%s ... : '%s' is not a particle number."
                        % (s, idx))
               if idx < 0 or idx >= len(in_particles) + len(out_particles):
                  error("In symmetries=%s ... : '%d' is not in a good range."
                        % (s, idx+1))

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
            error("Cannot apply 'flavour' or 'family' " +
               "symmetry to this external state.")

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
            error("Cannot apply 'lepton' or 'generation' " +
               "symmetry to this external state.")

         qi = list(leptons.keys())
         ai = list(anti_leptons.keys())
         for p in itertools.permutations(ai):
            lepton_assignments += 1
            valid = True
            lines = []
            for q, a in zip(qi, p):
               qpdg, qm, qg = leptons[q]
               apdg, am, ag = anti_leptons[a]
               if (flavour and qpdg != apdg) or (family and qg != ag):
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
         for k, h_set in fixed.items():
            if heli[k] not in h_set:
               return False

         for branches in fermion_filters:
            this_filter = False
            for lines in branches:
               branch = True
               for fermion, anti_fermion in lines:
                  hf = heli[fermion]
                  ha = heli[anti_fermion]
                        (fermion, anti_fermion, hf, ha))

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
       
def find_symmetry_group(helicity_list, conf):
   """
   Find a set of symmetry transformations which maps helicities of the
   given list onto each other.

   A symmetry transformation is given as a pair (h, lst) where h is
   an index in the original list, and lst is a list of triples (k, m, p)
   where k is the index of a momentum, m is either +1 or -1 and p is either
   True or False. m == -1 means that -vec(k,:) has to be plugged in at this
   position and p == True means that parity has to be applied to this
   vector.

   The result is a list of symmetry transformations. If result[i] == (i, lst)
   then lst should be None.

   """
   in_particles, out_particles = generate_particle_lists(conf)

   groups = {}

   # find groups of identical particles
   for i, p in enumerate(in_particles):
      name = str(p)
      if name not in groups:
         groups[name] = []

      groups[name].append(i)

   ofs = len(in_particles)

   for i, p in enumerate(out_particles):
      name = p.getPartner()
      if name not in groups:
         groups[name] = []

      groups[name].append(i+ofs)

