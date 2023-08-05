#!/usr/bin/env python

# setuptools is required
from setuptools import setup

with open('README.md') as fp:
    description = fp.read()

setup(
    # The package
    name="pandeia.engine",
    version="1.5",
    packages=["pandeia",
              "pandeia.engine",
              "pandeia.engine.defaults",
              "pandeia.engine.helpers",
              "pandeia.engine.helpers.schema"],
    # For PyPI
    description='Pandeia 3D Exposure Time Calculator compute engine',
    long_description=description,
    author='Adric Riedel, Klaus Pontoppidan, Craig Jones, Tim Pickering',
    #author_email='jwsthelp.stsci.edu',
    url='https://jwst.etc.stsci.edu',
    classifiers=["Intended Audience :: Science/Research",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Topic :: Scientific/Engineering :: Astronomy",
                 "Topic :: Software Development :: Libraries :: Python Modules"],
    # Other notes
    package_data={"pandeia.engine.defaults": ["*.json"]},
    install_requires=[
        "numpy>=1.13.3",
        "scipy",
        "astropy>=2",
        "photutils",
        "pysynphot"
    ],
    zip_safe=False
)
