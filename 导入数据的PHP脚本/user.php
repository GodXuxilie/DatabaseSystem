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

$file=fopen("users.dat","r");
while(!feof($file))
{
    $line=fgets($file);
	list($UserId, $Gender, $Age, $JobID, $ZipCode) = explode ("::", $line);
	echo "$UserId  $Gender  $Age  $JobID  $ZipCode<br>";
	$sql = "INSERT INTO User ".
           "VALUES ".
           "($UserId,'$Gender',$Age,$JobID,'$ZipCode',NULL);"; 
    mysqli_select_db( $conn, 'movie_recommend' );
    $retval = mysqli_query( $conn, $sql );
    if(! $retval )
    {
        die('无法插入数据: ' . mysqli_error($conn));
    }
}
echo "数据插入成功<br>";
fclose($file);

mysqli_close($conn);
?>