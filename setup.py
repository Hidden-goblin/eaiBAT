# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("readme.md", "r") as file:
    long_description = file.read()

setup(
    name="eaibat",
    version="0.0.9",
    description="Basic classes to ease BDD evidence creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hidden-goblin/eaiBAT.git",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'behave',
        'requests',
        'python-docx',
        'unidecode'
    ],
    python_requires='>=3.7, !=2.*',
    packages=find_packages(),
    include_package_data=True,
    # package_dir={'': 'eaiBat'},
    author="Eric Aïvayan",
    author_email="eric.aivayan@free.fr"
)
