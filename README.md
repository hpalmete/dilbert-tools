Dilbert Tools  
Copyright (c) 2008-2012 Scott Zeid  
[https://code.s.zeid.me/dilbert-tools](https://code.s.zeid.me/dilbert-tools)  

This consists of two Python command-line scripts:

`fetch-dilbert` downloads individual Dilbert comic strips

`update-dilbert` helps you maintain a private Dilbert collection

Both can be run on Python 2.5 on any supported platform, with the Python Imaging Library (PIL) module.  Windows EXE versions of the scripts are also available that do not require Python to be installed.

# Disclaimer
**These scripts are automated scripts that will scrape various pages from
  dilbert.com.  This is a violation of their terms of use.  Your use of
  these scripts is at your own risk.  By downloading or using these
  scripts, you agree to not hold me liable for any action taken against
  you due to your use or download of them.**

# Requirements

**If you're using the EXE version on Windows, you don't need to install
these.**  Otherwise, you'll need to install these if you haven't already:

 * Python 2.5 or 2.6 (not tested with 2.7 or 3.x)
 * Python Imaging Library (PIL)

You can install these on Ubuntu and other Debian-based distros with:

    $ sudo apt-get install python python-imaging

# `fetch-dilbert`

This script is capable of downloading Dilbert strips for a given day or
days, or a whole year at a time.

## Usage

Syntax:  `fetch-dilbert (options) [--output=|-o OUTPATH]`

The script takes two arguments.  One tells it which strip(s) to download,
and the other tells it where to put them.

The only required argument is one of the following:

 * `--date=DATE1[,DATE2[,...]]` or `--dates=DATE1[,DATE2[,...]]` or
   `-d DATE1[,DATE2[,...]]`
   Download one or more strips.  Each `DATE` can be either in YYYY-MM-DD
   format (e.g. 2008-06-24) or the word `today` (which tells it to
   download today's strip), and they are separated by commas.
 * `--year=YEAR` or `-y YEAR`
   Downloads all strips for the year `YEAR`.
 * `--help` or `-h`
   Shows a help message.

The other argument is optional, and it is the folder where you want the
strip(s) to be saved.

## Examples

 * `fetch-dilbert --dates=today,2008-06-23`
   Downloads today's strip and the one from June 23, 2008, and saves them
   to the current working directory.
 * `fetch-dilbert --date=2008-04-15 -o Comics/Dilbert/2008`
   Downloads the strip from April 15, 2008, and saves it to the folder
   `Comics/Dilbert/2008` within the current directory.
 * `fetch-dilbert --year=1997 -o Comics/Dilbert/1997`
   Downloads the strips from the year 1997 and saves them to the folder
   `Comics/Dilbert/1997` within the current directory.

## Changes
 * 2009-02-22 (r29)
   * Fixed to not try downloading any Dilbert strips before 1989-04-16
     (when the first one was published)
   * Fixed fetch-dilbert giving exit code 0 if there was a problem
     downloading a strip or strips using the --date/--dates argument
   * Now expands ~ (`*`nix home directory) and environment variables in
     argument values
 * 2008-07-15 (r25)
   * Rewritten in Python
   * Requires Python 2.5 and Python Imaging Library (PIL)
   * Specify output path for fetch- with --output=PATH option
   * --date, --year, --help, and --output have short options:  -d, -y, -h,
     and -o respectively in fetch
   * --file has been removed from fetch
   * --help's output is very short now in both scripts
 * 2008-07-12 (r20)
   * Uses dilbert.com/fast to find the strip URL; less bandwidth used
   * fetchStrip() changes modification time on DL'd strips to match the
     strip's date to help sorting by modification time
 * 2008-06-30
   * Uses PHP functions, rather than wget/other CLI tools, to
     download/proccess strips.
   * Works on Windows
   * Requires GD module
   * Windows exe that can be run without PHP
 * 2008-06-27
   * Added error handling
   * Options can be in any order now
   * `--date` and `--dates` mean the same thing now
   * Other minor changes
 * 2008-06-24
   * Initial public release

# `update-dilbert`

This script helps you maintain a collection of Dilbert strips.  It will
download all strips that have been published during the current year that
you don't already have.  Run daily after midnight Pacific time for best
results.

## Usage

Syntax:  `update-dilbert [--help | -h] [-v | --verbose] [-p |--path=(path to collection)]`

Run `update-dilbert -p (path to collection)` where `(path to collection)`
is where you keep your Dilberts and it will do the dirty work for you.
If you leave out `(path to collection)`, it will look in the current
directory.  `(path to collection)` should have one folder for each year
of Dilberts that you have (e.g. 1997, 1998, 1999, 2000, ...).

If you want it to tell you what it's doing, run
`update-dilbert -v (path to collection)`.  `update-dilbert -h` will show
a help message.

## Changes
 * 2009-02-22 (r29)
   * Fixed to not try downloading any Dilbert strips before 1989-04-16
     (when the first one was published)
   * Now expands ~ (`*`nix home directory) and environment variables in
     argument values
 * 2008-07-15 (r25)
   * Rewritten in Python
   * Requires Python 2.5 and Python Imaging Library (PIL)
   * Specify collection path for update with --path=PATH option
   * --verbose, --help, and --path have short options:  -v, -h, and -p
     respectively in update
   * --help's output is very short now in both scripts
 * 2008-07-12
   * Uses dilbert.com/fast to find the strip URL; less bandwidth used
   * fetchStrip() changes modification time on DL'd strips to match the
     strip's date to help sorting by modification time
   * Since fetchStrip() touches strips now, and the update script used to
     do that, remove that from the update script
 * 2008-07-01
   * Force error reporting to `E_WARNING` to prevent unnecessary messages.
 * 2008-06-30
   * No configuration needed
   * Windows exe that does not require PHP to be installed
   * Requires GD module
   * Can be run without fetch-dilbert
   * Runs on Windows
 * 2008-06-27
   * Added error handling
   * Other minor changes
 * 2008-06-24
   * Initial public release

# Archive contents
 * Unix/Linux/OSX (`*`nix)
    * fetch-dilbert - `*`nix script
    * update-dilbert - `*`nix script
    * README.txt - this file
    * CHANGES.txt - changelog
    * LICENSE.txt - GNU General Public License, v2
 * Windows
    * fetch-dilbert.py - Windows script
    * update-dilbert.py - Windows script
    * fetch-dilbert.exe - Windows EXE
    * update-dilbert.exe - Windows EXE
    * README.txt - this file
    * CHANGES.txt - changelog
    * LICENSE.txt - GNU General Public License, v2

## How do I use them?
Once you've extracted the scripts (see next question), see
<https://code.s.zeid.me/dilbert-tools>, or run `fetch-dilbert --help`
or `update-dilbert` --help for usage instructions.  You need to be in a
command prompt (Windows) (Start > Run > cmd.exe > OK) or a terminal
(`*`nix) to run them.

## Which files from the archive do I need?
On Unix/Linux/OSX/BSD/etc, you just need fetch-dilbert and update-dilbert.
Be sure to make them executable (`chmod +x <file>` at the terminal) before
you run them.

On Windows, you just need fetch-dilbert.exe and update-dilbert.exe.  The
EXEs do not need Python or PIL to be installed.  Then run them like:

    >fetch-dilbert ...

If you don't want to use these, you'll need the .py versions.  These need
to be run like:

    >C:\Python25\python fetch-dilbert.py ...

where C:\Python25 is where you installed Python.

## What else do I need?
If you're not using the Windows EXEs`*`, you need Python 2.5 and the
Python Imaging Module (PIL).

NOTE:  Python 3.x will not work.  Use Python 2.5 - 2.7 instead.

(`*` If you want to MAKE the EXE files, you will need Python and PIL.
(See below.))

If you're on Ubuntu, you can install them using:

    $ sudo apt-get install python python-imaging
 
Windows users who don't want to use the EXEs can download a ZIP file
containing both of these from the project home page.  Then, extract both
files, run the Python installer and THEN run the PIL installer.

## Can I modify them?
Yes.  First, clone the repository.  Then, just be sure to modify the files
in the `src/` directory if you want to make changes.  `common.inc.py` has
common functions used by both scripts.  When you're done, run the `build`
script to create the scripts that you actually run.

To build on `*`nix, run:

    $ ./build.py

On Windows, run this to make the EXEs:

    >C:\Python25\python build.py

where `C:\Python25` is where you installed Python, and this to make the
.py's:

    >C:\Python25\python build.py -n

The resulting files will be put in `unix/` for Unix/Linux builds, and
`windows/` for Windows builds.  If you want them somewhere else, use the
`-o PATH` option.
