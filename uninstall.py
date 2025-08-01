#!/usr/bin/env python3
import os
import shutil

bindir = os.path.join(os.environ["prefix"], os.environ["bindir"])
libdir = os.path.join(os.environ["prefix"], os.environ["libdir"])
includedir = os.path.join(os.environ["prefix"], os.environ["includedir"])
datadir = os.path.join(os.environ["prefix"], os.environ["datadir"])
py_dir = os.path.join(os.environ["prefix"], os.environ["py_dir"])

print(f"Removing {os.path.join(bindir, '../gosam.py')}...")
os.remove(os.path.join(bindir, "../gosam.py"))
print(f"Removing {bindir}...")
shutil.rmtree(bindir)
print(f"Removing {libdir}...")
shutil.rmtree(libdir)
print(f"Removing {includedir}...")
shutil.rmtree(includedir)
print(f"Removing {datadir}...")
shutil.rmtree(datadir)
print(f"Removing {py_dir}...")
shutil.rmtree(py_dir)
