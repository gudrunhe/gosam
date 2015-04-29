import sys
import os
import os.path
import imp
import StringIO
import hashlib

from time import gmtime, strftime

import golem.algorithms.mandelstam
import golem.algorithms.formfactors
import golem.util.config
import golem.util.tools
import golem.util.parser
import golem.properties
import golem.topolopy.functions
import golem.topolopy.objects
import golem.util.main_qgraf
import golem.util.constants as consts

import golem.templates.xmltemplates

from golem.util.path import golem_path, gosam_contrib_path
from golem.util.tools import copy_file, \
		debug, message, warning, \
		generate_particle_lists

from golem.util.config import GolemConfigError

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_qgraf import *
from golem.installation import GOLEM_VERSION, GOLEM_REVISION



def run_reduze(conf):
  pass  
