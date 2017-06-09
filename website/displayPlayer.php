<!DOCTYPE html>
<html>
<head>
<style>
table {
    width: 100%;
    border-collapse: collapse;
}

table, td, th {
    border: 1px solid black;
    padding: 5px;
}

th {text-align: left;}
</style>
</head>
<body>

<?php
session_start();
$con = mysqli_connect('localhost','root', 'password5', 'performance');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"ajax_demo");
$player = $_POST['Player'];
$splitselectedtext = explode(',', $player);
$surname = $splitselectedtext[0];

$sql="SELECT * FROM outfield WHERE Surname = '$surname'";
$outfieldresults = mysqli_query($con,$sql);
$sql2="SELECT * FROM goalkeeper WHERE Surname = '$surname'";
$goakeeperresults = mysqli_query($con,$sql2);

while($row = mysqli_fetch_array($outfieldresults)) {
    if($row['Position']!='Goalie'){
    echo "<br>" ."Name: " . $row['Forename'] . " " . $row['Surname'] ."<br>".
            "Position: " . $row['Position'] . "<br>".
            "Games Played: " . $row['Games Played'] . "<br>" .
            "Games Started: " . $row['Games Started'] . "<br>" .
            "Minutes Played: " . $row['Minutes Played'] . "<br>" .
            "Goals: " . $row['Goals'] . "<br>" .
            "Assists: " . $row['Assists'] . "<br>".
            "Shots: " . $row['Shots'] . "<br>" .
            "Shots On Target: " . $row['Shots on goal'] . "<br>" .
            "Yellow Cards: " . $row['Yellow cards'] . "<br>" .
            "Red Cards: " . $row['Red cards'] . "<br>" . "<br>" . 
            "<strong>Next Fixture: </strong>" . $row['Next opposition'] . "<br>".
            "<strong>Next Fixture Date: </strong>" . explode('/', $row["Next fixture date"])[1] . "/" . explode('/', $row["Next fixture date"])[0] . "/2017" . "<br>".
            "<strong>Social Media Score (From -10 to 10): </strong>" . $row['Social Media Score'] . "<br>" .
            "<strong>Chance of Scoring: </strong>" . $row['Chance of scoring'] . "%" . "<br>" .
            "<strong>Chance of Assisting:</strong> " . $row['Chance of assisting'] . "%" . "<br>" .
            "<strong>Chance of being carded: </strong>" . $row['Chance of being carded'] . "%" . "<br>";
        } else {
            while($row2 = mysqli_fetch_array($goakeeperresults)) {
            echo "<br>" ."Name: " . $row2['Forename'] . " " . $row2['Surname'] ."<br>".
            "Position: " . $row2['Position'] . "<br>".
            "Games Played: " . $row2['Games Played'] . "<br>" .
            "Games Started: " . $row2['Games Started'] . "<br>" .
            "Minutes Played: " . $row2['Minutes Played'] . "<br>" .
            "Goals Conceded: " . $row2['Goals Conceded'] . "<br>" .
            "Shots faced on target: " . $row2['Shots on target faced'] . "<br>" .
            "Saves: " . $row2['Saves'] . "<br>" .
            "Yellow Cards: " . $row2['Yellow Cards'] . "<br>" .
            "Red Cards: " . $row2['Red Cards'] . "<br>" . "<br>" . 
            "<strong>Next Fixture: </strong>" . $row2['Next opposition'] . "<br>".
            "<strong>Next Fixture Date: </strong>" .explode('/', $row2["Next fixture date"])[1] . "/" . explode('/', $row2["Next fixture date"])[0] . "/2017" . "<br>".
            "<strong>Social Media Score (From -10 to 10): </strong>" . $row2['Social Media Score'] . "<br>" .
            "<strong>Chance of clean sheet: </strong>" . $row2['Chance of clean sheet']. "%" . "<br>";

        }
    }
}
mysqli_close($con);
?>
</body>
</html>