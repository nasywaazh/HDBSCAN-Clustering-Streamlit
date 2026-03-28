import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title = "HDBSCAN Streamlit", layout="wide")

# Judul
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("APLIKASI KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA")
    st.divider()
    # Deskripsi
    st.write("""
    Aplikasi ini digunakan untuk mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir
    menggunakan metode HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise)
    dan Bayesian Optimization
    """)

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
