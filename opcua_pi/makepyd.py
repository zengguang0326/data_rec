# cython: language_level=3
from distutils.core import setup
from Cython.Build import cythonize
# setup(
#     name = 'Hello world',
#     ext_modules = cythonize("makeLicese.py"),
# )

setup(
    name = 'Hello world',
    ext_modules = cythonize("server_all.py"),
)



