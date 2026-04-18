import streamlit as st

st.set_page_config(
    page_title="HDBSCAN Klasterisasi Banjir",
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

.hero {
    background: linear-gradient(135deg, #1565c0 0%, #1976d2 55%, #0288d1 100%);
    border-radius: 20px;
    padding: 2.6rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #e3f2fd;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 0.9rem 0;
}
.hero-sub {
    font-size: 1.1rem;
    color: #bbdefb;
    line-height: 1.75;
    max-width: 760px;
    margin: 0;
    text-align: justify;
}
.pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.2rem;
}
.pill {
    padding: 5px 13px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.30);
    color: #e8f4fd;
}

.section-card {
    background: #ffffff;
    border: 1px solid #d4e8f8;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    transition: box-shadow 0.2s ease;
}
.section-card:hover {
    box-shadow: 0 4px 20px rgba(21, 101, 192, 0.09);
}
.section-heading {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1565c0;
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-icon {
    width: 32px; height: 32px;
    border-radius: 9px;
    background: #e3f2fd;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.body-text {
    font-size: 1.1rem;
    line-height: 1.85;
    color: #3d6b8e;
    text-align: justify;
    margin: 0;
}
.body-text + .body-text { margin-top: 1rem; }

.goal-list {
    list-style: none;
    padding: 0; margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
.goal-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    font-size: 1.3rem;
    line-height: 1.75;
    color: #3d6b8e;
}
.goal-dot {
    flex-shrink: 0;
    margin-top: 0.5rem;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #1976d2;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# JUDUL HALAMAN
st.markdown("""
<div class="hero">
    <h1 class="hero-title">APLIKASI KLASTERISASI WILAYAH<br>TERDAMPAK BANJIR DI INDONESIA</h1>
    <p class="hero-sub">
        Mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan metode
        HDBSCAN (<em>Hierarchical Density-Based Spatial Clustering of Applications with Noise</em>)
        yang dikombinasikan dengan <em>Bayesian Optimization</em> untuk klasterisasi yang akurat dan andal.
    </p>
    <div class="pills">
        <span class="pill">⚙️ HDBSCAN</span>
        <span class="pill">🔧 BAYESIAN OPTIMIZATION</span>
        <span class="pill">🗺️ KLASTERISASI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# LATAR BELAKANG
st.markdown("""
<div class="section-card">
    <h2 class="section-heading">
        LATAR BELAKANG
    </h2>
    <p class="body-text">
        Banjir merupakan salah satu bencana alam yang paling sering terjadi di Indonesia dengan ribuan kejadian
        setiap tahunnya yang menimbulkan dampak signifikan terhadap kerusakan infrastruktur dan gangguan aktivitas
        sosial masyarakat. Pada tahun 2024, banjir tercatat sebagai bencana alam yang paling dominan terjadi di
        Indonesia, disertai peningkatan jumlah korban dan kerusakan dibandingkan dengan tahun-tahun sebelumnya.
        Kondisi ini menunjukkan bahwa upaya mitigasi bencana banjir di Indonesia masih belum dilakukan secara
        optimal dan membutuhkan pendekatan yang lebih efektif berbasis data.
    </p>
    <p class="body-text">
        Di sisi lain, karakteristik dampak banjir di setiap provinsi di Indonesia cenderung berbeda-beda karena
        dipengaruhi oleh kondisi geografis, lingkungan, maupun sosial ekonomi. Oleh karena itu, diperlukan suatu
        sistem yang mampu mengidentifikasi pola dampak banjir dan mengelompokkan provinsi di Indonesia berdasarkan
        tingkat keparahan dampaknya. Aplikasi ini dikembangkan dengan memanfaatkan metode HDBSCAN yang dikombinasikan
        dengan <em>Bayesian Optimization</em> untuk menghasilkan klasterisasi yang lebih akurat. Aplikasi ini mampu
        menyajikan hasil klasterisasi dalam bentuk visualisasi interaktif sehingga memudahkan pengguna dalam memahami
        distribusi tingkat keparahan dampak banjir serta mendukung pengambilan keputusan dalam upaya mitigasi bencana
        secara lebih tepat sasaran.
    </p>
</div>
""", unsafe_allow_html=True)

# TUJUAN
st.markdown("""
<div class="section-card">
    <h2 class="section-heading">
        TUJUAN
    </h2>
    <ul class="goal-list">
        <li class="goal-item">
            <span class="goal-dot"></span>
            <span>Mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan
            metode HDBSCAN dan <em>Bayesian Optimization</em>.</span>
        </li>
        <li class="goal-item">
            <span class="goal-dot"></span>
            <span>Menyediakan peta interaktif untuk menampilkan visualisasi hasil klasterisasi secara
            intuitif dan mudah dipahami oleh pengguna.</span>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)
