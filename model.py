import datetime

class Anggota:
    def __init__(self, nama, alamat, divisi, no_hp, tanggal_masuk, id_anggota=None):
        self.id = id_anggota
        self.nama = nama.strip()
        self.alamat = alamat.strip()
        self.divisi = divisi.strip()
        self.no_hp = no_hp.strip()
        if isinstance(tanggal_masuk, str):
            self.tanggal_masuk = datetime.datetime.strptime(tanggal_masuk, "%Y-%m-%d").date()
        else:
            self.tanggal_masuk = tanggal_masuk

    def to_dict(self):
        return {
            "nama": self.nama,
            "alamat": self.alamat,
            "divisi": self.divisi,
            "no_hp": self.no_hp,
            "tanggal_masuk": self.tanggal_masuk.strftime("%Y-%m-%d")
        }