
import os.path
import golem

def golem_path(*dir):
	"""
	Calculates the path where Golem is installed.
	"""

	try:
		from golem.installation import DATA_DIR
		return os.path.join(DATA_DIR, *dir)
	except ImportError:
		# This means we work with the sources rather than
		# from the installed version.
		src_path = golem.__path__[0]
		for p in ['golem', 'python', 'src']:
			src_path, tail = os.path.split(src_path)
			assert(tail == p)
		return os.path.join(src_path, *dir)

def get_homedir():
	"""
	Try to determin the user's home directory.

	There seems to be no better solution (currently, at least).
	"""
	homedir = os.path.expanduser('~')

	# ...works on at least windows and linux. 
	# In windows it points to the user's folder 
	#  (the one directly under Documents and Settings, not My Documents)

	# In windows, you can choose to care about local versus roaming profiles.
	# You can fetch the current user's through PyWin32.
	#
	# For example, to ask for the roaming 'Application Data' directory:
	# (CSIDL_APPDATA asks for the roaming, CSIDL_LOCAL_APPDATA for the local one)
	# (See microsoft references for further CSIDL constants)
	try:
		from win32com.shell import shellcon, shell            
		homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
	except ImportError: # quick semi-nasty fallback for non-windows/win32com case
		homedir = os.path.expanduser("~")

	return homedir

