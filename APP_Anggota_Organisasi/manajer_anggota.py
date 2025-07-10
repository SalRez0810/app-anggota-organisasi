from model import Anggota
import database
import pandas as pd
import datetime

class ManajerAnggota:
    def tambah_anggota(self, anggota: Anggota) -> bool:
        sql = """INSERT INTO anggota (nama, alamat, divisi, no_hp, tanggal_masuk)
                 VALUES (?, ?, ?, ?, ?)"""
        params = (
            anggota.nama, anggota.alamat, anggota.divisi,
            anggota.no_hp, anggota.tanggal_masuk.strftime("%Y-%m-%d")
        )
        return database.execute_query(sql, params) is not None

    def get_semua_dataframe(self, tanggal=None):
        sql = "SELECT id, nama, alamat, divisi, no_hp, tanggal_masuk FROM anggota"
        params = ()
        if tanggal:
            sql += " WHERE tanggal_masuk = ?"
            params = (tanggal.strftime("%Y-%m-%d"),)
        sql += " ORDER BY tanggal_masuk DESC"
        df = database.get_dataframe(sql, params)
        if not df.empty:
            df['tanggal_masuk'] = pd.to_datetime(df['tanggal_masuk']).dt.strftime('%d-%m-%Y')
        return df

    def get_ringkasan_per_divisi(self):
        sql = "SELECT divisi, COUNT(*) as jumlah FROM anggota GROUP BY divisi ORDER BY jumlah DESC"
        rows = database.fetch_query(sql)
        return {row['divisi']: row['jumlah'] for row in rows} if rows else {}

    def hapus_anggota(self, nama):
        sql = "DELETE FROM anggota WHERE nama = ?"
        return database.execute_query(sql, (nama,)) is not None

    def update_anggota(self, anggota: Anggota) -> bool:
        sql = """UPDATE anggota SET nama = ?, alamat = ?, divisi = ?, no_hp = ?, tanggal_masuk = ?
                 WHERE id = ?"""
        params = (
            anggota.nama, anggota.alamat, anggota.divisi,
            anggota.no_hp, anggota.tanggal_masuk.strftime("%Y-%m-%d"), anggota.id
        )
        return database.execute_query(sql, params) is not None