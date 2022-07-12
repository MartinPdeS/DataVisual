#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import os
import sys
import numpy
import pathlib
import subprocess
import pkg_resources

from shutil                       import rmtree
from setuptools                   import setup, find_packages, Command




# Package meta-data.
NAME            = 'DataVisual'
DESCRIPTION     = 'A package multidimensional data visualisation.'
URL             = 'https://github.com/MartinPdeS/DataVisual'
EMAIL           = 'Martin.poinsinet.de.sivry@gmail.com'
AUTHOR          = 'Martin Poinsinet de Sivry',
REQUIRES_PYTHON = '>3.8.0'



__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'Version'), "r+") as f:
    Version = f.read().rstrip("\n").split(".")
    Major, Mid, Minor = int(Version[0]), int(Version[1]), int(Version[2])

if '--NewMajor' in sys.argv:
    Major += 1
    sys.argv.remove('--NewMajor')
if '--NewMid' in sys.argv:
    Mid += 1
    sys.argv.remove('--NewMidr')
if '--NewMinor' in sys.argv:
    Minor += 1
    sys.argv.remove('--NewMinor')

Version = f'{Major}.{Mid}.{Minor}'

print(f"DataVisual Version: {Version}")

with open(os.path.join(__location__, 'Version'), "w+") as f:
    f.writelines(Version)



requirementPath = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(requirementPath,'r') as requirements_txt:
    REQUIRED = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]


EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))


macro = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]

ext_modules = []


try:
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


about = {}
if not Version:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = Version


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name                          = NAME,
    version                       = about['__version__'],
    description                   = DESCRIPTION,
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    author                        = AUTHOR,
    author_email                  = EMAIL,
    setup_requires                = ['numpy', 'matplotlib'],
    python_requires               = '>=3.6',#REQUIRES_PYTHON,
    url                           = URL,
    packages                      = find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires              = REQUIRED,
    extras_require                = EXTRAS,
    dependency_links              = [],
    include_package_data          = True,
    ext_modules                   = ext_modules,
    license                       = 'MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ],
    # $ setup.py publish support.
    cmdclass={'upload': UploadCommand}, #'build_ext': build_ext
)
