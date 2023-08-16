#!/usr/bin/env python3
# vim: ts=3:sw=3
import os
try:
  from distutils.core import setup
  from distutils.sysconfig import get_config_vars
  from distutils.command.build_py import build_py as _build_py
  from distutils.command.install_scripts import install_scripts as _install_scripts
  from distutils.command.install import install as _install
  from distutils.command.install_data import install_data as _install_data
  from distutils.util import change_root as _change_root
  from distutils import log
except:
  from setuptools import setup
  from sysconfig import get_config_vars
  from setuptools.command.build_py import build_py as _build_py
  from setuptools.command.install_scripts import install_scripts as _install_scripts
  from setuptools.command.install import install as _install
  from setuptools._distutils.command.install_data import install_data as _install_data
  import logging as log
#From https://github.com/pypa/distutils/blob/main/distutils/util.py
  def _change_root(new_root, pathname):
    """Return 'pathname' with 'new_root' prepended.  If 'pathname' is
    relative, this is equivalent to "os.path.join(new_root,pathname)".
    Otherwise, it requires making 'pathname' relative and then joining the
    two, which is tricky on DOS/Windows and Mac OS.
    """
    if os.name == 'posix':
        if not os.path.isabs(pathname):
            return os.path.join(new_root, pathname)
        else:
            return os.path.join(new_root, pathname[1:])

    elif os.name == 'nt':
        (drive, path) = os.path.splitdrive(pathname)
        if path[0] == '\\':
            path = path[1:]
        return os.path.join(new_root, path)


import os.path
import os
import re
import fnmatch
import fileinput

def get_git_revision():
	# The revision string must be a hexadecimal integer smaller than 2**31.
	# GOLEM_REVISION will be defined as this number later on.
	import subprocess
	desired_length = 7
	try:
		revision = subprocess.check_output([
			"git", "--git-dir=.git", "rev-parse", "--short=%d" % desired_length, "HEAD"
		]).decode("utf-8").strip()
		assert len(revision) == desired_length
		return revision
	except (FileNotFoundError, subprocess.CalledProcessError):
		# No git or no .git; we must be in a release tarball;
		# lets try to extract the revision from PKG-INFO.
		try:
			with open("PKG-INFO", "r") as f:
				for line in f:
					if line.startswith("Version: "):
						if "-" in line:
							return re.search('gosam-([0-9.]*)-([a-z,0-9]*)',line).group(2)
					if line.startswith("Download-URL: "):
						if "-" in line:
							return re.search('gosam-([0-9.]*)-([a-z,0-9]*)',line).group(2)
			raise Exception("The git repository is missing and PKG-INFO has no version")
		except FileNotFoundError:
			raise Exception("Neither the git repository nor the PKG-INFO file exist")

VERSION = "2.1.1"
GIT_REVISION = get_git_revision()
TAR_VERSION = "%s-%s" % (VERSION,GIT_REVISION)


INFO = {
		'name': 'gosam',
		'version': VERSION,
		'author': 'The GoSam (Golem and Samurai) Collaboration',
		'author_email': 'gosam@hepforge.org',
		'maintainer': 'The GoSam Collaboration',
		'maintainer_email': 'gosam@hepforge.org',
		'url': 'http://projects.hepforge.org/gosam/',
		'download_url': 
		'http://projects.hepforge.org/gosam/downloads/gosam-%s.tar.gz' %
			TAR_VERSION,
		'description': 'GoSam, An Automated One-Loop Matrix Element Generator',
		'long_description': """\
				GoSam is a matrix element generator for one-loop
				amplitudes in quantum field theories.
				""",
		'license': "GPLv3+",
		'platforms': ["POSIX"],
		'classifiers': [
			"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Intended Audience :: Developers",
			"Intended Audience :: Science/Research",
			"Natural Language :: English",
			"Operating System :: POSIX",
			"Programming Language :: Fortran",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
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
			"templates/sum",
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
				",".join([s.strip() for s in VERSION.split(".")]))
		f.write("GOLEM_REVISION = '%s'\n" % GIT_REVISION)
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
			"import sys",
			"sys.path=sys.path[:1] + " + repr([py_path]) + " + sys.path[1:]",
			"## end of 'added by setup.py'",""])
		logs=[]
		for line in fileinput.input(installed_scripts,inplace=1):
			if line.startswith("### [line replaced by setup.py"):
				logs.append("Patching " + fileinput.filename())
				line=replace_text
			print(line, end='') # redirected to fileinput
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
			'src/python/golem/gosam-config.py',
			'src/python/golem/gosam.py'
		],
		cmdclass={'build_py': build_py,
			'install_scripts':install_scripts,
			'install_data':install_data,
			'install':install},
		data_files=my_data_files,
		**INFO
	)
