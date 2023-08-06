#!/usr/bin/env python

import os
import sys
import json

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist

import pyct.build


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    try:
        from param import version
    except:
        version = None
    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: param>=1.6.0 unavailable. If you are installing a package, this warning can safely be ignored. If you are creating a package or otherwise operating in a git repository, you should install param>=1.6.0.")
        return json.load(open(version_file_path, 'r'))['version_string']

def _build_models():
    try:
        from panel.compiler import build_custom_models
        print("Building custom models:")
        build_custom_models()
    except ImportError as e:
        print("Custom model compilation failed with: %s" % e)


class CustomDevelopCommand(develop):
    """Custom installation for development mode."""

    def run(self):
        _build_models()
        develop.run(self)

class CustomInstallCommand(install):
    """Custom installation for install mode."""

    def run(self):
        _build_models()
        install.run(self)

class CustomSdistCommand(sdist):
    """Custom installation for sdist mode."""

    def run(self):
        _build_models()
        sdist.run(self)

_COMMANDS = {
    'develop': CustomDevelopCommand,
    'install': CustomInstallCommand,
    'sdist':   CustomSdistCommand,
}

try:
    from wheel.bdist_wheel import bdist_wheel

    class CustomBdistWheelCommand(bdist_wheel):
        """Custom bdist_wheel command to force cancelling qiskit-terra wheel
        creation."""

        def run(self):
            """Do nothing so the command intentionally fails."""
            _build_models()
            bdist_wheel.run(self)

    _COMMANDS['bdist_wheel'] = CustomBdistWheelCommand
except:
    pass

########## dependencies ##########

install_requires = [
    'bokeh >=1.3.0',
    'param >=1.9.0',
    'pyviz_comms >=0.7.2',
    'markdown',
    'pyct >=0.4.4'
]

_recommended = [
    'notebook >=5.4',
    'holoviews >=1.12.0',
    'matplotlib',
    'pillow',
    'plotly'
]

extras_require = {
    'tests': [
        'coveralls',
        'nose',
        'flake8',
        'parameterized',
        'pytest',
        'scipy',
        'nbsmoke >=0.2.0',
        'pytest-cov ==2.5.1',
        'codecov',
        # For Panes.ipynb
        'hvplot',
        'plotly',
        'altair',
        'vega_datasets',
        'vtk ==8.1.1',
        'scikit-learn',
        'datashader'
    ],
    'recommended': _recommended,
    'doc': _recommended + [
        'nbsite >=0.6.1',
        'sphinx_ioam_theme',
        'sphinx <2',
        'selenium',
        'phantomjs',
        'lxml'
    ]
}

extras_require['all'] = sorted(set(sum(extras_require.values(), [])))

# until pyproject.toml/equivalent is widely supported (setup_requires
# doesn't work well with pip)
extras_require['build'] = [
    'param >=1.9.0',
    'pyct >=0.4.4',
    'setuptools >=30.3.0',
    'bokeh >=1.1.0',
    'pyviz_comms >=0.6.0',
    'nodejs >=9.11.1',
]

setup_args = dict(
    name='panel',
    version=get_setup_version("panel"),
    description='A high level dashboarding library for python visualization libraries.',
    long_description=open('README.md').read() if os.path.isfile('README.md') else 'Consult README.md',
    long_description_content_type="text/markdown",
    author="PyViz developers",
    author_email="developers@pyviz.org",
    maintainer="PyViz",
    maintainer_email="developers@pyviz.org",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    url='http://pyviz.org',
    cmdclass=_COMMANDS,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"],
    python_requires=">=2.7",
    entry_points={
        'console_scripts': [
            'panel = panel.cli:main'
        ]},
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['tests']
)

if __name__ == "__main__":

    example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'panel', 'examples')

    if 'develop' not in sys.argv and 'egg_info' not in sys.argv:
        pyct.build.examples(example_path, __file__, force=True)

    setup(**setup_args)
