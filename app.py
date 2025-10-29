import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date

st.set_page_config(
    page_title="Sistem Tanam & Panen Sawit 🌴",
    page_icon="🌾",
    layout="wide",
)

# ============================
# MOCK DATA
# ============================

tanam_data = pd.DataFrame({
    "ID": range(1, 11),
    "Nama_Lahan": [
        "Blok A1", "Blok A2", "Blok B1", "Blok B2", "Blok C1",
        "Blok C2", "Blok D1", "Blok D2", "Blok E1", "Blok E2"
    ],
    "Tanggal_Tanam": pd.date_range("2023-01-01", periods=10, freq="90D"),
    "Luas_Lahan (Ha)": np.random.randint(5, 15, 10),
    "Jumlah_Pohon": np.random.randint(1000, 2500, 10),
    "Varietas": np.random.choice(["Tenera", "DxP", "Lainnya"], 10),
    "Lokasi": np.random.choice(["Utara", "Selatan", "Timur", "Barat"], 10),
})

# Buat data hasil panen simulasi
panen_data = pd.DataFrame({
    "ID_Tanam": np.random.choice(tanam_data["ID"], 20),
    "Tanggal_Panen": pd.date_range("2024-01-01", periods=20, freq="30D"),
    "Hasil_Panen (Kg)": np.random.randint(5000, 20000, 20),
})

# ============================
# SIDEBAR MENU
# ============================

st.sidebar.title("🌴 Navigasi Sistem Sawit")
menu = st.sidebar.radio("Pilih Halaman", ["🏠 Dashboard", "📋 Input Data", "📈 Monitoring"])

# ============================
# DASHBOARD
# ============================

if menu == "🏠 Dashboard":
    st.title("🌾 Dashboard Produksi Sawit")

    total_lahan = tanam_data["Luas_Lahan (Ha)"].sum()
    total_pohon = tanam_data["Jumlah_Pohon"].sum()
    total_panen = panen_data["Hasil_Panen (Kg)"].sum()
    rata_panen = panen_data["Hasil_Panen (Kg)"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌱 Total Lahan", f"{total_lahan} Ha")
    c2.metric("🌳 Jumlah Pohon", total_pohon)
    c3.metric("🥥 Total Panen", f"{total_panen:,} Kg")
    c4.metric("📈 Rata-rata Panen", f"{rata_panen:,.0f} Kg")

    st.subheader("Grafik Tren Hasil Panen")
    panen_data["Bulan"] = pd.to_datetime(panen_data["Tanggal_Panen"]).dt.strftime("%Y-%m")
    chart_data = panen_data.groupby("Bulan")["Hasil_Panen (Kg)"].sum().reset_index()
    st.line_chart(chart_data.set_index("Bulan"))

# ============================
# INPUT DATA
# ============================

elif menu == "📋 Input Data":
    st.title("📥 Input Data Tanam & Panen")

    tab1, tab2 = st.tabs(["🌱 Data Tanam", "🥥 Data Panen"])

    with tab1:
        st.subheader("Tambah Data Tanam Baru")
        tanggal_tanam = st.date_input("Tanggal Tanam", date.today())
        luas = st.number_input("Luas Lahan (Ha)", min_value=0.0)
        pohon = st.number_input("Jumlah Pohon", min_value=0)
        varietas = st.selectbox("Varietas", ["Tenera", "DxP", "Lainnya"])
        lokasi = st.selectbox("Lokasi", ["Utara", "Selatan", "Timur", "Barat"])
        nama = st.text_input("Nama Lahan")
        if st.button("💾 Simpan Data Tanam"):
            st.success(f"✅ Data tanam '{nama}' berhasil disimpan (mock)!")

    with tab2:
        st.subheader("Input Data Panen")
        id_tanam = st.number_input("ID Tanam", min_value=1, max_value=10)
        tanggal_panen = st.date_input("Tanggal Panen", date.today())
        hasil = st.number_input("Hasil Panen (Kg)", min_value=0)
        pekerja = st.text_input("Nama Pekerja")
        catatan = st.text_area("Catatan")
        if st.button("💾 Simpan Data Panen"):
            st.success(f"✅ Data panen untuk lahan ID {id_tanam} berhasil disimpan (mock)!")

# ============================
# MONITORING
# ============================

elif menu == "📈 Monitoring":
    st.title("📊 Monitoring Perkembangan Sawit")

    today = pd.Timestamp.today()
    tanam_data["Umur (Bulan)"] = ((today - tanam_data["Tanggal_Tanam"]) / np.timedelta64(1, "D") / 30).astype(int)

    # Progress & status
    tanam_data["Progress (%)"] = np.clip(tanam_data["Umur (Bulan)"] / 36 * 100, 0, 100).astype(int)
    tanam_data["Status"] = tanam_data["Progress (%)"].apply(
        lambda x: "🚜 Baru Tanam" if x < 30 else "🌿 Tumbuh" if x < 70 else "🥥 Siap Panen"
    )

    lokasi_filter = st.multiselect("📍 Filter Lokasi", tanam_data["Lokasi"].unique(), default=None)
    filtered = tanam_data[tanam_data["Lokasi"].isin(lokasi_filter)] if lokasi_filter else tanam_data

    st.markdown("### 📋 Data Lahan Sawit")
    for i, row in filtered.iterrows():
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 2, 2, 3])
            c1.write(f"**{row['Nama_Lahan']}**")
            c1.write(f"📅 Tanam: {row['Tanggal_Tanam'].strftime('%d %b %Y')}")
            c2.write(f"🌱 Varietas: {row['Varietas']}")
            c2.write(f"📍 Lokasi: {row['Lokasi']}")
            c3.metric("⏳ Umur", f"{row['Umur (Bulan)']} bln")
            c3.metric("🌾 Progress", f"{row['Progress (%)']}%")
            progress_color = "green" if row["Progress (%)"] > 70 else "orange" if row["Progress (%)"] > 30 else "red"
            c4.progress(row["Progress (%)"] / 100)
            st.markdown(f"**Status:** <span style='color:{progress_color};font-weight:bold'>{row['Status']}</span>", unsafe_allow_html=True)
            st.divider()

    st.subheader("📦 Total Produksi per Lahan")
    summary = panen_data.groupby("ID_Tanam")["Hasil_Panen (Kg)"].sum().reset_index()
    merged = pd.merge(tanam_data[["ID", "Nama_Lahan"]], summary, left_on="ID", right_on="ID_Tanam", how="left").fillna(0)
    st.dataframe(merged[["Nama_Lahan", "Hasil_Panen (Kg)"]])

    st.bar_chart(merged.set_index("Nama_Lahan")["Hasil_Panen (Kg)"])

