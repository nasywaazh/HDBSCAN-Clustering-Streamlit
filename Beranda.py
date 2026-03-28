import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title = "HDBSCAN Streamlit", layout="wide")

# Judul 
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #1E3A8A;
}

.divider {
    height: 4px;
    background-color: #3B82F6;
    border: none;
    width: 80%;
    margin: 20px auto;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">APLIKASI KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Deskripsi
st.markdown("""
<div align="justify">
Aplikasi ini digunakan untuk mengelompokkan provinsi di Indonesia menggunakan metode 
HDBSCAN (*Hierarchical Density-Based Spatial Clustering of Applications with Noise*) 
dan *Bayesian Optimization*.
</div>
""", unsafe_allow_html=True)

# Latar Belakang
st.subheader("Latar Belakang")
st.markdown("""
<div align="justify">
Banjir merupakan salah satu bencana alam yang paling sering terjadi di Indonesia dengan ribuan kejadian setiap tahunnya
yang menimbulkan dampak signifikan terhadap kerusakan infrastruktur dan gangguan aktivitas sosial masyarakat. Pada tahun 2024,
banjir tercatat sebagai bencana alam yang paling dominan terjadi di Indonesia, disertai peningkatan jumlah korban dan kerusakan
dibandingkan dengan tahun-tahun sebelumnya. Kondisi ini menunjukkan bahwa upaya mitigasi bencana banjir di Indonesia masih belum
dilakukan secara optimal dan membutuhkan pendekatan yang lebih efektif berbasis data.

Di sisi lain, karakteristik dampak banjir di setiap provinsi di Indonesia cenderung berbeda-beda karena dipengaruhi oleh kondisi
geografis, lingkungan, maupun sosial ekonomi. Oleh karena itu, diperlukan suatu sistem yang mampu mengidentifikasi pola dampak banjir
dan mengelompokkan provinsi di Indonesia berdasarkan tingkat keparahan dampaknya. Aplikasi ini dikembangkan dengan memanfaatkan metode
HDBSCAN yang dikombinasikan dengan *Bayesian Optimization* untuk menghasilkan klasterisasi yang lebih akurat. Aplikasi ini mampu menyajikan
hasil klasterisasi dalam bentuk visualisasi interaktif sehingga memudahkan pengguna dalam memahami distribusi tingkat keparahan dampak banjir
serta mendukung pengambilan keputusan dalam upaya mitigasi bencana secara lebih tepat sasaran.
</div>
""", unsafe_allow_html=True)

# Tujuan
st.subheader("Tujuan")
st.markdown("""
<div align="justify">
- Mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan metode HDBSCAN dan *Bayesian Optimization*  
- Menyediakan peta interaktif untuk menampilkan visualisasi hasil klasterisasi  
- Menyediakan fitur prediksi kategori dampak banjir berdasarkan input data baru dari pengguna  
</div>
""", unsafe_allow_html=True)
