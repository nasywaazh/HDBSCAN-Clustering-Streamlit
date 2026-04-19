import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Peta Klasterisasi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# STYLE (SAMA DENGAN HALAMAN LAIN)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1a3a5c;
}

.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1080px !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #d0e4f7 !important;
}
[data-testid="stSidebar"] * { color: #1a5fa8 !important; }

#MainMenu, footer, header { visibility: hidden; }

/* HEADER */
.page-header {
    background: linear-gradient(135deg, #1565c0, #0288d1);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.page-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: white;
}
.page-sub {
    color: #bbdefb;
}

/* CARD */
.section-card {
    background: #ffffff;
    border: 1px solid #d4e8f8;
    border-radius: 16px;
    margin-bottom: 1rem;
}
.section-body {
    padding: 1.2rem 1.4rem;
}

/* METRIC */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
.metric-card {
    background: linear-gradient(135deg, #e8f4fd, #f0f9ff);
    border: 1px solid #c2dff5;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: #7bafd4;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1565c0;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPER
# =========================================================
def section(title):
    st.markdown(f"""
    <div class="section-card">
        <div class="section-body">
            <h3 style="color:#1565c0">{title}</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_html(items):
    cards = "".join(
        f'<div class="metric-card">'
        f'<p class="metric-label">{l}</p>'
        f'<p class="metric-value">{v}</p>'
        f'</div>'
        for l, v in items
    )
    st.markdown(f'<div class="metric-grid">{cards}</div>', unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="page-header">
    <h1 class="page-title">PETA KLASTERISASI BANJIR</h1>
    <p class="page-sub">
        Visualisasi geografis hasil klasterisasi wilayah terdampak banjir di Indonesia
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# VALIDASI DATA
# =========================================================
if "df_clustered" not in st.session_state:
    st.warning("Silakan lakukan klasterisasi terlebih dahulu!")
    st.stop()

df_result = st.session_state["df_clustered"].copy()

# =========================================================
# METRIC
# =========================================================
n_prov = df_result.shape[0]
n_cluster = len(set(df_result["Cluster"])) - (1 if -1 in df_result["Cluster"] else 0)
n_noise = (df_result["Cluster"] == -1).sum()

metric_html([
    ("Jumlah Provinsi", n_prov),
    ("Jumlah Klaster", n_cluster),
    ("Jumlah Noise", n_noise)
])

# =========================================================
# DATA TAMBAHAN
# =========================================================
df_result["label_klaster"] = df_result["Cluster"].apply(
    lambda x: "Noise" if x == -1 else f"Klaster {x}"
)

numeric_cols = df_result.select_dtypes(include=np.number).columns.drop("Cluster")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Peta")

    map_style = st.selectbox(
        "Gaya Peta",
        ["carto-positron", "carto-darkmatter", "open-street-map"]
    )

    selected_hover = st.multiselect(
        "Informasi Hover",
        options=numeric_cols,
        default=numeric_cols[:3]
    )

# =========================================================
# LOAD GEOJSON
# =========================================================
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    with urlopen(url) as response:
        return json.load(response)

geojson = load_geojson()

# =========================================================
# MAP SECTION
# =========================================================
section("Visualisasi Peta Klasterisasi")

fig = px.choropleth_mapbox(
    df_result,
    geojson=geojson,
    locations=df_result.index,
    color="label_klaster",
    hover_name="Provinsi",
    mapbox_style=map_style,
    zoom=3.8,
    center={"lat": -2.5, "lon": 118},
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DETAIL
# =========================================================
section("Detail Informasi Provinsi")

selected_prov = st.selectbox(
    "Pilih Provinsi",
    sorted(df_result["Provinsi"])
)

prov_data = df_result[df_result["Provinsi"] == selected_prov].iloc[0]

st.markdown(f"### {prov_data['label_klaster']}")

cols = st.columns(3)
for i, col in enumerate(numeric_cols):
    cols[i % 3].metric(
        label=col,
        value=f"{prov_data[col]:,.0f}"
    )

# =========================================================
# DOWNLOAD
# =========================================================
section("Download Hasil")

csv = df_result.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download CSV",
    csv,
    "hasil_klasterisasi.csv",
    "text/csv"
)
