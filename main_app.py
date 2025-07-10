import streamlit as st
import datetime
from model import Anggota
from manajer_anggota import ManajerAnggota
from konfigurasi import DAFTAR_DIVISI

# ✅ Konfigurasi Halaman & CSS
st.set_page_config(page_title="📋 Manajemen Anggota Organisasi", layout="wide", initial_sidebar_state="expanded")

# ✅ Tema Light & Dark Mode Responsive
st.markdown("""
    <style>
        .stApp {background-color: #f8fff8; color: #2e7d32;}
        .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; padding: 0.6em 1.2em;}
        .stTextInput>div>div>input, .stNumberInput>div>div>input {border-radius: 8px; border: 1px solid #81c784;}
        .stSelectbox>div>div {border-radius: 8px;}
        section[data-testid="stSidebar"] {background-color: #e8f5e9;}
        .css-1d391kg, .css-10trblm {color: #1b5e20 !important;}
        section[data-testid="stSidebar"] > div {padding-top: 20px;}

        @media (prefers-color-scheme: dark) {
            .stApp {background-color: #121212; color: #d0ffd0;}
            section[data-testid="stSidebar"] {background-color: #1b1b1b;}
            .css-1d391kg, .css-10trblm {color: #81c784 !important;}
            .stButton>button {background-color: #388e3c; color: white;}
            .stTextInput>div>div>input, .stNumberInput>div>div>input {
                border: 1px solid #81c784;
                background-color: #2c2c2c;
                color: #d0ffd0;
            }
            .stSelectbox>div>div {
                background-color: #2c2c2c;
                color: #d0ffd0;
            }
        }
    </style>
""", unsafe_allow_html=True)

manajer = ManajerAnggota()

# ✅ Halaman Login
def halaman_login():
    st.title("🔐 Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state["logged_in"] = True
            st.success("✅ Login berhasil.")
        else:
            st.error("❌ Username atau password salah.")

# ✅ Halaman Tambah
def halaman_tambah():
    st.title("📋 IRMAS AL-MUSTHOFA")
    st.markdown("### 🧑‍🤝‍🧑 Tambah Data Anggota Baru")
    st.info("Isilah form berikut untuk menambahkan anggota ke dalam sistem.")

    with st.form("form_tambah"):
        nama = st.text_input("Nama Lengkap")
        alamat = st.text_input("Alamat")
        divisi = st.selectbox("Divisi", DAFTAR_DIVISI)
        no_hp = st.text_input("Nomor HP")
        tanggal = st.date_input("Tanggal Masuk", value=datetime.date.today())
        simpan = st.form_submit_button("Simpan Data")

        if simpan:
            anggota = Anggota(nama, alamat, divisi, no_hp, tanggal)
            if manajer.tambah_anggota(anggota):
                st.success("✅ Data anggota berhasil ditambahkan.")
                st.rerun()
            else:
                st.error("❌ Gagal menambahkan anggota.")

# ✅ Halaman Riwayat
def halaman_riwayat():
    st.subheader("📄 Daftar Riwayat Anggota")
    df = manajer.get_semua_dataframe()
    if df.empty:
        st.info("📭 Belum ada data anggota.")
    else:
        st.dataframe(df, use_container_width=True)

    if st.session_state.get("logged_in"):
        with st.expander("✏️ Edit Data Anggota Berdasarkan ID"):
            id_edit = st.number_input("Masukkan ID Anggota", min_value=1, step=1)
            nama = st.text_input("Nama Baru")
            alamat = st.text_input("Alamat Baru")
            divisi = st.selectbox("Divisi Baru", DAFTAR_DIVISI)
            no_hp = st.text_input("Nomor HP Baru")
            tanggal = st.date_input("Tanggal Masuk Baru", value=datetime.date.today())
            if st.button("Update Data"):
                anggota = Anggota(nama, alamat, divisi, no_hp, tanggal, id_anggota=int(id_edit))
                if manajer.update_anggota(anggota):
                    st.success("✅ Data berhasil diperbarui.")
                    st.rerun()
                else:
                    st.error("❌ Gagal memperbarui data.")

        with st.expander("🗑️ Hapus Anggota Berdasarkan Nama"):
            nama_hapus = st.text_input("Masukkan nama anggota yang akan dihapus")
            if st.button("Hapus Data"):
                if manajer.hapus_anggota(nama_hapus):
                    st.success("✅ Data berhasil dihapus.")
                    st.rerun()
                else:
                    st.error("❌ Nama tidak ditemukan.")
    else:
        st.warning("⚠️ Login sebagai admin untuk akses Edit & Hapus.")

# ✅ Halaman Ringkasan
def halaman_ringkasan():
    st.subheader("📊 Statistik Anggota per Divisi")
    data = manajer.get_ringkasan_per_divisi()
    if data:
        st.bar_chart(data)
    else:
        st.info("📭 Belum ada data anggota.")

# ✅ Navigasi
def main():
    menu = st.sidebar.radio("📂 Menu Navigasi", ["➕ Tambah", "📑 Daftar Anggota", "📊 Grafik", "🔐 Login Jika Admin"])

    st.sidebar.markdown("---")
    st.sidebar.image("logo_irmas.png", width=150)
    st.sidebar.caption("Ikatan Remaja Masjid Al-Musthofa\nKebonagung, Tegowanu, Grobogan")
    st.sidebar.write("📅", datetime.date.today().strftime("%d %B %Y"))

    if menu == "➕ Tambah":
        halaman_tambah()
    elif menu == "📑 Daftar Anggota":
        halaman_riwayat()
    elif menu == "📊 Grafik":
        halaman_ringkasan()
    elif menu == "🔐 Login Jika Admin":
        halaman_login()

if __name__ == "__main__":
    main()
