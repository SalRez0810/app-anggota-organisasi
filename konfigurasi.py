import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'anggota_organisasi.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

DAFTAR_DIVISI = ["Ketua", "Wakil Ketua", "Sekretaris", "Bendahara", "Humas", "Perlengkapan", "Pubdekdok", "Lainnya"]
DIVISI_DEFAULT = "Lainnya"