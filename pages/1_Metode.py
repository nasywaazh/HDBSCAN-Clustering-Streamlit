import streamlit as st

st.set_page_config(
    page_title="Metode Klasterisasi",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1a3a5c;
}

[data-testid="stMain"] { background: #f0f6ff !important; }

.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1080px !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #d0e4f7 !important;
}
[data-testid="stSidebar"] * { color: #1a5fa8 !important; }

.page-header {
    background: linear-gradient(135deg, #1565c0 0%, #1976d2 55%, #0288d1 100%);
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 40%;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.page-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 0.6rem 0;
}
.page-sub {
    font-size: 1.1rem;
    color: #bbdefb;
    line-height: 1.7;
    margin: 0 0 1.4rem 0;
}

/* BADGE PILLS */
.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    position: relative;
    z-index: 1;
}
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 999px;
    padding: 0.45rem 1.1rem 0.45rem 0.7rem;
    color: #ffffff;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    transition: background 0.2s ease, border 0.2s ease;
    cursor: default;
    user-select: none;
}
.badge-pill:hover {
    background: rgba(255, 255, 255, 0.22);
    border-color: rgba(255, 255, 255, 0.4);
}
.badge-icon {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}

.method-card {
    background: #ffffff;
    border: 1px solid #d4e8f8;
    border-radius: 18px;
    margin-bottom: 1.4rem;
    overflow: hidden;
    transition: box-shadow 0.2s ease;
}
.method-card:hover {
    box-shadow: 0 6px 28px rgba(21, 101, 192, 0.11);
}
.method-header {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border-bottom: 1px solid #d4e8f8;
    padding: 1.3rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
}
.method-icon {
    width: 42px; height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #1565c0, #0288d1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.method-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #1565c0;
    margin: 0 0 0.2rem 0;
}
.method-subtitle {
    font-size: 1.1rem;
    font-weight: 500;
    color: #7bafd4;
    margin: 0;
    font-style: italic;
    line-height: 1.3;
}
.method-body {
    padding: 1.6rem 1.8rem;
}

.steps-label {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1976d2;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 1.4rem 0 0.9rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.steps-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #d4e8f8;
}

.step-list {
    list-style: none;
    padding: 0; margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.step-item {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    font-size: 1.1rem;
    line-height: 1.75;
    color: #3d6b8e;
    text-align: justify;
}
.step-num {
    flex-shrink: 0;
    width: 22px; height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1565c0, #0288d1);
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 0.22rem;
}

.body-text {
    font-size: 1.1rem;
    line-height: 1.85;
    color: #3d6b8e;
    text-align: justify;
    margin: 0;
}

.highlight-box {
    background: #e8f4fd;
    border: 1px solid #b3d9f5;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-top: 1.2rem;
    font-size: 0.85rem;
    line-height: 1.75;
    color: #1a5fa8;
}
.highlight-box strong { color: #1565c0; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# PAGE HEADER
st.markdown("""
<div class="page-header">
    <h1 class="page-title">METODE KLASTERISASI</h1>
    <p class="page-sub">
        Rangkuman metode yang digunakan dalam proses klasterisasi wilayah terdampak banjir di Indonesia,
        yaitu algoritma HDBSCAN dan Bayesian Optimization.
    </p>
    <div class="badge-row">
        <div class="badge-pill">
            <span class="badge-icon">🔵</span>
            HDBSCAN
        </div>
        <div class="badge-pill">
            <span class="badge-icon">⚙️</span>
            BAYESIAN OPTIMIZATION
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# HDBSCAN
st.markdown("""
<div class="method-card">
    <div class="method-header">
        <div class="method-icon">🔵</div>
        <div>
            <h2 class="method-title">HDBSCAN</h2>
            <p class="method-subtitle">Hierarchical Density-Based Spatial Clustering of Applications With Noise</p>
        </div>
    </div>
    <div class="method-body">
        <p class="body-text">
            HDBSCAN merupakan salah satu metode klasterisasi berbasis kepadatan (<i>density-based clustering</i>) yang
            dikembangkan dari algoritma DBSCAN. Metode ini menggabungkan pendekatan berbasis kepadatan dengan struktur
            hierarkis, serta menggunakan konsep stabilitas klaster untuk mengekstraksi klaster datar yang paling optimal.
            Keunggulan utama HDBSCAN adalah kemampuannya dalam menentukan jumlah klaster secara otomatis tanpa perlu
            menetapkan jumlah klaster di awal, mampu menangani data dengan kepadatan yang bervariasi, serta
            mengidentifikasi titik-titik yang tidak termasuk dalam klaster sebagai <i>noise</i>.
        </p>
        <p class="body-text" style="margin-top:1rem;">
            Dalam prosesnya, HDBSCAN menggunakan metrik <i>mutual reachability distance</i> untuk membangun struktur
            hierarki berdasarkan tingkat kepadatan antar titik data. Titik-titik yang tidak memenuhi ambang batas
            kepadatan akan diklasifikasikan sebagai <i>noise</i>, sedangkan kelompok data dengan jumlah anggota di
            bawah batas minimum tidak akan dianggap sebagai klaster yang valid.
        </p>
        <div class="steps-label">Alur Kerja HDBSCAN</div>
        <ol class="step-list">
            <li class="step-item">
                <span class="step-num">1</span>
                <span>Inisialisasi parameter utama, yaitu <i>minimum samples</i> (<i>min_samples</i>) dan
                <i>minimum cluster size</i> (<i>min_cluster_size</i>) sebagai dasar dalam menentukan kepadatan
                dan ukuran minimum klaster.</span>
            </li>
            <li class="step-item">
                <span class="step-num">2</span>
                <span>Menghitung <i>core distance</i> untuk setiap titik berdasarkan nilai <i>min_samples</i>
                dan menghitung <i>mutual reachability distance</i> antartitik data.</span>
            </li>
            <li class="step-item">
                <span class="step-num">3</span>
                <span>Membangun graf berbobot dan membentuk <i>Minimum Spanning Tree</i> (MST) berdasarkan
                <i>mutual reachability distance</i> untuk mempresentasikan hubungan antartitik.</span>
            </li>
            <li class="step-item">
                <span class="step-num">4</span>
                <span>Mengonstruksi struktur klaster hierarkis berdasarkan variasi kepadatan dengan menghapus
                <i>edge</i> secara bertahap dari MST sehingga terbentuk hierarki klaster dari yang paling
                padat hingga paling renggang.</span>
            </li>
            <li class="step-item">
                <span class="step-num">5</span>
                <span>Mengekstraksi klaster datar berdasarkan stabilitas klaster dengan mempertahankan klaster
                yang paling stabil sebagai hasil akhir, sementara titik yang tidak memenuhi kriteria stabilitas
                dikategorikan sebagai <i>noise</i>.</span>
            </li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)

# BAYESIAN OPTIMIZATION
st.markdown("""
<div class="method-card">
    <div class="method-header">
        <div class="method-icon">⚙️</div>
        <div>
            <h2 class="method-title">Bayesian Optimization</h2>
            <p class="method-subtitle">Optimasi Hyperparameter Berbasis Probabilistik</p>
        </div>
    </div>
    <div class="method-body">
        <p class="body-text">
            <i>Bayesian Optimization</i> digunakan untuk mencari <i>hyperparameter</i> optimal dari HDBSCAN secara
            efisien. Metode optimasi ini memanfaatkan prinsip Teorema Bayes untuk membangun model probabilistik dari
            fungsi objektif dengan menggunakan <i>Gaussian Process</i> sebagai pendekatan utama dalam memodelkan
            hubungan antara parameter dan nilai fungsi. Keunggulan utama dari teknik optimasi ini terletak pada
            kemampuannya dalam menemukan solusi optimal global dengan jumlah iterasi yang lebih sedikit, karena
            proses pencarian dipandu oleh informasi probabilistik dari evaluasi sebelumnya, bukan melalui
            eksplorasi acak.
        </p>
        <p class="body-text" style="margin-top:1rem;">
            Proses optimasi difokuskan pada <i>hyperparameter</i> utama HDBSCAN, yaitu <i>min_samples</i> dan
            <i>min_cluster_size</i>. Tujuan dari optimasi ini adalah untuk memaksimalkan kualitas klasterisasi yang
            diukur menggunakan indeks DBCV (<i>Density-Based Clustering Validation</i>) sebagai metrik evaluasi
            utama. Proses ini dilakukan secara iteratif dengan mengevaluasi berbagai kombinasi <i>hyperparameter</i>
            dan memperbarui model untuk mengarahkan pencarian ke hasil yang lebih optimal. Hasil dari proses optimasi
            ini berupa kombinasi hyperparameter terbaik yang akan digunakan dalam proses klasterisasi HDBSCAN untuk
            menghasilkan klaster yang lebih akurat dan stabil.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
