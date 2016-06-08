Dilbert Tools  
=============

Copyright (c) 2008-2016 Scott Zeid  
[https://code.s.zeid.me/dilbert-tools](https://code.s.zeid.me/dilbert-tools)  

Download Dilbert strips and maintain a private Dilbert collection.

- - - -

dilbert-tools consists of two Python command-line scripts:

* `fetch-dilbert` downloads individual Dilbert comic strips and their
  metadata.
* `update-dilbert` helps you maintain a private Dilbert collection.


Disclaimer
----------

**These scripts are automated scripts that will scrape various pages from
  dilbert.com.  This is a violation of their terms of use.  Your use of
  these scripts is at your own risk.  By downloading or using these
  scripts, you agree to not hold me liable for any action taken against
  you due to your use or download of them.**


Installation
------------

dilbert-tools requires Python 2.7 unless you are using the Windows EXEs.

To install dilbert-tools, you have several options:

* Extract `fetch-dilbert` and `update-dilbert` (or the EXE versions if on
  Windows) from the appropriate zip file for your platform.  If you are
  not on Windows, make sure `fetch-dilbert` and `update-dilbert` are
  executable.
* Download the `dilberttools-<version>.tar.gz` archive and run
  `pip install <archive>`.
* From the root of the repository, run `./setup.py install` or `pip install .`.


### Requirements

If you are not installing dilbert-tools with pip or using the Windows EXEs,
then you must also install the following:

* BeautifulSoup 4
* lxml
* Pillow
* PyYAML
* Requests

To install the requirements on Fedora:

    sudo dnf install python python-lxml python-pillow PyYAML python-requests python-pip
    sudo pip install -U beautifulsoup4

To install the requirements on Ubuntu and other Debian-based distros:

    sudo apt-get install python python-lxml python-pillow python-yaml python-pip
    sudo pip install -U beautifulsoup4 requests

To install the requirements on other platforms, with Python 2.7 and pip
already installed:

    pip install -U beautifulsoup4 lxml Pillow PyYAML requests


`fetch-dilbert`
---------------

This script downloads Dilbert strips for a given day or days, or a whole
year at a time.  It will also save the strips' titles, tags, and transcripts
to YAML files.

Each YAML file will be named `YYYY-MM-DD.yml` and will have the keys `date`,
`title`, `tags`, and `transcript`.  If there is no title or transcript for the
strip, then the respective key's value will be null.

If a strip has to be downloaded from a source other than
[dilbert.com](http://dilbert.com/), then its YAML file will also have a key
called `alternate-source` containing the URL of either the page that was used
or the image URL itself.  A warning will also be printed to standard error for
each alternate source tried.


### Usage

Syntax:  `fetch-dilbert [options] [--output-dir|-o <path>]`

The script takes two arguments.  One tells it which strip(s) to download,
and the other tells it where to put them.

A date or range of dates must be given on the command line using one of the
following arguments:

 * `--date=DATE1[,DATE2[,...]]` or `--dates=DATE1[,DATE2[,...]]` or
   `-d DATE1[,DATE2[,...]]`
   Download one or more strips.  Each `DATE` can be either in YYYY-MM-DD
   format (e.g. 2008-06-24) or the word `today` (which tells it to
   download today's strip).
 * `--year=YEAR` or `-y YEAR`
   Downloads all strips for the year `YEAR`.

The other argument is optional, and it is the folder where you want the
strip(s) to be saved.


### Examples

 * `fetch-dilbert --dates=today,2008-06-23`
   Downloads today's strip and the one from June 23, 2008, and saves them
   to the current working directory.
 * `fetch-dilbert --date=2008-04-15 -o Comics/Dilbert/2008`
   Downloads the strip from April 15, 2008, and saves it to the folder
   `Comics/Dilbert/2008` within the current directory.
 * `fetch-dilbert --year=1997 -o Comics/Dilbert/1997`
   Downloads the strips from the year 1997 and saves them to the folder
   `Comics/Dilbert/1997` within the current directory.


`update-dilbert`
----------------

This script helps you maintain a collection of Dilbert strips.  It will
download all strips that have been published during the current year that
you don't already have.  Run daily after midnight Pacific time for best
results.


### Usage

Syntax:  `update-dilbert [--help|-h] [-v|--verbose] [-p|--path <path>] [-m|--metadata-only]`

Run `update-dilbert -p <path>`, where `<path>` is where you keep your Dilbert
strips, and it will do the dirty work for you.  If the `-p` argument is omitted,
it will use the current directory.  `<path>` should contain directories whose
names are year numbers.  Year subdirectories will be created if necessary.


Building dilbert-tools
----------------------

To build dilbert-tools, run `make` from the root of the repository in a
Unix-like environment with the below dependencies installed.

To make the distribution zip files, run `make dist`.  Windows EXE files must be
created manually, and the Windows zip file will be created only if EXE files
for both scripts exist in `dist/<version-number>`.  The official EXEs are
created with [PyInstaller][PyInstaller] and [this `ezpyi` script][ezpyi] on
a Windows XP virtual machine, but similar freezing utilities are fine as well.

[PyInstaller]: http://www.pyinstaller.org/
[ezpyi]: https://code.s.zeid.me/bin/blob/master/ezpyi


### Build dependencies

* Unix-like environment (e.g. Linux, Cygwin, Windows Subsystem for Linux, O$ X, ...)
* GNU make
* zip
* setuptools
