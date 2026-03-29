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
<div style="text-align: justify;">
<ul>
<li>Inisialisasi parameter utama, yaitu <i>minimum samples</i> (<i>min_samples</i>) dan <i>minimum cluster size</i> (<i>min_cluster_size</i>) sebagai dasar dalam menentukan kepadatan dan ukuran minimum klaster.</li>
<li>Menghitung <i>core distance</i> untuk setiap titik berdasarkan nilai <i>min_samples</i> dan menghitung <i>mutual reachability distance</i> antartitik data.</li>
<li>Membangun graf berbobot dan membentuk <i>Minimum Spanning Tree</i> (MST) berdasarkan <i>mutual reachability distance</i> untuk mempresentasikan hubungan antartitik.</li>
<li>Mengonstruksi struktur klaster hierarkis berdasarkan variasi kepadatan dengan menghapus <i>edge</i> secara bertahap dari MST sehingga terbentuk hierarki klaster dari yang paling padat hingga paling renggang.</li>
<li>Mengekstraksi klaster datar berdasarkan stabilitas klaster dengan mempertahankan klaster yang paling stabil sebagai hasil akhir, sementara titik yang tidak memenuhi kriteria stabilititas dikategorikan sebagai <i>noise</i>.</li>
</ul>
</div>
""", unsafe_allow_html=True)
st.write("")

st.header("Bayesian Optimization")
st.write("""
Bayesian Optimization digunakan untuk menemukan parameter terbaik 
dalam proses clustering.
""")
