<?php
	include("main.php");
?>

<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>
<title>Spa</title>
<link rel="stylesheet" type="text/css" href="include/css.css">
<script src="include/js.js"></script>
<script src="include/jscolor.js"></script>
</head>

<body>
<div class="boxer">
	<div class="box-row">
		<div onclick="location.href='.?a=0';" class="box" style="background-color:red;border-top-left-radius: 50px;">Red</div>
		<div onclick="location.href='.?a=1';" class="box" style="background-color:green;">Green</div>
		<div onclick="location.href='.?a=2';" class="box" style="background-color:blue;;border-top-right-radius: 50px;">Blue</div>

	</div>
	<div class="box-row">
		
		<div onclick="location.href='.?a=3';" class="box" style="background-color:cyan;">Cyan</div>
		<div onclick="location.href='.?a=4';" class="box" style="background-color:magenta;">Magenta</div>
		<div onclick="location.href='.?a=5';" class="box" style="background-color:yellow;">Yellow</div>
	</div>
	<div class="box-row">
		
		<div onclick="location.href='.?a=6';" class="box" style="background-color:white;">White</div>
		<div class="box" id="rect" style="background-color:<?php echo $hex;?>;"><form action="." method="get"><input readonly class="jscolor {onFineChange:'update(this)'}" name="rgb" value="<?php echo substr($hex, 1);?>" onchange="this.form.submit()"><input type="hidden" name="a" value="7"></form></div>
		<div onclick="location.href='.?a=8';" class="box" style="background:repeating-radial-gradient( circle, #7FF591, #7FF591 10px, #B5F7B2 10px, #B5F7B2 20px);">Rainbow</div>
	</div>
	<div class="box-row">
		<div onclick="location.href='.?a=9';" class="box" style="background:repeating-radial-gradient( circle, #F57FDF, #F57FDF 10px, #F7B2C6 10px, #F7B2C6 20px);">Random</div>
		<div onclick="location.href='.';" class="box" style="background-color:#EB97EB;">Refresh</div>
		<div class="box" style="background-color:white;"></div>
	</div>
	<div class="box-row">
		<div onclick="location.href='.?c=0';" class="box" style="background-color:#ccffb3;">-</div>
		<div onclick="location.href='.?c=2';" class="box" style="background-color:#aaff80;">Parameter (<?php echo $parameter;?>)</div>
		<div onclick="location.href='.?c=1';" class="box" style="background-color: #ccffb3">+</div>
	</div>
	<div class="box-row">
		<div onclick="location.href='.?b=0';" class="box" style="background-color:#E1EEF2;border-bottom-left-radius: 50px;">-</div>
		<div onclick="location.href='.?b=2';" class="box" style="background-color:#ACAFB0;"><?php echo $brightness."% (".$mode_name.")";?></div>
		<div onclick="location.href='.?b=1';" class="box" style="background-color:#E1EEF2;border-bottom-right-radius: 50px;">+</div>
	</div>
</div>
</body>
</html>