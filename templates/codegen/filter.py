# vim: ts=3:sw=3:expandtab

import re


class _OutputFilter:
   def __init__(self, output, **opts):
      self.options = opts
      self.out = output
      self.setup()

   def reset(self, output):
      if isinstance(self.out, _OutputFilter):
         self.out.reset(output)
      else:
         self.out = output
      self.setup()
      return self

   def setup(self):
      pass

   def filter(self, chunk):
      return chunk

   def write(self, arg):
      self.out.write(self.filter(arg))

   def close(self):
      self.out.close()

class Fortran90(_OutputFilter):
   def setup(self):
      if "width" in self.options:
         self.width = int(self.options["width"])
         self.restrict_length = True
         self.indent = ""
         self.column = 0
         self.indenting = True

         self.indent_re = re.compile(r"^\s*")
      else:
         self.restrict_length = False

      if "ts" in self.options:
         self.tabsize = int(self.options["ts"])
      else:
         self.tabsize = -1

   
   def filter(self, chunk):
      if self.tabsize >= 0:
         xchunk = chunk.expandtabs(self.tabsize)
      else:
         xchunk = chunk

      if self.restrict_length:
         result = ""
         for line in xchunk.splitlines(True):
            if line.endswith("\n") or line.endswith("\r"):
               buf = line[:-1].rstrip()
               endl = line[-1:]
            else:
               buf = line
               endl = ""
            ll = len(buf)
            if self.indenting:
               ind = buf[:self.indent_re.search(buf).end()]
               self.indent += ind
               if len(ind) < ll:
                  self.indenting = False
            comment = False
            try:
                  if buf.lstrip(' ')[0] == '!':
                     comment = True
            except:
                  continue
            while self.column + ll > self.width:
               last = max(self.width - self.column - 1, 1)
               result += buf[:last]
               buf = buf[last:]
               ll = len(buf)
               if len(buf) > 0:
                  if comment == True:
                     result += " &\n" + self.indent  + "! &"
                     self.column = len(self.indent) + 1
                  else:
                     result += "&\n" + self.indent  + "&"
                     self.column = len(self.indent) + 1
            result += buf

            if endl == "":
               self.column += len(buf)
            else:
               result += endl
               self.column = 0
               self.indenting = True
               self.indent = ""
         return result
      else:
         return xchunk

class ExpandTab(_OutputFilter):
   def setup(self):
      if "ts" in self.options:
         self.tabsize = int(self.options["ts"])
      else:
         self.tabsize = 3

   def filter(self, chunk):
      if self.tabsize >= 0:
         return chunk.expandtabs(self.tabsize)
      else:
         return chunk

def FilterFactory(name, output, **opts):
   if name == "Fortran90":
      return Fortran90(output, **opts)
   if name == "ExpandTab":
      return ExpandTab(output, **opts)
   else:
      return None

