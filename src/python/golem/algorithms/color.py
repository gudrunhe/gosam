# vim: ts=3:sw=3:expandtab
import golem.util.tools
from golem.util.config import GolemConfigError

def colorbasis(quarks, aquarks, gluons):
   """
   Generates a SU(N) color basis for a set
   of quarks, antiquarks and gluons

   PARAMETER

   quarks -- list of quark indices
   aquarks -- list of anti-quark indices
   gluons -- list of gluon indices

   RESULT

   Yields pairs of lists (lines, traces) that for each
   color basis element contain the open and closed fundamental
   lines forming the basis elements
   """
   lhs = gluons + aquarks
   rhs = gluons + quarks
   nglue = len(gluons)

   try:
      for l in permutations(lhs):
         lines = []
         traces = []
         iglue = set(range(nglue))
         for a in aquarks:
            line = [a]
            r = rhs[l.index(a)]
            while r in [gluons[i] for i in iglue]:
               ir = gluons.index(r)
               line.append(r)
               iglue.remove(ir)
               r = rhs[l.index(r)]
            line.append(r)
            lines.append(line)
         while len(iglue) > 0:
            line = []
            ig = iglue.pop()
            g = gluons[ig]
            r = rhs[l.index(g)]
            while r in [gluons[i] for i in iglue]:
               ir = gluons.index(r)
               line.append(r)
               iglue.remove(ir)
               r = rhs[l.index(r)]
            line.append(r)
            traces.append(line)
         # check for tadpoles
         if len(traces) > 0:
            if min(map(len, traces)) <= 1:
               continue
         yield lines, traces
   except IndexError:
      raise GolemConfigError("It seems that the color charge is not conserved in the process you want to generate.\n\
Perhaps you need to change a particle to its anti-particle in the initial or final state.")

def get_color_basis(in_particles, out_particles):
   """
   Find all colored particles and build a color basis
   """
   quarks = []
   aquarks = []
   gluons = []
   li = len(in_particles)
   for i in range(li):
      p = in_particles[i]
      color_index = i

      if p.getColor() == 3:
         quarks.append(color_index)
      elif p.getColor() == -3:
         aquarks.append(color_index)
      elif p.getColor() == 8:
         gluons.append(color_index)

   for i in range(len(out_particles)):
      p = out_particles[i]
      color_index = li+i
      if p.getColor() == 3:
         aquarks.append(color_index)
      elif p.getColor() == -3:
         quarks.append(color_index)
      elif p.getColor() == 8:
         gluons.append(color_index)

   return [(lines, traces)
      for lines, traces in golem.algorithms.color.colorbasis(
         quarks, aquarks, gluons)]

def permutations(lst):
   """
   Generates all permutations of a list.
   """

   yield lst[:]

   N = len(lst)
   if N <= 1:
      return

   a = range(N)
   face_left = [True for i in a]

   def index_of_max_mobile():
      idx = -1
      max_mobile = -1
      for i in range(N):
         mobile = False
         if (i == 0) and face_left[i]:
            mobile = False
         elif (i == N - 1) and not face_left[i]:
            mobile = False
         elif face_left[i]:
            mobile = a[i - 1] < a[i]
         else:
            mobile = a[i + 1] < a[i]
         
         if mobile:
            if (idx == -1) or (a[i] > max_mobile):
               max_mobile = a[i]
               idx = i
      return idx

   def swap(index):
      if face_left[index]:
         tmp = a[index - 1]
         a[index - 1] = a[index]
         a[index] = tmp
         tmp = face_left[index - 1]
         face_left[index - 1] = face_left[index]
         face_left[index] = tmp
      else:
         tmp = a[index + 1]
         a[index + 1] = a[index]
         a[index] = tmp
         tmp = face_left[index + 1]
         face_left[index + 1] = face_left[index]
         face_left[index] = tmp

   max_index = index_of_max_mobile()


   while(max_index >= 0):
      k = a[max_index]
      swap(max_index)
      yield [lst[i] for i in a]
      for i in range(N):
         if a[i] > k:
            face_left[i] = not face_left[i]
      max_index = index_of_max_mobile()

def num_colors(F, G):
   """
   Predict the number of color structures
   for F quark-anti-quark pairs and G gluons.
   """
   # This is Equation (58) in my thesis:
   if G <= 0:
      # F factorial
      return golem.util.tools.factorial(F)
   else:
      return num_colors(F+1, G-1) - num_colors(F, G-1)
