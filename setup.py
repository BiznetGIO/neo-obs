"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from obs import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

with open(join(this_dir, 'requirements.txt'), encoding='utf-8') as fp:
    install_requires = fp.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['pytest', '--cov=obs', '-vv'])
        raise SystemExit(errno)


setup(
    name='neo-obs',
    version=__version__,
    description='A OBS command line tools',
    long_description=long_description,
    url='https://github.com/BiznetGIO',
    author='BiznetGio',
    author_email='support@biznetgio.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers', 'Topic :: Utilities',
        'License :: Public Domain', 'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='cli',
    include_package_data=True,
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires,
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov', 'pytest-ordering',
                 'testfixtures'],
    },
    entry_points={
        'console_scripts': [
            'obs=obs.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
