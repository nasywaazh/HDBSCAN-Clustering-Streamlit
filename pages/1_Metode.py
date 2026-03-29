import streamlit as st

st.title("Metode Klasterisasi")

st.header("HDBSCAN")
st.markdown("""
<div style="text-align: justify;">
HDBSCAN (<i>Hierarchical Density-Based Spatial Clustering of Applications with Noise</i>) merupakan merupakan salah satu metode
klasterisasi berbasis kepadatan (<i>density-based clustering</i>) yang dikembangkan dari algoritma DBSCAN. Metode ini menggabungkan pendekatan
berbasis kepadatan dengan struktur hierarkis, serta menggunakan konsep stabilitas klaster untuk mengekstraksi klaster datar yang paling optimal.
Keunggulan utama HDBSCAN adalah kemampuannya dalam menentukan jumlah klaster secara otomatis tanpa perlu menetapkan jumlah klaster di awal,
mampu menangani data dengan kepadatan yang bervariasi, serta mengidentifikasi titik-titik yang tidak termasuk dalam klaster sebagai <i>noise</i>.
</div>
""", unsafe_allow_html=True)
st.write("")
st.markdown("""
<div style="text-align: justify;">
Dalam prosesnya, HDBSCAN menggunakan metrik <i>mutual reachability distance</i> untuk membangun struktur hierarki berdasarkan tingkat
kepadatan antar titik data. Titik-titik yang tidak memenuhi ambang batas kepadatan akan diklasifikasikan sebagai <i>noise</i>, sedangkan
kelompok data dengan jumlah anggota di bawah batas minimum tidak akan dianggap sebagai klaster yang valid. Secara umum, alur kerja metode
HDBSCAN adalah sebagai berikut:
</div>
""", unsafe_allow_html=True)
st.markdown("""
- Inisialisasi parameter utama, yaitu minimum samples (min_samples) dan minimum cluster size (min_cluster_size) sebagai dasar dalam menentukan kepadatan dan ukuran minimum klaster
- Menghitung core distance untuk setiap titik berdasarkan nilai min_samples dan menghitung mutual reachability distance antartitik data
- Membangun graf berbobot dan membentuk Minimum Spanning Tree (MST) berdasarkan mutual reachability distance untuk mempresentasikan hubungan antartitik
- Mengonstruksi struktur klaster hierarkis berdasarkan variasi kepadatan dengan menghapus edge secara bertahap dari MST sehingga terbentuk hierarki klaster dari yang paling padat hingga paling renggang
- Mengekstraksi klaster datar berdasarkan stabilitas klaster dengan mempertahankan klaster yang paling stabil sebagai hasil akhir, sementara titik yang tidak memenuhi kriteria stabilititas dikategorikan sebagai noise
""")

st.header("Bayesian Optimization")
st.write("""
Bayesian Optimization digunakan untuk menemukan parameter terbaik 
dalam proses clustering.
""")
