# vim: ts=3:sw=3:expandtab

import os
import shutil
import sys
import golem
import golem.util.tools
import golem.installation
import re

from golem.util.config import GolemConfigError
from golem.util.main_misc import fill_config

try:
    from multiprocess import Pool
except ModuleNotFoundError:
    Pool = None

import logging

logger = logging.getLogger(__name__)


class OLPSubprocess:
    def __init__(self, id, process_name, process_path, p_ini, p_fin, key, conf):
        self.id = id
        self.process_name = process_name
        self.process_path = process_path
        self.p_ini = p_ini
        self.p_fin = p_fin
        self.crossings = {}
        self.crossings_conf = {}
        self.crossings_p_ini = {}
        self.crossings_p_fin = {}
        self.ids = {id: process_name}
        self.channels = {}
        self.key = key
        self.conf = conf
        self.crossings_conf[id] = conf
        self.crossings_p_ini[id] = p_ini
        self.crossings_p_fin[id] = p_fin

        self.num_legs = len(p_ini) + len(p_fin)
        self.num_helicities = -1
        self.generated_helicities = []

    def addCrossing(self, id, process_name, p_ini, p_fin, conf):
        self.crossings[process_name] = "%s > %s" % (" ".join(map(str, p_ini)), " ".join(map(str, p_fin)))
        self.ids[id] = process_name
        self.crossings_conf[id] = conf
        self.crossings_p_ini[id] = p_ini
        self.crossings_p_fin[id] = p_fin

    def removeCrossing(self, id):
        self.crossings.pop(self.ids.pop(id))
        self.crossings_conf.pop(id)
        self.crossings_p_ini.pop(id)
        self.crossings_p_fin.pop(id)

    def clearCrossings(self):
        self.crossings = {}
        self.ids = {self.id: self.process_name}
        self.crossings_conf = {self.id: self.conf}
        self.crossings_p_ini = {self.id: self.p_ini}
        self.crossings_p_fin = {self.id: self.p_fin}

    def assignChannels(self, id, channels):
        self.channels[id] = channels

    def assignNumberHelicities(self, nh, gh):
        self.num_helicities = nh
        self.generated_helicities = gh

    def getkey(self):
        return list(self.key)

    def getIDs(self):
        return list(self.ids.keys())

    def getIDConf(self, id):
        return self.crossings_conf[id]

    def __str__(self):
        return self.process_name

    def __int__(self):
        return self.id

    def getPath(self, path=None):
        if path is None:
            return self.process_path
        else:
            return os.path.join(path, self.process_path)

    def getConf(self, conf, path, base=None):
        if base:
            subproc_conf = base.copy()
        else:
            subproc_conf = conf.copy()

        # subproc_conf.cache["model"] = conf.cache["model"]
        subproc_conf[golem.properties.process_name] = self.process_name
        subproc_conf[golem.properties.process_path] = self.getPath(path)
        subproc_conf[golem.properties.particles_in] = list(map(str, self.p_ini))
        subproc_conf[golem.properties.particles_out] = list(map(str, self.p_fin))
        if len(self.crossings) > 0:
            subproc_conf[golem.properties.crossings] = [
                "%s: %s" % (name, process) for name, process in list(self.crossings.items())
            ]

        return subproc_conf


def getSubprocess(olpname, id, inp, out, subprocesses, subprocesses_flav, model, use_crossings, conf):
    def getparticle(name):
        return golem.util.tools.interpret_particle_name(name, model)

    p_ini = list(map(getparticle, inp))
    p_fin = list(map(getparticle, out))

    s_ini = list(map(str, p_ini))
    s_fin = list(map(str, p_fin))

    if len(olpname) > 0:
        process_name = "%s_p%d_%s_%s" % (olpname, id, "".join(s_ini), "".join(s_fin))
    else:
        process_name = "p%d_%s_%s" % (id, "".join(s_ini), "".join(s_fin))
    process_name = process_name.lower()
    originalkey = tuple(sorted(s_ini + s_fin))

    key = get_sp_key(p_ini, p_fin, use_crossings, conf)

    if use_crossings:
        # look for existing compatible subprocesses
        for skey in subprocesses:
            if skey[: len(key)] == key and is_config_compatible(subprocesses[skey].conf, conf):
                key = skey
                break

    if key in subprocesses and use_crossings and is_config_compatible(subprocesses[key].conf, conf):
        sp = subprocesses[key]
        sp.addCrossing(id, process_name, p_ini, p_fin, conf)
        is_new = False
        adapt_config(subprocesses[key].conf, conf)
    else:
        i = 0
        # append digit to distinguish it from other subprocesses
        while key in subprocesses:
            key = key + (i,) if i == 0 else key[:-1] + (i,)
            i = i + 1
        sp = OLPSubprocess(id, process_name, process_name, p_ini, p_fin, originalkey, conf)
        subprocesses[key] = sp
        is_new = True

    return sp, is_new


def get_sp_key(p_ini, p_fin, use_crossings, conf):
    if use_crossings:
        pflvgrps = conf.getProperty(golem.properties.flavour_groups)
        if pflvgrps != [] and pflvgrps != [""]:
            # The following piece of code constructs the channel key respecting
            # the given flavour groups/classes. Nested structure needed to deal
            # with all the possible cases occuring for multiple quark lines.

            # translate flavour_groups property into list of list -> flvgrps
            # set up dictionary to translate pdg codes into flavour group identifiers -> flvgrps_dict
            flvgrps = []
            flvgrps_dict = {}
            for i, fg in enumerate(pflvgrps):
                if fg == "":
                    break
                for flv in list(map(int, fg.split(":"))):
                    flvgrps_dict[flv] = (i, "fg" + str(i))
                    flvgrps_dict[-flv] = (i, "fgbar" + str(i))
                flvgrps.append(list(map(int, fg.split(":"))))

            # get pdg codes for channel, sort according to number of occurences (and value)
            pdg_proc = [(p.getPDGCode(), p.getPartnerPDGCode()) for p in p_ini] + [
                (p.getPartnerPDGCode(), p.getPDGCode()) for p in p_fin
            ]
            pdg_proc.sort(key=lambda x: x[1])
            pdg_proc.sort(key=lambda x: [p[0] for p in pdg_proc].count(x[1]))

            # Whether or not to take the quark generation into account
            generations = conf.getProperty(golem.properties.respect_generations)
            gen_key = [0, 0, 0]

            k = [1 for _ in range(len(pflvgrps))]
            key_fg = [None for _ in range(len(pdg_proc))]
            skip = [False for _ in range(len(pdg_proc))]
            for i, pi in enumerate(pdg_proc):
                if skip[i]:
                    continue
                if pi[0] in flvgrps_dict and pi[1] in flvgrps_dict:
                    fgp = flvgrps_dict[pi[0]]
                    fga = flvgrps_dict[pi[1]]
                    s_fgp = fgp[1] + str(k[fgp[0]])
                    s_fga = fga[1] + str(k[fgp[0]])
                    k[fgp[0]] = k[fgp[0]] + 1
                else:
                    s_fgp = str(pi[0])
                    s_fga = str(pi[1])
                for j, pj in enumerate(pdg_proc):
                    if skip[j]:
                        continue
                    if pj[0] == pi[0]:
                        key_fg[j] = s_fgp
                        skip[j] = True
                    elif pj[0] == pi[1]:
                        key_fg[j] = s_fga
                        skip[j] = True
                    if i == 0 and generations and pj[0] in flvgrps_dict and pj[1] in flvgrps_dict:
                        if abs(pj[0]) == 1 or abs(pj[0]) == 2:
                            gp = 1
                        elif abs(pj[0]) == 3 or abs(pj[0]) == 4:
                            gp = 2
                        elif abs(pj[0]) == 5 or abs(pj[0]) == 6:
                            gp = 3
                        else:
                            logger.critical(
                                "Particle pdg(" + str(pj[0]) + ") does not belong to a known quark flavour generation!"
                            )
                            sys.exit("GoSam terminated due to an error")
                        gen_key[gp - 1] = gen_key[gp - 1] + 1

            # sort to catch cases like (u ub u ub -> s sb) <-> (c cb c cb -> d db)
            # => Not the actual number of occurences per generation is important, but their relative distribution
            gen_key.sort()
            conf["gen_key"] = gen_key

            key = tuple(sorted(key_fg))
        else:
            key = tuple(sorted(list(map(str, p_ini)) + [p.getPartner() for p in p_fin]))
    else:
        key = tuple(list(map(str, p_ini)) + [p.getPartner() for p in p_fin])

    return key


def is_config_compatible(conf1, conf2):
    """Checks if a subprocess with conf2 can be a crossing of conf1"""
    special = {
        "olp.amplitudetype": (lambda a, b: True),  # => ignored
        "olp.no_loop_level": (lambda a, b: True),  # => ignored
        "order": (lambda a, b: a.startswith(b) or b.startswith(a)),
    }
    for i in conf1:
        if not i in conf2 or conf1[i] != conf2[i]:
            bval = conf2[i] if i in conf2 else ""
            if i in special:
                if special[i](conf1[i], bval):
                    continue
            return False
    for i in conf2:
        if not i in conf1:
            if i in special:
                if special[i]("", conf2[i]):
                    continue
            return False
    return True


def adapt_config(conf1, conf2):
    """Adapt the configuration conf1 of a subprocess
    that a subprocess with conf2 can be a crossing of it."""
    conf1["olp.no_tree_level"] = conf1["olp.no_tree_level"] and conf2["olp.no_tree_level"]
    conf1["olp.no_loop_level"] = conf1["olp.no_loop_level"] and conf2["olp.no_loop_level"]
    conf1["order"] = max(conf1["order"], conf2["order"])  # take longest
    return True


def derive_output_name(input_name, pattern, dest_dir=None):
    path, file = os.path.split(input_name)
    if dest_dir is not None:
        path = dest_dir
    path = os.path.join(path, "")
    stem, ext = os.path.splitext(file)

    output_name = pattern
    output_name = output_name.replace("%f", input_name)
    output_name = output_name.replace("%F", file)
    output_name = output_name.replace("%p", path)
    output_name = output_name.replace("%s", stem)
    output_name = output_name.replace("%e", ext)

    return output_name


def derive_coupling_names(model_path, conf):
    """
    Return a triple (qcd_name, qed_name, all_couplings):

    qcd_name      -- the name to be used for the strong coupling constant
    qed_name      -- the name to be used for the weak coupling constant
    all_couplings -- all names that have to be set to one if couplings are
                     stripped.

    It is recommended that the names QCD, QED, e, gs, gw, EE, EW, GG are used
    in model files, otherwise this routine has difficulties detecting them
    as couplings. These name can also be prefixed by the string 'mdl'
    """
    strong_coupling_names = ["QCD", "GS", "GG", "G"]
    weak_coupling_names = ["QED", "GW", "E", "EE", "EW"]

    # ---#[ Load model file as module:
    mod = golem.util.tools.getModel(conf, model_path)
    # ---#] Load model file as module:

    strong_couplings_found = {}
    weak_couplings_found = {}
    candidates = []

    for param in mod.types.keys():
        if param.startswith("mdl"):
            canonical_name = param[3:].upper()
        else:
            canonical_name = param.upper()
        if canonical_name in strong_coupling_names:
            strong_couplings_found[canonical_name] = param
        elif canonical_name in weak_coupling_names:
            weak_couplings_found[canonical_name] = param
        else:
            candidates.append(canonical_name)

    if len(strong_couplings_found) == 0:
        logger.critical(
            "Invalid model file: cannot determine name of strong coupling.\n" + "Candidates are:" + ",".join(candidates)
        )
        sys.exit("GoSam terminated due to an error")
    else:
        for name in strong_coupling_names:
            if name in strong_couplings_found:
                qcd_name = strong_couplings_found[name]
                break

    if len(weak_couplings_found) == 0:
        logger.critical(
            "Invalid model file: cannot determine name of weak coupling.", "Candidates are:" + ",".join(candidates)
        )
        sys.exit("GoSam terminated due to an error")
    else:
        for name in weak_coupling_names:
            if name in weak_couplings_found:
                qed_name = weak_couplings_found[name]
                break

    all_couplings = list(strong_couplings_found.values()) + list(weak_couplings_found.values())

    return qcd_name, qed_name, all_couplings


def get_power(conf):
    """
    Returns two lists:
       list of length three: [coupling_name, born_power, virt_power]
    The list specifies the option 'order'.

    If the list is empty the process is not specified unambiguously.
    """
    alpha_power = conf.getProperty("olp.alphapower", default=None)
    alphas_power = conf.getProperty("olp.alphaspower", default=None)
    correction_type = conf.getProperty("olp.correctiontype", default=None)
    notreelevel = conf.getBooleanProperty("olp.no_tree_level", default=False)
    nolooplevel = conf.getBooleanProperty("olp.no_loop_level", default=False)

    qcd_name = "QCD"
    qed_name = "QED"

    if notreelevel:
        if nolooplevel:
            raise GolemConfigError("Neither tree or loop contributions are requested")
        if correction_type == "QCD":
            if alphas_power is not None:
                qcd_tree_power = "NONE"
                qcd_loop_power = int(alphas_power)
            else:
                raise GolemConfigError("Requested QCD corrections without specifying strong coupling order")
            if alpha_power is not None:
                ew_tree_power = int(alpha_power)
                ew_loop_power = int(alpha_power)
            else:
                ew_tree_power = None
                ew_loop_power = None
        elif correction_type == "EW" or correction_type == "QED":
            if alpha_power is not None:
                ew_tree_power = "NONE"
                ew_loop_power = int(alpha_power)
            else:
                raise GolemConfigError("Requested QCD corrections without specifying strong coupling order")
            if alphas_power is not None:
                qcd_tree_power = int(alphas_power)
                qcd_loop_power = int(alphas_power)
            else:
                qcd_tree_power = None
                qcd_loop_power = None
        else:
            raise GolemConfigError(f"Unknown correction type {correction_type}")
    else:
        if alphas_power is not None:
            qcd_tree_power = int(alphas_power)
        else:
            qcd_tree_power = None
        if alpha_power is not None:
            ew_tree_power = int(alpha_power)
        else:
            ew_tree_power = None
        if nolooplevel:
            qcd_loop_power = None
            ew_loop_power = None
        else:
            if correction_type == "EW" or correction_type == "QED":
                if ew_tree_power is None:
                    raise GolemConfigError("Requested EW corrections without specifying electroweak coupling order")
                else:
                    ew_loop_power = ew_tree_power + 2
                qcd_loop_power = qcd_tree_power
            elif correction_type == "QCD":
                if qcd_tree_power is None:
                    raise GolemConfigError("Requested QCD corrections without specifying strong coupling order")
                else:
                    qcd_loop_power = qcd_tree_power + 2
                ew_loop_power = ew_tree_power
            else:
                raise GolemConfigError(f"Unknown correction type {correction_type}")

    if qcd_tree_power is not None:
        qcd_powers = [qcd_name, qcd_tree_power]
        if qcd_loop_power is not None:
            qcd_powers.append(qcd_loop_power)
    else:
        qcd_powers = []
    if ew_tree_power is not None:
        ew_powers = [qed_name, ew_tree_power]
        if ew_loop_power is not None:
            ew_powers.append(ew_loop_power)
    else:
        ew_powers = []

    return [*qcd_powers, *ew_powers]


def derive_zero_masses(model_path, slha_file, conf):
    mod_params = golem.util.olp_objects.SUSYLesHouchesFile(slha_file)
    # ---#[ Load model file as module:
    mod = golem.util.tools.getModel(conf, model_path)
    # ---#] Load model file as module:

    result = []
    for name, part in mod.particles.items():
        mass = part.getMass().strip()
        if mass in mod.slha_locations:
            block, coords = mod.slha_locations[mass]
            params = mod_params[block]
            id = tuple(coords)
            if id in params:
                if params[id] == 0.0:
                    result.append(mass)
            else:
                result.append(mass)
    return result


def handle_subprocess(
    conf, subprocess, subprocess_key, subprocesses_conf, path, from_scratch, use_crossings, contract_file
):
    helicities = {}
    subprocesses = {}
    subprocesses_conf_short = {}

    GOLEM_FULL = "GoSam %s" % ".".join(map(str, golem.installation.GOLEM_VERSION))

    process_path = subprocess.getPath(path)
    subprocess_conf = subprocess.getConf(subprocesses_conf[int(subprocess)], path)
    subprocess_conf["golem.name"] = "GoSam"
    subprocess_conf["golem.version"] = ".".join(map(str, golem.installation.GOLEM_VERSION))
    subprocess_conf["golem.full-name"] = GOLEM_FULL
    subprocess_conf["golem.revision"] = golem.installation.GOLEM_REVISION

    golem.util.tools.POSTMORTEM_CFG = subprocess_conf

    try:
        golem.util.main_misc.workflow(subprocess_conf)
        merge_extensions(subprocess_conf, conf)

        golem.util.main_misc.generate_process_files(subprocess_conf, from_scratch)

        # ---[ Handle Crossings:

        if use_crossings and any(
            [
                kw in subprocess_conf.getProperty(fltr) if subprocess_conf.getProperty(fltr) else False
                for fltr in ["filter.lo", "filter.nlo"]
                for kw in ["iprop_momentum", "ext_legs_from_vertex"]
            ]
        ):
            # If the crossings of the original subprocess are vetoed, a new parent subprocess
            # for the remaining crossings is needed
            keep_subprocess = subprocess_conf.getBooleanProperty("veto_crossings")
            parent_subprocess = None
            parent_key = None
            for id in subprocess.getIDs():
                if not id == subprocess.id:
                    # Build subprocess object for each crossing
                    key = tuple(
                        sorted(
                            list(map(str, subprocess.crossings_p_ini[id]))
                            + [p.getPartner() for p in subprocess.crossings_p_fin[id]]
                        )
                    ) + (id,)

                    sp = OLPSubprocess(
                        id,
                        subprocess.ids[id],
                        subprocess.ids[id],
                        subprocess.crossings_p_ini[id],
                        subprocess.crossings_p_fin[id],
                        key,
                        subprocess.crossings_conf[id],
                    )
                    # Prepare folder for each crossing
                    sp_subdir = str(sp)
                    sp_process_path = os.path.join(path, sp_subdir)
                    if not os.path.exists(sp_process_path):
                        logger.info("Creating directory %r" % sp_process_path)
                        try:
                            os.mkdir(sp_process_path)
                        except IOError as err:
                            logger.critical(str(err))
                            sys.exit("GoSam terminated due to an error")

                    sp_conf = sp.getConf(subprocesses_conf[int(sp)], path)
                    sp_conf["golem.name"] = "GoSam"
                    sp_conf["golem.version"] = ".".join(map(str, golem.installation.GOLEM_VERSION))
                    sp_conf["golem.full-name"] = GOLEM_FULL
                    sp_conf["golem.revision"] = golem.installation.GOLEM_REVISION

                    golem.util.tools.POSTMORTEM_CFG = sp_conf

                    try:
                        golem.util.main_misc.workflow(sp_conf)

                        # Generate the files for the crossing and apply the filters
                        golem.util.main_misc.generate_process_files(sp_conf, from_scratch)

                        # If the crossing is also vetoed, it has to be kept as separate subprocess and be
                        # removed from the list of crossings of the original subprocess
                        if sp_conf.getBooleanProperty("veto_crossings"):
                            subprocess.removeCrossing(id)
                            helicities[id] = list(golem.util.tools.enumerate_and_reduce_helicities(sp_conf))

                            subprocesses_conf_short[id] = sp_conf
                            subprocesses[key] = sp
                        else:
                            # If the current crossing is not vetoed, it's process files are not needed and can be
                            # removed
                            if not keep_subprocess:
                                shutil.rmtree(sp_process_path)
                            # If it can still be derived from the original subprocess, nothing has to be done
                            # If the original subprocess cannot be used, a new parent subprocess has to be chosen.
                            if subprocess_conf.getBooleanProperty("veto_crossings"):
                                if not parent_subprocess:
                                    parent_subprocess = sp
                                    parent_key = key
                                    keep_subprocess = False
                                else:
                                    parent_subprocess.addCrossing(sp.id, sp.process_name, sp.p_ini, sp.p_fin, sp.conf)
                                subprocess.removeCrossing(sp.id)

                    except golem.util.config.GolemConfigError as err:
                        logger.critical("Configuration file is not sound:" + str(err))
                        sys.exit("GoSam terminated due to an error")

            # Regenerate process files for the original subprocess with new list of crossings
            shutil.rmtree(process_path)
            os.mkdir(process_path)
            subprocess_conf = subprocess.getConf(subprocesses_conf[int(subprocess)], path)
            subprocess_conf["golem.name"] = "GoSam"
            subprocess_conf["golem.version"] = ".".join(map(str, golem.installation.GOLEM_VERSION))
            subprocess_conf["golem.full-name"] = GOLEM_FULL
            subprocess_conf["golem.revision"] = golem.installation.GOLEM_REVISION
            golem.util.main_misc.workflow(subprocess_conf)
            golem.util.main_misc.generate_process_files(subprocess_conf, from_scratch)
            # Regenerate process files for new parent subprocess if it exists
            if parent_subprocess:
                parent_path = os.path.join(path, str(parent_subprocess))
                shutil.rmtree(parent_path)
                os.mkdir(parent_path)
                parent_conf = parent_subprocess.getConf(subprocesses_conf[int(parent_subprocess)], path)
                parent_conf["golem.name"] = "GoSam"
                parent_conf["golem.version"] = ".".join(map(str, golem.installation.GOLEM_VERSION))
                parent_conf["golem.full-name"] = GOLEM_FULL
                parent_conf["golem.revision"] = golem.installation.GOLEM_REVISION
                golem.util.main_misc.workflow(parent_conf)
                golem.util.main_misc.generate_process_files(parent_conf, from_scratch)
                helicities[parent_subprocess.id] = list(golem.util.tools.enumerate_and_reduce_helicities(parent_conf))

                subprocesses_conf_short[parent_subprocess.id] = parent_conf
                subprocesses[parent_key] = parent_subprocess

        helicities[subprocess.id] = list(golem.util.tools.enumerate_and_reduce_helicities(subprocess_conf))

    except golem.util.config.GolemConfigError as err:
        logger.critical("Configuration file is not sound:" + str(err))
        sys.exit("GoSam terminated due to an error")

    subprocesses[subprocess_key] = subprocess
    subprocesses_conf_short[subprocess.id] = subprocess_conf

    return subprocesses, helicities, subprocesses_conf_short


def process_order_file(
    order_file_name,
    f_contract,
    path,
    default_conf,
    templates=None,
    ignore_case=False,
    ignore_unknown=False,
    from_scratch=False,
    mc_name="any",
    use_crossings=True,
    **opts,
):
    def getquarktype(quark):
        # keep only first capital letter
        # trick to transform anti-quarks in quarks
        if list(quark)[0].isupper():
            return list(quark)[0]
        else:
            return quark

    syntax_extensions = ["single_quotes", "double_quotes", "backslash_escape"]

    extensions = {}
    for ex in syntax_extensions:
        if ex in opts:
            extensions[ex] = opts[ex]
        else:
            extensions[ex] = False

    logger.debug("Processing order file at %r" % order_file_name)
    GOLEM_FULL = "GoSam %s" % ".".join(map(str, golem.installation.GOLEM_VERSION))
    result = 0

    conf = golem.util.config.Properties()
    conf += default_conf

    # check if any model.options are set in the config file (before filling in the defaults)
    config_model_options = conf.getListProperty("model.options") != []
    conf.setProperty("olp.config_model_options",config_model_options)

    try:
        config_ir_scheme = default_conf["regularisation_scheme"].upper()
    except AttributeError:
        config_ir_scheme = None

    ext_ir_scheme = None
    if "dred" in default_conf["extensions"] and "thv" in default_conf["extensions"]:
        logger.critical(
                        "Multiple regularisation schemes specified in extensions: thv and dred. Please pick one."
                    )
        sys.exit("GoSam terminated due to an error")
    if "dred" in default_conf["extensions"]:
        ext_ir_scheme = "DRED"
    if "thv" in default_conf["extensions"]:
        ext_ir_scheme = "THV"

    # check consistency of regularisation schemes in setup file (if present)
    if config_ir_scheme != None and ext_ir_scheme != None:
        if config_ir_scheme != ext_ir_scheme:
            logger.critical(
                        "Incompatible settings between regularisation_scheme and extensions: "
                        + "%r vs. %r" % (config_ir_scheme,ext_ir_scheme)
                    )
            sys.exit("GoSam terminated due to an error")


    if "olp_process_name" in opts:
        olp_process_name = opts["olp_process_name"].strip().lower()
    else:
        olp_process_name = ""

    conf["olp.process_name"] = olp_process_name

    mc_name_parts = mc_name.split("/", 1)
    conf["olp.mc.name"] = mc_name_parts[0].lower()
    if len(mc_name_parts) > 1:
        conf["olp.mc.version"] = mc_name_parts[1].lower()

    # Set options
    conf["olp.no_tree_level"] = False
    conf["olp.amplitudetype"] = "loop"

    # ---#[ Read order file:
    try:
        order_file = golem.util.olp_objects.OLPOrderFile(order_file_name, extensions)
    except IOError as err:
        raise golem.util.olp_objects.OLPError("while reading order file: %s" % err)

    mc_specials(conf, order_file)

    for pi_key in conf.getListProperty("mc_specials.keys"):
        if pi_key == "":
            continue
        if pi_key in default_conf:
            if conf["mc_specials."+pi_key] != conf[pi_key] and conf[pi_key] is not None and conf[pi_key] != "":
                logger.warning("Your BLHA order file '%s' specifies the property '%s' in a special '#@' instruction.\n" \
                "It will overwrite the default and/or the value given in the config file\n'%s':\n%s -> %s\n" \
                "Please check that this is really what you want to do! " 
                % (order_file_name,pi_key,conf["extra_setup_file"],conf[pi_key],conf["mc_specials."+pi_key]))
        key = pi_key.removeprefix("mc_specials")
        if key == "extensions":
            conf["extensions"] = conf["mc_specials.extensions"] if conf["extensions"] == "" else conf[extensions]+","+conf["mc_specials.extensions"]
        else:
            conf[key] = conf["mc_specials."+pi_key]
        conf._del("mc_specials."+pi_key)

    contract_file = golem.util.olp_objects.OLPContractFile(order_file)

    tmp_contract_file = golem.util.olp_objects.OLPContractFile(order_file)
    subprocesses_conf = []

    conf.setProperty("setup-file", order_file_name)
    orig_conf = conf.copy()

    file_ok = golem.util.olp_options.process_olp_options(contract_file, conf, ignore_case, ignore_unknown)

    for subprocess_number, (lineo, _, _, _) in enumerate(order_file.processes_ordered()):
        subconf = orig_conf.copy()
        subconf.activate_subconfig(subprocess_number)
        file_ok = golem.util.olp_options.process_olp_options(
            tmp_contract_file, subconf, ignore_case, ignore_unknown, lineo, quiet=True
        )
        subprocesses_conf.append(subconf)

    # ---#] Read order file:
    if file_ok:
        if not os.path.exists(path):
            logger.info("Creating directory %r" % path)
            os.mkdir(path)

        # ---#[ Import model file once for all subprocesses:
        imodel_path = os.path.join(path, "model")
        if not os.path.exists(imodel_path):
            logger.info("Creating directory %r" % imodel_path)
            os.mkdir(imodel_path)
        for lconf in [conf] + subprocesses_conf:
            golem.util.tools.prepare_model_files(lconf, imodel_path)

            lconf["modeltype"] = lconf.getListProperty("model")[-1]

            lconf["model"] = os.path.join(imodel_path, golem.util.constants.MODEL_LOCAL)
        # ---#] Import model file once for all subprocesses:
        # ---#[ Constrain masses:
        model_file = conf["olp.modelfile"]
        if model_file is not None:
            zero_masses = derive_zero_masses(imodel_path, model_file, conf)
            zero = golem.util.tools.getZeroes(conf)
            for m in zero_masses:
                if m not in zero:
                    zero.append(m)
                    logger.info("Identified %s==0 (from SLHA file)" % m)
            for lconf in [conf] + subprocesses_conf:
                lconf[golem.properties.zero] = ",".join(zero)
        # ---#] Constrain masses:

        model_conf = conf.copy()
        # This fills in the defaults where no option is given:
        for p in golem.properties.properties:
            if model_conf.getProperty(p) or model_conf.getProperty(p) == False or model_conf.getProperty(p) == 0:
                # Note that 'False'and '0' are actually valid values. We want to skip falsy values like [], " ", None, etc.
                model_conf.setProperty(str(p), model_conf.getProperty(p))

        model = golem.util.tools.getModel(model_conf, imodel_path)

        # zero property: convert masses and width defined through PDG code to internal parameter name 
        # (depends on model, so model.py must have been created already)
        orig_zero = conf.getListProperty("zero")
        new_zero = []
        for z in orig_zero:
            massmatch = re.search(r"mass\([0-9+][\;0-9+]+\)",z.lower())
            if massmatch:
                nz = re.sub(r"\;",r"),mass(",z.lower()).split(",")
                new_zero.extend(nz)
                continue
            widthmatch = re.search(r"width\([0-9+][\;0-9+]+\)",z.lower())
            if widthmatch:
                nz = re.sub(r"\;",r"),width(",z.lower()).split(",")
                new_zero.extend(nz)
                continue
            new_zero.append(z)
        for p in model.particles.values():
            searchm = "mass("+str(abs(p.getPDGCode()))+")"
            if searchm in list(map(str.lower,new_zero)):
                new_zero.pop(list(map(str.lower,new_zero)).index(searchm))
                if p.isMassive():
                    new_zero.append(p.getMass())
            searchw = "width("+str(abs(p.getPDGCode()))+")"
            if searchw in list(map(str.lower,new_zero)):
                new_zero.pop(list(map(str.lower,new_zero)).index(searchw))
                if p.hasWidth():
                    new_zero.append(p.getWidth())
        conf.setProperty("zero",",".join(list(set(new_zero))))
        for subconf in subprocesses_conf:
            subconf.setProperty("zero",",".join(list(set(new_zero))))

        # It can happen that a model defines names for a particle's mass and width but 
        # sets them to 0 in the parameters definiton (see e.g. the light quarks in the 
        # built-in models). We have to take care of that and add those names to the zero 
        # property to avoid erroneous code generation. Otherwise the user has to remember
        # to add these cases to 'zero' manually.
        if not conf.getBooleanProperty("massive_light_fermions"):
            zeros = conf.getListProperty("zero")
            for p in model.particles.values():
                if p.isMassive(zeros):
                    m = p.getMass(zeros)
                    try:
                        if float(model.parameters[m]) == 0.:
                            zeros.append(m)
                    except KeyError:
                        # dependent parameters are not part of parameters dict
                        pass
                if p.hasWidth(zeros):
                    w = p.getWidth(zeros)
                    try:
                        if float(model.parameters[w]) == 0.:
                            zeros.append(w)
                    except KeyError:
                        # dependent parameters are not part of parameters dict
                        pass
            conf.setProperty("zero",",".join(list(set(zeros))))
            for subconf in subprocesses_conf:
                subconf.setProperty("zero",",".join(list(set(zeros))))

        # ---#[ Setup excluded and massive particles :
        for lconf in [conf] + subprocesses_conf:
            list_exclude = []
            for i in [int(p) for p in lconf["__excludedParticles__"].split()] if lconf["__excludedParticles__"] else []:
                for n in model.particles:
                    particle = model.particles[n]
                    if particle.getPDGCode() == i:
                        list_exclude.append(str(particle))
            if list_exclude:
                if not lconf["filter.particles"]:
                    lconf["filter.particles"] = ",".join(f"{p}:0" for p in list_exclude)
                else:
                    lconf["filter.particles"] += "," + ",".join(f"{p}:0" for p in list_exclude)

            lconf["__excludedParticles__"] = None

            # Deactivated to avoid unintuitive behaviour. Particle 
            # masses should be taken as in the model file or set to 
            # zero (if desired) through the process card (*.in or *.rc)

            # set_massiveParticles = set()
            # list_default_zero_values = default_conf["zero"].split(",") if default_conf["zero"] else []
            # list_zero_values = []
            # list_nonzero_values = []
            # if lconf["__OLP_BLHA2__"] == "True":  # only supported in BLHA2
            #     for i in (
            #         [int(p) for p in lconf["__massiveParticles__"].split()] if lconf["__massiveParticles__"] else []
            #     ):
            #         for n in model.particles:
            #             particle = model.particles[n]
            #             if particle.getPDGCode() == i:
            #                 set_massiveParticles.add(particle.getPDGCode())
            #                 set_massiveParticles.add(-particle.getPDGCode())
            #                 mass = particle.getMass()
            #                 if mass != "0":
            #                     if mass in list_default_zero_values:
            #                         logger.critical(
            #                             "BLHA-file specifies particle %r (PDG %r) as massive, which\n" \
            #                             " conficts with 'zero' list provided in config file(s)\n %r."
            #                             % (str(particle),particle.getPDGCode(),default_conf["extra_setup_file"]))
            #                         sys.exit("GoSam terminated due to an error")
            #                     list_nonzero_values.append(mass)
            #                 width = particle.getWidth()
            #                 if width != "0":
            #                     list_nonzero_values.append(width)

            #     for n in model.particles:
            #         particle = model.particles[n]
            #         if particle.getPDGCode() not in set_massiveParticles:
            #             mass = particle.getMass()
            #             if mass != "0" and mass not in list_zero_values and mass not in list_nonzero_values:
            #                 list_zero_values.append(mass)
            #             width = particle.getWidth()
            #             if width != "0" and width not in list_zero_values and width not in list_nonzero_values:
            #                 list_zero_values.append(width)
            # if list_zero_values:
            #     if lconf["zero"]:
            #         lconf["zero"] = lconf["zero"] + "," + ",".join(list_zero_values)
            #     else:
            #         lconf["zero"] = ",".join(list_zero_values)

            # lconf["__massiveParticles__"] = None

        # ---#] Setup excluded and massive particles :

        # ---#[ Setup couplings :

        for lconf in [conf] + subprocesses_conf:
            qcd_name, qed_name, all_couplings = derive_coupling_names(imodel_path, lconf)
            coupling_power = get_power(lconf)

            if len(coupling_power) == 0:
                contract_file.setPropertyResponse(
                    "CorrectionType",
                    ["Error:", "Wrong or missing entries in", "CorrectionType, AlphaPower or AlphasPower"],
                )
                file_ok = False
            else:
                lconf[golem.properties.coupling_power] = ",".join(map(str, coupling_power))

            if "olp.operationmode" in lconf:
                strip_couplings = "CouplingsStrippedOff" in lconf.getListProperty("olp.operationmode")
            else:
                strip_couplings = False

            if strip_couplings:
                ones = lconf.getListProperty(golem.properties.one)
                for coupling in all_couplings:
                    if coupling not in ones:
                        ones.append(coupling)
                lconf[golem.properties.one] = ",".join(ones)
                conf["nlo_prefactors"] = 0
        # ---#] Setup couplings :
        # ---#[ Select regularisation scheme:
        for lconf in [conf] + subprocesses_conf:

            # In OLP mode IR-scheme is specified through IRregularisation, which might interfere with scheme given
            # in config file (if present). The following behaviour is implemented:
            #
            # OLP  | config (from e.g. golem.in)  | result
            # -----------------------------------------------------------------------
            # tHV  | None                         | "dred" + "convert_to_thv = True"
            # tHV  | regularisation_scheme=thv    | "thv"  + "convert_to_thv = False" 
            # tHV  | thv in extensions            | "thv"  + "convert_to_thv = False"
            # DRED | None                         | "dred" + "convert_to_thv = False"
            # DRED | regularisation_scheme=dred   | "dred" + "convert_to_thv = False"
            # DRED | dred in extensions           | "dred" + "convert_to_thv = False"
            # DRED | convert_to_thv=True          | "dred" + "convert_to_thv = True"
            # 
            #
            # In case of mismatch execution is terminated.
            #
            # OLP  | config (from e.g. golem.in)  | result
            # -----------------------------------------------------------------------
            # tHV  | regularisation_scheme=dred   | mismatch -> ERROR (terminate)
            # tHV  | dred in extensions           | mismatch -> ERROR (terminate)
            # DRED | regularisation_scheme=thv    | mismatch -> ERROR (terminate)
            # DRED | thv in extensions            | mismatch -> ERROR (terminate)

            ir_scheme = lconf["olp.irregularisation"].upper()
            ext = lconf.getListProperty(golem.properties.extensions)
            uext = [s.upper() for s in ext]

            # check BLHA regularisation scheme vs regularisation_scheme or extensions in setup file (if present)
            mismatch_schemes = [False, None]

            if ir_scheme == "CDR":
                logger.warning("GoSam results are returned in the 't Hooft-Veltman scheme,\n" \
                "which differs from requested CDR scheme at O(eps). For \n"
                "ordinary NLO calculations this should not be a problem.")
                ir_scheme = "THV"

            if config_ir_scheme != None:
                if config_ir_scheme != ir_scheme:
                    mismatch_schemes = [True, config_ir_scheme]

            if ext_ir_scheme != None:
                if ext_ir_scheme != ir_scheme:
                    mismatch_schemes = [True, ext_ir_scheme]

            if mismatch_schemes[0]:
                logger.critical(
                    "IR regularisation scheme specified in BLHA-file conflicts with " \
                    "scheme specified in config file(s)\n %r:\n %r vs. %r" \
                            % (default_conf["extra_setup_file"],ir_scheme,mismatch_schemes[1]))
                sys.exit("GoSam terminated due to an error")

            # choose behaviour according to table above
            if ir_scheme == "DRED":
                if "DRED" not in uext:
                    lconf["olp." + str(golem.properties.extensions)] = "DRED"
            elif ir_scheme == "THV":
                if config_ir_scheme == None and ext_ir_scheme == None:
                    if "DRED" not in uext:
                        lconf["olp." + str(golem.properties.extensions)] = "DRED"
                    lconf["convert_to_thv"] = True   
                else: 
                    # at this point we can be sure that at least one of config_ir_scheme or 
                    # ext_ir_scheme equal "tHV" because of the check above
                    if "tHV" not in uext:
                        lconf["olp." + str(golem.properties.extensions)] = "tHV"
                    lconf["convert_to_thv"] = False
            else:
                logger.critical("BLHA-file does not specify IRregularisation!")
                sys.exit("GoSam terminated due to an error")

    fill_config(conf)

    # ---#[ Iterate over subprocesses:
    subdivide = conf.getProperty("olp.subdivide", "no").lower() in ["yes", "true", "1"]
    channels = {}
    chelis = {}
    helicities = {}
    max_occupied_channel = -1
    subprocesses = {}
    subprocesses_flav = {}

    subprocesses_conf_short = {}

    if file_ok:
        for lineno, id, inp, outp in contract_file.processes_ordered():
            subprocess, is_new = getSubprocess(
                olp_process_name,
                id,
                inp,
                outp,
                subprocesses,
                subprocesses_flav,
                model,
                use_crossings,
                subprocesses_conf[id],
            )
            if is_new:
                subdir = str(subprocess)
                process_path = os.path.join(path, subdir)
                if not os.path.exists(process_path):
                    logger.info("Creating directory %r" % process_path)
                    try:
                        os.mkdir(process_path)
                    except IOError as err:
                        logger.critical(str(err))
                        sys.exit("GoSam terminated due to an error")

        # Now we run the loop again since all required crossings are added

        # store initial symmetries infos
        start_symmetries = conf["symmetries"]

        if Pool:
            with Pool(conf.getIntegerProperty("n_jobs")) as pool:
                sp_res = pool.map(
                    lambda sp: handle_subprocess(
                        conf, sp[1], sp[0], subprocesses_conf, path, from_scratch, use_crossings, contract_file
                    ),
                    subprocesses.items(),
                )
        else:
            sp_res = list(
                map(
                    lambda sp: handle_subprocess(
                        conf, sp[1], sp[0], subprocesses_conf, path, from_scratch, use_crossings, contract_file
                    ),
                    subprocesses.items(),
                )
            )

        for res in sp_res:
            subprocesses.update(res[0])
            helicities.update(res[1])
            subprocesses_conf_short.update(res[2])

        for sp_conf in subprocesses_conf_short.values():
            merge_extensions(sp_conf, conf)

        for sp in list(subprocesses.values()):
            for sp_id in sp.getIDs():
                generated_helicities = [t[0] for t in [t for t in helicities[sp.id] if t[1] is None]]
                chelis[sp_id] = len(helicities[sp.id])
                if subdivide:
                    num_channels = len(helicities[sp.id])
                    min_channel = max_occupied_channel + 1
                    max_channel = min_channel + num_channels - 1
                    max_occupied_channel += num_channels
                    channels[sp_id] = list(range(min_channel, max_channel + 1))
                else:
                    max_occupied_channel += 1
                    channel = max_occupied_channel
                    channels[sp_id] = [channel]

                contract_file.setProcessResponse(sp_id, channels[sp_id])
                sp.assignChannels(sp_id, channels[sp_id])
                sp.assignNumberHelicities(len(helicities[sp.id]), generated_helicities)

    # ---#] Iterate over subprocesses:
    # ---#[ Write output file:
    f_contract.write("# vim: syntax=olp\n")
    f_contract.write("#@OLP GoSam %s\n" % ".".join(map(str, golem.installation.GOLEM_VERSION)))
    f_contract.write("#@IgnoreUnknown %s\n" % ignore_unknown)
    f_contract.write("#@IgnoreCase %s\n" % ignore_case)
    f_contract.write("#@SyntaxExtensions %s\n" % " ".join([i for i in list(extensions.keys()) if extensions[i]]))
    try:
        contract_file.store(f_contract)
    except IOError as err:
        raise golem.util.olp_objects.OLPError("while writing contract file: %s" % err)
    # ---#] Write output file:

    # Contract file is written, no we can stop if there were any errors 
    if not file_ok:
        logger.critical("Your BLHA order file could not be processed properly.\n"
                        "Please, check configuration and contract files for errors!")
        sys.exit("GoSam terminated due to an error")   

    # ---#[ Process global templates:

    if templates is None:
        templates = ""

    if templates == "":
        templates = golem.util.tools.golem_path("olp", "templates")

    ext = golem.properties.getExtensions(conf)

    # This fills in the defaults where no option is given:
    for p in golem.properties.properties:
        if conf.getProperty(p) or conf.getProperty(p) == False or conf.getProperty(p) == 0:
            # Note that 'False'and '0' are actually valid values a property can be set to. 
            conf.setProperty(str(p), conf.getProperty(p))
        else:
            # this catches all falsy values like [], None, " ", etc., which mean
            # the property is not set yet. But not '0' and the acual bool 'False', 
            # which we checked for above, since those ARE possible values for a property.
            conf.setProperty(str(p), p.getDefault())

##################################################################################
#   ATTENTION!!! 
#   
#   The following original implementation looks fine but is broken, as properties
#   evaluating to 'False' or '0' will be counted as not initialized/given. But
#   this is not correct. A property can be set to either of these values and we
#   DO NOT want to overwrite it with its default. Code kept here as a warning.    
#
##################################################################################
#    for p in golem.properties.properties:
#        if conf.getProperty(p):
#            conf.setProperty(str(p), conf.getProperty(p))
#        else:
#            conf.setProperty(str(p), p.getDefault())




    golem.properties.setInternals(conf)

    # ---#[ Fill in information needed by the main config to generate the common source files
    conf["golem.name"] = "GoSam"
    conf["golem.version"] = ".".join(map(str, golem.installation.GOLEM_VERSION))
    conf["golem.full-name"] = GOLEM_FULL
    conf["golem.revision"] = golem.installation.GOLEM_REVISION

    orders = golem.util.config.split_power(",".join(map(str, conf.getListProperty(golem.properties.coupling_power))))
    powers = orders[0] if orders else []

    if len(powers) == 2:
        generate_tree_diagrams = True
        generate_loop_diagrams = False
    elif len(powers) == 3:
        generate_tree_diagrams = str(powers[1]).strip().lower() != "none"
        generate_loop_diagrams = True

    conf["generate_tree_diagrams"] = generate_tree_diagrams
    conf["generate_loop_diagrams"] = generate_loop_diagrams

    if "ewchoose" in golem.model.MODEL_OPTIONS:
        conf.setProperty("ewchoose", str(golem.model.MODEL_OPTIONS["ewchoose"]))
    else:
        conf.setProperty("ewchoose", False)

    # ---] Fill in information needed by the main config to generate the common source files

    golem.templates.xmltemplates.transform_templates(
        templates,
        path,
        conf.copy(),
        conf=conf,
        subprocesses=sorted(list(subprocesses.values()), key=lambda sp: sp.id),
        subprocesses_conf=[sp for _, sp in sorted(subprocesses_conf_short.items(), key=lambda spi: spi[0])],
        contract=contract_file,
        user="olp",
    )

    # ---#] Process global templates:
    return result


def mc_specials(conf, order_file):
    pi_keys = []
    for pi in order_file.processing_instructions():
        pi_parts = pi.strip().split(" ", 1)
        if pi_parts[0] == "regularisation_scheme":
            logger.critical("Property 'regularisation_scheme' cannot be set as a '#@' instruction in the BLHA order file!\n" \
            "Please only use BLHA's 'IRregularisation' keyword.")
            sys.exit("GoSam terminated due to an error")
        if pi_parts[0] == "extensions":
            if any(irs in [ext.lower() for ext in pi_parts[1].split(",")] for irs in ["dred","thv"]):
                logger.critical("IR regularisation scheme ('dred' or 'thv') cannot be added to 'extensions'\n"
                                "in a '#@' instruction in the BLHA order file! Please only use BLHA's 'IRregularisation' keyword.")
                sys.exit("GoSam terminated due to an error")   
        pi_keys.append(pi_parts[0])
        if len(pi_parts) == 2:
            conf.setProperty("mc_specials."+pi_parts[0], pi_parts[1])
        else:
            conf.setProperty("mc_specials."+pi_parts[0], True)
    conf.setProperty("mc_specials.keys",pi_keys)

    overwrite_warn = False

    mc_name = conf.getProperty("olp.mc.name").lower().strip()

    if mc_name != "any":        
        if conf.getProperty("mc_specials.olp.mc.name") is not None:
            mc_special_mc_name = conf.getProperty("mc_specials.olp.mc.name").lower().strip()
            if mc_name != mc_special_mc_name:
                overwrite_warn = True
    elif conf.getProperty("mc_specials.olp.mc.name") is not None:
        mc_name = conf.getProperty("mc_specials.olp.mc.name").lower().strip()
    
    mc_version = []
    s = ""
    mc_special_s = ""
    if conf.getProperty("olp.mc.version") is not None:
        s = conf.getProperty("olp.mc.version", default="").strip()
        if conf.getProperty("mc_specials.olp.mc.version") is not None:
            mc_special_s = conf.getProperty("mc_specials.olp.mc.version", default="").strip()
            if s != mc_special_s:
                overwrite_warn = True
    elif conf.getProperty("mc_specials.olp.mc.version") is not None:
        s = conf.getProperty("mc_specials.olp.mc.version", default="").strip()
    if len(s) > 0:
        mc_version = list(map(int, s.split(".")))

    if overwrite_warn:
        old_mc = mc_special_mc_name if mc_special_s == "" else mc_special_mc_name+"/"+mc_special_s
        new_mc = mc_name if s == "" else mc_name+"/"+s
        logger.warning("Command line argument --mc %s overwrites #@ instruction in BLHA order file: %s -> %s " 
                        % (new_mc,old_mc,new_mc))

    required_extensions = []

    if mc_name == "any":
        pass
    elif mc_name == "powheg" or mc_name == "powhegbox":
        required_extensions.extend(["f77"])
        required_extensions.extend(["olp_badpts"])
    elif mc_name == "amcatnlo":
        required_extensions.extend(["f77"])
    else:
        logger.warning("Unknown Monte Carlo program passed via the --mc argument: %s. This statement will be IGNORED!" % (mc_name))

    extensions = golem.properties.getExtensions(conf)
    add_extensions = []
    for ext in required_extensions:
        if ext not in extensions:
            add_extensions.append(ext)
    if len(add_extensions) > 0:
        conf.setProperty("%s-auto.extensions" % mc_name, ",".join(add_extensions))

def merge_extensions(conf_a, conf_b):
    """merge extensions from conf_a into conf_b"""

    extensions_a = golem.properties.getExtensions(conf_a)
    extensions_b = golem.properties.getExtensions(conf_b)

    add_extensions = []
    if conf_b.getProperty("merge-auto.extensions"):
        add_extensions = conf_b.getProperty("merge-auto.extensions").split(",")
    for ext in extensions_a:
        if ext and ext not in extensions_b and ext not in add_extensions:
            add_extensions.append(ext)
    if add_extensions:
        conf_b.setProperty("merge-auto.extensions", ",".join(add_extensions))
