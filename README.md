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

If you installed dilbert-tools with pip or if you are using the Windows
EXEs, then you do not need to install anything else.  Otherwise, you must
also install the following:

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

Syntax:  `fetch-dilbert [-h|--help] [-v|--verbose] [-o|--output|--output-dir <path>] <date/year> [...]`

A date or range of dates must be given on the command line as positional
arguments in one of the following formats:

 * `today`  
   Download today's strip.
 * YYYY-MM-DD  
   Download the strip from the given day.
 * YYYY  
   Download the strip from the given year.

Date/year arguments may be separated with spaces, commas, or both, and
extraneous spaces and commas will be ignored.

The `-o/--output/--output-dir` argument is optional, and it is the folder where
you want the strip(s) to be saved.  It defaults to saving in the current
directory.

The old `-d/--date`, `--dates`, and `-y/--year` arguments are deprecated, and
they may be removed at a later date.  You should transition to using the new
positional arguments if you are still using the old ones.


### Examples

 * `fetch-dilbert today 2008-06-23 1992`  
   Downloads today's strip, the one from June 23, 2008, and all strips from the
   year 1992 and saves them to the current working directory.
 * `fetch-dilbert 2008-04-15 -o Comics/Dilbert/2008`  
   Downloads the strip from April 15, 2008, and saves it to the folder
   `Comics/Dilbert/2008` within the current directory.
 * `fetch-dilbert 1997 -vo Comics/Dilbert/1997`  
   Downloads the strips from the year 1997, outputs progress messages to
   standard error, and saves them to the folder `Comics/Dilbert/1997` within
   the current directory.


`update-dilbert`
----------------

This script helps you maintain a collection of Dilbert strips.  It will
download all strips that have been published during the current year that
you don't already have.  Run daily after midnight Pacific time for best
results.


### Usage

Syntax:  `update-dilbert [-h|--help] [-v|--verbose] [-p|--path <path>] [-m|--metadata-only]`

Run `update-dilbert -p <path>`, where `<path>` is where you keep your Dilbert
strips, and it will do the dirty work for you.  If the `-p` argument is omitted,
it will use the current directory.  `<path>` should contain directories whose
names are year numbers.  Year subdirectories will be created if necessary.


Building dilbert-tools
----------------------

To build dilbert-tools, run `make` from the root of the repository in a
Unix-like environment with the below dependencies installed.

To make the distribution zip files, run `make dist`.  The Windows zip
file will be created only if EXE files for both scripts exist in
`dist/<version-number>`.


### Build dependencies

* Unix-like environment (e.g. Linux, Cygwin, Windows Subsystem for Linux, O$ X, ...)
* GNU make
* zip
* setuptools


### Making Windows EXEs

The official EXEs are created using `make exes`, which uses [`ezpyi`][ezpyi],
which is a wrapper for [PyInstaller][PyInstaller].  Except in Cygwin and MSYS,
`make exes` uses [Wine][Wine] via [this `ezpyi-wine` script][ezpyi-wine].

[ezpyi]: https://code.s.zeid.me/bin/blob/master/ezpyi
[PyInstaller]: http://www.pyinstaller.org/
[Wine]: https://www.winehq.org/
[ezpyi-wine]: https://code.s.zeid.me/bin/blob/master/ezpyi-wine

Note:  Windows Subsystem for Linux cannot be used to build Windows EXEs until
Microsoft add support for 32-bit ELF executables.  If that happens, then use
the steps for `ezpyi-wine` on Unix-like platforms.

On Unix-like platforms (except Cygwin and MSYS):

1. Install Wine.

2. [Download `ezpyi-wine`][ezpyi-wine], and preferably put it somewhere on
   your `$PATH`.

3. Set up the environment and install the runtime dependencies into it:  
   `ezpyi-wine : pip -U install beautifulsoup4 lxml Pillow PyYAML requests`

4. Run `make exes`, or if necessary, `make exes EZPYI_WINE=<path to ezpyi-wine>`.


On Cygwin or MSYS:

1. [Download `ezpyi`][ezpyi], and preferably put it somewhere on your
   Windows `%PATH%`.

2. Outside of Cygwin/MSYS, install [PyInstaller][PyInstaller] and the runtime
   dependencies.

3. Run `make exes`, or if necessary, `make exes EZPYI=<path to ezpyi>`.
