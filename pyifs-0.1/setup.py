# Setup script for python module.

from distutils.core import setup

setup(name = "pyifs",
      author = "Glenn Hutchings",
      author_email = "zondo@pillock.freeserve.co.uk",
      description = "Iterated Function Systems.",
      version = "0.1",
      license = "GPL",
      package_dir = {"": "src"},
      py_modules = ["ifs"])
