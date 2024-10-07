# vim: ts=3:sw=3
import sys
import os
import os.path
import io
import hashlib

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

from golem.util.find_libpaths import find_libraries

from golem.util.path import golem_path
from golem.util.tools import copy_file, generate_particle_lists

from golem.util.config import GolemConfigError, split_qgrafPower

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_qgraf import *
from golem.installation import GOLEM_VERSION, GOLEM_REVISION

import logging

logger = logging.getLogger(__name__)


def create_ff_files(conf, in_particles, out_particles):
    legs = len(in_particles) + len(out_particles)
    path = golem.util.tools.process_path(conf)

    for n in range(1, legs + 1):
        f = open(os.path.join(path, "ff-%d.hh" % n), "w")
        p = golem.algorithms.formfactors.FormFactorPrinter(f)

        f.write("* vim: ts=3:sw=3\n")
        ffset = []
        for r in range(n + 1):
            f.write("*---#[ Procedure TI%dr%d :\n" % (n, r))
            ffs = p.generate(n, r)
            ffset.extend(ffs)
            f.write("*---#] Procedure TI%dr%d :\n" % (n, r))

        f.write("*---#[ Set of Form Factors :\n")
        if len(ffset) > 0:
            f.write("Set FormFactors%d : " % n)
            f.write(",\n\t".join([", ".join(ffset[i : i + 10]) for i in range(0, len(ffset), 8)]))
            f.write(";\n")
        f.write("*---#] Set of Form Factors :\n")
        f.close()


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

    # OBSOLETE:
    ## we only need the ff-<n>.hh files if we create the virtual amplitude
    ## and if we use the extension 'golem95':
    ##flag_create_ff_files = conf.getBooleanProperty("generate_nlo_virt") \
    ##		and "golem95" in extensions
    flag_create_ff_files = False

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

    if flag_create_ff_files:
        create_ff_files(conf, in_particles, out_particles)

    cleanup(path)


def cleanup(path):
    cleanup_files = []

    for ext in [".tex", ".log", ".py", ".pyc", ".pyo"]:
        for stub in ["pyxotree", "pyxovirt", "topotree", "topovirt", "pyxoct", "topoct"]:
            cleanup_files.append(stub + ext)

    if True:
        for ext in ["", ".py", ".pyc", ".pyo"]:
            cleanup_files.append("model" + ext)

    # for filename in cleanup_files:
    # full_name = os.path.join(path, filename)
    # if os.path.exists(full_name):
    # os.remove(full_name)


def find_config_files():
    """
    Searches for configuration files in the default locations.
    These are used to fill the fields of newly created input
    files by preferred defaults.
    Use "golem.util.find_libpaths.find_libraries()"
    to find	external library paths.

    The procedure looks in the following locations:
            <golem path>
            <guessed share/gosam-contrib path>
            <user's home>
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
    avail_props = list(map(str, [p for p in golem.properties.properties]))
    for dir in directories:
        for file in files:
            full_name = os.path.join(dir, file)
            if os.path.exists(full_name):
                try:
                    with open(full_name, "r") as f:
                        props.load(f, avail_props)
                except GolemConfigError as err:
                    logger.critical("Configuration file is not sound:" + str(err))
                    sys.exit("GoSam terminated due to an error")
    libpaths = find_libraries()
    for flag in libpaths:
        props.setProperty(flag, libpaths[flag])
    return props


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
        f.write("\\begin{description}\n")
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

        if prop.isExperimental() and not changed:
            continue
        if prop.isHidden() and not changed:
            continue

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
                "\\item[\\texttt{%s}] (\\textit{%s})\n" % (str(prop).replace("_", "\\_"), stype.replace("_", "\\_"))
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
            if prop.getDefault() is not None:
                value = str(prop.getDefault())
                if len(value) > 0:
                    f.write("Default: \\verb|%s|\n" % value)

    if format is None:
        for prop in defaults:
            if prop.startswith("+") or prop.endswith(".extensions"):
                value = defaults[prop]
                f.write("%s=%s\n" % (prop, value))
    elif format == "LaTeX":
        f.write("\\end{description}\n")
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


def workflow(conf):
    """
    Creates additional properties which determine the workflow
    later in the program.

    Also does some checks whether the combination of properties
    makes sense.

    The additional properties are:

    generate_nlo_virt
    generate_lo_diagrams
    generate_eft_counterterms
    """
    ini = conf.getProperty(golem.properties.qgraf_in)
    fin = conf.getProperty(golem.properties.qgraf_out)
    path = golem.util.tools.process_path(conf)

    powers = conf.getProperty(golem.properties.qgraf_power)
    renorm = conf.getProperty(golem.properties.renorm)
    templates = conf.getProperty(golem.properties.template_path)
    templates = os.path.expandvars(templates)
    qgraf_options = conf.getProperty(golem.properties.qgraf_options)

    r2only = conf.getProperty(golem.properties.r2).lower().strip() == "only"
    # formopt = conf.getProperty(golem.properties.formopt)
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
        if conf.getProperty(p):
            conf.setProperty(str(p), conf.getProperty(p))

    # Check for incompatible configuration:
    raise_err = False
    err_str = ""
    if not (conf["is_ufo"] or ("FeynRules" in conf.getProperty("model"))):
        # model is not a UFO
        if conf.getProperty("order_names"):
            raise_err = True
            err_str = err_str + ", order_names" if err_str else "order_names"
        if conf.getBooleanProperty("enable_truncation_orders"):
            raise_err = True
            err_str = err_str + ", enable_truncation_orders" if err_str else "enable_truncation_orders"
        if conf.getBooleanProperty("renorm_eftwilson"):
            raise_err = True
            err_str = err_str + ", renorm_eftwilson" if err_str else "renorm_eftwilson"
        if conf.getBooleanProperty("use_vertex_labels"):
            raise_err = True
            err_str = err_str + ", use_vertex_labels" if err_str else "use_vertex_labels"
        if raise_err:
            raise GolemConfigError(
                "The properties '{0}'".format(err_str)
                + " which you set in your configuration are only compatible"
                + " with a UFO model, but you did not use one."
            )
    elif True if not conf.getProperty("order_names") else ("NP" not in conf.getProperty("order_names")):
        # model is a UFO, but no order_names specified or 'NP' not present in 'order_names'
        # Note: whether or not 'NP' is present in UFO is checked in feynrules.py, can't be done here
        if conf.getBooleanProperty("enable_truncation_orders"):
            raise_err = True
            err_str = err_str + ", enable_truncation_orders" if err_str else "enable_truncation_orders"
        if conf.getBooleanProperty("renorm_eftwilson"):
            raise_err = True
            err_str = err_str + ", renorm_eftwilson" if err_str else "renorm_eftwilson"
        if raise_err:
            raise GolemConfigError(
                "The properties '{0}'".format(err_str)
                + " which you set in your configuration can only be used when"
                + " 'order_names' are specified and contain the parameter 'NP'."
            )
    else:
        # model is a UFO and 'order_names' contain 'NP': Can use full EFT functionality
        pass

    if conf.getBooleanProperty("renorm_eftwilson") and conf.getBooleanProperty("renorm_ehc"):
        raise GolemConfigError(
            "\nYou set both 'renorm_eftwilson' and 'renorm_ehc' to 'true'.\n"
            + "The former suggests that you supply counterterms for\n"
            + "Wilson-coefficients by means of a UFO model, while the\n"
            + "latter turns on the hardcoded finite renormalisation of\n"
            + "effictive Higgs-gluon couplings like in the heavy-top limit.\n"
            + "This will probably cause some serious errors in your result,\n"
            + "so I will not let you do that, sorry.")

    if not conf["extensions"] and props["extensions"]:
        conf["extensions"] = props["extensions"]

    tmp_ext = golem.properties.getExtensions(conf)

    for p in conf["reduction_programs"].split(","):
        if not p in tmp_ext:
            if conf["gosam-auto-reduction.extensions"]:
                conf["gosam-auto-reduction.extensions"] = p + "," + conf["gosam-auto-reduction.extensions"]
            else:
                conf["gosam-auto-reduction.extensions"] = p

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

    check_dont_overwrite(conf)
    orders = split_qgrafPower(",".join(map(str, conf.getListProperty(golem.properties.qgraf_power))))
    powers = orders[0] if orders else []

    if len(powers) == 2:
        generate_lo_diagrams = True
        generate_nlo_virt = False
    elif len(powers) == 3:
        generate_lo_diagrams = str(powers[1]).strip().lower() != "none"
        generate_nlo_virt = True
    else:
        raise GolemConfigError("The property %s must have 2 or 3 arguments." % golem.properties.qgraf_power)

    conf["generate_lo_diagrams"] = generate_lo_diagrams
    conf["generate_nlo_virt"] = generate_nlo_virt
    conf["generate_eft_counterterms"] = conf.getBooleanProperty("renorm_eftwilson") and generate_nlo_virt
    conf["generate_yuk_counterterms"] = conf.getBooleanProperty("renorm_yukawa") and generate_nlo_virt
    conf["finite_renorm_ehc"] = conf.getBooleanProperty("renorm_ehc") and generate_nlo_virt

    if not conf["PSP_chk_method"] or conf["PSP_chk_method"].lower() == "automatic":
        conf["PSP_chk_method"] = "PoleRotation" if generate_lo_diagrams else "LoopInduced"

    # if ("onshell" not in qgraf_options) and ("offshell" not in qgraf_options):
    # qgraf_options.append("onshell")
    # conf[golem.properties.qgraf_options] = ",".join(qgraf_options)

    if generate_nlo_virt and not r2only:
        # Check if a suitable extension for the reduction is available
        red_flag = False
        ext = golem.properties.getExtensions(conf)
        for red in golem.properties.REDUCTION_EXTENSIONS:
            if red in ext:
                red_flag = True
                break
        if not red_flag:
            logger.warning(
                "Generating code for the virtual part without specifying\n"
                + "a reduction library is useless.\n"
                + "Please, make sure that at least one of the following\n"
                + "is added to 'extensions':\n"
                + ", ".join(golem.properties.REDUCTION_EXTENSIONS)
            )
            conf["gosam-auto-reduction.extensions"] = "ninja,golem95"
    if not generate_nlo_virt and conf["gosam-auto-reduction.extensions"]:
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

    if "better_num" not in ext:
        ext.append("better_num")

    if "noformopt" not in ext:
        ext.append("formopt")
    if "noderive" not in ext:
        ext.append("derive")

    if "cdr" in ext and "dred" in ext:
        logger.warning("Incompatible settings between regularisation_scheme and extensions. cdr is used.")

    if "no-fr5" in ext:
        logger.warning("no-fr5 is not supported anymore.")

    if not "dred" in ext:
        ext.append("dred")
    if conf["regularisation_scheme"] == "cdr" or "cdr" in ext:
        conf["olp.irregularisation"] = "CDR"

    # We need to put out an error if we specify formopt and some other extensions
    if "formopt" in ext:
        if "topolynomial" in ext:
            raise GolemConfigError(
                "Your configuration has select the extension 'topolynomial' \n"
                "and optimization by FORM 'formopt'. "
                + "The two options are not compatible. \nPlease change your input "
                + "card (remove topolynomial or add noformopt) and re-run."
            )
        if "r2_only" in ext:
            raise GolemConfigError("r2 only not supported with extension formopt. Add the 'noformopt' extension.\n")
        if conf["abbrev.level"] != "diagram" and conf["abbrev.level"] is not None:
            raise GolemConfigError("formopt only supported with abbrev.level=diagram\n")
    if ("ninja" in ext) and ("formopt" not in ext):
        raise GolemConfigError(
            "The ninja reduction method is only supported with formopt.\n"
            + "Please either remove noformopt or ninja in the input card\n"
        )

    # Check that is 'quadruple' is in the extensions, only Ninja with formopt is used
    if "quadruple" in ext:
        if ("ninja" not in ext) or ("samurai" in ext) or ("golem95" in ext):
            raise GolemConfigError(
                "The quadruple precision copy of the code can be generated only\n"
                + "in association with ninja. The gosam-contrib has to be compiled with the flag\n"
                + "'--enable-quadninja'. Please select only ninja as reduction program by setting:\n"
                + "'reduction_programs=ninja' in the input card.\n"
            )

    conf["reduction_interoperation"] = conf["reduction_interoperation"].upper()
    conf["reduction_interoperation_rescue"] = conf["reduction_interoperation_rescue"].upper()

    if generate_nlo_virt and conf.getProperty("enable_truncation_orders"):
        if "samurai" in ext:
            raise GolemConfigError(
                "The 'enable_truncation_orders' feature can only be used with ninja or golem95.\n"
                + "Please select one of those as your redution program by setting:\n"
                + "'reduction_programs=ninja, golem95' in the input card.\n"
            )

    if "shared" in ext:
        conf["shared.fcflags"] = "-fPIC"
        conf["shared.ldflags"] = "-fPIC"

    if conf.getBooleanProperty("helsum"):
        if not conf.getBooleanProperty("generate_lo_diagrams"):
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
    else:
        if conf.getProperty("polvec") == "numerical" and not "numpolvec" in ext:
            ext.append("numpolvec")

    for prop in golem.properties.properties:
        lines = prop.check(conf)
        if len(lines) > 0:
            logger.warning("\n".join(lines))

    conf["extensions"] = ext

    # the following commands will need to import 'model.py'
    # here we create it:
    golem.util.tools.prepare_model_files(conf)

    for prop in [golem.properties.zero, golem.properties.one]:
        lst = conf.getProperty(prop)
        golem.util.tools.expand_parameter_list(prop, conf)

    # debuging the diagsum property:
    conf["debug_diagsum"] = False


def run_analyzer(path, conf, in_particles, out_particles):
    generate_lo = conf.getBooleanProperty("generate_lo_diagrams")
    generate_virt = conf.getBooleanProperty("generate_nlo_virt")
    generate_ct = conf.getBooleanProperty("generate_eft_counterterms")

    model = golem.util.tools.getModel(conf)

    lo_flags = {}
    virt_flags = {}
    ct_flags = {}

    if generate_lo:
        modname = consts.PATTERN_TOPOLOPY_LO
        fname = os.path.join(path, "%s.py" % modname)
        logger.debug("Loading tree diagram file %r" % fname)
        mod_diag_lo = golem.util.tools.load_source(modname, fname)
        if conf.getBooleanProperty("unitary_gauge"):
            for d in mod_diag_lo.diagrams.values():
                d.unitary_gauge = True
        conf["ehc"] = False
        # keep_tree, tree_signs, tree_flows =
        keep_tree, tree_signs, treecache = golem.topolopy.functions.analyze_tree_diagrams(
            mod_diag_lo.diagrams, model, conf, filter_flags=lo_flags
        )

        if len(keep_tree) == 0:
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
        if conf.getBooleanProperty("unitary_gauge"):
            for d in mod_diag_virt.diagrams.values():
                d.unitary_gauge = True

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
        if conf.getBooleanProperty("unitary_gauge"):
            for d in mod_diag_ct.diagrams.values():
                d.unitary_gauge = True

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
