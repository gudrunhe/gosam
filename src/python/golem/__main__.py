# vim: ts=3:sw=3:expandtab

import sys
import golem.app.main as main
import golem.app.olp as olp

if __name__ == "__main__":
   argv = sys.argv[:]

   if "--olp" in argv[1:]:
      argv.remove("--olp")
      olp.main(argv)
   else:
      main.main(argv)
