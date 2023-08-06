#!/usr/bin/env python
# coding: utf-8

import io
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# the name of the project
name = 'nbsphinx-link'

version_ns = {}
with io.open(os.path.join(here, 'nbsphinx_link', '_version.py'), encoding="utf8") as f:
    exec(f.read(), {}, version_ns)


setup_args = dict(
    name            = name,
    description     = "A sphinx extension for including notebook files outside sphinx source root",
    version         = version_ns['__version__'],
    packages        = find_packages(here),
    author          = 'Vidar Tonaas Fauske',
    author_email    = 'vidartf@gmail.com',
    url             = 'https://github.com/vidartf/nbsphinx-link',
    license         = 'BSD-3',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Interactive', 'Interpreter', 'Shell', 'Web'],
    classifiers     = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires = [
        'nbsphinx',
        'sphinx>=1.8',
    ],
    entry_points = {
    }
)


if __name__ == '__main__':
    setup(**setup_args)
