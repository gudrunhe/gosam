# vim: ts=3:sw=3:expandtab
import feyngraph as fg

QUARKS = ["U", "D", "S", "C", "B", "T", "Ubar", "Dbar", "Sbar", "Cbar", "Bbar", "Tbar"]

def zero_loop(d: fg.Diagram):
   """
   Loops which cancel due to Furry's theorem.
   """
   return d.loopsize(0) == 3 and \
          all(p.particle().name() in QUARKS for p in d.chord(0)) and \
          sum(v.match_particle_combinations([["A"], QUARKS, QUARKS]) for v in d.loop_vertices(0)) == 1 and \
          sum(v.match_particle_combinations([["g"], QUARKS, QUARKS]) for v in d.loop_vertices(0)) == 2

def v_floop(d: fg.Diagram):
   """
   Closed quark loops with gauge boson attached to the loop
   """
   return sum(p.particle().name() in QUARKS for p in d.chord(0)) == d.loopsize(0) and \
          any(v.match_particle_combinations([["Z", "A"], QUARKS, QUARKS]) for v in d.loop_vertices(0)) \
          and not zero_loop(d)

def top_loop(d):
   return sum(p.particle().name() in ["T", "Tbar"] for p in d.chord(0)) == d.loopsize(0)

def b_loop(d: fg.Diagram):
   return sum(p.particle().name() in ["B", "Bbar"] for p in d.chord(0)) == d.loopsize(0)

def madloop_filter(d: fg.Diagram):
   return bridge_filter(d) and (not v_floop(d)) and (not top_loop(d)) and (not zero_loop(d))

def bridge_filter(d: fg.Diagram):
    return any(p.particle().name() in ["Z", "A"] for p in d.bridges())
