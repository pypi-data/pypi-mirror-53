#!/usr/bin/env python
"""Setup config for IPMIDB-APIs."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()

setup(
    name='ipmidb-tools',
    version='19.10.1-2',
    description="Toolset for IPMI interactions at CERN Data Center",
    author="Luca Gardi",
    author_email="luca.gardi@cern.ch",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/hw/ipmidb-tools",
    license='GPL',
    package_dir={'': 'src'},
    scripts=['bin/ipmi-grabber', 'bin/ipmiadm'],
    packages=['pyipmidb']
)
