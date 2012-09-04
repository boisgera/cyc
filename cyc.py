#!/usr/bin/env python
# coding: utf-8

"""
Cython-based compiler
"""

# Python 2.7 Standard Library
import contextlib
import os.path
import sys
import shutil
import tempfile

# Third-Party Libraries
import pbs

# Metadata
__author__ = u"Sébastien Boisgérault <Sebastien.Boisgerault@mines-paristech.fr>"
__license__ = "MIT License"
__url__ = "https://github.com/boisgera/cyc" 
__version__ = None


PYTHON_CFLAGS = str(pbs.pkg_config("python", cflags=True)).strip()

join = os.path.join

@contextlib.contextmanager
def temp_dir():
    dir = tempfile.mkdtemp()
    try:
        yield dir
    finally:
        shutil.rmtree(dir)

def compile(filename, build_dir=""):
    basename = ".".join(filename.split(".")[:-1])
    cname = join(build_dir, basename + ".c")
    pbs.cython(filename, o=cname)
    args = "-shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing".split()
    args.append([PYTHON_CFLAGS])
    args.append(["-o", basename + ".so", cname])
    pbs.gcc(*args)

def main(filenames):
    with temp_dir() as build_dir:
        for filename in filenames:
            compile(filename, build_dir)

if __name__ == "__main__":
    main(sys.argv[1:])

