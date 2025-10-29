import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- Mock Data ---
tanam_data = pd.DataFrame({
    "ID": [1, 2, 3],
    "Tanggal_Tanam": ["2023-03-10", "2024-01-15", "2024-06-01"],
    "Luas_Lahan (Ha)": [10, 8, 12],
    "Jumlah_Pohon": [1500, 1200, 1800],
    "Varietas": ["Tenera", "DxP", "Tenera"],
    "Lokasi": ["Blok A", "Blok B", "Blok C"]
})

panen_data = pd.DataFrame({
    "ID_Tanam": [1, 1, 2, 3, 3],
    "Tanggal_Panen": [
        "2024-04-20", "2024-07-18", "2024-09-05",
        "2024-08-12", "2024-10-15"
    ],
    "Hasil_Panen (Kg)": [12000, 15000, 9000, 11000, 12500],
    "Pekerja": ["Budi", "Andi", "Sari", "Tono", "Dewi"],
    "Catatan": ["Cuaca baik", "Tanah lembab", "Curah hujan tinggi", "Normal", "Produktif"]
})

# --- Sidebar ---
st.sidebar.title("🌴 Sistem Sawit")
menu = st.sidebar.radio("Navigasi", ["Dashboard", "Input Data", "Monitoring"])

# --- Dashboard ---
if menu == "Dashboard":
    st.title("🌾 Dashboard Produksi Sawit")

    total_lahan = tanam_data["Luas_Lahan (Ha)"].sum()
    total_pohon = tanam_data["Jumlah_Pohon"].sum()
    total_panen = panen_data["Hasil_Panen (Kg)"].sum()
    rata_panen = panen_data["Hasil_Panen (Kg)"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌱 Total Lahan", f"{total_lahan} Ha")
    col2.metric("🌳 Jumlah Pohon", total_pohon)
    col3.metric("🥥 Total Panen", f"{total_panen:,} Kg")
    col4.metric("📈 Rata-rata Panen", f"{rata_panen:,.0f} Kg")

    # Grafik tren panen
    st.subheader("Grafik Tren Hasil Panen (Kg per Bulan)")
    panen_data["Tanggal_Panen"] = pd.to_datetime(panen_data["Tanggal_Panen"])
    panen_data["Bulan"] = panen_data["Tanggal_Panen"].dt.strftime("%Y-%m")
    tren = panen_data.groupby("Bulan")["Hasil_Panen (Kg)"].sum().reset_index()

    st.line_chart(tren.set_index("Bulan"))

# --- Input Data ---
elif menu == "Input Data":
    st.title("📋 Input Data Tanam & Panen")

    tab1, tab2 = st.tabs(["🌱 Data Tanam", "🥥 Data Panen"])

    with tab1:
        st.subheader("Input Data Tanam")
        tanggal_tanam = st.date_input("Tanggal Tanam", datetime.date.today())
        luas = st.number_input("Luas Lahan (Ha)", min_value=0.0)
        pohon = st.number_input("Jumlah Pohon", min_value=0)
        varietas = st.selectbox("Varietas", ["Tenera", "DxP", "Lainnya"])
        lokasi = st.text_input("Lokasi Lahan")
        if st.button("Simpan Data Tanam"):
            st.success(f"✅ Data tanam {lokasi} tersimpan!")

    with tab2:
        st.subheader("Input Data Panen")
        id_tanam = st.number_input("ID Tanam", min_value=1)
        tanggal_panen = st.date_input("Tanggal Panen", datetime.date.today())
        hasil = st.number_input("Hasil Panen (Kg)", min_value=0)
        pekerja = st.text_input("Nama Pekerja")
        catatan = st.text_area("Catatan")
        if st.button("Simpan Data Panen"):
            st.success(f"✅ Data panen ID {id_tanam} berhasil disimpan!")

# --- Monitoring ---
elif menu == "Monitoring":
    st.title("📊 Monitoring Perkembangan Sawit")
    lokasi_filter = st.multiselect("Filter Lokasi", tanam_data["Lokasi"].unique())
    if lokasi_filter:
        filtered = tanam_data[tanam_data["Lokasi"].isin(lokasi_filter)]
    else:
        filtered = tanam_data

    # Hitung umur pohon
    today = pd.Timestamp.today()
    filtered["Umur (Bulan)"] = (
        (today - pd.to_datetime(filtered["Tanggal_Tanam"])) / np.timedelta64(1, "M")
    ).astype(int)

    st.dataframe(filtered)

    st.subheader("Perkembangan Produksi")
    st.bar_chart(panen_data.groupby("ID_Tanam")["Hasil_Panen (Kg)"].sum())

