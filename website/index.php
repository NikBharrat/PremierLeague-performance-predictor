<?php
	include_once "connection.php";
	session_start();
?>

<!DOCTYPE html>

<html>
<head>
	<title>Player Performance Predictor</title>
	<h1>Premier League Player Performance Predictor</h1>
	<link rel="stylesheet" type="text/css" href="homepagestyle.css">
</head>

<body>
	<div class = "team">
		<label>Select Team: </label> 
		<select name="team" onchange="getId(this.value);">
			<option value = "">Select Team</option>

			<?php
				$query = "SELECT DISTINCT(Team) AS Team FROM outfield ORDER BY Team ASC;";
				$results = mysqli_query($con, $query);

				foreach ($results as $team) {
				?>
			<option value = "<?php echo $team['Team']; ?>"><?php echo $team['Team'] ?></option>
			<?php
				}
			?>
		</select>	
	</div>	
</br>


</br>
	<div class="players">
		<label>Select a Player: </label>
		<select name="player" id="playerList" onchange="showUser(this.value)">
			<option value="">Select a player</option>
		</select>

	</div>

<script src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
	<script>
		function getId(value){
			$.ajax({
				type: "POST",
				url: "getdata.php",
				data: "Team="+value,
				success: function(data){
					$("#playerList").html(data);			
				}
			});
		}
	</script>

</br>

	<div id = "textbox">Select a team and player</div>
		<script>
		function showUser(value){
			$.ajax({
				type: "POST",
				url: "displayPlayer.php",
				data: "Player="+$("#playerList option:selected").text(),
				success: function(data){
					$("#textbox").html(data);			
				}
			});
		}
	</script>
</body>

</html>