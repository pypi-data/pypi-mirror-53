import os
import sys
from setuptools import setup

script_dir = os.path.dirname(os.path.abspath(__file__))


def readme():
    with open(os.path.join(script_dir, 'README.rst')) as f:
        return f.read()


# exec the version file to get access to the __version__ variable
exec(open(os.path.join(script_dir, 'asmlib', 'Version.py')).read())

author = 'Mario Werner'
author_email = 'mario.werner@iaik.tugraz.at'
name = 'asmlib'

# make the sphinx command available if sphinx is installed
try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'sphinx': BuildDoc}
except ImportError:
    cmdclass = {}

setup(name=name,
      version=__version__,
      description=('Tooling package for the computer architecture course at '
                   'Graz University of Technology.'),
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Utilities',
      ],
      keywords='TOY assembler simulator computer architecture teaching',
      url='https://extgit.iaik.tugraz.at/con/asmlib',
      author=author,
      author_email=author_email,
      license='GPLv3',
      packages=["asmlib", "asmlib.Tools"],
      entry_points={
          'console_scripts': ['toyasm-ng.py=asmlib.Tools.toyasm:main',
                              'toysim-ng.py=asmlib.Tools.toysim:main',
                              'riscvasm.py=asmlib.Tools.riscvasm:main',
                              'riscvsim.py=asmlib.Tools.riscvsim:main',
                              ],
      },
      cmdclass=cmdclass,
      command_options={
          'sphinx': {
              'build_dir': ('setup.py', 'doc/_build'),
              'project': ('setup.py', name),
              'release': ('setup.py', __version__),
              'source_dir': ('setup.py', 'doc'),
              'version': ('setup.py', __version__)}},
      python_requires='>=3.5',
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'pytest-console-scripts'],
      extras_require={
          'documentation': ['sphinx', 'sphinx-autodoc-typehints'],
      },
      # include_package_data=True,
      zip_safe=False
      )
