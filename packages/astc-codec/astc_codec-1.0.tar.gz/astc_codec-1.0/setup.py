import os
from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None


def all_c(folder, exclude=[]):
    return [
        os.path.join(root, file)
        for root, dirs, files in os.walk(folder)
        for file in files
        if file.endswith('.cc') and exclude not in os.path.join(root, file)
    ]


extensions = [
    Extension(
        name="astc_codec",
        sources=[
            "astc_codec.pyx",
            *all_c('astc-codec', '\\test'),
        ],
        language="c++",
        include_dirs=[
            "astc-codec"
        ],
        install_requires=[
            "cython"
        ],
    )
]
if cythonize:
    extensions = cythonize(extensions)

setup(ext_modules=extensions)
