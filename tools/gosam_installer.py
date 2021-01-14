#!/usr/bin/env python3

# GoSam Installation script
# Copyright 2013-2020 GoSam Collaboration
# Small parts of this file are based on the Rivet bootstrap script
# License: http://www.gnu.org/licenses/gpl.html GPL version 2 or higher

# -*- coding: utf8 -*-

import sys

def check_py_version():
    ver = sys.version_info
    if not(ver.major >= 3 and ver.minor >= 6):
        print("This installation script and GoSam need Python 3.6 or newer.")
        sys.exit(1)

check_py_version()

import os

# defaults:
CONFIG_URL=r"https://raw.githubusercontent.com/gudrunhe/gosam/master/tools/gosam_install.cfg"
DEFAULTPREFIX=os.path.join(os.getcwd(),"local")
INSTALLER_VERSION="20210114"

INSTALLOG_DEFAULT="installer-log.ini"

CONTACT="https://github.com/gudrunhe/gosam"

import configparser
import glob
import hashlib
import io
import logging
import os
import re
import readline
import shlex
import socket
import stat
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from optparse import OptionParser, OptionGroup


parser = OptionParser()

opts = {}
args = []
config = None

class ConfigClass():
    pass

class RuntimeException(Exception):
        pass

my_config = ConfigClass()

def handle_args():
    global parser,args,opts

    def intel_option_callback(option, opt, value, parser):
        parser.values.FC = "ifort"
        parser.values.CC = "icc"
        parser.values.CXX = "icpc"

    def prefix_callback(option, opt, value, parser, *args, **kwargs):
        parser.values.prefix = value
        parser.values.prefix_changed = True


    parser.add_option("--prefix", metavar="INSTALLDIR", nargs=1, default=DEFAULTPREFIX, dest="prefix",type="string",
                  help="Location to install packages to [%default]", callback=prefix_callback, action="callback")
    parser.add_option("-f", "--force", action="store_true", default=False, dest="FORCE",
                  help="Delete modified files [%default]")
    parser.add_option("-j", default="2", dest="JMAKE",
                  help="Num of 'make' threads to run in parallel (the n in 'make -j<n>') [%default]")
    parser.add_option("-v", "--verbose", action="store_const", const=logging.DEBUG, dest="LOGLEVEL",
                  default=logging.INFO, help="print debug (very verbose) messages")
    parser.add_option("-q", "--quiet", action="store_const", const=logging.WARNING, dest="LOGLEVEL",
                  default=logging.INFO, help="be very quiet")
    parser.add_option("--intel", help="Use Intel compiler (ifort, icc) instead of GNU compiler (gfortran, gcc).",
            action="callback",nargs=0,callback=intel_option_callback)

    parser.add_option("-u","--uninstall", action="store_true", default=False,
                  help="Uninstall an existing GoSam installation.")

    group = OptionGroup(parser, "Expert options", "Normally, you do not need to use them.")
    group.add_option("-c","--check", action="store_true", default=False,
                  help="Check installation for modified files.")
    group.add_option("-b","--batch", action="store_true", default=False, dest="BATCH",
                  help="Batch mode - no questions during the setup [%default]")
    group.add_option("--fc", metavar="FORTRANCOMPILER", default="gfortran", dest="FC",
                  help="Fortran compiler [%default]")
    group.add_option("--cc", metavar="CCOMPILER", default="gcc", dest="CC",
                  help="C compiler [%default]")
    group.add_option("--cxx", metavar="CXXCOMPILER", default="g++", dest="CXX",
                  help="C++ compiler [%default]")
    group.add_option("--quadruple", action="store_true", default=False, dest="QUADRUPLE",
                  help="Compile GoSam-Contrib in quadruple precision [%default]")
    group.add_option("-l","--install-log",metavar="INSTALLOG", default=os.path.join(os.getcwd(),INSTALLOG_DEFAULT), dest="INSTALLLOG",
                  help="Path to log file for upgrade/uninstall info [%default]")
    parser.add_option_group(group)


    opts, args = parser.parse_args()

    if opts.QUADRUPLE:
        opts.GOSAM_CONTRIB_OPTIONS = "--with-precision=quadruple"
    else:
        opts.GOSAM_CONTRIB_OPTIONS = ""

def setup_logging():
    ## Configure logging
    try:
        logging.basicConfig(level=opts.LOGLEVEL, format="%(message)s")
    except:
        pass
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger().setLevel(opts.LOGLEVEL)
    if logging.getLogger().handlers:
        logging.getLogger().handlers[0] = h
    else:
        logging.getLogger().addHandler(h)

def replace_environment_variables(text):
        for e in os.environ:
                text = text.replace("$"+e,os.environ[e])
                text = text.replace("${"+e+"}",os.environ[e])
        return text

def setup_autocompleter():
    def complete(text, state):
        text = replace_environment_variables(text)
        return (glob.glob(text+'*')+[None])[state]

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

def version_compare(ver1,ver2):
    """
    Compare versions
      -1: ver1 is older (lower) ver2
       1: ver1 is newer than (higher) ver2
       0: ver1 is the same ver2
    Here we interpret verion strings in the FreeBSD style [1]:
    - a version is a sequence of [number][letters][number] segments
      delimited by dots or any non-alphanumeric sequences;
    - a missing segment is considered to be just 0;
    - a missing initial number is considered to be -1;
    - a missing final number is 0.
    [1] https://github.com/freebsd/pkg/blob/release-1.13/libpkg/pkg_version.c
    >>> version_compare("1","2")
    -1
    >>> version_compare("1.0","1.0")
    0
    >>> version_compare("1.1","1.1patch1")
    -1
    >>> version_compare("1.2","1.1patch1")
    1
    >>> version_compare("1.8","1.09")
    -1
    >>> version_compare("a-5","a-03")
    1
    >>> version_compare("1.2", "1.2.0")
    0
    >>> version_compare("1.2", "1.2.rc1")
    1
    >>> version_compare("1.2", "1.2patch1")
    -1
    >>> version_compare("1.2.b1", "1.2.a2")
    1
    """
    rx = re.compile("([0-9]*)([a-zA-Z]*)([0-9]*)[^0-9a-zA-Z]*")
    ver1 = [(int(n1 or ("-1" if l else "0")), l, int(n2 or "0")) for n1,l,n2 in rx.findall(ver1)]
    ver2 = [(int(n1 or ("-1" if l else "0")), l, int(n2 or "0")) for n1,l,n2 in rx.findall(ver2)]
    while len(ver1) < len(ver2): ver1.append((0, "", 0))
    while len(ver2) < len(ver1): ver2.append((0, "", 0))
    for i in range(max(len(ver1), len(ver2))):
        c = (ver1[i] > ver2[i]) - (ver1[i] < ver2[i])
        if c:
            return c
    return 0

def get_free_diskspace(path):
    """ return the free disk space in MB """
    if hasattr(os, 'statvfs'):
        st = os.statvfs(path)
        return st.f_bavail * st.f_frsize / 1024 / 1024
    else:
        logging.error("Platform not supported. Cannot get free disk space.")
        return -1

class InstallTracker(object):
    def __init__(self,pkg_name,official_name,version,broken=False):
        self.pkg_name = pkg_name
        self.section = "pkg_"+pkg_name
        self.official_name = official_name
        self.version = version
        self.install_dirs = []
        self.install_files = []
        self.modified_files = []
        self.build_variables = dict()
        self.broken = broken

        self.removed_dirs = []
        self.removed_files = []

    def store_build_variables(self,opts):
        self.build_variables["fc"] = opts.FC
        self.build_variables["cc"] = opts.CC
        self.build_variables["cxx"] = opts.CXX
        self.build_variables["jmake"] = opts.JMAKE
        self.build_variables["prefix"] = opts.prefix
        if "gosam-contrib" in self.pkg_name and opts.GOSAM_CONTRIB_OPTIONS:
            self.build_variables["gosam_contrib_options"] = opts.GOSAM_CONTRIB_OPTIONS

    def retrive_build_variables(self,o):
        o.FC = self.build_variables.get("fc",opts.FC)
        o.CC = self.build_variables.get("cc",opts.CC)
        o.CXX = self.build_variables.get("cxx",opts.CXX)
        o.JMAKE = self.build_variables.get("jmake",opts.JMAKE)
        o.GOSAM_CONTRIB_OPTIONS = self.build_variables.get("gosam_contrib_options",opts.GOSAM_CONTRIB_OPTIONS)
        return o

    def sha1sum_file(self, filename):
        sha1sum = hashlib.sha1()
        if not os.path.exists(filename):
            return "NOTEXIST"
        with open(filename,'rb') as f:
            for chunk in iter(lambda: f.read(128*sha1sum.block_size), b''):
                 sha1sum.update(chunk)
        return sha1sum.hexdigest()

    def extract_automake_install(self, all_lines):
        expr_install = re.compile(r'.*install(?:\.sh)?\s+-c\s+(?:-m\s+\d*\s+)?(.*)',re.IGNORECASE)
        expr_makedir = re.compile(r'.*mkdir\s+(?:-p\s+)?(.*)',re.IGNORECASE)

        for line in all_lines:
            res = expr_makedir.match(line)
            if res:
                dirs = shlex.split(res.group(1))
                dirs = [d for d in dirs if os.path.isdir(d)]
                self.install_dirs = self.install_dirs + dirs
                continue
            res = expr_install.match(line)
            if not res:
                continue
            arguments = shlex.split(res.group(1))
            arguments = [a for a in arguments if len(a) >= 1 and a[1] != "-"]
            if len(arguments)<2:
                continue
            target = arguments[-1]
            if os.path.isdir(target):
                for f in arguments[:-1]:
                    fdir = os.path.join(target,os.path.basename(f))
                    if os.path.isfile(fdir) or os.path.islink(fdir):
                        self.install_files.append(fdir)
            elif os.path.isfile(target) or os.path.islink(target):
                self.install_files.append(target)

    def extract_setup_py(self, all_lines):
        expr_copying = re.compile(r'^copying (.*) -> (.*)',re.IGNORECASE)
        expr_writing = re.compile(r'^Writing (.*)',re.IGNORECASE)
        expr_makedir = re.compile(r'^creating (.*)',re.IGNORECASE)

        for line in all_lines:
            res = expr_makedir.match(line)
            if res and os.path.isdir(res.group(1)) and not res.group(1).startswith("build" + os.path.sep):
                self.install_dirs.append(res.group(1))
                continue
            res = expr_writing.match(line)
            if res and os.path.isfile(res.group(1)) and not res.group(1).startswith("build" + os.path.sep):
                self.install_files.append(res.group(1))
                continue
            res = expr_copying.match(line)
            if not res:
                continue
            if "build" + os.path.sep in res.group(2):
                continue
            target = os.path.join(res.group(2),os.path.basename(res.group(1)))
            if os.path.isfile(target) or os.path.islink(target):
                self.install_files.append(target)

    def add_directories(self,dirs):
        for d in dirs:
            if os.path.exists(d):
                self.install_dirs.append(d)

    def find_further_files(self):
        """ find links like libgolem.so.0->libgolem.so.0.0.0 """
        for f in self.install_files:
            if ".so" in f:
                d = os.path.dirname(f)
                fname = os.path.basename(f)
                fname_split = fname.split(".")
                for i in range(len(fname_split)-1,1,-1):
                    if not fname_split[i].isdigit():
                        break
                    new_f = os.path.join(d,".".join(fname_split[0:i]))
                    if os.path.exists(new_f) and os.path.islink(new_f) and \
                      not new_f in self.install_files:
                        self.install_files.append(new_f)


    def analyse_output(self,all_lines):
        #print "===== ANALYZE +++++++++++++++++++++"
        #print all_lines
        self.extract_automake_install(all_lines.split("\n"))
        self.extract_setup_py(all_lines.split("\n"))
        self.find_further_files()
        #print "===== ANALYZE result +++++++++++++++++++++"
        #print self.install_files
        #print self.install_dirs

    def store_to_ini_file(self, ini_file, uninstall_mode=False):
        db = configparser.ConfigParser()
        if os.path.exists(ini_file):
            db.read([ini_file])
        if not db.has_section("generic"):
            db.add_section("generic")
            db.set("generic","prefix",opts.prefix)
        section = "pkg_"+ self.pkg_name
        if not db.has_section(section):
            db.add_section(section)

        if not uninstall_mode:
            new_files_name = set(self.install_files)
        else:
            new_files_name = set()
        new_install_files_hashes = {}

        to_be_removed = []
        for i in new_files_name:
            new_install_files_hashes[i] = self.sha1sum_file(i)
            if new_install_files_hashes[i] == "NOTEXIST":
                to_be_removed.append(i)

        for i in to_be_removed:
            new_files_name.remove(i)

        old_install_files_name = set()
        old_install_files_hashes = {}
        if db.has_option(section,"install_files"):
            old_install_files = db.get(section,"install_files").split("\n")
            for i in old_install_files:
                if not " " in i:
                    continue
                try:
                    hash_value= i[:i.find(" ")]
                    name= i[i.find(" ")+1:]
                    if (name in self.removed_files) or (not os.path.exists(i)):
                        continue
                    old_install_files_name.add(name)
                    old_install_files_hashes[name] = hash_value
                except IndexError:
                    pass

        for i in old_install_files_name:
            if i not in new_files_name and os.path.exists(i):
                new_files_name.add(i)
                new_install_files_hashes[i] = old_install_files_hashes[i]
        new_install_files = []
        for i in new_files_name:
            new_install_files.append(new_install_files_hashes[i]+" " + i)
        db.set(section,"install_files","\n".join(new_install_files))

        if db.has_option(section,"install_dirs"):
            old_dirs = db.get(section,"install_dirs").split("\n")
            old_dirs = [i for i in old_dirs if os.path.exists(i)]
            new_dirs = "\n".join(list(set(old_dirs).union(self.install_dirs).difference(set(self.removed_dirs))))
        else:
            new_dirs = "\n".join(list(self.install_dirs))

        for n,v in self.build_variables.items():
            db.set(section,"build_"+n,v)

        db.set(section,"install_dirs",new_dirs)
        db.set(section,"installer_version",str(INSTALLER_VERSION)) # needed if the format changes not backwards-compatible
        db.set(section,"official_name",self.official_name)
        db.set(section,"version",self.version)
        if self.broken:
            db.set(section,"broken",str(self.broken))
        else:
            db.remove_option(section,"broken")


        if uninstall_mode:
            removable = len(new_install_files) == 0
            #ignore directories used in other packages:
            other_pkg_dirs = []
            for sec in db.sections():
                if sec == section:
                    continue
                if db.has_option(sec,"install_dirs"):
                    other_pkg_dirs.extend(db.get(sec,"install_dirs").split("\n"))

            removable = removable and (all([i in other_pkg_dirs for i in new_dirs.split("\n") ]) or not new_dirs)

            if removable:
                db.remove_section(section)

        # check if tracker is empty
        if len(db.sections()) == 1: # only "generic" section left
            try:
                os.unlink(ini_file)
            except OSError as err:
                logging.error("Could not remove install log to %s: %s" % (ini_file, str(err)))
                return False
        else:
            try:
                f = open(ini_file,"w")
                db.write(f)
                f.close()
            except IOError as err:
                logging.error("Could not write install log to %s: %s" % (ini_file, str(err)))
                return False
        return True

    def read_from_ini_file(self,ini_file):
        db = configparser.ConfigParser()
        self.install_files = []
        self.modified_files = []
        self.install_dirs = []
        if os.path.exists(ini_file):
            db.read([ini_file])
        section = "pkg_"+ self.pkg_name

        def db_get(s,o,d):
            if db.has_option(s,o):
                return db.get(s,o)
            else:
                return d

        self.official_name = db_get(section,"official_name",self.official_name)
        self.version = db_get(section,"version","")

        self.broken = db_get(section,"broken",False)

        section = "pkg_"+ self.pkg_name
        if not db.has_section(section):
            db.add_section(section)
        list_install_files = db_get(section,"install_files","")
        for f in list_install_files.split("\n"):
            pos = f.find(" ")
            checksum = ""
            if pos >= 0:
                checksum = f[:pos]
                filename = f[pos+1:]
            else:
                filename = f
            if os.path.exists(filename):
                    if checksum:
                        if checksum != self.sha1sum_file(filename):
                            self.modified_files.append(filename)
                    self.install_files.append(filename)
        list_install_dirs = db_get(section,"install_dirs","")
        for d in list_install_dirs.split("\n"):
            if os.path.exists(d) and os.path.isdir(d):
                self.install_dirs.append(d)

    def list_modified_files(self):
        return list(self.modified_files) # return a copy

    def uninstall(self,force=False,quiet=False):
        if not force and not quiet:
            for i in self.modified_files:
                logging.info("File %s was modified by hand. It will not be deleted." % i )
        elif force and not quiet:
            for i in self.modified_files:
                logging.info("File %s was modified by hand. It will be deleted (force mode)." % i )

        for f in self.install_files:
            if (force or (f not in self.modified_files)) and f.endswith(".py") and os.path.exists(f+"c"):
                self.install_files.append(f+"c")
            if (force or ( f not in self.modified_files)) and f.endswith(".py") and os.path.exists(f+"o"):
                self.install_files.append(f+"o")
        for f in self.install_files:
            if force or (f not in self.modified_files):
                if not quiet:
                    print("delete ", f)
                try:
                    os.unlink(f)
                    self.removed_files.append(f)
                except OSError as err:
                    logging.error("Could not remove file %s: %s" % (f, str(err)))

        directories = self.install_dirs
        # Innermost directories first
        directories.sort(key=lambda d: d.count(os.sep), reverse=True)
        for i in directories:
            if os.path.isdir(i) and not (os.listdir(i)):
                if not quiet:
                    print("delete directory ", i)
                try:
                    os.rmdir(i)
                    self.removed_dirs.append(i)
                except OSError as err:
                    logging.error("Could not remove directory %s: %s" % (i, str(err)))
            elif not quiet:
                logging.info("Directory %s is not empty - will not be removed." % i)


def download(url,outdir=None,outname=None, toMem=False, username="",password=""):
    if not toMem:
        if not outname:
            outname = os.path.basename(urllib.parse.urlparse(url)[2])
        if outdir:
            outpath = os.path.join(outdir, outname)
        else:
            outpath = outname
        if outdir and not os.path.exists(outdir):
            os.makedirs(outdir)
        if os.path.exists(outpath):
            #if not opts.FORCE and not os.stat(outpath).st_size==0:
            #    logging.info("Not overwriting %s" % outpath)
            #    return outpath
            #else:
            logging.info("Overwriting file at %s" % outpath)
            os.remove(outpath)
    hreq = None
    out = None
    try:
        logging.info("Downloading %s" % url)
        if username or password:
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, url, username, password)
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            opener = urllib.request.build_opener(handler)
            urllib.request.install_opener(opener)

        hreq = urllib.request.urlopen(url)
        if not toMem:
            out = open(outpath, "wb")
        else:
            out = io.BytesIO()
        out.write(hreq.read())
        hreq.close()
        if not toMem:
            out.close()
            return outpath
        else:
            return out
    except urllib.error.URLError as err:
        logging.error("Problem downloading file from %s: %s" % (url, str(err)))
    except urllib.error.HTTPError as e:
        logging.error("Problem downloading file from %s: Error code %s" % (url, e.code))
    except IOError as e:
        logging.error("Problem while writing file %s: %s" % (outpath, str (e)))
    if out:
        out.close()
    if hreq:
        hreq.close()
    return None


## Function to unpack a tarball
def unpack_tarball(path,targetdir,prune=False,overwrite=True):
    import tarfile
    tar = tarfile.open(path,errorlevel=2)
    targetdir = os.path.abspath(targetdir)
    try:
        if prune:
            prefix = os.path.commonprefix(tar.getnames())
        for i in tar.getnames():
            if "../" in i or os.path.isabs(i) or "\n" in i:
                logging.fatal("Not allowed filename %s in tarball %s." % (repr(i), repr(path)))
                return False
            if not prune:
                if not os.path.exists(os.path.join(targetdir, i)) or overwrite:
                    tar.extract(i, path=targetdir)
            else:
                target = i
                if i == prefix:
                    continue
                if len(i)>len(prefix) and prune and prefix:
                     target = target[len(prefix):]
                if target and os.path.sep == target[0]:
                    target = target[1:]
                if not target:
                    continue
                f = tar.getmember(i)
                if not f:
                    continue
                target = os.path.join(targetdir, target)
                logging.debug("Extract file -> %s" % target)
                if f.isdir():
                    if target and (not os.path.exists(target)):
                        os.makedirs(target)
                if f.isfile():
                    out_dir = os.path.dirname(target)
                    inf = tar.extractfile(i)
                    if out_dir and (not os.path.exists(out_dir)):
                        os.makedirs(out_dir)
                    with open(target, "wb") as outf:
                        outf.write(inf.read())
                    inf.close()
                    os.chmod(target,f.mode)
                    os.utime(target, (f.mtime, f.mtime))
                elif f.islnk() or f.issym():
                    true_link_target = os.path.abspath(os.path.join(os.path.dirname(target),f.linkname))
                    if not targetdir in os.commonprefix(true_link_target, targetdir):
                        logging.error("Not allowed link target %s of filename %s in tarball %s." % (repr(f.linkname),repr(i), repr(path)))
                        continue
                    if f.islnk():
                        os.link(true_link_target,target)
                    elif f.issym():
                        os.symlink(f.linkname,target)

    except tarfile.TarError as err:
        logging.error("Could not extract %s: %s" % (path,str(err)))
        return False
    except IOError as err:
        logging.error("Could not extract %s: %s" % (path,str(err)))
        return False
    except OSError as err:
        logging.error("Could not extract %s: %s" % (path,str(err)))
        return False


    tar.close()
    return True


def get_keypress():
    # source http://docs.python.org/2/faq/library#how-do-i-get-a-single-keypress-at-a-time
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                #c = sys.stdin.read(1)
                c = os.read(sys.stdin.fileno(), 1)
                return chr(ord(c))
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


def ask_yesno(message,default=False):
    if opts.BATCH:
        logging.info(message + " -> " + (default and "Yes" or "No") + " (batch mode)")
        return default
    if not default:
        message = message + " -- (N)o (y)es)? "
    else:
        message = message + " -- (Y)es (n)o)? "
    while 1:
        sys.stdout.write(message)
        sys.stdout.flush()
        c = get_keypress()
        sys.stdout.write("\n")
        if c == "\n":
            logging.debug(message + " -> " + (default and "Yes" or "No") + " (default)")
            return default
        if c in "YyJjOo":
            logging.debug(message + " -> " + "Yes")
            return True
        elif c in "Nn":
            logging.debug(message + " -> " + "No")
            return False
        elif c in "qQ":
            logging.fatal("Installation aborted.")
            sys.exit(1)

        print("Please press Y or N or Enter for the default (%s) or 'Q' to quit." % (default and "Y" or "N"))

def ask(message,default=None):
    if opts.BATCH:
        logging.info(message + " -> " + str(default) + " (batch mode)")
        return default
    c = input(message)
    sys.stdout.write("\n")
    if not c:
        c = default
    logging.debug(message + " -> " + default)
    return c



def generatePossibleDirs(suffix, **opts):
  user_home = os.getenv("HOME")
  #golem_dir = gpath.golem_path()
  curdir = os.path.abspath(os.path.curdir)
  result = []

  if suffix == "lib" and "libdir" in opts:
     libdir = opts["libdir"]
     result.append(libdir)

  if suffix == "bin" and "bindir" in opts:
     bindir = opts["bindir"]
     result.append(bindir)

  if "prefix" in opts:
     prefix = opts["prefix"]
     d = os.path.join(prefix, suffix)
     if d not in result:
        result.append(d)

  if suffix == "lib":
     ldp = os.getenv("LD_LIBRARY_PATH")
     if ldp:
        for path in ldp.split(os.path.pathsep):
           if path not in result:
              result.append(path)

  if suffix.startswith("include"):
     # guess include path from LD_LIBRARY_PATH
     ldp = os.getenv("LD_LIBRARY_PATH")
     if ldp:
        for path in ldp.split(os.path.pathsep):
           guess_path= os.path.abspath(os.path.join(path,os.path.pardir,suffix))
           if guess_path not in result:
              result.append(guess_path)

  if suffix == "bin":
     ldp = os.getenv("PATH")
     if ldp:
        for path in ldp.split(os.path.pathsep):
           if path not in result:
              result.append(path)
  for path in [
        os.path.join("/usr", suffix),
        os.path.join("/usr", "local", suffix),
        os.path.join(user_home, suffix),
        os.path.join(user_home, "local", suffix),
        #os.path.join(golem_dir, suffix),
        os.path.join(curdir, suffix),
        os.path.join(curdir, "local", suffix)]:
     if path not in result:
        result.append(path)

  return result

def find_executables(prognames, dirs):
    assert type(prognames) == list
    locations = []
    for progname in prognames:
        for dir in dirs:
           fname = os.path.join(dir, progname)
           if os.path.exists(fname) and (os.path.isfile(fname) or os.path.islink(fname)):
              if dir not in locations:
                 locations.append(fname)
    return locations

def get_form_version(executable):
    version_string = ""
    try:
        pipe = subprocess.Popen(executable,
           shell=True,
           encoding="utf8",
           bufsize=500,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE).stdout
        for line in pipe.readlines():
           lline = line.lower().strip()
           if "version" in lline:
              i = lline.index("version")
              j = lline.index("(")
              lline = lline[i+len("version"):j]
              #version = [int(re.sub("[^0-9]", "", s))
              #      for s in lline.split(".")]
              version_string = lline
           elif lline.startswith("form") or lline.startswith("tform"):
              # form version 4.0 prints
              # "FORM 4.0 (Jun 11 2012) 64-bits"
              try:
                 lline = lline.split(" ")[1]
              except IndexError:
                 pass
              version_string = lline
              #version = [int(re.sub("[^0-9]", "", s))
              #      for s in lline.split(".")]
    except OSError:
        logging.warning("Could not execute %s." % executable)
    return version_string

def get_qgraf_version(executable):
    try:
        pipe = subprocess.Popen(executable,
           shell=True,
           encoding="utf8",
           bufsize=500,
           stdout=subprocess.PIPE).stdout
        for line in pipe.readlines():
           lline = line.lower().strip()
           if "qgraf-" in lline:
               match = re.match(r".*qgraf-([^ ]*)\s*",line)
               if match and match.group(1):
                   return match.group(1).strip()
    except OSError:
        logging.warning("Could not execute %s." % executable)

def prepare_pkg(pkgname):
    section = "pkg_"+pkgname
    settings = dict(config.items(section))
    name = settings.get("official_name",pkgname)
    install = True
    final_path = ""
    if "check_if_existing" in settings and config.getboolean(section,"check_if_existing"):
        logging.info("Searching for existing " + name + " installations...")
        binaries = settings.get("binary","").split()
        answer = False
        if binaries:
            hints = find_executables(binaries,generatePossibleDirs("bin"))
            ver_parser = settings.get("version_parser","")
            found = ""
            newest_found_ver = ""
            if hints and ver_parser:
                    for p in hints:
                         ver = eval(ver_parser + '(' +repr(p)+")")
                         if not found or version_compare(ver,newest_found_ver)>0:
                             found = p
                             newest_found_ver = ver
            if newest_found_ver:
                logging.info("Found %s %s at %s" % (name,newest_found_ver,found))
                want_version = settings.get("version","")
                recent = version_compare(newest_found_ver, want_version)
                if recent < 0:
                    answer = ask_yesno(("The version of %s on the system is outdated (%s, ours is %s).\n"+
                      "Should GoSam use %s nevertheless at %s") % (name, newest_found_ver, want_version, name, found) ,False)
                if recent == 0:
                    answer = ask_yesno(("The version of %s on the system seems up to date (%s).\n"+
                      "Should GoSam use %s at %s") % (name, newest_found_ver, name, found) ,True)
                if recent > 0:
                    answer = ask_yesno(("The version of %s on the system is newer than expected (%s, ours is %s). This could cause incompabilities.\n"+
                      "Should GoSam use %s at %s") % (name, newest_found_ver, want_version, name, found) ,True)
                if answer:
                    final_path = newest_found_ver
                    install = False
            else:
                logging.debug("%s not found on the system." % name)

            if not answer:
                while 1:
                    answer = ask("Press ENTER if %s should be installed or provide a custom path to the directory with the %s binary: " % ( name, name ),"")
                    if answer and os.path.exists(answer) and os.path.isdir(answer):
                            for i in binaries:
                                tmp_path = os.path.join(answer,i)
                                if os.path.isfile(tmp_path) or os.path.islink(tmp_path):
                                    answer = tmp_path
                                    break
                    if answer and (not os.path.exists(answer) or not (os.path.isfile(answer) or os.path.islink(answer))):
                        logging.warning("Binary %s not found. Press Ctrl-C to stop." % answer)
                    else:
                        break
                if answer:
                    final_path = answer
                    logging.debug("Using %s from %s." % (name,final_path))
                    install = False
    return install, final_path

def install_pkg(pkgname):
    retval = True
    section = "pkg_"+pkgname
    settings = dict(config.items(section))
    if pkgname == "gosam_setup_env":
        write_gosam_env(update_mode=True)
        return retval
    name = settings.get("official_name",pkgname)
    logging.info("Installing %s." % name)
    download_dir = config.get("general","download_unpack_subdir")
    if not os.path.isdir(download_dir):
        try:
            download_dir = os.path.join(os.getcwd(),download_dir)
            os.makedirs(download_dir)
        except OSError as err:
            logging.fatal("Could not create download directory " + download_dir + ": " + str(err))
            return False
    if not os.access(download_dir, os.W_OK):
        logging.error("Can't write to download directory, %s. Exiting." % download_dir)
        return False

    target_file = pkgname+".tar.gz"
    settings_url = settings["url"]
    if "user" in settings and "password" in settings:
        target_file = download(settings_url,download_dir,target_file,username=settings["user"],password=settings["password"])
    else:
        target_file = download(settings_url,download_dir,target_file)
    if not target_file and "backup_url" in settings:
        logging.error("Could not download %s from %s, trying %s" % (name , settings["url"],settings["backup_url"]))
        settings_url = settings["backup_url"]
        target_file = download(settings_url,download_dir,target_file)
    if not target_file:
            logging.fatal("Could not download %s from %s" % (name , settings_url))
            #TODO backup solution
            return False
    unpack_dir= os.path.join(download_dir,pkgname)
    unpack_tarball(target_file,unpack_dir,prune=True)

    tracker = InstallTracker(pkgname,name,settings.get("version",""))
    tracker.store_build_variables(opts)

    ## Install to the PREFIX location
    prefix = os.path.abspath(opts.prefix)
    if not os.path.exists(prefix):
        os.makedirs(prefix)
        tracker.add_directories([prefix])
    if not os.access(prefix, os.W_OK):
        logging.error("Can't write to installation directory, %s... exiting" % prefix)
        return False

    bindir = os.path.join(prefix, "bin")
    if not os.path.exists(bindir):
        os.makedirs(bindir)
        tracker.add_directories([bindir])
    incdir = os.path.join(prefix, "include")
    if not os.path.exists(incdir):
        os.makedirs(incdir)
        tracker.add_directories([incdir])
    libdir = os.path.join(prefix, "lib")
    if not os.path.exists(libdir):
        os.makedirs(libdir)
        tracker.add_directories([libdir])

    my_config.paths.add(bindir)
    my_config.ldpaths.add(libdir)

    build_variables = dict()

    build_variables["prefix"] = prefix
    build_variables["incdir"] = incdir
    build_variables["libdir"] = libdir
    build_variables["bindir"] = bindir
    build_variables["fc"] = opts.FC
    build_variables["cc"] = opts.CC
    build_variables["cxx"] = opts.CXX
    build_variables["jmake"] = opts.JMAKE
    build_variables["gosam_contrib_options"] = opts.GOSAM_CONTRIB_OPTIONS

    if settings.get("use_backup_if_no_autotools",False):
        #TODO, but not here
        pass
    last_dir = os.getcwd()
    os.chdir(unpack_dir)


    if opts.LOGLEVEL == logging.INFO:
        sys.stdout.write("\n")

    steps = 0
    for no in range(99):
        if "setup_command"+str(no) in settings:
            steps = steps+1

    cur_step = 0
    try:
        tracker.broken = True
        tracker.store_to_ini_file( os.path.join(last_dir,opts.INSTALLLOG))
        for no in range(99):
            if "setup_command"+str(no) in settings:
                cur_step = cur_step+1
                command = settings["setup_command"+str(no)].format(**build_variables)
                if opts.LOGLEVEL == logging.INFO:
                    if "setup_comment"+str(no) in settings:
                        comment = settings["setup_comment"+str(no)].format(**build_variables)
                        sys.stdout.write("\r"+" "*80)
                        sys.stdout.write("\rBuilding and Installing %s: step [%s / %s - %s] ..." % (name, cur_step,steps,comment) )
                        sys.stdout.flush()
                    else:
                        sys.stdout.write("\r"+" "*80)
                        sys.stdout.write("\rBuilding and Installing %s: step [%s / %s] ... "% (name, cur_step,steps) )
                        sys.stdout.flush()
                logging.debug("Execute %s",repr(command))
                process = subprocess.Popen(command,
                   shell=True,
                   encoding="utf8",
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
                output_stdout,output_stderr= process.communicate()
                retcode= process.returncode
                if retcode != 0:
                    logging.error("\n%s step [%s / %s] failed." % (name, cur_step,steps))
                    if retcode < 0:
                        logging.error("Program was terminated by signal %s" % -retcode)
                    else:
                        logging.error("Program returned %s" % retcode)
                    sys.stdout.flush()
                    if output_stdout:
                        logging.error("Last stdout output lines:\n >" + "\n >".join(output_stdout.split("\n")[-15:]))
                    if output_stderr:
                        logging.error("Last stderr output lines:\n >" + "\n >".join(output_stderr.split("\n")[-15:]))
                if output_stdout:
                    logging.debug("Output stdout: " + output_stdout)
                if output_stderr:
                    logging.debug("Output stderr: " + output_stderr)
                tracker.analyse_output(output_stdout)
                tracker.analyse_output(output_stderr)
                if retcode != 0:
                    retval = False
                    break
                tracker.broken = not retval
                tracker.store_to_ini_file( os.path.join(last_dir,opts.INSTALLLOG))
        tracker.broken = not retval
        tracker.store_to_ini_file( os.path.join(last_dir,opts.INSTALLLOG))
    except OSError as err:
        retval = False
        logging.error(str(err))
        logging.error("Installation failed.")
    finally:
        os.chdir(last_dir)

    if not retval:
        logging.error("Installation failed.")

    if opts.LOGLEVEL == logging.INFO:
        sys.stdout.write(" finished.\n")
    return retval

def write_gosam_env(update_mode=False,successful_before=True):
    global config

    output_path = my_config.output_path
    paths = [ os.path.abspath(i) for i in my_config.paths ]
    ldpaths = [ os.path.abspath(i) for i in my_config.ldpaths ]
    basepath = os.path.abspath(opts.prefix)

    env_file = os.path.join(opts.prefix,"bin","gosam_setup_env.sh")

    tracker = InstallTracker("gosam_setup_env","gosam_setup_env.sh script","3")
    if not os.path.exists(os.path.join(opts.prefix,"bin")):
            os.makedirs(os.path.join(opts.prefix,"bin"))
            tracker.analyse_output("Creating %s" % os.path.join(opts.prefix,"bin"))
    try:
        fh = open(env_file,"w")
    except IOError as err:
        logging.error("Cannot create file "+repr(env_file) + ": " + str(err))
        return False
    fh.write("#!/bin/sh\n")
    fh.write("""
# tcsh and bash-compatible shell file to setup environment variables for the GoSam installation
# at """ + repr(basepath) + "\n")
    fh.write("# created by GoSam installation script %s\n" % INSTALLER_VERSION )
    fh.write("""
test "$?BASH_VERSION" = "0BASH_VERSION" || eval 'alias return true'
test "$?BASH_VERSION" = "0" || eval 'setenv() { export "$1=$2"; }'
(return 2>/dev/null) || ( echo "To setup the environment variables, please do not call this file, but source it:" && echo "  source $0" )
""")
    if paths:
        fh.write('setenv PATH ' + os.path.pathsep.join(['"'+i+'"' for i in paths]) + os.path.pathsep + "\"$PATH\"\n")
    if ldpaths:
        fh.write('setenv LD_LIBRARY_PATH ' + os.path.pathsep.join(['"'+i+'"' for i in ldpaths]) + os.path.pathsep + "\"$LD_LIBRARY_PATH\"\n")
    fh.close()
    tracker.analyse_output("Writing %s" % env_file)
    tracker.store_to_ini_file(opts.INSTALLLOG)
    if not update_mode:
        if args:
            if successful_before:
                logging.info("%s installed.\nYou need to run the following line to set environment variables before you can use it:" % ", ".join(args))
            else:
                logging.info("There was an error during installation of %s.\nYou need to run the following line to set environment variables before you can use it:" % ", ".join(args))
        else:
            if successful_before:
                logging.info("GoSam installed.\nYou need to run the following line to set environment variables before you can use GoSam:")
            else:
                logging.info("There was an error in the installation procedure. GoSam might not work correctly.\nYou need to run the following line to set environment variables before you can use GoSam:")
        logging.info(" source %s" % env_file)
    else:
        logging.info("%s updated." % env_file)

    rcfile = "~/profile"
    shell = ""
    try:
        shell = os.environ["SHELL"]
    except KeyError:
        pass
    if "bash" in shell:
        rcfile = "~/.bashrc"
    elif "zsh" in shell:
        rcfile = "~/.zshrc"
    elif "tcsh" in shell:
        rcfile = "~/.tcshrc"
    elif "csh" in shell:
        rcfile = "~/.cshrc"

    if not update_mode:
        logging.info("Add it to your %s to automate this after the re-login." % rcfile)
    return True

def general_check_environment():
    # find fortran compiler
    if opts.FC == "gfortran":
        fcs = [opts.FC] + config.get("general","supported_fortran_compilers").split()
        fcs = find_executables(fcs,generatePossibleDirs("bin"))
        if not fcs:
           logging.fatal("No fortran compiler found on the system. GoSam cannot be installed.")
           return False
        opts.FC = fcs[0]
    autoreconf = find_executables(["autoreconf"],generatePossibleDirs("bin"))
    if not autoreconf:
        logging.warning("autoreconf not found on the system. Autotools is needed for some applications of GoSam.")
    if not opts.uninstall:
        # check for free disk space
        build_space = int(config.get("general","minimal_build_diskspace",fallback="0"))
        install_space= int(config.get("general","minimal_install_diskspace",fallback="0"))

        install_path = os.path.abspath(opts.prefix)
        while not os.path.isdir(install_path):
            install_path = os.path.normpath(os.path.join(install_path,os.path.pardir))
        free_install = get_free_diskspace(install_path)
        if free_install >=0 and install_space and free_install<install_space:
            logging.warning("Not enough space for %s. About %s MB needed." % (os.path.abspath(opts.prefix),install_space) )

        build_path = config.get("general","download_unpack_subdir",fallback="")
        build_path_tmp = build_path
        while not os.path.isdir(build_path_tmp):
            build_path_tmp = os.path.normpath(os.path.join(build_path_tmp,os.path.pardir))
        free_build = get_free_diskspace(build_path_tmp)
        if free_build >=0 and build_space and free_build<build_space:
            logging.warning("Not enough space for %s. About %s MB needed." % (os.path.abspath(build_path), build_space) )



def read_config_file():
    global config
    bn = os.path.basename(CONFIG_URL)
    if os.path.exists(bn):
        cfg_file = open(bn,"rb")
        logging.warning(("Use local config file (%s). This file could be outdated.\nTo let the installer try to get " +
                "the most up-to-date file, delete this file.") % bn )
    else:
        cfg_file = download(CONFIG_URL,toMem=True)
    if not cfg_file:
        if os.path.exists(bn):
            logging.error("Could not read %s." % bn)
        else:
            logging.error("Could not download %s" % CONFIG_URL)
        sys.exit(1)
    config = configparser.ConfigParser()
    cfg_file.seek(0)
    config.read_string(cfg_file.read().decode("utf8"))
    assert config.has_option("general","pkg_install")
    assert config.has_option("general","download_unpack_subdir")

def check_self_update():
    global config

    if version_compare(config.get("gosam-installer","version",fallback=""),INSTALLER_VERSION)>0:
        if not os.path.exists(sys.argv[0]):
            logging.error("Cannot find myself: %s" % sys.argv[0])
            return True
        myself, ext = os.path.splitext(sys.argv[0])
        tmp_file = myself + "-new" + ext

        answer = ask_yesno("There is a new version of the installer available. Should I download and call it",default=True)
        if answer:
            url = config.get("gosam-installer","url",fallback="")
            success = False
            if url:
                success = download(url, outname=tmp_file)
            if not success:
                url = config.get("gosam-installer","backup_url",fallback="")
                if url:
                    success = download(url, outname=tmp_file)
            if not success:
                os.error("Could not download new version.")
                return False
            os.chmod(tmp_file, os.stat(sys.argv[0])[stat.ST_MODE])
            import py_compile
            handle,tmp_bin_path = tempfile.mkstemp()
            try:
                py_compile.compile(tmp_file,doraise=True,cfile=tmp_bin_path)
            except py_compile.PyCompileError:
                os.error("Syntax error in downloaded file. Please contact " + CONTACT + ".")
                return False
            finally:
                os.unlink(tmp_bin_path)
            os.rename(tmp_file,sys.argv[0])

            # call myself
            os.execl(sys.executable, *([sys.executable]+sys.argv))

def handle_pkgs(packages=None):
    global config
    install_pkgs = []
    ask_for_install = []
    available = config.get("general","pkg_install",fallback="").split()
    extra_packages = []
    if not packages:
        ask_for_install = available
    else:
        for p in packages :
            if p == "all":
                ask_for_install.extend(available)
                continue
            if not config.has_section("pkg_" + p):
                logging.error("Package %s unknown." % p)
            else:
                if p in available:
                    ask_for_install.append(p)
                else:
                    extra_packages.append(p)

    for p in available+extra_packages: # use sorting as in config
        if p not in ask_for_install and p not in extra_packages:
            continue
        should_be_installed,path = prepare_pkg(p)
        if should_be_installed:
            install_pkgs.append(p)
        else:
            if path:
                my_config.paths.add(os.path.abspath(os.path.dirname(path)))

    retval = True
    for p in install_pkgs:
        if not install_pkg(p):
            logging.error("Installation is not complete")
            logging.error("Run the installation script with the -u flag to remove all installed files.")
            retval = False
            break
    return retval



def uninstall(pkgs=None,updated_mode=False,second_run=False):
    ini_file = opts.INSTALLLOG
    db = configparser.ConfigParser()
    if os.path.exists(ini_file):
        db.read([ini_file])
    else:
        if not second_run:
            logging.fatal("No installation found. Please run from the directory with %s or use the -l option" % INSTALLOG_DEFAULT)
        else:
            return
    secs = db.sections()
    packages = []
    if pkgs:
        for i in pkgs:
            if i == "all":
                packages.extend([x[4:] for x in secs if x.startswith("pkg_")])
            elif "pkg_"+i in secs:
                packages.append(i)
            elif not second_run:
                logging.error("Package %s unknown/not installed" % i)
    else:
        packages = [x[4:] for x in secs if x.startswith("pkg_")]
    packages.reverse()
    for p in packages:
         tracker = InstallTracker(p,"","")
         tracker.read_from_ini_file(ini_file)
         tracker.uninstall(force=updated_mode,quiet=updated_mode)
         tracker.store_to_ini_file(ini_file,True)


def check_installation(pkg_name=None):
    ini_file = opts.INSTALLLOG
    pkg_list = []
    if pkg_name:
        pkg_list = [pkg_name]
    else:
        db = configparser.ConfigParser()
        if os.path.exists(ini_file):
            db.read([ini_file])
            secs = db.sections()
            pkg_list = [x[4:] for x in secs if x.startswith("pkg_")]
        else:
            logging.fatal("No installation found.")

    if not pkg_list:
        logging.info("No installed packages found.")
        return
    mod_files = []
    trackers = {}
    for p in pkg_list:
        trackers[p] = InstallTracker(p,"","")
        trackers[p].read_from_ini_file(ini_file)
        mod_files = mod_files + trackers[p].list_modified_files()
    if mod_files:
        m = "The following files were modified by hand:\n"
        for f in mod_files:
            m = m+ "\t%s\n" % f
        logging.info(m)
        return False
    else:
        logging.info("Installation OK: There are no installed files which were modified by hand.")
    return True

def is_already_installed():
    ini_file = opts.INSTALLLOG
    if os.path.exists(ini_file):
        db = configparser.ConfigParser()
        db.read([ini_file])
        if db.has_option("generic","prefix"):
            if os.path.abspath(db.get("generic","prefix")) != os.path.abspath(opts.prefix):
                logging.fatal(("Prefix '%s' is different to prefix '%s' in %s\nPlease start the installation script from "+
                    "another directory if you want to install to a different location or use the `-l` option.") % (opts.prefix,db.get("generic","prefix"),ini_file))
                sys.exit(1)
        else:
            return False
    if not os.path.exists(opts.prefix):
        return False
    if os.path.exists(os.path.join(opts.prefix,"bin","gosam_setup_env.sh")):
        return True

def check_is_complete():
    if not os.path.exists(os.path.join(opts.prefix,"bin","gosam.py")):
        return False
    if not os.path.exists(os.path.join(opts.prefix,"bin","gosam_setup_env.sh")):
        return False
    return True

def check_update(pkgs=None,new_packages=[]):
    ini_file = opts.INSTALLLOG
    update_list = []
    db = configparser.ConfigParser()
    if os.path.exists(ini_file):
        db.read([ini_file])
        secs = db.sections()
        if not pkgs:
            packages = [x[4:] for x in secs if x.startswith("pkg_")]
        else:
            packages = pkgs
    else:
        logging.fatal("No installation found.")
        return
    m = "The following updates are available:\n"
    for p in packages:
         sec= "pkg_" + p
         if not db.has_section(sec):
             new_packages.append(p)
             continue
         if db.has_option(sec,"version") and config.has_section(sec):
             broken = db.has_option(sec,"broken") and db.get(sec,"broken")
             if version_compare(config.get(sec,"version"), db.get(sec,"version",fallback=""))>0 or broken:
                 if broken:
                    m = m + "\t%s %s (broken) -> %s\n" % ( config.get(sec,"official_name"),
                         db.get(sec,"version") , config.get(sec,"version") )
                 else:
                    m = m + "\t%s %s -> %s\n" % ( config.get(sec,"official_name"),
                         db.get(sec,"version") , config.get(sec,"version") )
                 update_list.append(p)
    m = m + "Should these components be updated?"
    if not update_list:
        logging.info("All installed files are up-to-date.")
        return
    if len(update_list)>0:
        answer = ask_yesno(m,default=True)
        if not answer:
            return
    mod_files = []
    trackers = {}
    for p in update_list:
        trackers[p] = InstallTracker(p,"","")
        trackers[p].read_from_ini_file(ini_file)
        mod_files = mod_files + trackers[p].list_modified_files()
    if mod_files:
        m = "The following files were modified by hand:\n"
        for f in mod_files:
            m = m+ "\t%s\n" % f
        m = m + "This files are overwritten by the update. Continue?"
        answer = ask_yesno(m,default=(not opts.FORCE))
        if not answer:
            return
    for p in update_list:
        trackers[p].retrive_build_variables(opts)
        update_pkg(p,ini_file)

def update_pkg(pkg,ini_file):
    uninstall([pkg],updated_mode=True)
    install_pkg(pkg)

def init_settings():
    # set global timeout 10s for urllib2
    socket.setdefaulttimeout(10)
    my_config.paths = set()
    my_config.ldpaths = set()
    my_config.output_path = os.getcwd()

def save_settings():
    db = configparser.ConfigParser()
    ini_file = opts.INSTALLLOG
    if os.path.exists(ini_file):
        db.read([ini_file])
    if not db.has_section("generic"):
        db.add_section("generic")
    db.set("generic", "paths", "\n".join(list(my_config.paths)))
    db.set("generic", "ldpaths", "\n".join(list(my_config.ldpaths)))
    try:
        f = open(ini_file,"w")
        db.write(f)
        f.close()
    except IOError as err:
        logging.error("Could not write install log to %s: %s" % (ini_file, str(err)))
        return False
    return True



def load_settings():
    db = configparser.ConfigParser()
    ini_file = opts.INSTALLLOG
    if os.path.exists(ini_file):
        db.read([ini_file])
    if not db.has_section("generic"):
        return
    if db.has_option("generic","paths"):
        my_config.paths = set(db.get("generic", "paths").split("\n"))
    else:
        my_config.paths = set([os.path.join(opts.prefix,"bin")])
    if db.has_option("generic","ldpaths"):
        my_config.ldpaths = set(db.get("generic", "ldpaths").split("\n"))
    else:
        my_config.ldpaths = set([os.path.join(opts.prefix,"lib")])
    try:
        f = open(ini_file,"w")
        db.write(f)
        f.close()
    except IOError as err:
        logging.error("Could not write install log to %s: %s" % (ini_file, str(err)))
        return False
    return True


if __name__=="__main__":
    try:
        handle_args()
        init_settings()
        setup_logging()
        setup_autocompleter()
        logging.info("Welcome to the GoSam installer!")
        read_config_file()
        check_self_update()
        if opts.check:
            check_installation()
        elif opts.uninstall:
            uninstall(args)
            # try it twice
            uninstall(args,second_run=True)
        elif is_already_installed():
            logging.info("Existing installation found in %s." % opts.prefix)
            if not check_is_complete() and not args:
                logging.info("The current installation seems not be complete.\n" +
                 "For re-installation, you first need to uninstall existing files. Use the '-u' command-line flag for this.")
            load_settings()
            # check for updates:
            new_packages = []
            if args:
                check_update(args,new_packages)
            else:
                logging.info("Checking for updates...")
                check_update()
            if new_packages: # install missing
                general_check_environment()
                ret = handle_pkgs(new_packages)
                write_gosam_env(successful_before=ret)
            save_settings()
        else:
            general_check_environment()
            ret = handle_pkgs(args)
            write_gosam_env(successful_before=ret)
            save_settings()

    except Exception as e:
        import platform
        logging.info("\nSystem info: Python %s %s %s\n %s\n",platform.python_version(), platform.machine(), platform.system(), platform.platform())
        import traceback
        traceback.print_exc()
        logging.error("\n\n")
        logging.error("An error has occurred while installing/upgrading/removing GoSam or one of its dependencies. Sorry!")
        logging.error("Please contact the GoSam developers at " + CONTACT + " with a \n\
description of your problem, a copy of this script if you did not get it directly from the GoSam webpage, \n\
and any error trace that may have appeared and we'll try to get it fixed as soon as possible. \n\
Thanks for your help!")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
