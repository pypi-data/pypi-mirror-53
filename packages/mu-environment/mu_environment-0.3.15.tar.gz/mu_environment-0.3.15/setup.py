# @file setup.py
# This contains setup info for mu_environment pip module
#
##
# Copyright (c) 2018, Microsoft Corporation
#
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##

import setuptools
from setuptools.command.sdist import sdist
from setuptools.command.install import install
from setuptools.command.develop import develop
from MuEnvironment.bin.NuGet import DownloadNuget

with open("README.rst", "r") as fh:
    long_description = fh.read()


class PostSdistCommand(sdist):
    """Post-sdist."""
    def run(self):
        # we need to download nuget so throw the exception if we don't get it
        DownloadNuget()
        sdist.run(self)


class PostInstallCommand(install):
    """Post-install."""
    def run(self):
        try:
            DownloadNuget()
        except:
            pass
        install.run(self)


class PostDevCommand(develop):
    """Post-develop."""
    def run(self):
        try:
            DownloadNuget()
        except:
            pass
        develop.run(self)


setuptools.setup(
    name="mu_environment",
    author="Project Mu Team",
    author_email="maknutse@microsoft.com",
    description="Project Mu distributed dependency management, build, test, and tool environments.",
    long_description=long_description,
    url="https://github.com/microsoft/mu_pip_environment",
    license='BSD2',
    packages=setuptools.find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    cmdclass={
        'sdist': PostSdistCommand,
        'install': PostInstallCommand,
        'develop': PostDevCommand,
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['omnicache=MuEnvironment.Omnicache:main', 'nuget-publish=MuEnvironment.NugetPublishing:go']
    },
    install_requires=[
        'pyyaml',
        'mu_python_library>=0.4.6'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ]
)
