# flake8: noqa

# This file is part of modelbase.
#
# modelbase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# modelbase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with modelbase.  If not, see <http://www.gnu.org/licenses/>.


import pathlib
from setuptools import setup, Extension
from setuptools.command import build_ext


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


ext_modules = [
    Extension(
        "modelbase.pde.utils._perffuncs",
        ["modelbase/pde/utils/perffuncs.cpp"],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
        ],
        library_dirs=["modelbase/pde/utils/"],
        language="c++",
    )
]

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="modelbase",
    version="0.4.1",
    description="A package to build metabolic models",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ebenhoeh/modelbase",
    author="Oliver Ebenhoeh",
    author_email="oliver.ebenhoeh@hhu.de",
    license="GPL3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="modelling ode pde metabolic",
    project_urls={
        "Documentation": "https://modelbase.readthedocs.io/en/latest/",
        "Source": "https://gitlab.com/ebenhoeh/modelbase",
        "Tracker": "https://gitlab.com/ebenhoeh/modelbase/issues",
    },
    packages=["modelbase"],
    install_requires=[
        "numpy>=1.16",
        "scipy",
        "matplotlib>=3.0.3",
        "pandas",
        "pybind11>=2.3",
        "python-libsbml",
        "black",
        "pre-commit",
    ],
    setup_requires=["pybind11>=2.3"],
    python_requires=">3.5.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext.build_ext},
    zip_safe=False,
)
