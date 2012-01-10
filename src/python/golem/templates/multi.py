# vim: ts=3:sw=3:expandtab

import imp
import os.path

from golem.util.config import Properties
from golem.util.parser import Template, TemplateError
import golem.util.path
import golem.properties

import golem.templates.kinematics
import golem.templates.parameters
import golem.templates.factory

class MultiTemplate(Template):
   """
   Implements a template that allows to include files which are
   read by different Template classes
   """

   def setup(self, conf, opts):
      self._conf = conf
      self._opts = opts

   def _lookup(self, *args, **opts):
      name = self._remembered_name
      for option in golem.properties.properties:
         if name == option.getName():
            value = self._conf.getProperty(option)
            if option.getType() == list:
               # Yield elements of the list
               result = []
               if value is not None:
                  symbol_name = self._setup_name("name", "$_", opts)
                  first_name = self._setup_name("first", "is_first", opts)
                  last_name = self._setup_name("last", "is_last", opts)
                  index_name = self._setup_name("index", "index", opts)
                  if "shift" in opts:
                     base = int(opts["shift"])
                  else:
                     base = 0

                  props = Properties()
                  for i in range(len(value)):
                     props.setProperty(symbol_name, value[i])
                     props.setProperty(first_name, i == 0)
                     props.setProperty(last_name, i == len(value) - 1)
                     props.setProperty(index_name, i + base)
                     result.append(props)

               return result
            else:
               return self._conf.getProperty(option)
               
      return Template._lookup(self, name, *args, **opts)

   def include(self, *args, **opts):
      if len(args) != 1:
         raise TemplateError("[% include ... %] takes exactly one file name.")

      try:
         path = self._conf.getProperty(golem.properties.template_path)
         if path is None or len(path) == 0:
            path = golem.util.path.golem_path("templates")
         path = os.path.expandvars(path)
         path = os.path.expanduser(path)

         in_file = os.path.join(path, args[0])

         factory = golem.templates.factory.TemplateFactory()
         return factory.process(in_file, None, opts["class"],
               self._stack, self._conf, self._opts)
      except TemplateError as ex:
         raise TemplateError("In included file '%s': %s" % (
            args[0], ex))

