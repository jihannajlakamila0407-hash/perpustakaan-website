CREATE DATABASE IF NOT EXISTS db_perpustakaan_baru;
USE db_perpustakaan_baru;

CREATE TABLE IF NOT EXISTS anggota (
 id_anggota INT AUTO_INCREMENT PRIMARY KEY,
 nama_anggota VARCHAR(100) NOT NULL,
 jenis_kelamin VARCHAR(20),
 kelas VARCHAR(30),
 alamat TEXT,
 no_hp VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS petugas (
 id_petugas INT AUTO_INCREMENT PRIMARY KEY,
 nama_petugas VARCHAR(100) NOT NULL,
 username VARCHAR(50) NOT NULL,
 password VARCHAR(255) NOT NULL,
 no_hp VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS buku (
 id_buku INT AUTO_INCREMENT PRIMARY KEY,
 judul_buku VARCHAR(200) NOT NULL,
 pengarang VARCHAR(100),
 penerbit VARCHAR(100),
 tahun_terbit INT,
 kategori VARCHAR(80),
 stok INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS peminjaman (
 id_peminjaman INT AUTO_INCREMENT PRIMARY KEY,
 id_anggota INT NOT NULL,
 id_petugas INT NOT NULL,
 id_buku INT NOT NULL,
 tanggal_pinjam DATE NOT NULL,
 tanggal_kembali DATE,
 status ENUM('Dipinjam','Dikembalikan') DEFAULT 'Dipinjam',
 FOREIGN KEY (id_anggota) REFERENCES anggota(id_anggota),
 FOREIGN KEY (id_petugas) REFERENCES petugas(id_petugas),
 FOREIGN KEY (id_buku) REFERENCES buku(id_buku)
);
