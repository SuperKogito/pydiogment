# -*- coding: utf-8 -*-
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
path = pathlib.Path(__file__).parent

# get readme text
readme = (path / "README.md").read_text()
# define requirements
requires = ["numpy>=1.17.2", "scipy>=1.3.1"]

setup (
        name         = 'pydiogment',
        version      = '0.0.1',
        author       = 'SuperKogito, HMMalek',
        author_email = 'superkogito@gmail.com, hasna.m.malek@gmail.com',
        description  = 'Python audio augmentation',
        long_description = readme,
        long_description_content_type = "text/markdown",
        license      = 'BSD',
        url          = 'https://github.com/SuperKogito/pydiogment',
        packages     = find_packages(),
        classifiers  = [
                        'Development Status :: 3 - Alpha',
                        'Environment :: Console',
                        'Environment :: Web Environment',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: BSD License',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python',
                        'Topic :: Documentation',
                        'Topic :: Utilities',
                      ],
        platforms            = 'any',
        include_package_data = True,
        install_requires     = requires,
        python_requires      = '>=3.5',
     )
