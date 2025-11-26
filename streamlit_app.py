import streamlit as st
import numpy as np
import pandas as pd

# Def konstanta
PI = np.pi

# 1. Geometri

def hitung_lingkaran(r):
    """Menghitung Luas dan Keliling Lingkaran."""
    luas = PI * r**2
    keliling = 2 * PI * r
    return luas, keliling

def hitung_kubus(s):
    """Menghitung Volume dan Luas Permukaan Kubus."""
    volume = s**3
    luas_permukaan = 6 * s**2
    return volume, luas_permukaan

def hitung_silinder(r, t):
    """Menghitung Volume dan Luas Permukaan Silinder."""
    volume = PI * r**2 * t
    luas_permukaan = 2 * PI * r * (r + t)
    return volume, luas_permukaan

# 2.Duit

# Data Kurs cuman dummy ngabs
# Kurs ini adalah nilai 1 Mata Uang Asing terhadap Rupiah (IDR)
KURS_MATA_UANG = {
    "USD - Dolar AS": 16000.00,
    "JPY - Yen Jepang": 105.00,
    "EUR - Euro": 17500.00,
    "SGD - Dolar Singapura": 12000.00,
    "MYR - Ringgit Malaysia": 3500.00,
}

def konversi_kurs(jumlah_rupiah, mata_uang_tujuan, kurs_data):
    """Mengkonversi Rupiah ke mata uang asing berdasarkan kurs dummy."""
    if mata_uang_tujuan in kurs_data:
        nilai_kurs = kurs_data[mata_uang_tujuan]
        jumlah_hasil = jumlah_rupiah / nilai_kurs
        return jumlah_hasil, nilai_kurs
    return 0, 0

# 3 layout

st.set_page_config(page_title="Multi-Kalkulator", layout="wide")
st.title("Multi-Kalkulator: Geometri & Keuangan")
st.markdown("Pilih modul perhitungan yang lo butuh.")

# tab pemisah
tab_geo, tab_kurs = st.tabs(["📐 Kalkulator Geometri (GeoCalc)", "💵 Kalkulator Kurs Uang"])

# ==============================================================================
## 📐 Kalkulator Geometri (GeoCalc)
# ==============================================================================
with tab_geo:
    st.header("GeoCalc: Luas, Keliling, & Volume")
    
    pilihan_bentuk = st.selectbox(
        "Pilih Bentuk yang Ingin Dihitung:",
        ("Lingkaran (2D)", "Kubus (3D)", "Silinder (3D)")
    )
    
    st.markdown("---")

    # --- Lingkaran ---
    if pilihan_bentuk == "Lingkaran (2D)":
        st.subheader("⚪ Perhitungan Lingkaran")
        radius = st.slider("Masukkan Jari-jari (r):", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
        st.info(f"Rumus yang digunakan: Luas = $\\pi r^2$, Keliling = $2 \\pi r$")

        luas_lingkaran, keliling_lingkaran = hitung_lingkaran(radius)
        
        col_l, col_k = st.columns(2)
        col_l.metric("Luas Lingkaran", f"{luas_lingkaran:,.2f}")
        col_k.metric("Keliling Lingkaran", f"{keliling_lingkaran:,.2f}")

    # --- Kubus ---
    elif pilihan_bentuk == "Kubus (3D)":
        st.subheader("⬛ Perhitungan Kubus")
        sisi = st.slider("Masukkan Panjang Sisi (s):", min_value=0.1, max_value=10.0, value=3.0, step=0.1)
        st.info(f"Rumus yang digunakan: Volume = $s^3$, Luas Permukaan = $6 s^2$")
        
        volume_kubus, lp_kubus = hitung_kubus(sisi)

        col_v, col_lp = st.columns(2)
        col_v.metric("Volume Kubus", f"{volume_kubus:,.2f}")
        col_lp.metric("Luas Permukaan Kubus", f"{lp_kubus:,.2f}")

    # --- Silinder ---
    elif pilihan_bentuk == "Silinder (3D)":
        st.subheader(" цилинд Perhitungan Silinder")
        col_r, col_t = st.columns(2)
        radius = col_r.slider("Masukkan Jari-jari Alas (r):", min_value=0.1, max_value=10.0, value=3.0, step=0.1)
        tinggi = col_t.slider("Masukkan Tinggi (t):", min_value=0.1, max_value=20.0, value=10.0, step=0.1)
        
        st.info(f"Rumus yang digunakan: Volume = $\\pi r^2 t$, Luas Permukaan = $2 \\pi r(r+t)$")
        
        volume_silinder, lp_silinder = hitung_silinder(radius, tinggi)

        col_v, col_lp = st.columns(2)
        col_v.metric("Volume Silinder", f"{volume_silinder:,.2f}")
        col_lp.metric("Luas Permukaan Silinder", f"{lp_silinder:,.2f}")


# ==============================================================================
## Kalkulator Kurs Uang
# ==============================================================================
with tab_kurs:
    st.header("Konversi Kurs")
    st.warning("⚠️ DATA KURS YANG DI PAKAI CUMAN SIMULASI BUKAN REALTIME.")
    
    # Input Jumlah Rupiah
    jumlah_rupiah = st.number_input(
        "Jumlah Rupiah (IDR) yang Ingin Dikonversi:",
        min_value=1000,
        value=1000000,
        step=100000,
        format="%d"
    )
    
    # Hasil Konversi
    st.subheader("Hasil Konversi ke Berbagai Mata Uang:")

    kurs_keys = list(KURS_MATA_UANG.keys())
    
    # Membuat 3 kolom untuk menampilkan hasil
    cols = st.columns(3)

    for i, mata_uang in enumerate(kurs_keys):
        jumlah_hasil, nilai_kurs = konversi_kurs(jumlah_rupiah, mata_uang, KURS_MATA_UANG)
        
        with cols[i % 3]: # Menampilkan hasil per 3 kolom
            st.metric(
                label=f"{mata_uang} ({mata_uang.split(' - ')[0]})",
                value=f"{jumlah_hasil:,.2f}",
                delta=f"Kurs: 1 = Rp {nilai_kurs:,.0f}"
            )
            
    st.markdown("---")
    st.subheader("Tabel Kurs Simulas")
    
    # Tampilkan tabel kurs simulasi
    df_kurs = pd.DataFrame(
        list(KURS_MATA_UANG.items()), 
        columns=["Mata Uang", "Kurs (Rp per 1 Valas)"]
    )
    st.dataframe(df_kurs.set_index("Mata Uang"), use_container_width=True)
