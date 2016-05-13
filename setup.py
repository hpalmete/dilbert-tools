#!/usr/bin/env python2

# This file is public domain via CC0:
# <https://creativecommons.org/publicdomain/zero/1.0/>

from setuptools import setup, find_packages

setup(
 name="dilberttools",
 version="0.20160500",
 description="Download Dilbert strips and maintain a private Dilbert collection.",
 url="https://code.s.zeid.me/dilbert-tools",
 author="Scott Zeid",
 author_email="support+dilbert-tools@s.zeid.me",
 classifiers=[
  "Development Status :: 3 - Alpha",
  "Environment :: Console",
  "Intended Audience :: End Users/Desktop",
  "Natural Language :: English",
  "Programming Language :: Python :: 2",
  "Programming Language :: Python :: 2 :: Only",
  "Topic :: Software Development :: Libraries",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "Topic :: System :: Archiving :: Backup",
  "Topic :: Utilities",
 ],
 packages=find_packages(),
 install_requires=["Pillow"],
 entry_points={
  "console_scripts": [
   "fetch-dilbert=dilberttools.fetch:main",
   "update-dilbert=dilberttools.update:main",
  ]
 },
)
