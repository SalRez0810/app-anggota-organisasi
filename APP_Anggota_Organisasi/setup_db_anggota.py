import sqlite3
from konfigurasi import DB_PATH

def setup_database():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anggota (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    alamat TEXT NOT NULL,
                    divisi TEXT,
                    no_hp TEXT,
                    tanggal_masuk DATE NOT NULL
                )
            """)
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    setup_database()