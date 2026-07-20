# Mengunggah Repository Hasil

1. Buat repository kosong di GitHub, misalnya `quiz-login-register-selenium`.
2. Jangan centang pembuatan README karena paket ini sudah memilikinya.
3. Jalankan dari folder proyek:

```bash
git init
git add .
git commit -m "Add Selenium tests and GitHub Actions pipeline"
git branch -M main
git remote add origin https://github.com/USERNAME_ANDA/quiz-login-register-selenium.git
git push -u origin main
```

4. Buka tab **Actions** dan pastikan workflow `Selenium Login Register Tests` hijau.
5. Ganti placeholder repository pada PDF/README dengan URL aktual:

```text
https://github.com/USERNAME_ANDA/quiz-login-register-selenium
```
