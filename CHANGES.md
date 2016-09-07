* 2016-09-xx
    * Support the new dilbert.com redesign
    * Save YAML files for each strip containing the strip's date, title, tags,
      and transcript
    * In `fetch-dilbert`, dates and years to download are now given as
      positional arguments (this also allows downloading multiple years at
      once).  The old `-d/--date`, `--dates`, and `-y/--year` arguments are
      now deprecated and may be removed at a later date.
    * Try alternate sources if the strip's image cannot be found on dilbert.com.
    * Added `-v/--verbose` to fetch-dilbert
    * Now requires Python 2.7, BeautifulSoup 4, lxml, Pillow, PyYAML, and
      Requests.
    * Added a `-V/--version` argument to both scripts that prints the version
      number and exits
    * Technical details:
        * Errors are now handled properly:  tracebacks are printed to standard
          error and are raised/returned from the fetch_strip()/update_collection()
          functions (yay for being a better programmer now!)
        * Restructured into a Python package
        * The non-EXE executable script files are now ZIP files containing the
          code files.  They can still be executed just like regular Python scripts
          and still have shebang lines.
        * New build process (just run `make` from the root of the repository,
          and `make dist` to make the distribution files)
        * Windows EXEs can now be built with `make exes`, both on Windows and
          on Unix-like platforms such as Linux (via Wine).
        * Reorganized source tree
        * Binary blobs and PyInstaller are no longer kept in the Git repository
        * Now on GitLab

* 2012-10-10
    * Updated copyright notices
    * Updated README file and converted it to Markdown
    * Moved to Bitbucket

* 2009-02-22 (r29)
    * Fixed to not try downloading any Dilbert strips before 1989-04-16 (when
      the first one was published)
    * Fixed fetch-dilbert giving exit code 0 if there was a problem downloading
      a strip or strips using the --date/--dates argument
    * Both scripts now expand ~ (\*nix home directory) and environment variables
      in argument values

* 2008-07-15 (r25)
    * Rewritten in Python
    * Requires Python 2.5 and Python Imaging Library (PIL)
    * Specify output path for fetch- with --output=PATH option
    * --date, --year, --help, and --output have short options:  -d, -y, -h, and
      -o respectively in fetch
    * --file has been removed from fetch 
    * Specify collection path for update with --path=PATH option
    * --verbose, --help, and --path have short options:  -v, -h, and -p
      respectively in update
    * --help's output is very short now in both scripts

* 2008-07-12 (r20)
    * Uses dilbert.com/fast to find the strip URL; less bandwidth used
    * fetchStrip() changes modification time on DL'd strips to match the strip's
      date to help sorting by modification time
    * Since fetchStrip() touches strips now, and the update script used to do
      that, remove that from the update script 

* 2008-07-01 (r11)
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
