#!/usr/bin/env python3
from setuptools import setup
import sensors

setup(
    name='PySensors',
    version=sensors.__version__,
    author=sensors.__author__,
    author_email=sensors.__contact__,
    packages=['sensors'],
    # scripts=[],
    url='http://pypi.python.org/pypi/PySensors/',
    # download_url='',
    license=sensors.__license__,
    description='Python bindings to libsensors (via ctypes)',
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    keywords=['sensors', 'hardware', 'monitoring'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved ::'
        ' GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
    ],
    python_requires=">=3.6",
)
