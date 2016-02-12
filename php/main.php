<?php
include 'include/scripts.php';
include 'include/GetData.php';

if (isset($_GET['a'])) {
    $a = intval($_GET['a']);
    $db = new SQLite3('../db/data.sqlite');
    if ($a >= 0 && $a <= 9) {
        $a_stripped = $a;
    } else {
        $a_stripped = 0;
    }
    if ($a_stripped == 7) {
        if (isset($_GET['rgb'])) {
            $rgb = hex2rgb($_GET['rgb']);
            $red_stripped = intval($rgb[0]) % 256;
            $green_stripped = intval($rgb[1]) % 256;
            $blue_stripped = intval($rgb[2]) % 256;
            $sql = 'UPDATE data SET mode='.$a_stripped.
            ', r='.$red_stripped.
            ', g='.$green_stripped.
            ', b='.$blue_stripped.
            ' WHERE id=0;';
            $result = $db -> exec($sql);
        }
    } else {
        $sql = 'UPDATE data SET mode='.$a_stripped.
        ' WHERE id=0;';
        $result = $db -> exec($sql);
    }
    if ($brightness == 0) {
        $sql = 'UPDATE data SET brightness=100 WHERE id=0;';
        $result = $db -> exec($sql);
    }
    if (!$result) {
        echo "DB Error, could not update the database";
        echo 'MySQL Error: '.mysql_error();
        exit;
    }
    $db -> close();
}
elseif(isset($_GET['b'])) {

    $b_stripped = intval($_GET['b']);
    $db = new SQLite3('../db/data.sqlite');

    if ($b_stripped >= 0 && $b_stripped <= 2) {
        if ($b_stripped == 0 && $brightness - 25 < 0) {
            $new_bright = 0;
        }
        if ($b_stripped == 1 && $brightness + 25 > 100) {
            $new_bright = 100;
        }
        if ($b_stripped == 0 && $brightness - 25 >= 0) {
            $new_bright = $brightness - 25;
        }
        if ($b_stripped == 1 && $brightness + 25 <= 100) {
            $new_bright = $brightness + 25;
        }
        if ($b_stripped == 2 && $brightness > 0) {
            $new_bright = 0;
        }
        if ($b_stripped == 2 && $brightness == 0) {
            $new_bright = 100;
        }
    } else {
        $new_bright = $brightness;
    }
    $sql = 'UPDATE data SET brightness='.$new_bright.
    ' WHERE id=0;';
    $result = $db -> exec($sql);

    if (!$result) {
        echo "DB Error, could not update the databasen";
        echo 'MySQL Error: '.mysql_error();
        exit;
    }
    $db -> close();
}
elseif(isset($_GET['c'])) {

    $c_stripped = intval($_GET['c']);
    $db = new SQLite3('../db/data.sqlite');

    if ($c_stripped >= 0 && $c_stripped <= 2) {
        if ($c_stripped == 0 && ($parameter - 1) > 0) {
            $new_parameter = $parameter - 1;
        } else if ($c_stripped == 1) {
            $new_parameter = $parameter + 1;
        } else if ($c_stripped == 2) {
            $new_parameter = 2;
        } else {
            $new_parameter = $parameter;
        }
    }
    $sql = 'UPDATE data SET parameter='.$new_parameter.
    ' WHERE id=0;';
    $result = $db -> exec($sql);

    if (!$result) {
        echo "DB Error, could not query the databasen";
        echo 'MySQL Error: '.mysql_error();
        exit;
    }
	$db -> close();
}

include 'include/GetData.php';
$mode_name = spaStatus($mode);
?>