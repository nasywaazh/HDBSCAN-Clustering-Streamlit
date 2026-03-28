import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title = "HDBSCAN Streamlit", layout="wide")

# Judul
import streamlit as st

st.set_page_config(layout="wide")

# Judul
st.markdown("""
<h1 style='
text-align:center;
font-size:44px;
color:#1E3A8A;
'>
APLIKASI KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA
</h1>
""", unsafe_allow_html=True)

# Divider
st.markdown("""
<hr style='
height:4px;
border:none;
background-color:#3B82F6;
width:75%;
margin:auto;
margin-top:10px;
margin-bottom:25px;
'>
""", unsafe_allow_html=True)

# Deskripsi 
st.markdown("""
Aplikasi ini dikembangkan untuk **mengelompokkan provinsi di Indonesia berdasarkan tingkat keparahan dampak banjir** 
menggunakan metode **HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise)** 
yang dioptimasi dengan **Bayesian Optimization**.
""")

# Latar belakang singkat
st.subheader("📌 Latar Belakang")
st.markdown("""
Indonesia merupakan negara yang memiliki tingkat kerentanan tinggi terhadap bencana banjir. 
Perbedaan kondisi geografis, iklim, dan sosial antarwilayah menyebabkan dampak banjir yang bervariasi di setiap provinsi.

Melalui pendekatan **klasterisasi berbasis kepadatan**, aplikasi ini membantu:
- Mengidentifikasi pola dampak banjir
- Mengelompokkan wilayah dengan karakteristik serupa
- Mendukung pengambilan keputusan dalam mitigasi bencana
""")

# Tujuan aplikasi
st.subheader("🎯 Tujuan Aplikasi")
st.markdown("""
- Mengelompokkan wilayah berdasarkan tingkat keparahan dampak banjir  
- Menyediakan visualisasi peta klasterisasi interaktif  
- Memberikan prediksi kategori dampak banjir berdasarkan input data baru  
""")

st.divider()

# Fitur utama
st.subheader("⚙️ Fitur Utama")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - 📊 **Data Banjir**  
      Menampilkan data dampak banjir per provinsi

    - 🧠 **Metode**  
      Penjelasan HDBSCAN dan Bayesian Optimization
    """)

with col2:
    st.markdown("""
    - 🗺️ **Peta Klasterisasi**  
      Visualisasi tingkat keparahan banjir

    - 🔍 **Prediksi Klaster**  
      Input data baru untuk menentukan kategori dampak
    """)

st.divider()
