# vim: ts=3:sw=3:expandtab

import os
import re
import shutil
import sys
from collections.abc import Callable, Sequence
from types import ModuleType
from typing import Any, TextIO, cast, final

import golem
import golem.model
import golem.properties
import golem.util.constants
import golem.util.main_misc
import golem.util.olp_objects
import golem.util.olp_options
import golem.util.tools
from golem.installation import GOLEM_REVISION, GOLEM_VERSION
from golem.model import update_zero
from golem.model.particle import Particle
from golem.util.config import GolemConfigError, Properties, PropValue, split_power
from golem.util.main_misc import fill_config

try:
    from multiprocess import Pool
except ModuleNotFoundError:
    Pool = None

import logging

logger = logging.getLogger(__name__)


@final
class OLPSubprocess:
    def __init__(
        self,
        id: int,
        process_name: str,
        process_path: str,
        p_ini: list[Particle],
        p_fin: list[Particle],
        key: Sequence[str | int],
        conf: Properties,
    ):
        self.id = id
        self.process_name = process_name
        self.process_path = process_path
        self.p_ini = p_ini
        self.p_fin = p_fin
        self.crossings: dict[str, str] = {}
        self.crossings_conf: dict[int, Properties] = {}
        self.crossings_p_ini: dict[int, list[Particle]] = {}
        self.crossings_p_fin: dict[int, list[Particle]] = {}
        self.ids = {id: process_name}
        self.channels: dict[int, list[int]] = {}
        self.key = key
        self.conf = conf
        self.crossings_conf[id] = conf
        self.crossings_p_ini[id] = p_ini
        self.crossings_p_fin[id] = p_fin

        self.num_legs = len(p_ini) + len(p_fin)
        self.num_helicities = -1
        self.generated_helicities = []

    def addCrossing(
        self,
        id: int,
        process_name: str,
        p_ini: list[Particle],
        p_fin: list[Particle],
        conf: Properties,
    ):
        self.crossings[process_name] = "%s > %s" % (
            " ".join(map(str, p_ini)),
            " ".join(map(str, p_fin)),
        )
        self.ids[id] = process_name
        self.crossings_conf[id] = conf
        self.crossings_p_ini[id] = p_ini
        self.crossings_p_fin[id] = p_fin

    def removeCrossing(self, id: int):
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

    def assignChannels(self, id: int, channels: list[int]):
        self.channels[id] = channels

    def assignNumberHelicities(self, nh: int, gh: list[int]):
        self.num_helicities = nh
        self.generated_helicities = gh

    def getkey(self):
        return list(self.key)

    def getIDs(self):
        return list(self.ids.keys())

    def getIDConf(self, id: int):
        return self.crossings_conf[id]

    def __str__(self):
        return self.process_name

    def __int__(self):
        return self.id

    def getPath(self, path: str | None = None):
        if path is None:
            return self.process_path
        else:
            return os.path.join(path, self.process_path)

    def getConf(self, conf: Properties, path: str, base: None | Properties = None):
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
                "%s: %s" % (name, process)
                for name, process in list(self.crossings.items())
            ]

        return subproc_conf


def getSubprocess(
    olpname: str,
    id: int,
    inp: list[str],
    out: list[str],
    subprocesses: dict[tuple[str | int, ...], OLPSubprocess],
    _subprocesses_flav: dict[tuple[str | int, ...], OLPSubprocess],
    model: ModuleType,
    use_crossings: bool,
    conf: Properties,
) -> tuple[OLPSubprocess, bool]:
    def getparticle(name: str):
        return golem.util.tools.interpret_particle_name(name, model)

    p_ini = list(map(getparticle, inp))
    p_fin = list(map(getparticle, out))

    # replace special characters by placeholders, so the particle names can be used by other code
    replace_specials = {"~": "__tilde__", "+": "__plus__", "-": "__minus__"}

    s_ini: list[str] = []
    s_fin: list[str] = []

    for p in p_ini:
        s = str(p)
        for k, v in replace_specials.items():
            s = s.replace(k, v)
        s_ini.append(s)
    for p in p_fin:
        s = str(p)
        for k, v in replace_specials.items():
            s = s.replace(k, v)
        s_fin.append(s)

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
            if skey[: len(key)] == key and is_config_compatible(
                subprocesses[skey].conf, conf
            ):
                key = skey
                break

    if (
        key in subprocesses
        and use_crossings
        and is_config_compatible(subprocesses[key].conf, conf)
    ):
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
        sp = OLPSubprocess(
            id, process_name, process_name, p_ini, p_fin, originalkey, conf
        )
        subprocesses[key] = sp
        is_new = True

    return sp, is_new


def get_sp_key(
    p_ini: list[Particle], p_fin: list[Particle], use_crossings: bool, conf: Properties
) -> tuple[str, ...]:
    if use_crossings:
        pflvgrps = cast(list[str], conf.getProperty(golem.properties.flavour_groups))
        if pflvgrps != [] and pflvgrps != [""]:
            # The following piece of code constructs the channel key respecting
            # the given flavour groups/classes. Nested structure needed to deal
            # with all the possible cases occuring for multiple quark lines.

            # translate flavour_groups property into list of list -> flvgrps
            # set up dictionary to translate pdg codes into flavour group identifiers -> flvgrps_dict
            flvgrps: list[list[int]] = []
            flvgrps_dict: dict[int, tuple[int, str]] = {}
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
            key_fg: list[str | None] = [None for _ in range(len(pdg_proc))]
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
                    if (
                        i == 0
                        and generations
                        and pj[0] in flvgrps_dict
                        and pj[1] in flvgrps_dict
                    ):
                        if abs(pj[0]) == 1 or abs(pj[0]) == 2:
                            gp = 1
                        elif abs(pj[0]) == 3 or abs(pj[0]) == 4:
                            gp = 2
                        elif abs(pj[0]) == 5 or abs(pj[0]) == 6:
                            gp = 3
                        else:
                            logger.critical(
                                "Particle pdg("
                                + str(pj[0])
                                + ") does not belong to a known quark flavour generation!"
                            )
                            sys.exit("GoSam terminated due to an error")
                        gen_key[gp - 1] = gen_key[gp - 1] + 1

            # sort to catch cases like (u ub u ub -> s sb) <-> (c cb c cb -> d db)
            # => Not the actual number of occurences per generation is important, but their relative distribution
            gen_key.sort()
            conf["gen_key"] = gen_key

            key = tuple(sorted(cast(list[str], key_fg)))
        else:
            key = tuple(sorted(list(map(str, p_ini)) + [p.getPartner() for p in p_fin]))
    else:
        key = tuple(list(map(str, p_ini)) + [p.getPartner() for p in p_fin])

    return key


def is_config_compatible(conf1: Properties, conf2: Properties) -> bool:
    """Checks if a subprocess with conf2 can be a crossing of conf1"""
    special: dict[str, Callable[[str, str], bool]] = {
        "olp.amplitudetype": (lambda a, b: True),  # => ignored
        "olp.no_loop_level": (lambda a, b: True),  # => ignored
        "order": (lambda a, b: a.startswith(b) or b.startswith(a)),
    }
    for i in conf1:
        if i not in conf2 or conf1[i] != conf2[i]:
            bval = str(conf2[i]) if i in conf2 else ""
            if i in special:
                if special[i](str(conf1[i]), bval):
                    continue
            return False
    for i in conf2:
        if i not in conf1:
            if i in special:
                if special[i]("", str(conf2[i])):
                    continue
            return False
    return True


def adapt_config(conf1: Properties, conf2: Properties):
    """Adapt the configuration conf1 of a subprocess
    that a subprocess with conf2 can be a crossing of it."""
    conf1["olp.no_tree_level"] = cast(PropValue, conf1["olp.no_tree_level"]) and cast(
        PropValue, conf2["olp.no_tree_level"]
    )
    conf1["olp.no_loop_level"] = cast(PropValue, conf1["olp.no_loop_level"]) and cast(
        PropValue, conf2["olp.no_loop_level"]
    )
    conf1["order"] = max(
        cast(str, conf1["order"]), cast(str, conf2["order"])
    )  # take longest


def derive_output_name(input_name: str, pattern: str, dest_dir: str | None = None):
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


def derive_coupling_names(
    model_path: str | None, conf: Properties
) -> tuple[str, str, list[str]]:
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

    strong_couplings_found: dict[str, str] = {}
    weak_couplings_found: dict[str, str] = {}
    candidates: list[str] = []

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

    qcd_name = None
    if len(strong_couplings_found) == 0:
        logger.critical(
            "Invalid model file: cannot determine name of strong coupling.\n"
            + "Candidates are:"
            + ",".join(candidates)
        )
        sys.exit("GoSam terminated due to an error")
    else:
        for name in strong_coupling_names:
            if name in strong_couplings_found:
                qcd_name = strong_couplings_found[name]
                break

    qed_name = None
    if len(weak_couplings_found) == 0:
        logger.critical(
            "Invalid model file: cannot determine name of weak coupling.",
            "Candidates are:" + ",".join(candidates),
        )
        sys.exit("GoSam terminated due to an error")
    else:
        for name in weak_coupling_names:
            if name in weak_couplings_found:
                qed_name = weak_couplings_found[name]
                break

    all_couplings = list(strong_couplings_found.values()) + list(
        weak_couplings_found.values()
    )

    return cast(str, qcd_name), cast(str, qed_name), all_couplings


def get_power(conf: Properties) -> list[str | int]:
    """
    Returns two lists:
       list of length three: [coupling_name, born_power, virt_power]
    The list specifies the option 'order'.

    If the list is empty the process is not specified unambiguously.
    """
    alpha_power = cast(int | None, conf.getProperty("olp.alphapower", default=None))
    alphas_power = cast(int | None, conf.getProperty("olp.alphaspower", default=None))
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
                raise GolemConfigError(
                    "Requested QCD corrections without specifying strong coupling order"
                )
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
                raise GolemConfigError(
                    "Requested QCD corrections without specifying strong coupling order"
                )
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
                    raise GolemConfigError(
                        "Requested EW corrections without specifying electroweak coupling order"
                    )
                else:
                    ew_loop_power = ew_tree_power + 2
                qcd_loop_power = qcd_tree_power
            elif correction_type == "QCD":
                if qcd_tree_power is None:
                    raise GolemConfigError(
                        "Requested QCD corrections without specifying strong coupling order"
                    )
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


def derive_zero_masses(
    model_path: str | None, slha_file: str, conf: Properties
) -> list[str]:
    mod_params = golem.util.olp_objects.SUSYLesHouchesFile(slha_file)
    # ---#[ Load model file as module:
    mod = golem.util.tools.getModel(conf, model_path)
    # ---#] Load model file as module:

    result: list[str] = []
    for _, part in cast(dict[str, Particle], mod.particles).items():
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
    conf: Properties,
    subprocess: OLPSubprocess,
    subprocess_key: tuple[str | int, ...],
    subprocesses_conf: list[Properties],
    path: str,
    from_scratch: bool,
    no_clean: bool,
    use_crossings: bool,
    _contract_file: golem.util.olp_objects.OLPContractFile,
) -> tuple[
    dict[tuple[int | str, ...], OLPSubprocess], dict[int, Any], dict[int, Properties]
]:
    helicities: dict[int, Any] = {}
    subprocesses: dict[tuple[int | str, ...], OLPSubprocess] = {}
    subprocesses_conf_short: dict[int, Properties] = {}

    GOLEM_FULL = "GoSam %s" % ".".join(map(str, GOLEM_VERSION))

    process_path = subprocess.getPath(path)
    subprocess_conf = subprocess.getConf(subprocesses_conf[int(subprocess)], path)
    subprocess_conf["golem.name"] = "GoSam"
    subprocess_conf["golem.version"] = ".".join(map(str, GOLEM_VERSION))
    subprocess_conf["golem.full-name"] = GOLEM_FULL
    subprocess_conf["golem.revision"] = GOLEM_REVISION

    golem.util.tools.POSTMORTEM_CFG = subprocess_conf

    try:
        golem.util.main_misc.workflow(subprocess_conf)
        merge_extensions(subprocess_conf, conf)

        golem.util.main_misc.generate_process_files(subprocess_conf, from_scratch, no_clean)

        # ---[ Handle Crossings:

        if use_crossings and any(
            [
                kw in cast(str, subprocess_conf.getProperty(fltr))
                if subprocess_conf.getProperty(fltr)
                else False
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
                    sp_conf["golem.version"] = ".".join(map(str, GOLEM_VERSION))
                    sp_conf["golem.full-name"] = GOLEM_FULL
                    sp_conf["golem.revision"] = GOLEM_REVISION

                    golem.util.tools.POSTMORTEM_CFG = sp_conf

                    try:
                        golem.util.main_misc.workflow(sp_conf)

                        # Generate the files for the crossing and apply the filters
                        golem.util.main_misc.generate_process_files(
                            sp_conf, from_scratch, no_clean
                        )

                        # If the crossing is also vetoed, it has to be kept as separate subprocess and be
                        # removed from the list of crossings of the original subprocess
                        if sp_conf.getBooleanProperty("veto_crossings"):
                            subprocess.removeCrossing(id)
                            helicities[id] = list(
                                golem.util.tools.enumerate_and_reduce_helicities(
                                    sp_conf
                                )
                            )

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
                                    parent_key = cast(tuple[str | int, ...], key)
                                    keep_subprocess = False
                                else:
                                    parent_subprocess.addCrossing(
                                        sp.id,
                                        sp.process_name,
                                        sp.p_ini,
                                        sp.p_fin,
                                        sp.conf,
                                    )
                                subprocess.removeCrossing(sp.id)

                    except GolemConfigError as err:
                        logger.critical("Configuration file is not sound:" + str(err))
                        sys.exit("GoSam terminated due to an error")

            # Regenerate process files for the original subprocess with new list of crossings
            shutil.rmtree(process_path)
            os.mkdir(process_path)
            subprocess_conf = subprocess.getConf(
                subprocesses_conf[int(subprocess)], path
            )
            subprocess_conf["golem.name"] = "GoSam"
            subprocess_conf["golem.version"] = ".".join(map(str, GOLEM_VERSION))
            subprocess_conf["golem.full-name"] = GOLEM_FULL
            subprocess_conf["golem.revision"] = GOLEM_REVISION
            golem.util.main_misc.workflow(subprocess_conf)
            golem.util.main_misc.generate_process_files(subprocess_conf, from_scratch, no_clean)
            # Regenerate process files for new parent subprocess if it exists
            if parent_subprocess:
                parent_path = os.path.join(path, str(parent_subprocess))
                shutil.rmtree(parent_path)
                os.mkdir(parent_path)
                parent_conf = parent_subprocess.getConf(
                    subprocesses_conf[int(parent_subprocess)], path
                )
                parent_conf["golem.name"] = "GoSam"
                parent_conf["golem.version"] = ".".join(map(str, GOLEM_VERSION))
                parent_conf["golem.full-name"] = GOLEM_FULL
                parent_conf["golem.revision"] = GOLEM_REVISION
                golem.util.main_misc.workflow(parent_conf)
                golem.util.main_misc.generate_process_files(parent_conf, from_scratch, no_clean)
                helicities[parent_subprocess.id] = list(
                    golem.util.tools.enumerate_and_reduce_helicities(parent_conf)
                )

                subprocesses_conf_short[parent_subprocess.id] = parent_conf
                subprocesses[cast(tuple[str | int, ...], parent_key)] = (
                    parent_subprocess
                )

        helicities[subprocess.id] = list(
            golem.util.tools.enumerate_and_reduce_helicities(subprocess_conf)
        )

    except GolemConfigError as err:
        logger.critical("Configuration file is not sound:" + str(err))
        sys.exit("GoSam terminated due to an error")

    subprocesses[subprocess_key] = subprocess
    subprocesses_conf_short[subprocess.id] = subprocess_conf

    return subprocesses, helicities, subprocesses_conf_short


def process_order_file(
    order_file_name: str,
    f_contract: TextIO,
    path: str,
    default_conf: Properties,
    templates: list[str] | str | None = None,
    ignore_case: bool = False,
    ignore_unknown: bool = False,
    from_scratch: bool = False,
    no_clean: bool = False,
    mc_name: str = "any",
    use_crossings: bool = True,
    **opts: bool | str,
) -> int:
    syntax_extensions = ["single_quotes", "double_quotes", "backslash_escape"]

    extensions: dict[str, bool] = {}
    for ex in syntax_extensions:
        if ex in opts:
            extensions[ex] = opts[ex]
        else:
            extensions[ex] = False

    logger.debug("Processing order file at %r" % order_file_name)
    GOLEM_FULL = "GoSam %s" % ".".join(map(str, GOLEM_VERSION))
    result = 0

    conf = Properties()
    conf += default_conf

    # check if any model.options are set in the config file (before filling in the defaults)
    config_model_options = conf.getListProperty("model.options") != []
    conf.setProperty("olp.config_model_options", config_model_options)

    if "regularisation_scheme" in default_conf:
        config_ir_scheme = cast(str, default_conf["regularisation_scheme"]).upper()
    else:
        config_ir_scheme = None

    ext_ir_scheme = None
    cfg_extensions = cast(list[str], default_conf["extensions"])
    if "dred" in cfg_extensions and "thv" in cfg_extensions:
        logger.critical(
            "Multiple regularisation schemes specified in extensions: thv and dred. Please pick one."
        )
        sys.exit("GoSam terminated due to an error")
    if "dred" in cfg_extensions:
        ext_ir_scheme = "DRED"
    if "thv" in cfg_extensions:
        ext_ir_scheme = "THV"

    # check consistency of regularisation schemes in setup file (if present)
    if config_ir_scheme is not None and ext_ir_scheme is not None:
        if config_ir_scheme != ext_ir_scheme:
            logger.critical(
                "Incompatible settings between regularisation_scheme and extensions: "
                + "%r vs. %r" % (config_ir_scheme, ext_ir_scheme)
            )
            sys.exit("GoSam terminated due to an error")

    if "olp_process_name" in opts:
        olp_process_name = cast(str, opts["olp_process_name"]).strip().lower()
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

    for pi_key in cast(list[str], conf.getListProperty("mc_specials.keys")):
        if pi_key == "":
            continue
        if pi_key in default_conf:
            if (
                conf["mc_specials." + pi_key] != conf[pi_key]
                and conf[pi_key] is not None
                and conf[pi_key] != ""
            ):
                logger.warning(
                    "Your BLHA order file '%s' specifies the property '%s' in a special '#@' instruction.\n"
                    "It will overwrite the default and/or the value given in the config file\n'%s':\n%s -> %s\n"
                    "Please check that this is really what you want to do! "
                    % (
                        order_file_name,
                        pi_key,
                        conf["extra_setup_file"],
                        conf[pi_key],
                        conf["mc_specials." + pi_key],
                    )
                )
        key = pi_key.removeprefix("mc_specials")
        if key == "extensions":
            conf["extensions"] = (
                cast(str, conf["mc_specials.extensions"])
                if conf["extensions"] == ""
                else cast(str, conf["extensions"])
                + ","
                + cast(str, conf["mc_specials.extensions"])
            )
        else:
            conf[key] = cast(str, conf["mc_specials." + pi_key])
        conf._del("mc_specials." + pi_key)

    contract_file = golem.util.olp_objects.OLPContractFile(order_file)

    tmp_contract_file = golem.util.olp_objects.OLPContractFile(order_file)
    subprocesses_conf: list[Properties] = []

    conf.setProperty("setup-file", order_file_name)
    orig_conf = conf.copy()

    file_ok = golem.util.olp_options.process_olp_options(
        contract_file, conf, ignore_case, ignore_unknown
    )

    for subprocess_number, (lineo, _, _, _) in enumerate(
        order_file.processes_ordered()
    ):
        subconf = orig_conf.copy()
        subconf.activate_subconfig(subprocess_number)
        file_ok = golem.util.olp_options.process_olp_options(
            tmp_contract_file, subconf, ignore_case, ignore_unknown, lineo, quiet=True
        )
        subprocesses_conf.append(subconf)

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
         
        ir_scheme = cast(str, lconf["olp.irregularisation"]).upper()
        ext = cast(list[str], lconf.getListProperty(golem.properties.extensions))
        uext = [s.upper() for s in ext] 

        # check BLHA regularisation scheme vs regularisation_scheme or extensions in setup file (if present)
        mismatch_schemes = [False, None] 
        if ir_scheme == "CDR":
            logger.warning(
                "GoSam results are returned in the 't Hooft-Veltman scheme,\n"
                "which differs from requested CDR scheme at O(eps). For \n"
                "ordinary NLO calculations this should not be a problem."
            )
            ir_scheme = "THV" 
        if config_ir_scheme is not None:
            if config_ir_scheme != ir_scheme:
                mismatch_schemes = [True, config_ir_scheme]
        if ext_ir_scheme is not None:
            if ext_ir_scheme != ir_scheme:
                mismatch_schemes = [True, ext_ir_scheme] 

        if mismatch_schemes[0]:
            logger.critical(
                "IR regularisation scheme specified in BLHA-file conflicts with "
                "scheme specified in config file(s)\n %r:\n %r vs. %r"
                % (default_conf["extra_setup_file"], ir_scheme, mismatch_schemes[1])
            )
            sys.exit("GoSam terminated due to an error") 

        # choose behaviour according to table above
        if ir_scheme == "DRED":
            if "DRED" not in uext:
                lconf["olp." + str(golem.properties.extensions)] = "DRED"
        elif ir_scheme == "THV":
            if config_ir_scheme is None and ext_ir_scheme is None:
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
        golem.util.tools.prepare_model_files(conf, imodel_path)
        conf["modeltype"] = conf.getListProperty("model")[-1]
        conf["model"] = os.path.join(imodel_path, golem.util.constants.MODEL_LOCAL)
        for lconf in subprocesses_conf:
            lconf["is_ufo"] = cast(bool, conf.getBooleanProperty("is_ufo"))
            if conf.getBooleanProperty("is_ufo"):
                lconf["modeltype"] = lconf.getListProperty("model")[-1]
            else:
                lconf["modeltype"] = conf.getListProperty("model")[-1]
            lconf["model"] = os.path.join(imodel_path, golem.util.constants.MODEL_LOCAL)
        # ---#] Import model file once for all subprocesses:
        # ---#[ Constrain masses:
        model_file = cast(str | None, conf["olp.modelfile"])
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
            if (
                model_conf.getProperty(p)
                or not model_conf.getProperty(p)
                or model_conf.getProperty(p) == 0
            ):
                # Note that 'False'and '0' are actually valid values. We want to skip falsy values like [], " ", None, etc.
                model_conf.setProperty(
                    str(p), cast(PropValue, model_conf.getProperty(p))
                )

        model = golem.util.tools.getModel(model_conf, imodel_path)

        golem.util.tools.process_zero(conf, model)
        for subconf in subprocesses_conf:
            subconf.setProperty("zero", conf.getProperty("zero"))

        # ---#[ Setup excluded and massive particles :
        for lconf in [conf] + subprocesses_conf:
            list_exclude: list[str] = []
            for i in (
                [int(p) for p in cast(str, lconf["__excludedParticles__"]).split()]
                if lconf["__excludedParticles__"]
                else []
            ):
                for n in model.particles:
                    particle = model.particles[n]
                    if particle.getPDGCode() == i:
                        list_exclude.append(str(particle))
            if list_exclude:
                if not lconf["filter.particles"]:
                    lconf["filter.particles"] = ",".join(f"{p}:0" for p in list_exclude)
                else:
                    lconf["filter.particles"] = (
                        cast(str, lconf["filter.particles"])
                        + ","
                        + ",".join(f"{p}:0" for p in list_exclude)
                    )

            lconf["__excludedParticles__"] = None
 

        # ---#[ Setup couplings :
        for lconf in [conf] + subprocesses_conf:
            _, _, all_couplings = derive_coupling_names(imodel_path, lconf)
            coupling_power = get_power(lconf)

            if len(coupling_power) == 0:
                contract_file.setPropertyResponse(
                    "CorrectionType",
                    [
                        "Error:",
                        "Wrong or missing entries in",
                        "CorrectionType, AlphaPower or AlphasPower",
                    ],
                )
                file_ok = False
            else:
                lconf[golem.properties.coupling_power] = ",".join(
                    map(str, coupling_power)
                )

            if "olp.operationmode" in lconf:
                strip_couplings = "CouplingsStrippedOff" in lconf.getListProperty(
                    "olp.operationmode"
                )
            else:
                strip_couplings = False

            if strip_couplings:
                ones = cast(list[str], lconf.getListProperty(golem.properties.one))
                for coupling in all_couplings:
                    if coupling not in ones:
                        ones.append(coupling)
                lconf[golem.properties.one] = ",".join(ones)
                conf["nlo_prefactors"] = 0
        # ---#] Setup couplings :


    # ---#[ Iterate over subprocesses:
    subdivide = cast(str, conf.getProperty("olp.subdivide", "no")).lower() in [
        "yes",
        "true",
        "1",
    ]
    channels: dict[int, list[int]] = {}
    chelis = {}
    helicities: dict[int, Any] = {}
    max_occupied_channel = -1
    subprocesses: dict[tuple[str | int, ...], OLPSubprocess] = {}
    subprocesses_flav: dict[tuple[str | int, ...], OLPSubprocess] = {}

    subprocesses_conf_short: dict[int, Properties] = {}

    if file_ok:
        assert model
        for _, id, inp, outp in contract_file.processes_ordered():
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

        if (
            False
        ):  # Pool: TODO: FeynGraph models can currently not be shared between processes
            with Pool(conf.getIntegerProperty("n_jobs")) as pool:
                print(conf)
                sp_res = pool.map(
                    lambda sp: handle_subprocess(
                        conf,
                        sp[1],
                        sp[0],
                        subprocesses_conf,
                        path,
                        from_scratch,
                        no_clean,
                        use_crossings,
                        contract_file,
                    ),
                    subprocesses.items(),
                )
        else:
            sp_res = list(
                map(
                    lambda sp: handle_subprocess(
                        conf,
                        sp[1],
                        sp[0],
                        subprocesses_conf,
                        path,
                        from_scratch,
                        no_clean,
                        use_crossings,
                        contract_file,
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
                generated_helicities = cast(
                    list[int],
                    [t[0] for t in [t for t in helicities[sp.id] if t[1] is None]],
                )
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

                contract_file.setProcessResponse(sp_id, list(map(str, channels[sp_id])))
                sp.assignChannels(sp_id, channels[sp_id])
                sp.assignNumberHelicities(len(helicities[sp.id]), generated_helicities)

    # ---#] Iterate over subprocesses:
    # ---#[ Write output file:
    f_contract.write("# vim: syntax=olp\n")
    f_contract.write("#@OLP GoSam %s\n" % ".".join(map(str, GOLEM_VERSION)))
    f_contract.write("#@IgnoreUnknown %s\n" % ignore_unknown)
    f_contract.write("#@IgnoreCase %s\n" % ignore_case)
    f_contract.write(
        "#@SyntaxExtensions %s\n"
        % " ".join([i for i in list(extensions.keys()) if extensions[i]])
    )
    try:
        contract_file.store(f_contract)
    except IOError as err:
        raise golem.util.olp_objects.OLPError("while writing contract file: %s" % err)
    # ---#] Write output file:

    # Contract file is written, no we can stop if there were any errors
    if not file_ok:
        logger.critical(
            "Your BLHA order file could not be processed properly.\n"
            "Please, check configuration and contract files for errors!"
        )
        sys.exit("GoSam terminated due to an error")

    # ---#[ Process global templates:

    if templates is None:
        templates = ""

    if templates == "":
        templates = golem.util.tools.golem_path("olp", "templates")

    ext = golem.properties.getExtensions(conf)

    # This fills in the defaults where no option is given:
    for p in golem.properties.properties:
        if conf.getProperty(p) or not conf.getProperty(p) or conf.getProperty(p) == 0:
            # Note that 'False'and '0' are actually valid values a property can be set to.
            conf.setProperty(str(p), cast(PropValue, conf.getProperty(p)))
        else:
            # this catches all falsy values like [], None, " ", etc., which mean
            # the property is not set yet. But not '0' and the acual bool 'False',
            # which we checked for above, since those ARE possible values for a property.
            conf.setProperty(str(p), cast(PropValue, p.getDefault()))

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
    conf["golem.version"] = ".".join(map(str, GOLEM_VERSION))
    conf["golem.full-name"] = GOLEM_FULL
    conf["golem.revision"] = GOLEM_REVISION

    orders = split_power(
        ",".join(map(str, conf.getListProperty(golem.properties.coupling_power)))
    )
    powers = orders[0] if orders else []

    generate_tree_diagrams = False
    generate_loop_diagrams = False
    if len(powers) == 2:
        generate_tree_diagrams = True
        generate_loop_diagrams = False
        is_loopinduced = False
    elif len(powers) == 3:
        generate_tree_diagrams = str(powers[1]).strip().lower() != "none"
        generate_loop_diagrams = True
        is_loopinduced = not generate_tree_diagrams

    conf["generate_tree_diagrams"] = generate_tree_diagrams
    conf["generate_loop_diagrams"] = generate_loop_diagrams

    generate_counterterms = (
        cast(bool, conf.getBooleanProperty("renorm")) 
        and generate_loop_diagrams 
        and not is_loopinduced
    )

    conf["generate_counterterms"] = generate_counterterms

    if "ewchoose" in golem.model.MODEL_OPTIONS:
        conf.setProperty("ewchoose", str(golem.model.MODEL_OPTIONS["ewchoose"]))
    else:
        conf.setProperty("ewchoose", False)

    # ---] Fill in information needed by the main config to generate the common source files

    # ---[ Optimize common model files (in case of UFO model and optimized_import=True)
    if conf.getBooleanProperty("is_ufo") and conf.getBooleanProperty(
        "optimized_import"
    ):
        golem.util.tools.optimize_model(
            conf,
            os.path.dirname(cast(str, conf["model"])),
            olp=True,
            sconf=subprocesses_conf_short,
        )
        # Reload model:
        _ = golem.util.tools.getModel(conf, os.path.join(path, "model"))
    # ---] Optimize common model files

    golem.templates.xmltemplates.transform_templates(
        templates,
        path,
        conf.copy(),
        conf=conf,
        subprocesses=sorted(list(subprocesses.values()), key=lambda sp: sp.id),
        subprocesses_conf=[
            sp
            for _, sp in sorted(subprocesses_conf_short.items(), key=lambda spi: spi[0])
        ],
        contract=contract_file,
        user="olp",
    )

    # ---#] Process global templates:

    if not no_clean:
        golem.util.main_misc.cleanup(os.path.join(path, "model"))

    return result


def mc_specials(conf: Properties, order_file: golem.util.olp_objects.OLPOrderFile):
    pi_keys: list[str] = []
    for pi in order_file.processing_instructions():
        pi_parts = pi.strip().split(" ", 1)
        if pi_parts[0] == "regularisation_scheme":
            logger.critical(
                "Property 'regularisation_scheme' cannot be set as a '#@' instruction in the BLHA order file!\n"
                "Please only use BLHA's 'IRregularisation' keyword."
            )
            sys.exit("GoSam terminated due to an error")
        if pi_parts[0] == "extensions":
            if any(
                irs in [ext.lower() for ext in pi_parts[1].split(",")]
                for irs in ["dred", "thv"]
            ):
                logger.critical(
                    "IR regularisation scheme ('dred' or 'thv') cannot be added to 'extensions'\n"
                    "in a '#@' instruction in the BLHA order file! Please only use BLHA's 'IRregularisation' keyword."
                )
                sys.exit("GoSam terminated due to an error")
        pi_keys.append(pi_parts[0])
        if len(pi_parts) == 2:
            conf.setProperty("mc_specials." + pi_parts[0], pi_parts[1])
        else:
            conf.setProperty("mc_specials." + pi_parts[0], True)
    conf.setProperty("mc_specials.keys", pi_keys)

    overwrite_warn = False

    mc_name = cast(str, conf.getProperty("olp.mc.name")).lower().strip()

    mc_special_mc_name = ""
    if mc_name != "any":
        if conf.getProperty("mc_specials.olp.mc.name") is not None:
            mc_special_mc_name = (
                cast(str, conf.getProperty("mc_specials.olp.mc.name")).lower().strip()
            )
            if mc_name != mc_special_mc_name:
                overwrite_warn = True
    elif conf.getProperty("mc_specials.olp.mc.name") is not None:
        mc_name = cast(str, conf.getProperty("mc_specials.olp.mc.name")).lower().strip()

    s = ""
    mc_special_s = ""
    if conf.getProperty("olp.mc.version") is not None:
        s = cast(str, conf.getProperty("olp.mc.version", default="")).strip()
        if conf.getProperty("mc_specials.olp.mc.version") is not None:
            mc_special_s = cast(
                str, conf.getProperty("mc_specials.olp.mc.version", default="")
            ).strip()
            if s != mc_special_s:
                overwrite_warn = True
    elif conf.getProperty("mc_specials.olp.mc.version") is not None:
        s = cast(
            str, conf.getProperty("mc_specials.olp.mc.version", default="")
        ).strip()

    if overwrite_warn:
        old_mc = (
            mc_special_mc_name
            if mc_special_s == ""
            else mc_special_mc_name + "/" + mc_special_s
        )
        new_mc = mc_name if s == "" else mc_name + "/" + s
        logger.warning(
            "Command line argument --mc %s overwrites #@ instruction in BLHA order file: %s -> %s "
            % (new_mc, old_mc, new_mc)
        )

    required_extensions: list[str] = []

    if mc_name == "any":
        pass
    elif mc_name == "powheg" or mc_name == "powhegbox":
        required_extensions.extend(["f77"])
        required_extensions.extend(["olp_badpts"])
    elif mc_name == "amcatnlo":
        required_extensions.extend(["f77"])
    else:
        logger.warning(
            "Unknown Monte Carlo program passed via the --mc argument: %s. This statement will be IGNORED!"
            % (mc_name)
        )

    extensions = golem.properties.getExtensions(conf)
    add_extensions: list[str] = []
    for ext in required_extensions:
        if ext not in extensions:
            add_extensions.append(ext)
    if len(add_extensions) > 0:
        conf.setProperty("%s-auto.extensions" % mc_name, ",".join(add_extensions))


def merge_extensions(conf_a: Properties, conf_b: Properties):
    """merge extensions from conf_a into conf_b"""

    extensions_a = golem.properties.getExtensions(conf_a)
    extensions_b = golem.properties.getExtensions(conf_b)

    add_extensions = []
    if conf_b.getProperty("merge-auto.extensions"):
        add_extensions = cast(str, conf_b.getProperty("merge-auto.extensions")).split(
            ","
        )
    for ext in extensions_a:
        if ext and ext not in extensions_b and ext not in add_extensions:
            add_extensions.append(ext)
    if add_extensions:
        conf_b.setProperty("merge-auto.extensions", ",".join(add_extensions))
