from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "ganti-kunci-rahasia-ini")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "db_perpustakaan_baru"),
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def dashboard():
    db = get_db()
    cur = db.cursor(dictionary=True)
    counts = {}
    for key, table in [("anggota","anggota"),("petugas","petugas"),("buku","buku"),("peminjaman","peminjaman")]:
        cur.execute(f"SELECT COUNT(*) AS total FROM {table}")
        counts[key] = cur.fetchone()["total"]
    cur.execute("""
        SELECT p.id_peminjaman, a.nama_anggota, b.judul_buku,
               p.tanggal_pinjam, p.tanggal_kembali, p.status
        FROM peminjaman p
        JOIN anggota a ON p.id_anggota=a.id_anggota
        JOIN buku b ON p.id_buku=b.id_buku
        ORDER BY p.id_peminjaman DESC LIMIT 5
    """)
    recent = cur.fetchall()
    cur.close(); db.close()
    return render_template("dashboard.html", counts=counts, recent=recent)

@app.route("/anggota", methods=["GET","POST"])
def anggota():
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == "POST":
        cur.execute("INSERT INTO anggota (nama_anggota, jenis_kelamin, kelas, alamat, no_hp) VALUES (%s,%s,%s,%s,%s)",
                    (request.form["nama"], request.form["jk"], request.form["kelas"], request.form["alamat"], request.form["no_hp"]))
        db.commit(); flash("Data anggota berhasil ditambahkan.")
        cur.close(); db.close()
        return redirect(url_for("anggota"))
    cur.execute("SELECT * FROM anggota ORDER BY id_anggota DESC")
    rows = cur.fetchall(); cur.close(); db.close()
    return render_template("anggota.html", rows=rows)

@app.post("/anggota/hapus/<int:id>")
def hapus_anggota(id):
    db=get_db(); cur=db.cursor()
    try:
        cur.execute("DELETE FROM anggota WHERE id_anggota=%s",(id,)); db.commit()
        flash("Data anggota dihapus.")
    except mysql.connector.Error:
        db.rollback(); flash("Anggota tidak bisa dihapus karena masih memiliki transaksi.")
    cur.close(); db.close()
    return redirect(url_for("anggota"))

@app.route("/buku", methods=["GET","POST"])
def buku():
    db=get_db(); cur=db.cursor(dictionary=True)
    if request.method=="POST":
        cur.execute("INSERT INTO buku (judul_buku,pengarang,penerbit,tahun_terbit,kategori,stok) VALUES (%s,%s,%s,%s,%s,%s)",
                    (request.form["judul"],request.form["pengarang"],request.form["penerbit"],request.form["tahun"],request.form["kategori"],request.form["stok"]))
        db.commit(); flash("Data buku berhasil ditambahkan.")
        cur.close(); db.close()
        return redirect(url_for("buku"))
    cur.execute("SELECT * FROM buku ORDER BY id_buku DESC")
    rows=cur.fetchall(); cur.close(); db.close()
    return render_template("buku.html",rows=rows)

@app.post("/buku/hapus/<int:id>")
def hapus_buku(id):
    db=get_db(); cur=db.cursor()
    try:
        cur.execute("DELETE FROM buku WHERE id_buku=%s",(id,)); db.commit(); flash("Data buku dihapus.")
    except mysql.connector.Error:
        db.rollback(); flash("Buku tidak bisa dihapus karena masih memiliki transaksi.")
    cur.close(); db.close()
    return redirect(url_for("buku"))

@app.route("/petugas", methods=["GET","POST"])
def petugas():
    db=get_db(); cur=db.cursor(dictionary=True)
    if request.method=="POST":
        cur.execute("INSERT INTO petugas (nama_petugas,username,password,no_hp) VALUES (%s,%s,%s,%s)",
                    (request.form["nama"],request.form["username"],request.form["password"],request.form["no_hp"]))
        db.commit(); flash("Data petugas berhasil ditambahkan.")
        cur.close(); db.close()
        return redirect(url_for("petugas"))
    cur.execute("SELECT id_petugas,nama_petugas,username,no_hp FROM petugas ORDER BY id_petugas DESC")
    rows=cur.fetchall(); cur.close(); db.close()
    return render_template("petugas.html",rows=rows)

@app.post("/petugas/hapus/<int:id>")
def hapus_petugas(id):
    db=get_db(); cur=db.cursor()
    try:
        cur.execute("DELETE FROM petugas WHERE id_petugas=%s",(id,)); db.commit(); flash("Data petugas dihapus.")
    except mysql.connector.Error:
        db.rollback(); flash("Petugas tidak bisa dihapus karena masih memiliki transaksi.")
    cur.close(); db.close()
    return redirect(url_for("petugas"))

@app.route("/peminjaman", methods=["GET","POST"])
def peminjaman():
    db=get_db(); cur=db.cursor(dictionary=True)
    if request.method=="POST":
        cur.execute("""INSERT INTO peminjaman
            (id_anggota,id_petugas,id_buku,tanggal_pinjam,tanggal_kembali,status)
            VALUES (%s,%s,%s,%s,%s,'Dipinjam')""",
            (request.form["anggota"],request.form["petugas"],request.form["buku"],request.form["tanggal_pinjam"],request.form["tanggal_kembali"] or None))
        db.commit(); flash("Peminjaman berhasil dicatat.")
        cur.close(); db.close()
        return redirect(url_for("peminjaman"))
    cur.execute("SELECT id_anggota,nama_anggota FROM anggota ORDER BY nama_anggota")
    anggota_list=cur.fetchall()
    cur.execute("SELECT id_petugas,nama_petugas FROM petugas ORDER BY nama_petugas")
    petugas_list=cur.fetchall()
    cur.execute("SELECT id_buku,judul_buku,stok FROM buku WHERE stok>0 ORDER BY judul_buku")
    buku_list=cur.fetchall()
    cur.execute("""SELECT p.*,a.nama_anggota,b.judul_buku,t.nama_petugas
        FROM peminjaman p JOIN anggota a ON p.id_anggota=a.id_anggota
        JOIN buku b ON p.id_buku=b.id_buku JOIN petugas t ON p.id_petugas=t.id_petugas
        ORDER BY p.id_peminjaman DESC""")
    rows=cur.fetchall(); cur.close(); db.close()
    return render_template("peminjaman.html",rows=rows,anggota_list=anggota_list,petugas_list=petugas_list,buku_list=buku_list)

@app.post("/peminjaman/status/<int:id>")
def status_peminjaman(id):
    db=get_db(); cur=db.cursor()
    cur.execute("UPDATE peminjaman SET status=%s WHERE id_peminjaman=%s",(request.form["status"],id))
    db.commit(); cur.close(); db.close()
    flash("Status peminjaman diperbarui.")
    return redirect(url_for("peminjaman"))

@app.route("/laporan")
def laporan():
    db=get_db(); cur=db.cursor(dictionary=True)
    cur.execute("""SELECT p.*,a.nama_anggota,b.judul_buku,t.nama_petugas
        FROM peminjaman p JOIN anggota a ON p.id_anggota=a.id_anggota
        JOIN buku b ON p.id_buku=b.id_buku JOIN petugas t ON p.id_petugas=t.id_petugas
        ORDER BY p.id_peminjaman DESC""")
    rows=cur.fetchall(); cur.close(); db.close()
    return render_template("laporan.html",rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
