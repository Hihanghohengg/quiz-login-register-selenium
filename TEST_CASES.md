# Daftar Testcase Login dan Register

## Modul Login

| ID | Skenario | Data Uji | Hasil yang Diharapkan | Otomasi |
|---|---|---|---|---|
| LGN-001 | Membuka halaman login | URL `/login.php` | Judul, username, password, dan tombol tampil | Pass |
| LGN-002 | Navigasi ke register | Klik `Register` | Berpindah ke `/register.php` | Pass |
| LGN-003 | Semua field kosong | username/password kosong | Pesan `Data tidak boleh kosong !!` | Pass |
| LGN-004 | Login valid | `testuser` / `Password123!` | Redirect ke stub `index.php` dan session terbentuk | Pass |
| LGN-005 | Username tidak dikenal | `unknown-user` | Pesan generik `Username atau password salah !!` | XFail - defect pesan |
| LGN-006 | Password salah | `testuser` / `WrongPassword!` | Pesan generik autentikasi | XFail - tidak ada pesan |
| LGN-007 | Percobaan SQL injection | `' OR 1=1 -- ` | Tidak terautentikasi | Pass |
| LGN-008 | Masking password | inspeksi atribut | `type=password` | Pass |

## Modul Register

| ID | Skenario | Data Uji | Hasil yang Diharapkan | Otomasi |
|---|---|---|---|---|
| REG-001 | Membuka halaman register | URL `/register.php` | Seluruh field dan tombol tampil | Pass |
| REG-002 | Navigasi ke login | Klik `Login` | Berpindah ke `/login.php` | Pass |
| REG-003 | Semua field kosong | semua kosong | Pesan `Data tidak boleh kosong !!` | Pass |
| REG-004 | Konfirmasi password berbeda | password ≠ repassword | Pesan `Password tidak sama !!` | Pass |
| REG-005 | Registrasi valid | data Budi | Redirect dan seluruh field tersimpan benar | XFail - `$nama` undefined |
| REG-006 | Username duplikat | username `testuser` | Registrasi ditolak, jumlah record tetap satu | XFail - cek field salah |
| REG-007 | Format email salah | `bukan-email` | Browser menahan submit | Pass |
| REG-008 | Masking password | inspeksi atribut | kedua field `type=password` | Pass |
| REG-009 | Input hanya spasi | string spasi | Pesan data kosong | Pass |
