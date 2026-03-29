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

        # Informasi data
        st.subheader("Informasi Data")
        col1, col2 = st.columns(2)
        col1.metric("Jumlah Baris", df.shape[0])
        col2.metric("Jumlah Kolom", df.shape[1])

        # Preview data
        st.subheader("Preview Data")
        st.dataframe(df, use_container_width=True)

        # Tampilkan tipe data
        st.subheader("Tipe Data")
        dtype_df = df.dtypes.reset_index()
        dtype_df.columns = ["Nama Kolom", "Tipe Data"]
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

        # Simpan ke session state
        st.session_state["data"] = df

    except Exception as e:
        st.error(f"Terjadi error saat membaca file: {e}")

else:
    st.info("Upload file terlebih dahulu!")
