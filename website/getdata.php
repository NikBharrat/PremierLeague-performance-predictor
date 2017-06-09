<?php
	include_once "connection.php";

if(!empty($_POST['Team'])){
	$team = $_POST['Team'];
	$query = "SELECT * FROM outfield WHERE Team = '$team'";
	$results = mysqli_query($con, $query);

	foreach ($results as $player) {
	?>
	<option value = "<?php echo $player['Team']; ?>"><?php echo $player['Surname'].", ". $player['Position']?></option>
	<?php
	}
}
?>
