import sys, os

from setuptools import find_packages, setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        # Import each Hy module to ensure it's compiled.
        import os, importlib
        for dirpath, _, filenames in sorted(os.walk("hy")):
            for filename in sorted(filenames):
                if filename.endswith(".hy"):
                    importlib.import_module(
                        dirpath.replace("/", ".").replace("\\", ".") +
                        "." + filename[:-len(".hy")])
        install.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
  name = "debugaahy",
  version = "0.1.1",
  license = "gpl-3.0",
  description = "debugaahy",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "Alex Anggada",
  packages = find_packages(include=["debugaahy", "debugaahy.*"]),
  package_data = {"debugaahy": ["printingMethods.hy"]},
  install_requires = ["hy"],
  classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Operating System :: OS Independent",
    "Topic :: Database",
  ],
)
