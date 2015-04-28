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
import math

__all_olp_options__ = {}
__olp_lower_case__ = {}
__required_olp_options__ = set()
__required_olp_options_default__ = {} # called with default value if not present

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

def required_olp_option_default(default):
	def wrap(f):
		name = f.__name__
		__olp_lower_case__[name.lower()] = name
		__all_olp_options__[name] = f
		def wrapped_f(*args):
			f(default,*args)
		__required_olp_options_default__[name]=wrapped_f
		return f
	return wrap


@optional_olp_option
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
def ParameterCard(values, conf, ignore_case):
	file_name = " ".join(values)
	conf["olp.modelfile"] = file_name
	if os.path.exists(file_name):
		return __value_OK__
	else:
		return __value_ERR__ + "SLHA file does not exist."

@optional_olp_option
def SubdivideSubprocess(values, conf, ignore_case):
	supported_values = ["yes", "no", "true", "false"]
	return expect_one_keyword(values, conf, ignore_case,
		"olp.subdivide", supported_values)

@optional_olp_option
def Model(values, conf, ignore_case):
	if len(values)>=1 and values[0][:5].lower()=="ufo:/":
		file_name = os.path.abspath(" ".join(values)[5:].strip())
		conf["olp.ufomodel"] = file_name
		if os.path.exists(file_name) and os.path.isdir(file_name) \
				and os.path.exists(os.path.join(file_name, "__init__.py")):
			conf[golem.properties.model] = ["FeynRules", file_name]
			return __value_OK__
		else:
			warning("UFOModel which expands to '%s' does not exist." % file_name)
			return __value_ERR__ + "UFO model does not exist or is not a valid model."

	supported_values = ["SMdiag", "SMnondiag"]
	return expect_one_keyword(values, conf, ignore_case,
			"model", supported_values)

@optional_olp_option
def CouplingPower(values, conf, ignore_case):
	if len(values) > 2:
		return __value_ERR__ + "too many values."

	elif len(values) == 2:

		if values[0].lower() == 'qcd':
			try:
				power = int(values[1])
				conf["olp.alphaspower"] = str(power)
				return __value_OK__
			except ValueError:
				return __value_ERR__ + "non-integer value encountered."
		elif values[0].lower() == 'qed':
			try:
				power = int(values[1])
				conf["olp.alphapower"] = str(power)
				return __value_OK__
			except ValueError:
				return __value_ERR__ + "non-integer value encountered."
		else:
			return __value_ERR__ + "unrecognized type of CouplingPower."
	else:
		return __value_ERR__ + "too few arguments in CouplingPower."

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
def EWScheme(values, conf, ignore_case):
	if len(values) > 1:
		return __value_ERR__ + "too many values."
	supported_values = ["alphaGF","alpha0","alphaMZ","alphaRUN","alphaMSbar","OLPDefined"]
	ret=expect_one_keyword(values, conf, True,
		"olp.ewscheme", supported_values)
	return ret


@optional_olp_option
def WidthScheme(values, conf, ignore_case):
	if len(values) > 1:
		return __value_ERR__ + "too many values."
	supported_values = ["ComplexMass","FixedWidth"]
	ret=expect_one_keyword(values, conf, True,
		"olp.widthscheme", supported_values)
	if ret == "ComplexMass":
		warning("Complex Mass scheme not yet fully implemented!")
	return ret


@optional_olp_option
def AmplitudeType(values, conf, ignore_case):
	# Amplitudetype LoopInterference (alias: LIEffInterference) is an extension to BLHA2
	if len(values) > 1:
		return __value_ERR__ + "too many values."
	supported_values = ["Loop","Tree","ccTree","scTree","LoopInduced","LoopInterference","LIEffInterference"]
	ret=expect_one_keyword(values, conf, True,
		"olp.amplitudetype", supported_values)
	if hasattr(conf,"psp_chk_method_last"):
		# reset PSP_chk_method if necessary
		conf["PSP_chk_method"]=conf.psp_chk_method_last if conf.psp_chk_method_last else "Automatic"
	if ret.startswith(__value_OK__) and 'tree' in conf["olp.amplitudetype"].lower():
		conf["olp.no_tree_level"] = False
		conf["olp.no_loop_level"] = True
	if ret.startswith(__value_OK__) and 'loopinduced' in conf["olp.amplitudetype"].lower():
		conf["olp.no_tree_level"] = True
		conf["olp.no_loop_level"] = False
	elif ret.startswith(__value_OK__) and conf["olp.amplitudetype"].lower() in ["loopinterference","lieffinterference"]:
		conf["olp.no_tree_level"] = False
		conf["olp.no_loop_level"] = False
		if not conf["PSP_chk_method"] or conf["PSP_chk_method"].lower() in ["automatic","polerotation"]:
			conf.psp_chk_method_last=conf["PSP_chk_method"]
			conf["PSP_chk_method"]="LoopInduced"
	elif ret.startswith(__value_OK__) and 'loop' in conf["olp.amplitudetype"].lower():
		conf["olp.no_tree_level"] = False
		conf["olp.no_loop_level"] = False
	return ret

@optional_olp_option
def Precision(values, conf, ignore_case):
	if len(values) > 1:
		return __value_ERR__ + "requires one value."
	if (len(values)==1):
		try:
			prec=-math.log10(float(values[0]))
		except ValueError:
			return __value_ERR__ + "not positive float value encountered."
		conf["PSP_chk_th1"]=str(int(prec))
		conf["PSP_check"]=True
		return __value_OK__
	return __value_OK__ + " # WARNING: blank -> Precision check disabled."

@optional_olp_option
def AccuracyTarget(values, conf, ignore_case):
	if len(values) > 1:
		return __value_ERR__ + "requires one value."
	if (len(values)==1):
		try:
			prec=-math.log10(float(values[0]))
		except ValueError:
			return __value_ERR__ + "not positive float value encountered."
		conf["PSP_chk_th1"]=str(int(prec))
		conf["PSP_check"]=True
		return __value_OK__
	return __value_OK__ + " # WARNING: blank -> Precision check disabled."

@optional_olp_option
def DebugUnstable(values, conf, ignore_case):
	supported_values = ["yes", "no", "true", "false"]
	ret=expect_one_keyword(values, conf, True,
		"PSP_verbosity", supported_values)
	if ret==__value_OK__:
		if conf["PSP_verbosity"].lower() in ["yes","true"]:
			conf["PSP_verbosity"]="True"
		else:
			conf["PSP_verbosity"]="False"
	return ret

@optional_olp_option
def PrecisionCheck(values, conf, ignore_case):
   supported_values = ["disabled","off"] + golem.properties.config_PSP_chk_method._options
   ret=expect_one_keyword(values, conf, True,
                  "PSP_chk_method", supported_values)
   if ret==__value_OK__:
      if conf["PSP_chk_method"].lower() in ["disabled","off"]:
         conf["PSP_chk_method"]="Automatic"
         conf["PSP_check"]="False"
   return ret

@optional_olp_option
def ExcludedParticles(values, conf, ignore_case):
	excl=[]
	for p in values:
		try:
			excl.append(str(int(p)))
		except ValueError:
			return __value_ERR__ + " only PDG codes allowed."
	conf["__excludedParticles__"] = " ".join(excl);
	return __value_OK__


@optional_olp_option
def MassiveParticles(values, conf, ignore_case):
	if conf["__OLP_BLHA2__"]=="False" or conf["__OLP_BLHA2__"] is None:
		return __value_ERR__ + " option only allowed with InterfaceVersion BLHA2."
	massive=[]
	for p in values:
		try:
			massive.append(str(int(p)))
		except ValueError:
			return __value_ERR__ + " only PDG codes allowed."
	conf["__massiveParticles__"] = " ".join(massive);
	return __value_OK__

@optional_olp_option
def LightMassiveParticles(values, conf, ignore_case):
	return __value_ERR__ + " LightMassiveParticles not supported."

@optional_olp_option
def Extra(values, conf, ignore_case):
	if len(values)>1 and values[0] in __all_olp_options__:
		return __all_olp_options__[values[0]](values[1:], conf, ignore_case)
	return __value_OK__ + " # Ignored by OLP"

@required_olp_option_default(["BLHA1"])
def InterfaceVersion(values, conf, ignore_case):
	if len(values)!= 1:
			return __value_ERR__ + " unknown version"
	version=str(values[0]).upper()
	if version=="BLHA1":
		conf["__OLP_BLHA1__"]=True
		conf["__OLP_BLHA2__"]=False
		if not conf["extensions"] or not "olp_blha1" in conf["extensions"]:
			conf["extensions"]=(conf["extensions"] + "," if conf["extensions"]  else "") + "olp_blha1"
	elif version=="BLHA2":
		conf["__OLP_BLHA1__"]=False
		conf["__OLP_BLHA2__"]=True
		return __value_OK__
	return __value_ERR__ + "Interface version %s not supported" % version

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
        parameters = list(values)
        if len(values) > 0:
                if parameters[0] == "alpha_s":
                        #parameters.remove("alpha_s")
                        conf["olp.alphas"] = 1
                        conf["olp.parameters"] = parameters
                else:
                        conf["olp.alphas"] = 0
                        conf["olp.parameters"] = parameters
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

def process_olp_options(contract_file, conf, ignore_case, ignore_unknown, until_lineno=None, quiet=False):
	global __all_olp_options__, __olp_lower_case__, __required_olp_options__
	global __required_olp_options_default__
	backup = (__all_olp_options__,__olp_lower_case__, \
            __required_olp_options__, __required_olp_options_default__ )
	error_count = 0
	missing = set(__required_olp_options__)
	for lineno,name, values in contract_file.options_ordered():
		if until_lineno and lineno>until_lineno:
			break
		if ignore_case and name.lower() in __olp_lower_case__:
			key = __olp_lower_case__[name.lower()]
		elif name in __all_olp_options__:
			key = name
		elif ignore_unknown:
			contract_file.setPropertyResponseOrdered(name,
					__value_OK__ + " # Ignored by OLP",lineno)
			continue
		else:
			contract_file.setPropertyResponseOrdered(name,
					"Error: Unknown by OLP",lineno)
			if not quiet:
				warning("Line %s: Keyword '%s' unknown." % (name, lineno))
			error_count += 1
			continue

		if key in missing:
			missing.remove(key)
		if key in __required_olp_options_default__.keys():
			del __required_olp_options_default__[key]

		handler = __all_olp_options__[key]
		response = handler(values, conf, ignore_case)
		contract_file.setPropertyResponseOrdered(name, response,lineno)
		if not contract_file.isPropertyOk(name):
			if not quiet:
				warning("Line %s: Option '%s' failed. %s" % (lineno, name, response))
			error_count += 1
	for key in __required_olp_options_default__:
		handler=__required_olp_options_default__[key]
		handler(conf,ignore_case)

	if len(missing) > 0:
		error_count += 1
		if not quiet:
			warning("Missing required options: %s" % ", ".join(missing))
		raise OLPError("Missing required options: %s" % ", ".join(missing))

	( __all_olp_options__,__olp_lower_case__,
			__required_olp_options__, __required_olp_options_default__ ) = backup

	return error_count == 0
