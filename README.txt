WEBSITE PERPUSTAKAAN RUANG BACA
Teknologi: Python Flask + MySQL

CARA MENJALANKAN:
1. Ekstrak ZIP ini.
2. Jalankan MySQL melalui XAMPP.
3. Pastikan database db_perpustakaan_baru dan tabelnya sudah ada.
   Jika belum ada, buka phpMyAdmin > Import > pilih database.sql.
   Jika database lama sudah berisi data, jangan hapus atau replace tabel yang ada.
4. Buka CMD di folder project.
5. Jalankan: python -m pip install -r requirements.txt
6. Jalankan: python app.py
7. Buka browser: http://127.0.0.1:5000

PENGATURAN DATABASE:
Default: host=localhost, user=root, password kosong,
database=db_perpustakaan_baru.
Jika MySQL kamu memakai password, atur environment variable DB_PASSWORD
sebelum menjalankan app.py.

MENU:
Dashboard, Data Anggota, Data Petugas, Data Buku, Peminjaman, Laporan.

CATATAN:
Ini aplikasi lokal untuk latihan. Belum memiliki login, fitur edit data,
pengurangan stok otomatis, dan pengamanan password petugas. Jangan gunakan
untuk data pribadi sungguhan atau dipublikasikan ke internet sebelum
ditambahkan keamanan yang memadai.
