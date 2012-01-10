# vim: ts=3:sw=3:expandtab

def zero_loop(d):
   """
   Loops which cancel due to Furry's theorem.
   """
   return d.chord(QUARKS) == d.loopsize() and \
          d.loopsize() == 3 and \
          d.loopvertices([A], QUARKS, QUARKS) == 1 and \
          d.loopvertices([g], QUARKS, QUARKS) == 2
          
def v_floop(d):
   """
   Closed quark loops with gauge boson attached to the loop
   """
   return d.chord(QUARKS) == d.loopsize() and \
          d.loopvertices([Z,A], QUARKS, QUARKS) >= 1 \
          and not zero_loop(d)

def top_loop(d):
   return d.chord([T,Tbar]) == d.loopsize()

def b_loop(d):
   return d.chord([B,Bbar]) == d.loopsize()

def madloop_filter(d):
   return (not v_floop(d)) and (not top_loop(d)) and (not zero_loop(d))
