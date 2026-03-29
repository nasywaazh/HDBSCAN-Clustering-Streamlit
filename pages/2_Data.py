import streamlit as st
import pandas as pd

st.title("DATA INDIKATOR DAMPAK BANJIR")

# Upload file
uploaded_file = st.file_uploader(
    "Upload file CSV atau Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Membaca file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File berhasil diupload!")

        # Menampilkan informasi data
        st.subheader("Informasi Dataset")
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Baris", df.shape[0])
        col2.metric("Jumlah Kolom", df.shape[1])

        # Preview data
        st.subheader("Preview Data")
        st.dataframe(df, use_container_width=True)

        # Tampilkan tipe data
        st.subheader("Tipe Data")
        st.dataframe(df.dtypes.astype(str))

        # Optional: download kembali
        st.subheader("Download Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download sebagai CSV",
            data=csv,
            file_name="data_clean.csv",
            mime="text/csv"
        )

        # Simpan ke session state (penting untuk halaman lain)
        st.session_state["data"] = df

    except Exception as e:
        st.error(f"Terjadi error saat membaca file: {e}")

else:
    st.info("Upload file terlebih dahulu!")
