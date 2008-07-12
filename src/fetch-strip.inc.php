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
