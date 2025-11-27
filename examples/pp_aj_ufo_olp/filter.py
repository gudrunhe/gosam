import feyngraph as fg

QUARKS = ["u", "d", "s", "c", "b", "t", "u~", "d~", "s~", "c~", "b~", "t~"]

def furry_zero(d: fg.Diagram):
   """
   Loops which cancel due to Furry's theorem.
   """
   test = d.loopsize(0) != 3 or \
          not all(p.particle().name() in QUARKS for p in d.chord(0)) or \
          not (sum(v.match_particle_combinations([["a"], QUARKS, QUARKS]) for v in d.loop_vertices(0)) == 1 or \
          sum(v.match_particle_combinations([["g"], QUARKS, QUARKS]) for v in d.loop_vertices(0)) == 2)
   return test 
