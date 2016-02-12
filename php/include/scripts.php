<?php
function hex2rgb($hex) {
   $hex = str_replace("#", "", $hex);

   if(strlen($hex) == 3) {
      $r = hexdec(substr($hex,0,1).substr($hex,0,1));
      $g = hexdec(substr($hex,1,1).substr($hex,1,1));
      $b = hexdec(substr($hex,2,1).substr($hex,2,1));
   } else {
      $r = hexdec(substr($hex,0,2));
      $g = hexdec(substr($hex,2,2));
      $b = hexdec(substr($hex,4,2));
   }
   $rgb = array($r, $g, $b);
   //return implode(",", $rgb); // returns the rgb values separated by commas
   return $rgb; // returns an array with the rgb values
}

function rgb2hex($rgb) {
   $hex = "#";
   $hex .= str_pad(dechex($rgb[0]), 2, "0", STR_PAD_LEFT);
   $hex .= str_pad(dechex($rgb[1]), 2, "0", STR_PAD_LEFT);
   $hex .= str_pad(dechex($rgb[2]), 2, "0", STR_PAD_LEFT);

   return $hex; // returns the hex value including the number sign (#)
}
function spaStatus($mode) {
	if ($mode == 0) {
		$mode_name = "Red";
	} elseif ($mode == 1) {
		$mode_name = "Green";
	} elseif ($mode == 2) {
		$mode_name = "Blue";
	} elseif ($mode == 3) {
		$mode_name = "Cyan";
	} elseif ($mode == 4) {
		$mode_name = "Magenta";
	} elseif ($mode == 5) {
		$mode_name = "Yellow";
	} elseif ($mode == 6) {
		$mode_name = "White";
	} elseif ($mode == 7) {
		$mode_name = "Set";
	} elseif ($mode == 8) {
		$mode_name = "Rainbow";
	} elseif ($mode == 9) {
		$mode_name = "Random";
	} else {
		$mode_name = "Undef";
	}
	return $mode_name;
}
?>