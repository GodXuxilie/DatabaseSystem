<?php
$dbhost = 'localhost';
$dbuser = 'root';
$dbpass = '';
$conn = mysqli_connect($dbhost, $dbuser, $dbpass);
if(! $conn )
{
    die('Could not connect: ' . mysqli_error());
}
echo "数据库连接成功!<br>";

$file=fopen("ratings.dat","r");
while(!feof($file))
{
    $line=fgets($file);
	list($UserId, $MovieId, $Rating, $Time_Stamp) = explode ("::", $line);
	//echo "$UserId  $Gender  $Age  $JobID  $ZipCode<br>";
	$sql = "INSERT INTO Review ".
           "VALUES ".
           "($UserId,$MovieId,$Rating,'$Time_Stamp');"; 
    mysqli_select_db( $conn, 'movie_recommend' );
    mysqli_query( $conn, $sql );
}
echo "数据插入成功<br>";
fclose($file);

mysqli_close($conn);
?>