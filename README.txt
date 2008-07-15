Dilbert Tools by Scott Wallace
Version r25
http://code.google.com/p/dilbert-tools
Readme File

Unix/Linux/OSX (*nix) Archive Contents:
 fetch-dilbert - *nix script
 update-dilbert - *nix script
 README.txt - this file
 CHANGES.txt - changelog
 LICENSE.txt - GNU General Public License, v2
Windows Archive Contents:
 fetch-dilbert.py - Windows script
 update-dilbert.py - Windows script
 fetch-dilbert.exe - Windows EXE
 update-dilbert.exe - Windows EXE
 README.txt - this file
 CHANGES.txt - changelog
 LICENSE.txt - GNU General Public License, v2

How do I use them?
Once you've extracted the scripts (see next question), see
<http://code.google.com/p/dilbert-tools/>, or run fetch-dilbert --help
or update-dilbert --help for usage instructions.  You need to be in a command
prompt (Windows) (Start > Run > cmd.exe > OK) or a terminal (*nix) to run them.

Which files from the archive do I need?
On Unix/Linux/OSX/BSD/etc, you just need fetch-dilbert and update-dilbert.  Be
sure to make them executable (chmod +x <file> at the terminal) before you run
them.

On Windows, you just need fetch-dilbert.exe and update-dilbert.exe.  The EXEs
do not need Python or PIL to be installed.  Then run them like:
>fetch-dilbert ...

If you don't want to use these, you'll need the .py versions.  These need to
be run like:
>C:\Python25\python fetch-dilbert.py ...
where C:\Python25 is where you installed Python.

What else do I need?
If you're not using the Windows EXEs*, you need Python 2.5 and the Python
Imaging Module (PIL).
* If you want to MAKE the EXE files, you will need Python and PIL.  (See below.)

If you're on Ubuntu, you can install them using:
 $ sudo apt-get install python python-imaging
 
Windows users who don't want to use the EXEs can download a ZIP file containing
both of these from the project home page.  Then, extract both files, run
the Python installer and THEN run the PIL installer.

Can I modify them?
Yes.  First, check out the latest sources from the SVN repository.  See
<http://code.google.com/p/dilbert-tools/source/checkout> for instructions.
Then, just be sure to modify the files in the src/ directory if you want to
make changes.  common.inc.py has common functions used by both scripts.  When
you're done, run the build script to create the scripts that you actually run.

To build on *nix, run:
$ ./build.py

On Windows, run this to make the EXEs:
>C:\Python25\python build.py
where C:\Python25 is where you installed Python,
and this to make the .py's:
>C:\Python25\python build.py -n

The resulting files will be put in unix/ for Unix/Linux builds, and windows/
for Windows builds.  If you want them somewhere else, use the -o PATH option.

DISCLAIMER:
These scripts are automated scripts that will scrape various pages from
dilbert.com.  This is a violation of their terms of use.  Your use of these
scripts is at your own risk.  By using these scripts, you agree to not hold
Scott Wallace (me) liable for any action taken against you due to your use of
these scripts.
