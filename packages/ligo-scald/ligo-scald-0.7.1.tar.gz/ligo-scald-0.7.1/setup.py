import os
from setuptools import setup

install_requires = [
    'bottle >= 0.12',
    'h5py >= 2.3',
    'ligo-common >= 1.0',
    'numpy >= 1.7',
    'PyYAML >= 3.10',
    'urllib3 >= 1.10',
    'python-dateutil',
]

setup(
    name = 'ligo-scald',
    description = 'SCalable Analytics for Ligo Data',
    version = '0.7.1',
    author = 'Patrick Godwin',
    author_email = 'patrick.godwin@ligo.org',
    url = 'https://git.ligo.org/gstlal-visualisation/ligo-scald.git',
    license = 'GPLv2+',

    packages = ['ligo', 'ligo.scald', 'ligo.scald.io', 'static', 'templates'],
    namespace_packages = ['ligo'],

    package_data = {
        'static': ['*'],
        'templates': ['*'],
    },

    entry_points = {
        'console_scripts': [
            'scald = ligo.scald.__main__:main',
        ],
    },

    install_requires = install_requires,

    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    ],

)
