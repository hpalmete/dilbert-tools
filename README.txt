Dilbert Tools by Scott Wallace
Revision 11
http://code.google.com/p/dilbert-tools

Unix Archive Contents:
 fetch-dilbert - *nix script
 update-dilbert - *nix script
 README.txt - this file
Windows Archive Contents:
 fetch-dilbert.php - Windows script
 update-dilbert.php - Windows script
 fetch-dilbert.exe - Windows EXE
 update-dilbert.exe - Windows EXE
 README.txt - this file

How do I use them?
Once you've extracted the scripts (see next question), see
<http://www.scott-wallace.net/dilbert-tools>, or run fetch-dilbert --help
or update-dilbert --help for usage instructions.

Which files do I need?
On Unix/Linux/OSX/BSD/etc, you just need fetch-dilbert and update-dilbert.
On Windows, you just need fetch-dilbert.exe and update-dilbert.exe.  These do
not need PHP to be installed.  If you want to run these on Windows using the
PHP interpreter, use the .php's instead.see
<http://www.scott-wallace.net/dilbert-tools>

What are the prerequisites?
Unless you're using the EXEs, you need PHP (command line interface and its GD
module.  Both PHP 4 and 5 will work, but I recommend PHP 5.  If you're on
Ubuntu, you can install them using:
 $ sudo apt-get install php5-cli php5-gd
Windows users can download the installer from <php.net>.  Be sure to select the
GD module during setup.
If you're on a Unix-based system, be sure to run chmod +x fetch-dilbert and
chmod +x update-dilbert before you run them.

Can I modify them?
Yes.  First, check out the latest sources from the SVN repository.  See
<http://code.google.com/p/dilbert-tools/source/checkout> for instructions.
Then, just be sure to modify the files in the src/ directory if you want to
make changes.  fetch-strip.inc.php has the function that fetches and converts
the strips.  When you're done, run php -f build to create the scripts that you
actually run.  If you're on Windows, that command will also create the EXE
files.  To make the Windows scripts on non-Windows systems, run:
 $ php -f build -- --windows
That command will not make the EXEs, though.
The resulting files will be put in unix/ for Unix/Linux builds, and windows/
for Windows builds.

DISCLAIMER:
These scripts are automated scripts that will scrape various pages from
dilbert.com.  This is a violation of their terms of use.  Your use of these
scripts is at your own risk.  By using these scripts, you agree to not hold
Scott Wallace (me) liable for any action taken against you due to your use of
these scripts.
