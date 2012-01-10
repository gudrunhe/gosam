# vim: ts=3:sw=3
import golem
import golem.util.parser
from golem.util.config import Properties

class OLPTemplate(golem.util.parser.Template):
	"""
	Template used to generate files for the Les Houches One-Loop interface.
	"""

	def init_contract(self, contract_file):
		self._contract_file = contract_file
		self._subprocesses = None
		self._pstack = []

	def init_channels(self, subprocesses):
		self._subprocesses = subprocesses

	def subprocesses(self, *args, **opts):
		if "prefix" in opts:
			prefix = opts["prefix"]
		else:
			prefix = ""
		first_name = self._setup_name("first", prefix + "is_first", opts)
		last_name = self._setup_name("last", prefix + "is_last", opts)
		id_name = self._setup_name("id", prefix + "id", opts)
		index_name = self._setup_name("index", prefix + "index",	opts)
		path_name = self._setup_name("path", prefix + "path", opts)
		name_name = self._setup_name("var", prefix + "$_", opts)
		numlegs_name = self._setup_name("num_legs", prefix + "num_legs", opts)
		numhelis_name = self._setup_name("num_helicities",
				prefix + "num_helicities", opts)

		last = len(self._subprocesses) - 1
		for index, subprocess in enumerate(self._subprocesses):
			props = Properties()
			props[first_name] = (index == 0)
			props[last_name] = (index == last)

			props[index_name] = index 
			props[id_name] = int(subprocess)
			props[name_name] = str(subprocess)
			props[path_name] = subprocess.process_path
			props[numlegs_name] = subprocess.num_legs
			props[numhelis_name] = subprocess.num_helicities

			self._pstack.append(subprocess)
			yield props
			self._pstack.pop()

	def crossings(self, *args, **opts):
		if "prefix" in opts:
			prefix = opts["prefix"]
		else:
			prefix = ""
		first_name = self._setup_name("first", prefix + "is_first", opts)
		last_name = self._setup_name("last", prefix + "is_last", opts)
		id_name = self._setup_name("id", prefix + "id", opts)
		index_name = self._setup_name("index", prefix + "index",	opts)
		name_name = self._setup_name("var", prefix + "$_", opts)
		channels_name = self._setup_name("channels", prefix + "channels", opts)

		include_self = "include-self" in args

		if len(self._pstack) == 0:
			raise TemplateError(
					"[% @for crossings %] outside [% @for subprocesses %]")

		subprocess = self._pstack[-1]

		ids = subprocess.getIDs()
		if not include_self:
			ids.remove(int(subprocess))

		last = len(ids) - 1
		for index, id in enumerate(ids):
			props = Properties()
			props[first_name] = (index == 0)
			props[last_name] = (index == last)
			props[index_name] = index 

			props[id_name] = id
			props[name_name] = subprocess.ids[id]
			props[channels_name] = subprocess.channels[id]

			yield props

