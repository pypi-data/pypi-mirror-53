#!/usr/bin/env python3

"""Setup for adcc"""
import setuptools

from setuptools import find_packages, setup

# Version of the python bindings and adcc python package.
__version__ = '0.1.0'

long_description = """
adcc is a python-based framework for performing quantum-chemical simulations
based upon the algebraic-diagrammatic construction (ADC) approach.

As of now PP-ADC and CVS-PP-ADC methods are available to compute excited
states on top of an MP2 ground state. The underlying Hartree-Fock reference
is not computed inside adcc, much rather external packages should be used
for this purpose. Interfaces to seamlessly interact with pyscf, psi4,
VeloxChem or molsturm are available, but other SCF codes or even statically
computed data can be easily used as well.

Notice, that only the adcc python and C++ source code are released under the
terms of the GNU Lesser General Public License v3 (LGPLv3) license. This
license does not apply to the libadccore.so binary file contained inside
the directory '/adcc/lib/' of the distributed tarball. For further details
see the file LICENSE_adccore.
""".strip()  # TODO extend
setup(
    name='adcc',
    description='adcc:  Seamlessly connect your host program to ADC',
    long_description=long_description,
    #
    url='https://adc-connect.org',
    author="Michael F. Herbst, Maximilian Scheurer",
    author_email='adcc+developers@michael-herbst.com',
    license="LGPL v3",
    #
    version=__version__,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',
        'License :: Free For Educational Use',
        'Intended Audience :: Science/Research',
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Education",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],
    #
    packages=find_packages(exclude=["*.test*", "test"]),
    zip_safe=False,
    #
    platforms=["Linux", "Mac OS-X"],
    python_requires='>=3.5',
)
