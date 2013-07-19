# vim: ts=3:sw=3

# NOTE:
# In order to distinguish standardized options from Golem extensions
# we prefix everything that has not been agreed on by "GX_".
# Users should be aware that those options might disappear or be renamed
# in the future.

import os.path
import golem.properties
from golem.util.olp_objects import OLPError
from golem.util.tools import warning

__all_olp_options__ = {}
__olp_lower_case__ = {}
__required_olp_options__ = set()

__value_OK__ = "OK"
__value_ERR__ = "Error:"

def required_olp_option(f):
	name = f.__name__
	__olp_lower_case__[name.lower()] = name
	__all_olp_options__[name] = f
	__required_olp_options__.add(name)

def optional_olp_option(f):
	name = f.__name__
	__olp_lower_case__[name.lower()] = name
	__all_olp_options__[name] = f

@required_olp_option
def MatrixElementSquareType(values, conf, ignore_case):
	err_flag = False
	NoTreeLevel = "GX_NoTreeLevel"

	supported_values = ["CHsummed", "CHaveraged",
			"Csummed", "Caveraged",
			"Hsummed", "Haveraged","CHaveragedSymm","CHsummedSymm", NoTreeLevel]

	lower_case_values = {}
	for name in supported_values:
		lower_case_values[name.lower()] = name

	checked_values = []
	for value in values:
		if ignore_case:
			lvalue = value.lower()
			if lvalue in lower_case_values:
				checked_values.append(lower_case_values[lvalue])
			else:
				err_flag = True
		elif value in supported_values:
			checked_values.append(value)
		else:
			err_flag = True

	col_avg = True
	hel_avg = True
	sym_fac = False
	no_tree = False

	if NoTreeLevel in checked_values:
		no_tree = True
		checked_values = filter(lambda x: x != NoTreeLevel, checked_values)

	if "CHsummed" in checked_values:
		if len(checked_values) > 1:
			err_flag = True
		else:
			col_avg = False
			hel_avg = False
	elif "CHaveraged" in checked_values:
		if len(checked_values) > 1:
			err_flag = True
		else:
			sym_fac = True
	elif "CHaveragedSymm" in checked_values:
		if len(checked_values) > 1:
			err_flag = True
		else:
			sym_fac = True
	elif "CHsummedSymm" in checked_values:
		if len(checked_values) > 1:
			err_flag = True
		else:
			col_avg = False
			hel_avg = False
			sym_fac = True
	else:
		if len(checked_values) != 2:
			err_flag = True
		if "Csummed" in checked_values:
			col_avg = False
		elif "Caveraged" in checked_values:
			pass
		else:
			err_flag = True

		if "Hsummed" in checked_values:
			hel_avg = False
		elif "Haveraged" in checked_values:
			pass
		else:
			err_flag = True

	if err_flag:
		return __value_ERR__ + " Illegal value.\n" + \
				"#  Allowed values are: \n" + \
				"#    CHsummed\n" + \
				"#    CHaveraged\n" + \
				"#    Csummed Haveraged\n" + \
				"#    Hsummed Caveraged\n" + \
				"#    CHsummedSymm\n" + \
				"#    GX_NoTreeLevel\n"
	else:
		conf["olp.include_color_average"] = col_avg
		conf["olp.include_helicity_average"] = hel_avg
		conf["olp.include_symmetry_factor"] = sym_fac
		conf["olp.no_tree_level"] = no_tree

		return __value_OK__

@required_olp_option
def IRregularisation(values, conf, ignore_case):
	err_flag = False
	supported_values = ["tHV", "DRED", "CDR"]
	return expect_one_keyword(values, conf, ignore_case,
		"olp.irregularisation", supported_values)

@optional_olp_option
def IRsubtractionMethod(values, conf, ignore_case):
	err_flag = False
	supported_values = ["None"]
	return expect_one_keyword(values, conf, ignore_case,
		"olp.irsubtractionmethod", supported_values)

@optional_olp_option
def MassiveParticleScheme(values, conf, ignore_case):
	err_flag = False
	supported_values = ["OnShell"]
	return expect_one_keyword(values, conf, ignore_case,
		"olp.massiveparticlescheme", supported_values)

@optional_olp_option
def OperationMode(values, conf, ignore_case):
	supported_values = ["CouplingsStrippedOff"]

	return expect_many_keywords(values, conf, ignore_case,
		"olp.operationmode", supported_values)

@required_olp_option
def CorrectionType(values, conf, ignore_case):
	supported_values = ["QCD", "EW"]
	return expect_one_keyword(values, conf, ignore_case,
		"olp.correctiontype", supported_values)

@optional_olp_option
def ModelFile(values, conf, ignore_case):
	file_name = " ".join(values)
	conf["olp.modelfile"] = file_name
	if os.path.exists(file_name):
		return __value_OK__
	else:
		return __value_ERR__ + "model file does not exist."

@optional_olp_option
def SubdivideSubprocess(values, conf, ignore_case):
	supported_values = ["yes", "no", "true", "false"]
	return expect_one_keyword(values, conf, ignore_case,
		"olp.subdivide", supported_values)

@optional_olp_option
def AlphasPower(values, conf, ignore_case):
	if len(values) > 1:
		return __value_ERR__ + "too many values."
	elif len(values) == 1:
		try:
			power = int(values[0])
			conf["olp.alphaspower"] = str(power)
			return __value_OK__
		except ValueError:
			return __value_ERR__ + "non-integer value encountered."
	else:
		warning("AlphasPower left blank in order file.")
		return __value_OK__ + " # WARNING: should not be blank."

@optional_olp_option
def AlphaPower(values, conf, ignore_case):
	if len(values) > 1:
		return __value_ERR__ + "too many values."
	elif len(values) == 1:
		try:
			power = int(values[0])
			conf["olp.alphapower"] = str(power)
			return __value_OK__
		except ValueError:
			return __value_ERR__ + "non-integer value encountered."
	else:
		warning("AlphaPower left blank in order file.")
		return __value_OK__ + " # WARNING: should not be blank."


@optional_olp_option
def UFOModel(values, conf, ignore_case):
	"""
	NOT YET PART OF THE STANDARD
	"""
	file_name = os.path.abspath(" ".join(values).strip())
	conf["olp.ufomodel"] = file_name
	if os.path.exists(file_name) and os.path.isdir(file_name) \
			and os.path.exists(os.path.join(file_name, "__init__.py")):

		conf[golem.properties.model] = ["FeynRules", file_name]
		return __value_OK__
	else:
		warning("UFOModel which expands to '%s' does not exist." % file_name)
		return __value_ERR__ + "UFO model does not exist or is not a valid model."

@optional_olp_option
def Parameters(values, conf, ignore_case):
	"""
	NOT YET PART OF THE STANDARD
	"""
	#conf["olp.parameters"] = values
	if values[0] == "alpha_s":
		values.remove("alpha_s")		
		conf["olp.alphas"] = 1
		conf["olp.parameters"] = values
	else:
		conf["olp.alphas"] = 0
		conf["olp.parameters"] = values
		warning("WARNING: by convention the first parameter should be 'alpha_s.'")
		return __value_OK__ + "# WARNING: by convention the first parameter should be 'alpha_s'."
	return __value_OK__
	
def expect_one_keyword(values, conf, ignore_case, key, supported_values):
	err_flag = False

	lower_case_values = {}
	for name in supported_values:
		lower_case_values[name.lower()] = name

	checked_values = []
	for value in values:
		if ignore_case:
			lvalue = value.lower()
			if lvalue in lower_case_values:
				checked_values.append(lower_case_values[lvalue])
			else:
				err_flag = True
		elif value in supported_values:
			checked_values.append(value)
		else:
			err_flag = True

	if err_flag:
		if len(supported_values) > 1:
			str_val = ", ".join(supported_values[:-1])
			str_val += " and " + supported_values[-1]
		elif len(supported_values) == 0:
			str_val = ""
		else:
			str_val = supported_values[0]
		return __value_ERR__ + " Unsupported values encountered.\n" + \
				"# Supported values: " + str_val

	if len(checked_values) != 1:
		return __value_ERR__ + " Expected exactly one value."

	conf[key] = checked_values[0]
	return __value_OK__

def expect_many_keywords(values, conf, ignore_case, key, supported_values):
	err_flag = False

	lower_case_values = {}
	for name in supported_values:
		lower_case_values[name.lower()] = name

	checked_values = []
	for value in values:
		if ignore_case:
			lvalue = value.lower()
			if lvalue in lower_case_values:
				checked_values.append(lower_case_values[lvalue])
			else:
				err_flag = True
		elif value in supported_values:
			checked_values.append(value)
		else:
			err_flag = True

	if err_flag:
		if len(supported_values) > 1:
			str_val = ", ".join(supported_values[:-1])
			str_val += " and " + supported_values[-1]
		elif len(supported_values) == 0:
			str_val = ""
		else:
			str_val = supported_values[0]
		return __value_ERR__ + " Unsupported values encountered.\n" + \
				"# Supported values: " + str_val

	conf[key] = ",".join(checked_values)

	return __value_OK__

def process_olp_options(contract_file, conf, ignore_case, ignore_unknown):
	error_count = 0
	missing = set(__required_olp_options__)
	for name, values in contract_file.options():
		if ignore_case and name.lower() in __olp_lower_case__:
			key = __olp_lower_case__[name.lower()]
		elif name in __all_olp_options__:
			key = name
		elif ignore_unknown:
			contract_file.setPropertyResponse(name,
					__value_OK__ + " # Ignored by OLP")
			continue
		else:
			contract_file.setPropertyResponse(name,
					"Error: Unknown by OLP")
			error_count += 1
			continue

		if key in missing:
			missing.remove(key)

		handler = __all_olp_options__[key]
		response = handler(values, conf, ignore_case)
		contract_file.setPropertyResponse(name, response)
		if not contract_file.isPropertyOk(name):
			error_count += 1

	if len(missing) > 0:
		error_count += 1
		raise OLPError("Missing required options: %s" % ", ".join(missing))
	return error_count == 0
