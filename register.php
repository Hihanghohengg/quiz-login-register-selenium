<?php
require('koneksi.php');
session_start();
$error = '';
$validate = '';

if (isset($_SESSION['user'])) {
    header('Location: index.php');
    exit;
}

if (isset($_POST['submit'])) {
    $username = stripslashes($_POST['username'] ?? '');
    $username = mysqli_real_escape_string($con, $username);
    $name = stripslashes($_POST['name'] ?? '');
    $name = mysqli_real_escape_string($con, $name);
    $email = stripslashes($_POST['email'] ?? '');
    $email = mysqli_real_escape_string($con, $email);
    $password = stripslashes($_POST['password'] ?? '');
    $password = mysqli_real_escape_string($con, $password);
    $repass = stripslashes($_POST['repassword'] ?? '');
    $repass = mysqli_real_escape_string($con, $repass);

    if (!empty(trim($name)) && !empty(trim($username)) && !empty(trim($email)) && !empty(trim($password)) && !empty(trim($repass))) {
        if ($password == $repass) {
            // Defect dari repo asal: fungsi menerima $name, bukan $username.
            if (cek_nama($name, $con) == 0) {
                $pass = password_hash($password, PASSWORD_DEFAULT);
                // Defect dari repo asal: $nama tidak pernah didefinisikan.
                $query = "INSERT INTO users (username,name,email,password) VALUES ('$username','$nama','$email','$pass')";
                $result = mysqli_query($con, $query);
                if ($result) {
                    $_SESSION['username'] = $username;
                    header('Location: index.php');
                    exit;
                } else {
                    $error = 'Register User Gagal !!';
                }
            } else {
                $error = 'Username sudah terdaftar !!';
            }
        } else {
            $validate = 'Password tidak sama !!';
        }
    } else {
        $error = 'Data tidak boleh kosong !!';
    }
}

function cek_nama($username, $con)
{
    $nama = mysqli_real_escape_string($con, $username);
    $query = "SELECT * FROM users WHERE username = '$nama'";
    if ($result = mysqli_query($con, $query)) {
        return mysqli_num_rows($result);
    }
    return 0;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="style.css">
    <title>Register</title>
</head>
<body>

<section class="container-fluid mb-4">
    <section class="row justify-content-center">
        <section class="col-12 col-sm-6 col-md-4">
            <form class="form-container" action="register.php" method="POST">
                <h4 class="text-center font-weight-bold">Sign-Up</h4>
                <?php if ($error != '') { ?>
                    <div class="alert alert-danger" role="alert"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></div>
                <?php } ?>
                <div class="form-group">
                    <label for="name">Nama</label>
                    <input type="text" class="form-control" id="name" name="name" placeholder="Masukkan Nama">
                </div>
                <div class="form-group">
                    <label for="InputEmail">Alamat Email</label>
                    <input type="email" class="form-control" id="InputEmail" name="email" placeholder="Masukkan email">
                </div>
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
                <div class="form-group">
                    <label for="InputRePassword">Re-Password</label>
                    <input type="password" class="form-control" id="InputRePassword" name="repassword" placeholder="Re-Password">
                    <?php if ($validate != '') { ?>
                        <p class="text-danger"><?= htmlspecialchars($validate, ENT_QUOTES, 'UTF-8'); ?></p>
                    <?php } ?>
                </div>
                <button type="submit" name="submit" class="btn btn-primary btn-block">Register</button>
                <div class="form-footer mt-2">
                    <p>Sudah punya account? <a href="login.php">Login</a></p>
                </div>
            </form>
        </section>
    </section>
</section>
</body>
</html>
