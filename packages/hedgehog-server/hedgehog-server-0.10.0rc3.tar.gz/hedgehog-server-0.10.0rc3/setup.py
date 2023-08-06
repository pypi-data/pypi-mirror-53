"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# this will load the __version__ variable
exec(open("hedgehog/server/_version.py", encoding="utf-8").read())

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hedgehog-server',
    version=__version__,
    description='Hedgehog Robot Controller Server',
    long_description=long_description,
    url="https://github.com/PRIArobotics/HedgehogServer",
    author="Clemens Koza",
    author_email="koza@pria.at",
    license="AGPLv3+",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
    ],

    keywords='hedgehog robotics controller server',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['concurrent-utils ~=0.2.0', 'hedgehog-protocol ~=0.10.0rc2',
                      'hedgehog-utils[protobuf,zmq,trio] ~=0.7.0rc1', 'hedgehog-platform ~=0.2.0'],

    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        # TODO adding extras for existing requirement does not work
        'dev': ['pytest', 'pytest-runner', 'pytest-asyncio', 'pytest-trio', 'pytest-cov', 'pytest-timeout', 'mypy'],
        #'raspberry': ['hedgehog-platform[raspberry] ~=0.2.0'],
        'raspberry': ['RPi.GPIO', 'pyserial-asyncio'],
    },

    package_data={
        'hedgehog': ['server/vision/haarcascade_frontalface_alt.xml'],
    },

    entry_points={
        'console_scripts': [
            'hedgehog-server = hedgehog.server.server:main',
            'hedgehog-simulator = hedgehog.server.simulator:main',
        ],
    },
)
