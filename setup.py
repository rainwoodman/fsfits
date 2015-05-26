from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy

def myext(*args):
    return Extension(*args, include_dirs=["./", numpy.get_include()],
            extra_compile_args=['-std=c99'] )
extensions = [
        myext("fsfits.bitshuffle.ext", ["fsfits/bitshuffle/ext.pyx", 
                "fsfits/bitshuffle/bitshuffle.c", 
                "fsfits/bitshuffle/lz4.c", 
                ]
                
        ),
        ]
setup(
    name="fsfits", version="0.1",
    author="Yu Feng",
    description="fsfits",
    package_dir = {'fsfits': 'fsfits'},
    install_requires=['cython', 'numpy'],
    packages= ['fsfits'],
    requires=['numpy'],
    ext_modules = cythonize(extensions)

)

