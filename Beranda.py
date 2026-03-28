import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title = "HDBSCAN Streamlit", layout="wide")

# Judul
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1E3A8A;
}

.divider {
    height: 4px;
    background-color: #3B82F6;
    border: none;
    width: 60%;
    margin: 20px auto;
}
</style>
""", unsafe_allow_html=True)

# Pakai HTML
st.markdown('<div class="title">APLIKASI KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Latar Belakang
st.subheader("Latar Belakang")
st.markdown("""
Indonesia merupakan negara yang memiliki tingkat kerentanan tinggi terhadap bencana banjir. 
Perbedaan kondisi geografis, iklim, dan sosial antarwilayah menyebabkan dampak banjir yang bervariasi di setiap provinsi.

Melalui pendekatan **klasterisasi berbasis kepadatan**, aplikasi ini membantu:
- Mengidentifikasi pola dampak banjir
- Mengelompokkan wilayah dengan karakteristik serupa
- Mendukung pengambilan keputusan dalam mitigasi bencana
""")

# Tujuan
st.subheader("Tujuan")
st.markdown("""
- Mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan metode HDBSCAN dan Bayesian Optimization
- Menampilkan visualisasi hasil klasterisasi interaktif  
- Memberikan hasil prediksi kategori dampak banjir berdasarkan input data baru  
""")
