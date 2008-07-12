<?php

/* update-dilbert by Scott Wallace
 * A PHP script to help you update your collection of Dilbert strips.
 * Requires fetch-dilbert.  See bottom for more info.
 *
 * Changes:
 * 2008-07-12:
 *  - Uses dilbert.com/fast to find the strip URL; less bandwidth used
 *  - fetchStrip() changes modification time on DL'd strips to match the strip's
 *    date to help sorting by modification time
 * 2008-06-30:
 *  - No configuration needed
 *  - Run update-dilbert --help for NEW instructions
 *  - Windows exe that does not require PHP to be installed
 *  - Requires GD module
 *  - Can be run without fetch-dilbert
 *  - Runs on Windows
 * 2008-06-27:
 *  - Added error handling
 *  - Other minor changes
 * 2008-06-24:
 *  - Initial public release
 */

ini_set("error_reporting", "E_WARNING");

// The meat of the script
$script		= (isset($argv[0]) && $argv[0] != "") ? basename($argv[0]) : "update-dilbert";
$options	= parseArguments($argv);
$path		= ($options['input'][1]) ? $options['input'][1] : ".";
$windows	= (strtolower(substr(php_uname('s'), 0, 3)) == "win") ? true : false;
#$execCmd = ($windows === true) ? "php.exe -f {$config['fetchDilbertPath']}" : $config['fetchDilbertPath'];

if ($options['verbose'] || $options['v']) $option = 'verbose';
elseif ($options['help'] || $options['h']) $option = 'help';

if ($option == 'help') printHelp();
elseif ($option == 'verbose') $update = updateDilbertCollection(true);
else $update = updateDilbertCollection();

if ($update !== true) exit(1);

// From <http://www.php.net/manual/en/function.scandir.php>, but modified
// scandir(str $dir) for PHP4
// Used in PHP5 also b/c bamcompile (Windows) doesn't like function_exists()
function listDir($dir) {
 $dh = opendir($dir);
 while (false !== ($filename = readdir($dh))) {
  $files[] = $filename;
 }
 closedir($dh);
 sort($files);
 return $files;
}
function updateDilbertCollection($verbose = false) {
 global $path, $script, $windows;
 $currentYearPath = $path."/".date("Y");
 if (is_dir($currentYearPath) === false) {
  if (mkdir($currentYearPath)) {
   if ($verbose) echo "Created directory $currentYearPath.\n";
  }
  else return false;
 }
 $directoryListArray = listDir($currentYearPath);
 $directoryListArrayClean = array();
 foreach ($directoryListArray as $d) {
  if ($d !== "." && $d !== "..")
   $directoryListArrayClean[] = str_replace(".png", '', $d);
 }
 $yearToDate = generateYearToDateArray("Y-m-d");
 $neededDates = array();
 foreach ($yearToDate as $d) {
  if (!in_array($d, $directoryListArrayClean))
   $neededDates[] = $d;
 }
 sort($neededDates);
 if ($verbose) {
  $numberNeeded = count($neededDates);
  if ($numberNeeded == 0) echo "You're up to date!\n";
  if ($numberNeeded == 1) echo "Need to fetch one strip.\n";
  if ($numberNeeded > 1) echo "Need to fetch ".count($neededDates)." strips.\n";
 }
 $numberFailed = 0;
 foreach ($neededDates as $d) {
  if ($verbose) echo "Fetching strip for $d... ";
  if (!fetchStrip($d, $currentYearPath)) {
   if ($verbose) echo "failed!\n";
   else echo "$script:  error while downloading strip for $d\n";
   $numberFailed++;
  }
  else if ($verbose) echo "done!\n";
 }
 if ($verbose && $numberNeeded > 0 && $numberFailed == 0) {
  echo "You're up to date now!\n"; return true;
 }
 if ($numberFailed == 1) echo "There was a problem while downloading one strip.\n";
 if ($numberFailed > 1) echo "There were problems while downloading $numberFailed strips.\n";
 return false;
}

function generateYearToDateArray($format) {
 $today = date("z", mktime());
 $daysInYear = $today + 1;
 $array = array();
 while ($daysInYear > 0) {
  $array[] = date($format, mktime(0, 0, 0, 1, $daysInYear, date("Y")));
  $daysInYear--;
 }
 sort($array);
 return $array;
}

function fetchStrip($theDate, $foutputPath) {
 $fdate = trim($theDate);
 if (!$html = file_get_contents("http://www.dilbert.com/fast/$fdate/")) return false;
 $pieces = explode("<img src=\"/dyn/str_strip/0", $html);
 $pieces2 = explode(".strip.print.gif", $pieces[1]);
 $url = "http://www.dilbert.com/dyn/str_strip/0".$pieces2[0].".strip.gif";
 $file = "$foutputPath/$fdate.png";
 $strip = @imagecreatefromgif("$url");
 if (!$strip) return false;
 if (!imagepng($strip, $file)) return false; // saves $strip to $file with compression level 9
 if (!imagedestroy($strip)) return false;
 touch($file, strtotime($fdate)); // changes modtime on $file to the strip's date to help sorting by modtime (ignored on Winblows)
 return true; 
}

function parseArguments($arguments) {
 # from http://tinyurl.com/5e2qkp, but modified
 # parses arguments Unix-style
 $args = array();
 foreach ($arguments as $arg) {
  if (preg_match('#^-{1,2}([a-zA-Z0-9]*)=?(.*)$#', $arg, $matches)) {
   $key = $matches[1];
   switch ($matches[2]) {
    case '':
     case 'true':
      $arg = true;
      break;
     case 'false':
      $arg = false;
      break;
     default:
      $arg = $matches[2];
   }
   /* make unix like -afd == -a -f -d */
   if(preg_match("/^-([a-zA-Z0-9]+)/", $matches[0], $match)) {
    $string = $match[1];
    for($i=0; strlen($string) > $i; $i++) {
     $args[$string[$i]] = true;
    }
   }
   else
    $args[$key] = $arg;
  }
  else
   $args['input'][] = $arg;
 }
 return $args;
}

function printHelp() {
 global $script;
 /* HELP/INSTRUCTIONS: */
 echo <<<EOF
update-dilbert by Scott Wallace
A script to help you update your collection of Dilbert strips.

Prerequisites:  PHP command line interface (4 or 5; 5 recommended) and PHP GD 
module
You can install these on Ubuntu with:
 $ sudo apt-get install php5-cli php5-gd
You do not need to install the prerequisites if you are using the Windows EXE
file (update-dilbert.exe).

Usage:  $script [--help | -h] [-v | --verbose] [collectionPath]

-h or --help will show this message and exit.  -v or --verbose will have the
script tell you what it's doing.  Without either option, the script will run
quietly (i.e. no output).

collectionPath is the folder where you keep your Dilberts in.  It should have
one folder for each year of Dilberts you have downloaded.  If you do not
specify this, it defaults to the current directory.

Known issues:
 - update-dilbert only supports the following directory structure:
   <collectionPath>/<year>
 - It violates Dilbert.com's terms of service even more than fetch-dilbert
   itself does.  This will not be fixed (obviously).

All strips are downloaded directly from dilbert.com.

NOTE:  This script has been tested on PHP 5 on Ubuntu Linux 8.04 and PHP 5 on
Windows.  This script MUST be run from the command line.

WARNING:  This script is an automated script that will scrape various pages
from dilbert.com.  This is a violation of their terms of use.  Your use of
this script is at your own risk.  By using this script, you agree to not hold
Scott Wallace liable for any action taken against you due to your use of this
script.\n
EOF;
 exit;
}

?>