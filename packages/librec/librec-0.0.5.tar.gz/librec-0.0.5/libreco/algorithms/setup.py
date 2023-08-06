from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np

compile_args = ['-Wno-unused-function', '-Wno-maybe-uninitialized', '-O3', '-ffast-math']
link_args = []
compile_args.append("-fopenmp")
link_args.append("-fopenmp")

setup(ext_modules=cythonize([Extension('superSVD_cy', ['superSVD_cy.pyx'], include_dirs=[np.get_include()]),
                             Extension('superSVD_cys', ['superSVD_cys.pyx'], include_dirs=[np.get_include()]),
                             Extension('Als_cy', ['Als_cy.pyx'],
                                       extra_compile_args=compile_args, extra_link_args=link_args),
                             Extension('Als_rating_cy', ['Als_rating_cy.pyx'])]))



