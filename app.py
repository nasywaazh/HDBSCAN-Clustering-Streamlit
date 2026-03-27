import streamlit as st

st.set_page_config(page_title="Klasterisasi Banjir", layout="wide")

st.title("🌊 Aplikasi Klasterisasi Wilayah Terdampak Banjir")

st.write("""
Aplikasi ini digunakan untuk mengelompokkan wilayah terdampak banjir di Indonesia 
menggunakan metode **HDBSCAN** dan **Bayesian Optimization**.

### 📌 Menu:
- 📊 Data
- 📘 Metode
- 🗺️ Peta Klaster
- 🧪 Klasterisasi

Silakan pilih menu di sidebar 👈
""")