import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="HDBSCAN Klasterisasi Banjir",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Custom ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #020f1f !important;
    font-family: 'Inter', sans-serif;
    color: #c8dff5;
}

/* ── App Background with animated gradient mesh ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(0, 80, 180, 0.25) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 90% 80%, rgba(0, 40, 120, 0.30) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 50% 50%, rgba(0, 120, 220, 0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #010c1a 0%, #021428 60%, #010c1a 100%) !important;
    border-right: 1px solid rgba(0, 140, 255, 0.18) !important;
}
[data-testid="stSidebar"] * { color: #a8cdf0 !important; }
[data-testid="stSidebarNavLink"] {
    border-radius: 8px !important;
    margin: 2px 8px !important;
    transition: background 0.2s ease !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: rgba(0, 120, 255, 0.15) !important;
}

/* ── Main content padding ── */
[data-testid="stMain"] { padding-top: 0 !important; }
.main .block-container {
    padding: 2rem 3rem 3rem 3rem !important;
    max-width: 1100px !important;
    position: relative;
    z-index: 1;
}

/* ── Hero Header ── */
.hero-wrap {
    position: relative;
    margin-bottom: 2.5rem;
    padding: 3rem 3rem 2.8rem 3rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #001533 0%, #002755 50%, #001f45 100%);
    border: 1px solid rgba(0, 160, 255, 0.22);
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0, 140, 255, 0.20) 0%, transparent 70%);
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0, 80, 200, 0.15) 0%, transparent 70%);
}
.hero-badge {
    display: inline-block;
    padding: 5px 14px;
    background: rgba(0, 140, 255, 0.15);
    border: 1px solid rgba(0, 180, 255, 0.30);
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #60c0ff;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(1.5rem, 3vw, 2.4rem);
    font-weight: 800;
    line-height: 1.2;
    color: #ffffff;
    margin: 0 0 1rem 0;
    background: linear-gradient(135deg, #ffffff 30%, #7cc8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.98rem;
    font-weight: 400;
    color: #7aaed4;
    line-height: 1.7;
    max-width: 780px;
    margin: 0;
    text-align: justify;
}

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 160, 255, 0.40), transparent);
    margin: 0.8rem 0 2rem 0;
    border: none;
}

/* ── Section Cards ── */
.section-card {
    background: linear-gradient(135deg, #001228 0%, #001a38 100%);
    border: 1px solid rgba(0, 130, 220, 0.18);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.section-card:hover {
    border-color: rgba(0, 160, 255, 0.35);
    box-shadow: 0 0 30px rgba(0, 120, 255, 0.10);
}
.section-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #0090ff, #0040aa);
    border-radius: 4px 0 0 4px;
}

/* ── Section Heading ── */
.section-heading {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #4fb3ff;
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    letter-spacing: 0.01em;
}
.section-icon {
    width: 30px; height: 30px;
    border-radius: 8px;
    background: rgba(0, 140, 255, 0.15);
    border: 1px solid rgba(0, 160, 255, 0.25);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

/* ── Body Text ── */
.body-text {
    font-size: 0.94rem;
    line-height: 1.85;
    color: #96c4e8;
    text-align: justify;
    margin: 0;
}

/* ── Goal List ── */
.goal-list {
    list-style: none;
    padding: 0; margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}
.goal-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    font-size: 0.94rem;
    line-height: 1.7;
    color: #96c4e8;
}
.goal-dot {
    flex-shrink: 0;
    margin-top: 0.35rem;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0090ff, #00d4ff);
    box-shadow: 0 0 8px rgba(0, 180, 255, 0.50);
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.6rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1;
    min-width: 150px;
    background: linear-gradient(135deg, #001228 0%, #001a38 100%);
    border: 1px solid rgba(0, 130, 220, 0.20);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(0, 140, 255, 0.10) 0%, transparent 70%);
    pointer-events: none;
}
.stat-num {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff, #60c0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.stat-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #5a90b8;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Method Pills ── */
.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.pill-blue {
    background: rgba(0, 100, 220, 0.18);
    border: 1px solid rgba(0, 140, 255, 0.30);
    color: #70c0ff;
}
.pill-cyan {
    background: rgba(0, 180, 220, 0.13);
    border: 1px solid rgba(0, 200, 240, 0.25);
    color: #60d4ff;
}

/* ── Hide default Streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.stDeployButton { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #010c1a; }
::-webkit-scrollbar-thumb { background: rgba(0, 120, 220, 0.40); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0, 160, 255, 0.60); }
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🌊 Sistem Klasterisasi Bencana</div>
    <h1 class="hero-title">Aplikasi Klasterisasi Wilayah<br>Terdampak Banjir di Indonesia</h1>
    <p class="hero-sub">
        Mengelompokkan provinsi di Indonesia berdasarkan indikator dampak banjir menggunakan metode
        HDBSCAN (<em>Hierarchical Density-Based Spatial Clustering of Applications with Noise</em>)
        yang dikombinasikan dengan <em>Bayesian Optimization</em> untuk menghasilkan klasterisasi yang akurat dan andal.
    </p>
    <div class="pill-row">
        <span class="pill pill-blue">⚙️ HDBSCAN</span>
        <span class="pill pill-blue">🔧 Bayesian Optimization</span>
        <span class="pill pill-cyan">🗺️ Peta Interaktif</span>
        <span class="pill pill-cyan">📊 34 Provinsi</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-num">34</div>
        <div class="stat-label">Provinsi Indonesia</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">2024</div>
        <div class="stat-label">Data Terkini</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">HDBSCAN</div>
        <div class="stat-label">Metode Utama</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">BO</div>
        <div class="stat-label">Optimasi Parameter</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LATAR BELAKANG ─────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <h2 class="section-heading">
        <span class="section-icon">📋</span>
        Latar Belakang
    </h2>
    <p class="body-text">
        Banjir merupakan salah satu bencana alam yang paling sering terjadi di Indonesia dengan ribuan kejadian setiap 
        tahunnya yang menimbulkan dampak signifikan terhadap kerusakan infrastruktur dan gangguan aktivitas sosial masyarakat. 
        Pada tahun 2024, banjir tercatat sebagai bencana alam yang paling dominan terjadi di Indonesia, disertai peningkatan 
        jumlah korban dan kerusakan dibandingkan dengan tahun-tahun sebelumnya. Kondisi ini menunjukkan bahwa upaya mitigasi 
        bencana banjir di Indonesia masih belum dilakukan secara optimal dan membutuhkan pendekatan yang lebih efektif berbasis data.
    </p>
    <br>
    <p class="body-text">
        Di sisi lain, karakteristik dampak banjir di setiap provinsi di Indonesia cenderung berbeda-beda karena dipengaruhi oleh 
        kondisi geografis, lingkungan, maupun sosial ekonomi. Oleh karena itu, diperlukan suatu sistem yang mampu mengidentifikasi 
        pola dampak banjir dan mengelompokkan provinsi di Indonesia berdasarkan tingkat keparahan dampaknya. Aplikasi ini 
        dikembangkan dengan memanfaatkan metode HDBSCAN yang dikombinasikan dengan <em>Bayesian Optimization</em> untuk menghasilkan 
        klasterisasi yang lebih akurat. Aplikasi ini mampu menyajikan hasil klasterisasi dalam bentuk visualisasi interaktif 
        sehingga memudahkan pengguna dalam memahami distribusi tingkat keparahan dampak banjir serta mendukung pengambilan 
        keputusan dalam upaya mitigasi bencana secara lebih tepat sasaran.
    </p>
</div>
""", unsafe_allow_html=True)

# ── TUJUAN ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <h2 class="section-heading">
        <span class="section-icon">🎯</span>
        Tujuan
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
