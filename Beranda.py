import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="HDBSCAN Streamlit", layout="wide")

# Logo
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

# Logo tengah BESAR
st.sidebar.image("logo.png", width=180)

# Judul
st.title("APLIKASI KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA")
st.divider()

# Deskripsi
st.markdown("""
<div style="text-align: justify;">
Aplikasi ini digunakan untuk mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan metode
HDBSCAN (<i>Hierarchical Density-Based Spatial Clustering of Applications with Noise</i>) dan <i>Bayesian Optimization</i>.
</div>
""", unsafe_allow_html=True)

st.write("")

# Latar Belakang
st.subheader("Latar Belakang")
st.markdown("""
<div style="text-align: justify;">
Banjir merupakan salah satu bencana alam yang paling sering terjadi di Indonesia dengan ribuan kejadian setiap tahunnya 
yang menimbulkan dampak signifikan terhadap kerusakan infrastruktur dan gangguan aktivitas sosial masyarakat. 
Pada tahun 2024, banjir tercatat sebagai bencana alam yang paling dominan terjadi di Indonesia, disertai peningkatan 
jumlah korban dan kerusakan dibandingkan dengan tahun-tahun sebelumnya. Kondisi ini menunjukkan bahwa upaya mitigasi 
bencana banjir di Indonesia masih belum dilakukan secara optimal dan membutuhkan pendekatan yang lebih efektif berbasis data.
""", unsafe_allow_html=True)
st.write("")
st.markdown("""
<div style="text-align: justify;">
Di sisi lain, karakteristik dampak banjir di setiap provinsi di Indonesia cenderung berbeda-beda karena dipengaruhi oleh 
kondisi geografis, lingkungan, maupun sosial ekonomi. Oleh karena itu, diperlukan suatu sistem yang mampu mengidentifikasi 
pola dampak banjir dan mengelompokkan provinsi di Indonesia berdasarkan tingkat keparahan dampaknya. Aplikasi ini 
dikembangkan dengan memanfaatkan metode HDBSCAN yang dikombinasikan dengan <i>Bayesian Optimization</i> untuk menghasilkan 
klasterisasi yang lebih akurat. Aplikasi ini mampu menyajikan hasil klasterisasi dalam bentuk visualisasi interaktif 
sehingga memudahkan pengguna dalam memahami distribusi tingkat keparahan dampak banjir serta mendukung pengambilan 
keputusan dalam upaya mitigasi bencana secara lebih tepat sasaran.
""", unsafe_allow_html=True)

st.write("")  

# Tujuan
st.subheader("Tujuan")
st.markdown("""
<div style="text-align: justify;">
<ul>
<li>Mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan metode HDBSCAN dan <i>Bayesian Optimization</i>.</li>  
<li>Menyediakan peta interaktif untuk menampilkan visualisasi hasil klasterisasi.</li>  
<li>Menyediakan fitur prediksi kategori dampak banjir berdasarkan input data baru dari pengguna.</li>
</ul>
</div>
""", unsafe_allow_html=True)
