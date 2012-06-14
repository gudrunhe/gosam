#!/usr/bin/env python
# vim: ts=3:sw=3

from distutils.core import setup
from distutils.sysconfig import get_config_vars
from distutils.command.build_py import build_py as _build_py
from distutils.command.install_scripts import install_scripts as _install_scripts
from distutils.command.install import install as _install
from distutils.command.install_data import install_data as _install_data
from distutils.util import change_root as _change_root
from distutils import log

import os.path
import os
import fnmatch
import fileinput

VERSION = "1.0"
SVN_REVISION = "$Rev$"
TAR_VERSION = "%s-%d" % (
		VERSION,
		int(SVN_REVISION.replace("$Rev:", "").replace("$", "")))


INFO = {
		'name': 'gosam',
		'version': TAR_VERSION,
		'author': 'The GoSam (Golem and Samurai) Collaboration',
		'author_email': 'gosam@hepforge.org',
		'maintainer': 'Thomas Reiter',
		'maintainer_email': 'reiterth@mpp.mpg.de',
		'url': 'http://projects.hepforge.org/gosam/',
		'download_url': 
		'http://projects.hepforge.org/gosam/downloads/gosam-%s.tar.gz' %
			TAR_VERSION,
		'description': 'GoSam, An Automated One-Loop Matrix Element Generator',
		'long_description': """\
				GoSam is a matrix element generator for one-loop
				amplitudes in quantum field theories.
				""",
		'license': "License :: OSI Approved :: GNU General Public License (GPL)",
		'platforms': "POSIX",
		'classifiers': [
			"License :: OSI Approved :: GNU General Public License (GPL)",
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Intended Audience :: Developers",
			"Intended Audience :: Science/Research",
			"Natural Language :: English",
			"Operating System :: POSIX",
			"Programming Language :: Fortran",
			"Programming Language :: Python 2.5",
			"Topic :: Scientific/Engineering :: Physics"
		],
		'provides': ["gosam (%s)" % VERSION]
}

DATA_DIRS = [
			"templates",
			"templates/codegen",
			"templates/common",
			"templates/doc",
			"templates/helicity",
			"templates/matrix",
			"olp/templates",
			"models",
			"src/form",
			"haggies"
]

DATA_EXCLUDE = [
	"*~",
	".svn*",
	"*.pyc",
	"*.pyo",
]

def getDataFiles(data_dir):
	global DATA_EXCLUDE
	lst = []

	for file in os.listdir(data_dir):
		exclude = False
		for exc_pattern in DATA_EXCLUDE:
			if fnmatch.fnmatch(file, exc_pattern) or \
					os.path.isdir(os.path.join(data_dir, file)):
				exclude = True
				break
		if not exclude:
			lst.append(os.path.join(data_dir, file))
	return lst

class build_py(_build_py):

	def create_installation_py(self):
		dist = self.distribution
		inst = dist.get_command_obj("install_data")
		inst.initialize_options()
		inst.finalize_options()

		data_dir = os.path.join(inst.install_dir, "share", "golem")
		fname = self.get_module_outfile(
				self.build_lib, ["golem"], "installation")

		self.mkpath(os.path.dirname(fname))

		f = open(fname, "w")
		f.write("# vim: ts=3:sw=3:expandtab\n")
		f.write("DATA_DIR = %r\n" % data_dir)

		f.write("INFO = {")
		first = True
		for name, value in INFO.items():
			if first:
				first = False
				f.write("\n   ")
			else:
				f.write(",\n   ")
			f.write("%r: %r" % (name, value))
		f.write("\n}\n\n")
		f.write("GOLEM_VERSION = [%s]\n" %
				",".join(map(lambda s: s.strip(), VERSION.split("."))))
		f.write("GOLEM_REVISION = %d\n" %
				int(SVN_REVISION.replace("$Rev:", "").replace("$", "")))
		f.close()

	def run(self):
		self.create_installation_py()
		_build_py.run(self)

installed_scripts=[]

class install_scripts(_install_scripts):
	def run(self):
		global installed_scripts
		_install_scripts.run(self)
		installed_scripts=self.get_outputs()

orig_install_lib=None

class install_data(_install_data):
	def run(self):
		orig_root = self.root
		orig_install_dir = self.install_dir

		# circumvent self.root-ignored bug
		# by overwritting self.install_dir
		if self.root:
			self.install_dir = _change_root(self.root,self.install_dir)
			self.root=None

		_install_data.run(self)

		# restore
		self.root=orig_root
		self.install_dir=orig_install_dir



class install(_install):
	def run(self):
		_install.run(self)
		global orig_install_lib
		if orig_install_lib:
			py_path=orig_install_lib
		else:
			py_path=self.install_lib
		replace_text="\n".join([
			"## added by setup.py:",
			"import site",
			"site.addsitedir("+repr(py_path)+")",
			"## end of 'added by setup.py'",""])
		logs=[]
		for line in fileinput.input(installed_scripts,inplace=1):
			if line.startswith("### [line replaced by setup.py"):
				logs.append("Patching " + fileinput.filename())
				line=replace_text
			print line, # redirected to fileinput
		for message in logs:
			log.info(message)
	def change_roots (self, *names):
		global orig_install_lib
		orig_install_lib=self.install_lib
		_install.change_roots(self,*names)

if __name__ == "__main__":
	my_data_files=[]
	for dir in DATA_DIRS:
		target_dir = os.path.join("share", "golem", dir)
		files = getDataFiles(dir)
		my_data_files.append( (target_dir, files) )


	setup(
		packages=[
			'golem',
			'golem.algorithms',
			'golem.app',
			'golem.model',
			'golem.pyxo',
			'golem.templates',
			'golem.topolopy', 
			'golem.util'],
		package_dir={
			'golem': 'src/python/golem'
		},
		scripts=[
			'src/python/golem/golem-config.py',
			'src/python/golem/golem-init.py',
			'src/python/golem/golem-main.py',
			'src/python/golem/gosam.py'
		],
		cmdclass={'build_py': build_py,
			'install_scripts':install_scripts,
			'install_data':install_data,
			'install':install},
		data_files=my_data_files,
		**INFO
	)
