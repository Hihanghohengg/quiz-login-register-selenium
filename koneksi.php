<?php
// Default tetap kompatibel dengan XAMPP; environment variables dipakai di CI.
$host = getenv('DB_HOST') ?: 'localhost';
$port = (int) (getenv('DB_PORT') ?: 3306);
$user = getenv('DB_USER') ?: 'root';
$password = getenv('DB_PASSWORD') !== false ? getenv('DB_PASSWORD') : '';
$db = getenv('DB_NAME') ?: 'quiz_pengupil';

$con = mysqli_connect($host, $user, $password, $db, $port);
if (!$con) {
    die('Connection failed: ' . mysqli_connect_error());
}
mysqli_set_charset($con, 'utf8mb4');
?>
