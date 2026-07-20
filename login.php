<?php
require('koneksi.php');
session_start();
$error = '';
$validate = '';

if (isset($_SESSION['username'])) {
    header('Location: index.php');
    exit;
}

if (isset($_POST['submit'])) {
    $username = stripslashes($_POST['username'] ?? '');
    $username = mysqli_real_escape_string($con, $username);
    $password = stripslashes($_POST['password'] ?? '');
    $password = mysqli_real_escape_string($con, $password);

    if (!empty(trim($username)) && !empty(trim($password))) {
        $query = "SELECT * FROM users WHERE username = '$username'";
        $result = mysqli_query($con, $query);
        $rows = mysqli_num_rows($result);

        if ($rows != 0) {
            $hash = mysqli_fetch_assoc($result)['password'];
            if (password_verify($password, $hash)) {
                $_SESSION['username'] = $username;
                header('Location: index.php');
                exit;
            }
            // Defect dari repo asal: password salah tidak menghasilkan pesan error.
        } else {
            // Defect dari repo asal: pesan ini tidak sesuai konteks login.
            $error = 'Register User Gagal !!';
        }
    } else {
        $error = 'Data tidak boleh kosong !!';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="style.css">
    <title>Login</title>
</head>
<body>
<section class="container-fluid mb-4">
    <section class="row justify-content-center">
        <section class="col-12 col-sm-6 col-md-4">
            <form class="form-container" action="login.php" method="POST" novalidate>
                <h4 class="text-center font-weight-bold">Sign-In</h4>
                <?php if ($error != '') { ?>
                    <div class="alert alert-danger" role="alert"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></div>
                <?php } ?>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" class="form-control" id="username" name="username" placeholder="Masukkan username">
                </div>
                <div class="form-group">
                    <label for="InputPassword">Password</label>
                    <input type="password" class="form-control" id="InputPassword" name="password" placeholder="Password">
                    <?php if ($validate != '') { ?>
                        <p class="text-danger"><?= htmlspecialchars($validate, ENT_QUOTES, 'UTF-8'); ?></p>
                    <?php } ?>
                </div>
                <button type="submit" name="submit" class="btn btn-primary btn-block">Sign In</button>
                <div class="form-footer mt-2">
                    <p>Belum punya account? <a href="register.php">Register</a></p>
                </div>
            </form>
        </section>
    </section>
</section>
</body>
</html>
