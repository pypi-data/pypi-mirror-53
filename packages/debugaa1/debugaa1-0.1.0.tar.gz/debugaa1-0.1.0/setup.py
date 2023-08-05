from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name="debugaa1",
  version="0.1.0",
  license="gpl-3.0",
  description="debugaa1",
  long_description=long_description,
  long_description_content_type="text/markdown",
  author="Alex Anggada",
  packages=find_packages(),
  classifiers=[
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
