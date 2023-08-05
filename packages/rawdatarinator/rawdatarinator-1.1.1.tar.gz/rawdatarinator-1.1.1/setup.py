'''Setup.py
'''

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    '''Subclass build_ext to bootstrap numpy.'''
    def finalize_options(self):
        _build_ext.finalize_options(self)

        # Prevent numpy from thinking it's still in its setup process
        import numpy as np
        self.include_dirs.append(np.get_include())

extensions = [
    Extension(
        'rawdatarinator.twixread',
        [
            "bart/src/misc/version.c",
            "bart/src/num/vecops.c",
            "bart/src/num/simplex.c",
            "bart/src/num/optimize.c",
            "bart/src/num/multind.c",
            "bart/src/misc/ya_getopt.c",
            "bart/src/misc/opts.c",
            "bart/src/misc/misc.c",
            "bart/src/misc/io.c",
            "bart/src/misc/mmio.c",
            "bart/src/misc/debug.c",
            "bart/src/twixread.c",
            # "src/twixread_pyx.pyx"
            "src/twixread_pyx.c"
        ],
        include_dirs=['src/', 'bart/src/'],
        extra_compile_args=['-O3']#, '-ffast-math']
    ),
    Extension(
        'rawdatarinator.read',
        # ['src/readcfl.pyx'],
        ['src/readcfl.c'],
        include_dirs=[]),
    Extension(
        'rawdatarinator.write',
        # ['src/writecfl.pyx'],
        ['src/writecfl.c'],
        include_dirs=[]),
]

setup(
    name='rawdatarinator',
    version='1.1.1',
    author='Nicholas McKibben',
    author_email='nicholas.bgp@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/mckib2/rawdatarinator',
    license='GPL',
    description='Read Siemens raw data.',
    long_description=open('README.rst').read(),
    install_requires=[
        "numpy>=1.17.2",
    ],
    cmdclass={'build_ext': build_ext},
    setup_requires=['numpy'],
    python_requires='>=3.5',

    # And now for Cython generated files...
    ext_modules=extensions
)
