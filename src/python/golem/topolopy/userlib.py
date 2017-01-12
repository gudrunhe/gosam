# vim: ts=3:sw=3:expandtab

class _CurryFunctor:
   def __call__(self, d):
      pass

   def __add__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] + t[1])

   def __sub__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] - t[1])

   def __mul__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] * t[1])

   def __floordiv__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] // t[1])

   def __mod__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] % t[1])

   def __divmod__(self, b):
      return _CurryBinOp(self, b, lambda t: divmod(t[0], t[1]))

   def __pow__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0]**t[1])

   def __lshift__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] << t[1])

   def __rshift__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] >> t[1])

   def __and__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] & t[1])

   def __or__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] | t[1])

   def __xor__(self, b):
      return _CurryBinOp(self, b,
            lambda t: (t[0] and not t[1]) or (t[1] and not t[0]))

   def __eq__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] == t[1])

   def __lt__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] < t[1])

   def __le__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] <= t[1])

   def __gt__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] > t[1])

   def __ge__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] >= t[1])

   def __ne__(self, b):
      return _CurryBinOp(self, b, lambda t: t[0] != t[1])

   def __neg__(self):
      return _CurryUnOp(self, lambda a: -a)

   def __pos__(self):
      return _CurryUnOp(self, lambda a: +a)

   def __abs__(self):
      return _CurryUnOp(self, lambda a: abs(a))

   def __invert__(self):
      return _CurryUnOp(self, lambda a: ~a)

   def __complex__(self):
      return _CurryUnOp(self, lambda a: complex(a))
   
   def __int__(self):
      return _CurryUnOp(self, lambda a: int(a))

   def __long__(self):
      return _CurryUnOp(self, lambda a: long(a))

   def __float__(self):
      return _CurryUnOp(self, lambda a: float(a))

   def __oct__(self):
      return _CurryUnOp(self, lambda a: oct(a))

   def __hex__(self):
      return _CurryUnOp(self, lambda a: hex(a))

   def __str__(self):
      return _CurryUnOp(self, lambda a: str(a))

   def __repr__(self):
      return _CurryUnOp(self, lambda a: repr(a))

   def __len__(self):
      return _CurryUnOp(self, lambda a: len(a))

def _eval(arg, d):
   if isinstance(arg, _CurryFunctor):
      return arg(d)
   else:
      return arg

class _CurryBinOp(_CurryFunctor):
   def __init__(self, a, b, op):
      self.a = a
      self.b = b
      self.op = op

   def __call__(self, d):
      a = _eval(self.a, d)
      b = _eval(self.b, d)
      op = self.op

      return op((a, b))

class _CurryUnOp(_CurryFunctor):
   def __init__(self, a, op):
      self.a = a
      self.op = op

   def __call__(self, d):
      a = _eval(self.a, d)
      op = self.op

      return op(a)

class _CurryNullOp(_CurryFunctor):
   def __init__(self, op):
      self.op = op

   def __call__(self, d):
      op = self.op

      return op(d)

class AND(_CurryFunctor):
   def __init__(self, *args):
      self.args = args

   def __call__(self, d):
      for arg in self.args:
         if not _eval(arg, d):
            return False
      return True

class OR(_CurryFunctor):
   def __init__(self, *args):
      self.args = args

   def __call__(self, d):
      for arg in self.args:
         if _eval(arg, d):
            return True
      return False

class NOT(_CurryFunctor):
   def __init__(self, arg):
      self.arg = arg

   def __call__(self, d):
      return not _eval(self.arg, d)

class VERTICES(_CurryFunctor):
   def __init__(self, *args, **opts):
      self.args = args
      self.opts = opts

   def __call__(self, d):
      return d.vertices(*(self.args), **(self.opts))

class LOOPVERTICES(_CurryFunctor):
   def __init__(self, *args, **opts):
      self.args = args
      self.opts = opts

   def __call__(self, d):
      return d.loopvertices(*(self.args), **(self.opts))

class IPROP(_CurryFunctor):
   def __init__(self, *args, **opts):
      self.args = args
      self.opts = opts

   def __call__(self, d):
      return d.iprop(*(self.args), **(self.opts))

class CHORD(_CurryFunctor):
   def __init__(self, *args, **opts):
      self.args = args
      self.opts = opts

   def __call__(self, d):
      return d.chord(*(self.args), **(self.opts))

class BRIDGE(_CurryFunctor):
   def __init__(self, *args, **opts):
      self.args = args
      self.opts = opts

   def __call__(self, d):
      return d.bridge(*(self.args), **(self.opts))

class NFGEN(_CurryFunctor):
   def __init__(self, *quarks):
      self.quarks = quarks  

   def __call__(self, d):
      global QUARKS
      s_keep  = d.chord(self.quarks)
      s_all   = d.chord(QUARKS)
      if s_all == d.loopsize():
         return s_keep == s_all
      else:
         return True

LOOPSIZE  = _CurryNullOp(lambda d: d.loopsize())
RANK      = _CurryNullOp(lambda d: d.rank(True))
RANK0     = _CurryNullOp(lambda d: d.rank(False))
MQSE      = _CurryNullOp(lambda d: d.isMassiveQuarkSE())
SCALELESS = _CurryNullOp(lambda d: d.isScaleless())
SIGN      = _CurryNullOp(lambda d: d.sign())
NF        = _CurryNullOp(lambda d: d.isNf())
QBMASSES  = _CurryNullOp(lambda d: d.QuarkBubbleMasses())
TRUE      = _CurryNullOp(lambda d: True)
FALSE     = _CurryNullOp(lambda d: False)
