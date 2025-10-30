# vim: ts=3:sw=3
import sys
import os
import os.path
import io
import hashlib
import re

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

from golem.util.path import golem_path
from golem.util.tools import copy_file, generate_particle_lists

from golem.util.config import GolemConfigError, split_qgrafPower

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_qgraf import *
from golem.installation import GOLEM_VERSION, GOLEM_REVISION, LIB_DIR

import logging

logger = logging.getLogger(__name__)

def generate_process_files(conf, from_scratch=False):
    """
    This routine is a wrapper around anything that needs to be done
    for creating a new process.
    """
    # properties will be filled later:
    props = golem.util.config.Properties()

    # This fills in the defaults where no option is given:
    for p in golem.properties.properties:
        props.setProperty(str(p), conf.getProperty(p))

    golem.properties.setInternals(conf)

    path = golem.util.tools.process_path(conf)

    templates = conf.getProperty(golem.properties.template_path)
    templates = os.path.expandvars(templates)

    if templates is None or len(templates) == 0:
        templates = golem_path("templates")

    for name in conf:
        props[name] = conf[name]

    if not os.path.exists(path):
        raise GolemConfigError("Process path does not exist: %s" % path)

    in_particles, out_particles = generate_particle_lists(conf)

    helicity_map = golem.util.tools.enumerate_and_reduce_helicities(conf)

    # Obtain the files required by QGraf from the template file.
    golem.templates.xmltemplates.transform_templates(
        templates,
        path,
        props,
        conf=conf,
        in_particles=in_particles,
        out_particles=out_particles,
        user="qgraf",
        from_scratch=from_scratch,
        helicity_map=helicity_map,
    )

    # First thing to be done because the Makefiles
    # Need to know the number of diagrams.
    run_qgraf(conf, in_particles, out_particles)

    # Run the new analyzer:
    logger.info("Analyzing diagrams")
    (
        keep_tree,
        keep_virt,
        keep_vtot,
        eprops,
        keep_ct,
        loopcache,
        loopcache_tot,
        tree_signs,
        flags,
        massive_bubbles,
        treecache,
        ctcache,
        ct_signs,
    ) = run_analyzer(path, conf, in_particles, out_particles)
    # keep_tree, keep_virt, keep_ct, loopcache, tree_signs, flags, massive_bubbles = \
    # run_analyzer(path, conf, in_particles, out_particles)

    props.setProperty("topolopy.keep.tree", ",".join(map(str, keep_tree)))
    props.setProperty("topolopy.keep.virt", ",".join(map(str, keep_virt)))
    props.setProperty("topolopy.keep.vtot", ",".join(map(str, keep_vtot)))
    props.setProperty("topolopy.keep.ct", ",".join(map(str, keep_ct)))
    props.setProperty("topolopy.count.tree", len(keep_tree))
    props.setProperty("topolopy.count.virt", len(keep_virt))
    props.setProperty("topolopy.count.docu", len(keep_vtot))
    props.setProperty("topolopy.count.ct", len(keep_ct))
    props.setProperty("templates", templates)
    props.setProperty("process_path", path)
    props.setProperty("max_rank", conf["__max_rank__"])

    if conf.getBooleanProperty("write_vanishing_amplitude"):
        props.setProperty("write_vanishing_amplitude", "true")
    else:
        props.setProperty("write_vanishing_amplitude", "false")

    conf["__info.count.tree__"] = len(keep_tree)
    conf["__info.count.virt__"] = len(keep_virt)
    conf["__info.count.docu__"] = len(keep_vtot)
    conf["__info.count.ct__"] = len(keep_ct)

    for key, value in list(golem.util.tools.derive_coupling_names(conf).items()):
        props.setProperty("%s_COUPLING_NAME" % key, value)

    # Create and populate subdirectories
    golem.templates.xmltemplates.transform_templates(
        templates,
        path,
        props,
        conf=conf,
        in_particles=in_particles,
        out_particles=out_particles,
        user="main",
        from_scratch=from_scratch,
        treecache=treecache,
        loopcache=loopcache,
        loopcache_tot=loopcache_tot,
        tree_signs=tree_signs,
        # tree_flows=tree_flows,
        heavy_quarks=[p for p in conf.getListProperty("__heavy_quarks__") if len(p.strip()) > 0],
        lo_flags=flags[0],
        nlo_flags=flags[1],
        massive_bubbles=massive_bubbles,
        diagram_sum=eprops,
        helicity_map=helicity_map,
        ctcache=ctcache,
        ct_signs=ct_signs,
        ct_flags=flags[2],
    )
    cleanup(path)


def cleanup(path):
    cleanup_files = []

    for ext in [".tex", ".log", ".py", ".pyc", ".pyo"]:
        for stub in ["pyxotree", "pyxovirt", "topotree", "topovirt", "pyxoct", "topoct"]:
            cleanup_files.append(stub + ext)

    if True:
        for ext in ["", ".py", ".pyc", ".pyo"]:
            cleanup_files.append("model" + ext)

    for filename in cleanup_files:
        full_name = os.path.join(path, filename)
        if os.path.exists(full_name):
            os.remove(full_name)


def find_config_files():
    """
    Searches for configuration files in the default locations.
    These are used to fill the fields of newly created input
    files by preferred defaults.

    The procedure looks in the following locations:
            <working directory>

    The follwing file names are considered configuration files
            .gosam
            .golem
            gosam.in
            golem.in
            gosam.conf
            golem.conf
    """
    props = golem.util.config.Properties()
    directories = [os.getcwd()]
    files = [".gosam", ".golem", "gosam.in", "golem.in", "gosam.conf", "golem.conf"]
    files_found = []
    avail_props = list(map(str, [p for p in golem.properties.properties]))
    for dir in directories:
        for file in files:
            full_name = os.path.join(dir, file)
            if os.path.exists(full_name):
                try:
                    with open(full_name, "r") as f:
                        props.load(f, avail_props)
                    files_found.append(os.path.abspath(file))
                except GolemConfigError as err:
                    logger.critical("Configuration file is not sound:" + str(err))
                    sys.exit("GoSam terminated due to an error")
    props.setProperty("pkg_config_path", os.path.join(LIB_DIR, "pkgconfig"))
    return props, files_found


def write_template_file(fname, defaults, format=None):
    """
    Creates a template file using the given default-configuration
    if present.

    fname --- name of the file to be created
    """
    width = 70  # line width
    tw = 3  # tab width

    logger.info("Writing template file %r" % fname)
    script = sys.argv[0]
    f = open(fname, "w")
    if format is None:
        f.write("#!/usr/bin/env " + script + "\n")
    elif format == "LaTeX":
        f.write("\\begin{basedescript}{\\desclabelstyle{\\pushlabel}}\n")
        f.write("\\setlength\\itemsep{30pt}\n")
    else:
        raise GolemConfigError("Unknown Format in write_template_file(..., %r)" % format)

    if format is None:
        for prop in defaults:
            if prop.startswith("$"):
                value = defaults[prop]
                f.write("%s=%s\n" % (prop, value))
    for prop in golem.properties.properties:
        changed = str(prop) in defaults.propertyNames()
        subprocess_specific_settings = False
        for k in defaults:
            if k.startswith(str(prop) + "["):
                subprocess_specific_settings = True
                changed = True
                break

        if prop.isExperimental() and not changed and not format == "LaTeX":
            continue
            pass
        if prop.isHidden() and not changed and not format == "LaTeX":
            continue
            pass

        if prop.getType() == str:
            stype = "text"
        elif prop.getType() == int:
            stype = "integer number"
        elif prop.getType() == bool:
            stype = "true/false"
        elif prop.getType() == list:
            stype = "comma separated list"
        else:
            stype = str(prop.getType())

        if format is None:
            text = "### %s (%s) " % (prop, stype)
            if len(text) < width:
                f.write("%s%s\n" % (text, "#" * (width - len(text))))
            else:
                f.write("%s\n" % text)
        elif format == "LaTeX":
            f.write(
                "\\item[\\colorbox{gray!30}{\\texttt{%s}}] (\\textit{%s})\n" % (str(prop).replace("_", "\\_"), stype.replace("_", "\\_"))
            )

        if format is None:
            for line in prop.getDescription().splitlines(False):
                text = "# %s" % (line.expandtabs(tw))
                if len(text) < width - 2:
                    f.write("%s%s #\n" % (text, " " * ((width - 2) - len(text))))
                else:
                    f.write("%s\n" % text)
            f.write("#" * width + "\n")
        elif format == "LaTeX":
            f.write("\\begin{verbatim}\n")
            first = True
            for line in prop.getDescription().splitlines(False):
                if first:
                    indent = len(line) - len(line.lstrip())
                    first = False
                    prev_empty = False

                text = line[indent:].rstrip()

                if text.strip() == "":
                    prev_empty = True
                else:
                    if prev_empty:
                        f.write("\n")
                    f.write(line[indent:].rstrip() + "\n")
                    prev_empty = False
            f.write("\\end{verbatim}\n")

        if format is None:
            if str(prop) in defaults.propertyNames():
                value = defaults.getProperty(prop)
                if isinstance(value, list):
                    value = ",".join(value)
                f.write("%s=%s\n" % (str(prop), value))
            elif prop.getDefault() is None:
                f.write("# %s=\n" % prop)
            else:
                f.write("# %s=%s\n" % (prop, prop.getDefault()))
            if subprocess_specific_settings:
                for k in defaults:
                    if k.startswith(str(prop) + "["):
                        f.write("%s=%s\n" % (k, defaults.getProperty(k)))
            f.write("\n")
        elif format == "LaTeX":
            if str(prop) == "qgraf.bin":
                f.write("Default: \\verb|<gosam-prefix>/bin/GoSam/qgraf|\n\\\\")
            elif str(prop) == "form.bin":
                f.write("Default: \\verb|<gosam-prefix>/bin/GoSam/tform|\n\\\\")
            else:
                if prop.getDefault() is not None:
                    value = str(prop.getDefault())
                    if len(value) > 0:
                        f.write("Default: \\verb|%s|\n\\\\" % value)
                    else:
                        f.write("Default: \\verb|\"\"|\n\\\\")
                else:
                        f.write("Default: \\verb|None|\n\\\\")

        if format == "LaTeX":
            if prop.isHidden() is not None:
                value = str(prop.isHidden())
                if len(value) > 0:
                    f.write("Hidden: \\verb|%s|\n\\\\" % value)

        if format == "LaTeX":
            if prop.isExperimental() is not None:
                value = str(prop.isExperimental())
                if len(value) > 0:
                    f.write("Experimental: \\verb|%s|\n\\\\" % value)

    if format is None:
        for prop in defaults:
            if prop.startswith("+") or prop.endswith(".extensions"):
                value = defaults[prop]
                f.write("%s=%s\n" % (prop, value))
    elif format == "LaTeX":
        f.write("\\end{basedescript}\n")
    f.close()


def read_golem_dir_file(path):
    """
    Looks for the file .golem.dir under the given path.
    """
    result = golem.util.config.Properties()

    dir_file = os.path.join(path, consts.GOLEM_DIR_FILE_NAME)
    if os.path.exists(dir_file):
        try:
            with open(dir_file, "r") as f:
                result.load(f)
        except GolemConfigError as err:
            logger.critical("Configuration file is not sound:" + str(err))
            sys.exit("GoSam terminated due to an error")

        ver = list(map(int, result["golem-version"].split(".")))

        # be compatible between internal 1.99 releases and 2.0.*
        if ver == [1, 99] and GOLEM_VERSION[:2] == [2, 0]:
            logger.warning(
                "This directory has been generated with an older version "
                + "of GoSam (%s).\n" % result["golem-version"]
                + "If you get compiler errors, you might need to remove all files\n"
                + "including '.golem.dir' and rerun gosam.py."
            )
            return result

        # be compatible to older 2.0.* releases
        if ver[:2] == [2, 0] and GOLEM_VERSION[:2] == [2, 0] and ver[:3] <= (GOLEM_VERSION[:3] + [0] * 5)[:3]:
            if ver[:3] != (GOLEM_VERSION[:3] + [0] * 5)[:3]:
                logger.warning(
                    "This directory has been generated with an older version "
                    + "of GoSam (%s).\n" % result["golem-version"]
                    + "If you get compiler errors, you might need to remove all files\n"
                    + "including '.golem.dir' and rerun gosam.py."
                )
                return result

        for gv, v in zip(GOLEM_VERSION + [0] * 5, ver):
            if gv > v:
                raise GolemConfigError(
                    "This directory has been generated with an older version "
                    + "of GoSam (%s).\n" % result["golem-version"]
                    + "Please, remove all files, including '.golem.dir' "
                    + "and rerun gosam.py."
                )
            elif gv < v:
                raise GolemConfigError(
                    "This directory has been generated with a newer version "
                    + "of GoSam (%s).\n" % result["golem-version"]
                    + "Please, remove all files, including '.golem.dir' "
                    + "and rerun gosam.py."
                )

    return result


def write_golem_dir_file(path, fname, conf):
    """
    Writes .golem.dir which will allow us later to identify
    this directory as a golem directory and to logically
    link it with the original setup file.

    PARAMETER

    path -- the path where the file should be located
    fname -- the name of the setup file used.
    """
    dir_info = golem.util.config.Properties()
    dir_info["setup-file"] = os.path.abspath(fname)
    if os.path.exists(os.path.abspath(fname)):
        dir_info["setup-file-sha1"] = hashlib.sha1(open(os.path.abspath(fname), "rb").read()).hexdigest()
    dir_info["golem-version"] = ".".join(map(str, GOLEM_VERSION))
    dir_info["golem-revision"] = str(GOLEM_REVISION)
    dir_info["process-name"] = conf.getProperty(golem.properties.process_name)
    dir_info["time-stamp"] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    with open(os.path.join(path, consts.GOLEM_DIR_FILE_NAME), "w") as f:
        dir_info.store(f, "Do not remove this file!")


def check_dont_overwrite(conf):
    path = golem.util.tools.process_path(conf)

    dir_info = read_golem_dir_file(path)

    if "setup-file" in dir_info:
        setup_file_conf = conf["setup-file"]
        setup_file_dir = dir_info["setup-file"]

        if not os.path.exists(setup_file_dir):
            raise GolemConfigError(
                "The directory %r contains files created by %r, " % (path, setup_file_dir)
                + "which does no longer exist.\n"
                + "If you actually want to overwrite these files "
                + "you need to remove the file %r in that directory." % consts.GOLEM_DIR_FILE_NAME
            )

        if not os.path.samefile(setup_file_conf, setup_file_dir):
            raise GolemConfigError(
                "The directory %r contains files created by %r, " % (path, setup_file_dir)
                + "which is not the same as %r.\n" % setup_file_conf
                + "If you actually want to overwrite these files "
                + "you need to remove the file %r in that directory." % consts.GOLEM_DIR_FILE_NAME
            )

def fill_config(conf):
    """
    Checks whether the combination of properties in the given config
    makes sense and sets additional properties based on the given
    ones.

    The additional properties are:

    generate_loop_diagrams
    generate_tree_diagrams
    generate_eft_counterterms
    is_loopinduced
    """

    # save the settings given in the process config file
    rc_conf = conf.copy()

    ini = conf.getProperty(golem.properties.qgraf_in)
    fin = conf.getProperty(golem.properties.qgraf_out)

    # Prepare a copy of the setup file in the property [% user.setup %]
    buf = io.StringIO()
    conf.store(
        buf,
        properties=golem.properties.properties,
        info=["golem.full-name", "golem.name", "golem.version", "golem.revision", "setup-file"],
    )
    conf.setProperty("user.setup", buf.getvalue())
    buf.close()

    # properties will be filled later:
    props = golem.util.config.Properties()

    experimentals = list(map(str, [p for p in golem.properties.properties if p.isExperimental()]))
    for name in conf:
        if name in experimentals:
            logger.warning(
                ("Your configuration sets the property %r " % name)
                + "which is an undocumented and only partially tested feature.\n"
                + "Please, feel free to test this feature but be aware that\n"
                + "====== WE DON'T GUARANTEE FOR ANYTHING! ====="
            )

    # This fills in the defaults where no option is given:
    for p in golem.properties.properties:
        if conf.getProperty(p) or conf.getProperty(p) == False or conf.getProperty(p) == 0:
            # Note that 'False'and '0' are actually valid values. We want to skip falsy values like [], " ", None, etc.
            conf.setProperty(str(p), conf.getProperty(p))

    # Check for required properties in standalone mode:
    if not conf["__OLP_MODE__"]:
        if (True if conf.getProperty("in") is None else conf.getProperty("in")==""):
            raise GolemConfigError("You have to specify at least one 'in' particle!")
        if (True if conf.getProperty("out") is None else conf.getProperty("out")==""):
            raise GolemConfigError("You have to specify at least one 'out' particle!")
        if (True if conf.getProperty("order") is None else conf.getProperty("order")==""):
            raise GolemConfigError("You have to specify the perturbative order of your process!")

    # Check for non-fatal incompatible configurations:
    orders = split_qgrafPower(",".join(map(str, conf.getListProperty(golem.properties.qgraf_power))))
    if orders is None:
        orders = []

    if all(len(p) == 2 for p in orders):
        generate_tree_diagrams = True
        generate_loop_diagrams = False
        is_loopinduced = False
    elif all(len(p) == 3 for p in orders):
        generate_tree_diagrams = not any(str(p[1]).strip().lower() == "none" for p in orders)
        generate_loop_diagrams = True
        is_loopinduced = not generate_tree_diagrams
    else:
        raise GolemConfigError("The property %s must have 2 or 3 arguments." % golem.properties.qgraf_power)

    conf["__LOOPINDUCED__"] = is_loopinduced

    no_renorm = generate_loop_diagrams and not conf.getBooleanProperty("renorm")
    raise_warn = False
    warn_str = ""
    for p in ["renorm_alphas",
              "renorm_mqwf",
              "renorm_gluonwf",
              "renorm_qmass",
              "renorm_logs",
              "renorm_gamma5",
              "renorm_yukawa",
              "renorm_eftwilson",
              "renorm_ehc",
              "MSbar_yukawa",
              "use_MQSE"]:
        if conf.getBooleanProperty(p) and no_renorm:
            raise_warn = True
            warn_str = warn_str + ",\n" + p if warn_str else p
    if raise_warn:
        logger.warning("You explicitly turned off QCD renormalisation by setting renorm=False.\n"
                       + "The following settings will therefore have no effect:\n"
                       + warn_str)

    # Check for fatal incompatible configurations:
    raise_err = False
    err_str = ""
    err_count = 0
    if not (conf["is_ufo"] or ("FeynRules" in conf.getProperty("model"))):
        # model is not a UFO
        if conf.getProperty("order_names"):
            raise_err = True
            err_str = err_str + ", order_names" if err_str else "order_names"
            err_count += 1
        if conf.getBooleanProperty("enable_truncation_orders"):
            raise_err = True
            err_str = err_str + ", enable_truncation_orders" if err_str else "enable_truncation_orders"
            err_count += 1
        if conf.getBooleanProperty("renorm_eftwilson"):
            raise_err = True
            err_str = err_str + ", renorm_eftwilson" if err_str else "renorm_eftwilson"
            err_count += 1
        if conf.getBooleanProperty("use_vertex_labels"):
            raise_err = True
            err_str = err_str + ", use_vertex_labels" if err_str else "use_vertex_labels"
            err_count += 1
        if conf.getBooleanProperty("loop_suppressed_Born"):
            raise_err = True
            err_str = err_str + ", loop_suppressed_Born" if err_str else "loop_suppressed_Born"
            err_count += 1
        if raise_err:
            if err_count > 1:
                raise GolemConfigError(
                    "The properties '{0}'".format(err_str)
                    + " which you set in your configuration are only compatible"
                    + " with a UFO model, but you did not use one."
                )
            else:
                raise GolemConfigError(
                    "The property '{0}'".format(err_str)
                    + " which you set in your configuration are only compatible"
                    + " with a UFO model, but you did not use one."
                )
    elif True if not conf.getProperty("order_names") else ("NP" not in conf.getProperty("order_names")):
        # model is a UFO, but no order_names specified or 'NP' not present in 'order_names'
        # Note: whether or not 'NP' is present in UFO is checked in feynrules.py, can't be done here
        if conf.getBooleanProperty("enable_truncation_orders"):
            raise_err = True
            err_str = err_str + ", enable_truncation_orders" if err_str else "enable_truncation_orders"
            err_count += 1
        if conf.getBooleanProperty("renorm_eftwilson"):
            raise_err = True
            err_str = err_str + ", renorm_eftwilson" if err_str else "renorm_eftwilson"
            err_count += 1
        if raise_err:
            if err_count > 1:
                raise GolemConfigError(
                    "The properties '{0}'".format(err_str)
                    + " which you set in your configuration can only be used when"
                    + " 'order_names' are specified and contain the parameter 'NP'."
                )
            else:
                raise GolemConfigError(
                    "The property '{0}'".format(err_str)
                    + " which you set in your configuration can only be used when"
                    + " 'order_names' are specified and contain the parameter 'NP'."
                )
    else:
        # model is a UFO and 'order_names' contain 'NP': Can use full EFT functionality
        pass

    if conf.getBooleanProperty("loop_suppressed_Born"):
        if not is_loopinduced:
            raise GolemConfigError(
            "\nThe property 'loop_suppressed_Born' can only be set\n"
            + "to 'True' when calculating a loop-induced process.")
        if not conf.getProperty("order_names") or ("QL" not in conf.getProperty("order_names")):
            raise GolemConfigError(
            "\nThe property 'loop_suppressed_Born' can only be set to 'True'\n"
            + "when 'order_names' are specified and contain the parameter 'QL'.")
        if not conf.getBooleanProperty("enable_truncation_orders"):
            raise GolemConfigError(
            "\nThe property 'loop_suppressed_Born' can only be set to 'True'\n"
            + "when also 'enable_truncation_orders=True'.")

    if conf.getBooleanProperty("renorm_eftwilson") and conf.getBooleanProperty("renorm_ehc"):
        raise GolemConfigError(
            "\nYou set both 'renorm_eftwilson' and 'renorm_ehc' to 'true'.\n"
            + "The former suggests that you supply counterterms for\n"
            + "Wilson-coefficients by means of a UFO model, while the\n"
            + "latter turns on the hardcoded finite renormalisation of\n"
            + "effictive Higgs-gluon couplings like in the heavy-top limit.\n"
            + "This will probably cause some serious errors in your result,\n"
            + "so I will not let you do that, sorry.")

        # END: Check for incompatible configuration


    # Discard all diagrams with double insertions, when truncation orders 
    # are used. Is also done later in golem.frm, but doing it here reduces 
    # the number of generated diagrams and speeds up the calculation.
    # Note: cannot be done when a filter module is used -> has to be part of the module
    if conf.getBooleanProperty("enable_truncation_orders"):
        for fltr in ["lo","nlo","ct"]:
            if conf["filter."+fltr] is None:
                logger.info("\'enable_truncation_orders=True\' -> adding filter.%s: d.order('NP')<=1 " % fltr)
                conf["filter."+fltr] = "lambda d: d.order('NP')<=1"
            elif conf["filter."+fltr].startswith("lambda d:"):
                logger.info("\'enable_truncation_orders=True\' -> appending filter.%s: d.order('NP')<=1 " % fltr)
                conf["filter."+fltr] = conf["filter."+fltr] + " and d.order('NP')<=1"
            else:
                logger.warning("You seem to be using a filter for the %s component " % (fltr) \
                + "defined in a filter module: %s.\n" % (conf["filter."+fltr]) \
                + "Since you are also using the 'enable_truncation_orders' feature please make sure you\n"
                + "restrict order('NP')<=1 to avoid double insertions of EFT operators (if applicable).")

    # For loop-induced processed any tree diagram must contain a 
    # loop suppressed operator, while loop diagrams must not. Add appropriate filters here.
    # Note: cannot be done when a filter module is used -> has to be part of the module
    if conf.getBooleanProperty("loop_suppressed_Born"):
        for l, fltr in enumerate(["nlo","lo"]):
            if conf["filter."+fltr] is None:
                conf["filter."+fltr] = "lambda d: d.order('QL')==" + str(l) 
            elif conf["filter."+fltr].startswith("lambda d:"):
                conf["filter."+fltr] = conf["filter."+fltr] + " and d.order('QL')==" + str(l)
            else:
                logger.warning("You seem to be using a filter for the %s component " % (fltr) \
                + "defined in a filter module: %s.\n" % (conf["filter."+fltr]) \
                + "Since you are also using the 'loop_suppressed_Born' feature please make sure you\n"
                + "include order('QL')==%d. to ensure proper loop counting." % (l))

    if not conf["extensions"] and props["extensions"]:
        conf["extensions"] = props["extensions"]

    tmp_ext = golem.properties.getExtensions(conf)

    # add appropriate reduction programs to extensions
    if rc_conf["reduction_programs"] is None:
        # no input provided by the user -> defaults (ninja+golem95)
        reduction_programs = conf.getListProperty("reduction_programs")
    else:
        # use reduction programs specified by the user
        reduction_programs = rc_conf.getListProperty("reduction_programs")

    if not golem.installation.WITH_GOLEM:
        if reduction_programs == ["golem95"]:
            raise GolemConfigError("The configuration requests only 'golem95' as reduction library,"+
                                    "but GoSam was built without Golem.\n"+
                                    "Please reinstall GoSam with support for Golem or select a diferent reduction library.")
        elif "golem95" in reduction_programs:
            logger.warning("The configuration requests 'golem95' as a reduction library, but GoSam was build without Golem.\n"+
                            "Removing 'golem95' from 'reduction_programs'.")
            reduction_programs.remove("golem95")
            conf.setProperty("reduction_programs",",".join(reduction_programs))

    for p in reduction_programs:
        if not p in tmp_ext:
            if conf["gosam-auto-reduction.extensions"]:
                conf["gosam-auto-reduction.extensions"] = p + "," + conf["gosam-auto-reduction.extensions"]
            else:
                conf["gosam-auto-reduction.extensions"] = p

    generate_counterterms = conf.getBooleanProperty("renorm") and generate_loop_diagrams and not is_loopinduced

    conf["generate_tree_diagrams"] = generate_tree_diagrams
    conf["generate_loop_diagrams"] = generate_loop_diagrams
    conf["is_loopinduced"] = is_loopinduced
    conf["generate_eft_loopind"] = conf.getBooleanProperty("loop_suppressed_Born") and is_loopinduced
    conf["generate_counterterms"] = generate_counterterms
    conf["generate_eft_counterterms"] = conf.getBooleanProperty("renorm_eftwilson") and generate_counterterms and generate_loop_diagrams
    conf["generate_ym_counterterms"] = (conf.getBooleanProperty("renorm_yukawa") \
                                        or conf.getBooleanProperty("renorm_qmass") \
                                        or conf.getBooleanProperty("renorm_gamma5")) \
        and generate_counterterms and generate_loop_diagrams
    conf["finite_renorm_ehc"] = conf.getBooleanProperty("renorm_ehc") and generate_loop_diagrams
    conf["use_MQSE"] = conf.getBooleanProperty("use_MQSE")

    if not conf["PSP_chk_method"] or conf["PSP_chk_method"].lower() == "automatic":
        conf["PSP_chk_method"] = "PoleRotation" if generate_tree_diagrams else "LoopInduced"

    if generate_loop_diagrams:
        # Check if a suitable extension for the reduction is available
        red_flag = False
        ext = golem.properties.getExtensions(conf)
        for red in golem.properties.REDUCTION_EXTENSIONS:
            if red in ext:
                red_flag = True
                break
        if not red_flag:
            raise GolemConfigError(
                "Generating code for\n"
                + "the virtual part without specifying a reduction library is useless. Please,\n"
                + "make sure that at least one of the following is added to 'extensions':\n"
                + ", ".join(golem.properties.REDUCTION_EXTENSIONS)
            )
    if not generate_loop_diagrams and conf["gosam-auto-reduction.extensions"]:
        conf["gosam-auto-reduction.extensions"] = ""

    if not conf["reduction_interoperation"]:
        conf["reduction_interoperation"] = -1

    if not conf["reduction_interoperation_rescue"]:
        conf["reduction_interoperation_rescue"] = -1

    if len(ini) > 2:
        logger.warning(
            "You specified a process with %d incoming particles.\n" % len(ini)
            + "This software has not been fully tested for processes\n"
            + "with more than two incoming particles.\n"
            + "We don't say this is impossible or wrong.\n"
            + "====== BUT WE DON'T GUARANTEE FOR ANYTHING! ====="
        )

    # retrive final extensions from other options
    ext = golem.properties.getExtensions(conf)

    # check consistency of regularisation schemes in setup file 
    # (can be skipped in OLP mode: already checked in util/olp.py:process_order_file)
    if not conf["__OLP_MODE__"]:
        mismatch_schemes = [False, None]
    
        if conf["regularisation_scheme"] == "dred":
            if "thv" in ext:
                mismatch_schemes = [True, "thv"]
            if not "dred" in ext:
                ext.append("dred")
        elif conf["regularisation_scheme"] == "thv":
            if "dred" in ext:
                mismatch_schemes = [True, "dred"]
            if not "thv" in ext:
                ext.append("thv")
        else:
            logger.critical(
                    "Unknown regularisation_scheme in config: %s" % str(conf["regularisation_scheme"])
                )
            sys.exit("GoSam terminated due to an error")
    
        if mismatch_schemes[0]:
            logger.critical(
                    "Incompatible settings between regularisation_scheme and extensions: "
                    + "%r vs. %r" % (conf["regularisation_scheme"],mismatch_schemes[1])
                )
            sys.exit("GoSam terminated due to an error")
    
        if "thv" in ext and "dred" in ext:
            logger.critical(
                    "Multiple regularisation schemes specified in extensions: thv and dred. Please pick one."
                )
            sys.exit("GoSam terminated due to an error")
    else:
        ext.append(conf["olp.extensions"])
        ext = list(set(ext))

    if "thv" in ext and conf.getProperty("r2") != "explicit":
        logger.critical(
                "When using the tHV regularisation scheme, only explicit construction of the R2 terms is permitted. "
                + "Please use DRED as regularisation scheme or switch to r2=explict."
            )
        sys.exit("GoSam terminated due to an error")

    if "thv" in ext and (conf["is_ufo"] or ("FeynRules" in conf.getProperty("model"))):
        logger.warning(
              "You are using the tHV regularisation scheme and a UFO model. Note that in tHV a finite\n"
            + "renormalisation of the non-singlet axial-vector current (-> gamma_5) is required. The\n"
            + "corresponding counterterms are only available for the built-in models.\n"
            + "=> If your process contains non-singlet axial-vector currents you will get a WRONG RESULT!\n"

        )

    # Check that is 'quadruple' is in the extensions, only Ninja is used
    if "quadruple" in ext:
        if ("ninja" not in conf["reduction_programs"]):
            raise GolemConfigError(
                "The quadruple precision copy of the code can be generated only\n"
                + "in association with ninja. Please add ninja as reduction program to 'reduction_programs' in the input card.\n"
            )

    conf["reduction_interoperation"] = conf["reduction_interoperation"].upper()
    conf["reduction_interoperation_rescue"] = conf["reduction_interoperation_rescue"].upper()

    if conf.getBooleanProperty("helsum"):
        if conf.getBooleanProperty("is_loopinduced"):
            raise GolemConfigError(
                'The "helsum" feature is not implemented for loop-induced processes.\n'
                + 'Set "helsum=false" for the selected process.\n'
            )
        if "generate-all-helicities" not in ext:
            ext.append("generate-all-helicities")
        if conf.getProperty("polvec") == "numerical" or "numpolvec" in ext:
            raise GolemConfigError(
                'The "helsum" feature is only implemented for explicit\n'
                + 'polarization vectors. Please either set "helsum=false"\n'
                + 'or "polvec=explicit" in the input card."\n'
            )
        if conf.getBooleanProperty("enable_truncation_orders"):
            raise GolemConfigError(
                'The "helsum" feature is not implemented for "enable_truncation_orders=True".\n'
                + 'Set "helsum=false" for the selected process.\n'
            )
    else:
        if conf.getProperty("polvec") == "numerical" and not "numpolvec" in ext:
            ext.append("numpolvec")

    for prop in golem.properties.properties:
        lines = prop.check(conf)
        if len(lines) > 0:
            logger.warning("\n".join(lines))

    conf["extensions"] = ext

    # debuging the diagsum property:
    conf["debug_diagsum"] = False

def workflow(conf):
    """
    Creates additional properties which determine the workflow
    later in the program.
    """
    fill_config(conf)
    check_dont_overwrite(conf)
    path = golem.util.tools.process_path(conf)
    # Check if path exists. If it doesn't, try to create it
    if not os.path.exists(path):
        try:
            rp = os.path.relpath(path)
            if not os.path.sep in rp:
                os.mkdir(rp)
                logger.warning("Process path %r created." % path)
        except OSError as err:
            raise GolemConfigError("Could not create process path: %r\r%s" % (path, err))

    if not os.path.exists(path):
        raise GolemConfigError("The process path does not exist: %r" % path)

    # the following commands will need to import 'model.py'
    # here we create it:
    golem.util.tools.prepare_model_files(conf)


    # zero property: convert masses and width defined through PDG code to internal parameter name 
    # (depends on model, so model.py must have been created already)
    # (can be skipped in OLP mode: already checked in util/olp.py:process_order_file)
    if not conf["__OLP_MODE__"]:
        model = golem.util.tools.getModel(conf)
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


    # It can happen that a model defines names for a particle's mass and width but 
    # sets them to 0 in the parameters definiton (see e.g. the light quarks in the 
    # built-in models). We have to take care of that and add those names to the zero 
    # property to avoid erroneous code generation. Otherwise the user has to remember
    # to add these cases to 'zero' manually.
    # (can be skipped in OLP mode: already checked in util/olp.py:process_order_file)
    if not conf["__OLP_MODE__"] and not conf.getBooleanProperty("massive_light_fermions"):
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


    for prop in [golem.properties.zero, golem.properties.one]:
        golem.util.tools.expand_parameter_list(prop, conf)


def run_analyzer(path, conf, in_particles, out_particles):
    generate_lo = conf.getBooleanProperty("generate_tree_diagrams")
    generate_virt = conf.getBooleanProperty("generate_loop_diagrams")
    generate_ct = conf.getBooleanProperty("generate_eft_counterterms")
    generate_eftli = conf.getBooleanProperty("generate_eft_loopind")

    _unitary_gauge = conf.getBooleanProperty("unitary_gauge")
    _use_MQSE = conf.getBooleanProperty("use_MQSE")

    model = golem.util.tools.getModel(conf)

    lo_flags = {}
    virt_flags = {}
    ct_flags = {}

    if generate_lo or generate_eftli:
        modname = consts.PATTERN_TOPOLOPY_LO
        fname = os.path.join(path, "%s.py" % modname)
        logger.debug("Loading tree diagram file %r" % fname)
        mod_diag_lo = golem.util.tools.load_source(modname, fname)
        if _unitary_gauge or _use_MQSE:
            for d in mod_diag_lo.diagrams.values():
                d.unitary_gauge = _unitary_gauge
                d.use_MQSE = _use_MQSE
        conf["ehc"] = False
        # keep_tree, tree_signs, tree_flows =
        keep_tree, tree_signs, treecache = golem.topolopy.functions.analyze_tree_diagrams(
            mod_diag_lo.diagrams, model, conf, filter_flags=lo_flags
        )

        if len(keep_tree) == 0 and not generate_eftli:
            if conf.getBooleanProperty("ignore_empty_subprocess"):
                conf.setProperty("write_vanishing_amplitude", "true")
            else:
                logger.critical(
                    "No remaining diagrams in subprocess {} after applying filters, use --ignore-empty-subprocess to continue anyway.".format(
                        conf["process_name"]
                    )
                )
                sys.exit("GoSam terminated due to an error")
    else:
        keep_tree = []
        tree_signs = {}
        treecache = golem.topolopy.objects.TreeCache()
        # tree_flows = {}

    quark_masses = []
    complex_masses = []
    massive_bubbles = {}
    if generate_virt:
        zero = golem.util.tools.getZeroes(conf)
        onshell = {}
        i = 1
        for p in in_particles:
            m = p.getMass(zero)
            key = "es%d" % i
            if str(m) == "0":
                onshell[key] = "0"
            else:
                onshell[key] = "%s**2" % m

        modname = consts.PATTERN_TOPOLOPY_VIRT
        fname = os.path.join(path, "%s.py" % modname)
        logger.debug("Loading one-loop diagram file %r" % fname)
        mod_diag_virt = golem.util.tools.load_source(modname, fname)
        if _unitary_gauge or _use_MQSE:
            for d in mod_diag_virt.diagrams.values():
                d.unitary_gauge = _unitary_gauge
                d.use_MQSE = _use_MQSE

        keep_virt, keep_vtot, eprops, loopcache, loopcache_tot = golem.topolopy.functions.analyze_loop_diagrams(
            mod_diag_virt.diagrams,
            model,
            conf,
            onshell,
            quark_masses,
            complex_masses,
            filter_flags=virt_flags,
            massive_bubbles=massive_bubbles,
        )

    else:
        keep_virt = []
        keep_vtot = []
        eprops = {}
        loopcache = golem.topolopy.objects.LoopCache()
        loopcache_tot = golem.topolopy.objects.LoopCache()

    if generate_ct:
        modname = consts.PATTERN_TOPOLOPY_CT
        fname = os.path.join(path, "%s.py" % modname)
        logger.debug("Loading counterterm diagram file %r" % fname)
        mod_diag_ct = golem.util.tools.load_source(modname, fname)
        if _unitary_gauge or _use_MQSE:
            for d in mod_diag_ct.diagrams.values():
                d.unitary_gauge = _unitary_gauge
                d.use_MQSE = _use_MQSE

        keep_ct, ct_signs, ctcache = golem.topolopy.functions.analyze_ct_diagrams(
            mod_diag_ct.diagrams, model, conf, filter_flags=ct_flags
        )
    else:
        keep_ct = []
        ct_signs = {}
        ctcache = golem.topolopy.objects.CTCache()

    conf["__heavy_quarks__"] = quark_masses
    conf["complex_masses"] = complex_masses

    if not isinstance(lo_flags, dict):
        lo_flags = dict(enumerate(lo_flags))
    if not isinstance(virt_flags, dict):
        virt_flags = dict(enumerate(virt_flags))
    if not isinstance(ct_flags, dict):
        ct_flags = dict(enumerate(ct_flags))

    flags = (lo_flags, virt_flags, ct_flags)

    # return keep_tree, keep_virt, loopcache, tree_signs, tree_flows, flags
    return (
        keep_tree,
        keep_virt,
        keep_vtot,
        eprops,
        keep_ct,
        loopcache,
        loopcache_tot,
        tree_signs,
        flags,
        massive_bubbles,
        treecache,
        ctcache,
        ct_signs,
    )
