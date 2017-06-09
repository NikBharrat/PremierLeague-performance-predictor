<?php
	//Connect To Database
	$con = mysqli_connect('localhost','root', 'password5', 'performance');

	if(mysqli_connect_errno()){
		echo "Failed to connect".mysqli_connect_errno();
	}


?>
