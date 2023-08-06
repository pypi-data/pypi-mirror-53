"""Setup file for hippy building/installing"""
import os
import sys
import platform
from distutils.sysconfig import parse_makefile
from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    FOUND_CYTHON = True
except ModuleNotFoundError:
    FOUND_CYTHON = False

def _build_opts():
    hosts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../host'))
    valid_host = False
    hosts = os.listdir(hosts_dir)
    if 'HIP_HOSTTYPE' in os.environ:
        host = os.environ['HIP_HOSTTYPE']
        makefile = os.path.join(hosts_dir, host, "makefile.h")
        if os.path.isfile(makefile):
            valid_host = True

    if not valid_host:
        errmsg = '"HIP_HOSTTYPE" environment variable not correctly set.\n'
        errmsg = "%sIt has to be set with a value from: \n\t- " %errmsg
        errmsg = "%s%s" %(errmsg, "\n\t- ".join(hosts))
        raise RuntimeError(errmsg)

    os.environ["CGNS"] = "1"
    os.system("make -p -f %s  > makefile_out 2>&1" %makefile)
    out = parse_makefile("makefile_out")
    os.remove("makefile_out")
    opts = {"CFLAGS":[], "LFLAGS":[]}
    opts["LFLAGS"].extend("-L../lib_do/clapack/ -lclapack_LINUX".split())
    opts["LFLAGS"].extend("-L../lib_do/clapack/F2CLIBS/libf2c -lf2c".split())
    mk_vars = ['LIBFLAGS_LINUX', 'LIBFLAGS_HDF5', 'LIBFLAGS_CGNS', 'CFLAGS']
    for var in mk_vars:
        opts["LFLAGS"].extend(out[var].split())
    opts["CFLAGS"].extend(out['MACH_FLAGS'].split())
    return opts

def build_extension():
    """Build extension"""
    build_from_src = False
    if len(sys.argv) > 1:
        if sys.argv[1].strip().lower() == "build" and FOUND_CYTHON:
            build_from_src = True

    if not build_from_src:
        ext = [Extension("hip_wrapper",
                         language='c',
                         sources=['./hippy/hip_wrapper.c'])]
    else:
        opts = _build_opts()
        ext = cythonize(Extension("hip_wrapper",
                                  extra_compile_args=opts['CFLAGS'],
                                  include_dirs=["../src"],
                                  extra_link_args=opts['LFLAGS'],
                                  language='c',
                                  sources=['./hippy/hip_wrapper.pyx']
                                  )
                        )
    return ext

NAME = "hipppy"
VERSION = "0.1.0"
DESCR = """A Python interface to Hip which is a package for manipulating
           unstructured computational grids and their associated datasets"""
URL = "http://www.cerfacs.fr/avbp7x/hip.php"

AUTHOR = "Jens-Dominik Mueller, CERFACS"
EMAIL = "j.mueller@qmul.ac.uk, gabriel.staffelbach@cerfacs.fr, erraiya@cerfacs.fr"

LICENSE = "CeCILL-B Free Software License Agreement (CECILL-B)"

SRC_DIR = "hippy"
PACKAGES = [SRC_DIR]
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
EXT = build_extension()

setup(packages=PACKAGES,
      name=NAME,
      version=VERSION,
      description=DESCR,
      long_description=README,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license=LICENSE,
      ext_modules=EXT,
      python_requires='>=3.6.0',
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Topic :: Scientific/Engineering :: Physics"
                   ]
      )
