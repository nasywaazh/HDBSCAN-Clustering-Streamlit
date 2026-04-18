import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Indikator Dampak Banjir",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ─────────────────────────────────────────────
if "data_uploaded" not in st.session_state:
    st.session_state["data_uploaded"] = False

if "data" not in st.session_state:
    st.session_state["data"] = None


# ── STYLE ─────────────────────────────────────────────────────
st.markdown(""" 
<style>
body { font-family: 'Plus Jakarta Sans', sans-serif; }

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
}
.section-title {
    font-size: 1rem;
    font-weight: 800;
    color: #1565c0;
}

/* METRIC */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}
.metric-card {
    background: #e8f4fd;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #1565c0;
}
</style>
""", unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────
st.title("DATA INDIKATOR DAMPAK BANJIR")


# ── UPLOAD SECTION ────────────────────────────────────────────
if not st.session_state["data_uploaded"]:

    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">📂</div>
            <h2 class="section-title">Upload Dataset</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.9rem; color:#3d6b8e;">
    Upload file terlebih dahulu sebelum menjalankan proses klasterisasi.
    </p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Format file CSV atau Excel",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state["data"] = df
            st.session_state["data_uploaded"] = True
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {e}")


# ── DATA DISPLAY ──────────────────────────────────────────────
if st.session_state["data_uploaded"]:

    df = st.session_state["data"]

    st.success("✅ Dataset berhasil diupload!")

    # tombol reset
    if st.button("🔄 Upload Ulang Dataset"):
        st.session_state["data_uploaded"] = False
        st.session_state["data"] = None
        st.rerun()

    # ── INFORMASI DATA ─────────────────────────
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">📊</div>
            <h2 class="section-title">Informasi Data</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    n_obs = df.shape[0]
    n_var = df.shape[1]
    n_missing = df.isnull().sum().sum()
    n_dup = df.duplicated().sum()

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p>Observasi</p>
            <p class="metric-value">{n_obs}</p>
        </div>
        <div class="metric-card">
            <p>Variabel</p>
            <p class="metric-value">{n_var}</p>
        </div>
        <div class="metric-card">
            <p>Missing</p>
            <p class="metric-value">{n_missing}</p>
        </div>
        <div class="metric-card">
            <p>Duplikat</p>
            <p class="metric-value">{n_dup}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PREVIEW ────────────────────────────────
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">👁️</div>
            <h2 class="section-title">Preview Data</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True)

    # ── TIPE DATA ─────────────────────────────
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">🔍</div>
            <h2 class="section-title">Tipe Data Variabel</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    dtype_df = df.dtypes.reset_index()
    dtype_df.columns = ["Nama Variabel", "Tipe Data"]

    st.dataframe(dtype_df, use_container_width=True)
