#!/usr/bin/env python
# vim: ts=3:sw=3

from distutils.core import setup
from distutils.sysconfig import get_config_vars
from distutils.command.build_py import build_py as _build_py

import os.path
import os
import fnmatch

VERSION = "1.0"
INFO = {
		'name': 'gosam',
		'version': VERSION,
		'author': 'The GoSam (Golem and Samurai) Collaboration',
		'author_email': 'gosam@hepforge.org',
		'maintainer': 'Thomas Reiter',
		'maintainer_email': 'reiterth@mpp.mpg.de',
		'url': 'http://projects.hepforge.org/gosam/',
		'download_url': 
		'http://projects.hepforge.org/gosam/downloads/gosam-%s.tar.gz' %
			VERSION,
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
				",".join(map(lambda s: s.strip(), INFO["version"].split("."))))

		f.close()

	def run(self):
		self.create_installation_py()
		_build_py.run(self)

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
		cmdclass={'build_py': build_py},
		data_files=my_data_files,
		**INFO
	)
