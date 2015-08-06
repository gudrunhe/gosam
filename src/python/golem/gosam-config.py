#!/usr/bin/env python
# vim:ts=3:sw=3:expandtab
import sys

### [line replaced by setup.py - do not delete]

from golem.util.config import Configurator, OPTIONAL, REQUIRED
from golem.util.find_libpaths import find_libraries, components

if __name__ == "__main__":

   hints = {}

   outfile = None
   
   for arg in sys.argv[1:]:
      if arg.startswith("--with-"):
         tmp = arg[7:]
         if "=" in tmp:
            name, value = tmp.split("=", 1)
            hints[name.strip()] = value.strip()
         pass
      elif arg.startswith("--enable-"):
         tmp = arg[9:]
         if tmp not in components:
            components[tmp] = OPTIONAL

      elif arg.startswith("--disable-"):
         tmp = arg[10:]
         if tmp in components:
            if components[tmp] == OPTIONAL:
               del components[tmp]
            else:
               print("%r cannot be disabled" % tmp)
               sys.exit(-2)
      else:
         outfile = arg

   cdict, config = find_libraries(hints, return_config=True)

   if outfile is None:
      f = sys.stdout
   else:
      f = open(outfile, "w")

   keys = sorted(cdict.keys())
   for key in keys:
      value = cdict[key]
      f.write("%s=%s\n" % (key, value))

   if outfile is not None:
      f.close()
      config.message("Configuration has been written to %r" % outfile)
