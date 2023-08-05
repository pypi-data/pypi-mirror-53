# ----------------------------------------------------------------------------
# IW - Pyramidal algoriths for waveltt decomposition on Graph
#         - see file license.txt
#
# distutils:
import re, os, sys
import io
import shutil
#from distutils.core import setup, Extension
from setuptools import setup, find_packages, Extension
from distutils.command.clean import clean as _clean
from distutils.dir_util import remove_tree
from distutils.command.sdist import sdist
# Test if Cython is installed
USE_CYTHON = True

try:
    from Cython.Distutils import build_ext
except:
    USE_CYTHON = False
    raise 'Cannot build iw without cython'
    sys.exit()

try:
    import numpy
except:
    raise 'Cannot build iw without numpy'
    sys.exit()

# --------------------------------------------------------------------
# Clean target redefinition - force clean everything supprimer de la liste '^core\.*$',
relist = ['^.*~$', '^#.*#$', '^.*\.aux$', '^.*\.pyc$', '^.*\.o$']
reclean = []
USE_COPYRIGHT = True
try:
    from copyright import writeStamp, eraseStamp
except ImportError:
    USE_COPYRIGHT = False

###################
# Get IntertwiningWavelet version
####################
def get_version():
    v_text = open('VERSION').read().strip()
    v_text_formted = '{"' + v_text.replace('\n', '","').replace(':', '":"')
    v_text_formted += '"}'
    v_dict = eval(v_text_formted)
    return v_dict["iw"]

########################
# Set IntertwiningWavelet __version__
########################
def set_version(iw_dir, version):
    filename = os.path.join(iw_dir, '__init__.py')
    buf = ""
    for line in open(filename, "rb"):
        if not line.decode("utf8").startswith("__version__ ="):
            buf += line.decode("utf8")
    f = open(filename, "wb")
    f.write(buf.encode("utf8"))
    f.write(('__version__ = "%s"\n' % version).encode("utf8"))

for restring in relist:
    reclean.append(re.compile(restring))


def wselect(args, dirname, names):
    for n in names:
        for rev in reclean:
            if (rev.match(n)):
                os.remove("%s/%s" %(dirname, n))
        break


######################
# Custom clean command
######################
class clean(_clean):
    def walkAndClean(self):
        os.walk("..", wselect, [])
        pass

    def run(self):
        clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('iw'):
            for filename in filenames:
                if (filename.endswith('.so') or
                        filename.endswith('.pyd') or
                        filename.endswith('.dll') or
                        filename.endswith('.pyc')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


##############################
# Custom sdist command
##############################
class m_sdist(sdist):
    """ Build source package

    WARNING : The stamping must be done on an default utf8 machine !
    """

    def run(self):
        if USE_COPYRIGHT:
            writeStamp()
            sdist.run(self)
            # eraseStamp()
        else:
            sdist.run(self)


##########################
# File path read command
##########################
def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with io.open(os.path.join(*paths), 'r', encoding='utf-8') as f:
        return f.read()


opj = os.path.join
ICI = os.getcwd()

PATH_INCLUDES = [numpy.get_include(), '.', './iw/test', 'iw/multiresolution',
                 './iw', './iw/reconstruction', './iw/function_fab', './iw/diaconis_fill',
                 './iw/kernel_c']

PATH_LIBRARIES = ['build', os.path.abspath("./kernel_c"), '.'] # ICI+'/lib'
LINK_LIBRARIES = ["m", ]

EXTRA_COMPIL_ARGS = ['-g', '-w']

ext_modules = [Extension("iw.function_fab.stairsum",
                         ["iw/function_fab/stairsum.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.diaconis_fill.complementschur",
                         ["iw/diaconis_fill/complementschur.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.diaconis_fill.cal_beta_gamma",
                         ["iw/diaconis_fill/cal_beta_gamma.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.multiresolution.sparsify_matrix",
                         ["iw/multiresolution/sparsify_matrix.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.multiresolution.tab_one_step_Lambda",
                         ["iw/multiresolution/tab_one_step_Lambda.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.reconstruction.operateur_reconstruction_one_step",
                         ["iw/reconstruction/operateur_reconstruction_one_step.pyx",],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.graph_c",
                         ["iw/graph_c.pyx",
                          "iw/kernel_c/cuore.c", "iw/kernel_c/lodge.c",
                          "iw/kernel_c/rforest_internal.c"],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         include_path=PATH_INCLUDES,
                         libraries=LINK_LIBRARIES,
                         extra_compile_args=EXTRA_COMPIL_ARGS,
                         ),
               Extension("iw.multiresolution.struct_multires_Lbarre",
                         ["iw/multiresolution/struct_multires_Lbarre.pyx",
                          "iw/reconstruction/operateur_reconstruction_one_step.pyx",
                          "iw/graph_c.pyx", "iw/kernel_c/cuore.c", "iw/kernel_c/lodge.c",
                          "iw/kernel_c/rforest_internal.c"],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         include_path=PATH_INCLUDES,
                         libraries=LINK_LIBRARIES,
                         extra_compile_args=EXTRA_COMPIL_ARGS,
                         ),
               Extension("iw.reconstruction.tab_compute_multires_coeffs_sparse",
                         ["iw/reconstruction/tab_compute_multires_coeffs_sparse.pyx",
                          "iw/multiresolution/struct_multires_Lbarre.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         ),
               Extension("iw.reconstruction.tab_reconstruction_multires",
                         ["iw/reconstruction/tab_reconstruction_multires.pyx",
                          "iw/multiresolution/struct_multires_Lbarre.pyx", ],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         include_path=PATH_INCLUDES,
                         extra_compile_args=EXTRA_COMPIL_ARGS,

                         ),
               Extension("iw.intertwining_wavelet",
                         ["iw/intertwining_wavelet.pyx",
                          "iw/graph_c.pyx",
                          "iw/multiresolution/struct_multires_Lbarre.pyx",
                          "iw/reconstruction/tab_reconstruction_multires.pyx",
                          "iw/reconstruction/tab_compute_multires_coeffs_sparse.pyx", "iw/kernel_c/cuore.c", "iw/kernel_c/lodge.c",
                          "iw/kernel_c/rforest_internal.c"],
                         include_dirs=PATH_INCLUDES,
                         library_dirs=PATH_LIBRARIES,
                         libraries=LINK_LIBRARIES,
                         include_path=PATH_INCLUDES,
                         extra_compile_args=EXTRA_COMPIL_ARGS,
                         ), ]


####################
# Setup method
####################
def setup_package():
    """ Setup function"""
    # set version
    VERSION = get_version()
    iw_dir = 'iw'
    set_version(iw_dir, VERSION)
    setup(
         name="IntertwiningWavelet",
         version=VERSION,
         description="IntertwiningWavelet : Pyramidal algorithms for wavelet decomposition on Graphs",
         long_description=(read('README.rst') + '\n\n' +
                            read('HISTORY.rst') + '\n\n' +
                            read('AUTHORS.rst')),
         author="Labex Archimede AMU",
         author_email="dominique.benielli@univ-amu.fr",
         license='new BSD',
         packages=['iw', 'iw.test', 'iw.function_fab',
                   'iw.diaconis_fill', 'iw.multiresolution',
                   'iw.reconstruction'],
         package_dir={'iw': 'iw',
                      'iw.function_fab': 'iw/function_fab',
                      'iw.diaconis_fill': 'iw/diaconis_fill',
                      'iw.multiresolution': 'iw/multiresolution',
                      'iw.reconstruction': 'iw/reconstruction',
                      },
         package_data={'iw': ['*.pxd'], 'iw.function_fab': ['*.pxd'],
                       'iw.diaconis_fill': ['*.pxd'], 'iw.multiresolution': ['*.pxd'],
                       'iw.reconstruction': ['*.pxd'], },
         ext_modules=ext_modules,
         install_requires=['numpy>=1.8', 'scipy>=0.16'],
         test_suite='nose.collector',
         tests_require=['nose', 'coverage'],
         define_macros=[('CYTHON_TRACE', '1'), ('CYTHON_TRACE_NOGIL', '1')],
         compiler_directives={'embedsignature': True, 'linetrace': True,
                              'binding': True, 'profile': True, },
         cmdclass={'build_ext': build_ext, 'clean': clean, 'sdist': m_sdist},
         classifiers=['Development Status :: 5 - Production/Stable',
                       'Intended Audience :: Science/Research',
                       'Intended Audience :: Developers',
                       'Natural Language :: English',
                       'License :: OSI Approved :: BSD License',
                      'Operating System :: MacOS :: MacOS X',
                       'Operating System :: POSIX :: Linux', 
                       'Programming Language :: Python :: 3.6',
                       'Topic :: Scientific/Engineering',
                       'Topic :: Scientific/Engineering :: Mathematics'
                       ],
    )


if __name__ == "__main__":
    setup_package()
