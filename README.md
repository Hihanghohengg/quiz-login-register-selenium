# Pengujian Selenium Modul Login dan Register

Repository ini merupakan jawaban tugas pengujian untuk aplikasi PHP/MySQL `hermanka/quiz-pengupil`. Solusi menggunakan Selenium WebDriver (Python), pytest, Page Object Model, MySQL test fixture, test stub untuk halaman tujuan redirect, dan GitHub Actions.

## Link

- Repository aplikasi asal: `https://github.com/hermanka/quiz-pengupil`
- Repository hasil Anda setelah diunggah: `https://github.com/USERNAME_ANDA/quiz-login-register-selenium`

## Dokumen Pengumpulan

- PDF final: `docs/Laporan_Pengujian_Selenium_Login_Register.pdf`
- DOCX editable: `docs/Laporan_Pengujian_Selenium_Login_Register.docx`

Sebelum dikumpulkan, ganti `[ISI NAMA]`, `[ISI NIM]`, `[ISI KELAS]`, dan `USERNAME_ANDA` pada dokumen. Setelah repository diunggah, cantumkan URL GitHub aktual pada halaman sampul.

## Struktur

```text
.
├── .github/workflows/selenium.yml
├── db/quiz_pengupil.sql
├── tests/
│   ├── page_objects/
│   ├── stubs/index.php
│   ├── conftest.py
│   ├── test_login.py
│   └── test_register.py
├── login.php
├── register.php
├── koneksi.php
├── requirements.txt
├── pytest.ini
├── TEST_CASES.md
└── docs/
```

## Prasyarat Lokal

- PHP 8.x dengan ekstensi `mysqli`
- MySQL/MariaDB
- Python 3.11+
- Google Chrome/Chromium dan ChromeDriver yang kompatibel

## Menjalankan Secara Lokal

### 1. Database

```bash
mysql -u root -p < db/quiz_pengupil.sql
```

Untuk XAMPP tanpa password root:

```bash
mysql -u root < db/quiz_pengupil.sql
```

### 2. Virtual environment

```bash
python -m venv .venv
```

Aktivasi Windows:

```powershell
.venv\Scripts\activate
```

Aktivasi Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Dependency

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Linux/macOS:

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=''
export DB_NAME=quiz_pengupil
export BASE_URL=http://127.0.0.1:8000
```

PowerShell:

```powershell
$env:DB_HOST='127.0.0.1'
$env:DB_PORT='3306'
$env:DB_USER='root'
$env:DB_PASSWORD=''
$env:DB_NAME='quiz_pengupil'
$env:BASE_URL='http://127.0.0.1:8000'
```

### 5. Install stub dan jalankan aplikasi

Linux/macOS:

```bash
./scripts/start-local.sh
```

Windows PowerShell:

```powershell
Copy-Item tests/stubs/index.php index.php
php -d display_errors=0 -S 127.0.0.1:8000
```

### 6. Jalankan test

Terminal baru:

```bash
pytest --junitxml=artifacts/junit.xml
```

Expected summary: 13 passed dan 4 xfailed, selama defect aplikasi asal belum diperbaiki.

## Stub dan Driver

- **Selenium ChromeDriver** mengendalikan browser sungguhan.
- **`tests/stubs/index.php`** menggantikan modul dashboard yang tidak tersedia di repo asal. Stub hanya memverifikasi bahwa login/register berhasil membuat session dan redirect.
- **MySQL fixture** pada `tests/conftest.py` me-reset database sebelum setiap testcase agar hasil deterministik.

## CI/CD

Workflow `.github/workflows/selenium.yml` melakukan checkout, menjalankan MySQL service container, mengimpor skema, memasang dependency, menyalin stub, menjalankan PHP server, menjalankan Selenium headless, dan mengunggah JUnit XML, log PHP, serta screenshot bila ada kegagalan.

## Known Defects

1. Login dengan password salah tidak menampilkan pesan.
2. Username tidak ditemukan memakai pesan `Register User Gagal !!`.
3. Register memeriksa duplikasi menggunakan nilai `name`, bukan `username`.
4. Query INSERT memakai `$nama` yang tidak didefinisikan.
5. Skema database asal tidak menerapkan `UNIQUE` pada username/email.

Test untuk defect tersebut ditandai `xfail(strict=True)` sehingga defect terdokumentasi tanpa membuat pipeline merah. Setelah defect diperbaiki, ubah test menjadi test normal dan perbarui expected result.
