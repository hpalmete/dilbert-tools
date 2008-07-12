<?php

/* fetch-dilbert by Scott Wallace
 * A PHP script to download Dilbert strips from a given date or dates, and
 * convert them to PNG format using ImageMagick's convert command.
 * See bottom for more info.
 *
 * Changes:
 * 2008-07-12:
 *  - Uses dilbert.com/fast to find the strip URL; less bandwidth used
 *  - Changes modification time on DL'd strips to match the strip's date to
 *    help sorting by modification time
 * 2008-06-30:
 *  - Uses PHP functions, rather than wget/other CLI tools, to download/proccess
 *    strips.
 *  - Works on Windows
 *  - Requires GD module
 *  - Windows exe that can be run without PHP
 * 2008-06-27:
 *  - Added error handling
 *  - Options can be in any order now
 *  - --date and --dates mean the same thing now
 *  - Other minor changes
 * 2008-06-24:
 *  - Initial public release
 */

ini_set("error_reporting", "E_WARNING");

$options	= parseArguments($argv);
$script		= (isset($options['input'][0])) ? basename($options['input'][0]) : 'fetch-dilbert';
$outputPath	= (isset($options['input'][1])) ? $options['input'][1] : '.';
$errorMessage	= "$script:  error downloading the strip for ";

$modes = array('file','year','date','dates','help');
foreach ($modes as $m) {
 if ($options[$m]) $mode = array($m, $options[$m]);
}

if ($mode) {
 if ($mode[0] == 'file') {
  $file = $mode[1];
  if ($file === true) noStrip();
  if (file_exists($file)) {
   if (!$dates = @file("$file"))
    error("There was a problem opening the file $file.\n");
   foreach ($dates as $idate) {
    if (trim($idate) == "today") $jdate = date("Y-m-d");
    else $jdate = trim($idate);
    if (fetchStrip($jdate, $outputPath) !== true) error("$errorMessage$jdate.\n");
   }
  }
  else error("The file $file does not exist.\n");
 }
 elseif ($mode[0] == 'year') {
  $year = $mode[1];
  $dates = generateYearArray($year, "Y-m-d");
  foreach ($dates as $idate) {
   if (fetchStrip($idate, $outputPath) !== true)
    error("$errorMessage$idate.\n");
  }
 }
 elseif ($mode[0] == 'date' || $mode[0] == 'dates') {
  $dates = explode(",", $mode[1]);
  foreach ($dates as $idate) {
   if ($idate == "today")
    $jdate = date("Y-m-d");
   else
    $jdate = $idate;
   if (fetchStrip($jdate, $outputPath) !== true)
    error("$errorMessage$jdate.\n");
  }
 }
 elseif ($mode[0] == 'help')
  printHelp();
}
else noStrip();

function error($msg, $status = 1) {
 echo $msg; exit($status);
}
function noStrip() {
 global $script;
 echo "Usage: $script (--date|--dates)=date1[,date2[,...]]|--year=YEAR|\n--file=FILE|--help [outputPath]\n";
 echo "For help on using this script, run:\n";
 echo "$script --help\n";
 exit(1);
}
/*INCLUDE:src/fetch-strip.inc.php*/
function generateYearArray($fyear, $format) {
 $feb = cal_days_in_month(CAL_GREGORIAN, 2, $fyear);
 $daysInYear = ($feb === 29) ? 366 : 365;
 $array = array();
 while ($daysInYear > 0) {
  $array[] = date($format, mktime(0, 0, 0, 1, $daysInYear, $fyear));
  $daysInYear--;
 }
 sort($array);
 return $array;
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
fetch-dilbert by Scott Wallace
A PHP script to download Dilbert strips from a given date or dates, and
convert them to PNG format using the PHP GD module.

Prerequisites:  PHP command line interface (4 or 5; 5 recommended) and PHP GD 
module
You can install these on Ubuntu with:
 $ sudo apt-get install php5-cli php5-gd
You do not need to install the prerequisites if you are using the Windows EXE
file (fetch-dilbert.exe).

Usage:  $script (--date|--dates)=date1[,date2[,...]]|--year=YEAR|
--file=FILE|--help [outputPath]

You can specify the date(s) to download in several ways:
(Note:  the options --date and --dates mean the same thing)
- $ fetch-dilbert --date=DATE or
  $ fetch-dilbert --dates=DATE
  will download the strip from the date DATE (in YYYY-MM-DD format).  If DATE
  is "today" (no quotes), it will download the strip from the current date.
  Example:  $ fetch-dilbert --date=2008-06-01
  will download the strip from 2008-06-01
- $ fetch-dilbert --date=date1[,date2[,...]] or
  $ fetch-dilbert --dates=date1[,date2[,...]]
  will download the strips from the specified dates, separated by commas
  Example:  $ fetch-dilbert --dates=2007-04-13,2008-06-12,today
  will download the strips from 2007-04-13, 2008-06-12, and the current date
- $ fetch-dilbert --year=YEAR
  will download all strips from the year YEAR
- $ fetch-dilbert --file=FILE
  will download all strips specified in the file FILE.  FILE should have each
  desired date written in YYYY-MM-DD format, or the word today, one per line.
  Example:  $ fetch-dilbert --file=dates.txt
  If dates.txt contains:
   2008-01-01
   2008-05-25
   today
  the strips from 2008-01-01, 2008-05-25, and the current date will be
  downloaded.

$ fetch-dilbert --help
will show this message.

Unless you specify the optional paramater outputPath, strips will be saved
to the current directory.  Set the outputPath to the directory you want to
download the desired strip(s) to if you want them saved somewhere else.
outputPath can be relative or absolute.
Example:  $ fetch-dilbert --date=today ~/Comics/Dilbert/2008
will download today's strip to the directory ~/Comics/Dilbert/2008.

All strips are downloaded directly from dilbert.com.

NOTE:  This script has been tested on PHP 5 on Ubuntu Linux 8.04 and PHP 5 on
Windows.  This script MUST be run from the command line.

WARNING:  This script is an automated script that will scrape various pages
from dilbert.com.  This is a violation of their terms of use.  Your use of
this script is at your own risk.  By using this script, you agree to not hold
Scott Wallace liable for any action taken against you due to your use of this
script.\n
EOF;
exit();
}

?>
