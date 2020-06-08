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

$sql = "CREATE TABLE User( ".
        "UserID INT NOT NULL, ".
        "Gender CHAR(1), ".
        "Age INT, ".
        "JobID INT, ".
		"ZipCode VARCHAR(15),".
		"Password VARCHAR(70),".
        "PRIMARY KEY ( UserID ))ENGINE=InnoDB DEFAULT CHARSET=utf8; ";
mysqli_select_db( $conn, 'movie_recommend' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('数据表创建失败: ' . mysqli_error($conn));
}
echo "数据表User创建成功<br>";

$sql = "CREATE TABLE Movie( ".
        "MovieID INT NOT NULL, ".
        "Title varchar(150), ".
        "PRIMARY KEY ( MovieID ))ENGINE=InnoDB DEFAULT CHARSET=utf8; ";
mysqli_select_db( $conn, 'movie_recommend' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('数据表创建失败: ' . mysqli_error($conn));
}
echo "数据表Movie创建成功<br>";

$sql = "CREATE TABLE Movie_Genre( ".
        "MovieID INT NOT NULL, ".
        "Genre varchar(20) );";
mysqli_select_db( $conn, 'movie_recommend' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('数据表创建失败: ' . mysqli_error($conn));
}
echo "数据表Movie_Genre创建成功<br>";

$sql = "CREATE TABLE Review( ".
        "UserID INT NOT NULL, ".
        "MovieID INT NOT NULL, ".
		"Rating int,".
		"Time_Stamp varchar(10),".
        "PRIMARY KEY ( UserID,MovieID ))ENGINE=InnoDB DEFAULT CHARSET=utf8; ";
mysqli_select_db( $conn, 'movie_recommend' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('数据表创建失败: ' . mysqli_error($conn));
}
echo "数据表Review创建成功<br>";

$sql = "CREATE TABLE Watch_History( ".
        "UserID INT NOT NULL, ".
        "MovieID INT NOT NULL, ".
		"Time_Stamp varchar(10),".
        "PRIMARY KEY ( UserID,MovieID,Time_Stamp ))ENGINE=InnoDB DEFAULT CHARSET=utf8; ";
mysqli_select_db( $conn, 'movie_recommend' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('数据表创建失败: ' . mysqli_error($conn));
}
echo "数据表Watch_History创建成功<br>";

mysqli_close($conn);
?>