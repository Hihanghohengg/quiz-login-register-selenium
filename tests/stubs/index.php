<?php
// Test Stub: menggantikan dashboard/index.php yang tidak tersedia di repo asal.
session_start();
if (!isset($_SESSION['username'])) {
    header('Location: login.php');
    exit;
}
?>
<!doctype html>
<html lang="id">
<head><meta charset="utf-8"><title>Stub Dashboard</title></head>
<body>
<h1 id="welcome">Selamat datang, <?= htmlspecialchars($_SESSION['username'], ENT_QUOTES, 'UTF-8'); ?></h1>
<p id="stub-marker">TEST_STUB_INDEX</p>
</body>
</html>
