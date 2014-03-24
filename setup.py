from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext


# http://stackoverflow.com/a/21621689/2691632
class build_ext(_build_ext):

    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

# Use Cython now
from Cython.Build import cythonize
cy_ext = cythonize("./cyassimp.pyx", force=True)


setup(name='cyassimp',
      version='0.1',
      description='Fast Cython bindings for The Open Assimp Import Library',
      author='James Booth',
      author_email='james.booth08@imperial.ac.uk',
      ext_modules=cy_ext,
      packages=find_packages(),
      cmdclass={'build_ext': build_ext},
      setup_requires=['numpy>=1.8.0',
                      'cython>=0.18.0'],
      install_requires=['numpy>=1.8.0',
                        'cython>=0.18.0']
      )
