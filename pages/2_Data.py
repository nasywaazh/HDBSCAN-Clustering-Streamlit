import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Indikator Dampak Banjir",
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

/* PAGE HEADER */
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
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    cursor: default;
    user-select: none;
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

/* SECTION CARD */
.section-card {
    background: #ffffff;
    border: 1px solid #d4e8f8;
    border-radius: 18px;
    margin-bottom: 1.4rem;
    overflow: hidden;
}
.section-header {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border-bottom: 1px solid #d4e8f8;
    padding: 1rem 1.6rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #1565c0, #0288d1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.section-title {
    font-size: 1rem;
    font-weight: 800;
    color: #1565c0;
    margin: 0;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.section-body {
    padding: 1.4rem 1.6rem;
}

/* METRIC CARDS */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}
.metric-card {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f9ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #7bafd4;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #1565c0;
    line-height: 1;
    margin: 0;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: #f7fbff;
    border: 2px dashed #90caf9;
    border-radius: 14px;
    padding: 0.5rem;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #1976d2;
}
[data-testid="stFileUploader"] label {
    color: #1565c0 !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #d4e8f8 !important;
}

/* ALERT BOXES */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* SUCCESS / INFO / ERROR */
div[data-baseweb="notification"] {
    border-radius: 12px !important;
}

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
    <h1 class="page-title">DATA INDIKATOR DAMPAK BANJIR</h1>
    <p class="page-sub">
        Pengguna mengunggah data indikator dampak banjir sebelum melakukan proses klasterisasi.
    </p>
    <div class="badge-row">
        <div class="badge-pill"><span class="badge-icon">📂</span> Upload Data</div>
        <div class="badge-pill"><span class="badge-icon">📊</span> Eksplorasi Data</div>
    </div>
</div>
""", unsafe_allow_html=True)

# UPLOAD SECTION
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon">📂</div>
        <h2 class="section-title">Upload Dataset</h2>
    </div>
    <div class="section-body">
        <p style="
            font-size: 0.9rem;
            color: #3d6b8e;
            margin-bottom: 0.8rem;
            line-height: 1.6;
        ">
        Upload file terlebih dahulu!
        </p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Format file CSV atau Excel",
    type=["csv", "xlsx"],
    label_visibility="visible"
)

st.markdown("</div></div>", unsafe_allow_html=True)

# CONTENT
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"File **{uploaded_file.name}** berhasil diupload!")

        # INFORMASI DATA
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <h2 class="section-title">Informasi Data</h2>
            </div>
            <div class="section-body">
        """, unsafe_allow_html=True)

        n_obs      = df.shape[0]
        n_var      = df.shape[1]
        n_missing  = int(df.isnull().sum().sum())
        n_dup      = int(df.duplicated().sum())

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <p class="metric-label">Jumlah Observasi</p>
                <p class="metric-value">{n_obs:,}</p>
            </div>
            <div class="metric-card">
                <p class="metric-label">Jumlah Variabel</p>
                <p class="metric-value">{n_var:,}</p>
            </div>
            <div class="metric-card">
                <p class="metric-label">Missing Values</p>
                <p class="metric-value">{n_missing:,}</p>
            </div>
            <div class="metric-card">
                <p class="metric-label">Data Duplikat</p>
                <p class="metric-value">{n_dup:,}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # PREVIEW DATA
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <h2 class="section-title">Preview Data</h2>
            </div>
            <div class="section-body">
        """, unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # TIPE DATA
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <div class="section-icon">🔍</div>
                <h2 class="section-title">Tipe Data Variabel</h2>
            </div>
            <div class="section-body">
        """, unsafe_allow_html=True)

        dtype_df = df.dtypes.reset_index()
        dtype_df.columns = ["Nama Variabel", "Tipe Data"]
        dtype_df["Tipe Data"] = dtype_df["Tipe Data"].astype(str)
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Simpan ke session state
        st.session_state["data"] = df

    except Exception as e:
        st.error(f"Terjadi error saat membaca file: {e}")

else:
    st.markdown("""
    <div class="section-card">
        <div class="section-body" style="text-align:center; padding: 2.5rem 1.6rem; color: #7bafd4;">
            <div style="font-size:3rem; margin-bottom:0.8rem;">📁</div>
            <p style="font-size:0.95rem; font-weight:600; color:#1976d2; margin:0 0 0.3rem 0;">
                Belum ada data yang diupload
            </p>
            <p style="font-size:0.85rem; margin:0; color:#7bafd4;">
                Silahkan upload file CSV atau Excel terlebih dahulu
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
