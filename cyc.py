#!/usr/bin/env python

# Python 2.7 Standard Library
import sys

# Third-Party Libraries
import pbs

# -----

PYTHON_CFLAGS = str(pbs.pkg_config("python", cflags=True)).strip()

def compile(filename):
    """gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
      $(CFLAGS) -o mod.so mod.c
    """
    basename = ".".join(filename.split(".")[:-1])
    pbs.cython(filename, o=basename + ".c")
    args = "-shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing".split()
    args.append([PYTHON_CFLAGS])
    args.append(["-o", basename + ".so", basename + ".c"])
    pbs.gcc(*args)

if __name__ == "__main__":
    main(sys.argv[1:])
