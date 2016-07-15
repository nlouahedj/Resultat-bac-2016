<?php


$db = new PDO('sqlite:data.db');

$filter = "";

if(isset($_GET["matricule"]) && $_GET["matricule"]){
	$filter .= "matricule LIKE '%".$_GET["matricule"]."%' ";
}

if(isset($_GET["f_name"]) && $_GET["f_name"]){
	$filter .= $filter != ""? ", ": "";
	$filter .= "f_name LIKE \'%".$_GET["f_name"]."%\' ";
}
if(isset($_GET["l_name"]) && $_GET["l_name"]){
	$filter .= $filter != ""? ", ": "";
	$filter .= "l_name LIKE '%".$_GET["l_name"]."%' ";
}
if(isset($_GET["birth_date"]) && $_GET["birth_date"]){
	$filter .= $filter != ""? ", ": "";
	$filter .= "birth_date LIKE '%".$_GET["birth_date"]."%' ";
}
if(isset($_GET["birth_place"]) && $_GET["birth_place"]){
	$filter .= $filter != ""? ", ": "";
	$filter .= "birth_place LIKE '%".$_GET["birth_place"]."%' ";
}
if(isset($_GET["field"]) && $_GET["field"]){
	$filter .= $filter != ""? ", ": "";
	$filter .= "field LIKE '%".$_GET["field"]."%' ";
}
if(isset($_GET["grade"]) && $_GET["grade"]){
	$filter .= $filter != ""? ", ": "";
	$filter .= "grade LIKE '%".$_GET["grade"]."%' ";
}

$query_string = "SELECT * FROM grades ";
$query_string .= $filter != ""? "WHERE ".$filter : "";
$result = $db->query($query_string);
if(isset($_GET["json"])){

	$arr = array();
	foreach($result as $r){
		$arr[$r['matricule']] = array(
						"f_name" => $r["f_name"],
						"l_name" => $r["l_name"],
						"field" => $r["field"],
						"birth_date" => $r["birth_date"],
						"birth_place" => $r["birth_place"],
						"grade" => $r["grade"],
						);
	}
	echo json_encode($arr, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}
else{ //not json
?>
<!DOCTYPE html>
<html>
<head>
<title>BAC 016</title>
<link href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css" rel="stylesheet">
</head>
<body>
<table id="grades" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>ID</th>
                <th>First name</th>
                <th>Last name</th>
                <th>Birth date</th>
                <th>Birth place</th>
                <th>field</th>
                <th>grade</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
                <th>ID</th>
                <th>First name</th>
                <th>Last name</th>
                <th>Birth date</th>
                <th>Birth place</th>
                <th>field</th>
                <th>grade</th>
            </tr>
        </tfoot>
        <tbody>
        <? foreach($result as $r){ ?>
            <tr>
                <td><? echo $r['matricule'];?></td>
                <td><? echo $r['f_name'];?></td>
                <td><? echo $r['l_name'];?></td>
                <td><? echo $r['birth_date'];?></td>
                <td><? echo $r['birth_place'];?></td>
                <td><? echo $r['field'];?></td>
                <td><? echo $r['grade'];?></td>
            </tr>
        <? } ?>
        </tbody>
</table>
<a href="index.php">Home</a>

<script src="https://code.jquery.com/jquery-1.12.3.min.js"></script>
<script src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>
<script>
$(document).ready(function() {
    $('#grades').DataTable();
} );
</script>

</body>
</html>
<?
} // end else
?>