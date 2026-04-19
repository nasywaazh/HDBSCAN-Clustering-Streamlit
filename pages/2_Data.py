import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Data Indikator",
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
    font-size: 3rem;
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
    margin-bottom: 1.2rem;
    overflow: hidden;
}
.section-header {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border-bottom: 1px solid #d4e8f8;
    padding: 1rem 1.7rem;
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
    font-size: 1.3rem;
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
    font-size: 1rem;
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
[data-testid="stFileUploader"]:hover { border-color: #1976d2; }
[data-testid="stFileUploader"] label {
    color: #1565c0 !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

/* SAFE TABLE */
.safe-table-wrap {
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid #d4e8f8;
    margin-bottom: 1rem;
}
.safe-table-wrap table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #ffffff;
}
.safe-table-wrap thead tr {
    background: linear-gradient(135deg, #e3f2fd, #eff8ff);
}
.safe-table-wrap th {
    padding: 0.6rem 0.9rem;
    text-align: left;
    font-weight: 700;
    color: #1565c0;
    border-bottom: 1px solid #d4e8f8;
    white-space: nowrap;
}
.safe-table-wrap td {
    padding: 0.5rem 0.9rem;
    color: #1a3a5c;
    border-bottom: 1px solid #eaf4fc;
}
.safe-table-wrap tr:last-child td { border-bottom: none; }
.safe-table-wrap tr:hover td { background: #f0f9ff; }

[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# HELPERS
def safe_table(df_show, max_rows=500):
    df_render = df_show.head(max_rows).reset_index(drop=True)
    headers = "".join(f"<th>{col}</th>" for col in df_render.columns)
    rows = ""
    for _, row in df_render.iterrows():
        cells = "".join(
            f"<td>{round(val, 4) if isinstance(val, float) else val}</td>"
            for val in row.values
        )
        rows += f"<tr>{cells}</tr>"
    html = (
        '<div class="safe-table-wrap">'
        "<table>"
        f"<thead><tr>{headers}</tr></thead>"
        f"<tbody>{rows}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
    if len(df_show) > max_rows:
        st.caption(f"⚠️ Menampilkan {max_rows} dari {len(df_show)} baris")


def section_header(icon, title):
    st.markdown(f"""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">{icon}</div>
            <h2 class="section-title">{title}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)


# GUARD SESSION
def wait_for_session(max_retries=3):
    for _ in range(max_retries):
        try:
            _ = st.session_state.get("_session_ready", False)
            st.session_state["_session_ready"] = True
            return True
        except Exception:
            time.sleep(0.3)
    return False

if not wait_for_session():
    st.error("Sesi belum siap, silakan refresh halaman!")
    st.stop()


# PAGE HEADER
st.markdown("""
<div class="page-header">
    <h1 class="page-title">DATA INDIKATOR DAMPAK BANJIR</h1>
    <p class="page-sub">
        Pengguna mengunggah dataset dengan format file CSV atau Excel terlebih dahulu
        sebelum menjalankan proses klasterisasi
    </p>
    <div class="badge-row">
        <div class="badge-pill"><span class="badge-icon">📂</span> Upload Data</div>
        <div class="badge-pill"><span class="badge-icon">🔍</span> Eksplorasi Data</div>
    </div>
</div>
""", unsafe_allow_html=True)


# UPLOAD SECTION
section_header("📂", "Upload Dataset")

uploaded_file = st.file_uploader(
    "Format file CSV atau Excel",
    type=["csv", "xlsx"],
    label_visibility="visible"
)

# CONTENT
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File telah berhasil diupload!")

        # INFORMASI DATA
        section_header("🔍", "Informasi Dataset")

        n_obs     = df.shape[0]
        n_var     = df.shape[1]
        n_missing = int(df.isnull().sum().sum())
        n_dup     = int(df.duplicated().sum())

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

        st.markdown("<div style='margin-bottom:1.6rem;'></div>", unsafe_allow_html=True)

        # PREVIEW DATA
        section_header("🔍", "Preview Dataset")
        safe_table(df)

        # TIPE DATA
        section_header("🔍", "Tipe Dataset")
        dtype_df = df.dtypes.reset_index()
        dtype_df.columns = ["Nama Variabel", "Tipe Data"]
        dtype_df["Tipe Data"] = dtype_df["Tipe Data"].astype(str)
        safe_table(dtype_df)

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
                Silakan upload file terlebih dahulu
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
