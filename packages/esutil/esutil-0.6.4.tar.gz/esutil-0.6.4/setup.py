import sys,os
import time
from sys import stdout,stderr
from glob import glob
import platform

from distutils.core import setup,Extension

import distutils.sysconfig
import os

# can we build recfile?
packages = ['esutil']
ext_modules = []
try:
    import numpy
    include_dirs=[numpy.get_include()]
    include_dirs += ['esutil/include']
    have_numpy=True
except:
    have_numpy=False
    ext_modules=[]
    include_dirs=[]

    stdout.write('Numpy not found:  Not building C extensions\n')
    time.sleep(5)

if platform.system()=='Darwin':
    extra_compile_args = ['-stdlib=libc++']
    extra_link_args=[]
else:
    extra_compile_args=[]
    extra_link_args=[]


if have_numpy:
    # recfile
    include_dirs += ['esutil/recfile']
    recfile_sources = ['esutil/recfile/records.cpp',
                       'esutil/recfile/records_wrap.cpp']
    recfile_module = Extension('esutil.recfile._records',
                               extra_compile_args=extra_compile_args,
                               extra_link_args=extra_link_args,
                               sources=recfile_sources,
                               include_dirs=include_dirs)
    ext_modules.append(recfile_module)
    packages.append('esutil.recfile')

    # cosmology package
    cosmo_sources = glob('esutil/cosmology/*.c')
    cosmo_module = Extension('esutil.cosmology._cosmolib',
                             extra_compile_args=extra_compile_args,
                             extra_link_args=extra_link_args,
                             sources=cosmo_sources,
                             include_dirs=include_dirs)
    ext_modules.append(cosmo_module)
    packages.append('esutil.cosmology')



    # HTM
    include_dirs += ['esutil/htm','esutil/htm/htm_src']
    htm_sources = glob('esutil/htm/htm_src/*.cpp')
    htm_sources += ['esutil/htm/htmc.cc','esutil/htm/htmc_wrap.cc']
    htm_module = Extension('esutil.htm._htmc',
                           extra_compile_args=extra_compile_args,
                           extra_link_args=extra_link_args,
                           sources=htm_sources,
                           include_dirs=include_dirs)

    ext_modules.append(htm_module)
    packages.append('esutil.htm')




    # stat package
    #include_dirs += ['esutil/stat']
    #chist_sources = ['chist.cc','chist_wrap.cc']
    #chist_sources = ['esutil/stat/'+s for s in chist_sources]
    chist_sources = ['esutil/stat/chist_pywrap.c']
    chist_module = Extension('esutil.stat._chist',
                             extra_compile_args=extra_compile_args,
                             extra_link_args=extra_link_args,
                             sources=chist_sources,
                             include_dirs=include_dirs)
    ext_modules.append(chist_module)
    stat_util_sources = ['_stat_util.c']
    stat_util_sources = ['esutil/stat/'+s for s in stat_util_sources]
    stat_util_module = Extension('esutil.stat._stat_util',
                                 extra_compile_args=extra_compile_args,
                                 extra_link_args=extra_link_args,
                                 sources=stat_util_sources,
                                 include_dirs=include_dirs)
    ext_modules.append(stat_util_module)
    packages.append('esutil.stat')


    # integrate package

    #cgauleg_sources = glob('esutil/integrate/*.cc')
    cgauleg_sources = glob('esutil/integrate/cgauleg_pywrap.c')
    cgauleg_module = Extension('esutil.integrate._cgauleg',
                               extra_compile_args=extra_compile_args,
                               extra_link_args=extra_link_args,
                               sources=cgauleg_sources,
                               include_dirs=include_dirs)
    ext_modules.append(cgauleg_module)
    packages.append('esutil.integrate')


    packages.append('esutil.unit_tests')

long_description="""
A python package including a wide variety of utilities, focused primarily on
numerical python, statistics, and file input/output.   Includes specialized
tools for astronomers.

For full documentation see the project web site http://code.google.com/p/esutil/


Tests
-----

All tests should pass

```python
import esutil as eu
eu.test()
```
"""

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Topic :: Scientific/Engineering :: Astronomy",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]


setup(name='esutil',
      version="0.6.4",
      author="Erin Scott Sheldon",
      author_email="erin.sheldon@gmail.com",
      classifiers=classifiers,
      description='Erin Sheldons Python Utilities',
      long_description=long_description,
      license = "GPL",
      url='http://code.google.com/p/esutil/',
      packages=packages,
      ext_modules=ext_modules)
#, install_requires=['numpy'])
