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

$file=fopen("movies.dat","r");
while(!feof($file))
{
    $line=fgets($file);
	list($MovieId, $Title, $Genre) = explode ("::", $line);
	$sql = "INSERT INTO Movie ".
           "VALUES ".
           "($MovieId,'$Title');"; 
    mysqli_select_db( $conn, 'movie_recommend' );
    mysqli_query( $conn, $sql );
	
	list($G1,$G2,$G3,$G4,$G5,$G6,$G7)=explode("|",$Genre);
	//echo "$G1 $G2 $G3 $G4 $G5 $G6 $G7<br>";
	
	if($G1!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G1');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
	
	if($G2!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G2');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
	
	if($G3!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G3');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
	
	if($G4!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G4');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
	
	if($G5!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G5');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
	
	if($G6!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G6');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
	
	if($G7!=NULL)
	{
		$sql = "INSERT INTO Movie_Genre ".
           "VALUES ".
           "($MovieId,'$G7');"; 
        mysqli_select_db( $conn, 'movie_recommend' );
        mysqli_query( $conn, $sql );
	}
}
echo "数据插入成功<br>";
fclose($file);

mysqli_close($conn);
?>