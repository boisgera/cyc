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
import script


# Metadata
__author__ = u"Sébastien Boisgérault <Sebastien.Boisgerault@mines-paristech.fr>"
__license__ = "MIT License"
__url__ = "https://github.com/boisgera/cyc" 
__version__ = None


@contextlib.contextmanager
def temp_dir():
    dir = tempfile.mkdtemp()
    try:
        yield dir
    finally:
        shutil.rmtree(dir)

CFLAGS = str(pbs.pkg_config("python", cflags=True)).strip()
LIBS = str(pbs.pkg_config("python", libs=True)).strip()

def compile(filename, main=False, build_dir=""):
    name = ".".join(filename.split(".")[:-1])
    basename = os.path.basename(name)
    cname = os.path.join(build_dir, basename + ".c")
    pbs.cython(filename, "--embed", o=cname)
    if main:
        args = [CFLAGS]
        args.append(["-o", name, cname])
        args.append(LIBS)
    else:
        args = ["-shared", "-pthread", "-fPIC", CFLAGS]
        args.append(["-o", name + ".so", cname])
    pbs.gcc(*args)

def main(args=None):
    args = args or sys.argv[1:]
    spec = "help main" 
    options, filenames = script.parse(spec, args)
    if options.help or not filenames:
        print help()
    else:
        main = bool(options.main)
        with temp_dir() as build_dir:
            for filename in filenames:
                compile(filename, main=main, build_dir=build_dir)

def help():
    """usage:

    cyc [-m/--main] [FILENAMES]
"""
    return help.__doc__

if __name__ == "__main__":
    main()


