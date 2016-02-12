<?php
$db = new SQLite3('../db/data.sqlite');
$result = $db -> query('select * from data WHERE id=0;');

while ($row = $result -> fetchArray()) {
    $mode = $row["mode"];
    $brightness = $row["brightness"];
    $r = $row["r"];
    $g = $row["g"];
    $b = $row["b"];
    $parameter = $row["parameter"];
}
$rgb = array( $r, $g, $b );
$hex = rgb2hex($rgb);
$db->close();
?>